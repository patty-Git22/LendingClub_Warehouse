from pathlib import Path
import duckdb

# Project root
ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = next((ROOT / "data" / "raw").glob("accepted_*.csv*"))
DB_PATH = ROOT / "warehouse" / "lendingclub.duckdb"


def load() -> int:
    con = duckdb.connect(str(DB_PATH))
    con.execute("CREATE SCHEMA IF NOT EXISTS bronze")
    # all_varchar = keep raw text; typing happens in silver
    con.execute(f"""
        CREATE OR REPLACE TABLE bronze.loans_raw AS
        SELECT *,
               current_timestamp AS _loaded_at,
               '{RAW_FILE.name}'  AS _source_file
        FROM read_csv('{RAW_FILE.as_posix()}', header=true, all_varchar=true)
    """)
    n = con.execute("SELECT count(*) FROM bronze.loans_raw").fetchone()[0]
    con.close()
    print(f"Loaded {n:,} rows into bronze.loans_raw")
    return n


if __name__ == "__main__":
    load()