-- Pharmacovigilance System Database Schema
-- PostgreSQL 15+

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Reporters table (patients and healthcare professionals)
CREATE TABLE reporters (
  id SERIAL PRIMARY KEY,
  uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
  reporter_type VARCHAR(20) NOT NULL CHECK (reporter_type IN ('patient', 'hcp')),
  name TEXT,
  phone TEXT,
  email TEXT,
  language VARCHAR(10) DEFAULT 'en',
  verified BOOLEAN DEFAULT FALSE,
  encrypted_data BYTEA, -- AES-256 encrypted PHI
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Adverse events table
CREATE TABLE events (
  id SERIAL PRIMARY KEY,
  uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
  reporter_id INT REFERENCES reporters(id) ON DELETE CASCADE,
  
  -- Drug information
  suspected_drug TEXT,
  dose TEXT,
  frequency TEXT,
  start_date DATE,
  stop_date DATE,
  
  -- Adverse effect details
  adverse_effect TEXT,
  seriousness TEXT CHECK (seriousness IN ('serious', 'non-serious', 'unknown')),
  hospitalization BOOLEAN,
  outcome TEXT CHECK (outcome IN ('recovered', 'recovering', 'not_recovered', 'fatal', 'unknown')),
  
  -- Medical context
  comorbidities TEXT,
  medications TEXT, -- Concomitant medications
  
  -- Follow-up management
  followup_status VARCHAR(20) DEFAULT 'pending' CHECK (followup_status IN ('pending', 'in_progress', 'completed', 'escalated')),
  missing_fields JSONB, -- Array of missing field names
  
  -- Consent and compliance
  consent BOOLEAN DEFAULT FALSE,
  consent_timestamp TIMESTAMP,
  
  -- Risk scoring
  risk_score FLOAT CHECK (risk_score >= 0 AND risk_score <= 100),
  risk_class VARCHAR(20) CHECK (risk_class IN ('low', 'medium', 'high', 'critical')),
  hospitalization_risk FLOAT,
  mortality_risk FLOAT,
  
  -- Metadata
  encrypted_data BYTEA, -- AES-256 encrypted PHI
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- OTP tokens for verification
CREATE TABLE otp_tokens (
  id SERIAL PRIMARY KEY,
  reporter_id INT REFERENCES reporters(id) ON DELETE CASCADE,
  token_hash VARCHAR(255) NOT NULL, -- Hashed OTP
  channel VARCHAR(20) NOT NULL CHECK (channel IN ('sms', 'whatsapp', 'email')),
  phone_or_email TEXT NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  verified BOOLEAN DEFAULT FALSE,
  verified_at TIMESTAMP,
  attempts INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Audit logs for compliance
CREATE TABLE audit_logs (
  id SERIAL PRIMARY KEY,
  event_id INT REFERENCES events(id) ON DELETE CASCADE,
  reporter_id INT REFERENCES reporters(id),
  action TEXT NOT NULL,
  channel TEXT,
  user_role VARCHAR(50),
  ip_address VARCHAR(45),
  meta JSONB,
  timestamp TIMESTAMP DEFAULT NOW()
);

-- Follow-up questions sent to users
CREATE TABLE followup_questions (
  id SERIAL PRIMARY KEY,
  event_id INT REFERENCES events(id) ON DELETE CASCADE,
  question_text TEXT NOT NULL,
  question_language VARCHAR(10) DEFAULT 'en',
  field_name TEXT, -- Which missing field this question addresses
  channel VARCHAR(20) CHECK (channel IN ('sms', 'whatsapp', 'email')),
  sent_at TIMESTAMP DEFAULT NOW(),
  answered BOOLEAN DEFAULT FALSE,
  answer_text TEXT,
  answered_at TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_reporters_phone ON reporters(phone);
CREATE INDEX idx_reporters_email ON reporters(email);
CREATE INDEX idx_reporters_verified ON reporters(verified);
CREATE INDEX idx_events_reporter_id ON events(reporter_id);
CREATE INDEX idx_events_followup_status ON events(followup_status);
CREATE INDEX idx_events_risk_class ON events(risk_class);
CREATE INDEX idx_events_created_at ON events(created_at DESC);
CREATE INDEX idx_otp_tokens_expires_at ON otp_tokens(expires_at);
CREATE INDEX idx_otp_tokens_reporter_id ON otp_tokens(reporter_id);
CREATE INDEX idx_audit_logs_event_id ON audit_logs(event_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp DESC);
CREATE INDEX idx_followup_questions_event_id ON followup_questions(event_id);

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_reporters_updated_at BEFORE UPDATE ON reporters
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_events_updated_at BEFORE UPDATE ON events
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
