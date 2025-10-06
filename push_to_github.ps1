# -----------------------------
# Push all local project files to GitHub
# -----------------------------
Write-Host "🚀 Starting Git upload process..." -ForegroundColor Cyan

# Initialize repo if not already done
if (-not (Test-Path ".git")) {
    git init
    Write-Host "✅ Initialized new Git repository." -ForegroundColor Green
}

# Add all files (force include new or modified)
git add -A
Write-Host "📁 Added all files to staging." -ForegroundColor Yellow

# Commit the files with a timestamp message
 = "Automated commit - 2025-10-06 19:39:19"
git commit -m ""
Write-Host "📝 Commit created: " -ForegroundColor Green

# Check if remote origin is set
 = git remote get-url origin 2>
if (-not ) {
     = Read-Host "Enter your GitHub repo URL (e.g. https://github.com/username/lg-inventory-agent-demo.git)"
    git remote add origin 
    git branch -M main
    Write-Host "🔗 Remote origin added: " -ForegroundColor Yellow
} else {
    Write-Host "🔗 Existing remote: " -ForegroundColor Gray
}

# Push to GitHub main branch
Write-Host "⬆️  Pushing files to GitHub..." -ForegroundColor Cyan
git push -u origin main

if (0 -eq 0) {
    Write-Host "✅ All files successfully pushed to GitHub!" -ForegroundColor Green
} else {
    Write-Host "❌ Push failed. Please check your network or credentials." -ForegroundColor Red
}
