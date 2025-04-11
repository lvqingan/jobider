-- Disable foreign key constraint checks
SET FOREIGN_KEY_CHECKS = 0;
-- Disable unique constraint checks
SET UNIQUE_CHECKS = 0;

-- Drop the database if it exists
DROP DATABASE IF EXISTS jobider;

-- Create the database
CREATE DATABASE jobider CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- Use the created database
USE jobider;

-- Drop the table if it exists
DROP TABLE IF EXISTS companies;

-- Create the companies table
CREATE TABLE companies (
    id int unsigned NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL UNIQUE,
    parent_id int unsigned DEFAULT NULL,
    source VARCHAR(255) NOT NULL,
    index_url varchar(255) NOT NULL,
    post_params json DEFAULT NULL,
    PRIMARY KEY (id),
    KEY parent_id (parent_id),
    CONSTRAINT companies_parent_id_foreign FOREIGN KEY (parent_id) REFERENCES companies (id) ON DELETE SET NULL
);

-- Drop the table if it exists
DROP TABLE IF EXISTS company_details;

-- Create the company_details table
CREATE TABLE company_details (
    company_id int unsigned NOT NULL,
    logo longblob,
    about text,
    website varchar(255) DEFAULT NULL,
    industry varchar(255) DEFAULT NULL,
    company_size varchar(255) DEFAULT NULL,
    country varchar(255) DEFAULT NULL,
    city varchar(255) DEFAULT NULL,
    founded varchar(255) DEFAULT NULL,
    linkedin varchar(512) DEFAULT NULL,
    facebook varchar(255) DEFAULT NULL,
    youtube varchar(255) DEFAULT NULL,
    instagram varchar(255) DEFAULT NULL,
    twitter varchar(255) DEFAULT NULL,
    PRIMARY KEY (company_id),
    CONSTRAINT company_details_company_id_foreign FOREIGN KEY (company_id) REFERENCES companies (id) ON DELETE CASCADE
);

-- Drop the table if it exists
DROP TABLE IF EXISTS jobs;

-- Create the jobs table
CREATE TABLE jobs (
    id int unsigned NOT NULL AUTO_INCREMENT,
    company_id int unsigned NOT NULL,
    internal_id varchar(255) NOT NULL,
    external_id varchar(255) DEFAULT NULL,
    title varchar(255) NOT NULL,
    description text,
    employment_type varchar(50) DEFAULT NULL,
    benefits text,
    requirements text,
    url varchar(255) NOT NULL,
    locations json DEFAULT NULL,
    published_at datetime DEFAULT NULL,
    expired_at datetime DEFAULT NULL,
    updated_at datetime DEFAULT NULL,
    workplace varchar(50) DEFAULT NULL,
    PRIMARY KEY (id),
    KEY company_id (company_id),
    CONSTRAINT jobs_company_id_foreign FOREIGN KEY (company_id) REFERENCES companies (id) ON DELETE CASCADE
);
CREATE INDEX idx_company_id_unique_id ON jobs (company_id, internal_id, external_id);

-- Enable foreign key constraint checks
SET FOREIGN_KEY_CHECKS = 1;
-- Enable unique constraint checks
SET UNIQUE_CHECKS = 1;    