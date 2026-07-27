import sqlite3
import pandas as pd
import streamlit as st
from pathlib import Path

# Database Path
BASE_DIR = Path(__file__).resolve().parents[3]
DB_PATH = BASE_DIR / "nifty100.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# -----------------------------
# Companies
# -----------------------------
@st.cache_data(ttl=600)
def get_companies():
    conn = get_connection()

    try:
        return pd.read_sql(
            """
            SELECT *
            FROM companies
            ORDER BY company_name
            """,
            conn,
        )

    finally:
        conn.close()


# -----------------------------
# Financial Ratios
# -----------------------------
@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):
    conn = get_connection()

    try:
        query = """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        """

        params = [ticker]

        if year is not None:
            query += " AND year=?"
            params.append(year)

        query += " ORDER BY year"

        return pd.read_sql(query, conn, params=params)

    finally:
        conn.close()


# -----------------------------
# Profit & Loss
# -----------------------------
@st.cache_data(ttl=600)
def get_pl(ticker):
    conn = get_connection()

    try:
        return pd.read_sql(
            """
            SELECT *
            FROM profitandloss
            WHERE company_id=?
            ORDER BY year
            """,
            conn,
            params=[ticker],
        )

    finally:
        conn.close()


# -----------------------------
# Balance Sheet
# -----------------------------
@st.cache_data(ttl=600)
def get_bs(ticker):
    conn = get_connection()

    try:
        return pd.read_sql(
            """
            SELECT *
            FROM balancesheet
            WHERE company_id=?
            ORDER BY year
            """,
            conn,
            params=[ticker],
        )

    finally:
        conn.close()


# -----------------------------
# Cash Flow
# -----------------------------
@st.cache_data(ttl=600)
def get_cf(ticker):
    conn = get_connection()

    try:
        return pd.read_sql(
            """
            SELECT *
            FROM cashflow
            WHERE company_id=?
            ORDER BY year
            """,
            conn,
            params=[ticker],
        )

    finally:
        conn.close()


# -----------------------------
# Sector Information
# -----------------------------
@st.cache_data(ttl=600)
def get_sectors():
    conn = get_connection()

    try:
        return pd.read_sql(
            """
            SELECT *
            FROM sectors
            ORDER BY broad_sector, company_id
            """,
            conn,
        )

    finally:
        conn.close()


# -----------------------------
# Peer Groups
# -----------------------------
@st.cache_data(ttl=600)
def get_peers():
    conn = get_connection()

    try:
        return pd.read_sql(
            """
            SELECT *
            FROM peer_groups
            ORDER BY company_id
            """,
            conn,
        )

    finally:
        conn.close()


# -----------------------------
# Market Cap
# -----------------------------
@st.cache_data(ttl=600)
def get_market_cap(year=None):
    conn = get_connection()

    try:
        query = """
        SELECT *
        FROM market_cap
        """

        params = []

        if year is not None:
            query += " WHERE year=?"
            params.append(year)

        query += " ORDER BY market_cap_crore DESC"

        return pd.read_sql(query, conn, params=params)

    finally:
        conn.close()


# -----------------------------
# Analysis
# -----------------------------
@st.cache_data(ttl=600)
def get_analysis():
    conn = get_connection()

    try:
        return pd.read_sql(
            """
            SELECT *
            FROM analysis
            """,
            conn,
        )

    finally:
        conn.close()