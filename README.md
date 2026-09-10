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

See `REPORT.md`. Results are recorded per immutable Git commit and earlier
failures remain part of the evidence.
