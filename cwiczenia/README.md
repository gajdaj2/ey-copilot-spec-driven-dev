# Ćwiczenia — instrukcje krok po kroku

Każde ćwiczenie ze szkolenia *Python + AI w produkcji* ma tu osobny plik z instrukcją:
cel, czas, wejście, kroki z gotowymi promptami dla GitHub Copilot, punkty kontrolne,
typowe problemy i definicję ukończenia.

> Zasada: **najpierw spróbuj sam**, z instrukcją ze slajdu. Ten katalog jest pomocą,
> gdy utkniesz albo chcesz sprawdzić, czy niczego nie pominąłeś.

## Dzień 1 — Vibe coding z GitHub Copilot

| # | Ćwiczenie | Czas | Plik |
|---|---|---|---|
| 1 | Copilot gotowy do pracy i start repozytorium | 20 min | [dzien-1/cw1-copilot-start.md](dzien-1/cw1-copilot-start.md) |
| 2 | Cztery iteracje w Copilocie | 25 min | [dzien-1/cw2-cztery-iteracje.md](dzien-1/cw2-cztery-iteracje.md) |
| 3 | Praca w parach nad prototypem | 45 min | [dzien-1/cw3-prototyp-w-parach.md](dzien-1/cw3-prototyp-w-parach.md) |
| 4 | Przegląd bezpieczeństwa i pomiar długu | 20 min | [dzien-1/cw4-bezpieczenstwo-i-dlug.md](dzien-1/cw4-bezpieczenstwo-i-dlug.md) |
| 5 | Konfiguracja Copilota w repozytorium | 35 min | [dzien-1/cw5-konfiguracja-copilota.md](dzien-1/cw5-konfiguracja-copilota.md) |

## Dzień 2 — Spec-driven development

| # | Ćwiczenie | Czas | Plik |
|---|---|---|---|
| 1 | Inwentaryzacja ukrytych wymagań | 15 min | [dzien-2/cw1-inwentaryzacja.md](dzien-2/cw1-inwentaryzacja.md) |
| 2 | Specyfikacja „Document Service” | 45 min | [dzien-2/cw2-specyfikacja.md](dzien-2/cw2-specyfikacja.md) |
| 3 | Document Service w pętli TDD | 40 min | [dzien-2/cw3-tdd.md](dzien-2/cw3-tdd.md) |
| 4 | Problem details i change request v1.1 | 30 min | [dzien-2/cw4-bledy-i-change-request.md](dzien-2/cw4-bledy-i-change-request.md) |

## Konwencje w instrukcjach

- `▶ Copilot (Ask)` / `▶ Copilot (Plan)` / `▶ Copilot (Agent)` — wybierz tego agenta w czacie VS Code
  i wklej prompt z bloku kodu. Zespoły „CLI” wklejają ten sam prompt w `copilot`.
- `$` — polecenie w terminalu (z aktywnym `.venv`).
- ✅ **Punkt kontrolny** — sprawdź, zanim pójdziesz dalej.
- 🆘 **Jeśli utkniesz** — typowe problemy i rozwiązania.
- Po każdym działającym kroku: **commit**. Przed większą zmianą agenta: czyste drzewo (`git status`).
