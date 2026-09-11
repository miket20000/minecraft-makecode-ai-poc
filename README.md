# Minecraft Education + MakeCode + external API transport PoC

This repository tests one narrow question: can a program running from
Minecraft Education Code Builder call an external Echo API and use its
response in the Minecraft world?

The project deliberately contains no AI provider integration, credentials,
Resource Pack, custom PXT target, or production gateway. A data-only Behavior
Pack skeleton exists from an earlier candidate commit, but the operator stopped
the current scope before any pack was installed or tested.

## Candidate 1: Identity

Import this repository as a Minecraft MakeCode Extension. It exposes category
`AI` and block `AI zapytaj [tekst]` backed by `AI.ask(text: string): string`.
For the Identity candidate it simply returns its argument.

Student program:

```typescript
player.onChat("ai", function () {
    player.say(AI.ask("hello"))
})
```

Typing `ai` in Minecraft must display `hello`. This validates extension import
and runtime execution only; it is not evidence of HTTP transport.

## Echo API

Run with Python 3 and the exact observed MakeCode runtime origin:

```text
python echo_server.py --origin https://trg-minecraft.userpxt.io
```

The server listens only on `127.0.0.1:8765` and implements `POST /echo` plus
the minimal CORS preflight required by the PoC.

For the Companion loopback PoC, `--origin none` is sufficient because Python
does not send a browser `Origin` header. Both servers also accept an optional
`--log-path` for the Windows active-session launch used in the measurement.

## Result

`PASS-COMPANION-CONNECT`: the MakeCode-only path remains `NO-GO`, but the
encrypted local Companion completed
`Minecraft -> Companion -> Echo API -> Companion -> Minecraft` in the real
world. See `REPORT.md` for the per-candidate results and observed limitations.
Earlier failures remain part of the evidence.

Candidate commits:

- `88f5a93`: local Identity control;
- `0135609`: direct `fetch()` / `pxt.Util.requestAsync()` probe;
- `47c67da` and cache-distinct `8ca7925`: simulator-side shim probe;
- `017d4ee`: Editor Extension manifest probe.
- `fca927a`: encrypted local Minecraft <-> Companion round-trip;
- `66c22d9`: complete encrypted Companion + Echo API round-trip.

## Companion `/connect` probe

The continuation PoC first tests Minecraft Education's native `/connect`
(`wsserver`) command against `companion_ws_probe.py`. The probe listens only on
the selected local address, records the WebSocket handshake and messages, and
does not issue Minecraft commands.

`companion_ws_subprotocol.py` is a separate candidate that additionally
negotiates the single subprotocol offered by Minecraft Education:
`com.microsoft.minecraft.wsencrypt`. It still performs no encryption exchange
or command processing; its purpose is to identify the first application
message and the minimum remaining protocol boundary.

`companion_connect_local.py` is the next immutable candidate. It sends one
`PlayerMessage` subscription and one `say CONNECT_LOCAL_OK` request, then maps
the exact player chat message `companion hello` to `say hello`. This is the
smallest event-to-command check before adding Echo HTTP.

`companion_connect_encrypted.py` is the operator-authorized encrypted
candidate. It implements only the required P-384 ECDH exchange and the
AES-256-CFB8 session used by `com.microsoft.minecraft.wsencrypt`, then repeats
the same one-event/one-command round-trip. Its two pinned Python dependencies
are listed in `requirements-companion.txt`.

Minimal Windows PoC commands:

```text
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-companion.txt
.venv\Scripts\python echo_server.py --origin none
.venv\Scripts\python companion_connect_encrypted.py
```

Then, in Minecraft Education:

```text
/connect 127.0.0.1:19131/ws
companion echo hello
```

The final line must produce an Echo `POST`, an encrypted `/say hello`, a game
event, and a successful command response. The implementation is a transport
PoC, not a production security or lifecycle design.

## Untested Behavior Pack control

`behavior_pack` is the earlier data-only skeleton. It was not installed or run
because the operator explicitly ended this iteration after Companion.
