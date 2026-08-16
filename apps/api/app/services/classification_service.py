"""
Classification service for HS code ranking and tariff lookup.
Uses vector search + LLM ranking for top-5 HS code suggestions.
"""

from typing import Any

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TariffRecord, LineItem, ClassificationCandidate
from app.ai.extraction import classify_line_item


async def search_tariffs(
    session: AsyncSession,
    query: str,
    limit: int = 10,
) -> list[TariffRecord]:
    """
    Search tariff records by description or HS code.
    
    Args:
        session: Database session
        query: Search query
        limit: Maximum results
        
    Returns:
        List of matching tariff records
    """
    search_pattern = f"%{query}%"
    result = await session.execute(
        select(TariffRecord)
        .where(
            TariffRecord.description.ilike(search_pattern)
            | TariffRecord.hs_code.ilike(search_pattern)
            | TariffRecord.sa_tariff_code.ilike(search_pattern)
        )
        .limit(limit)
    )
    return list(result.scalars().all())


async def classify_line_item(
    session: AsyncSession,
    line_item_id: str,
    description: str,
    context: dict[str, Any] | None = None,
) -> list[ClassificationCandidate]:
    """
    Classify a line item to HS codes.
    
    Pipeline:
    1. Get LLM classification candidates
    2. Look up tariff records for each candidate
    3. Store candidates with tariff data
    
    Args:
        session: Database session
        line_item_id: ID of line item to classify
        description: Product description
        context: Additional context
        
    Returns:
        List of classification candidates with tariff data
    """
    # Get LLM classification
    llm_candidates = await classify_line_item(description, context)

    candidates = []
    for candidate in llm_candidates:
        hs_code = candidate["hs_code"]

        # Look up tariff record
        result = await session.execute(
            select(TariffRecord).where(TariffRecord.hs_code == hs_code)
        )
        tariff = result.scalar_one_or_none()

        # Create classification candidate
        classification = ClassificationCandidate(
            line_item_id=line_item_id,
            hs_code=hs_code,
            sa_tariff_code=tariff.sa_tariff_code if tariff else None,
            confidence=candidate["confidence"],
            reasoning=candidate.get("reasoning", ""),
            permit_flags=candidate.get("permit_flags", []),
            duty_rate=tariff.duty_rate if tariff else None,
            vat_rate=tariff.vat_rate if tariff else None,
        )
        session.add(classification)
        candidates.append(classification)

    await session.commit()

    # Refresh all candidates
    for c in candidates:
        await session.refresh(c)

    return candidates


async def classify_shipment(
    session: AsyncSession,
    shipment_id: str,
) -> dict[str, list[ClassificationCandidate]]:
    """
    Classify all line items in a shipment.
    
    Args:
        session: Database session
        shipment_id: Shipment ID
        
    Returns:
        Dictionary mapping line_item_id to classification candidates
    """
    # Get all line items for shipment
    result = await session.execute(
        select(LineItem).where(LineItem.shipment_id == shipment_id)
    )
    line_items = result.scalars().all()

    results = {}
    for item in line_items:
        candidates = await classify_line_item(
            session=session,
            line_item_id=item.id,
            description=item.description,
        )
        results[item.id] = candidates

    return results


async def get_classification_candidates(
    session: AsyncSession,
    line_item_id: str,
    limit: int = 5,
) -> list[ClassificationCandidate]:
    """
    Get classification candidates for a line item.
    
    Args:
        session: Database session
        line_item_id: Line item ID
        limit: Maximum candidates to return
        
    Returns:
        List of classification candidates sorted by confidence
    """
    result = await session.execute(
        select(ClassificationCandidate)
        .where(ClassificationCandidate.line_item_id == line_item_id)
        .order_by(ClassificationCandidate.confidence.desc())
        .limit(limit)
    )
    return list(result.scalars().all())
