# Ćwiczenie 4 — Przegląd bezpieczeństwa i pomiar długu

| | |
|---|---|
| **Czas** | 20 min |
| **Blok** | 4 — Granice, jakość i bezpieczeństwo vibe codingu |
| **Cel** | Znaleźć i naprawić typowe błędy kodu z AI w swoim prototypie; zmierzyć dług jako punkt odniesienia |
| **Wejście** | Tag `v0.1-prototyp` |
| **Rezultat** | Poprawiony upload z testem ataku + uzupełniony `TECH_DEBT.md` z tabelą pomiarów |

```bash
$ git switch -c fix/security-review
```

## Krok 1 — Copilot jako recenzent (5 min)

```text
▶ Copilot (Ask)
Przejrzyj #file:app/main.py i #file:app/llm.py pod kątem bezpieczeństwa:
sekrety w kodzie, walidacja wejścia (nazwy plików, rozmiar, typ), path traversal,
SQL injection, brak timeoutów, dane wrażliwe w logach, gołe except.
Zwróć tabelę: plik:linia | problem | ryzyko (wys/śr/nis) | proponowana poprawka.
Nie zmieniaj kodu. Bez uwag o stylu.
```

Porównaj wynik z checklistą ze slajdu „Checklista przeglądu kodu wygenerowanego przez AI”.
Co Copilot pominął? Co jest fałszywym alarmem?

## Krok 2 — Najpierw test ataku, potem poprawka (8 min)

```text
▶ Copilot (Agent)
Dopisz do tests/test_documents.py testy, które dowodzą podatności uploadu:
- nazwa pliku "../../app/main.py" nie może zapisać pliku poza UPLOADS,
- plik > 5 MB → 413,
- rozszerzenie .exe → 415.
NIE poprawiaj jeszcze kodu. Uruchom pytest i pokaż, które testy są czerwone.
```

✅ **Punkt kontrolny:** nowe testy są **czerwone** (to dowód, że podatność istnieje). Commit testów.

```text
▶ Copilot (Agent)
Popraw POST /documents tak, by testy powyżej przeszły: nazwa przez Path(...).name,
lista dozwolonych rozszerzeń (.md, .txt), odczyt maks. 5 MB + 1 bajt, sprawdzenie, że
ścieżka po resolve() leży w UPLOADS. Nie zmieniaj testów.
```

```bash
$ pytest -q && git commit -am "fix: walidacja uploadu (path traversal, 413, 415)"
```

## Krok 3 — Pomiar długu (5 min)

```bash
$ ruff check . --statistics
$ bandit -q -r app
$ gitleaks detect --source . --no-banner      # albo: pre-commit run gitleaks --all-files
$ pytest --cov=app --cov-report=term-missing
```

Wpisz wyniki do tabeli „Pomiar” w `TECH_DEBT.md` z dzisiejszą datą.

## Krok 4 — Uzupełnij rejestr (2 min)

```text
▶ Copilot (Ask)
Przejrzyj repozytorium #codebase i zaproponuj wpisy do TECH_DEBT.md w formacie
| ID | Skrót | Ryzyko | Wpływ | Właściciel | Spłata |. Nie zmieniaj kodu.
```

Krytycznie wybierz, co dopisać (min. 5 pozycji łącznie). Oznacz TD-04 (walidacja uploadu) jako spłacone dziś.

```bash
$ git commit -am "docs: przegląd bezpieczeństwa i baseline długu"
$ git switch main && git merge --no-ff fix/security-review -m "merge: przegląd bezpieczeństwa"
```

## 🆘 Jeśli utkniesz

| Problem | Rozwiązanie |
|---|---|
| Test path traversal przechodzi od razu | TestClient/httpx normalizuje `../` w URL — atak jest w **nazwie pliku** w multipart, nie w ścieżce URL |
| `gitleaks: command not found` | `pre-commit run gitleaks --all-files` (pre-commit instaluje gitleaks sam) |
| bandit zgłasza `B101 assert` w testach | Uruchamiaj tylko na `app` (`-r app`), nie na `tests` |
| Copilot chce zmienić testy przy poprawce | Odrzuć; dopisz „nie zmieniaj testów — popraw kod” |

## ✔ Definicja ukończenia

- [ ] Testy ataku napisane **przed** poprawką (widać w historii gita)
- [ ] Upload odrzuca `../`, > 5 MB i niedozwolone typy; `pytest` zielony
- [ ] Tabela pomiarów w `TECH_DEBT.md` z datą
- [ ] Min. 5 pozycji długu z ryzykiem i terminem
