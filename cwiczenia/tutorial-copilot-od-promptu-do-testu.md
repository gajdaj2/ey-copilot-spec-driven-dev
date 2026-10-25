# Tutorial — od podpowiedzi do testu z GitHub Copilot

| | |
|---|---|
| **Czas** | 90 min |
| **Poziom** | Początkujący użytkownik Copilota, podstawy Pythona i terminala |
| **Cel** | Przećwiczyć Inline Suggestions, Ask, Plan i Agent na małym, lokalnym zadaniu |
| **Wejście** | Repozytorium po instalacji zależności developerskich, VS Code i zalogowany GitHub Copilot |
| **Rezultat** | `app/text_utils.py` z funkcją `normalize_question` oraz testy w `tests/test_text_utils.py` |

Tutorial nie wymaga `.env`, klucza do LLM ani nowych zależności. Rozszerzenie GitHub Copilot wymaga dostępu do Copilota. Polecenia i ścieżki są takie same w Windows, macOS i Linux.

## Krok 0 — Przygotowanie (10 min)

Otwórz w VS Code folder repozytorium i sprawdź, czy Copilot jest zalogowany. W terminalu:

```bash
git status --short
git switch -c tutorial/copilot-basics
```

Przed rozpoczęciem `git status --short` powinien być pusty. Jeśli pokazuje wcześniejsze zmiany, nie zaczynaj tutoriala na tym drzewie: zachowaj je zgodnie z zasadami zespołu i wróć do ćwiczenia na czystym drzewie. Nie usuwaj cudzych ani własnych zmian na potrzeby tutoriala. Upewnij się, że aktywny interpreter ma zainstalowane zależności developerskie z `pyproject.toml`.

W tym tutorialu:

- **Inline Suggestions** podpowiadają kod w edytorze; `Tab` akceptuje widoczną podpowiedź, `Esc` ją odrzuca.
- **Ask** wyjaśnia i odpowiada, ale nie powinien edytować plików.
- **Plan** proponuje kolejność prac, bez implementacji.
- **Agent** może zmieniać pliki; po pracy sprawdzamy jego diff.

Nazwy i położenie kontrolek mogą się różnić zależnie od wersji VS Code. W razie wątpliwości użyj pola wyboru trybu w Copilot Chat.

## Krok 1 — Ask: zrozum istniejący test (15 min)

W Copilot Chat wybierz **Ask** i wklej:

```text
▶ Copilot (Ask)
#file:tests/test_environment.py
Wyjaśnij test_env_is_ignored_by_git własnymi słowami:
co uruchamia, po czym rozpoznaje sukces i dlaczego ten test jest przydatny.
Nie edytuj plików i nie zakładaj, że uruchomiłeś test.
```

Sprawdź odpowiedź w `tests/test_environment.py`. Odszukaj `git check-ignore` i warunek sprawdzający kod zakończenia procesu.

✅ **Punkt kontrolny:** potrafisz wskazać w kodzie, jak test sprawdza, że `.env` jest ignorowany przez Git. Jeśli odpowiedź Copilota nie zgadza się ze źródłem, pierwszeństwo ma kod.

## Krok 2 — Inline Suggestions: mała funkcja (15 min)

W eksploratorze VS Code utwórz `app/text_utils.py`. Wpisz sygnaturę i docstring:

```python
def normalize_question(text: str) -> str:
    """Trim and collapse whitespace in a question."""
```

W kolejnej linii wpisz komentarz opisujący zachowanie, a pod nim poproś Inline Suggestions o uzupełnienie funkcji:

```python
    # Trim both ends and replace every run of whitespace with one space.
```

Przeczytaj podpowiedź, zanim ją zaakceptujesz. Powinna zwracać tekst bez białych znaków na brzegach i z pojedynczymi spacjami pomiędzy słowami. Dla pustego lub zawierającego wyłącznie białe znaki wejścia powinna zwrócić `""`. W Pythonie można to uzyskać przez `" ".join(text.split())`.

✅ **Punkt kontrolny:** sprawdź ręcznie wynik dla `"  zmiana   adresu  "` oraz `"   "`. Odrzuć podpowiedź, jeśli nie spełnia kryteriów; możesz wpisać poprawne rozwiązanie samodzielnie.

## Krok 3 — Plan: zaprojektuj testy (15 min)

W Copilot Chat wybierz **Plan** i wklej:

```text
▶ Copilot (Plan)
Zaplanuj testy pytest dla app.text_utils.normalize_question.
Uwzględnij zwykły tekst, białe znaki na początku i końcu,
wiele spacji pomiędzy słowami oraz tekst pusty i z samych białych znaków.
Wypisz oczekiwane wejścia i wyniki oraz plik, który trzeba utworzyć.
Nie edytuj żadnych plików i nie dodawaj zależności.
```

Oceń plan: czy każdy przypadek ma jednoznaczny oczekiwany wynik? Zanim przejdziesz dalej, dopisz brakujący przypadek albo doprecyzuj wynik.

✅ **Punkt kontrolny:** plan obejmuje co najmniej zwykły tekst, normalizację spacji i pusty wynik; pliki nie zostały zmienione przez tryb Plan.

## Krok 4 — Agent: utwórz testy (20 min)

Wybierz **Agent** i wklej zaakceptowany plan jako kontekst razem z ograniczeniami:

```text
▶ Copilot (Agent)
Utwórz tests/test_text_utils.py dla istniejącej funkcji
app.text_utils.normalize_question, zgodnie z tym planem:
[wklej zaakceptowany plan]

Ograniczenia: zmień lub utwórz wyłącznie tests/test_text_utils.py.
Nie zmieniaj app/text_utils.py, innych testów ani zależności.
Testuj zachowanie funkcji, nie jej szczegóły implementacyjne.
```

Przejrzyj diff. Sprawdź, czy testy asercjami opisują uzgodnione wejścia i wyniki. Następnie uruchom:

```bash
pytest -q
```

✅ **Punkt kontrolny:** wszystkie testy są zielone, a zmiany Agenta ograniczają się do `tests/test_text_utils.py`.

## Krok 5 — Przegląd i poprawka (10 min)

Sprawdź zmiany i białe znaki:

```bash
git status --short
git add app/text_utils.py tests/test_text_utils.py
git diff --cached -- app/text_utils.py tests/test_text_utils.py
git diff --cached --check
```

Jeśli test nie przechodzi, najpierw przeczytaj traceback i porównaj rzeczywisty wynik z kryterium. Potem poproś Agenta o poprawę implementacji, nie testu:

```text
▶ Copilot (Agent)
Oto wynik pytest: [wklej traceback bez sekretów].
Moja hipoteza: [napisz, co według Ciebie jest przyczyną].
Sprawdź ją i popraw wyłącznie app/text_utils.py.
Nie zmieniaj testów ani zależności. Wyjaśnij krótko przyczynę.
```

Ponownie uruchom `pytest -q` i sprawdź diff. Nie akceptuj zmiany asercji tylko po to, by test przeszedł.

## Krok 6 — Podsumowanie (5 min)

Omów z partnerem lub zapisz:

1. Który tryb najlepiej pasował do wyjaśnienia, planowania i edycji?
2. Którą podpowiedź zaakceptowałeś, a którą odrzuciłeś i dlaczego?
3. Co sprawdziłeś samodzielnie przed uznaniem wyniku Agenta?

Po sprawdzeniu testów i diffu możesz zapisać wynik:

```bash
git add app/text_utils.py tests/test_text_utils.py
git commit -m "tutorial: normalize questions with Copilot"
```

## 🆘 Jeśli utkniesz

| Problem | Rozwiązanie |
|---|---|
| Copilot Chat prosi o zalogowanie | Zaloguj się na konto z dostępem do GitHub Copilot i ponownie otwórz czat. |
| Nie widzę trybu Ask, Plan lub Agent | Sprawdź picker trybu Copilot Chat i aktualizację rozszerzeń VS Code/Copilot Chat. |
| Nie pojawia się Inline Suggestion | Sprawdź, czy Copilot jest aktywny dla pliku Python; wpisz komentarz opisujący oczekiwany kod i chwilę poczekaj. |
| `ModuleNotFoundError` dla `app.text_utils` | Uruchom `pytest` z katalogu głównego repozytorium i sprawdź, czy istnieje `app/__init__.py`. |
| Test pokazuje nieoczekiwane spacje | Sprawdź, czy implementacja obsługuje dowolne białe znaki; `str.split()` bez separatora dzieli po ich ciągach. |
| Agent zmienił dodatkowe pliki | Nie akceptuj niechcianych zmian. Przywróć tylko niechciane pliki, które powstały w tej sesji, i ponów zadanie z dokładnym ograniczeniem zakresu. |

## ✔ Definicja ukończenia

- [ ] Wyjaśniłem istniejący test w trybie Ask i zweryfikowałem odpowiedź w kodzie.
- [ ] Funkcja `normalize_question` obsługuje zwykły tekst oraz puste i wielokrotne białe znaki.
- [ ] Testy obejmują uzgodnione przypadki i `pytest -q` przechodzi.
- [ ] Przejrzałem diff; zmiany dotyczą tylko `app/text_utils.py` i `tests/test_text_utils.py`.
- [ ] Nie dodano zależności ani sekretów.