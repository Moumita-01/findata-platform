import os

import oracledb
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()

# (symbol, asset_class, currency)
TICKERS = [
    # India
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "SBIN.NS", "ITC.NS", "LT.NS", "WIPRO.NS", "BHARTIARTL.NS",
    "AXISBANK.NS", "MARUTI.NS", "SUNPHARMA.NS", "TATASTEEL.NS", "ONGC.NS",
    # USA
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "JPM", "V", "JNJ", "XOM", "WMT",
    # Europe
    "NESN.SW", "NOVN.SW", "ROG.SW", "UBSG.SW", "SAP.DE", "SIE.DE",
    # ETFs / Index funds
    "SPY", "QQQ", "GLD", "TLT", "NIFTYBEES.NS",
]


def main():
    conn = oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN"),
    )
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE securities")

    sql = """
        INSERT INTO securities
        (security_id, symbol, name, asset_class, currency, sector)
        VALUES (:1, :2, :3, :4, :5, :6)
    """

    rows = []
    for i, symbol in enumerate(TICKERS, start=1):
        try:
            info = yf.Ticker(symbol).info
            quote_type = info.get("quoteType", "EQUITY")
            asset_class = "ETF" if quote_type == "ETF" else "EQUITY"
            rows.append((
                i,
                symbol,
                (info.get("longName") or info.get("shortName") or symbol)[:200],
                asset_class,
                (info.get("currency") or "USD")[:3].upper(),
                (info.get("sector") or "N/A")[:50],
            ))
            print(f"OK   {symbol}")
        except Exception as e:
            print(f"SKIP {symbol}: {e}")

    cur.executemany(sql, rows)
    conn.commit()
    print(f"Loaded {len(rows)} securities")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()