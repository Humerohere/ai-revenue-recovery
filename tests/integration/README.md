# Integration tests

Require Postgres and Redis (`docker compose up -d db redis`) and are marked
`@pytest.mark.integration`. Twilio, the LLM provider, and Google Calendar are
always faked -- no test makes a real outbound call.
