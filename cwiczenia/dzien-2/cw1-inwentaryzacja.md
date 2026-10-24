# Ćwiczenie 1 (Dzień 2) — Inwentaryzacja ukrytych wymagań

| | |
|---|---|
| **Czas** | 15 min |
| **Blok** | 1 — Dlaczego spec-driven: od „vibe” do kontraktu |
| **Cel** | Wydobyć z prototypu D1 wszystkie decyzje, które muszą trafić do specyfikacji |
| **Wejście** | Tag `v0.1-prototyp`, `TECH_DEBT.md`, `prompts/*.md` |
| **Rezultat** | `specs/001-document-service/inventory.md` + otwarte pytania do product ownera |

```bash
$ git switch main && git switch -c spec/001-document-service
$ mkdir -p specs/001-document-service
```

## Krok 1 — Copilot wypisuje obserwowalne zachowania (4 min)

Agent **Ask** albo **Plan** — tylko odczyt, nic nie zmieni:

```text
▶ Copilot (Ask)
#codebase Wypisz WSZYSTKIE zachowania tej aplikacji, które klient API może zaobserwować:
endpointy (metoda, ścieżka), kształt żądań i odpowiedzi, kody statusu, komunikaty błędów,
limity (rozmiar, długość, typy plików), zachowanie w przypadkach brzegowych
(pusty plik, duplikat, brak odpowiedzi w dokumencie, błąd LLM, timeout).
Format: tabela | # | zachowanie | gdzie w kodzie (plik:linia) |. Nie zmieniaj kodu.
```

## Krok 2 — Klasyfikacja (5 min)

Skopiuj tabelę do `inventory.md` i dodaj kolumnę **Status**:

| Status | Znaczenie |
|---|---|
| `DECYZJA` | Świadomie ustaliliśmy wczoraj i chcemy zachować |
| `PRZYPADEK` | Tak wyszło z generowania — do potwierdzenia lub zmiany |
| `NIE WIEMY` | Brak zachowania lub nikt nie wie, co powinno się stać |

## Krok 3 — Pytania i dług (4 min)

1. Dopisz sekcję `## Otwarte pytania` — wszystko z „jak to właściwie powinno działać?” z wczoraj.
2. Przejrzyj `TECH_DEBT.md`: które pozycje to **brakujące wymagania**? (np. „brak walidacji uploadu” → wymaganie o limitach i typach). Dopisz je do pytań.
3. Pytania biznesowe zadaj **prowadzącemu (product owner)**, odpowiedzi zapisz obok pytań.

Przykładowe pytania, które warto zadać:

- Czy upload identycznego pliku (ten sam SHA-256) to błąd, czy zwracamy istniejący dokument?
- Jaki jest maksymalny rozmiar pliku i jakie typy przyjmujemy w v1?
- Co zwracamy, gdy dokument nie zawiera odpowiedzi — błąd czy poprawną odpowiedź z flagą?
- Ile czekamy na LLM i co zwracamy po przekroczeniu czasu?
- Czy lista dokumentów ma być posortowana? Stronicowana?

## Krok 4 — Commit (2 min)

```bash
$ git add specs/ && git commit -m "spec: inwentaryzacja zachowań prototypu"
```

## 🆘 Jeśli utkniesz

| Problem | Rozwiązanie |
|---|---|
| Copilot proponuje zmiany w kodzie | Używasz agenta Agent — przełącz na Ask/Plan; dopisz „nie zmieniaj kodu” |
| Lista jest pobieżna | Dopytaj per endpoint: „#file:app/main.py — dla POST /documents wypisz wszystkie ścieżki błędów” |
| Nie macie prototypu z D1 | Użyj repo referencyjnego od prowadzącego (tag `v0.1-prototyp`) |

## ✔ Definicja ukończenia

- [ ] `inventory.md` z min. 15 zachowaniami i statusem każdego
- [ ] Sekcja „Otwarte pytania” z odpowiedziami product ownera, gdzie były potrzebne
- [ ] Commit na gałęzi `spec/001-document-service`
