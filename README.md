# Minecraft Education + MakeCode + external API transport PoC

This repository tests one narrow question: can a program running from
Minecraft Education Code Builder call an external Echo API and use its
response in the Minecraft world?

The project deliberately contains no AI provider integration, credentials,
Behavior Pack, Resource Pack, custom PXT target, or production gateway.

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

## Result

`NO-GO`: no tested in-scope mechanism provided
`Minecraft Education -> API -> Minecraft Education`. See `REPORT.md` for the
per-environment results and observed limitations. Results are recorded per
immutable Git commit and earlier failures remain part of the evidence.

Candidate commits:

- `88f5a93`: local Identity control;
- `0135609`: direct `fetch()` / `pxt.Util.requestAsync()` probe;
- `47c67da` and cache-distinct `8ca7925`: simulator-side shim probe;
- `017d4ee`: Editor Extension manifest probe.

## Companion `/connect` probe

The continuation PoC first tests Minecraft Education's native `/connect`
(`wsserver`) command against `companion_ws_probe.py`. The probe listens only on
the selected local address, records the WebSocket handshake and messages, and
does not issue Minecraft commands.
