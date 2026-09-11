# Minimal evidence index

- `identity-extension-block.png` — Code Builder shows category `AI` and block
  `AI zapytaj "hello"` for commit `88f5a93`.
- `identity-world-result.png` — the real Minecraft world shows `hello` after
  chat command `ai` for the local Identity control.
- `shim-world-result.png` — the real Minecraft world shows receipt of chat
  command `ai`, but no `hello` or `AI_ERROR`, for shim candidate `8ca7925`.
- `editor-probe-no-button.png` — the `AI` flyout for probe `017d4ee` contains
  only the ordinary block; there is no `Editor` button.
- `echo.log` — complete Echo server request log from the PoC. The only request
  was the independent PowerShell contract check; no runtime preflight or POST
  reached the server.

Screenshots were captured from Minecraft Education / Code Builder 1.26.3200.0
on `mt` with WinApp CLI.

## Native `/connect` continuation

- `connect-help-input.png` and `connect-help-result.png` — exact
  `/help connect` and the in-game alias/usage response.
- `wsserver-help-input.png` and `wsserver-help-result.png` — exact
  `/help wsserver` and the in-game response.
- `connect-path-input.png` and `connect-path-result.png` — exact
  `/connect 127.0.0.1:19131/ws` and the resulting in-game connection error.
- `connect-handshake-initial.log` — server-side loopback handshake evidence for
  candidate `0828516`; no application message arrived.
- `connect-subprotocol-input.png` and `connect-subprotocol-result.png` — exact
  `/connect 127.0.0.1:19131/ws` and in-game `Connection established` for
  candidate `0a50cac`.
- `connect-subprotocol.log` — WebSocket v13 handshake with offered and selected
  `com.microsoft.minecraft.wsencrypt`; the connection remained active.
- `connect-roundtrip-plaintext-input.png` and
  `connect-roundtrip-plaintext-result.png` — exact connection command and the
  established socket without a visible `CONNECT_LOCAL_OK` result.
- `connect-roundtrip-plaintext.log` — candidate `7e0b4f6` sent the smallest
  plaintext `PlayerMessage` subscription and `say CONNECT_LOCAL_OK`; Minecraft
  returned status `-2147418107`, `Encrypted session required`.
- `connect-settings-encryption.png` — General Settings after stopping the
  listener: WebSockets are enabled and the `Require Encrypted Websockets`
  control is unavailable (greyed out), so it was not changed for the PoC.
- `connect-encrypted-d6605a3-input.png` and
  `connect-encrypted-d6605a3-result.png` — exact `/connect` command and visible
  `CONNECT_ENCRYPTED_OK` emitted by the encrypted command from candidate
  `d6605a3`.
- `connect-encrypted-d6605a3.log` — sanitized protocol evidence: P-384 key
  agreement completed, AES-256-CFB8 outbound traffic reached Minecraft, but
  the first inbound frame failed UTF-8 decoding after decryption. Ephemeral
  public-key and salt values are deliberately not retained.
- `connect-encrypted-5a87569.log` — on `student-l-wm66`, the candidate accepted
  the one plaintext transition frame and then decrypted event and command
  responses. The player message arrived in `body.message`, so the historical
  `body.properties.Message` parser did not trigger the return command. This is
  retained as `FAIL` for the full round-trip at that SHA.
