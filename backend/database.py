import sqlite3
import pandas as pd
import os
from backend.config import DB_PATH

def connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = connect()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ticks (
            symbol TEXT,
            ts TEXT,
            price REAL,
            size REAL
        )
    """)
    conn.commit()
    conn.close()

def insert_tick(tick):
    conn = connect()
    conn.execute(
        "INSERT INTO ticks VALUES (?, ?, ?, ?)",
        (tick["symbol"], tick["ts"], tick["price"], tick["size"])
    )
    conn.commit()
    conn.close()

def load_symbol(symbol):
    conn = connect()
    df = pd.read_sql(
        "SELECT * FROM ticks WHERE symbol=?",
        conn,
        params=(symbol,)
    )
    conn.close()

    if df.empty:
        return df

    df["ts"] = pd.to_datetime(
        df["ts"],
        utc=True,
        format="mixed",
        errors="coerce"
    )

    df = df.dropna(subset=["ts"])
    return df.set_index("ts").sort_index()


def resample(df, rule):
    if df.empty:
        return df

    return (
        df.resample(rule)
          .agg({
              "price": "last",
              "size": "sum"
          })
          .dropna()
    )
