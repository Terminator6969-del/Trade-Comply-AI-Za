"""
Pytest configuration and fixtures for TradeComply API tests.
"""

import asyncio
import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Async SQLAlchemy setup for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def async_engine():
    """Create an async SQLAlchemy engine for testing."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    # Create tables
    async with engine.begin() as conn:
        from app.models import Base
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Cleanup
    async with engine.begin() as conn:
        from app.models import Base
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture
async def async_session(async_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create an async SQLAlchemy session for testing."""
    async_session_maker = sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_jwt_token():
    """Create a mock JWT token for testing."""
    return "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyLWlkIiwib3JnX2lkIjoib3JnLWlkIiwiaWF0IjoxNjQwOTk1MjAwLCJleHAiOjE2NDEwODE2MDB9.HMAC-SHA256-signature"


@pytest.fixture
def mock_user_data():
    """Create mock user data for testing."""
    return {
        "email": "test@example.com",
        "password": "Test@Password123",
        "full_name": "Test User",
    }


@pytest.fixture
def mock_org_data():
    """Create mock organization data for testing."""
    return {
        "name": "Test Organization",
        "slug": "test-org",
        "plan": "free",
    }


@pytest.fixture
def mock_shipment_data():
    """Create mock shipment data for testing."""
    return {
        "reference": "SHIP-2026-001",
        "shipment_type": "import",
    }


@pytest.fixture
def mock_party_data():
    """Create mock party data for testing."""
    return {
        "party_type": "importer",
        "name": "Test Importer",
        "vat_number": "4123456789",
        "customs_code": "1234567",
    }
