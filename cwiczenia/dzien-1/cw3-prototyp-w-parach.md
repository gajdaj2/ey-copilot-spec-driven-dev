# Ćwiczenie 3 — Praca w parach nad prototypem asystenta

| | |
|---|---|
| **Czas** | 45 min |
| **Blok** | 3 — Prototyp asystenta: od zera do działania |
| **Cel** | Działający asystent: upload → lista → pytanie → odpowiedź, zbudowany z Copilotem |
| **Wejście** | `main` po Ćwiczeniu 2 (`/health`, testy), plik `.env` z kluczem |
| **Rezultat** | Tag `v0.1-prototyp`, README z uruchomieniem, min. 5 wpisów w `TECH_DEBT.md` |

## Role (zmiana co iterację)

- **Driver** — pisze prompty w Copilocie (najpierw **Plan**, potem **Agent**).
- **Navigator** — czyta diff, pilnuje commitów, prowadzi `TECH_DEBT.md`, pyta „czy na pewno?”.

```bash
$ git switch -c feat/prototyp
```

## I1 — Konfiguracja z `.env` (5 min)

```text
▶ Copilot (Agent)
Kontekst: #file:app/main.py, plik .env.example (LLM_API_KEY, LLM_BASE_URL, LLM_MODEL).
Zadanie: dodaj app/config.py, który ładuje .env (python-dotenv) i udostępnia te 3 wartości.
Brak LLM_API_KEY = błąd przy starcie z czytelnym komunikatem.
Ograniczenia: nie loguj i nie wypisuj wartości klucza; bez nowych zależności.
Akceptacja: aplikacja startuje z .env; bez klucza — czytelny błąd.
```

✅ `git status` nie pokazuje `.env`. Commit.

## I2 — Upload i lista dokumentów (8 min)

Najpierw **Plan**, potem **Agent**:

```text
▶ Copilot (Plan)
Zaplanuj POST /documents (upload jednego pliku .md/.txt do data/uploads/) i GET /documents
(posortowana lista nazw). Wypisz pliki do zmiany i testy. Nie edytuj kodu.
```

```text
▶ Copilot (Agent)
Zaimplementuj plan powyżej w app/main.py. Wymaga python-multipart (jest w zależnościach).
Akceptacja: curl -F "file=@data/sample_docs/pelnomocnik.md" http://127.0.0.1:8000/documents → 201;
GET /documents zwraca ["pelnomocnik.md"].
```

```bash
$ curl -F "file=@data/sample_docs/pelnomocnik.md" http://127.0.0.1:8000/documents
$ curl http://127.0.0.1:8000/documents
```

Navigator: dopisz dług, np. `TD-0x | Brak walidacji nazwy, typu i rozmiaru pliku | Path traversal, DoS | Wysoki | … | D1/D2`.
W kodzie komentarz `# DŁUG: TD-0x`. Commit.

## I3 — Wpięcie LLM i `POST /ask` (10 min)

```text
▶ Copilot (Agent)
Kontekst: #file:app/main.py #file:app/config.py
Zadanie: utwórz app/llm.py z funkcją answer(document: str, question: str) -> str
(klient openai.OpenAI z api_key i base_url z config, model z LLM_MODEL, temperature=0).
Prompt systemowy: odpowiadaj WYŁĄCZNIE na podstawie dokumentu; jeśli brak odpowiedzi — powiedz to wprost.
Dokument w znacznikach <dokument>…</dokument>, przycięty do 30 000 znaków (oznacz # DŁUG).
Dodaj POST /ask {"document": "<nazwa>", "question": "..."} → {"answer": "..."}; 404 gdy brak pliku.
Ograniczenia: main.py importuje answer przez `from app.llm import answer`.
Akceptacja: pytanie „Ile dni trwa weryfikacja pełnomocnictwa?” do pelnomocnik.md zwraca odpowiedź z „14 dni”.
```

```bash
$ curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" \
    -d '{"document":"pelnomocnik.md","question":"Ile dni trwa weryfikacja pełnomocnictwa?"}'
```

Commit. Zmiana ról.

## I4 — Prosty UI (7 min)

```text
▶ Copilot (Agent)
Utwórz static/index.html: formularz uploadu, lista z GET /documents (odświeżana po uploadzie),
select dokumentu, pole pytania i wynik z POST /ask. Czysty HTML + JS (fetch), bez frameworków i CDN.
W app/main.py zamontuj StaticFiles(directory="static", html=True) na "/" — NA KOŃCU pliku, po endpointach.
Akceptacja: http://127.0.0.1:8000/ pozwala przejść cały scenariusz; /docs i API nadal działają.
```

## I5 — Testy i dane (8 min)

```text
▶ Copilot (Agent)
Napisz tests/test_documents.py: upload + lista (UPLOADS podmienione na tmp_path przez monkeypatch),
/ask z mockiem: monkeypatch.setattr(app.main, "answer", ...) — NIE app.llm.answer,
/ask dla nieistniejącego dokumentu → 404.
Akceptacja: pytest -q zielony BEZ dostępu do sieci; żaden test nie woła prawdziwego LLM.
```

Navigator sprawdza: czy któryś test **testuje mocka zamiast kodu** (mock zwraca „OK” i asercja sprawdza „OK”)?

## I6 — Funkcja do wyboru (pozostały czas)

Jedna z: historia pytań · podgląd dokumentu · obsługa PDF · limit długości pytania (np. 500 znaków).
Najpierw **Plan**, potem **Agent**, potem commit.

## Zamknięcie

Zadajcie 3 pytania testowe, w tym **jedno, na które dokument nie zawiera odpowiedzi**
(np. do `pelnomocnik.md`: „Jaki jest limit karty kredytowej?”). Asystent powinien przyznać, że nie wie.

```bash
$ pytest -q
$ git switch main && git merge --no-ff feat/prototyp -m "merge: prototyp asystenta"
$ git tag v0.1-prototyp
```

## 🆘 Jeśli utkniesz

| Problem | Rozwiązanie |
|---|---|
| `Form data requires "python-multipart"` | `pip install -e ".[dev]"`; paczka jest w `pyproject.toml` |
| Wszystkie endpointy zwracają 404 po I4 | `app.mount("/", StaticFiles…)` jest przed endpointami — przenieś na koniec pliku |
| Test woła prawdziwe API / wisi | Mockujesz `app.llm.answer` zamiast `app.main.answer` |
| `401` / `AuthenticationError` z LLM | Zły klucz lub `LLM_BASE_URL`; sprawdź `.env` (nie wklejaj klucza do czatu!) |
| `UnicodeDecodeError` przy /ask | Plik nie jest UTF-8 albo to PDF — oznacz jako dług lub zrób I6 „obsługa PDF” |
| Asystent zmyśla odpowiedź | Wzmocnij prompt systemowy; dopisz do długu „brak cytowania źródeł → D3” |

## ✔ Definicja ukończenia

- [ ] Osoba spoza zespołu uruchamia aplikację z README w < 5 min
- [ ] Upload, lista i pytanie działają z UI
- [ ] Asystent przyznaje „brak informacji”, gdy dokument nie zawiera odpowiedzi
- [ ] `pytest` przechodzi bez sieci (LLM zamockowany)
- [ ] Brak sekretów w repo (`gitleaks detect` / pre-commit)
- [ ] Historia commitów pokazuje iteracje, tag `v0.1-prototyp`
- [ ] `TECH_DEBT.md`: min. 5 pozycji z ryzykiem i planem spłaty
