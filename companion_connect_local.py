#!/usr/bin/env python3
"""Minimal event-to-command round-trip over Minecraft Education /connect."""

import argparse
import asyncio
import json
import uuid
from datetime import datetime, timezone

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
            "version": 1,
            "requestId": str(uuid.uuid4()),
            "messageType": "commandRequest",
            "messagePurpose": purpose,
        },
        "body": body,
    }


async def send_packet(connection, purpose, body):
    message = packet(purpose, body)
    await connection.send(json.dumps(message, separators=(",", ":")))
    emit(
        "sent",
        purpose=purpose,
        request_id=message["header"]["requestId"],
        body=body,
    )


def player_message(message):
    header = message.get("header", {})
    body = message.get("body", {})
    properties = body.get("properties", {})
    event_name = header.get("eventName") or body.get("eventName")
    if event_name != "PlayerMessage":
        return None
    return (
        properties.get("Message")
        or properties.get("message")
        or body.get("message")
    )


async def handle(connection):
    emit(
        "websocket_connected",
        local=list(connection.local_address),
        remote=list(connection.remote_address),
        path=connection.request.path,
        selected_subprotocol=connection.subprotocol,
    )
    await send_packet(connection, "subscribe", {"eventName": "PlayerMessage"})
    await send_packet(
        connection,
        "commandRequest",
        {
            "version": 1,
            "commandLine": "say CONNECT_LOCAL_OK",
            "origin": {"type": "player"},
        },
    )
    count = 0
    try:
        async for raw in connection:
            count += 1
            if not isinstance(raw, str):
                emit("received", number=count, kind="binary", length=len(raw))
                continue
            emit("received", number=count, kind="text", payload=raw)
            try:
                message = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if player_message(message) == "companion hello":
                await send_packet(
                    connection,
                    "commandRequest",
                    {
                        "version": 1,
                        "commandLine": "say hello",
                        "origin": {"type": "player"},
                    },
                )
    except ConnectionClosed as error:
        emit("websocket_closed", messages=count, code=error.code, reason=error.reason)


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
