CREATE TABLE clients (
    client_id     NUMBER PRIMARY KEY,
    first_name    VARCHAR2(100),
    last_name     VARCHAR2(100),
    country       VARCHAR2(50),
    risk_profile  VARCHAR2(20),
    created_at    DATE DEFAULT SYSDATE,
    updated_at    DATE DEFAULT SYSDATE
);

INSERT INTO clients (client_id, first_name, last_name, country, risk_profile)
VALUES (1, 'Test', 'User', 'India', 'MEDIUM');

COMMIT;

SELECT * FROM clients;

DROP TABLE clients PURGE;

CREATE TABLE clients (
    client_id     NUMBER PRIMARY KEY,
    first_name    VARCHAR2(100),
    last_name     VARCHAR2(100),
    email         VARCHAR2(200),
    country       VARCHAR2(50),
    risk_profile  VARCHAR2(20),
    kyc_status    VARCHAR2(20),
    created_at    DATE DEFAULT SYSDATE,
    updated_at    DATE DEFAULT SYSDATE
);