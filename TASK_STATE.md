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

1. Utwórz osobny commit standardowego simulator-side shimu deklarowanego przez
   `simFiles`, z `//% promise shim=AI::ask` i jednym `POST /echo`.
2. Zaimportuj projekt z dokładnym SHA kandydata (normalny importer cache'uje
   stary ref) i sprawdź Code Builder oraz rzeczywisty świat.
3. Jeżeli shim nie zostanie załadowany lub skompilowany, zakończ ten wariant
   jako `FAIL`; nie twórz własnego targetu.
4. Zapisuj `PASS`, `FAIL` i `BLOCKED`; nie usuwaj wcześniejszych wyników.
