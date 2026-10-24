# Ćwiczenie 4 (Dzień 2) — Problem details i change request v1.1

| | |
|---|---|
| **Czas** | 30 min |
| **Blok** | 4 — Solidna usługa i powtarzalny proces |
| **Cel** | Spójny kontrakt błędów + przećwiczony proces zmiany spec → kontrakt → testy → kod |
| **Wejście** | Usługa po Ćwiczeniu 3 |
| **Rezultat** | Tag `v0.2-service`: zielona bramka, aktualny `contracts/openapi.json`, spec v1.1, zaktualizowany `TECH_DEBT.md` |

## Krok 1 — Kontrakt błędów (10 min)

```text
▶ Copilot (Agent)
Dodaj app/api/problems.py: wyjątek Problem(status, slug, title, detail="", **ext),
handler zwracający application/problem+json (type, title, status, detail, instance + rozszerzenia)
oraz handler RequestValidationError → 422 "validation-error" z listą pól BEZ wartości wejściowych.
Zamień wszystkie HTTPException w usłudze na Problem wg katalogu błędów ze #file:specs/001-document-service/spec.md.
Nie zmieniaj testów AC.
```

Następnie (RED → GREEN) dopisz do testów AC asercje formatu — **to zmiana spec**, więc najpierw dopisz do `spec.md`
sekcję „Katalog błędów” (type · status · kiedy · AC), potem testy:

```python
assert r.headers["content-type"].startswith("application/problem+json")
assert r.json()["type"].endswith("/document-too-large")
```

✅ **Punkt kontrolny:** żaden endpoint nie zwraca gołego 500; `curl` z błędnym JSON zwraca problem+json.

## Krok 2 — Spec Reviewer (5 min)

Utwórz `.github/agents/spec-reviewer.agent.md` (wzór na slajdzie „Review zgodności”) i uruchom go:

```text
▶ Copilot (Spec Reviewer)
Porównaj bieżące zmiany (git diff main) z #file:specs/001-document-service/spec.md.
Zwróć tabelę rozbieżności. Bez uwag o stylu.
```

Zespoły „CLI”:

```bash
$ copilot -p "Porównaj git diff main ze specs/001-document-service/spec.md" --agent spec-reviewer --allow-tool='shell(git:*)'
```

Popraw prawdziwe rozbieżności; szum zignoruj (i zanotuj, ile go było).

## Krok 3 — Change request (10 min)

Prowadzący przydziela jedną zmianę:

- **CR-A „Tagi”:** upload przyjmuje opcjonalne `tags: list[str]` (max 5, każdy ≤ 30 znaków); `GET /v1/documents?tag=…` filtruje.
- **CR-B „Paginacja”:** `GET /v1/documents?limit=&offset=` (limit 1–100, domyślnie 20), odpowiedź `{items, total}`.

Kolejność **zawsze ta sama**, jeden branch / PR:

1. **Spec** — `spec.md` → wersja 1.1, nowe AC-11/AC-12, aktualizacja nie-celów.
2. **Kontrakt** — `app/schemas.py` (pola opcjonalne z domyślnymi wartościami!).
3. **Testy** — `test_ac11_…`, `test_ac12_…` — czerwone; stare testy bez zmian.
4. **Kod** — Agent implementuje do zielonego.

```text
▶ Copilot (Agent)
Specyfikacja zmieniła się: #file:specs/001-document-service/spec.md (v1.1, AC-11, AC-12).
Krok 1: zaktualizuj app/schemas.py. Krok 2: napisz testy AC-11, AC-12 (mają być czerwone) i ZATRZYMAJ SIĘ.
```

Po commicie testów: „Zaimplementuj AC-11 i AC-12. Nie zmieniaj tests/.”

## Krok 4 — Kontrakt w repo i zmiany łamiące (3 min)

```text
▶ Copilot (Agent)
Napisz scripts/export_openapi.py: tworzy aplikację przez create_app z FileStorage w katalogu
tymczasowym i FakeLLM z tests/conftest.py, zapisuje app.openapi() jako JSON (indent=2, sort_keys=True)
do specs/001-document-service/contracts/openapi.json. Bez nowych zależności.
```

```bash
$ git show main:specs/001-document-service/contracts/openapi.json > /tmp/openapi-main.json 2>/dev/null || true
$ python scripts/export_openapi.py
$ git diff --stat specs/001-document-service/contracts/
$ oasdiff breaking /tmp/openapi-main.json specs/001-document-service/contracts/openapi.json --fail-on ERR   # jeśli macie oasdiff
```

Odpowiedz w opisie PR: **czy zmiana jest łamiąca? dlaczego?** (tabela ze slajdu „Wersjonowanie kontraktu”).

## Krok 5 — Dług i tag (2 min)

Zaktualizuj `TECH_DEBT.md`: spłacone z D1 (oznacz), nowe, przechodzące na D3–D4.

```bash
$ ruff check . && pytest -q
$ git commit -am "feat: problem details + CR v1.1" && git tag v0.2-service
```

## 🆘 Jeśli utkniesz

| Problem | Rozwiązanie |
|---|---|
| 422 z FastAPI nadal w starym formacie | Zarejestruj handler `RequestValidationError` w `create_app` (nie tylko `Problem`) |
| Błąd walidacji zwraca wartości pól | Buduj listę błędów z `loc` i `type`, bez `input` |
| Stare testy padają po CR | Pole w odpowiedzi stało się wymagane / zmieniło kształt → to zmiana łamiąca; wróć do spec |
| `oasdiff` niedostępny | Ręczny `git diff` kontraktu + tabela „co jest zmianą łamiącą” ze slajdu |
| Spec Reviewer zwraca same uwagi o stylu | Dopisz w agencie „Nie oceniaj stylu. Tylko rozbieżności ze spec.” |

## ✔ Definicja ukończenia

- [ ] Wszystkie błędy jako `application/problem+json` z katalogu; brak gołych 500
- [ ] Spec Reviewer uruchomiony, rozbieżności poprawione
- [ ] Change request w kolejności spec → kontrakt → testy → kod (widać w historii)
- [ ] `contracts/openapi.json` aktualny; odpowiedź „łamiąca czy nie” w PR
- [ ] `TECH_DEBT.md` zaktualizowany; tag `v0.2-service`
