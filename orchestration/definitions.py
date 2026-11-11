import sys
from pathlib import Path
import dagster as dg
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ingestion.load_bronze import load

dbt_project = DbtProject(project_dir = ROOT / "dbt", profiles_dir = ROOT / "dbt")
dbt_project.prepare_if_dev()

# Key matching the dbt model name to the dagster asset name
@dg.asset(key = ["bronze", "loans_raw"], group_name = "ingestion")
def loans_raw() -> dg.MaterializeResult:
    n = load()
    return dg.MaterializeResult(metadata = {"row_count": n})

@dbt_assets(manifest = dbt_project.manifest_path)
def lendingclub_dbt(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context = context).stream()

defs = dg.Definitions(
    assets=[loans_raw, lendingclub_dbt],
    resources={"dbt": DbtCliResource(project_dir=dbt_project)},
)