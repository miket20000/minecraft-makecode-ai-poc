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
