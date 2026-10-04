# 🔧 Correção de Python — Resumo Executivo

## Problema Encontrado

Ao executar `python run.py`, ocorreu erro de incompatibilidade:

```
AssertionError: Class <class 'sqlalchemy.sql.elements.SQLCoreOperations'> 
directly inherits TypingOnly but has additional attributes
```

**Causa**: Python 3.13.7 + SQLAlchemy 2.0.23 são incompatíveis

## Solução Adotada

**Opção Recomendada**: Usar Python 3.12 (versão estável)

- Totalmente compatível com SQLAlchemy 2.0.23
- Amplamente testado
- Suporte completo
- Fácil instalação em Windows 11

## O que foi criado

5 arquivos de suporte para facilitar a correção:

### 📋 Documentação

1. **COMECE_AQUI.txt** — Guia de início rápido
   - Timeline: 15-20 minutos
   - Checklist de progresso
   - Perguntas frequentes
   - **LEIA PRIMEIRO**

2. **CORRIGIR_PYTHON.md** — Guia completo
   - 3 passos detalhados
   - Opções alternativas
   - Troubleshooting
   - Comparativo de versões

3. **FIX_PYTHON_RAPIDO.txt** — Resumo em 3 passos
   - Formato texto simples
   - Instruções concisas
   - Teste rápido

4. **LEIA_PRIMEIRO.txt** — Visão geral executiva
   - Timeline visual
   - Próximos passos
   - Tempo estimado
   - O que fazer depois

### 🔧 Scripts Automatizados

5. **INSTALAR_PYTHON312.ps1** — Desinstalação
   - Script interativo PowerShell
   - Desinstala Python 3.13 automaticamente
   - Oferece opção manual se necessário

6. **APOS_PYTHON312.ps1** — Configuração
   - Executa APÓS instalar Python 3.12
   - Recria ambiente virtual (venv)
   - Instala todas as dependências
   - Deixa tudo pronto

## Próximos Passos

### Passo 1: Desinstalar Python 3.13 (5 min)

**Opção A - Manual (Recomendado)**:
1. Abra Settings > Apps > Apps & features
2. Procure por "Python 3.13"
3. Clique em "Uninstall"
4. **MARQUE**: "Remove Python 3.13 from PATH" (importante!)
5. Confirme

**Opção B - Automático**:
```powershell
cd C:\iplan-sisgen\capacidade1
.\INSTALAR_PYTHON312.ps1
# Escolha opção [1]
```

### Passo 2: Instalar Python 3.12 (5 min)

1. Vá para: https://www.python.org/downloads/release/python-3120/
2. Baixe: **Windows installer (64-bit)**
3. Execute o instalador
4. **NA PRIMEIRA TELA**:
   - ☑️ "Install launcher for all users"
   - ☑️ **"Add Python 3.12 to PATH"** ← CRÍTICO!
5. Clique "Install Now"
6. Aguarde completar (~3 min)
7. Clique "Close"

### Passo 3: Configurar Projeto (5 min)

Abra PowerShell (normal) e execute:

```powershell
cd C:\iplan-sisgen\capacidade1
.\APOS_PYTHON312.ps1
```

Este script irá:
- Verificar Python 3.12
- Recrear ambiente virtual
- Instalar dependências
- Deixar tudo pronto

### Passo 4: Testar (1 min)

```powershell
python --version
# Esperado: Python 3.12.x

python run.py
# Deve iniciar sem erros
```

### Passo 5: Acessar Aplicação (1 min)

Abra navegador: **http://localhost:5000**

Você deve ver o menu com 14 funcionalidades.

## Tempo Total

⏱️ **15-20 minutos**

- Desinstalação: 5 min
- Download/instalação Python 3.12: 5-10 min
- Configuração do projeto: 5 min
- Teste: 1 min

Maioria é download (depende de sua internet).

## Verificação

Após cada passo, você pode verificar:

```powershell
# Verificar versão Python
python --version

# Verificar venv ativo
python -c "import sys; print(sys.prefix)"

# Verificar dependências
pip list
```

## Se Algo Falhar

Veja a seção "SE ALGO FALHAR" em **CORRIGIR_PYTHON.md**

Problemas comuns e soluções:

- "python is not recognized" → Python não está no PATH
- "Module not found" → venv com Python 3.13
- Erro de permissão → Precisa reinstalar (admin)

## Depois de Tudo Funcionar

1. Teste os 14 módulos da aplicação
2. Valide comportamento conforme evidências originais
3. Se tudo OK: **"CAPACIDADE APROVADA"**

## Arquivos Relacionados

- Documentação original: `README.md`
- Guia rápido: `QUICK_START.md`
- Detalhes técnicos: `COMPLETION_SUMMARY.md`

## Status

✅ **Correção análisada e mitigada**
✅ **Arquivos de suporte criados**
✅ **Scripts automatizados prontos**
✅ **Documentação completa fornecida**

**Próximo**: Seguir os 5 passos acima (15-20 min)

---

**Criado**: Outubro de 2026
**Versão Python necessária**: 3.12.x
**Sistema Operacional**: Windows 11

