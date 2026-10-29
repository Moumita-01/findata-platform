import os
import time

import numpy as np
import oracledb
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

TOTAL_TXNS = 5_000_000
CHUNK = 250_000
START_DATE = pd.Timestamp("2022-01-01")
END_DATE = pd.Timestamp("2026-10-01")

TXN_TYPES = np.array(["DEPOSIT", "WITHDRAWAL", "TRANSFER", "BUY", "SELL", "FEE", "DIVIDEND"])
TYPE_P = [0.25, 0.20, 0.20, 0.12, 0.10, 0.08, 0.05]
STATUSES = np.array(["COMPLETED", "PENDING", "FAILED"])
STATUS_P = [0.95, 0.03, 0.02]

rng = np.random.default_rng(42)


def main():
    conn = oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN"),
    )
    cur = conn.cursor()

    cur.execute("SELECT account_id, currency FROM accounts")
    acc = pd.DataFrame(cur.fetchall(), columns=["account_id", "currency"])
    cur.execute("SELECT security_id FROM securities")
    sec_ids = np.array([r[0] for r in cur.fetchall()])

    cur.execute("TRUNCATE TABLE transactions")

    sql = """
        INSERT INTO transactions
        (txn_id, account_id, security_id, txn_type, amount,
         quantity, currency, txn_date, status)
        VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)
    """

    days = (END_DATE - START_DATE).days
    acc_ids = acc["account_id"].to_numpy()
    acc_cur = acc["currency"].to_numpy()

    t0 = time.time()
    loaded = 0
    while loaded < TOTAL_TXNS:
        n = min(CHUNK, TOTAL_TXNS - loaded)
        idx = rng.integers(0, len(acc_ids), n)
        types = rng.choice(TXN_TYPES, n, p=TYPE_P)
        is_trade = np.isin(types, ["BUY", "SELL", "DIVIDEND"])

        sec = np.where(is_trade, rng.choice(sec_ids, n), 0)
        qty = np.where(is_trade, np.round(rng.uniform(1, 500, n), 4), 0)
        amount = np.round(rng.lognormal(6, 1.2, n), 2)
        dates = START_DATE + pd.to_timedelta(rng.integers(0, days, n), unit="D")

        rows = list(zip(
            (np.arange(loaded + 1, loaded + n + 1)).tolist(),
            acc_ids[idx].tolist(),
            [int(s) if s else None for s in sec],
            types.tolist(),
            amount.tolist(),
            [float(q) if q else None for q in qty],
            acc_cur[idx].tolist(),
            dates.to_pydatetime().tolist(),
            rng.choice(STATUSES, n, p=STATUS_P).tolist(),
        ))
        cur.executemany(sql, rows)
        conn.commit()
        loaded += n
        print(f"Loaded {loaded:,} / {TOTAL_TXNS:,}  ({time.time() - t0:.0f}s)")

    print(f"Done in {time.time() - t0:.0f} seconds")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()