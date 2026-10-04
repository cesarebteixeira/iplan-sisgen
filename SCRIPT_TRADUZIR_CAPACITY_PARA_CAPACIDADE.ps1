# ============================================================================
# Script PowerShell para Traduzir "Capacity 1" para "Capacidade 1"
# ============================================================================
# Propósito: Substituir todas as ocorrências de "Capacity 1" por "Capacidade 1"
# Data: 03/10/2026
# Uso: .\SCRIPT_TRADUZIR_CAPACITY_PARA_CAPACIDADE.ps1
# ============================================================================

param(
    [string]$RootPath = "C:\iplan-sisgen\capacidade1",
    [switch]$DryRun = $true  # $true = apenas visualiza; $false = faz mudanças
)

Write-Host "============================================================================"
Write-Host "SCRIPT DE TRADUÇÃO: Capacity 1 → Capacidade 1"
Write-Host "============================================================================"
Write-Host "Caminho raiz: $RootPath"
Write-Host "Modo: $(if ($DryRun) { 'VISUALIZAÇÃO (Dry-Run)' } else { 'EXECUTAR MUDANÇAS' })"
Write-Host ""

# Definir os padrões de busca e substituição
$replacements = @(
    @{
        Pattern = "Capacity 1 - Estrutura da rede e do gasto"
        Replacement = "Capacidade 1 - Estrutura da rede e do gasto"
        Description = "String completa com " -" e descrição"
    },
    @{
        Pattern = "Capacity 1"
        Replacement = "Capacidade 1"
        Description = "String simples 'Capacity 1'"
    }
)

# Extensões de arquivo a processar
$fileExtensions = @("*.py", "*.html", "*.css", "*.txt", "*.md")

# Contadores
$totalFilesFound = 0
$totalReplacements = 0
$filesModified = @()

Write-Host "ETAPA 1: Buscando arquivos..."
Write-Host "─────────────────────────────────────────────────────────────────────────────"

# Procurar todos os arquivos
foreach ($extension in $fileExtensions) {
    $files = Get-ChildItem -Path $RootPath -Filter $extension -Recurse -ErrorAction SilentlyContinue
    
    foreach ($file in $files) {
        $content = Get-Content -Path $file.FullName -Raw -ErrorAction SilentlyContinue
        
        if ($null -eq $content) {
            continue
        }
        
        $hasMatches = $false
        $matchCount = 0
        
        # Verificar cada padrão
        foreach ($replacement in $replacements) {
            if ($content -match [regex]::Escape($replacement.Pattern)) {
                $hasMatches = $true
                # Contar ocorrências
                $matches = [regex]::Matches($content, [regex]::Escape($replacement.Pattern))
                $matchCount += $matches.Count
            }
        }
        
        if ($hasMatches) {
            $totalFilesFound++
            $totalReplacements += $matchCount
            
            Write-Host "Arquivo: $($file.FullName -replace [regex]::Escape($RootPath), '.')"
            Write-Host "  Ocorrências encontradas: $matchCount"
            Write-Host ""
        }
    }
}

Write-Host "RESUMO DA BUSCA:"
Write-Host "───────────────────────────────────────────────────────────────────────────"
Write-Host "Total de arquivos com 'Capacity': $totalFilesFound"
Write-Host "Total de ocorrências: $totalReplacements"
Write-Host ""

if ($totalFilesFound -eq 0) {
    Write-Host "Nenhum arquivo contendo 'Capacity' foi encontrado."
    exit 0
}

# Se não é dry-run, fazer as substituições
if (-not $DryRun) {
    Write-Host "ETAPA 2: Executando substituições..."
    Write-Host "─────────────────────────────────────────────────────────────────────────────"
    Write-Host ""
    
    foreach ($extension in $fileExtensions) {
        $files = Get-ChildItem -Path $RootPath -Filter $extension -Recurse -ErrorAction SilentlyContinue
        
        foreach ($file in $files) {
            $content = Get-Content -Path $file.FullName -Raw -ErrorAction SilentlyContinue
            $originalContent = $content
            
            if ($null -eq $content) {
                continue
            }
            
            $hasChanges = $false
            
            # Aplicar cada padrão de substituição
            foreach ($replacement in $replacements) {
                if ($content -match [regex]::Escape($replacement.Pattern)) {
                    $content = $content -replace [regex]::Escape($replacement.Pattern), $replacement.Replacement
                    $hasChanges = $true
                }
            }
            
            if ($hasChanges) {
                try {
                    Set-Content -Path $file.FullName -Value $content -Encoding UTF8
                    $filesModified += $file.FullName
                    Write-Host "Modificado: $($file.FullName -replace [regex]::Escape($RootPath), '.')"
                }
                catch {
                    Write-Host "ERRO ao modificar: $($file.FullName)" -ForegroundColor Red
                    Write-Host "Detalhes: $_" -ForegroundColor Red
                }
            }
        }
    }
    
    Write-Host ""
    Write-Host "RESUMO DE MODIFICAÇÕES:"
    Write-Host "───────────────────────────────────────────────────────────────────────────"
    Write-Host "Total de arquivos modificados: $($filesModified.Count)"
    Write-Host ""
    
    if ($filesModified.Count -gt 0) {
        Write-Host "Arquivos modificados:"
        $filesModified | ForEach-Object {
            Write-Host "  ✓ $($_ -replace [regex]::Escape($RootPath), '.')"
        }
    }
}
else {
    Write-Host "MODO DRY-RUN: Nenhuma mudança foi feita."
    Write-Host "Para executar de verdade, execute com: -DryRun `$false"
    Write-Host ""
    Write-Host "EXEMPLO:"
    Write-Host "  .\SCRIPT_TRADUZIR_CAPACITY_PARA_CAPACIDADE.ps1 -DryRun `$false"
}

Write-Host ""
Write-Host "============================================================================"
Write-Host "PROCESSO CONCLUÍDO"
Write-Host "============================================================================"

# ============================================================================
# INSTRUÇÕES DE USO
# ============================================================================
<#
COMO USAR ESTE SCRIPT:

1. VISUALIZAÇÃO (Dry-Run):
   .\SCRIPT_TRADUZIR_CAPACITY_PARA_CAPACIDADE.ps1
   ou
   .\SCRIPT_TRADUZIR_CAPACITY_PARA_CAPACIDADE.ps1 -DryRun $true

2. EXECUTAR MUDANÇAS:
   .\SCRIPT_TRADUZIR_CAPACITY_PARA_CAPACIDADE.ps1 -DryRun $false

3. ESPECIFICAR CAMINHO DIFERENTE:
   .\SCRIPT_TRADUZIR_CAPACITY_PARA_CAPACIDADE.ps1 -RootPath "C:\outro\caminho" -DryRun $false

PADRÕES DE SUBSTITUIÇÃO:
────────────────────────
1. "Capacity 1 - Estrutura da rede e do gasto" 
   → "Capacidade 1 - Estrutura da rede e do gasto"

2. "Capacity 1" 
   → "Capacidade 1"

ARQUIVOS A SEREM PROCESSADOS:
─────────────────────────────
- *.py   (Python)
- *.html (HTML/Templates)
- *.css  (CSS)
- *.txt  (Text)
- *.md   (Markdown)

SEGURANÇA:
──────────
✓ O script sempre faz backup na memória
✓ Use -DryRun $true primeiro para visualizar mudanças
✓ Os arquivos originais são sobrescritos com UTF-8 encoding
✓ Recomenda-se ter backup antes de executar

#>
