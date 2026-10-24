# docs-assistant — repozytorium startowe

Asystent dokumentacji wewnętrznej fikcyjnego **Banku Bałtyckiego**.
Projekt sztafetowy szkolenia *Python + AI w produkcji* — **Dzień 1: vibe coding z GitHub Copilot**.

Repozytorium jest celowo prawie puste: aplikację (FastAPI + LLM + prosty UI)
generujemy z pomocą GitHub Copilot (VS Code: Ask · Plan · Agent, Copilot CLI) w trakcie dnia. Gotowe są tylko elementy,
których nie zostawiamy przypadkowi: struktura, zależności, sekrety, dane i rejestr długu.

## Struktura

```
docs-assistant/
├── .github/
│   ├── copilot-instructions.md  # instrukcje dla Copilota (rozbudowa w Bloku 5)
│   └── prompts/
│       └── wyjasnij-repo.prompt.md  # /wyjasnij-repo — Ćwiczenie 1
├── .vscode/
│   ├── extensions.json     # Copilot, Copilot Chat, Python, Ruff
│   └── settings.json       # pytest, ruff, auto-approve tylko bezpiecznych poleceń
├── app/                    # kod aplikacji (generujemy z Copilotem)
├── cwiczenia/              # instrukcje krok po kroku do każdego ćwiczenia (D1, D2)
├── tests/                  # testy pytest
├── data/
│   └── sample_docs/        # WYŁĄCZNIE dane syntetyczne
├── .env.example            # nazwy zmiennych, bez wartości
├── .gitignore              # .env, .venv, data/uploads/ ...
├── .pre-commit-config.yaml # gitleaks + ruff
├── pyproject.toml          # Python 3.12+, fastapi, uvicorn
├── TECH_DEBT.md            # rejestr świadomie zaciągniętego długu
└── AGENTS.md               # odsyłacz dla innych agentów
```

## Start (ok. 5 minut)

Wymagania: Python 3.12 lub 3.13, git.

```bash
git clone <adres-repozytorium> docs-assistant && cd docs-assistant

# wariant A: venv + pip
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# wariant B: uv
uv venv && source .venv/bin/activate && uv pip install -e ".[dev]"

# sekrety: kopiujemy szablon i wpisujemy KLUCZ SZKOLENIOWY
cp .env.example .env

# hooki: skaner sekretów i linter przy każdym commicie
pre-commit install

# sprawdzenie środowiska
pytest
```

`pytest` powinien pokazać zielone testy środowiska (`tests/test_environment.py`).

Gdy w Bloku 2–3 powstanie `app/main.py`, aplikację uruchamiamy poleceniem:

```bash
uvicorn app.main:app --reload
# http://127.0.0.1:8000/docs
```

## Ćwiczenia

Instrukcje krok po kroku z gotowymi promptami: [cwiczenia/README.md](cwiczenia/README.md).

## GitHub Copilot

1. Zainstaluj rekomendowane rozszerzenia (VS Code zaproponuje je po otwarciu folderu).
2. Zaloguj się do Copilota **kontem firmowym** (licencja Business/Enterprise) — nie prywatnym.
3. Otwórz czat (`Ctrl+Alt+I` / `⌃⌘I`), wybierz agenta **Ask** i wpisz `/wyjasnij-repo`.
4. Zespoły „CLI”: zainstaluj [Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli)
   i uruchom `copilot` w katalogu repozytorium.

Który tryb kiedy:

| Tryb | Do czego | Zmienia pliki? |
|---|---|---|
| Ask | wyjaśnianie repo, błędów, API | nie |
| Plan | plan zmiany przed implementacją | nie |
| Agent | implementacja, testy, poprawki | tak — przeglądaj diff, commituj po każdym kroku |
| Copilot CLI / cloud agent | praca w terminalu / issue → PR | tak — tylko z dobrymi instrukcjami repo |

## Zasady pracy na szkoleniu

1. **Gałąź na każdy eksperyment** — `main` zawsze działa.
2. **Commit po każdym działającym kroku** — git to Twój przycisk „cofnij” dla agenta.
3. **Sekrety tylko w `.env`** — nigdy w kodzie, promptach, testach ani logach.
   Wyciek klucza = rotacja klucza, nie „usunięcie commita”.
4. **Tylko dane syntetyczne** — do `data/` nie trafiają prawdziwe dokumenty, dane klientów
   ani zrzuty z systemów.
5. **Świadomy skrót = wpis w `TECH_DEBT.md`** + komentarz `# DŁUG:` w kodzie.
6. Zgody dla agenta: automatycznie tylko `pytest`, `ruff`, `git status/diff` (`.vscode/settings.json`);
   polecenia sieciowe, usuwanie plików, instalacje — zawsze po potwierdzeniu. Nigdy „zatwierdzaj wszystko”.

## Dane przykładowe

`data/sample_docs/` zawiera pięć fikcyjnych procedur Banku Bałtyckiego z konkretnymi
faktami (terminy, listy dokumentów, opłaty), o które można pytać asystenta:

| Plik | Temat |
|---|---|
| `pelnomocnik.md` | Ustanowienie i zmiana pełnomocnika do rachunku firmowego |
| `zastrzezenie-karty.md` | Zastrzeżenie karty płatniczej |
| `reklamacja.md` | Reklamacja transakcji kartowej |
| `zmiana-danych.md` | Zmiana danych osobowych klienta |
| `zamkniecie-rachunku.md` | Zamknięcie rachunku osobistego |

Wszystkie nazwy, kwoty i terminy są zmyślone na potrzeby szkolenia.

## Rozwiązanie Bloku 5

Gałąź `blok5-rozwiazanie` zawiera przykładową konfigurację Copilota: pełne instrukcje repo,
instrukcje dla `tests/`, prompt file `/nowy-endpoint`, custom agenta *Security Reviewer*,
skill `fastapi-endpoint` i hook blokujący sekrety (preview). Zajrzyj **po** Ćwiczeniu 5:

```bash
git diff main..blok5-rozwiazanie --stat
```
