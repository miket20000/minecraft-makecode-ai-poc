# Transport PoC report

## Result

`NO-GO`

## Working flow

No in-scope transport flow was established.

The control flow without transport did work:

```text
Minecraft Education -> ordinary MakeCode Extension (local identity) -> Minecraft Education
```

Neither tested ordinary Extension mechanism nor the Editor Extension probe
provided:

```text
Minecraft Education -> API -> Minecraft Education
```

## Tested variants

| Candidate | Standalone simulator | Code Builder | Minecraft world | Reason/evidence |
| --- | --- | --- | --- | --- |
| Echo API contract | n/a | n/a | PASS (PowerShell client on `mt`) | Port 8765 was initially free. `POST /echo` with `{"text":"hello"}` returned `{"text":"hello"}`. |
| Identity (`88f5a93`) | BLOCKED | PASS | PASS | Standalone had no Minecraft event/result channel. In Code Builder, category `AI` and block `AI zapytaj` were visible; chat command `ai` displayed `hello` in the Minecraft world. This proves Extension execution, not HTTP. |
| Direct HTTP (`0135609`) | BLOCKED | FAIL | FAIL | Exact-SHA project was rejected as an Extension error. Code Builder displayed `Looks like there are some errors in the extensions added to this project. How would you like to proceed?` on import and again on Start. No runnable Minecraft candidate and no Echo request resulted. |
| Simulator-side shim (`8ca7925`; transport code unchanged from `47c67da`) | BLOCKED | PASS | FAIL | Package imported and started in Code Builder. Minecraft received chat command `ai`, but produced neither `hello` nor `AI_ERROR`; Echo received no `OPTIONS` or `POST`. The shim did not provide a completed runtime call. |
| HTTPS fallback | NOT TESTED | NOT TESTED | NOT TESTED | Conditional test was not triggered: neither ordinary Extension mechanism issued any network request, so there was no evidence of a localhost-, mixed-content-, PNA-, or CORS-only block. |
| Editor Extension manifest probe (`017d4ee`) | n/a | FAIL | FAIL | The actual target had neither required target flag/allowlist nor an `Editor` button or iframe after importing the probe. Therefore no API call or return path to the running project existed. |

## Observed limitations

- Programmatic UIA value setting does not replace Monaco editor contents in
  this Code Builder build. The test used focused keyboard input and verified
  the resulting editor value before execution; this is a test-tool limitation,
  not an application failure.
- Code Builder reused the previously cached `88f5a93` dependency when the
  `0135609` URL search result was added normally. The exported project proved
  this by containing `github:miket20000/minecraft-makecode-ai-poc#88f5a93...`.
  That run was classified `BLOCKED`, then repeated with an imported project
  whose exported dependency was verified as `#0135609...`.
- For the exact Direct HTTP candidate, Code Builder exposed only its aggregate
  Extension-error message; it did not render individual compiler diagnostics.
- The loopback Echo API contract passed independently on Windows: port 8765
  was initially free and `POST /echo` returned `{"text":"hello"}`. Its log
  contained no request from the Direct HTTP candidate.
- The standard `//% promise shim=AI::ask` package with its implementation in
  `simFiles` loaded and the student program started, but the call never returned
  and the simulator-side file emitted no request to Echo. Code Builder exposed
  no runtime diagnostic for the stalled call.
- HTTPS was not tested because neither ordinary Extension mechanism reached
  the point of issuing an HTTP request; no evidence indicated a localhost,
  mixed-content, PNA, or CORS-only failure.
- The loaded target configuration returned no value for
  `appTheme.allowPackageExtensions` and no
  `packages.approvedEditorExtensionUrls`. The manifest probe loaded as an
  ordinary package but exposed no `Editor` button and loaded no Editor
  Extension iframe.
- Standalone MakeCode could run a blank project, but it had no connected
  Minecraft event/result channel. Exact project-file import through the CDP
  test path was not repeatable, so standalone transport results are
  `BLOCKED`, not product `FAIL`.

## Recommended architecture

There is no working architecture inside the approved constraints. The
simplest attempted architecture was an ordinary Extension, but the target did
not expose a usable HTTP mechanism to student/runtime code. The current
Minecraft target also did not admit the Editor Extension probe.

Choosing a transport would therefore require a new operator decision that
expands scope (for example a supported companion, pack, custom target, or a
future first-party target capability). None of those variants was implemented
or evaluated in this PoC.

## Next step

Do not start the GP AI Gateway/model PoC yet. First decide whether to stop or
authorize evaluation of one out-of-scope transport boundary. If a supported
channel later reaches `PASS`, the next minimal PoC is:

```text
AI zapytaj [prompt] -> GP AI Gateway -> one test model
-> structured response -> player.say/action in Minecraft
```

No OpenAI, Gemini, Qwen, or OpenRouter request was made during this PoC.

## Evidence and cleanup

The minimal screenshots and complete Echo request log are indexed in
[`evidence/README.md`](evidence/README.md). After the tests, Echo process
`44648` was stopped, Windows reported no listener on port `8765`, the PoC
runtime directory was absent, and only the explicitly created temporary files
were removed from `mt`.

## Versions and diagnostic sources

- Minecraft Education: `1.26.3200.0` on `mt`.
- Minecraft MakeCode target: `2.1.27`; PXT: `12.1.17`.
- Deployed target configuration:
  <https://cdn.makecode.com/api/config/minecraft/targetconfig/v2.1.27>
- Deployed target and simulator bundles:
  <https://cdn.makecode.com/blob/316b630ce6f3a95360fb693dcf198cdf7d9080cc/target.js>
  and
  <https://cdn.makecode.com/blob/af43071094954073b6ce90e430cbbe422f15b1af/sim.js>.
- Editor Extension requirements:
  <https://makecode.com/extensions/extensions>,
  <https://github.com/microsoft/pxt/blob/master/webapp/src/extensionManager.ts>,
  and
  <https://github.com/microsoft/pxt/blob/master/pxteditor/editorcontroller.ts>.
