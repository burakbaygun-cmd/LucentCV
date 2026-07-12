param (
    [string]$env = "dev"
)

if ($env -eq "dev") {
    Write-Host "Starting LucentCV Development Environment..." -ForegroundColor Green
    
    # Start Backend in a new window
    Write-Host "Starting FastAPI Backend..."
    Start-Process powershell -ArgumentList "-NoExit -Command `"cd backend; python -m uvicorn main:app --reload`""
    
    # Start Frontend in a new window
    Write-Host "Starting Next.js Frontend..."
    Start-Process powershell -ArgumentList "-NoExit -Command `"cd frontend; npm run dev`""
    
} elseif ($env -eq "docker") {
    Write-Host "Starting Docker Environment..." -ForegroundColor Green
    docker-compose up -d
} else {
    Write-Host "Unknown environment. Use 'dev' or 'docker'." -ForegroundColor Red
}
