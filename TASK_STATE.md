# TASK STATE

## Cel i zakres

Empirycznie ustalić, czy Minecraft Education 1.26.3200.0 może przez MakeCode
2.1.27 komunikować się z zewnętrznym API i odebrać wynik w uruchomionym
świecie. Test używa wyłącznie lokalnego Echo API; bez modeli AI, sekretów,
pakietów Minecraft i własnego targetu PXT.

## Stan

- Publiczne repozytorium: `miket20000/minecraft-makecode-ai-poc`.
- Wynik końcowy: `NO-GO` w zatwierdzonym zakresie.
- Badany host: `mt`; Minecraft Education 1.26.3200.0, MakeCode target 2.1.27,
  PXT 12.1.17.
- Kandydat 1 (Identity), commit `88f5a93`, zaimportował się do nowego projektu
  `AI transport PoC`; kategoria `AI` i blok `AI zapytaj` były widoczne.
- `player.say(AI.ask("hello"))` po komendzie czatu `ai` wyświetlił `hello`
  w rzeczywistym świecie Minecraft: `PASS` dla Code Buildera i świata.
- Identity nie testuje transportu HTTP i nie spełnia kryterium `PASS-A`.
- Kandydat Direct HTTP, commit `0135609`, używał jednego wywołania `fetch()` i
  jednego `pxt.Util.requestAsync()`. Projekt z dokładnie tym SHA został
  odrzucony jako błąd Extension przy imporcie i ponownie przy Start: `FAIL`.
- Pierwszy projekt Direct HTTP faktycznie zachował w eksporcie stary SHA
  `88f5a93`; jego wynik oznaczono `BLOCKED`, a nie jako wynik transportu.
- Standalone MakeCode uruchomił pusty projekt, lecz bez połączenia zdarzeń i
  wyników z Minecraftem. Import dokładnego pliku projektu przez CDP nie był
  powtarzalny: transport standalone `BLOCKED`, nie błąd produktu.
- Echo API na Windows loopback przeszło test kontraktu PowerShell, ale nie
  zarejestrowało żadnego żądania od poprawnego kandydata Direct HTTP.
- Kandydat Shim `8ca7925` (kod transportu z `47c67da`, osobna nazwa pakietu
  wyłącznie przeciw cache) zaimportował się i wystartował. Komenda `ai` dotarła
  do świata, ale nie było odpowiedzi ani żądania w logu Echo: runtime `FAIL`.
- HTTPS nie jest wymagany: żaden mechanizm nie wykonał nawet preflightu/POST,
  więc nie zaobserwowano blokady specyficznej dla localhost/CORS/mixed content.
- Targetconfig nie zawiera wartości dla `appTheme.allowPackageExtensions` ani
  `packages.approvedEditorExtensionUrls`. Kandydat Editor probe `017d4ee`
  zaimportował zwykłą kategorię/blok, ale nie pokazał przycisku `Editor` i nie
  załadował iframe: Editor Extension `FAIL`.
- Brak działającego przepływu `Minecraft -> API -> Minecraft`; `PASS-A` i
  `PASS-B` nie zostały osiągnięte.

## Ograniczenia i decyzje

- Każdy mechanizm transportu otrzymuje osobny commit/kandydata.
- `PASS-A` wymaga pełnego przepływu runtime Minecraft -> API -> runtime
  Minecraft; wynik wyłącznie w edytorze/simulatorze nie wystarcza.
- Editor Extension i HTTPS są badane dopiero po niepowodzeniu prostszego
  wariantu.
- Nie modyfikować istniejącego PoC `vps-gp/www/minecraft-ai-editor` ani
  zastanej zmiany `.gitignore` w repozytorium `vps-gp`.

## Środowisko i źródła prawdy

- Minecraft Education: 1.26.3200.0 na `mt`.
- Minecraft MakeCode target: 2.1.27; PXT: 12.1.17.
- Sterowanie UI: WinApp CLI na `mt` przez SSH.
- Repozytorium i zweryfikowane zachowanie runtime są źródłem prawdy o PoC.

## START HERE

1. Przeczytaj `REPORT.md`; zawiera końcową macierz wyników i ograniczenia.
2. Nie rozpoczynaj integracji modelu ani gatewaya. Brak autoryzowanego kanału
   transportowego w aktualnym zakresie.
3. Nierozwiązana decyzja operatora: zatrzymać temat albo osobno autoryzować
   ocenę jednego wariantu spoza zakresu (np. wspierany companion, pack, własny
   target lub przyszła funkcja first-party).
