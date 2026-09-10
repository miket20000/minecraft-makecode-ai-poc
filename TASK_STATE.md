# TASK STATE

## Cel i zakres

Empirycznie ustalić, czy Minecraft Education 1.26.3200.0 może przez MakeCode
2.1.27 komunikować się z zewnętrznym API i odebrać wynik w uruchomionym
świecie. Test używa wyłącznie lokalnego Echo API; bez modeli AI, sekretów,
pakietów Minecraft i własnego targetu PXT.

## Stan

- Publiczne repozytorium: `miket20000/minecraft-makecode-ai-poc`.
- Badany host: `mt`; Minecraft Education i Code Builder są uruchomione.
- Kandydat 1 (Identity) jest przygotowywany.
- Wcześniejsze wyniki: brak wykonanych scenariuszy.

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

1. Dokończ minimalny kandydat Identity i wykonaj commit.
2. Zaimportuj go do nowego projektu Code Builder, nie nadpisując istniejącego.
3. Potwierdź blok `AI zapytaj [tekst]` oraz `player.say(AI.ask("hello"))`
   w rzeczywistym świecie Minecraft.
4. Zapisuj `PASS`, `FAIL` i `BLOCKED`; nie usuwaj wcześniejszych niepowodzeń.

