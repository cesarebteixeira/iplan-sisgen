# Quick Start Guide - Capacity 1

## Installation (5 minutes)

### Step 1: Open PowerShell
Open Windows PowerShell 5.1 or higher.

### Step 2: Install Dependencies
```powershell
cd C:\iplan-sisgen\capacidade1
pip install -r requirements.txt
```

### Step 3: Run the Application
```powershell
python run.py
```

You should see:
```
Starting Capacity 1 - Estrutura da rede e do gasto
Version: 1.0.0
Access the application at http://localhost:5000
```

### Step 4: Open in Web Browser
Navigate to: **http://localhost:5000**

You should see the home page with all 14 functional modules.

---

## First Steps After Installation

### 1. Create a Neighborhood (Bairro)
1. Click **"Bairros"** in the navigation
2. Click **"Novo Bairro"**
3. Enter:
   - Código: `001`
   - Descrição: `Centro`
4. Click **"Criar"**

### 2. Create a Budgetary Unit (Unidade)
1. Click **"Unidades"** in navigation
2. Click **"Nova Unidade"**
3. Enter:
   - Código: `1001`
   - Descrição: `Secretaria de Educação`
4. Click **"Criar"**

### 3. Create a Group (Grupo)
1. Click **"Grupos"**
2. Click **"Novo Grupo"**
3. Select a unit you created
4. Enter group details
5. Click **"Criar"**

---

## Key Features to Explore

### Audit Trail
- Go to **"Consultas"** → **"Consultar Auditoria"**
- View all CREATE, UPDATE, DELETE operations
- See who made changes and when

### Historical Records
- Go to **"Consultas"** → **"Consultar Histórico"**
- Track organizational changes
- View transfer and transition records

### Data Management
- **F-001**: Neighborhoods
- **F-002**: Budgetary Units
- **F-003**: Organizational Groups
- **F-005**: Classified Accounts
- **F-006**: Process Types
- **F-007**: Reference Periods
- **F-008**: Holidays
- **F-009**: Projects
- **F-010**: Organization-Project Links

### Transfers & Transitions
- **F-011**: Record organization transfers
- **F-012**: Record SDI transitions

---

## Troubleshooting

### Issue: "pip is not recognized"
**Solution**: Make sure Python 3.11+ is installed and added to PATH
```powershell
python --version
```

### Issue: "Port 5000 is already in use"
**Solution**: Change the port in run.py or kill the process:
```powershell
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

### Issue: "ModuleNotFoundError"
**Solution**: Make sure requirements are installed:
```powershell
pip install -r requirements.txt
```

### Issue: Database errors
**Solution**: Delete app.db and restart (data will be recreated):
```powershell
Remove-Item app.db
python run.py
```

---

## API Usage

### List All Bairros
```
GET http://localhost:5000/bairro/
```

### Get Single Bairro
```
GET http://localhost:5000/bairro/api/001
```
Response:
```json
{
  "codigo_bairro": "001",
  "descricao": "Centro",
  "data_criacao": "2024-10-03T12:00:00"
}
```

### Query Audit Trail
```
GET http://localhost:5000/consulta/api/auditoria?tabela=bairro&operacao=CREATE&limit=10
```

### Get System Statistics
```
GET http://localhost:5000/consulta/api/resumo
```

---

## Common Operations

### Search/Filter
- Most list pages have search boxes
- Use filters to find specific records
- Pagination is 15 items per page

### Edit Records
- Click **"Editar"** button on any list
- Modify the fields
- Click **"Atualizar"** to save

### Delete Records
- Click **"Deletar"** button
- Confirm the deletion
- Record is logged in audit trail

### View History
- Go to **"Transferências"** or **"Transições"**
- View organizational change records

---

## User Interface Tips

### Navigation
- Main menu is at the top (dark blue bar)
- Click any module name to access it
- Use **"Voltar"** or **"Cancelar"** to go back

### Forms
- Red error messages indicate validation errors
- Green success messages confirm operations
- All required fields are marked

### Tables
- Hover over rows for highlighting
- Pagination controls are at the bottom
- Click column headers for sorting (not implemented yet)

---

## Database

### Location
```
C:\iplan-sisgen\capacidade1\app.db
```

### Tables
- bairro
- unidade_orcamentaria
- grupo
- fonte_recursos
- conta_classificada
- tipo_processo
- periodo_referencia
- feriado_orgao
- projeto
- vinculo_orgao_projeto
- historico_periodo_orgao
- auditoria

### Accessing via SQLite
```powershell
sqlite3 app.db
.tables
SELECT * FROM bairro;
.exit
```

---

## Configuration

### Modify Settings
Edit `app/config.py` to change:

```python
# Database location
SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"

# Items per page
ITEMS_PER_PAGE = 15

# Flask debug mode
DEBUG = True

# Secret key for sessions
SECRET_KEY = "dev-secret-key-change-in-production"
```

### After Changes
Restart the application:
```powershell
# Press Ctrl+C to stop
# Then run again
python run.py
```

---

## Help & Support

### Documentation Files
- **README.md** - Complete documentation
- **COMPLETION_SUMMARY.md** - Technical implementation details
- **QUICK_START.md** - This file

### Code Comments
- All source code has docstring comments
- Business rules are referenced with RN numbers
- Validation rules link to C023T document

### Contact
For issues or questions, refer to the implementation documentation in the Python files.

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+C | Stop the application |
| Ctrl+Shift+Delete | Clear browser history |
| F5 | Refresh page |
| Ctrl+F | Search on page |

---

## Next Steps

1. ✅ Application is running
2. ✅ Database is initialized
3. ✅ Create sample data
4. ✅ Explore all modules
5. ✅ Test CRUD operations
6. ✅ Review audit trail
7. ✅ Check historical records
8. ✅ Ready for production

---

## Performance Tips

### For Better Performance
- Use pagination (15 items/page)
- Filter before searching large datasets
- Close unused browser tabs
- Restart if application becomes sluggish

### Database Maintenance
- SQLite is suitable for development
- For production, upgrade to PostgreSQL
- Regular backups of app.db file

---

**Capacity 1 is ready to use!**

Need more help? Check the README.md or COMPLETION_SUMMARY.md files.

Happy using! 🚀
