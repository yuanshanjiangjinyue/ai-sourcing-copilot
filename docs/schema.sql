-- Conceptual PostgreSQL DDL for the first *real* pilot; demo runtime instead uses SQLite for RFQ drafts.
CREATE TABLE tenants (
 id UUID PRIMARY KEY,
 name TEXT NOT NULL,
 created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE products (
 id UUID PRIMARY KEY,
 tenant_id UUID NOT NULL REFERENCES tenants(id),
 sku TEXT NOT NULL,
 name TEXT NOT NULL,
 product_type TEXT NOT NULL,
 interface TEXT,
 shutter TEXT,
 resolution_mp NUMERIC(8,2),
 max_fps NUMERIC(10,2),
 specifications JSONB NOT NULL DEFAULT '{}',
 approval_state TEXT NOT NULL DEFAULT 'unverified',
 updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
 UNIQUE(tenant_id,sku)
);
CREATE TABLE product_documents (
 id UUID PRIMARY KEY,
 tenant_id UUID NOT NULL REFERENCES tenants(id),
 product_id UUID NOT NULL REFERENCES products(id),
 source_url TEXT,
 object_key TEXT NOT NULL,
 doc_version TEXT,
 valid_from DATE,
 reviewed_by UUID,
 reviewed_at TIMESTAMPTZ,
 sha256 TEXT NOT NULL
);
CREATE TABLE compatibility_edges (
 id UUID PRIMARY KEY,
 tenant_id UUID NOT NULL REFERENCES tenants(id),
 source_product_id UUID NOT NULL REFERENCES products(id),
 target_product_id UUID NOT NULL REFERENCES products(id),
 relation_type TEXT NOT NULL,
 rule_version TEXT NOT NULL,
 evidence_document_id UUID REFERENCES product_documents(id),
 verification_state TEXT NOT NULL DEFAULT 'unverified'
);
CREATE TABLE suppliers (
 id UUID PRIMARY KEY,
 tenant_id UUID NOT NULL REFERENCES tenants(id),
 legal_name TEXT NOT NULL,
 supplier_type TEXT NOT NULL,
 verification_state TEXT NOT NULL DEFAULT 'unverified'
);
CREATE TABLE supplier_offers (
 id UUID PRIMARY KEY,
 tenant_id UUID NOT NULL REFERENCES tenants(id),
 supplier_id UUID NOT NULL REFERENCES suppliers(id),
 product_id UUID NOT NULL REFERENCES products(id),
 currency CHAR(3) NOT NULL,
 unit_price NUMERIC(14,4) NOT NULL,
 min_quantity INT NOT NULL,
 max_quantity INT,
 incoterm TEXT,
 valid_until TIMESTAMPTZ,
 lead_days INT,
 quote_document_id UUID,
 verification_state TEXT NOT NULL DEFAULT 'unverified'
);
CREATE TABLE requirements (
 id UUID PRIMARY KEY,
 tenant_id UUID NOT NULL REFERENCES tenants(id),
 original_text TEXT NOT NULL,
 hard_constraints JSONB NOT NULL,
 parsing_method TEXT NOT NULL,
 confirmed_by UUID,
 confirmed_at TIMESTAMPTZ,
 created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE matches (
 id UUID PRIMARY KEY,
 tenant_id UUID NOT NULL REFERENCES tenants(id),
 requirement_id UUID NOT NULL REFERENCES requirements(id),
 product_id UUID NOT NULL REFERENCES products(id),
 status TEXT NOT NULL,
 failures JSONB NOT NULL DEFAULT '[]',
 rank_score NUMERIC(7,3),
 rule_version TEXT NOT NULL,
 evidence JSONB NOT NULL DEFAULT '[]'
);
CREATE TABLE rfqs (
 id UUID PRIMARY KEY,
 tenant_id UUID NOT NULL REFERENCES tenants(id),
 requirement_id UUID NOT NULL REFERENCES requirements(id),
 status TEXT NOT NULL DEFAULT 'draft',
 approved_by UUID,
 approved_at TIMESTAMPTZ,
 created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE rfq_lines (
 id UUID PRIMARY KEY,
 rfq_id UUID NOT NULL REFERENCES rfqs(id),
 product_id UUID NOT NULL REFERENCES products(id),
 quantity INT NOT NULL CHECK(quantity>0),
 destination_country TEXT,
 note TEXT
);
CREATE TABLE audit_events (
 id UUID PRIMARY KEY,
 tenant_id UUID NOT NULL REFERENCES tenants(id),
 actor_id UUID,
 event_type TEXT NOT NULL,
 entity_type TEXT NOT NULL,
 entity_id UUID,
 action_payload JSONB NOT NULL DEFAULT '{}',
 created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_products_tenant_type ON products(tenant_id,product_type);
CREATE INDEX idx_req_tenant_date ON requirements(tenant_id,created_at DESC);
CREATE INDEX idx_rfq_tenant_status ON rfqs(tenant_id,status);
-- Actual embedding column dimension and HNSW index must match the selected embedding model.
-- CREATE EXTENSION IF NOT EXISTS vector;
-- ALTER TABLE product_documents ADD COLUMN embedding vector(<model_dimension>);