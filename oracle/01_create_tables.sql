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

CREATE TABLE accounts (
    account_id     NUMBER PRIMARY KEY,
    client_id      NUMBER NOT NULL REFERENCES clients(client_id),
    account_type   VARCHAR2(20),
    currency       VARCHAR2(3),
    balance        NUMBER(18,2),
    status         VARCHAR2(10),
    opened_at      DATE DEFAULT SYSDATE,
    updated_at     DATE DEFAULT SYSDATE
);

CREATE INDEX idx_accounts_client ON accounts(client_id);

CREATE TABLE securities (
    security_id    NUMBER PRIMARY KEY,
    symbol         VARCHAR2(20) UNIQUE,
    name           VARCHAR2(200),
    asset_class    VARCHAR2(20),
    currency       VARCHAR2(3),
    sector         VARCHAR2(50)
);