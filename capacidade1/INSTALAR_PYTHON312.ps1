# Script para Desinstalar Python 3.13 e Instalar Python 3.12
# Execute como Administrador

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Instalacao de Python 3.12" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Passo 1: Verificar Python atual
Write-Host "PASSO 1: Verificando Python atual..." -ForegroundColor Yellow
python --version
Write-Host ""

# Passo 2: Opcoes
Write-Host "PASSO 2: Escolha uma opcao:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  [1] Desinstalar Python 3.13 automaticamente (REQUER ADMIN)"
Write-Host "  [2] Apenas mostrar como desinstalar manualmente"
Write-Host ""

$choice = Read-Host "Digite 1 ou 2"

if ($choice -eq "1") {
    Write-Host ""
    Write-Host "Tentando desinstalar Python 3.13..." -ForegroundColor Yellow
    
    try {
        # Encontrar e desinstalar Python 3.13
        $python313 = Get-WmiObject Win32_Product | Where-Object { $_.Name -like "*Python 3.13*" }
        
        if ($python313) {
            Write-Host "Encontrado: $($python313.Name)"
            Write-Host "Desinstalando..." -ForegroundColor Yellow
            $python313.Uninstall() | Out-Null
            Start-Sleep -Seconds 3
            Write-Host "Python 3.13 desinstalado com sucesso!" -ForegroundColor Green
        } else {
            Write-Host "Python 3.13 nao encontrado" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "Erro ao desinstalar: $_" -ForegroundColor Red
        Write-Host "Tente desinstalar manualmente via 'Programas e Recursos'" -ForegroundColor Yellow
    }
}
elseif ($choice -eq "2") {
    Write-Host ""
    Write-Host "PASSOS MANUAIS:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Abra Settings (Configuracoes)"
    Write-Host "2. Vá para: Apps > Apps & features"
    Write-Host "3. Procure por 'Python 3.13'"
    Write-Host "4. Clique em 'Uninstall'"
    Write-Host "5. Marque 'Remove Python 3.13 from PATH'"
    Write-Host "6. Confirme"
    Write-Host ""
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Agora instale Python 3.12" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "PASSOS:"
Write-Host ""
Write-Host "1. Abra navegador: https://www.python.org/downloads/release/python-3120/"
Write-Host ""
Write-Host "2. Baixe: 'Windows installer (64-bit)'"
Write-Host ""
Write-Host "3. Execute o instalador (python-3.12.0-amd64.exe)"
Write-Host ""
Write-Host "4. NA PRIMEIRA TELA, MARQUE ESTAS OPCOES:"
Write-Host "   [X] Install launcher for all users"
Write-Host "   [X] Add Python 3.12 to PATH    <-- MUITO IMPORTANTE!"
Write-Host ""
Write-Host "5. Clique 'Install Now'"
Write-Host ""
Write-Host "6. Espere completar"
Write-Host ""
Write-Host "7. Clique 'Disable path length limit' (opcional)"
Write-Host ""
Write-Host "8. Clique 'Close'"
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "Apos instalar Python 3.12, execute:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  python --version"
Write-Host ""
Write-Host "Deve mostrar: Python 3.12.x"
Write-Host ""

Pause
