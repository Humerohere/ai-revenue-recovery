# MVP Implementation Plan

Scope of the first milestone:

    Missed Call -> SMS -> AI conversation -> Lead -> Appointment -> Shop notification

## 1. Architecture

One FastAPI monolith plus one Celery worker. Postgres for state, Redis as broker
and for idempotency and rate-limit keys. Nothing else.

Webhook handlers do four things and stop: verify the Twilio signature, persist the
event for idempotency, enqueue a task, return. All slow work (AI turns, calendar
calls, outbound SMS) happens in the worker, because Twilio times out at ~15s and
retries on failure — doing it inline means duplicate texts and lost work on restart.

No Celery beat in the MVP: there are no scheduled jobs at milestone 1.

Explicitly out of scope: microservices, Kubernetes, a second queue, websockets,
GraphQL, feature flags, multi-tenancy beyond a `shop_id` foreign key.

## 2. Missed-call detection

The shop keeps its public number and sets conditional (busy / no-answer) forwarding
to a Twilio number we provision. Our voice webhook returns `<Dial>` to the shop's
real line with an `action` callback.

A call is **missed** when `DialCallStatus` is `no-answer`, `busy` or `failed`, or is
`completed` with `DialCallDuration < MISSED_CALL_MIN_SECONDS` (default 10s, which
catches voicemail pickups). Excluded: numbers on the opt-out list, and the shop's
own number. Pure function, unit-tested against recorded Twilio payloads.

## 3. Database schema

Postgres + Alembic. UUID primary keys, all timestamps `timestamptz` in UTC,
rendered in shop-local time via `shops.timezone`.

| Table | Key columns |
|---|---|
| `shops` | name, timezone, twilio_number, forward_to_number, business_hours (JSONB), slot_duration_minutes, slot_lead_time_minutes, google_calendar_id, google_refresh_token_encrypted, notify_phone, is_active |
| `users` | shop_id, email (unique), password_hash, role |
| `calls` | shop_id, twilio_call_sid (unique), from_number, to_number, dial_status, duration_seconds, is_missed, started_at |
| `leads` | shop_id, call_id, customer_phone, customer_name, vehicle_year/make/model, problem_summary, urgency, status, is_qualified, qualification_reason |
| `conversations` | shop_id, lead_id, channel, state (active/booked/closed/handoff), turn_count, last_message_at |
| `messages` | conversation_id, direction, body, provider_sid, delivery_status, ai_model, created_at |
| `appointments` | shop_id, lead_id, start_at, end_at, status, google_event_id |
| `opt_outs` | shop_id, phone (unique together) |
| `webhook_events` | provider, event_sid (unique with provider), payload JSONB |

Indexes: `messages(conversation_id, created_at)`, `leads(shop_id, status)`,
`appointments(shop_id, start_at)`, `conversations(shop_id, state)`, and a partial
unique index enforcing one open conversation per `(shop_id, customer_phone)`.

## 4. API endpoints

Twilio webhooks (signature-verified, no auth header):

- `POST /webhooks/twilio/voice` — returns TwiML dial instruction
- `POST /webhooks/twilio/voice/status` — missed-call detection, enqueue first SMS
- `POST /webhooks/twilio/sms` — inbound reply, enqueue AI turn
- `POST /webhooks/twilio/sms/status` — delivery status

Dashboard API (JWT bearer, every query scoped to `current_user.shop_id`):

- `POST /api/v1/auth/login`, `GET /api/v1/auth/me`
- `GET|PATCH /api/v1/shops/me`
- `GET /api/v1/calls`, `GET /api/v1/leads`, `GET /api/v1/leads/{id}`
- `GET /api/v1/conversations/{id}/messages`
- `GET /api/v1/appointments`
- `GET /api/v1/integrations/google/connect` then `/callback`

Ops: `GET /health`, `GET /health/ready`.

## 5. AI layer

`app/ai/base.py` defines a single `LLMProvider` protocol with one `complete()`
method. Implementations: Anthropic (default), OpenAI, and a scripted fake for
tests, selected by `AI_PROVIDER` through a factory. No vendor SDK is imported
outside `app/ai/`.

**The model never produces a price or a time.** It only calls tools, and every
tool is deterministic Python:

| Tool | Guarantee |
|---|---|
| `record_customer_info` | writes structured fields to `leads` |
| `get_available_slots` | business hours minus Calendar busy blocks; returns opaque slot ids |
| `book_appointment(slot_id)` | rejects any id not in the freshly computed set; re-validates against Calendar before writing |
| `escalate_to_human` | sets conversation to `handoff`, texts the shop |

There is deliberately no pricing tool. Turn cap `MAX_AI_TURNS` (default 12), then
automatic handoff. Qualification is a pure function, not the model's opinion.

## 6. Security and compliance

- Twilio signature validation on all four webhooks, enforced by a dependency; 403 otherwise.
- Idempotency via the `webhook_events` unique constraint; Celery tasks keyed by event sid.
- Settings from environment only. Secrets have no defaults — the app refuses to boot without them.
- Google refresh tokens encrypted at rest with Fernet (`ENCRYPTION_KEY`).
- bcrypt passwords, HS256 JWTs with 60-minute expiry.
- TCPA: STOP / UNSUBSCRIBE / CANCEL / QUIT and HELP handled before the LLM sees the
  message; opt-out list checked before every send; quiet hours (21:00–08:00
  shop-local) defer the first SMS; opt-out footer on the first outbound message.
- Structured logs with phone numbers and message bodies redacted at the formatter.
- Redis rate limit per `from_number` so an SMS loop cannot burn API spend.

## 7. Testing strategy

pytest + pytest-asyncio + httpx. Postgres and Redis from docker compose, schema
built by Alembic, each test in a rolled-back transaction. Twilio, the LLM and
Google Calendar are always faked.

- **Unit:** missed-call classification, slot generation across DST boundaries,
  qualification rules, quiet hours, opt-out parsing, signature verification.
- **Integration:** webhook to task to DB assertions; the same event sid twice sends
  one SMS; an opted-out number blocks the send; an invented `slot_id` is rejected.
- **One end-to-end test** covering the whole milestone-1 chain. That test is the
  definition of done for the MVP.

CI: ruff, ruff format, mypy, pytest against service containers.

## 8. Milestones

| # | Deliverable | Done when |
|---|---|---|
| M0 | Skeleton, config, Docker, migrations, CI | `docker compose up` boots, `/health` green, CI passes |
| M1 | Missed call to SMS | A real missed call produces exactly one SMS; retries do not duplicate |
| M2 | AI conversation to lead | Multi-turn SMS fills a `leads` row; opt-out honoured |
| M3 | Slots, booking, Calendar | Booked appointment appears on the shop's calendar; invented slots rejected |
| M4 | Shop notification + read-only dashboard | Shop gets a booking SMS; Next.js lists leads and appointments |
| M5 | Hardening, deploy, first pilot shop | One paying shop live |
