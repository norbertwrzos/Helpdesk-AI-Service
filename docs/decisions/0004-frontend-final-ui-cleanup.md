# ADR 0004 — Finalne uporządkowanie UI

**Data:** 2026-05-29  
**Status:** Accepted

## Kontekst

Frontend prototypu wymagał uporządkowania tras, nawigacji i zakresu widoków dla dwóch mockowych ról. Celem było doprowadzenie UI do spójnego stanu demonstracyjnego bez rozszerzania zakresu backendowego.

## Decyzje

### 1. Układ aplikacji

Interfejs pozostaje oparty na `AppShell` z boczną nawigacją zależną od roli, topbarem oraz przewijalnym obszarem treści.

### 2. Role i nawigacja

`agent` widzi:
- Dashboard
- Zgłoszenia
- Baza wiedzy
- AI
- Ustawienia

`end_user` widzi:
- Moje zgłoszenia (`/portal/tickets`)
- Nowe zgłoszenie (`/portal/new-ticket`)
- Profil (`/portal/profile`)
- Wylogowanie

Portal użytkownika końcowego nie posiada osobnej bazy wiedzy i nie udostępnia tras panelu agenta.

### 3. Zakres widoku Ustawienia

Strona `Settings` zawiera wyłącznie:
- Kategorie,
- Priorytety,
- Profil.

Konfiguracja kategorii i priorytetów pozwala na dodawanie i edycję bez operacji usuwania.

### 4. Analiza AI w szczegółach zgłoszenia

Analiza AI jest uruchamiana wyłącznie z widoku `/tickets/:id`, ponieważ operuje na pojedynczym zgłoszeniu i jego kontekście.

### 5. Mock auth

- brak JWT i sesji backendowej,
- wybór użytkownika na stronie logowania,
- przechowywanie roli w `localStorage`,
- ochrona tras po stronie frontendu przez `ProtectedRoute`.

### 6. Routing końcowy

```text
/login                  — publiczny
/                       — redirect zależny od roli
/dashboard              — agent
/tickets                — agent
/tickets/:id            — agent
/knowledge              — agent
/knowledge/:id          — agent
/ai                     — agent
/settings               — agent
/portal/tickets         — end_user
/portal/tickets/:id     — end_user
/portal/new-ticket      — end_user
/portal/profile         — end_user
*                       — 404
```

## Konsekwencje

- końcowy zakres UI jest zgodny z aktualnym MVP,
- panel agenta zachowuje bazę wiedzy i narzędzia AI,
- portal użytkownika końcowego został uproszczony do zgłoszeń i profilu,
- ustawienia systemu są spójne z aktywnym zakresem produktu.
