# 🔧 Correção: Python 3.13 → Python 3.12

## 📋 Problema Identificado

Você está usando **Python 3.13.7**, mas há uma incompatibilidade entre Python 3.13 e SQLAlchemy 2.0.23.

**Erro**:
```
AssertionError: Class <class 'sqlalchemy.sql.elements.SQLCoreOperations'> 
directly inherits TypingOnly but has additional attributes
```

**Solução**: Usar Python 3.12 (versão estável e totalmente compatível)

---

## ✅ Solução em 3 Passos

### PASSO 1: Desinstalar Python 3.13

#### Opção A: Via Settings (Mais fácil)

1. Abra **Settings** (Configurações)
2. Vá para **Apps > Apps & features**
3. Procure por **"Python 3.13"**
4. Clique em **"Uninstall"**
5. **IMPORTANTE**: Marque a opção **"Remove Python 3.13 from PATH"**
6. Clique **"Uninstall"** novamente
7. Aguarde completar
8. Clique **"Close"**

#### Opção B: Via PowerShell (Automático)

Abra PowerShell **como Administrador** e execute:

```powershell
cd C:\iplan-sisgen\capacidade1
.\INSTALAR_PYTHON312.ps1
```

Escolha opção **[1]** para desinstalar automaticamente.

### PASSO 2: Instalar Python 3.12

1. Abra navegador e vá para: **https://www.python.org/downloads/release/python-3120/**

2. Baixe o arquivo: **Windows installer (64-bit)**
   - Arquivo: `python-3.12.0-amd64.exe` (ou versão mais recente 3.12.x)

3. Execute o instalador (double-click)

4. **⚠️ IMPORTANTE NA PRIMEIRA TELA:**
   - ☑️ Marque: **"Install launcher for all users"**
   - ☑️ Marque: **"Add Python 3.12 to PATH"** ← **CRÍTICO!**
   - Clique: **"Install Now"**

5. Aguarde instalação completar (2-3 minutos)

6. Clique **"Disable path length limit"** (opcional mas recomendado)

7. Clique **"Close"**

### PASSO 3: Reconfigurar Projeto

Abra **PowerShell** (normal, não precisa admin) e execute:

```powershell
cd C:\iplan-sisgen\capacidade1
.\APOS_PYTHON312.ps1
```

Este script irá:
- ✅ Verificar Python 3.12
- ✅ Recrear ambiente virtual (venv)
- ✅ Instalar todas as dependências
- ✅ Ficar pronto para executar

---

## 🧪 Verificação

Após completar os 3 passos, verifique no PowerShell:

```powershell
python --version
```

**Esperado:**
```
Python 3.12.x
```

Se mostrar 3.12, você está pronto! ✅

---

## 🚀 Executar Aplicação

Depois de verificado, execute:

```powershell
cd C:\iplan-sisgen\capacidade1

# Se venv não está ativado:
.\venv\Scripts\Activate.ps1

# Executar:
python run.py
```

**Esperado:**
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://localhost:5000
* Press CTRL+C to quit
```

Abra navegador: **http://localhost:5000** ✅

---

## ❓ Se Encontrar Problemas

### Erro: "python: command not found" ou "python is not recognized"

**Causa**: Python não está no PATH

**Solução**:
1. Desinstale Python 3.12 completamente
2. Reinstale, **MARCANDO** "Add Python 3.12 to PATH"
3. Reinicie PowerShell após instalar

### Erro: "Module not found" após atualizar Python

**Solução**:
```powershell
cd C:\iplan-sisgen\capacidade1
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### venv já criado com Python 3.13

**Solução**:
```powershell
cd C:\iplan-sisgen\capacidade1
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 📊 Comparação

| Aspecto | Python 3.13 | Python 3.12 |
|---------|------------|-----------|
| **SQLAlchemy 2.0.23** | ❌ Incompatível | ✅ Compatível |
| **Flask 3.0.0** | ✅ Compatível | ✅ Compatível |
| **Estabilidade** | ⚠️ Novo | ✅ Testado |
| **Suporte** | ✅ Futuro | ✅ Presente |
| **Performance** | Ligeiramente melhor | Comprovada |

---

## ✅ Checklist Final

- [ ] Python 3.13 desinstalado
- [ ] Python 3.12 instalado
- [ ] Python 3.12 adicionado ao PATH
- [ ] PowerShell reiniciado
- [ ] `python --version` mostra 3.12.x
- [ ] `cd C:\iplan-sisgen\capacidade1` e executado `.\APOS_PYTHON312.ps1`
- [ ] Dependências instaladas
- [ ] `python run.py` executa sem erro
- [ ] Navegador abre `http://localhost:5000`

---

## 🎯 Próximo Passo

Após confirmar tudo funcionando:

```powershell
python run.py
# Abrir: http://localhost:5000
```

Teste os 14 módulos e valide conforme evidências.

---

**Qualquer dúvida, execute os scripts ou refaça os passos acima.** ✅

