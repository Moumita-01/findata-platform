import os
import random
from datetime import datetime, timedelta

import oracledb
from dotenv import load_dotenv
from faker import Faker

load_dotenv()

NUM_CLIENTS = 100_000
BATCH_SIZE = 10_000

fake = Faker("en_IN")
Faker.seed(42)
random.seed(42)

COUNTRIES = ["India", "Switzerland", "Singapore", "UK", "USA", "UAE", "Germany"]
COUNTRY_WEIGHTS = [40, 15, 12, 10, 10, 8, 5]
RISK_PROFILES = ["LOW", "MEDIUM", "HIGH"]
RISK_WEIGHTS = [30, 50, 20]
KYC_STATUSES = ["VERIFIED", "PENDING", "EXPIRED"]
KYC_WEIGHTS = [85, 10, 5]


def make_row(client_id: int):
    created = datetime.now() - timedelta(days=random.randint(0, 3650))
    return (
        client_id,
        fake.first_name(),
        fake.last_name(),
        fake.unique.email(),
        random.choices(COUNTRIES, COUNTRY_WEIGHTS)[0],
        random.choices(RISK_PROFILES, RISK_WEIGHTS)[0],
        random.choices(KYC_STATUSES, KYC_WEIGHTS)[0],
        created,
        created,
    )


def main():
    conn = oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN"),
    )
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE clients")

    sql = """
        INSERT INTO clients
        (client_id, first_name, last_name, email, country,
         risk_profile, kyc_status, created_at, updated_at)
        VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)
    """

    start = datetime.now()
    for batch_start in range(1, NUM_CLIENTS + 1, BATCH_SIZE):
        rows = [
            make_row(i)
            for i in range(batch_start, min(batch_start + BATCH_SIZE, NUM_CLIENTS + 1))
        ]
        cur.executemany(sql, rows)
        conn.commit()
        print(f"Loaded {batch_start + len(rows) - 1:,} / {NUM_CLIENTS:,}")

    print(f"Done in {(datetime.now() - start).seconds} seconds")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()