$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
& .\.venv\Scripts\Activate.ps1

Write-Host "1/4 Loading bronze..." -ForegroundColor Cyan
python -m ingestion.load_bronze

Write-Host "2/4 Building silver/gold + dbt tests..." -ForegroundColor Cyan
Push-Location dbt
dbt build --profiles-dir .
if ($LASTEXITCODE -ne 0) { Pop-Location; throw "dbt build failed" }
Pop-Location

Write-Host "3/4 Data quality report..." -ForegroundColor Cyan
python quality\report.py

Write-Host "4/4 Python tests..." -ForegroundColor Cyan
pytest -q
if ($LASTEXITCODE -ne 0) { throw "pytest failed" }

Write-Host "Pipeline complete." -ForegroundColor Green
