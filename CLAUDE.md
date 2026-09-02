# Ledgerly conventions

## Layers

Requests flow `view -> service -> repository -> model`. Keep each layer to its job.

- **Views** (`<app>/views/`) are thin: parse the request, call one service method, serialise the result. Business-scoped views extend `BaseBusinessView`, which checks membership of the `business_id` in the URL.
- **Services** (`<app>/services/`) hold business logic. They use repositories and clients, never the ORM directly.
- **Repositories** (`<app>/repositories/`) own every ORM query for one model.
- **Clients** (`<app>/clients/`) wrap outbound HTTP. They extend `BaseAPIClient` and raise `ExternalServiceError`.
- **Webhook processors** (`<app>/webhook_processors/`) implement `WebhookProcessorInterface`. Webhook views extend `BaseWebhookView`.
- **DTOs** (`<app>/dtos.py`) are frozen dataclasses passed between layers.
- **Choices and constants** live in `<app>/choices.py` and `<app>/constants.py`. No string literals for statuses or event types.
- **Celery tasks** (`<app>/tasks.py`) stay thin and call a service.

## Style

- Keyword-only arguments on our own functions and methods.
- One-line docstrings. No inline comments.
- Money is `Decimal` end to end, serialised as strings.
- Tests live in `<app>/tests/`, and builders in `<app>/tests/factories.py`.

## Apps

- `core`: businesses, membership, base classes, shared utils.
- `payments`: payees, payments, Paystream webhooks, notifications.
- `invoices`: invoice uploads and the Claude extraction agent (`invoices/agents/`, prompt and tools in `invoices/prompts/`).
