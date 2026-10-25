# Tutorial — projektowanie custom agents w GitHub Copilot

| | |
|---|---|
| **Czas** | 90 min |
| **Poziom** | Osoba znająca podstawy pracy z Copilot Chat i repozytorium Git |
| **Cel** | Zaprojektować custom agenta z dobrym opisem, ograniczonymi narzędziami i kontrolowanym handoffem |
| **Wejście** | VS Code z dostępem do GitHub Copilot, otwarty folder repozytorium |
| **Rezultat** | `.github/agents/docs-planner.agent.md` oraz sprawdzony plan i handoff w harnessie Local |

Ćwiczenie dotyczy custom agents w VS Code i używa harnessu **Local**, ponieważ handoffy opisane tutaj są obsługiwane w Local. W Copilot harness konfiguracja custom agents działa inaczej, a handoffy z tego formatu nie mają zastosowania. Local wybiera się jako **harness** w Chat view; nie jest to nazwa modelu ani agenta. Local nie jest dostępny w Agents window.

Custom agent jest przydatny dla powtarzalnej roli, która potrzebuje własnych instrukcji albo innego zestawu narzędzi, np. planowania zmian lub przeglądu bezpieczeństwa. Nie zastępuje promptu do jednorazowego zadania ani instrukcji, które mają obowiązywać zawsze.

## Krok 0 — Przygotuj czyste drzewo i Local (10 min)

Otwórz Chat view w VS Code, rozpocznij nową sesję i w **Session Target** wybierz `Local`. Sprawdź, czy jesteś zalogowany do GitHub Copilot. W terminalu:

```bash
git status --short
git switch -c tutorial/custom-agent-design
```

Przed rozpoczęciem drzewo powinno być czyste. Jeśli widzisz wcześniejsze zmiany, zachowaj je zgodnie z zasadami zespołu i wróć do ćwiczenia na czystym drzewie; niczego nie usuwaj na potrzeby tutoriala.

✅ **Punkt kontrolny:** w Chat view widać harness `Local`, a `git status --short` przed utworzeniem gałęzi nie pokazuje zmian.

## Krok 1 — Opisz rolę i moment użycia (15 min)

Zaprojektujesz **Docs Planner**: agenta, który czyta repozytorium i przygotowuje plan zmian dokumentacji, ale nie edytuje plików.

Zanim napiszesz frontmatter, uzupełnij te zdania:

1. **Rola:** planuje zmiany README i dokumentacji repozytorium.
2. **Użyj, gdy:** trzeba zmienić strukturę dokumentacji, instrukcję uruchomienia albo opis projektu.
3. **Nie używaj, gdy:** zadanie wymaga implementacji kodu aplikacji lub bezpośredniej edycji plików.
4. **Wynik:** cel, pliki w zakresie, kroki, ryzyka i kryteria akceptacji.

### Słowa kluczowe i `description`

W schemacie custom agentów VS Code **nie ma osobnego pola `keywords`**. Frazy opisujące zadanie umieszczaj w `description`, na przykład `README updates`, `documentation structure` i `editorial review`. Opis mówi, co agent robi i kiedy go użyć; pomaga rozpoznać właściwą rolę, ale nie gwarantuje automatycznego wyboru na podstawie jednego słowa. W ćwiczeniu agenta wybierzesz ręcznie z pickera.

Unikaj ogólnych opisów typu `Helpful coding agent`. Opisz konkretną pracę i najważniejsze granice. Jeśli opis zawiera dwukropek, ujmij całą wartość w cudzysłów, np. `description: "Use when: planning documentation changes"`.

✅ **Punkt kontrolny:** `description` pozwala odróżnić planowanie dokumentacji od implementacji kodu; nie dodano nieobsługiwanego pola `keywords`.

## Krok 2 — Zrozum plik i pola frontmatter (20 min)

Workspace custom agents w formacie VS Code umieszcza się w `.github/agents/`. Nazwa pliku kończy się na `.agent.md`. Plik składa się z opcjonalnego nagłówka YAML ograniczonego liniami `---` oraz treści Markdown z instrukcjami. W YAML używaj spacji, nie tabulatorów.

Najważniejsze pola nagłówka:

| Pole | Do czego służy | Wskazówka |
|---|---|---|
| `name` | Nazwa widoczna w interfejsie | Krótka, rozpoznawalna nazwa roli. |
| `description` | Co agent robi i kiedy go użyć | Dodaj konkretne sytuacje użycia i granice; to tutaj zapisuj frazy, których szukasz. |
| `argument-hint` | Podpowiedź dla osoby wpisującej zadanie | Opisz potrzebny kontekst, nie reguły agenta. |
| `tools` | Narzędzia dostępne agentowi | Przyznawaj tylko potrzebne; nazwy i obsługa zależą od harnessu. |
| `model` | Preferowany model lub lista preferencji | Opcjonalne; bez niego używany jest bieżący wybór. Nie wiąż agenta z modelem bez potrzeby. |
| `reasoning-effort` | Poziom wysiłku rozumowania | Zależne od modelu i harnessu; pomiń w przenośnym przykładzie Local. |
| `user-invocable` | Widoczność w pickerze | `false` ukrywa agenta z pickera, np. dla pomocniczego subagenta. |
| `disable-model-invocation` | Możliwość wywołania przez innego agenta jako subagenta | Niezależne od widoczności w pickerze. |
| `agents` | Lista agentów dostępnych jako subagenci | W Local wymaga narzędzia `agent`; nie jest potrzebne w tym ćwiczeniu. |
| `handoffs` | Przyciski przejścia do kolejnego agenta | W tym formacie obsługiwane przez Local. Szczegóły w kroku 5. |
| `target` | Docelowe środowisko, np. `vscode` lub `github-copilot` | To nie jest wybór harnessu. Pomijamy, jeśli nie konfigurujemy konkretnego targetu. |
| `mcp-servers` | Serwery MCP dla Copilot cloud agent | Nie jest używane przez custom agents w VS Code Local. |
| `hooks` | Akcje związane z cyklem życia narzędzi | Zaawansowany temat; obsługa zależy od harnessu i konfiguracji. |
| `infer` | Starsze sterowanie widocznością i wywoływaniem | Przestarzałe; używaj osobno `user-invocable` i `disable-model-invocation`. |

Nie dopisuj wszystkich pól do każdego agenta. Użyj tylko tych, które zmieniają jego widoczność, możliwości albo zachowanie. Pole `tools` powinno respektować zasadę najmniejszych uprawnień: jeśli agent ma tylko planować i recenzować, nie dawaj mu narzędzi edycji.

W Local lista `tools` ogranicza narzędzia dostępne agentowi. Bez tej listy dostępne są narzędzia z tool pickera. Aliasy takie jak `read` i `search` oraz ich dostępność zależą od środowiska; inne harnessy mogą mieć inne nazwy i możliwości. Przed przeniesieniem pliku sprawdź ich obsługę.

### Widoczność a wywołanie jako subagent

- `user-invocable: true` pokazuje agenta w pickerze; to wartość domyślna.
- `user-invocable: false` ukrywa go w pickerze, ale samo w sobie nie blokuje użycia jako subagenta.
- `disable-model-invocation: true` blokuje wywołanie przez innego agenta jako subagenta; nie ukrywa agenta przed użytkownikiem.
- `infer` jest przestarzałe i nie należy go używać w nowych plikach.

✅ **Punkt kontrolny:** umiesz wyjaśnić, dlaczego agent planujący ma `tools: ['read', 'search']`, a widoczność w pickerze jest niezależna od wywołania jako subagent.

## Krok 3 — Napisz instrukcje agenta (15 min)

Treść Markdown to kontrakt agenta. Powinna podawać rolę, zakres, sposób pracy i format odpowiedzi. Zamiast „bądź dokładny”, napisz, jakie pliki ma sprawdzić, jak ma rozróżniać fakty od założeń i jak ma wyglądać plan. Ograniczenia w treści wspierają zachowanie, ale nie zastępują ograniczeń narzędzi.

Utwórz `.github/agents/docs-planner.agent.md`:

```markdown
---
name: Docs Planner
description: >-
  Plan changes to repository documentation. Use for README updates,
  documentation structure, setup instructions, and editorial review.
  Do not use for implementing application code.
argument-hint: Describe the documentation change and its acceptance criteria
tools: ['read', 'search']
user-invocable: true
disable-model-invocation: true
handoffs:
  - label: Implement reviewed plan
    agent: agent
    prompt: Implement only the plan approved above. Keep changes within its stated scope, run relevant checks, and summarize the diff.
    send: false
---
You plan repository documentation changes; you do not edit files.

Inspect the relevant documentation and repository guidance.
Separate verified facts from assumptions.
Do not invent commands, files, dependencies, or project behavior.
Return a concise plan with: goal, files in scope, steps, risks, and acceptance checks.
Do not start implementation. The user must review the plan first.
```

`name` to etykieta w UI, a nazwa pliku to ścieżka zapisu. `argument-hint` jest krótką podpowiedzią w polu czatu. W treści nie umieszczaj sekretów ani danych klientów. W tym przykładzie `send: false` wymaga ręcznego sprawdzenia promptu przekazania.

✅ **Punkt kontrolny:** agent ma krótki, konkretny opis, czytelny zakres i format odpowiedzi; dostępne mu narzędzia są tylko do odczytu.

## Krok 4 — Testuj wybór i granice agenta (15 min)

Zapisz plik, upewnij się, że harness nadal wskazuje `Local`, a następnie wybierz **Docs Planner** z pickera. Poproś go o plan poprawy instrukcji startu w README:

```text
Przygotuj plan poprawy instrukcji startu projektu dla nowej osoby.
Uwzględnij sekcję README.md, sprawdź istniejące polecenia i nie proponuj nowych zależności.
```

Sprawdź odpowiedź z plikami repozytorium. Czy agent wskazał faktyczne ścieżki i kryteria akceptacji? Czy nie zaczął edytować? Następnie podaj mu prośbę spoza zakresu, np. dodanie endpointu FastAPI. Powinien wskazać, że to zadanie implementacyjne, a nie przygotować kod.

Jeśli agent nie pojawia się w pickerze, sprawdź lokalizację `.github/agents/`, końcówkę `.agent.md`, separatory YAML i diagnostykę customizations. Jeśli nie widzisz Local, sprawdź Chat view oraz polityki i ustawienia VS Code; dostępność harnessu może zależeć od środowiska.

✅ **Punkt kontrolny:** Docs Planner jest wybieralny, tworzy plan bez zmian plików i nie udaje implementera.

## Krok 5 — Zaprojektuj i użyj handoffu (10 min)

Handoff to kontrolowany następny krok, nie automatyczne przekazanie sterowania. Po odpowiedzi agenta Local pokazuje przycisk z `label`. Wybór przełącza rozmowę do wskazanego `agent`, przenosi kontekst i wypełnia `prompt`.

Pola handoffu:

| Pole | Wymagane | Znaczenie |
|---|---|---|
| `label` | Tak | Tekst przycisku. Opisz rezultat, np. `Implement reviewed plan`. |
| `agent` | Tak | Identyfikator agenta docelowego, np. wbudowanego `agent`. |
| `prompt` | Tak | Instrukcja wypełniana przy przejściu. Ogranicz zakres i określ weryfikację. |
| `send` | Nie | `send: false` (domyślnie) pozwala sprawdzić prompt przed wysłaniem; `send: true` wysyła go automatycznie. |
| `model` | Nie | Opcjonalny model dla następnego kroku, jeśli dostępny; w ćwiczeniu pomijamy. |

Wybierz **Implement reviewed plan**. Przeczytaj wypełniony prompt i upewnij się, że akceptujesz plan oraz zakres, dopiero potem wyślij go do agenta implementującego. Jeśli handoff nie pojawia się, sprawdź, czy aktywny jest Local harness: handoffy z tego pliku nie działają w Copilot harness.

### Handoff a subagent

- **Handoff:** użytkownik widzi przycisk, zatwierdza przejście, a aktywny agent się zmienia.
- **Subagent:** agent deleguje pracę innemu agentowi jako część własnego zadania; nie jest to przycisk do ręcznego zatwierdzenia kolejnego etapu.

Nie dodawaj równocześnie konfiguracji `agents` tylko dlatego, że plik ma handoff. To dwa różne mechanizmy.

✅ **Punkt kontrolny:** prompt handoffu jest widoczny przed wysłaniem i prowadzi do implementacji dopiero po Twoim zatwierdzeniu.

## Krok 6 — Przegląd i podsumowanie (5 min)

Sprawdź zmiany:

```bash
git status --short
git diff -- .github/agents/docs-planner.agent.md
```

Nowy plik może być jeszcze nieśledzony i wtedy zwykły `git diff` go nie pokaże. Otwórz go bezpośrednio w edytorze albo dodaj go jawnie i obejrzyj staged diff:

```bash
git add .github/agents/docs-planner.agent.md
git diff --cached -- .github/agents/docs-planner.agent.md
git diff --cached --check
```

Omów z partnerem: które frazy dodałeś do `description`, jakie narzędzie celowo pominąłeś, co sprawdziłeś przed handoffem i dlaczego `send` pozostało `false`.

## 🆘 Jeśli utkniesz

| Problem | Rozwiązanie |
|---|---|
| Agent nie pojawia się w pickerze | Sprawdź `.github/agents/`, rozszerzenie `.agent.md`, poprawne separatory YAML i ustawienie `user-invocable`. |
| Agent nie jest wybierany przy zadaniu opisanym słowem z `description` | Wybierz go ręcznie w pickerze; opis nie gwarantuje automatycznego routingu. |
| YAML nie ładuje się poprawnie | Użyj spacji, sprawdź wcięcia listy `handoffs` i poprawne separatory. |
| Agent może edytować mimo roli planera | Sprawdź `tools` i aktywny harness; treść „nie edytuj” sama nie ogranicza uprawnień. |
| Nie ma przycisku handoffu | Upewnij się, że używasz Local harness; sprawdź wymagane pola `label`, `agent`, `prompt` i poprawny YAML. |
| Wybór handoffu od razu wysyła prompt | Ustaw `send: false` lub usuń pole `send`; sprawdź prompt przed ręcznym wysłaniem. |
| Agent jest ukryty, ale ma być wybierany ręcznie | Ustaw `user-invocable: true` albo usuń to pole. `disable-model-invocation` steruje inną możliwością. |

## ✔ Definicja ukończenia

- [ ] Agent znajduje się w `.github/agents/docs-planner.agent.md` i poprawnie ładuje się w Local.
- [ ] `description` zawiera konkretne przypadki użycia; nie dodano pola `keywords`.
- [ ] Agent przygotowuje plan, nie edytuje plików i ma tylko narzędzia potrzebne do odczytu.
- [ ] Potrafię wyjaśnić różnicę między `user-invocable` i `disable-model-invocation` oraz między handoffem i subagentem.
- [ ] Handoff prowadzi do wbudowanego agenta implementującego, a prompt jest sprawdzany przed wysłaniem.
- [ ] Diff został przejrzany; tutorial nie wymaga nowych zależności ani sekretów.

## Dokumentacja

- [Custom agents w VS Code](https://code.visualstudio.com/docs/agent-customization/custom-agents)
- [Referencja pliku custom agent](https://code.visualstudio.com/docs/agents/reference/custom-agent-file-reference)
- [Wybór harnessu w VS Code](https://code.visualstudio.com/docs/agents/run/agent-harnesses)