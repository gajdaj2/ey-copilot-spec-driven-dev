# Ćwiczenie 2 — Cztery iteracje w Copilocie

| | |
|---|---|
| **Czas** | 25 min |
| **Blok** | 2 — Prompting do kodu i pętla iteracji |
| **Cel** | Przejść samodzielnie pętlę *generuj → uruchom → przeczytaj błąd → popraw* z promptami o 4 elementach |
| **Wejście** | Repozytorium po Ćwiczeniu 1 |
| **Rezultat** | 4 commity na `feat/warmup` → scalone do `main`, plik `prompts/blok2.md` |

Zespoły „VS Code” pracują w czacie w trybie **Agent**, zespoły „CLI” — w `copilot` w terminalu. Prompty są te same.

## Krok 0 — Gałąź i plik na prompty (1 min)

```bash
$ git switch -c feat/warmup
$ mkdir -p prompts && echo "# Prompty — Blok 2" > prompts/blok2.md
```

Każdy prompt, który wyślesz, wklej też do `prompts/blok2.md` z liczbą iteracji.

## Krok 1 — Szkielet i `/health` (5 min)

```text
▶ Copilot (Agent)
Kontekst: pusty pakiet app/, Python 3.12, zależności w pyproject.toml (fastapi, uvicorn już są).
Zadanie: utwórz app/main.py z aplikacją FastAPI i endpointem GET /health.
Ograniczenia: nie dodawaj zależności; nie zmieniaj tests/test_environment.py.
Przykład odpowiedzi: {"status": "ok"}
Akceptacja: `uvicorn app.main:app --reload` startuje, `curl http://127.0.0.1:8000/health` zwraca {"status":"ok"}.
```

```bash
$ uvicorn app.main:app --reload          # w osobnym terminalu
$ curl http://127.0.0.1:8000/health
$ git add -A && git commit -m "feat: szkielet FastAPI i /health"
```

## Krok 2 — `POST /echo` z Pydantic (5 min)

```text
▶ Copilot (Agent)
Kontekst: #file:app/main.py
Zadanie: dodaj POST /echo przyjmujący JSON {"text": "..."} (model Pydantic EchoIn, text 1–200 znaków)
i zwracający {"text": "<TEKST WIELKIMI LITERAMI>"}.
Ograniczenia: nie zmieniaj /health; bez nowych zależności.
Akceptacja: w http://127.0.0.1:8000/docs widać /echo; {"text":"ala"} → {"text":"ALA"}.
```

✅ Sprawdź w `/docs` (Swagger) → *Try it out*. Commit.

## Krok 3 — Testy (7 min)

```text
▶ Copilot (Agent)
Kontekst: #file:app/main.py
Zadanie: napisz tests/test_api.py (pytest + fastapi.testclient.TestClient) dla /health i /echo:
happy path, brak pola text (422), text dłuższy niż 200 znaków (422).
Ograniczenia: nie zmieniaj app/main.py.
Akceptacja: `pytest -q` — wszystkie testy zielone.
```

```bash
$ pytest -q
```

Jeśli coś jest czerwone: **najpierw sam przeczytaj traceback**, potem wklej go Copilotowi z hipotezą
(„chyba brakuje httpx”). Commit.

## Krok 4 — Czytelny błąd 422 (5 min)

```bash
$ curl -s -X POST http://127.0.0.1:8000/echo -H "Content-Type: application/json" -d '{}'
```

```text
▶ Copilot (Agent)
Oto odpowiedź dla POST /echo z pustym JSON: <wklej odpowiedź>.
Zmień obsługę błędów walidacji tak, by odpowiedź miała postać
{"error": "validation_error", "fields": ["text"]} ze statusem 422.
Ograniczenia: zmień tylko app/main.py; testy z kroku 3 muszą przejść (popraw kod, nie asercje,
chyba że asercja sprawdza stary format — wtedy wyjaśnij zmianę).
Akceptacja: curl powyżej zwraca nowy format; pytest -q zielony.
```

Commit, potem scalenie:

```bash
$ pytest -q && git switch main && git merge --no-ff feat/warmup -m "merge: warmup Blok 2"
```

## Krok 5 — Notatka (2 min)

W `prompts/blok2.md` zapisz: liczbę iteracji na krok, **jedną halucynację lub „prawie działa”**, jedno zdanie
„co zaskoczyło nas w Copilocie”. Commit.

## 🆘 Jeśli utkniesz

| Problem | Rozwiązanie |
|---|---|
| `ModuleNotFoundError: app` przy uvicorn | Uruchamiaj z katalogu głównego repo; `app/__init__.py` musi istnieć |
| TestClient: `httpx` not installed | `pip install -e ".[dev]"` — httpx jest w zależnościach dev |
| Copilot dodaje nowe paczki | Odrzuć zmianę (*Undo*), dopisz w prompcie „bez nowych zależności” |
| Ten sam błąd 3× z rzędu | Stop. `git restore .`, mniejszy krok albo napisz poprawkę sam |
| Agent „naprawił” test, zmieniając asercję | Odrzuć; dopisz „popraw kod, nie testy” |
| Port 8000 zajęty | `uvicorn app.main:app --reload --port 8001` |

## ✔ Definicja ukończenia

- [ ] `/health`, `/echo`, testy, czytelny 422 — 4 commity
- [ ] `pytest -q` zielony na `main`
- [ ] `prompts/blok2.md` z promptami, liczbą iteracji i jedną obserwacją
