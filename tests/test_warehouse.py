from pathlib import Path
import pytest
import duckdb

DB = Path(__file__).resolve().parents[1] / "warehouse" / "lendingclub.duckdb"

@pytest.fixture(scope = "module")
def con():
    c = duckdb.connect(str(DB), read_only=True)
    yield c
    c.close()

def test_load_bronze(con):
    assert con.execute("SELECT count(*) FROM bronze.loans_raw").fetchone()[0] > 2000000

def test_silver_matchis_gold(con):
    silver = con.execute("SELECT count(*) FROM silver.stg_loans").fetchone()[0]
    gold = con.execute("SELECT count(*) FROM gold.fct_loans").fetchone()[0]
    assert silver == gold

def test_no_orphan_loans(con):
    orphans = con.execute("""
        SELECT count(*) FROM gold.fct_loans f
        LEFT JOIN gold.dim_grade g USING (grade_key)
        WHERE g.grade_key IS NULL
    """).fetchone()[0]
    assert orphans == 0
