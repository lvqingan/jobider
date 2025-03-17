CREATE TABLE companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    parent_id INT,
    source INT UNSIGNED NOT NULL,
    index_url VARCHAR(255) NOT NULL,
    request_method ENUM('GET', 'POST') NOT NULL,
    FOREIGN KEY (parent_id) REFERENCES companies(id) ON DELETE SET NULL
);

CREATE TABLE company_details (
    company_id INT PRIMARY KEY,
    logo LONGBLOB NOT NULL,
    about TEXT,
    website VARCHAR(255),
    industry VARCHAR(255),
    company_size VARCHAR(255),
    country VARCHAR(255),
    city VARCHAR(255),
    founded YEAR,
    linkedin VARCHAR(255),
    facebook VARCHAR(255),
    youtube VARCHAR(255),
    instagram VARCHAR(255),
    twitter VARCHAR(255),
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

CREATE TABLE jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    source_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    employment_type VARCHAR(50),
    benefits TEXT,
    requirements TEXT,
    url VARCHAR(255) NOT NULL,
    locations VARCHAR(255),
    published_at DATETIME,
    updated_at DATETIME,
    workplace VARCHAR(50),
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

CREATE INDEX idx_jobs_published_at ON jobs (published_at);

CREATE INDEX idx_jobs_updated_at ON jobs (updated_at);