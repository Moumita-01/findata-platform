import os
import random
from datetime import datetime, timedelta

import oracledb
from dotenv import load_dotenv

load_dotenv()
random.seed(42)

ACCOUNT_TYPES = ["SAVINGS", "CURRENT", "INVESTMENT", "LOAN"]
TYPE_WEIGHTS = [40, 25, 30, 5]
CURRENCIES = ["INR", "USD", "EUR", "CHF", "GBP", "SGD"]
CURRENCY_WEIGHTS = [40, 20, 15, 10, 10, 5]
STATUSES = ["ACTIVE", "DORMANT", "CLOSED"]
STATUS_WEIGHTS = [90, 7, 3]
BATCH_SIZE = 20_000


def main():
    conn = oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN"),
    )
    cur = conn.cursor()
    cur.execute("SELECT client_id FROM clients")
    client_ids = [r[0] for r in cur.fetchall()]

    cur.execute("TRUNCATE TABLE accounts")

    sql = """
        INSERT INTO accounts
        (account_id, client_id, account_type, currency, balance,
         status, opened_at, updated_at)
        VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
    """

    rows, account_id = [], 1
    start = datetime.now()
    for client_id in client_ids:
        for _ in range(random.choices([1, 2, 3], [50, 35, 15])[0]):
            opened = datetime.now() - timedelta(days=random.randint(0, 3650))
            rows.append((
                account_id,
                client_id,
                random.choices(ACCOUNT_TYPES, TYPE_WEIGHTS)[0],
                random.choices(CURRENCIES, CURRENCY_WEIGHTS)[0],
                round(random.uniform(100, 500_000), 2),
                random.choices(STATUSES, STATUS_WEIGHTS)[0],
                opened,
                opened,
            ))
            account_id += 1
            if len(rows) >= BATCH_SIZE:
                cur.executemany(sql, rows)
                conn.commit()
                print(f"Loaded {account_id - 1:,} accounts")
                rows = []

    if rows:
        cur.executemany(sql, rows)
        conn.commit()

    print(f"Total accounts: {account_id - 1:,} in {(datetime.now() - start).seconds}s")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()