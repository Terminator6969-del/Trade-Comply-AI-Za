"""Initial schema: all tables for TradeComply AI South Africa MVP.

Revision ID: 0001_initial_schema
Revises: (none - initial migration)
Create Date: 2026-08-14

Tables created:
  organizations, users, memberships, audit_logs, usage_events,
  parties, shipments, documents, extracted_fields, line_items,
  tariff_records, classification_candidates
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ------------------------------------------------------------------
    # organizations
    # ------------------------------------------------------------------
    op.create_table(
        "organizations",
        sa.Column("id", sa.String(36), primary_key=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("slug", sa.String(255), nullable=False, unique=True),
        sa.Column("plan", sa.String(50), nullable=False, server_default="free"),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
    )
    op.create_index("ix_organizations_slug", "organizations", ["slug"])

    # ------------------------------------------------------------------
    # users
    # ------------------------------------------------------------------
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True, nullable=False),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"])

    # ------------------------------------------------------------------
    # memberships
    # ------------------------------------------------------------------
    op.create_table(
        "memberships",
        sa.Column("id", sa.String(36), primary_key=True, nullable=False),
        sa.Column(
            "organization_id",
            sa.String(36),
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.String(36),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("role", sa.String(50), nullable=False, server_default="viewer"),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )
    op.create_index("ix_memberships_organization_id", "memberships", ["organization_id"])
    op.create_index("ix_memberships_user_id", "memberships", ["user_id"])

    # ------------------------------------------------------------------
    # audit_logs
    # ------------------------------------------------------------------
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.String(36), primary_key=True, nullable=False),
        sa.Column(
            "organization_id",
            sa.String(36),
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.String(36),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("resource_type", sa.String(100), nullable=True),
        sa.Column("resource_id", sa.String(36), nullable=True),
        sa.Column("details", sa.JSON, nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )
    op.create_index("ix_audit_logs_organization_id", "audit_logs", ["organization_id"])
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"])

    # ------------------------------------------------------------------
    # usage_events
    # ------------------------------------------------------------------
    op.create_table(
        "usage_events",
        sa.Column("id", sa.String(36), primary_key=True, nullable=False),
        sa.Column(
            "organization_id",
            sa.String(36),
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("event_type", sa.String(100), nullable=False),
        sa.Column("quantity", sa.Integer, nullable=False, server_default="1"),
        sa.Column("metadata", sa.JSON, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )
    op.create_index("ix_usage_events_organization_id", "usage_events", ["organization_id"])

    # ------------------------------------------------------------------
    # parties
    # ------------------------------------------------------------------
    op.create_table(
        "parties",
        sa.Column("id", sa.String(36), primary_key=True, nullable=False),
        sa.Column(
            "organization_id",
            sa.String(36),
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("party_type", sa.String(50), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("registration_number", sa.String(100), nullable=True),
        sa.Column("vat_number", sa.String(50), nullable=True),
        sa.Column("customs_code", sa.String(50), nullable=True),
        sa.Column("address_line1", sa.String(255), nullable=True),
        sa.Column("address_line2", sa.String(255), nullable=True),
        sa.Column("city", sa.String(100), nullable=True),
        sa.Column("postal_code", sa.String(20), nullable=True),
        sa.Column("country", sa.String(2), nullable=True),
        sa.Column("contact_person", sa.String(255), nullable=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("phone", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
    )
    op.create_index("ix_parties_organization_id", "parties", ["organization_id"])
    op.create_index("ix_parties_party_type", "parties", ["party_type"])

    # ------------------------------------------------------------------
    # shipments
    # ------------------------------------------------------------------
    op.create_table(
        "shipments",
        sa.Column("id", sa.String(36), primary_key=True, nullable=False),
        sa.Column(
            "organization_id",
            sa.String(36),
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("reference", sa.String(100), nullable=False),
        sa.Column("shipment_type", sa.String(20), nullable=False, server_default="import"),
        sa.Column("transport_mode", sa.String(20), nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="draft"),
        sa.Column("risk_level", sa.String(20), nullable=False, server_default="low"),
        sa.Column("origin_country", sa.String(2), nullable=True),
        sa.Column("destination_country", sa.String(2), nullable=True),
        sa.Column("port_of_loading", sa.String(100), nullable=True),
        sa.Column("port_of_discharge", sa.String(100), nullable=True),
        sa.Column("border_post", sa.String(100), nullable=True),
        sa.Column("incoterms", sa.String(10), nullable=True),
        sa.Column("currency", sa.String(3), nullable=True),
        sa.Column("invoice_date", sa.Date, nullable=True),
        sa.Column("estimated_arrival_date", sa.Date, nullable=True),
        sa.Column(
            "importer_id",
            sa.String(36),
            sa.ForeignKey("parties.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "exporter_id",
            sa.String(36),
            sa.ForeignKey("parties.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "supplier_id",
            sa.String(36),
            sa.ForeignKey("parties.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "consignee_id",
            sa.String(36),
            sa.ForeignKey("parties.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "notify_party_id",
            sa.String(36),
            sa.ForeignKey("parties.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "clearing_agent_id",
            sa.String(36),
            sa.ForeignKey("parties.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "created_by",
            sa.String(36),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
    )
    op.create_index("ix_shipments_organization_id", "shipments", ["organization_id"])
    op.create_index("ix_shipments_reference", "shipments", ["reference"])

    # ------------------------------------------------------------------
    # documents
    # ------------------------------------------------------------------
    op.create_table(
        "documents",
        sa.Column("id", sa.String(36), primary_key=True, nullable=False),
        sa.Column(
            "organization_id",
            sa.String(36),
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "shipment_id",
            sa.String(36),
            sa.ForeignKey("shipments.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("document_type", sa.String(50), nullable=False, server_default="other"),
        sa.Column("file_name", sa.String(255), nullable=False),
        sa.Column("file_size", sa.Integer, nullable=True),
        sa.Column("content_type", sa.String(100), nullable=True),
        sa.Column("storage_key", sa.String(500), nullable=True),
        sa.Column("extraction_status", sa.String(30), nullable=False, server_default="pending"),
        sa.Column("ocr_text", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
    )
    op.create_index("ix_documents_organization_id", "documents", ["organization_id"])
    op.create_index("ix_documents_shipment_id", "documents", ["shipment_id"])

    # ------------------------------------------------------------------
    # extracted_fields
    # ------------------------------------------------------------------
    op.create_table(
        "extracted_fields",
        sa.Column("id", sa.String(36), primary_key=True, nullable=False),
        sa.Column(
            "document_id",
            sa.String(36),
            sa.ForeignKey("documents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("field_name", sa.String(100), nullable=False),
        sa.Column("field_value", sa.Text, nullable=True),
        sa.Column("confidence", sa.Float, nullable=False),
        sa.Column("source", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )
    op.create_index("ix_extracted_fields_document_id", "extracted_fields", ["document_id"])

    # ------------------------------------------------------------------
    # line_items
    # ------------------------------------------------------------------
    op.create_table(
        "line_items",
        sa.Column("id", sa.String(36), primary_key=True, nullable=False),
        sa.Column(
            "shipment_id",
            sa.String(36),
            sa.ForeignKey("shipments.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("description", sa.String(500), nullable=False),
        sa.Column("quantity", sa.Integer, nullable=False, server_default="1"),
        sa.Column("unit_price", sa.Float, nullable=False, server_default="0.0"),
        sa.Column("total_value", sa.Float, nullable=False, server_default="0.0"),
        sa.Column("hs_code_suggested", sa.String(20), nullable=True),
        sa.Column("confidence", sa.Float, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
    )
    op.create_index("ix_line_items_shipment_id", "line_items", ["shipment_id"])

    # ------------------------------------------------------------------
    # tariff_records
    # ------------------------------------------------------------------
    op.create_table(
        "tariff_records",
        sa.Column("id", sa.String(36), primary_key=True, nullable=False),
        sa.Column("hs_code", sa.String(20), nullable=False),
        sa.Column("sa_tariff_code", sa.String(20), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("duty_rate", sa.Float, nullable=False, server_default="0.0"),
        sa.Column("vat_rate", sa.Float, nullable=False, server_default="15.0"),
        sa.Column("unit_of_measure", sa.String(50), nullable=True),
        sa.Column("country_of_origin", sa.JSON, nullable=True),
        sa.Column("chapter", sa.String(10), nullable=True),
        sa.Column("section", sa.String(10), nullable=True),
        sa.Column("embedding", sa.JSON, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
    )
    op.create_index("ix_tariff_records_hs_code", "tariff_records", ["hs_code"])
    op.create_index("ix_tariff_records_sa_tariff_code", "tariff_records", ["sa_tariff_code"])
    op.create_index("ix_tariff_records_chapter", "tariff_records", ["chapter"])

    # ------------------------------------------------------------------
    # classification_candidates
    # ------------------------------------------------------------------
    op.create_table(
        "classification_candidates",
        sa.Column("id", sa.String(36), primary_key=True, nullable=False),
        sa.Column(
            "line_item_id",
            sa.String(36),
            sa.ForeignKey("line_items.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("hs_code", sa.String(20), nullable=False),
        sa.Column("sa_tariff_code", sa.String(20), nullable=True),
        sa.Column("confidence", sa.Float, nullable=False),
        sa.Column("reasoning", sa.Text, nullable=True),
        sa.Column("permit_flags", sa.JSON, nullable=True),
        sa.Column("duty_rate", sa.Float, nullable=True),
        sa.Column("vat_rate", sa.Float, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )
    op.create_index(
        "ix_classification_candidates_line_item_id",
        "classification_candidates",
        ["line_item_id"],
    )
    op.create_index(
        "ix_classification_candidates_hs_code",
        "classification_candidates",
        ["hs_code"],
    )


def downgrade() -> None:
    # Drop tables in reverse dependency order
    op.drop_table("classification_candidates")
    op.drop_table("tariff_records")
    op.drop_table("line_items")
    op.drop_table("extracted_fields")
    op.drop_table("documents")
    op.drop_table("shipments")
    op.drop_table("parties")
    op.drop_table("usage_events")
    op.drop_table("audit_logs")
    op.drop_table("memberships")
    op.drop_table("users")
    op.drop_table("organizations")
