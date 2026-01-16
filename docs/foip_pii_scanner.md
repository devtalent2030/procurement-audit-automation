# FOIP / PII Scanner (NLP/NER)

## Goal
Detect potential FOIP/privacy risks in unstructured procurement notes before archiving or distributing reports.

## Example risks flagged
- personal names
- email addresses
- phone numbers
- “confidential / do not disclose” keywords

## Approach
- Rule-based keyword checks (fast)
- NLP/NER model for entity detection (future extension)
