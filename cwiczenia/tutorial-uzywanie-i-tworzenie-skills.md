# Tutorial — używanie i tworzenie Agent Skills

| | |
|---|---|
| **Czas** | 90 min |
| **Poziom** | Osoba znająca podstawy Copilot Chat i pracę z repozytorium |
| **Cel** | Znaleźć i wywołać skill, a następnie utworzyć własny skill z opisem, instrukcjami i referencją |
| **Wejście** | VS Code z dostępem do GitHub Copilot, otwarty folder repozytorium |
| **Rezultat** | `.github/skills/procedure-checker/SKILL.md` oraz `references/answer-format.md` |

Tutorial używa VS Code i syntetycznych dokumentów z `data/sample_docs/`. Nie wymaga klucza LLM, nowych zależności ani zmian w kodzie aplikacji. Skills są otwartym standardem, ale lokalizacje i obsługa opcjonalnych pól mogą różnić się między klientami.

## Krok 0 — Przygotowanie (10 min)

Otwórz folder repozytorium w VS Code i upewnij się, że Copilot jest zalogowany. W terminalu sprawdź stan drzewa:

```bash
git status --short
```

Jeśli widzisz wcześniejsze zmiany, zachowaj je zgodnie z zasadami zespołu i zacznij na czystym drzewie. Nie usuwaj zmian na potrzeby tutoriala.

Skills dostępne dla projektu znajdziesz zwykle w `.github/skills/<nazwa>/SKILL.md`. VS Code obsługuje też `.agents/skills/` i `.claude/skills/`; wybierz lokalizację zgodną z klientami, w których zespół ma używać skill. Skill prywatny zapisuje się w katalogu użytkownika, np. `~/.copilot/skills/`, a nie w katalogu promptów.

✅ **Punkt kontrolny:** znasz lokalizację skill współdzielonego z projektem i pracujesz wyłącznie na fikcyjnych procedurach.

## Krok 1 — Wybierz właściwą personalizację (10 min)

Skill opisuje wyspecjalizowany, wielokrotnie używany proces. Może zawierać instrukcje, przykłady oraz dodatkowe pliki, takie jak skrypty lub referencje. Porównaj:

| Potrzeba | Użyj |
|---|---|
| Stałe zasady projektu, np. styl i konwencje | Instrukcji repozytorium lub instrukcji plikowych |
| Jeden konkretny prompt z parametrami | Prompt file lub zwykłego promptu |
| Powtarzalnej procedury z dodatkowymi materiałami | Skill |
| Osobnej roli z własnymi narzędziami lub etapem przekazania pracy | Custom agent |

W Copilot Chat wpisz `/` i sprawdź menu skills. Możesz też otworzyć **Configure Skills** (w Local skrótem `/skills`) lub Agent Customizations. Skills widoczne w menu zależą od tego, co jest zainstalowane i obsługiwane w danym środowisku.

Jeśli znajdziesz odpowiedni skill, uruchom go z krótkim, bezpiecznym zadaniem i sprawdź jego wynik. Jeśli nie ma pasującego skill, kontynuuj: w tym repo nie zakładamy obecności konkretnego skill, a ćwiczenie utworzy własny.

✅ **Punkt kontrolny:** potrafisz wyjaśnić, dlaczego wielokrotnej procedury z referencją nie warto za każdym razem wklejać jako osobnego promptu.

## Krok 2 — Zaprojektuj skill i jego opis (15 min)

Stworzysz `procedure-checker`, który odpowiada na pytania o fikcyjne procedury bankowe wyłącznie na podstawie wskazanego pliku. Zanim utworzysz pliki, określ:

1. **Możliwość:** wyszukiwanie i streszczanie faktów z procedury.
2. **Kiedy użyć:** pytania o wymagane dokumenty, terminy i opłaty w procedurach.
3. **Kiedy nie użyć:** pytania spoza wskazanego dokumentu lub wymagające interpretacji nieopisanych zasad.
4. **Wynik:** krótka odpowiedź, wskazanie pliku i sekcji oraz jasna informacja, gdy dokument nie zawiera odpowiedzi.

### `name` i `description`

`name` i `description` są wymagane. Nazwa:

- ma od 1 do 64 znaków;
- używa wyłącznie małych liter ASCII, cyfr i pojedynczych łączników `-`;
- nie zaczyna się ani nie kończy łącznikiem i nie zawiera `--`;
- musi być identyczna z nazwą katalogu skill.

W tym ćwiczeniu nazwa katalogu i wartość pola to `procedure-checker`. Nie używaj wielkich liter, spacji, ukośników ani prefiksów organizacji.

`description` ma od 1 do 1024 znaków. Powinien krótko opisywać **co skill robi** i **kiedy go używać**. Dodaj konkretne frazy, na które Copilot może dopasować zadanie, np. `required documents`, `processing deadlines`, `fees` i `bank procedure`. Frazy w opisie wspierają automatyczne dopasowanie, ale nie gwarantują wywołania skill; możesz uruchomić go ręcznie przez `/procedure-checker`.

✅ **Punkt kontrolny:** nazwa spełnia reguły i jest identyczna z nazwą katalogu; opis zawiera zarówno możliwości, jak i sytuacje użycia.

## Krok 3 — Utwórz `SKILL.md` (20 min)

Utwórz katalog `.github/skills/procedure-checker/` i w nim `SKILL.md`. Zacznij od wymaganego frontmatter:

```markdown
---
name: procedure-checker
description: >-
  Finds and verifies facts in synthetic bank procedures. Use when answering
  questions about required documents, processing deadlines, fees, or procedure
  steps in the repository's sample_docs.
argument-hint: "[ścieżka do procedury] [pytanie]"
user-invocable: true
disable-model-invocation: false
---

# Sprawdzanie procedur

## Procedura

1. Odczytaj wskazany plik z `data/sample_docs/`.
2. Odpowiadaj wyłącznie na podstawie jego treści. Nie dopowiadaj zasad ani faktów.
3. Podaj ścieżkę i nagłówek sekcji, które potwierdzają odpowiedź.
4. Jeśli dokument nie zawiera odpowiedzi, napisz to wprost. Nie zgaduj.
5. Cytuj krótko; nie kopiuj całej procedury.

Przedstaw wynik zgodnie z [formatem odpowiedzi](./references/answer-format.md).
Wszystkie dokumenty w `data/sample_docs/` są fikcyjne i służą tylko szkoleniu.
```

Frontmatter jest YAML-em pomiędzy liniami `---`. Używaj spacji, poprawnych wcięć i krótkich wartości; jeśli wartość zawiera dwukropek, ujmij ją w cudzysłów.

### Opcjonalne pola

| Pole | Znaczenie |
|---|---|
| `argument-hint` | Podpowiedź dla osoby wywołującej skill jako slash command; nie jest instrukcją dla modelu. |
| `user-invocable` | Czy skill pojawia się w menu `/`; domyślnie `true`. `false` ukrywa go z menu, ale nadal pozwala na automatyczne użycie. |
| `disable-model-invocation` | Czy model może załadować skill automatycznie; domyślnie `false`. `true` wymaga ręcznego wywołania przez `/`. |
| `context: fork` | Eksperymentalne uruchomienie skill w osobnym kontekście; wymaga ustawienia `github.copilot.chat.skillTool.enabled`. Nie używamy go w tym ćwiczeniu. |
| `license` | Krótka informacja o licencji skill. |
| `compatibility` | Wymagania środowiskowe, jeśli skill ich rzeczywiście potrzebuje. |
| `metadata` | Dodatkowe metadane jako mapa klucz-wartość; wartości zgodnie ze specyfikacją powinny być tekstowe. |
| `allowed-tools` | Eksperymentalna lista preautoryzowanych narzędzi; obsługa zależy od klienta i nie zastępuje przeglądu bezpieczeństwa. |

Nie dodawaj opcjonalnych pól „na zapas”. `user-invocable` kontroluje menu, a `disable-model-invocation` automatyczne dopasowanie; to niezależne ustawienia.

✅ **Punkt kontrolny:** `name` i `description` są obecne, opis mieści się w limicie i katalog nazywa się dokładnie `procedure-checker`.

## Krok 4 — Dodaj referencję i użyj skill (15 min)

Utwórz plik `.github/skills/procedure-checker/references/answer-format.md`:

```markdown
# Format odpowiedzi

Odpowiedz w formacie:

- **Odpowiedź:** krótko i bez dopowiadania nieopisanych zasad.
- **Podstawa:** ścieżka pliku i nagłówek sekcji.
- **Brakujące informacje:** wypisz, czego dokument nie określa, albo napisz „brak”.
```

Link w `SKILL.md` jest względny wobec pliku skill. Dodatkowy plik nie powinien być obszerną kopią instrukcji; trzymaj szczegóły w referencji i jawnie ją linkuj.

W Copilot Chat wybierz skill z menu `/` lub wpisz:

```text
/procedure-checker data/sample_docs/pelnomocnik.md Ile dni roboczych trwa standardowa weryfikacja?
```

Sprawdź odpowiedź w źródle. Procedura podaje do 14 dni roboczych od złożenia kompletnego wniosku; potwierdzenie powinno wskazać sekcję „Weryfikacja i terminy”. Potem zadaj pytanie o fakt, którego dokument nie zawiera, np. limit karty kredytowej. Skill powinien przyznać, że brak danych.

✅ **Punkt kontrolny:** odpowiedź ma podstawę w pliku i sekcji; przy braku informacji skill nie zgaduje.

## Krok 5 — Sprawdź automatyczne dopasowanie i granice (10 min)

W nowej wiadomości opisz potrzebę bez slash command, używając słów z `description`, np.:

```text
Sprawdź wymagane dokumenty i opłatę w data/sample_docs/pelnomocnik.md.
Podaj źródłową sekcję i nie dopowiadaj niczego spoza procedury.
```

Sprawdź, czy Copilot użył skill lub jego instrukcji. Automatyczne dopasowanie zależy od klienta i kontekstu; samo umieszczenie skill w obsługiwanym katalogu nie gwarantuje jego użycia. Jeśli nie został dobrany, uruchom go jawnie przez `/procedure-checker`.

Sprawdź też pytanie spoza jego zakresu. Skill ma odmówić zgadywania i wskazać, że podana procedura nie odpowiada na pytanie.

✅ **Punkt kontrolny:** umiesz odróżnić ręczne wywołanie od automatycznego dopasowania i zweryfikować odpowiedź w dokumencie.

## Krok 6 — Zasoby, bezpieczeństwo i przegląd (10 min)

Skills są ładowane stopniowo: nazwa i opis pomagają wykryć właściwy skill; pełny `SKILL.md` jest ładowany po aktywacji; dodatkowe zasoby są potrzebne dopiero wtedy, gdy skill do nich odsyła. Wykorzystaj to:

- trzymaj `SKILL.md` zwięzły; standard zaleca poniżej 500 linii i mniej niż 5000 tokenów;
- duże tabele wiedzy umieszczaj w `references/`, szablony w `assets/`, a skrypty w `scripts/`;
- linkuj dodatkowe pliki ścieżkami względnymi względem skill i nie twórz długich łańcuchów referencji;
- skrypty opisuj jasno, obsługuj błędy i sprawdzaj ich kod przed uruchomieniem.

Przed użyciem skill pobranego z internetu lub udostępnionego przez inną osobę sprawdź jego treść, źródła, linkowane pliki i skrypty. Nie dodawaj sekretów ani prawdziwych danych klientów. Instrukcje w skill kierują zachowaniem modelu, ale nie są twardą granicą bezpieczeństwa.

Sprawdź zmiany:

```bash
git status --short
git diff -- .github/skills/procedure-checker/
```

Nowe pliki mogą być nieśledzone i niewidoczne w zwykłym `git diff`. Otwórz je bezpośrednio w edytorze albo dodaj jawnie i obejrzyj staged diff:

```bash
git add .github/skills/procedure-checker/
git diff --cached -- .github/skills/procedure-checker/
git diff --cached --check
```

Po przeglądzie możesz zapisać ćwiczenie commitem:

```bash
git commit -m "tutorial: add procedure-checker skill"
```

✅ **Punkt kontrolny:** skill i referencja są w zakresie; nie zawierają sekretów, niepotrzebnych danych ani niezweryfikowanych skryptów.

## 🆘 Jeśli utkniesz

| Problem | Rozwiązanie |
|---|---|
| Skill nie pojawia się w menu `/` | Sprawdź wspieraną lokalizację, nazwę katalogu równą `name`, poprawne YAML i `user-invocable`. Otwórz Configure Skills lub diagnostykę customizations. |
| Skill nie uruchamia się automatycznie | Sprawdź, czy `description` zawiera konkretne możliwości i sytuacje użycia; wywołaj ręcznie przez `/procedure-checker`. Automatyczne dopasowanie nie jest gwarantowane. |
| Skill jest niewidoczny w menu, ale ładuje się sam | Sprawdź `user-invocable: false`; ustaw `true` lub usuń pole, jeśli ma być dostępny przez slash command. |
| Skill dostępny tylko przez `/` | Sprawdź `disable-model-invocation: true`; ustaw `false` lub usuń pole, jeśli ma być dobierany automatycznie. |
| Skill się nie ładuje mimo poprawnej ścieżki | Sprawdź, czy `name` składa się z małych liter, cyfr i łączników, ma maks. 64 znaki i dokładnie zgadza się z nazwą katalogu. |
| Skill nie znajduje pliku referencji | Użyj ścieżki względnej wobec `SKILL.md` i jawnie podlinkuj plik w treści instrukcji. |
| Copilot podał niepotwierdzony fakt | Otwórz wskazany dokument, sprawdź sekcję i popraw instrukcje tak, by wymagały źródła albo odpowiedzi „brak informacji”. |

## ✔ Definicja ukończenia

- [ ] Potrafię wskazać, kiedy użyć skill zamiast promptu, instrukcji lub custom agenta.
- [ ] Utworzyłem `.github/skills/procedure-checker/SKILL.md` z prawidłową nazwą i opisem.
- [ ] Skill ma konkretne słowa i sytuacje użycia w `description`, a nazwa zgadza się z katalogiem.
- [ ] Dodałem i podlinkowałem referencję w `references/answer-format.md`.
- [ ] Uruchomiłem skill jawnie i sprawdziłem, czy brakujące informacje nie są zgadywane.
- [ ] Przetestowałem automatyczne dopasowanie i wiem, że nie jest gwarantowane.
- [ ] Przejrzałem wszystkie pliki skill przed commitem; nie ma sekretów ani prawdziwych danych.

## Dokumentacja

- [Używanie Agent Skills w VS Code](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Specyfikacja Agent Skills](https://agentskills.io/specification)