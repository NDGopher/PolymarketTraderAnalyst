# Reset repo to origin/main and launch Suspension Edge Lab
Set-Location $PSScriptRoot

Write-Host "Resetting repo to origin/main..." -ForegroundColor Yellow

$prevErrorAction = $ErrorActionPreference
$ErrorActionPreference = "Continue"
git merge --abort 2>$null | Out-Null
$ErrorActionPreference = $prevErrorAction

git fetch origin main
git checkout main 2>$null | Out-Null
git reset --hard origin/main
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] git reset failed." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Done. Starting Suspension Edge Lab..." -ForegroundColor Green
Set-Location "$PSScriptRoot\polymarket-trader-analyzer"
& "$PSScriptRoot\polymarket-trader-analyzer\START_SUSPENSION_LAB.ps1"
