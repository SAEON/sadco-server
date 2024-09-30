CREATE TABLE sadco.download_audit (
    timestamp TIMESTAMP NOT NULL,
    client_id VARCHAR NOT NULL,
    user_id VARCHAR,
    survey_type VARCHAR,
    parameters VARCHAR,
    download_file_size NUMERIC,
    download_file_checksum VARCHAR,
    PRIMARY KEY (timestamp, client_id)
);
