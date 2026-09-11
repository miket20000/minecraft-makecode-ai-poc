# TASK STATE

## Cel i zakres

Empirycznie ustalić, czy Minecraft Education 1.26.3200.0 może przez MakeCode
2.1.27 komunikować się z zewnętrznym API i odebrać wynik w uruchomionym
świecie. Test używa wyłącznie lokalnego Echo API; bez modeli AI, sekretów,
modeli AI, sekretów ani własnego targetu PXT. Pierwszy etap MakeCode pozostaje
zamknięty jako `NO-GO`; kontynuacja bada natywne `/connect`/Companion.
Operator zawęził bieżący etap: zakończyć po Companion i nie rozpoczynać testów
Behavior Pack.

## Stan

- Publiczne repozytorium: `miket20000/minecraft-makecode-ai-poc`.
- Wynik etapu MakeCode: `NO-GO`; rozszerzony PoC Companion/Pack jest w toku.
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
- Kontynuacja 2026-09-11: w rzeczywistym świecie obie komendy `/help connect`
  i `/help wsserver` są rozpoznawane. Gra opisuje `wsserver (also connect)` i
  składnię `/connect <serverUri: text>`: dostępność `AVAILABLE`.
- Port `19131` był wolny; Windows Python 3.13.14 ma już bibliotekę
  `websockets` 17.0. Dodano minimalny handshake/message probe, bez logiki
  poleceń zwrotnych.
- Kandydat `0828516` przyjął handshake dla dokładnego
  `/connect ws://127.0.0.1:19131` (ścieżka `//`) i wariantu historycznej
  składni `/connect 127.0.0.1:19131/ws` (ścieżka `/ws`). Oba połączenia były
  inicjowane z loopback Minecrafta, ale klient zamykał je po około 0,1 s bez
  wiadomości i wyświetlał `Could not connect to server`: handshake `PASS`,
  połączenie aplikacyjne `FAIL`.
- Biblioteka zgłosiła `invalid status code`; historyczna implementacja
  `mcwss` deklaruje subprotokół `com.microsoft.minecraft.wsencrypt`. Następny
  kandydat ma negocjować tylko ten subprotokół i zarejestrować pierwszą
  wiadomość, bez implementowania pełnego szyfrowania.
- Kandydat `0a50cac` wynegocjował oferowany przez klienta subprotokół
  `com.microsoft.minecraft.wsencrypt`. Dla dokładnego
  `/connect 127.0.0.1:19131/ws` Minecraft wyświetlił
  `Connection established to server`, a socket pozostał otwarty. Klient nie
  wysłał spontanicznej wiadomości: handshake i trwałe połączenie `PASS`.
- Kandydat `7e0b4f6` wysłał przez utrzymany socket minimalną subskrypcję
  `PlayerMessage` oraz `say CONNECT_LOCAL_OK`. Minecraft odpowiedział kodem
  `-2147418107` i tekstem `Encrypted session required`; w świecie nie pojawił
  się efekt polecenia. `PASS-CONNECT-LOCAL` nie został osiągnięty.
- Ustawienie świata ma `Websockets Enabled`; `Require Encrypted Websockets`
  jest w interfejsie wyszarzone. Połączenie plaintext wymaga implementacji
  sesji kryptograficznej.
- Operator rozszerzył zakres o szyfrowanie. Kandydat `d6605a3` wykonał P-384
  ECDH i ustanowił AES-256-CFB8. Zaszyfrowane polecenie zwrotne wyświetliło
  `CONNECT_ENCRYPTED_OK` w świecie, ale pierwsza ramka Minecraft -> Companion
  nie została poprawnie odszyfrowana (`UnicodeDecodeError`). To częściowy
  `PASS` wyjścia Companion -> Minecraft i nadal `FAIL` pełnego round-trip.

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

1. Kontynuuj tylko szyfrowany Companion: ustal, czy pierwsza ramka zwrotna po
   włączeniu AES-256-CFB8 jest plaintextem albo wymaga innego stanu odbiorczego.
2. Uzyskaj pełne `Minecraft -> Companion -> Minecraft`, następnie dołącz Echo
   API i powtórz pełny round-trip w rzeczywistym świecie.
3. Po etapie Companion zaktualizuj raport, posprzątaj procesy i zatrzymaj się.
   Nie rozpoczynaj Behavior Pack.
