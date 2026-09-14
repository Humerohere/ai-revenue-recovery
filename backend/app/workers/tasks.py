"""Celery tasks.

M0 stub. Planned tasks:
  send_missed_call_sms(call_id)    -- M1
  handle_inbound_sms(message_id)   -- M2
  notify_shop_of_booking(appt_id)  -- M4

Every task must be idempotent: it is keyed by the originating webhook event sid.
"""
