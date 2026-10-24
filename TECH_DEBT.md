# Rejestr długu technicznego

Dług zaciągamy świadomie i zapisujemy jawnie. **Wpis bez terminu to nie dług, to zapomnienie.**
W kodzie oznaczamy skrót komentarzem `# DŁUG: TD-xx …` — `grep -rn "DŁUG" app/` znajduje wszystkie miejsca.

| ID | Skrót | Ryzyko | Wpływ | Właściciel | Spłata |
|---|---|---|---|---|---|

<!--
Dopisuj wiersze w trakcie dnia (pierwszy — w Ćwiczeniu 1), np.:
| TD-01 | Brak CI (testy i skanery tylko lokalnie) | Regresje niewidoczne dla zespołu | Średni | … | D2 |
| TD-02 | Brak uwierzytelniania API | Dostęp dla każdego w sieci | Wysoki | … | D4 |
| TD-03 | Cały dokument w prompcie | Koszt, utrata treści > limit | Wysoki | … | D3 (RAG) |
| TD-04 | Brak walidacji uploadu | Path traversal, DoS | Wysoki | … | D1/D2 |
-->

## Pomiar (punkt odniesienia)

Uruchom w Bloku 4 i wpisz wyniki z datą — w Dniu 2 porównamy.

```bash
ruff check . --statistics
bandit -q -r app
gitleaks detect --source . --no-banner
pytest --cov=app --cov-report=term-missing
```

| Data | ruff (ostrzeżenia) | bandit (wys./śr./nis.) | gitleaks | pokrycie |
|---|---|---|---|---|
|  |  |  |  |  |
