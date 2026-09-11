#!/usr/bin/env python3
"""Minimal encrypted Minecraft Education /connect round-trip."""

import argparse
import asyncio
import base64
import hashlib
import json
import os
import uuid
from datetime import datetime, timezone

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed


MINECRAFT_SUBPROTOCOL = "com.microsoft.minecraft.wsencrypt"


def emit(event, **fields):
    print(
        json.dumps(
            {"timestamp": datetime.now(timezone.utc).isoformat(), "event": event, **fields},
            ensure_ascii=False,
        ),
        flush=True,
    )


def packet(purpose, body):
    return {
        "header": {
            "requestId": str(uuid.uuid4()),
            "messagePurpose": purpose,
            "version": 1,
        },
        "body": body,
    }


def command_packet(command_line):
    return packet("commandRequest", {"version": 1, "commandLine": command_line})


def raw_base64(value):
    return base64.b64encode(value).decode("ascii").rstrip("=")


def decode_base64(value):
    return base64.b64decode(value + "=" * (-len(value) % 4))


async def send_json(connection, value, encryptor=None):
    data = json.dumps(value, separators=(",", ":")).encode("utf-8")
    encrypted = encryptor is not None
    if encrypted:
        data = encryptor.update(data)
        await connection.send(data, text=True)
    else:
        await connection.send(data.decode("utf-8"))
    emit(
        "sent",
        purpose=value["header"]["messagePurpose"],
        request_id=value["header"]["requestId"],
        encrypted=encrypted,
        command=value.get("body", {}).get("commandLine"),
        event_name=value.get("body", {}).get("eventName"),
    )


async def receive_json(connection, decryptor=None):
    raw = await connection.recv(decode=False)
    if isinstance(raw, str):
        raw = raw.encode("utf-8")
    encrypted = decryptor is not None
    if encrypted:
        raw = decryptor.update(raw)
    value = json.loads(raw.decode("utf-8"))
    emit(
        "received",
        purpose=value.get("header", {}).get("messagePurpose"),
        request_id=value.get("header", {}).get("requestId"),
        encrypted=encrypted,
        status_code=value.get("body", {}).get("statusCode"),
        status_message=value.get("body", {}).get("statusMessage"),
        event_name=(
            value.get("header", {}).get("eventName")
            or value.get("body", {}).get("eventName")
        ),
    )
    return value


def event_message(value):
    body = value.get("body", {})
    properties = body.get("properties", {})
    if isinstance(properties, str):
        properties = json.loads(properties)
    event_name = value.get("header", {}).get("eventName") or body.get("eventName")
    if event_name != "PlayerMessage":
        return None
    return properties.get("Message") or properties.get("message")


async def handle(connection):
    emit(
        "websocket_connected",
        local=list(connection.local_address),
        remote=list(connection.remote_address),
        path=connection.request.path,
        selected_subprotocol=connection.subprotocol,
    )

    try:
        name_request = command_packet("/getlocalplayername")
        await send_json(connection, name_request)
        name_response = await receive_json(connection)
        if name_response.get("body", {}).get("statusCode") != 0:
            raise RuntimeError("getlocalplayername failed")

        private_key = ec.generate_private_key(ec.SECP384R1())
        public_key = private_key.public_key().public_bytes(
            serialization.Encoding.DER,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        salt = os.urandom(16)
        enable_command = (
            f'/enableencryption "{raw_base64(public_key)}" '
            f'"{raw_base64(salt)}"'
        )
        enable_request = command_packet(enable_command)
        await send_json(connection, enable_request)
        enable_response = await receive_json(connection)
        body = enable_response.get("body", {})
        if body.get("statusCode") != 0 or not body.get("publicKey"):
            raise RuntimeError("enableencryption failed")

        client_key = serialization.load_der_public_key(
            decode_base64(body["publicKey"])
        )
        if not isinstance(client_key, ec.EllipticCurvePublicKey):
            raise RuntimeError("client returned a non-EC public key")
        shared_secret = private_key.exchange(ec.ECDH(), client_key)
        secret_key = hashlib.sha256(salt + shared_secret).digest()
        cipher = Cipher(algorithms.AES(secret_key), modes.CFB8(secret_key[:16]))
        encryptor = cipher.encryptor()
        decryptor = cipher.decryptor()
        emit("encryption_established", curve="P-384", cipher="AES-256-CFB8")

        await send_json(
            connection,
            packet("subscribe", {"eventName": "PlayerMessage"}),
            encryptor,
        )
        await send_json(
            connection,
            command_packet("/say CONNECT_ENCRYPTED_OK"),
            encryptor,
        )

        while True:
            message = await receive_json(connection, decryptor)
            if event_message(message) == "companion hello":
                emit("trigger", text="companion hello")
                await send_json(
                    connection,
                    command_packet("/say hello"),
                    encryptor,
                )
    except ConnectionClosed as error:
        emit("websocket_closed", code=error.code, reason=error.reason)
    except Exception as error:
        emit("session_error", error_type=type(error).__name__, message=str(error))
        await connection.close()


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=19131)
    args = parser.parse_args()
    async with serve(
        handle,
        args.host,
        args.port,
        subprotocols=[MINECRAFT_SUBPROTOCOL],
    ):
        emit("listening", host=args.host, port=args.port)
        await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
