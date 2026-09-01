# One-time fix: abort broken merge, sync to main, launch lab
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "Resetting repo to origin/main..." -ForegroundColor Yellow
git merge --abort 2>$null
git fetch origin main
git checkout main 2>$null
git reset --hard origin/main

Write-Host "Done. Starting Suspension Edge Lab..." -ForegroundColor Green
Set-Location "$PSScriptRoot\polymarket-trader-analyzer"
& "$PSScriptRoot\polymarket-trader-analyzer\START_SUSPENSION_LAB.ps1"
