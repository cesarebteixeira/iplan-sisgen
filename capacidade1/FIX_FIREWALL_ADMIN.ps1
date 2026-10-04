# Script para adicionar Flask (porta 5000) ao Windows Firewall
# EXECUTAR COMO ADMINISTRADOR!

Write-Host ""
Write-Host "╔═════════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║                                                                 ║" -ForegroundColor Yellow
Write-Host "║   SCRIPT DE FIREWALL - EXECUTAR COMO ADMINISTRADOR!           ║" -ForegroundColor Yellow
Write-Host "║                                                                 ║" -ForegroundColor Yellow
Write-Host "╚═════════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
Write-Host ""

# Verificar se está rodando como admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "❌ ERRO: Este script DEVE ser executado como Administrador!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Como executar como admin:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  1. Abra PowerShell" -ForegroundColor White
    Write-Host "  2. Clique com botão direito em PowerShell" -ForegroundColor White
    Write-Host "  3. Selecione 'Executar como administrador'" -ForegroundColor White
    Write-Host "  4. Digite: C:\iplan-sisgen\capacidade1\FIX_FIREWALL_ADMIN.ps1" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host "✅ Executando com permissões de administrador" -ForegroundColor Green
Write-Host ""

Write-Host "Adicionando Flask (porta 5000) ao Windows Firewall..." -ForegroundColor Yellow
Write-Host ""

# Adicionar regra para porta 5000 (entrada)
Write-Host "1. Adicionando regra de entrada (Inbound) para porta 5000..." -ForegroundColor Cyan
netsh advfirewall firewall add rule `
    name="Flask Application Port 5000 (Inbound)" `
    dir=in `
    action=allow `
    protocol=tcp `
    localport=5000 `
    profile=any `
    description="Allows Flask web application on localhost:5000"

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Regra de entrada adicionada" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Falha ao adicionar (pode já existir)" -ForegroundColor Yellow
}

Write-Host ""

# Adicionar regra para porta 5000 (saída)
Write-Host "2. Adicionando regra de saída (Outbound) para porta 5000..." -ForegroundColor Cyan
netsh advfirewall firewall add rule `
    name="Flask Application Port 5000 (Outbound)" `
    dir=out `
    action=allow `
    protocol=tcp `
    localport=5000 `
    profile=any `
    description="Allows Flask web application on localhost:5000"

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Regra de saída adicionada" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Falha ao adicionar (pode já existir)" -ForegroundColor Yellow
}

Write-Host ""

# Adicionar Python ao firewall (opcional)
Write-Host "3. Adicionando python.exe ao firewall (via venv)..." -ForegroundColor Cyan

$pythonPath = "C:\iplan-sisgen\capacidade1\venv\Scripts\python.exe"

if (Test-Path $pythonPath) {
    netsh advfirewall firewall add rule `
        name="Python Flask Application" `
        dir=in `
        action=allow `
        program="$pythonPath" `
        profile=any `
        description="Allows Python Flask web framework"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Python adicionado ao firewall" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Falha ao adicionar (pode já existir)" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ⚠️  Python não encontrado em: $pythonPath" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "╔═════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                 ✅ FIREWALL CONFIGURADO                        ║" -ForegroundColor Green
Write-Host "╚═════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "Próximas ações:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1. Feche este PowerShell" -ForegroundColor White
Write-Host "  2. Abra PowerShell NOVO (admin não é mais necessário)" -ForegroundColor White
Write-Host "  3. Execute:" -ForegroundColor White
Write-Host ""
Write-Host "     cd C:\iplan-sisgen\capacidade1" -ForegroundColor Cyan
Write-Host "     .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "     python run.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "  4. Acesse: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""

Write-Host "Pressione qualquer tecla para fechar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
