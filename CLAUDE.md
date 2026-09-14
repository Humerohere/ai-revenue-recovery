# AI Revenue Recovery

## Product

We are building a SaaS/service for US auto repair shops.

The product automatically follows up with customers when a shop
misses a phone call.

The system should:

1. Detect missed calls
2. Send an immediate SMS
3. Start an AI conversation
4. Understand the customer's problem
5. Collect customer information
6. Qualify the lead
7. Offer appointment times
8. Book appointments
9. Notify the shop
10. Store the conversation and lead

## Business Goal

Reach $3,000/month with approximately 10 customers
paying ~$299/month.

## Target Customer

Independent US auto repair shops.

## Technology

Backend:
- Python
- FastAPI
- PostgreSQL
- Redis
- Celery when required

Frontend:
- Next.js/React

Infrastructure:
- Docker
- GitHub Actions

AI:
- Claude/GPT abstraction so the application is not
  permanently tied to one provider.

Communications:
- Twilio or another suitable provider.

Calendar:
- Google Calendar.

## Engineering Principles

- Do not over-engineer.
- Build the smallest production-capable MVP.
- Write tests for important business logic.
- Never hardcode secrets.
- Use environment variables.
- Use migrations.
- Use Docker for local infrastructure.
- Keep AI provider code behind an abstraction.
- Never allow the LLM to invent prices or appointments.
- Business rules must remain deterministic.
- Every major feature must have tests.
- Do not delete existing tests to make a feature pass.

## Current Stage

We are building the MVP.

The first milestone is:

Missed Call
→ SMS
→ AI conversation
→ Lead
→ Appointment
→ Shop notification
