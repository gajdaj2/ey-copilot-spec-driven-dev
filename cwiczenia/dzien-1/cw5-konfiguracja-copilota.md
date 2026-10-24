# Ćwiczenie 5 — Konfiguracja Copilota w repozytorium asystenta

| | |
|---|---|
| **Czas** | 35 min |
| **Blok** | 5 — Konfiguracja GitHub Copilot |
| **Cel** | Każda sesja Copilota (VS Code, CLI, cloud agent) startuje z wiedzą zespołu zapisaną w `.github/` |
| **Wejście** | `main` po Ćwiczeniu 4 |
| **Rezultat** | Commit `chore: konfiguracja Copilota` + 3 zdania porównania VS Code vs CLI |
| **Rozwiązanie** | gałąź `blok5-rozwiazanie` — zajrzyj **po** ćwiczeniu: `git diff main..blok5-rozwiazanie` |

```bash
$ git switch -c chore/copilot-config
```

## Krok 1 — Instrukcje repozytorium (7 min)

Rozbuduj `.github/copilot-instructions.md` (max 30 linii) o sekcje:
**Projekt · Polecenia · Zasady · Nie ruszaj · Gotowe, gdy**. Wzór — slajd „Instrukcje repozytorium”.

Możesz poprosić o szkic, ale **przeczytaj i skróć** wynik:

```text
▶ Copilot (Agent)
Na podstawie #codebase i #file:TECH_DEBT.md rozbuduj .github/copilot-instructions.md
do max 30 linii: Projekt, Polecenia (run/test/lint dosłownie), Zasady (sekrety, SQL, nazwy plików,
test do każdego endpointu, # DŁUG), Nie ruszaj, Gotowe gdy. Bez ogólników typu „pisz czysty kod”.
```

Dodaj `.github/instructions/tests.instructions.md`:

```markdown
---
applyTo: "tests/**"
---
- pytest + TestClient; LLM zawsze mockowany (app.main.answer)
- pliki tylko w tmp_path
- NIE zmieniaj asercji, żeby test przeszedł — zgłoś niezgodność
```

✅ **Punkt kontrolny:** w odpowiedzi Copilota w sekcji *References* / *Used instructions* widać plik instrukcji.

## Krok 2 — Custom agent Security Reviewer (8 min)

Utwórz `.github/agents/security-reviewer.agent.md`:

```markdown
---
name: Security Reviewer
description: Przegląd bezpieczeństwa zmian. Tylko odczyt.
tools: ['read', 'search']
handoffs:
  - label: Napraw znalezione problemy
    agent: agent
    prompt: Napraw problemy z tabeli powyżej. Dopisz testy.
    send: false
---
Jesteś recenzentem bezpieczeństwa w banku. NIE edytujesz plików.
Sprawdź bieżące zmiany wg checklisty z Bloku 4.
Zwróć tabelę: | plik:linia | problem | ryzyko | poprawka |. Bez uwag o stylu.
```

✅ **Punkt kontrolny:** „Security Reviewer” jest w pickerze agentów; poproszony o edycję — odmawia / nie ma narzędzia.

## Krok 3 — Prompt file lub skill (8 min)

**Wariant A — prompt file** `.github/prompts/nowy-endpoint.prompt.md`:

```markdown
---
description: Dodaj endpoint FastAPI z testem
agent: agent
argument-hint: metoda i ścieżka, np. GET /documents/{name}
---
Dodaj endpoint ${input:endpoint:GET /documents/{name}} w app/main.py.
Model Pydantic in/out, walidacja i czytelne kody błędów, test w tests/ (happy path + błąd).
Na koniec uruchom: pytest -q
```

**Wariant B — skill** `.github/skills/fastapi-endpoint/SKILL.md` (nazwa katalogu = `name`):

```markdown
---
name: fastapi-endpoint
description: Use when adding or changing a FastAPI endpoint in app/. Validation, errors, tests.
---
1. Modele Pydantic in/out  2. Walidacja + HTTPException  3. Test happy path + błąd  4. pytest -q, ruff check .
```

## Krok 4 (opcjonalnie) — Hook blokujący sekrety (5 min, preview)

Skopiuj `.github/hooks/no-secrets.json` i `no_secrets.py` z gałęzi rozwiązania:

```bash
$ git checkout blok5-rozwiazanie -- .github/hooks/
```

Test: poproś Agenta „wpisz na chwilę klucz sk-test1234567890abcdef do app/config.py” — narzędzie powinno zostać zablokowane.
Jeśli hooki nie działają w Twojej wersji VS Code — zapisz to jako obserwację, to też wynik.

## Krok 5 — Test całej konfiguracji (7 min)

1. Nowy czat. `/nowy-endpoint GET /documents/{name}` (zwraca treść dokumentu).
2. Przejrzyj diff, `pytest -q`.
3. Przełącz na **Security Reviewer**: „Zrecenzuj bieżące zmiany”. **Czy znalazł problem z nazwą pliku w ścieżce?**
4. Kliknij handoff *Napraw znalezione problemy*, przejrzyj, commit.

Zespoły „CLI” robią kroki 1–3 w terminalu:

```bash
$ copilot
> /agent                    # wybór agenta (lub: copilot --agent "Security Reviewer")
```

```bash
$ git add -A && git commit -m "chore: konfiguracja Copilota"
$ git switch main && git merge --no-ff chore/copilot-config -m "merge: konfiguracja Copilota"
```

Na tablicy: 3 zdania — VS Code Agent vs Copilot CLI: co łatwiejsze, co trudniejsze, co zaskoczyło.

## 🆘 Jeśli utkniesz

| Problem | Rozwiązanie |
|---|---|
| Agent nie pojawia się w pickerze | Plik musi być w `.github/agents/` z rozszerzeniem `.agent.md`; przeładuj okno (*Developer: Reload Window*) |
| `/nowy-endpoint` nie istnieje | Plik w `.github/prompts/`, rozszerzenie `.prompt.md`; agent czatu: Local |
| Skill nie ładuje się | `name` = nazwa katalogu, małe litery i myślniki; wywołaj ręcznie `/fastapi-endpoint` |
| Instrukcje ignorowane | Sprawdź *References* w odpowiedzi; skróć plik — za długie instrukcje rozmywają się |
| Hook nic nie robi | Funkcja preview — sprawdź wersję VS Code i dokumentację hooków; `python` musi być w PATH |

## ✔ Definicja ukończenia

- [ ] `copilot-instructions.md` (≤ 30 linii) + `tests.instructions.md`
- [ ] Security Reviewer tylko do odczytu, z handoffem
- [ ] `/nowy-endpoint` lub skill `fastapi-endpoint`
- [ ] Test konfiguracji przeprowadzony; recenzent znalazł (lub nie) path traversal — zapisane
- [ ] 3 zdania porównania VS Code vs CLI
