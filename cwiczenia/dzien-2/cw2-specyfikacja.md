# Ćwiczenie 2 (Dzień 2) — Specyfikacja „Document Service”

| | |
|---|---|
| **Czas** | 45 min |
| **Blok** | 2 — Pisanie specyfikacji wykonywalnych |
| **Cel** | Kompletna, zatwierdzona specyfikacja i plan zadań — wejście dla Copilota w Bloku 3 |
| **Wejście** | `inventory.md` z Ćwiczenia 1 + odpowiedzi product ownera |
| **Rezultat** | Commit `spec: document-service v1` — `spec.md`, `app/schemas.py`, `plan.md`, `tasks.md`; zero `[DO WYJAŚNIENIA]` |

Opcjonalnie ze Spec Kit (`specify init . --ai copilot`, potem `/speckit.constitution`, `/speckit.specify`,
`/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`). Poniżej wariant **bez** Spec Kit — te same kroki ręcznie.

## Krok 1 — Konstytucja (5 min)

Dopisz do `.github/copilot-instructions.md` sekcję (albo utwórz `.specify/memory/constitution.md`):

```markdown
## Zasady projektu (konstytucja)
1. Każda zmiana zachowania zaczyna się od zmiany w specs/.
2. Testy kryteriów akceptacji (tests/*_ac.py) powstają przed kodem; agent ich nie zmienia.
3. Pydantic v2 (app/schemas.py) jest jedynym źródłem schematów API.
4. Błędy API w formacie application/problem+json (RFC 9457).
5. Zależności zewnętrzne (LLM, storage) za interfejsami; w testach tylko fake'i.
6. Żadnych danych produkcyjnych ani sekretów w repozytorium.
```

## Krok 2 — `spec.md` (15 min)

Skopiuj szablon do `specs/001-document-service/spec.md` i wypełnij dla 4 operacji:
**upload · lista · pobranie/usunięcie · pytanie**.

```markdown
# Document Service — specyfikacja v1.0

## Cel
<1–2 zdania, bez technologii: kto, jaki problem>

## Zakres (v1)
- POST   /v1/documents                    — upload
- GET    /v1/documents                    — lista
- GET    /v1/documents/{id} | DELETE …    — pobranie / usunięcie
- POST   /v1/documents/{id}/questions     — pytanie do dokumentu

## Nie-cele (v1)
- wyszukiwanie w wielu dokumentach (D3 — RAG)
- uwierzytelnianie (D4), historia rozmowy, streaming

## Przypadki brzegowe
- <wejście> → <status> <type błędu>

## Kryteria akceptacji
| ID | Given | When | Then |
|---|---|---|---|
| AC-01 | … | … | … |

## Otwarte pytania
- [DO WYJAŚNIENIA] …
```

Wskazówki: przypadki brzegowe bierzesz z `inventory.md` (status `NIE WIEMY` i `PRZYPADEK`).
Minimum **10 kryteriów AC**, np. AC-01 upload OK, AC-02 duplikat → 409, AC-03 > 5 MB → 413, AC-04 zły typ → 415,
AC-05 brak dokumentu → 404, AC-06 puste/za długie pytanie → 422, AC-07 odpowiedź znaleziona, AC-08 brak odpowiedzi → `found=false`,
AC-09 błąd LLM → 502, AC-10 timeout LLM → 504.

## Krok 3 — `app/schemas.py` (8 min)

```text
▶ Copilot (Agent)
#file:specs/001-document-service/spec.md
Utwórz app/schemas.py (Pydantic v2): klasa bazowa Contract z ConfigDict(extra="forbid",
frozen=True, str_strip_whitespace=True); QuestionIn, AnswerOut, DocumentOut, DocumentList.
KAŻDE ograniczenie z sekcji „Przypadki brzegowe” odwzoruj w Field(...) (min/max_length, le, pattern, Literal).
Dodaj examples i description. Nie twórz endpointów. Nie zmieniaj innych plików.
```

Sprawdź ręcznie: czy pytanie `"   "` nie przejdzie walidacji? (`str_strip_whitespace` + `min_length=1`)

```bash
$ python -c "from app.schemas import QuestionIn; QuestionIn(question='   ')"   # oczekiwany ValidationError
```

## Krok 4 — Clarify (5 min)

```text
▶ Copilot (Ask)
#file:specs/001-document-service/spec.md #file:app/schemas.py
Zadaj mi pytania o WSZYSTKIE niejasności, sprzeczności i brakujące przypadki brzegowe
w tej specyfikacji. Maks. 10 pytań, każde z propozycją 2 odpowiedzi.
```

Rozstrzygnij pytania (biznesowe — z prowadzącym), dopisz decyzje do `spec.md`, usuń wszystkie `[DO WYJAŚNIENIA]`.

## Krok 5 — Plan i zadania (agent Plan) (7 min)

```text
▶ Copilot (Plan)
#file:specs/001-document-service/spec.md #file:app/schemas.py #file:.github/copilot-instructions.md
Przygotuj plan.md i tasks.md:
- struktura: app/api, app/service.py, app/storage.py, app/llm/ (port + klient), create_app()
- każde zadanie ≤ 30 min, z listą plików i AC, które pokrywa
- najpierw testy (czerwone), potem implementacja; oznacz [P] zadania równoległe
- wypisz założenia i pytania, jeśli spec jest niejasna
```

Zapisz wynik do `specs/001-document-service/plan.md` i `tasks.md` (Agent Plan nie zapisuje plików — skopiuj
albo poproś Agenta: „zapisz powyższy plan do …”).

**Review krzyżowy (5 min):** wymieńcie się `spec.md` z sąsiednim zespołem. Pytanie kontrolne: „co się stanie, jeśli…?”

```bash
$ git add -A && git commit -m "spec: document-service v1"
```

## 🆘 Jeśli utkniesz

| Problem | Rozwiązanie |
|---|---|
| Kryteria „życzeniowe” („system działa szybko”) | Każde AC musi dać się sprawdzić testem: konkretne wejście → konkretny status/pole |
| Copilot dopisuje endpointy w schemas.py | Odrzuć; prompt „nie twórz endpointów, zmieniaj tylko app/schemas.py” |
| Sprzeczność spec ↔ prototyp | Spec wygrywa — prototyp był odkrywaniem; zapisz decyzję w spec |
| Za dużo szczegółów technicznych w Celu | Cel bez technologii; technologia → plan.md |

## ✔ Definicja ukończenia

- [ ] Konstytucja (5–7 zasad) w repo
- [ ] `spec.md`: 6 sekcji, min. 10 AC z ID, zero `[DO WYJAŚNIENIA]`
- [ ] `app/schemas.py` odwzorowuje ograniczenia ze spec
- [ ] `plan.md` + `tasks.md` (zadania wskazują AC)
- [ ] Review krzyżowy zrobiony, uwagi naniesione
