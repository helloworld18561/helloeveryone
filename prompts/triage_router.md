# Triage Router Prompt

This prompt will be used by the event triage router agent to classify incoming events based on urgency and type.

{{user_event_description}}

### Instructions
- Review the event description and metadata.
- Assign the event to categories P0, P1, or P3 based on the trigger matrix.
- Return a summary and recommended queue.
