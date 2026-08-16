/**
 * Shared type definitions for TradeComply AI South Africa
 * These types are used across frontend and backend
 */

// ==================== Organizations ====================
export interface Organization {
  id: string;
  name: string;
  slug: string;
  plan: 'free' | 'pro' | 'enterprise';
  created_at: string;
  updated_at: string;
}

// ==================== Users ====================
export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  organization_id: string;
  created_at: string;
  updated_at: string;
}

export interface Membership {
  id: string;
  organization_id: string;
  user_id: string;
  role: 'owner' | 'admin' | 'compliance_manager' | 'clerk' | 'viewer' | 'api_service';
  created_at: string;
}

// ==================== Authentication ====================
export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
  organization_name?: string;
}

// ==================== Shipments ====================
export type ShipmentType = 'import' | 'export' | 'transit';
export type ShipmentStatus = 'draft' | 'submitted' | 'approved' | 'rejected' | 'completed';
export type RiskLevel = 'low' | 'medium' | 'high';

export interface Shipment {
  id: string;
  organization_id: string;
  reference: string;
  shipment_type: ShipmentType;
  status: ShipmentStatus;
  risk_level: RiskLevel;
  importer_id?: string;
  exporter_id?: string;
  supplier_id?: string;
  consignee_id?: string;
  clearing_agent_id?: string;
  created_at: string;
  updated_at: string;
}

export interface ShipmentCreateRequest {
  reference: string;
  shipment_type: ShipmentType;
  importer_id?: string;
  exporter_id?: string;
  supplier_id?: string;
  consignee_id?: string;
  clearing_agent_id?: string;
}

// ==================== Parties ====================
export type PartyType = 'importer' | 'exporter' | 'supplier' | 'consignee' | 'clearing_agent';

export interface Party {
  id: string;
  organization_id: string;
  party_type: PartyType;
  name: string;
  vat_number?: string;
  customs_code?: string;
  address?: string;
  contact_email?: string;
  contact_phone?: string;
  created_at: string;
  updated_at: string;
}

// ==================== Documents ====================
export type DocumentType = 'invoice' | 'packing_list' | 'bill_of_lading' | 'airway_bill' | 'commercial_invoice' | 'certificate_of_origin' | 'other';

export interface Document {
  id: string;
  shipment_id: string;
  document_type: DocumentType;
  file_key: string;
  file_name: string;
  extraction_status: 'pending' | 'processing' | 'completed' | 'failed';
  created_at: string;
  updated_at: string;
}

export interface DocumentUploadRequest {
  document_type: DocumentType;
  file: File; // For frontend
  file_key?: string; // For backend
}

// ==================== Extraction ====================
export interface ExtractedField {
  id: string;
  document_id: string;
  field_name: string;
  field_value: unknown;
  confidence: number; // 0.0 - 1.0
  verified: boolean;
}

export interface LineItem {
  id: string;
  shipment_id: string;
  description: string;
  quantity: number;
  unit_price: number;
  total_value: number;
  hs_code_suggested?: string;
  confidence?: number;
}

// ==================== Classification ====================
export interface ClassificationCandidate {
  hs_code: string;
  sa_tariff_code?: string;
  confidence: number;
  reasoning: string;
  duty_rate?: number;
  vat_rate?: number;
  permit_flags?: string[];
}

export interface TariffRecord {
  id: string;
  hs_code: string;
  sa_tariff_code: string;
  description: string;
  duty_rate: number;
  vat_rate: number;
  created_at: string;
}

// ==================== Compliance ====================
export type ComplianceSeverity = 'info' | 'warning' | 'error' | 'critical';

export interface ComplianceCheck {
  id: string;
  shipment_id: string;
  rule_pack: string;
  rule_code: string;
  severity: ComplianceSeverity;
  message: string;
  recommended_action?: string;
  created_at: string;
}

export interface ComplianceRule {
  id: string;
  organization_id: string;
  rule_pack: 'sars_tariff' | 'itac_permits' | 'nrcs_loa' | 'dangerous_goods' | 'valuation';
  rule_code: string;
  condition: Record<string, unknown>;
  active: boolean;
  created_at: string;
}

// ==================== Duties ====================
export interface DutyEstimate {
  id: string;
  shipment_id: string;
  customs_value: number;
  duty_amount: number;
  vat_amount: number;
  total_estimated: number;
  duty_rate: number;
  vat_rate: number;
  disclaimer: string;
  created_at: string;
  updated_at: string;
}

// ==================== Packets ====================
export type PacketFormat = 'json' | 'csv' | 'pdf';

export interface Packet {
  shipment: Shipment;
  documents: Document[];
  extracted_fields: ExtractedField[];
  line_items: LineItem[];
  classification_candidates: Record<string, ClassificationCandidate[]>;
  compliance_checks: ComplianceCheck[];
  duty_estimate: DutyEstimate;
  audit_trail: AuditLog[];
}

// ==================== Audit ====================
export interface AuditLog {
  id: string;
  organization_id: string;
  user_id: string;
  action: string;
  entity_type: string;
  entity_id: string;
  before_value?: Record<string, unknown>;
  after_value?: Record<string, unknown>;
  ip_address?: string;
  created_at: string;
}

// ==================== API Responses ====================
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}
