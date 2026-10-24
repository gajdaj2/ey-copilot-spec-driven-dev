# Ćwiczenie 1 — Copilot gotowy do pracy i start repozytorium

| | |
|---|---|
| **Czas** | 20 min |
| **Blok** | 1 — Czym jest vibe coding i jak ustawić warsztat |
| **Cel** | Działające środowisko, zalogowany Copilot i pierwszy commit wygenerowany z jego pomocą |
| **Wejście** | To repozytorium (gałąź `main`), klucz szkoleniowy od prowadzącego |
| **Rezultat** | Commit `chore: README i środowisko` + pierwszy wpis w `TECH_DEBT.md` |

## Krok 1 — Zespół i środowisko (5 min)

1. Zespoły 2–3 osobowe. Ustalcie, czy jesteście zespołem **„VS Code”** czy **„CLI”** (prowadzący pilnuje proporcji ~50/50).
2. Otwórz folder repozytorium w VS Code. Zainstaluj rekomendowane rozszerzenia (powiadomienie w prawym dolnym rogu
   albo `Extensions` → filtr `@recommended`).
3. Zaloguj się do GitHub Copilot **kontem firmowym** (ikona Copilota na pasku stanu → *Sign in*).

```bash
$ python -m venv .venv
$ source .venv/bin/activate        # Windows: .venv\Scripts\activate
$ pip install -e ".[dev]"
$ cp .env.example .env             # Windows: copy .env.example .env
$ pre-commit install
$ pytest
```

4. Otwórz `.env` i wpisz klucz szkoleniowy w `LLM_API_KEY=`, adres w `LLM_BASE_URL=` i model w `LLM_MODEL=` (z kartki).

✅ **Punkt kontrolny:** `pytest` pokazuje `5 passed`; `git status` **nie** pokazuje pliku `.env`.

**Zespoły „CLI”** dodatkowo: zainstaluj Copilot CLI (instrukcja od prowadzącego / dokumentacja GitHub),
uruchom `copilot` w katalogu repozytorium i zaloguj się (`/login`).

## Krok 2 — Pierwsza rozmowa w trybie Ask (5 min)

Otwórz czat Copilota (`Ctrl+Alt+I`, macOS `⌃⌘I`), wybierz agenta **Ask** i wywołaj gotowy prompt file:

```text
/wyjasnij-repo
```

Albo wpisz ręcznie:

```text
▶ Copilot (Ask)
Wyjaśnij strukturę tego repozytorium #codebase: do czego służy każdy katalog i plik
konfiguracyjny. Potem wypisz, czego brakuje w README, żeby nowa osoba uruchomiła projekt
w 5 minut na Windows, macOS i Linux. Nie proponuj zmian w kodzie aplikacji. Maks. 15 punktów.
```

✅ **Punkt kontrolny:** odpowiedź wspomina `.env.example`, `TECH_DEBT.md`, `data/sample_docs` — znaczy, że Copilot czyta repo.

## Krok 3 — Poprawki README w trybie Agent (7 min)

Upewnij się, że drzewo jest czyste (`git status`). Przełącz agenta na **Agent**:

```text
▶ Copilot (Agent)
Popraw README.md na podstawie listy braków z poprzedniej odpowiedzi.
Ograniczenia: zmieniaj tylko README.md; nie dodawaj zależności; zachowaj istniejące sekcje.
Akceptacja: polecenia w sekcji „Start” działają na Windows i macOS/Linux (podaj oba warianty),
jest sekcja „Najczęstsze problemy” z min. 3 pozycjami.
```

1. Przeczytaj diff (w czacie *Keep / Undo* albo `git diff`). Czy zmienił tylko README?
2. Wykonaj 1–2 polecenia z nowego README, żeby sprawdzić, że działają.
3. Commit:

```bash
$ git add README.md
$ git commit -m "chore: README i środowisko"
```

## Krok 4 — Pierwszy wpis długu (3 min)

Dopisz w tabeli `TECH_DEBT.md` (pod nagłówkiem tabeli) pierwszy wiersz, np.:

```markdown
| TD-01 | Brak CI (testy i skanery tylko lokalnie) | Regresje niewidoczne dla zespołu | Średni | <imię> | D2 |
```

```bash
$ git commit -am "docs: TD-01 w rejestrze długu"
```

Zapisz na tablicy: nazwa zespołu · VS Code/CLI · model wybrany w Copilocie.

## 🆘 Jeśli utkniesz

| Problem | Rozwiązanie |
|---|---|
| Brak ikony Copilota / „not signed in” | Paleta poleceń → *GitHub Copilot: Sign In*; sprawdź, że to konto firmowe z licencją |
| Nie widzę agentów Ask/Plan/Agent | Zaktualizuj VS Code i rozszerzenie Copilot Chat; picker agentów jest pod polem czatu |
| `/wyjasnij-repo` nie działa | Otwórz **folder** repozytorium (nie pojedynczy plik); prompt files leżą w `.github/prompts/` |
| `pip install` — błąd wersji Pythona | Wymagany 3.12 lub 3.13: `python --version`; utwórz venv właściwym interpreterem |
| `test_env_is_ignored_by_git` czerwony | Uruchamiasz pytest poza repozytorium gita albo zmieniłeś `.gitignore` |
| Agent zmienił więcej niż README | `git restore .` i powtórz prompt z mocniejszym ograniczeniem „zmieniaj tylko README.md” |

## ✔ Definicja ukończenia

- [ ] `pytest` zielony, `.env` poza gitem
- [ ] Copilot odpowiada w trybie Ask, prompt `/wyjasnij-repo` działa
- [ ] Commit `chore: README i środowisko` (diff dotyczy tylko README)
- [ ] Pierwszy wiersz w `TECH_DEBT.md`
