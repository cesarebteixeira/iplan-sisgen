# 🎯 PLANO EXECUTÁVEL — Correção de Python 3.13 → 3.12

## Status Atual

| Elemento | Situação |
|----------|----------|
| Python no sistema | 3.13.7 (ATIVO) |
| Python 3.12 | NÃO INSTALADO |
| venv | Criado com Python 3.13 (PRECISA RECRIAR) |
| SQLAlchemy 2.0.23 | Incompatível com 3.13 |
| Aplicação | NÃO FUNCIONA |

---

## 📋 PLANO DE AÇÃO (4 passos)

### ⏱️ Tempo Total: ~30-40 minutos

Distribuição:
- Desinstalar Python 3.13: **5 min**
- Instalar Python 3.12: **10-15 min**
- Recrear venv e dependências: **10-15 min**
- Testar: **5 min**

---

## PASSO 1: DESINSTALAR PYTHON 3.13 (5 minutos)

### Método 1: Via Settings (RECOMENDADO)

**AÇÃO**:
1. Abra **Settings** (Configurações)
2. Vá para: **Apps > Apps & features**
3. Na barra de pesquisa, procure: **"Python 3.13"**
4. Clique no resultado: **Python 3.13.7** (64-bit)
5. Clique em: **Uninstall**
6. **IMPORTANTE**: Na janela que aparecer, MARQUE: ☑️ **"Remove Python 3.13 from PATH"**
7. Clique: **Uninstall** (novamente)
8. Aguarde a desinstalação completar (1-2 minutos)
9. Clique: **Close**

**VERIFICAÇÃO**:
- Windows pode pedir reinicialização
- Se pedir, **REINICIE o computador** agora

### Método 2: Via PowerShell (Se Settings não funcionar)

Abra PowerShell **COMO ADMINISTRADOR** e execute:

```powershell
Get-WmiObject Win32_Product | Where-Object Name -like "*Python 3.13*" | ForEach-Object { $_.Uninstall() }
```

Aguarde completar.

---

## PASSO 2: INSTALAR PYTHON 3.12 (10-15 minutos)

### AÇÃO:

1. **Abra navegador** e vá para:
   ```
   https://www.python.org/downloads/release/python-3120/
   ```

2. **Procure o botão de download** na página:
   - Scroll para baixo um pouco
   - Procure: **"Windows installer (64-bit)"**
   - Clique em: **python-3.12.0-amd64.exe**
   - (Ou versão 3.12.x mais recente que aparecer)

3. **Aguarde download** completar (arquivo ~100 MB)

4. **Execute o instalador** (double-click no arquivo baixado)

5. **Na primeira janela do instalador**:
   - ☑️ Marque: **"Install launcher for all users"**
   - ☑️ Marque: **"Add Python 3.12 to PATH"** ← **CRÍTICO!**
   - Clique: **"Install Now"**

6. **Deixe instalar** (vai levar 3-5 minutos)

7. **Quando aparecer a tela final**:
   - Verá opção: "Disable path length limit" (opcional)
   - Clique: **"Close"**

### VERIFICAÇÃO:

Abra **PowerShell** (novo) e execute:

```powershell
python --version
```

**DEVE MOSTRAR**: `Python 3.12.0` (ou 3.12.x)

Se mostrar 3.12.x, ✅ está correto!

---

## PASSO 3: RECREAR VENV E INSTALAR DEPENDÊNCIAS (10-15 minutos)

### AÇÃO:

Abra **PowerShell** e execute os comandos abaixo **NA SEQUÊNCIA**:

#### 3.1 Navegar para o projeto

```powershell
cd C:\iplan-sisgen\capacidade1
```

#### 3.2 Verificar localização atual

```powershell
Get-Location
```

**Esperado**: `C:\iplan-sisgen\capacidade1`

#### 3.3 Remover venv antigo (criado com Python 3.13)

```powershell
Remove-Item -Recurse -Force venv
```

**Esperado**: Sem mensagem de erro (pode levar alguns segundos)

#### 3.4 Verificar que foi deletado

```powershell
Test-Path venv
```

**Esperado**: `False` (significa que foi deletado)

#### 3.5 Criar novo venv com Python 3.12

```powershell
python -m venv venv
```

**Esperado**: Sem mensagem de erro (vai levar 30 segundos)

#### 3.6 Ativar o novo venv

```powershell
.\venv\Scripts\Activate.ps1
```

**Esperado**: Prompt muda para: `(venv) PS C:\iplan-sisgen\capacidade1>`

#### 3.7 Atualizar pip (gerenciador de pacotes)

```powershell
python -m pip install --upgrade pip
```

**Esperado**: "Successfully installed pip X.X.X"

#### 3.8 Instalar dependências

```powershell
pip install -r requirements.txt
```

**Esperado**: 
```
Successfully installed Flask-3.0.0 Flask-SQLAlchemy-3.1.1 SQLAlchemy-2.0.23 ...
```

(Vai levar 2-3 minutos)

#### 3.9 Verificar instalação

```powershell
pip list
```

**Esperado**: Ver listado:
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- SQLAlchemy 2.0.23

---

## PASSO 4: TESTAR APLICAÇÃO (5 minutos)

### AÇÃO:

#### 4.1 Verificar Python no venv

```powershell
python --version
```

**Esperado**: `Python 3.12.x`

#### 4.2 Iniciar a aplicação

```powershell
python run.py
```

**Esperado**:
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://localhost:5000
* Press CTRL+C to quit
```

#### 4.3 Abrir navegador

Abra seu navegador e vá para:
```
http://localhost:5000
```

**Esperado**: 
- Página carrega
- Vê menu com 14 funcionalidades
- Nenhum erro no console

#### 4.4 Parar a aplicação

No PowerShell onde `python run.py` está rodando:
```
CTRL+C
```

---

## ✅ CHECKLIST DE PROGRESSO

Marque conforme você completa cada item:

### Passo 1: Desinstalar Python 3.13
- [ ] Abri Settings > Apps & features
- [ ] Procurei "Python 3.13"
- [ ] Desinstalei com "Remove from PATH"
- [ ] Reiniciei computador (se solicitado)

### Passo 2: Instalar Python 3.12
- [ ] Baixei python-3.12.0-amd64.exe
- [ ] Executei o instalador
- [ ] Marquei "Add Python 3.12 to PATH"
- [ ] Instalação completou sem erros
- [ ] Verifiquei: `python --version` mostra 3.12.x

### Passo 3: Recrear venv
- [ ] Naveguei para C:\iplan-sisgen\capacidade1
- [ ] Deletei venv antigo
- [ ] Criei novo venv com `python -m venv venv`
- [ ] Ativei venv (prompt mudou para (venv))
- [ ] Atualizei pip
- [ ] Instalei dependências com `pip install -r requirements.txt`
- [ ] Verifiquei com `pip list` (Flask, SQLAlchemy, etc presentes)

### Passo 4: Testar
- [ ] Executei `python run.py`
- [ ] Aplicação iniciou em http://localhost:5000
- [ ] Navegador carregou página com 14 funcionalidades
- [ ] Nenhum erro foi mostrado

---

## 🚨 POSSÍVEIS PROBLEMAS E SOLUÇÕES

### Problema: "python is not recognized"

**Causa**: Python 3.12 não está no PATH

**Solução**:
1. Desinstale Python 3.12
2. Reinstale, **MARCANDO** "Add Python 3.12 to PATH"
3. Reinicie PowerShell
4. Tente novamente

### Problema: "Permission denied" ao remover venv

**Causa**: Alguns arquivos ainda estão em uso

**Solução**:
```powershell
# Feche todas as instâncias de PowerShell
# Abra uma nova como Administrador
Remove-Item -Recurse -Force C:\iplan-sisgen\capacidade1\venv
```

### Problema: "Module not found" ao instalar dependências

**Causa**: pip não foi atualizado

**Solução**:
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Problema: Aplicação ainda mostra erro de SQLAlchemy

**Causa**: venv não foi recriado corretamente

**Solução**:
```powershell
# Parar a aplicação (CTRL+C)
deactivate  # Desativar venv
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

### Problema: "Access denied" ao desinstalar Python 3.13

**Causa**: Precisa de permissão de administrador

**Solução**:
1. Abra PowerShell como **Administrador**
2. Execute novamente:
   ```powershell
   Get-WmiObject Win32_Product | Where-Object Name -like "*Python 3.13*" | ForEach-Object { $_.Uninstall() }
   ```

---

## 📞 SUPORTE

Se algo não funcionar:

1. **Leia a seção "Possíveis Problemas"** acima
2. **Verifique o arquivo**: `C:\iplan-sisgen\capacidade1\CORRIGIR_PYTHON.md`
3. **Consulte**: `FIX_PYTHON_RAPIDO.txt` para versão simplificada

---

## ⏭️ DEPOIS DE TUDO FUNCIONAR

Quando `http://localhost:5000` carregar com sucesso:

1. Teste os 14 módulos da aplicação
2. Valide comportamento conforme evidências originais
3. Se tudo OK: **"CAPACIDADE APROVADA"**

---

**Tempo estimado: 30-40 minutos**

**Comece pelo Passo 1 agora!** ✅

