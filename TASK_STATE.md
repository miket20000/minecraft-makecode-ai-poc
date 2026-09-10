# TASK STATE

## Cel i zakres

Empirycznie ustalić, czy Minecraft Education 1.26.3200.0 może przez MakeCode
2.1.27 komunikować się z zewnętrznym API i odebrać wynik w uruchomionym
świecie. Test używa wyłącznie lokalnego Echo API; bez modeli AI, sekretów,
pakietów Minecraft i własnego targetu PXT.

## Stan

- Publiczne repozytorium: `miket20000/minecraft-makecode-ai-poc`.
- Badany host: `mt`; Minecraft Education i Code Builder są uruchomione.
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
- Standalone MakeCode nie utworzył projektu z dokładnym SHA po imporcie: `FAIL`.
- Echo API na Windows loopback przeszło test kontraktu PowerShell, ale nie
  zarejestrowało żadnego żądania od poprawnego kandydata Direct HTTP.
- Kandydat Shim `8ca7925` (kod transportu z `47c67da`, osobna nazwa pakietu
  wyłącznie przeciw cache) zaimportował się i wystartował. Komenda `ai` dotarła
  do świata, ale nie było odpowiedzi ani żądania w logu Echo: runtime `FAIL`.
- HTTPS nie jest wymagany: żaden mechanizm nie wykonał nawet preflightu/POST,
  więc nie zaobserwowano blokady specyficznej dla localhost/CORS/mixed content.

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

1. Potwierdź na faktycznym targetconfig brak
   `appTheme.allowPackageExtensions` i `packages.approvedEditorExtensionUrls`.
2. Utwórz jeden cache-distinct manifest probe z `extension.url`; bez GitHub
   Pages i bez pełnej strony.
3. Zaimportuj probe do kolejnego nowego projektu. Brak przycisku Editor albo
   iframe kończy Editor Extension jako `FAIL`.
4. Następnie wykonaj cleanup Echo/portu i plików tymczasowych, zakończ raport
   jako `NO-GO`, zaktualizuj stan i wykonaj końcowy commit.
