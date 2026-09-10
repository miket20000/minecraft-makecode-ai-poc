# Transport PoC report

## Result

`IN PROGRESS`

## Working flow

Not established yet.

## Tested variants

| Candidate | Standalone simulator | Code Builder | Minecraft world | Reason/evidence |
| --- | --- | --- | --- | --- |
| Identity (`88f5a93`) | NOT TESTED | PASS | PASS | Extension imported; category `AI` and block `AI zapytaj` visible; chat command `ai` displayed `hello` in the Minecraft world. This proves Extension execution, not HTTP. |
| Direct HTTP (`0135609`) | FAIL | FAIL | FAIL | Exact-SHA project was rejected as an Extension error. Code Builder displayed `Looks like there are some errors in the extensions added to this project. How would you like to proceed?` on import and again on Start. Standalone import returned to Home without creating the project. Echo log contained no runtime request. |

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

## Recommended architecture

Pending empirical result.

## Next step

Pending empirical result.
