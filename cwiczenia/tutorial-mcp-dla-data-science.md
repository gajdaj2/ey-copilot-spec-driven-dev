# Tutorial — MCP dla Data Science: od dokumentacji do danych

| | |
|---|---|
| **Czas** | 75 min |
| **Poziom** | Początkujący, bez wymagań programistycznych |
| **Cel** | Dodać serwery MCP w VS Code, użyć ich do pytań o dokumentację i zweryfikować wywołane narzędzia |
| **Wejście** | VS Code z dostępem do GitHub Copilot i połączeniem z internetem |
| **Rezultat** | Sprawdzone połączenia Microsoft Learn MCP i Context7; opcjonalne demo GitHub MCP |

Nie trzeba edytować plików JSON ani uruchamiać komend w terminalu. Dwa główne serwery są zdalne, więc nie wymagają instalowania Node.js ani Pythona. Tutorial nie wymaga zmian w repozytorium ani nowych zależności.

**Ważne o danych:** nie wklejaj do promptów danych klientów, prywatnych notebooków, wyników badań objętych ograniczeniami ani sekretów. Zapytania do zdalnego serwera opuszczają komputer. Przed dodaniem MCP sprawdź wydawcę, adres i wymagane uprawnienia; zatwierdzaj tylko narzędzia, których działanie rozumiesz.

## Krok 0 — Przygotowanie (10 min)

Otwórz folder repozytorium w VS Code i Copilot Chat. Do tych ćwiczeń używaj publicznej dokumentacji albo ogólnych pytań bez danych projektu.

MCP łączy klienta, np. VS Code, z serwerem oferującym konkretne narzędzia. W ćwiczeniu poprosisz Copilota o użycie tych narzędzi i sprawdzisz, czy faktycznie zostały wywołane. Samo dodanie serwera nie oznacza jeszcze, że odpowiedź z niego korzysta.

✅ **Punkt kontrolny:** wiesz, że MCP daje dostęp do narzędzi lub źródeł, a zdalne połączenie może wysyłać zapytanie poza komputer.

## Krok 1 — Wybierz serwer do zadania (10 min)

| Serwer | Co daje osobie z Data Science | Wymagania |
|---|---|---|
| **Microsoft Learn MCP** | Wyszukiwanie i pobieranie oficjalnej dokumentacji Microsoft, np. Fabric lub Azure Machine Learning | Zdalny endpoint; bez logowania i opłat według dokumentacji Microsoft |
| **Context7** | Aktualna dokumentacja bibliotek i przykłady, np. pandas lub scikit-learn | Zdalny endpoint; OAuth w przeglądarce |
| **GitHub MCP** (opcjonalne demo) | Pytania o README, pliki i strukturę publicznego repozytorium z przykładem analitycznym | Konto GitHub i OAuth; dostępne operacje zależą od uprawnień i konfiguracji narzędzi |

Wybieraj MCP tylko wtedy, gdy potrzebujesz jego konkretnego źródła lub narzędzia. Nie dodawaj serwera „na zapas”. Microsoft Learn służy do dokumentacji Microsoft; Context7 do dokumentacji bibliotek; GitHub MCP do kontekstu GitHub. To różne źródła, a nie trzy wersje tego samego modelu.

✅ **Punkt kontrolny:** potrafisz wskazać, którego serwera użyć do dokumentacji Fabric, którego do pandas i dlaczego GitHub MCP jest tu tylko dodatkiem.

## Krok 2 — Dodaj Microsoft Learn MCP (15 min)

1. Otwórz Command Palette: `Ctrl+Shift+P` (macOS: `⌘⇧P`).
2. Uruchom **MCP: Add Server**.
3. Wybierz dodanie serwera z URL, a następnie transport **HTTP**.
4. Wpisz endpoint:

   ```text
   https://learn.microsoft.com/api/mcp
   ```

5. Nadaj mu czytelną nazwę, np. `microsoft-learn`, i wybierz konfigurację osobistą **Global**. Nie zapisuj konfiguracji osobistej jako pliku projektu ani do repozytorium.
6. Przeczytaj komunikat zaufania i potwierdź połączenie tylko wtedy, gdy zgadza się adres wydawcy.

Microsoft Learn MCP jest zdalny, publiczny i według dokumentacji nie wymaga uwierzytelnienia. Udostępnia wyszukiwanie dokumentacji oraz pobieranie artykułów i przykładów kodu.

W nowej wiadomości poproś:

```text
Użyj Microsoft Learn MCP, nie odpowiadaj wyłącznie z pamięci modelu.
Znajdź oficjalną dokumentację Microsoft Fabric dotyczącą lakehouse.
Podaj krótki opis i link do artykułu, który zwróciło narzędzie.
Nie używaj żadnych prywatnych danych.
```

Rozwiń szczegóły wywołania w czacie. Sprawdź, czy wskazują Microsoft Learn MCP, czy wynik zawiera źródłowy artykuł i czy odpowiedź odpowiada temu wynikowi.

✅ **Punkt kontrolny:** widzisz wywołanie narzędzia Microsoft Learn i możesz otworzyć wskazaną dokumentację. Sama wiarygodnie brzmiąca odpowiedź bez wywołania nie zalicza testu.

## Krok 3 — Dodaj Context7 (15 min)

Dodaj kolejny serwer przez **MCP: Add Server**. Wybierz URL i transport **HTTP**, a jako endpoint użyj adresu OAuth:

```text
https://mcp.context7.com/mcp/oauth
```

Nadaj mu identyfikator `context7`. Gdy VS Code poprosi o logowanie, dokończ OAuth w przeglądarce. Nie kopiuj tokenu do czatu ani plików projektu. Jeśli organizacja blokuje zewnętrzne serwery lub logowanie, pomiń ten krok i skorzystaj z demo prowadzącego.

Poproś o dokumentację biblioteki:

```text
Użyj Context7 MCP, żeby znaleźć aktualną dokumentację pandas dla grupowania danych
przez DataFrame.groupby. Najpierw znajdź właściwą bibliotekę, potem pobierz dokumentację
dotyczącą tego zagadnienia. Podaj źródło i krótki przykład. Nie używaj moich plików.
```

Sprawdź w szczegółach, czy użyto narzędzi Context7 do znalezienia biblioteki i pobrania dokumentacji. Otwórz źródło i zweryfikuj przykład. Jeśli serwer zwróci inny pakiet o podobnej nazwie, popraw zapytanie.

✅ **Punkt kontrolny:** odpowiedź odwołuje się do dokumentacji znalezionej przez Context7, a nie tylko do wiedzy modelu.

## Krok 4 — Porównaj źródła i odpowiedzi (10 min)

Zadaj oba pytania, każde z właściwym serwerem:

1. **Microsoft Learn:** prośba o oficjalne źródło dotyczące usługi Microsoft, np. lakehouse w Fabric.
2. **Context7:** prośba o aktualne API biblioteki pandas lub scikit-learn.

Porównaj, czy wskazane źródła są odpowiednie i czy odpowiedź nie wykracza poza dokumentację. Poproś Copilota o wprost oznaczenie brakujących informacji, zamiast zgadywania.

✅ **Punkt kontrolny:** umiesz odróżnić odpowiedź opartą na wyniku serwera od odpowiedzi wygenerowanej bez jego użycia.

## Krok 5 — Opcjonalne demo GitHub MCP (10 min)

To demo prowadzi instruktor albo uczestnik z kontem szkoleniowym. Oficjalny GitHub MCP Server ma zdalny endpoint:

```text
https://api.githubcopilot.com/mcp/
```

Dodanie wymaga uwierzytelnienia OAuth i może udostępnić narzędzia do modyfikowania repozytoriów, issues lub pull requestów. Zgoda na OAuth może dać dostęp do więcej niż publicznego przykładu. Dlatego:

- użyj konta testowego albo środowiska zatwierdzonego przez organizację;
- sprawdź ekran zgody i dokładne uprawnienia przed zatwierdzeniem;
- użyj wyłącznie publicznego repozytorium szkoleniowego;
- w **Configure Tools** wyłącz narzędzia zapisujące, jeśli można je jednoznacznie rozpoznać;
- jeśli nie da się potwierdzić ograniczenia operacji zapisujących, nie łącz serwera na urządzeniach uczestników — obejrzyj demo prowadzącego.

Bezpieczny prompt demonstracyjny:

```text
Użyj GitHub MCP do odczytania README i listy plików w publicznym repozytorium
[wstaw adres repozytorium szkoleniowego]. Streść strukturę. Nie twórz ani nie zmieniaj
plików, issues, pull requestów ani ustawień.
```

✅ **Punkt kontrolny:** wiesz, że prośba „nie zmieniaj niczego” nie usuwa uprawnień zapisujących przyznanych serwerowi. O bezpieczeństwie decydują również OAuth i dostępne narzędzia.

## Krok 6 — Zaufanie, weryfikacja i sprzątanie (5 min)

Przed każdym MCP sprawdź nazwę wydawcy, endpoint lub polecenie startowe, transport, wymagania logowania i oferowane narzędzia. Serwery uruchamiane lokalnie mogą wykonywać kod na komputerze; serwery zdalne otrzymują zapytania wysyłane przez klienta. Nie zatwierdzaj poleceń ani wywołań narzędzi automatycznie, jeśli nie rozumiesz ich skutków.

Po ćwiczeniu:

1. Otwórz **Chat: Open Customizations** → **MCP Servers**.
2. Zatrzymaj albo usuń połączenia, których nie chcesz zachować.
3. Wyloguj się z Context7/GitHub, jeśli udostępniasz komputer lub kończysz pracę z kontem testowym.
4. Otwórz widok **Source Control**. Konfiguracja Global nie powinna pojawić się w zmianach repozytorium.

✅ **Punkt kontrolny:** wiesz, jak sprawdzić użycie serwera i jak usunąć połączenie; do czatu nie trafiły prywatne dane ani tokeny.

## 🆘 Jeśli utkniesz

| Problem | Rozwiązanie |
|---|---|
| Nie widzę **MCP: Add Server** | Otwórz lokalny folder w VS Code, sprawdź dostępność AI/Copilot i ograniczenia administracyjne. Interfejs może różnić się między wersjami. |
| Serwer został dodany, ale nie działa | Sprawdź, czy wybrałeś URL i HTTP, poprawny endpoint oraz właściwą konfigurację/harness. Uruchom serwer ponownie z widoku MCP Servers. |
| Microsoft Learn zwraca błąd HTTP w przeglądarce | To endpoint dla klienta MCP, a nie zwykła strona WWW. Testuj go przez wywołanie z Copilot Chat. |
| Context7 prosi o ponowne logowanie | Dokończ OAuth w przeglądarce lub sprawdź dostęp organizacyjny; nie wklejaj tokenu do wiadomości. |
| Copilot odpowiada, ale nie widzę wywołania MCP | Poproś ponownie o użycie nazwanego serwera i sprawdź szczegóły wywołania. Jeśli narzędzie się nie pojawiło, odpowiedź nie potwierdza działania MCP. |
| Organizacja blokuje serwer lub OAuth | Nie obchodź polityki. Pomiń połączenie i skorzystaj z demonstracji prowadzącego. |

## ✔ Definicja ukończenia

- [ ] Dodałem Microsoft Learn MCP z oficjalnego endpointu i sprawdziłem jego wywołanie.
- [ ] Dodałem Context7 przez OAuth albo zapisałem, dlaczego blokada organizacji uniemożliwiła ćwiczenie.
- [ ] Sprawdziłem, że odpowiedź wynika z wyniku narzędzia i prowadzi do źródłowej dokumentacji.
- [ ] Rozumiem ryzyko GitHub MCP i wiem, dlaczego jego demo jest opcjonalne.
- [ ] Nie przesłałem prywatnych danych ani sekretów i posprzątałem zbędne połączenia.
- [ ] Widok **Source Control** nie pokazuje konfiguracji osobistych serwerów MCP.

## Dokumentacja

- [Dodawanie serwerów MCP w VS Code](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
- [Microsoft Learn MCP](https://learn.microsoft.com/en-us/training/support/mcp)
- [Context7 — klienci MCP](https://context7.com/docs/resources/all-clients)
- [GitHub MCP Server](https://github.com/github/github-mcp-server)