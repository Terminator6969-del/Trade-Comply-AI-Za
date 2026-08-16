You are building TradeComply AI South Africa.

Rules:
- Use TypeScript for frontend.
- Use Python 3.12 and FastAPI for backend.
- Use SQLAlchemy 2.0 typed models.
- Use Pydantic v2 schemas.
- Every API route must validate input.
- Every database query must filter by organization_id unless explicitly global.
- Never expose secrets.
- Never store plain-text passwords.
- Use audit logs for mutation actions.
- AI outputs must include confidence.
- Compliance checks must be deterministic where possible.
- Do not implement direct SARS submission.
- Add tests for critical paths.
- Keep code modular and typed.