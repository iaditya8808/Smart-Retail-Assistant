# Testing Notes

Run the full test suite:

```bash
pytest
```

Run only API tests:

```bash
pytest tests/test_api.py
```

Run only ML tests:

```bash
pytest tests/test_ml_models.py
```

The API tests use FastAPI's test client. Some endpoints may return service-unavailable or fallback responses when MongoDB, Azure OpenAI, or the document retriever are not configured locally.

Before a demo, check:

- `uvicorn backend.main:app --reload` starts cleanly.
- `POST /predict` returns either local or Azure ML prediction output.
- `POST /multi-agent` returns the selected agent and response.
