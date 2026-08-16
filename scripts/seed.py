"""
Database seeding script for TradeComply AI South Africa.

Seeds:
  1. Real South African Schedule 1 tariff records (HS codes for high-risk / high-volume
     verticals: solar & energy storage, textiles/apparel, steel & industrial equipment,
     chemicals & dangerous goods, electronics, automotive, agriculture).
  2. Demo organization + admin user (admin@demo.com / demo-password-123)
  3. Demo trade parties (clearing agent, overseas supplier, SA importer)
  4. Demo shipments + line items for testing classification & compliance

Usage:
    # From workspace root
    python scripts/seed.py
    # Or using uv
    uv run --project apps/api python scripts/seed.py
"""

import asyncio
import os
import sys
from datetime import datetime, date
from uuid import uuid4

# Ensure app package is importable
_repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_repo_root, "apps", "api"))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.core.security import get_password_hash
from app.models import (
    Organization,
    User,
    Membership,
    Party,
    Shipment,
    LineItem,
    TariffRecord,
)

# ---------------------------------------------------------------------------
# South African Tariff Data
# ---------------------------------------------------------------------------
TARIFF_RECORDS = [
    # Solar & Energy Storage (Chapter 85)
    {
        "hs_code": "8541.40",
        "sa_tariff_code": "8541.40.10",
        "description": "Photovoltaic cells, modules and panels (solar panels)",
        "duty_rate": 0.0,
        "vat_rate": 15.0,
        "unit_of_measure": "u",
        "chapter": "85",
        "section": "XVI",
    },
    {
        "hs_code": "8541.43",
        "sa_tariff_code": "8541.43.00",
        "description": "Photovoltaic cells assembled in modules or made up into panels — other",
        "duty_rate": 0.0,
        "vat_rate": 15.0,
        "unit_of_measure": "u",
        "chapter": "85",
        "section": "XVI",
    },
    {
        "hs_code": "8507.60",
        "sa_tariff_code": "8507.60.10",
        "description": "Lithium-ion batteries and battery packs for energy storage",
        "duty_rate": 5.0,
        "vat_rate": 15.0,
        "unit_of_measure": "u",
        "chapter": "85",
        "section": "XVI",
    },
    {
        "hs_code": "8507.80",
        "sa_tariff_code": "8507.80.20",
        "description": "Other electric accumulators, including battery storage packs",
        "duty_rate": 5.0,
        "vat_rate": 15.0,
        "unit_of_measure": "u",
        "chapter": "85",
        "section": "XVI",
    },
    {
        "hs_code": "8504.40",
        "sa_tariff_code": "8504.40.10",
        "description": "Static converters — inverters (solar / UPS hybrid inverters)",
        "duty_rate": 0.0,
        "vat_rate": 15.0,
        "unit_of_measure": "u",
        "chapter": "85",
        "section": "XVI",
    },
    {
        "hs_code": "8544.42",
        "sa_tariff_code": "8544.42.10",
        "description": "Insulated electric conductors fitted with connectors, voltage ≤1000V",
        "duty_rate": 5.0,
        "vat_rate": 15.0,
        "unit_of_measure": "m",
        "chapter": "85",
        "section": "XVI",
    },
    {
        "hs_code": "8536.50",
        "sa_tariff_code": "8536.50.10",
        "description": "Other switches, voltage ≤1000V — isolators, circuit breakers",
        "duty_rate": 0.0,
        "vat_rate": 15.0,
        "unit_of_measure": "u",
        "chapter": "85",
        "section": "XVI",
    },
    {
        "hs_code": "8539.50",
        "sa_tariff_code": "8539.50.10",
        "description": "LED lamps — light-emitting diode lamps (NRCS LOA required)",
        "duty_rate": 20.0,
        "vat_rate": 15.0,
        "unit_of_measure": "u",
        "chapter": "85",
        "section": "XVI",
    },
    # Textiles & Apparel (Chapters 61, 62, 64)
    {
        "hs_code": "6109.10",
        "sa_tariff_code": "6109.10.10",
        "description": "T-shirts, singlets and similar garments of cotton (knitted)",
        "duty_rate": 45.0,
        "vat_rate": 15.0,
        "unit_of_measure": "u",
        "chapter": "61",
        "section": "XI",
    },
    {
        "hs_code": "6110.20",
        "sa_tariff_code": "6110.20.10",
        "description": "Jerseys, pullovers, sweatshirts of cotton (knitted)",
        "duty_rate": 45.0,
        "vat_rate": 15.0,
        "unit_of_measure": "u",
        "chapter": "61",
        "section": "XI",
    },
    {
        "hs_code": "6203.42",
        "sa_tariff_code": "6203.42.10",
        "description": "Men's trousers and bib-and-brace overalls of cotton (woven denim/workwear)",
        "duty_rate": 40.0,
        "vat_rate": 15.0,
        "unit_of_measure": "u",
        "chapter": "62",
        "section": "XI",
    },
    {
        "hs_code": "6204.62",
        "sa_tariff_code": "6204.62.10",
        "description": "Women's trousers / jeans of cotton (woven)",
        "duty_rate": 45.0,
        "vat_rate": 15.0,
        "unit_of_measure": "u",
        "chapter": "62",
        "section": "XI",
    },
    {
        "hs_code": "6403.99",
        "sa_tariff_code": "6403.99.10",
        "description": "Footwear with outer soles of rubber/plastics/leather",
        "duty_rate": 30.0,
        "vat_rate": 15.0,
        "unit_of_measure": "pr",
        "chapter": "64",
        "section": "XII",
    },
    # Steel & Industrial Equipment (Chapters 72, 73, 84 - ITAC sensitive)
    {
        "hs_code": "7213.10",
        "sa_tariff_code": "7213.10.10",
        "description": "Bars and rods of iron/steel, hot-rolled, with indentations (rebar)",
        "duty_rate": 10.0,
        "vat_rate": 15.0,
        "unit_of_measure": "kg",
        "chapter": "72",
        "section": "XV",
    },
    {
        "hs_code": "7208.51",
        "sa_tariff_code": "7208.51.10",
        "description": "Flat-rolled iron/steel, hot-rolled, ≥10mm thick (steel plates)",
        "duty_rate": 10.0,
        "vat_rate": 15.0,
        "unit_of_measure": "kg",
        "chapter": "72",
        "section": "XV",
    },
    {
        "hs_code": "7306.30",
        "sa_tariff_code": "7306.30.10",
        "description": "Other tubes, pipes, hollow profiles of iron/steel, welded, circular",
        "duty_rate": 10.0,
        "vat_rate": 15.0,
        "unit_of_measure": "kg",
        "chapter": "73",
        "section": "XV",
    },
    {
        "hs_code": "8413.70",
        "sa_tariff_code": "8413.70.10",
        "description": "Centrifugal pumps for liquids (industrial water pumps)",
        "duty_rate": 5.0,
        "vat_rate": 15.0,
        "unit_of_measure": "u",
        "chapter": "84",
        "section": "XVI",
    },
    {
        "hs_code": "8421.39",
        "sa_tariff_code": "8421.39.10",
        "description": "Filtering or purifying machinery for liquids or gases",
        "duty_rate": 0.0,
        "vat_rate": 15.0,
        "unit_of_measure": "u",
        "chapter": "84",
        "section": "XVI",
    },
    {
        "hs_code": "8471.30",
        "sa_tariff_code": "8471.30.10",
        "description": "Portable automatic data processing machines (laptops)",
        "duty_rate": 0.0,
        "vat_rate": 15.0,
        "unit_of_measure": "u",
        "chapter": "84",
        "section": "XVI",
    },
    # Chemicals & Dangerous Goods (Chapters 27, 29, 38)
    {
        "hs_code": "2915.21",
        "sa_tariff_code": "2915.21.00",
        "description": "Acetic acid (glacial acetic acid) — Dangerous Goods UN2789 Class 8/3",
        "duty_rate": 0.0,
        "vat_rate": 15.0,
        "unit_of_measure": "kg",
        "chapter": "29",
        "section": "VI",
    },
    {
        "hs_code": "3808.91",
        "sa_tariff_code": "3808.91.10",
        "description": "Insecticides — preparations for agricultural/retail sale",
        "duty_rate": 10.0,
        "vat_rate": 15.0,
        "unit_of_measure": "kg",
        "chapter": "38",
        "section": "VI",
    },
    {
        "hs_code": "2710.12",
        "sa_tariff_code": "2710.12.10",
        "description": "Light oils and petroleum preparations (petrol/gasoline)",
        "duty_rate": 0.0,
        "vat_rate": 15.0,
        "unit_of_measure": "l",
        "chapter": "27",
        "section": "V",
    },
    # Automotive (Chapter 87)
    {
        "hs_code": "8703.23",
        "sa_tariff_code": "8703.23.10",
        "description": "Passenger motor vehicles, engine 1500cc to 3000cc",
        "duty_rate": 25.0,
        "vat_rate": 15.0,
        "unit_of_measure": "u",
        "chapter": "87",
        "section": "XVII",
    },
    {
        "hs_code": "8708.99",
        "sa_tariff_code": "8708.99.90",
        "description": "Motor vehicle parts and accessories, other",
        "duty_rate": 20.0,
        "vat_rate": 15.0,
        "unit_of_measure": "u",
        "chapter": "87",
        "section": "XVII",
    },
    # Agriculture (Zero VAT items)
    {
        "hs_code": "1001.99",
        "sa_tariff_code": "1001.99.10",
        "description": "Wheat and meslin — other grain (zero-rated VAT)",
        "duty_rate": 0.0,
        "vat_rate": 0.0,
        "unit_of_measure": "kg",
        "chapter": "10",
        "section": "II",
    },
    {
        "hs_code": "0805.10",
        "sa_tariff_code": "0805.10.10",
        "description": "Fresh oranges (citrus fruit)",
        "duty_rate": 10.0,
        "vat_rate": 0.0,
        "unit_of_measure": "kg",
        "chapter": "08",
        "section": "II",
    },
]

# ---------------------------------------------------------------------------
# Demo Seed Entities
# ---------------------------------------------------------------------------
DEMO_ORG = {
    "name": "TradeComply Demo",
    "slug": "tradecomply-demo",
    "plan": "pro",
}

DEMO_USER = {
    "email": "admin@demo.com",
    "password": "demo-password-123",
    "full_name": "Admin User",
}

DEMO_PARTIES = [
    {
        "party_type": "clearing_agent",
        "name": "Swift Customs Brokers (Pty) Ltd",
        "customs_code": "CB20156",
        "vat_number": "4520156789",
        "country": "ZA",
        "address_line1": "12 Bayhead Road, Durban, 4001",
        "email": "ops@swiftcustoms.co.za",
        "phone": "+27312012345",
    },
    {
        "party_type": "supplier",
        "name": "Shenzhen GreenPower Tech Co., Ltd",
        "customs_code": None,
        "vat_number": None,
        "country": "CN",
        "address_line1": "Building B, Longhua Industrial Zone, Shenzhen, China",
        "email": "export@greenpower-sz.com",
        "phone": "+8675511223344",
    },
    {
        "party_type": "importer",
        "name": "SA Solar Imports (Pty) Ltd",
        "customs_code": "IM20987",
        "vat_number": "4612345678",
        "country": "ZA",
        "address_line1": "45 Keyes Ave, Rosebank, Johannesburg, 2196",
        "email": "imports@sasolar.co.za",
        "phone": "+27113456789",
    },
]

DEMO_SHIPMENTS = [
    {
        "reference": "TC-2026-001",
        "shipment_type": "import",
        "transport_mode": "sea",
        "status": "compliance_ready",
        "risk_level": "low",
        "origin_country": "CN",
        "destination_country": "ZA",
        "port_of_loading": "Yantian, Shenzhen",
        "port_of_discharge": "Durban",
        "incoterms": "CIF",
        "currency": "USD",
        "invoice_date": date(2026, 7, 15),
        "estimated_arrival_date": date(2026, 8, 20),
        "line_items": [
            {
                "description": "Monocrystalline solar panels 400W, 72-cell",
                "quantity": 500,
                "unit_price": 95.0,
                "total_value": 47500.0,
                "hs_code_suggested": "8541.40",
                "confidence": 0.94,
            },
            {
                "description": "Lithium iron phosphate (LFP) battery modules 100Ah 48V",
                "quantity": 50,
                "unit_price": 480.0,
                "total_value": 24000.0,
                "hs_code_suggested": "8507.60",
                "confidence": 0.91,
            },
            {
                "description": "Hybrid grid-tie solar inverter 5kW 48V",
                "quantity": 20,
                "unit_price": 380.0,
                "total_value": 7600.0,
                "hs_code_suggested": "8504.40",
                "confidence": 0.88,
            },
        ],
    },
    {
        "reference": "TC-2026-002",
        "shipment_type": "import",
        "transport_mode": "sea",
        "status": "needs_review",
        "risk_level": "medium",
        "origin_country": "CN",
        "destination_country": "ZA",
        "port_of_loading": "Shanghai",
        "port_of_discharge": "Durban",
        "incoterms": "FOB",
        "currency": "USD",
        "invoice_date": date(2026, 7, 28),
        "estimated_arrival_date": date(2026, 9, 5),
        "line_items": [
            {
                "description": "Cotton T-shirts, assorted colours, men size M-XL",
                "quantity": 5000,
                "unit_price": 3.2,
                "total_value": 16000.0,
                "hs_code_suggested": "6109.10",
                "confidence": 0.92,
            },
            {
                "description": "Men woven denim jeans, blue wash, sizes 30-38",
                "quantity": 2000,
                "unit_price": 7.5,
                "total_value": 15000.0,
                "hs_code_suggested": "6203.42",
                "confidence": 0.89,
            },
        ],
    },
    {
        "reference": "TC-2026-003",
        "shipment_type": "import",
        "transport_mode": "sea",
        "status": "draft",
        "risk_level": "high",
        "origin_country": "DE",
        "destination_country": "ZA",
        "port_of_loading": "Hamburg",
        "port_of_discharge": "Durban",
        "incoterms": "CIF",
        "currency": "EUR",
        "invoice_date": date(2026, 8, 1),
        "estimated_arrival_date": date(2026, 9, 15),
        "line_items": [
            {
                "description": "Glacial acetic acid 99.8% pure, UN2789 Dangerous Goods Class 8/3",
                "quantity": 20,
                "unit_price": 450.0,
                "total_value": 9000.0,
                "hs_code_suggested": "2915.21",
                "confidence": 0.96,
            },
        ],
    },
]


# ---------------------------------------------------------------------------
# Seed Operations
# ---------------------------------------------------------------------------
async def seed_tariffs(session: AsyncSession, now: datetime) -> int:
    """Insert South African tariff records idempotently."""
    inserted = 0
    for r in TARIFF_RECORDS:
        existing = await session.execute(
            select(TariffRecord).where(TariffRecord.hs_code == r["hs_code"])
        )
        if existing.scalar_one_or_none() is not None:
            continue

        tariff = TariffRecord(
            id=str(uuid4()),
            hs_code=r["hs_code"],
            sa_tariff_code=r["sa_tariff_code"],
            description=r["description"],
            duty_rate=r["duty_rate"],
            vat_rate=r["vat_rate"],
            unit_of_measure=r.get("unit_of_measure"),
            country_of_origin=None,
            chapter=r.get("chapter"),
            section=r.get("section"),
            embedding=None,
            created_at=now,
            updated_at=now,
        )
        session.add(tariff)
        inserted += 1

    await session.flush()
    return inserted


async def seed_org_and_user(session: AsyncSession, now: datetime) -> tuple[Organization, User]:
    """Create demo organization, admin user, and membership idempotently."""
    result = await session.execute(
        select(Organization).where(Organization.slug == DEMO_ORG["slug"])
    )
    org = result.scalar_one_or_none()
    if org is None:
        org = Organization(
            id=str(uuid4()),
            name=DEMO_ORG["name"],
            slug=DEMO_ORG["slug"],
            plan=DEMO_ORG["plan"],
            created_at=now,
            updated_at=now,
        )
        session.add(org)
        await session.flush()
        print(f"  ✅ Created organization: {org.name}")
    else:
        print(f"  ⏭️  Organization already exists: {org.name}")

    result = await session.execute(select(User).where(User.email == DEMO_USER["email"]))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(
            id=str(uuid4()),
            email=DEMO_USER["email"],
            password_hash=get_password_hash(DEMO_USER["password"]),
            full_name=DEMO_USER["full_name"],
            is_active=True,
            created_at=now,
            updated_at=now,
        )
        session.add(user)
        await session.flush()
        print(f"  ✅ Created user: {user.email}")
    else:
        print(f"  ⏭️  User already exists: {user.email}")

    result = await session.execute(
        select(Membership).where(
            Membership.organization_id == org.id,
            Membership.user_id == user.id,
        )
    )
    if result.scalar_one_or_none() is None:
        membership = Membership(
            id=str(uuid4()),
            organization_id=org.id,
            user_id=user.id,
            role="owner",
            created_at=now,
        )
        session.add(membership)
        await session.flush()
        print("  ✅ Created owner membership")

    return org, user


async def seed_parties(
    session: AsyncSession, org_id: str, now: datetime
) -> dict[str, Party]:
    """Seed demo parties idempotently."""
    parties: dict[str, Party] = {}
    for pdata in DEMO_PARTIES:
        result = await session.execute(
            select(Party).where(
                Party.organization_id == org_id,
                Party.name == pdata["name"],
            )
        )
        party = result.scalar_one_or_none()
        if party is None:
            party = Party(
                id=str(uuid4()),
                organization_id=org_id,
                party_type=pdata["party_type"],
                name=pdata["name"],
                customs_code=pdata.get("customs_code"),
                vat_number=pdata.get("vat_number"),
                country=pdata.get("country"),
                address_line1=pdata.get("address_line1"),
                email=pdata.get("email"),
                phone=pdata.get("phone"),
                created_at=now,
                updated_at=now,
            )
            session.add(party)
            await session.flush()
            print(f"  ✅ Created party [{pdata['party_type']}]: {party.name}")
        else:
            print(f"  ⏭️  Party already exists: {party.name}")
        parties[pdata["name"]] = party
    return parties


async def seed_shipments(
    session: AsyncSession,
    org: Organization,
    user: User,
    parties: dict[str, Party],
    now: datetime,
) -> None:
    """Seed demo shipments and line items idempotently."""
    importer = parties.get("SA Solar Imports (Pty) Ltd")
    supplier = parties.get("Shenzhen GreenPower Tech Co., Ltd")
    agent = parties.get("Swift Customs Brokers (Pty) Ltd")

    for sdata in DEMO_SHIPMENTS:
        result = await session.execute(
            select(Shipment).where(
                Shipment.organization_id == org.id,
                Shipment.reference == sdata["reference"],
            )
        )
        shipment = result.scalar_one_or_none()
        if shipment is not None:
            print(f"  ⏭️  Shipment already exists: {sdata['reference']}")
            continue

        shipment = Shipment(
            id=str(uuid4()),
            organization_id=org.id,
            reference=sdata["reference"],
            shipment_type=sdata["shipment_type"],
            transport_mode=sdata.get("transport_mode"),
            status=sdata["status"],
            risk_level=sdata["risk_level"],
            origin_country=sdata.get("origin_country"),
            destination_country=sdata.get("destination_country"),
            port_of_loading=sdata.get("port_of_loading"),
            port_of_discharge=sdata.get("port_of_discharge"),
            incoterms=sdata.get("incoterms"),
            currency=sdata.get("currency"),
            invoice_date=sdata.get("invoice_date"),
            estimated_arrival_date=sdata.get("estimated_arrival_date"),
            importer_id=importer.id if importer else None,
            supplier_id=supplier.id if supplier else None,
            clearing_agent_id=agent.id if agent else None,
            created_by=user.id,
            created_at=now,
            updated_at=now,
        )
        session.add(shipment)
        await session.flush()
        print(f"  ✅ Created shipment: {shipment.reference} [{shipment.status}]")

        for li_data in sdata.get("line_items", []):
            line_item = LineItem(
                id=str(uuid4()),
                shipment_id=shipment.id,
                description=li_data["description"],
                quantity=li_data.get("quantity", 1),
                unit_price=li_data.get("unit_price", 0.0),
                total_value=li_data.get("total_value", 0.0),
                hs_code_suggested=li_data.get("hs_code_suggested"),
                confidence=li_data.get("confidence"),
                created_at=now,
                updated_at=now,
            )
            session.add(line_item)
        await session.flush()
        print(f"     ↳ Added {len(sdata['line_items'])} line items")


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------
async def main() -> None:
    print("\n🌱 TradeComply AI South Africa — Database Seeder")
    print("=" * 55)

    engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as session:
        now = datetime.utcnow()

        print("\n📦 Seeding South African tariff records …")
        count = await seed_tariffs(session, now)
        print(f"  ✅ Inserted {count} new tariff records ({len(TARIFF_RECORDS)} total)")

        print("\n🏢 Seeding demo organization & admin user …")
        org, user = await seed_org_and_user(session, now)

        print("\n👥 Seeding demo parties …")
        parties = await seed_parties(session, org.id, now)

        print("\n🚢 Seeding demo shipments & line items …")
        await seed_shipments(session, org, user, parties, now)

        await session.commit()

    await engine.dispose()

    print("\n✅ Database seeding completed successfully!")
    print("\n📋 Demo Credentials:")
    print(f"   Email:    {DEMO_USER['email']}")
    print(f"   Password: {DEMO_USER['password']}")
    print(f"   API Docs: http://localhost:8000/docs")
    print()


if __name__ == "__main__":
    asyncio.run(main())
