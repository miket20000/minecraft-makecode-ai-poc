# Transport PoC report

## Result

`PASS-COMPANION-CONNECT`

The previous MakeCode-only result remains `NO-GO`. A separate encrypted local
Companion established the required real-world round-trip on
`student-l-wm66` with Minecraft Education `1.26.4501.0`.

## Working flow

```text
Minecraft Education player chat: companion echo hello
  -> /connect 127.0.0.1:19131/ws
  -> com.microsoft.minecraft.wsencrypt
  -> Companion (P-384 ECDH, AES-256-CFB8)
  -> POST http://127.0.0.1:8765/echo {"text":"hello"}
  -> 200 {"text":"hello"}
  -> encrypted /say hello
  -> Minecraft event + commandResponse statusCode=0
```

The final transport candidate is commit `66c22d9`. No AI provider, credential,
Behavior Pack, Resource Pack, custom PXT target, or production gateway was
used.

## Tested variants

| Variant | Result | Technical reason/evidence |
| --- | --- | --- |
| MakeCode Extension -> HTTP | `NO-GO` | Previous stage: direct HTTP did not compile/load, the simulator shim never completed or reached Echo, and the target rejected the Editor Extension probe. |
| `/connect` availability | `AVAILABLE` | On real Minecraft Education `1.26.3200.0` on `mt`, both `/help connect` and `/help wsserver` returned the `wsserver (also connect)` usage. |
| `/connect` WebSocket handshake without subprotocol (`0828516`) | `FAIL` application session | TCP/WebSocket v13 connected from loopback, then Minecraft closed it and displayed `Could not connect to server`. |
| `/connect` encrypted subprotocol (`0a50cac`) | `PASS` handshake | Negotiating `com.microsoft.minecraft.wsencrypt` kept the socket open and Minecraft displayed `Connection established`. |
| Plaintext `/connect` round-trip (`7e0b4f6`) | `FAIL` | Minecraft returned `-2147418107`, `Encrypted session required`; no command effect appeared. |
| First encrypted command (`d6605a3`) | `FAIL` full round-trip / partial outbound `PASS` | P-384/AES-256-CFB8 command displayed `CONNECT_ENCRYPTED_OK` on `mt`, but the first inbound transition frame was incorrectly treated as encrypted and failed UTF-8 decoding. |
| Encrypted transition probe (`5a87569`) | `FAIL` full round-trip | It accepted the single plaintext transition frame and decrypted later traffic. The real player message used current `body.message`, not historical `body.properties.Message`, so the trigger was not recognized at that SHA. |
| Encrypted Minecraft <-> Companion (`fca927a`) | `PASS-CONNECT-LOCAL` | `companion hello` arrived as an encrypted event; Companion sent encrypted `/say hello`; Minecraft emitted the resulting event and returned `statusCode=0`. |
| Companion + Echo API (`66c22d9`) | `PASS-COMPANION-CONNECT` | Independent Echo contract passed. The Minecraft event triggered a second `POST /echo` 200; response length 5 was sent as encrypted `/say hello`; Minecraft returned the corresponding event and `statusCode=0`. |
| Behavior Pack | `NOT TESTED` | Operator stopped scope after the Companion stage. The previously committed data-only skeleton was not installed or run. |
| Pack direct HTTP | `NOT TESTED` | Operator stopped scope after the Companion stage. |
| Pack + Companion | `NOT TESTED` | Operator stopped scope after the Companion stage. |

## Previous MakeCode result preserved

- Identity `88f5a93`: category/block and local `hello` worked in Code Builder
  and the real Minecraft world, proving Extension execution only.
- Direct HTTP `0135609`: exact-SHA project was rejected as an Extension error;
  no Echo request was made.
- Simulator shim `8ca7925` (transport code from `47c67da`): imported and
  started, but the call did not return and no request reached Echo.
- Editor Extension `017d4ee`: no target permission/allowlist, `Editor` button,
  or iframe, and therefore no return channel to Minecraft.
- Standalone MakeCode remained `BLOCKED` as transport evidence because it had
  no connected real-world Minecraft result channel.

## Observed limitations

- The successful flow requires the user to issue `/connect
  127.0.0.1:19131/ws`. The PoC did not automate this command.
- Microsoft's command contract marks `/wsserver`/`/connect` as Admin-only and
  requiring cheats. Both tested worlds permitted the command; the rejection
  behavior for a lower-permission student was not measured.
- The tested client required `com.microsoft.minecraft.wsencrypt`; plaintext
  command traffic was explicitly rejected. The implemented session uses P-384
  ECDH, a SHA-256 derived key, and stateful AES-256-CFB8 in both directions.
- After the `ws:encrypt` response, Minecraft sends one additional plaintext
  transition frame before encrypted responses. The Companion must accept that
  exact transition.
- Minecraft Education `1.26.4501.0` emits `PlayerMessage` text directly as
  `body.message`; relying only on the historical nested `properties` shape
  misses player input.
- The minimal Windows runtime used Python 3.13.3 plus pinned `cryptography
  45.0.7` and `websockets 17.0`. The Companion and Echo bound only to
  `127.0.0.1`; LAN and `wss://` were not measured.
- The PoC Companion has no authentication and is intentionally loopback-only.
  It contains no provider key or other secret.
- On `student-l-wm66`, the protected WinApp v0.6.0 bridge could control the
  Minecraft window, but a window-only screenshot of its OGLES surface was
  entirely black. Minecraft F2 created no image file. `--capture-screen` was
  not used because it could include other applications. The successful
  command is instead proven by the correlated encrypted game event and
  `commandResponse statusCode=0`; an earlier real-game screenshot from `mt`
  visibly shows the encrypted `CONNECT_ENCRYPTED_OK` command.
- The successful client version on `student-l-wm66` was `1.26.4501.0`; the
  availability and earlier encryption diagnostics on `mt` used
  `1.26.3200.0`.

The following were not measured and must not be inferred from this PoC:
Code Builder coexistence, multiple simultaneous WebSocket connections, LAN
connections, reconnection after a Minecraft restart, or programmatic
invocation of `/connect`.

## Test execution notes

- One WinApp helper used invalid command names and issued no input; it was a
  tooling `BLOCKED`, not a candidate failure.
- On `mt`, keyboard focus drift once opened the existing
  `Wejście Agenta ClickOn` world. No command or movement was performed; it was
  immediately saved and exited, and later navigation used step-by-step
  screenshots to select the isolated PoC world.
- On `student-l-wm66`, the first background `Start-Process` listener ended
  with its SSH session. The existing protected active-session bridge was then
  used to launch the measured processes. The first final-candidate input was
  also `BLOCKED` by an already-open chat panel; after an explicit Esc, the
  exact `/connect` command produced the measured handshake.

## Recommended architecture

Use a small local Companion installed on each student computer:

```text
Minecraft Education
  -> manual /connect to loopback
  -> encrypted local Companion
  -> HTTPS GP AI Gateway
  -> encrypted command back to Minecraft
```

This is the simplest tested working boundary. For a production decision, the
manual connection step, lifecycle/reconnect behavior, local process
installation, gateway authentication, and the private-protocol maintenance
cost require an explicit design review. The local listener should remain
loopback-only; outbound gateway traffic should use HTTPS.

## Next step

The next minimal PoC, not implemented here, is:

```text
AI zapytaj [prompt]
  -> encrypted local Companion
  -> GP AI Gateway
  -> one test model
  -> structured response
  -> Minecraft message/action
```

No OpenAI, Gemini, Qwen, OpenRouter, or other model request was made.

## Evidence and cleanup

The evidence index is [`evidence/README.md`](evidence/README.md). It preserves
the earlier MakeCode `NO-GO`, every material `/connect` failure, the encrypted
transition diagnostics, `PASS-CONNECT-LOCAL`, and the complete Echo
round-trip. Ephemeral keys, salts, and player names are not retained in the
committed protocol logs.

Temporary Companion/Echo processes and ports were cleaned up after the final
readback; the exact runtime directories and test helpers created for this PoC
were removed from both Windows hosts and the GP hop.

## Versions and diagnostic sources

- Successful host: `student-l-wm66` (`L-WM66`), Minecraft Education
  `1.26.4501.0`, Python `3.13.3`, WinApp CLI `0.6.0` protected bridge.
- Initial host: `mt`, Minecraft Education `1.26.3200.0`.
- Minecraft MakeCode target: `2.1.27`; PXT: `12.1.17`.
- Microsoft `/wsserver` command documentation:
  <https://learn.microsoft.com/en-us/minecraft/creator/commands/commands/wsserver?view=minecraft-bedrock-stable>.
- Historical protocol reference used only to seed the minimal empirical probe:
  <https://github.com/Sandertv/mcwss>.
