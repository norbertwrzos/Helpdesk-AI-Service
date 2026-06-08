# Frontend — Helpdesk AI Service

Frontend React + TypeScript + Vite dla panelu agenta i portalu użytkownika końcowego.

## Uruchomienie

```bash
npm install
npm run dev
```

Domyślny adres dev servera: http://localhost:5173

## Build produkcyjny

```bash
npm run build
npm run preview
```

## Zakres UI

- agent: Dashboard, Zgłoszenia, Baza wiedzy, AI, Ustawienia,
- end_user: Moje zgłoszenia, Nowe zgłoszenie, Profil,
- Ustawienia: Kategorie, Priorytety, Profil.

## Proxy API

Vite proxy przekierowuje wywołania `/api/*` do backendu pod `http://localhost:8000`.
