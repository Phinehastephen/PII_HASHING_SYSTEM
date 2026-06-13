-- Stage 1
CREATE DATABASE pii_hashing_system;

USE pii_hashing_system;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE uploaded_files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255),
    uploaded_by INT,
    status VARCHAR(50),
    records_processed INT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE processing_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_id INT,
    records_processed INT,
    records_hashed INT,
    errors_found INT,
    report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- use after only using stage 1 (Stage 2 ) 
DROP TABLE IF EXISTS uploaded_files;

CREATE TABLE uploaded_files (
    id INT AUTO_INCREMENT PRIMARY KEY,

    filename VARCHAR(255),

    stored_filename VARCHAR(255),

    uploaded_by INT,

    status VARCHAR(50) DEFAULT 'Pending',

    records_processed INT DEFAULT 0,

    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (uploaded_by)
    REFERENCES users(id)
);