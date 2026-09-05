# Local-First Automation

A sanitized reference implementation of a local-first automation backend built with FastAPI and Python.

This public repository uses synthetic events and simplified workflows to demonstrate backend engineering patterns without exposing private automation logic, production data, credentials or infrastructure details.

## Current Features

- FastAPI event ingestion
- Pydantic request validation
- separation between API and workflow layers
- retry handling for transient failures
- SQLite-backed idempotency
- health check endpoint
- structured logging

## Example Flow

```text
Synthetic Client Event
    ↓
FastAPI
    ↓
Pydantic Validation
    ↓
Workflow
    ↓
Idempotency Check
    ↓
Processing / Retry
    ↓
SQLite
    ↓
Structured Response
```

## Example Event Types

The public version uses synthetic examples such as:
- task_created
- notification_received
- sample_event

Real event names, payloads and integrations are intentionally excluded.


## Status

Under active development.

## Planned additions:
- automated testing with pytest
- Docker
- GitHub Actions CI
- deployment workflow
- improved error handling and observability