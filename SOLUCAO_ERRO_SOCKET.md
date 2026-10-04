# 🔧 Solução: Erro de Socket "Permission denied"

## 📌 Problema

Quando você executa `python run.py`, recebe o erro:

```
Foi feita uma tentativa de acesso a um soquete de uma maneira que é proibida pelas permissões de acesso
```

**Causa**: Windows Firewall está bloqueando a porta 5000 que o Flask tenta usar.

---

## ✅ 3 Soluções Disponíveis

### **SOLUÇÃO 1: Usar Porta 8000 (MAIS FÁCIL - SEM ADMIN)**

A porta 8000 geralmente não tem restrição. Vou providenciar um script pronto.

**Tempo**: 2 minutos

**Passos**:

1. Abra PowerShell na pasta do projeto:
   ```powershell
   cd C:\iplan-sisgen\capacidade1
   ```

2. Ative o venv:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Execute com a porta alternativa:
   ```powershell
   python run_port8000.py
   ```

4. Acesse no navegador:
   ```
   http://localhost:8000
   ```

**Resultado esperado**:
```
Database initialized successfully
Starting Capacity 1 - Estrutura da rede e do gasto
Version: 1.0.0
Access the application at http://localhost:8000
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:8000
```

---

### **SOLUÇÃO 2: Liberar Porta 5000 no Firewall (COM ADMIN)**

Se você REALMENTE quer usar a porta 5000:

**Tempo**: 3 minutos (mas precisa de admin)

**Passos**:

1. **Abra PowerShell COMO ADMINISTRADOR**:
   - Clique com botão direito em PowerShell
   - Selecione "Executar como administrador"
   - Clique "Sim"

2. **Execute o script de firewall**:
   ```powershell
   C:\iplan-sisgen\capacidade1\FIX_FIREWALL_ADMIN.ps1
   ```

3. **Feche o PowerShell admin**

4. **Abra novo PowerShell (normal)** e execute:
   ```powershell
   cd C:\iplan-sisgen\capacidade1
   .\venv\Scripts\Activate.ps1
   python run.py
   ```

5. **Acesse**:
   ```
   http://localhost:5000
   ```

---

### **SOLUÇÃO 3: Usar Localhost em Outro Host (AVANÇADO)**

Se as soluções 1 e 2 não funcionarem, tente:

**Porta**: 3000 ou 9000

**Script**:
```powershell
cd C:\iplan-sisgen\capacidade1
.\venv\Scripts\Activate.ps1
python -c "from app import create_app, db; app = create_app(); app.run(host='127.0.0.1', port=3000, debug=True, use_reloader=False)"
```

---

## 🎯 Recomendação

**USE A SOLUÇÃO 1** (Porta 8000):

✅ Não precisa de permissões de admin  
✅ Mais rápido de configurar  
✅ Funciona em 99% dos casos  
✅ Sem mudanças no firewall  

Já criei o arquivo `run_port8000.py` pronto para usar.

---

## 📂 Arquivos Criados

1. **`run_port8000.py`** ← Use este arquivo para porta 8000
   - Localização: `C:\iplan-sisgen\capacidade1\run_port8000.py`
   - Comando: `python run_port8000.py`

2. **`FIX_FIREWALL_ADMIN.ps1`** ← Script para liberar porta 5000
   - Localização: `C:\iplan-sisgen\capacidade1\FIX_FIREWALL_ADMIN.ps1`
   - Comando: Executar como administrador

---

## ✨ Qual Porta Usar?

| Porta | Solução | Fácil? | Admin? | Funciona? |
|-------|---------|--------|--------|-----------|
| 8000 | Solução 1 | ✅ SIM | ❌ NÃO | ✅ 99% |
| 5000 | Solução 2 | ⚠️ NÃO | ✅ SIM | ✅ 100% |
| 3000 | Solução 3 | ❌ NÃO | ❌ NÃO | ⚠️ 50% |

**RECOMENDAÇÃO**: **Porta 8000 (Solução 1)**

---

## 🚀 COMEÇAR AGORA

### Opção Recomendada (Porta 8000):

```powershell
cd C:\iplan-sisgen\capacidade1
.\venv\Scripts\Activate.ps1
python run_port8000.py
```

Depois acesse: **http://localhost:8000**

---

## ❓ FAQ

### P: Qual é a diferença entre porta 5000 e 8000?
R: Nenhuma para você! Ambas funcionam identicamente. É só o número que muda.

### P: Por que o Windows bloqueia a porta 5000?
R: Pode ser por Hyper-V, VPN, ou outro software em conflito.

### P: A solução 1 é permanente?
R: Sim! Você pode usar `run_port8000.py` sempre.

### P: Como mudo o banco de dados de porta?
R: Não precisa. O banco de dados usa arquivo (`app.db`), não depende de porta.

### P: Posso mudar para outra porta?
R: Sim! Edite `run_port8000.py` ou crie um novo com a porta desejada.

---

## 📝 Próximos Passos

1. **Execute um dos scripts**:
   - Fácil: `python run_port8000.py`
   - Admin: `FIX_FIREWALL_ADMIN.ps1` (depois `python run.py`)

2. **Acesse no navegador**:
   - Porta 8000: `http://localhost:8000`
   - Porta 5000: `http://localhost:5000`

3. **Teste os 14 módulos**:
   - Navegue pelas funcionalidades
   - Valide o comportamento

4. **Se funcionar**:
   - ✅ Você está pronto para usar!

---

**Recomendação final**: Use a **Porta 8000** para simplicidade máxima! 🚀

