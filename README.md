# Ledgerly

Ledgerly is the accounts payable dashboard our customers use to see the vendor payments they send through Paystream, our payments processor, and to turn vendor invoices into payments.

- **Payments** are scheduled in Paystream. Paystream tells us about every payment and status change through signed webhooks, and we mirror them into `Payment` rows.
- **Invoices** arrive as OCR text exports. An extraction agent built on Claude reads each one, matches or creates the payee, and submits structured fields for a human to review. Approving an invoice schedules the payment in Paystream.

## Stack

- `backend/`: Django 5, Django REST Framework, Celery, SQLite locally.
- `frontend/`: React 18, TypeScript, Vite.

## Setup

Needs Python 3.10+ and Node 20+.

```bash
./setup.sh
```

This creates the virtualenv, loads an anonymised snapshot of production data (`backend/fixtures/snapshot.json`), and runs the extraction agent over the sample invoice inbox.

Run the two servers:

```bash
cd backend && .venv/bin/python manage.py runserver
cd frontend && npm run dev
```

Open http://localhost:5173. The frontend signs in as `ops@acme.test` (Acme Corp, `ECL-1001`).

### API tokens for local testing

| User | Business | Token |
|---|---|---|
| ops@acme.test | Acme Corp, ECL-1001 | `295a70dcb095570e0e2c71b3dfe93c8e22617d72` |
| finance@globex.test | Globex Ltd, ECL-1002 | `49640234e0b8ea7d44353417c2ac10f497626563` |
| ap@initech.test | Initech, ECL-1003 | `d733cf56a8f4d18c92ee36a391f52d349072d3bf` |

```bash
curl -H "Authorization: Token 295a70dcb095570e0e2c71b3dfe93c8e22617d72" localhost:8000/api/businesses/ECL-1001/payments/summary/
```

## Tests

```bash
cd backend && .venv/bin/python manage.py test
cd frontend && npm run typecheck
```

## Working with Paystream locally

There is no Paystream sandbox locally. Send yourself a signed event:

```bash
cd backend
.venv/bin/python manage.py send_test_webhook payment.settled --data '{"id": "pp_..."}'
```

Event shapes are in `docs/paystream-webhooks.md`.

## The extraction agent

Without `ANTHROPIC_API_KEY`, the agent replays recorded Claude responses from `backend/fixtures/llm_recordings/`, keyed by the sha256 of the document text, so the sample inbox works offline. A new document with no recording fails with a clear error. Set `ANTHROPIC_API_KEY` to run the agent live.

## Architecture

See `CLAUDE.md`.
