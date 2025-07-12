-- PNCP Ingestion Database Initialization Script
-- This script creates the initial database structure

-- Create database if not exists (PostgreSQL doesn't have CREATE DATABASE IF NOT EXISTS)
-- The database should be created by the Docker container environment variables

-- Enable UUID extension for future use
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Log successful initialization
DO $$
BEGIN
    RAISE NOTICE 'PNCP Ingestion Database initialized successfully';
END $$; 