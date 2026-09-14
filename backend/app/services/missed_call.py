"""Deterministic missed-call classification (PLAN.md s2). M0 stub -- M1.

A call is missed when DialCallStatus is no-answer/busy/failed, or completed with
DialCallDuration < settings.missed_call_min_seconds. Never an LLM decision.
"""
