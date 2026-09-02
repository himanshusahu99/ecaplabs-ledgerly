# Paystream webhooks

Paystream sends events to `POST /webhooks/paystream/`.

## Signature

Every request carries `X-Paystream-Signature`: the hex SHA-256 HMAC of the raw body, using the shared webhook secret (`PAYSTREAM_WEBHOOK_SECRET`). Reject anything that does not match.

## Envelope

```json
{
  "id": "evt_4f1c2a9b7d3e8a10",
  "type": "payment.created",
  "created": "2026-10-10T14:02:11.204Z",
  "data": { }
}
```

## Event types

| Type | `data` |
|---|---|
| `payment.created` | `id`, `business_id`, `payee_id`, `amount` (decimal string), `currency`, `memo`, `scheduled_for` |
| `payment.processing` | `id` |
| `payment.settled` | `id` |
| `payment.failed` | `id`, `failure_code` |
| `payment.cancelled` | `id` |

`data.id` is the Paystream payment id (`pp_...`). `payee_id` and `business_id` are our ids, which we attach as metadata when the payment is scheduled.

## Acknowledging

Respond with any 2xx to acknowledge an event.
