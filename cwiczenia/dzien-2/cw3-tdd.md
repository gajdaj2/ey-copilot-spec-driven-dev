# Ćwiczenie 3 (Dzień 2) — Document Service w pętli TDD

| | |
|---|---|
| **Czas** | 40 min |
| **Blok** | 3 — Od specyfikacji do kodu sterowanego AI |
| **Cel** | Usługa realizująca spec — testy AC napisane przed kodem i zielone |
| **Wejście** | `spec.md`, `schemas.py`, `tasks.md` z Ćwiczenia 2 |
| **Rezultat** | Min. 8 z 10 AC z zielonymi testami; w historii gita commit testów przed commitem kodu |

## Krok 0 — Reguła „agent nie zmienia testów AC” (3 min)

Dopisz do `.github/instructions/tests.instructions.md`:

```markdown
- Pliki tests/*_ac.py są wykonywalną specyfikacją. NIE edytuj ich.
- Test czerwony = popraw kod. Jeśli uważasz, że test jest błędny — zgłoś to i zatrzymaj się.
```

Opcjonalnie (hooki preview): hook `preToolUse` odmawiający zapisu do `tests/*_ac.py`.

## Krok 1 — Szkielet i fake LLM (T001–T002, 7 min)

```text
▶ Copilot (Agent)
#file:specs/001-document-service/plan.md #file:app/schemas.py
Zrealizuj T001–T002: app/main.py z fabryką create_app(storage, llm) (routery z prefiksem /v1),
app/llm/port.py z Protocol LLMPort.answer(document, question) -> LLMAnswer,
app/storage.py z FileStorage(root: Path), tests/conftest.py z FakeLLM(reply=None, error=None)
i fixture client(tmp_path) → TestClient(create_app(FileStorage(tmp_path), FakeLLM())).
Bez logiki endpointów. Akceptacja: pytest zbiera testy środowiska i przechodzi.
```

Commit: `chore: szkielet usługi i FakeLLM`.

## Krok 2 — RED: testy z kryteriów (T003, 8 min)

```text
▶ Copilot (Agent)
Z tabeli kryteriów w #file:specs/001-document-service/spec.md napisz tests/test_documents_ac.py
dla AC-01..AC-04. Nazwy: test_ac01_..., granice z obu stron (5 MB przechodzi, 5 MB + 1 → 413),
AC-01 sprawdza DOKŁADNY zestaw pól odpowiedzi. Używaj fixture client. NIE implementuj endpointów.
```

```bash
$ pytest tests/test_documents_ac.py -q
```

✅ **Punkt kontrolny:** testy są **czerwone z właściwego powodu** (404/405 — brak endpointu), a nie `ImportError`.

```bash
$ git add tests/ && git commit -m "test: AC-01..AC-04 upload (red)"
```

## Krok 3 — GREEN: implementacja (T004, 8 min)

```text
▶ Copilot (Agent)
Zaimplementuj upload tak, by tests/test_documents_ac.py przeszły. NIE zmieniaj plików w tests/.
Logika (limity, duplikat po sha256) w app/service.py, nie w routerze. Uruchom pytest -q.
```

```bash
$ pytest -q && git commit -am "feat: upload wg AC-01..AC-04 (green)"
```

## Krok 4 — Pytanie z structured output (T005–T006, 10 min)

RED:

```text
▶ Copilot (Agent)
Napisz tests/test_questions_ac.py dla AC-05..AC-10 (FakeLLM: reply=LLMAnswer(...),
error=LLMTimeout() / LLMUnavailable()). Parametryzuj AC-06: "", "   ", 501 znaków. Bez implementacji.
```

Commit testów, potem GREEN:

```text
▶ Copilot (Agent)
Zaimplementuj POST /v1/documents/{id}/questions: DocumentService.ask używa LLMPort;
app/llm/client.py — OpenAICompatibleLLM z response_format json_schema (strict) z LLMAnswer.model_json_schema(),
timeout 20 s, walidacja odpowiedzi LLMAnswer.model_validate_json; APITimeoutError → LLMTimeout,
APIError/ValidationError → LLMUnavailable. NIE zmieniaj tests/. Testy używają tylko FakeLLM.
```

## Krok 5 — Porządek (4 min)

1. Odhacz zadania w `tasks.md`.
2. `ruff check . && pytest -q`.
3. Commit. Brakujące AC → `TECH_DEBT.md` z planem.

**Bonus:** skrypt macierzy pokrycia AC → test:

```text
▶ Copilot (Agent)
Napisz scripts/traceability.py: zbiera ID AC z spec.md (regex AC-\d+) i nazwy testów z
`pytest --collect-only -q`, drukuje tabelę markdown | AC | testy | status (brak testu / jest) |.
```

## 🆘 Jeśli utkniesz

| Problem | Rozwiązanie |
|---|---|
| Testy czerwone przez `ImportError` | Najpierw szkielet (krok 1); test ma failować na asercji, nie na imporcie |
| Agent zmienia testy | `git restore tests/`; wzmocnij regułę w `tests.instructions.md`; prompt „NIE zmieniaj tests/” |
| 5 MB przechodzi/nie przechodzi „na odwrót” | Typowa pomyłka `<` vs `<=`; test granicy z obu stron to wyłapie |
| `strict` json_schema odrzucony przez API | Wszystkie pola wymagane (`quote: str \| None` bez domyślnej), `extra="forbid"`; sprawdź wsparcie u dostawcy |
| Test woła prawdziwy LLM | `create_app` musi przyjmować `llm`; w testach zawsze `FakeLLM` |

## ✔ Definicja ukończenia

- [ ] Min. 8/10 AC z zielonymi testami, brakujące w `TECH_DEBT.md`
- [ ] W `git log` commity `test: … (red)` przed `feat: … (green)`
- [ ] `create_app` z wstrzykiwanymi zależnościami; testy bez sieci
- [ ] Zadania odhaczone w `tasks.md`
