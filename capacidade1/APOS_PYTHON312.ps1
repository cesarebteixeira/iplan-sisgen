# Script para executar APOS instalar Python 3.12
# Execute no PowerShell apos instalar Python 3.12

Write-Host "========================================" -ForegroundColor Green
Write-Host "  Configuracao pos-instalacao" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Verificar Python
Write-Host "Verificando Python 3.12..." -ForegroundColor Yellow
python --version

Write-Host ""

# Navegar para projeto
cd C:\iplan-sisgen\capacidade1

Write-Host "Diretorio: $(Get-Location)" -ForegroundColor Cyan
Write-Host ""

# Criar/ativar venv
Write-Host "Recriando ambiente virtual..." -ForegroundColor Yellow

# Remover venv antigo se existir
if (Test-Path ".\venv") {
    Write-Host "Removendo venv antigo..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force ".\venv"
}

# Criar novo venv
python -m venv venv

# Ativar venv
Write-Host "Ativando venv..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "Atualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host ""
Write-Host "Instalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Pronto para rodar!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Execute:"
Write-Host ""
Write-Host "  python run.py"
Write-Host ""
Write-Host "Depois abra:"
Write-Host ""
Write-Host "  http://localhost:5000"
Write-Host ""

Pause
