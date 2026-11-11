from pathlib import Path
from datetime import datetime
import duckdb
import pandas as pd

# Set project root
ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "warehouse" / "lendingclub.duckdb"
HISTORY = ROOT / "outputs" / "quality_history.csv"

con = duckdb.connect(str(DB_PATH), read_only=True)
cols = [r[0] for r in con.execute("Describe silver.stg_loans").fetchall()]
exprs = ", ".join(f"avg(({c} is null)::int) as \"{c}\"" for c in cols)
rates = con.execute(f"select {exprs} from silver.stg_loans").df().T.reset_index()
rates.columns = ["column", "null_rate"]
rates["run_at"] = datetime.now().isoformat(timespec = "seconds")
con.close()

if HISTORY.exists():
    prev = pd.read_csv(HISTORY)
    last = prev[prev.run_at == prev.run_at.max()][["column", "null_rate"]]
    cmp = rates.merge(last, on = "column", suffixes=("", "_prev"))
    drift = cmp[(cmp.null_rate - cmp.null_rate_prev).abs() > 0.01]
    print("Drift detected\n", drift if not drift.empty else "None")
    rates = pd.concat([prev, rates])

rates.to_csv(HISTORY, index=False)
print(f"Quality report saved to {HISTORY}")