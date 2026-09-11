#!/usr/bin/env python3
"""Minimal /connect WebSocket handshake and message probe."""

import argparse
import asyncio
import json
from datetime import datetime, timezone

from websockets.asyncio.server import serve


def emit(event, **fields):
    print(
        json.dumps(
            {"timestamp": datetime.now(timezone.utc).isoformat(), "event": event, **fields},
            ensure_ascii=False,
        ),
        flush=True,
    )


async def handle(connection):
    request = connection.request
    headers = request.headers
    emit(
        "websocket_connected",
        local=list(connection.local_address),
        remote=list(connection.remote_address),
        path=request.path,
        origin=headers.get("Origin"),
        user_agent=headers.get("User-Agent"),
        websocket_version=headers.get("Sec-WebSocket-Version"),
    )
    count = 0
    try:
        async for message in connection:
            count += 1
            if isinstance(message, str):
                emit("message", number=count, kind="text", payload=message)
            else:
                emit("message", number=count, kind="binary", length=len(message))
    finally:
        emit("websocket_closed", messages=count)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=19131)
    args = parser.parse_args()
    async with serve(handle, args.host, args.port):
        emit("listening", host=args.host, port=args.port)
        await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
