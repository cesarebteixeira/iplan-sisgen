# Referência Rápida - Códigos F-00X e String "Capacity"

## Resumo em 30 segundos

**O Que Procurava?**
- Códigos F-001 até F-014: Identificadores documentais de funcionalidades
- String "Capacity": Nome da aplicação em 58 locais

**Onde Estão?**
- **F-00X**: Em 13 arquivos `app/routes/*_routes.py` (44 ocorrências)
- **"Capacity"**: Em 9 arquivos Python + 49 templates HTML (58 ocorrências total)

**O Que É?**
- Não é código gerado automaticamente
- São documentação incorporada no código-fonte
- Especificação vem de `resposta-capacidade1-fase3.md`

---

## Mapeamento Funcionalidades

| F-Code | Arquivo | Funcionalidade | Linhas | Status |
|--------|---------|---|---|---|
| F-001 | `bairro_routes.py` | Manter Bairros | 2,19,37,90,142 | ✅ |
| F-002 | `unidade_routes.py` | Manter Unidades | 2,34,50,97,140 | ✅ |
| F-003 | `grupo_routes.py` | Manter Grupos | 2,41,56,112,164 | ✅ |
| F-004 | `fonte_routes.py` | Consultar Fontes | 2,16,34,51 | ✅ |
| F-005 | `conta_routes.py` | Classificar Contas | 2,34,49,103,153 | ✅ |
| F-006 | `tipo_processo_routes.py` | Manter Tipos | 2,32,47,92,135 | ✅ |
| F-007 | `periodo_routes.py` | Criar Períodos | 2,48,66,143,205 | ✅ |
| F-008 | `feriado_routes.py` | Manter Feriados | 2,45,62,124,183 | ✅ |
| F-009 | `projeto_routes.py` | Manter Projetos | 2,33,48,98,144 | ✅ |
| F-010 | `vinculo_routes.py` | Vínculos | Múltiplas | ✅ |
| F-011 | `transferencia_routes.py` | Transferências | Múltiplas | ✅ |
| F-012 | `transicao_routes.py` | Transições | Múltiplas | ✅ |
| F-013/14 | `consulta_routes.py` | Consultas | Múltiplas | ✅ |

---

## Localização de "Capacity" por Tipo

### Python (9 arquivos)

```
✓ app/config.py (Linha 24)
✓ app/__init__.py (Linha 2)
✓ app/database.py (Linha 2)
✓ app/models/__init__.py (Linha 2)
✓ app/routes/__init__.py (Linha 2)
✓ app/validations/__init__.py (Linha 2)
✓ run.py (Linha 2)
✓ run_port8000.py (Linha 2)
✓ app/static/css/style.css (Linha 1)
```

### HTML Templates (49 arquivos)

```
✓ base.html (3 ocorrências)
✓ index.html (2 ocorrências)
✓ Todos os */lista.html (14 arquivos, 1 ocorrência cada)
✓ Todos os */criar.html (14 arquivos, 1 ocorrência cada)
✓ Todos os */editar.html (10 arquivos, 1 ocorrência cada)
✓ Todos os */detalhes.html (3 arquivos, 1 ocorrência cada)
✓ */buscar.html (1 arquivo, 1 ocorrência)
✓ consulta/* (8 arquivos, 1 ocorrência cada)
```

---

## Estrutura de Implementação

### Como o F-Code Aparece em Uma Rota

```python
"""
Routes for F-001 (Manter Bairros)    # ← F-001 AQUI
Manages neighborhood operations
"""

@bp.route('/', methods=['GET'])
def listar():
    """
    F-001: List all neighborhoods     # ← F-001 AQUI
    """
    # implementação...

@bp.route('/criar', methods=['GET', 'POST'])
def criar():
    """
    F-001: Create a new neighborhood  # ← F-001 AQUI
    """
    # implementação...
```

### Como Aparece em Um Template

```html
{% block title %}Bairros - Capacity 1{% endblock %}
                              ^^^^^^^^^^
                         Aparece aqui

<h2>F-001: Manter Bairros</h2>
    ^^^^^
  F-Code aqui
```

---

## Padrão de Busca

### Para Encontrar F-00X

**PowerShell:**
```powershell
Get-ChildItem -Path "C:\iplan-sisgen\capacidade1\app\routes\*.py" | 
  ForEach-Object { Select-String -Path $_.FullName -Pattern "F-00[0-9]" }
```

**Resultado:** 44 ocorrências em 13 arquivos

### Para Encontrar "Capacity"

**PowerShell:**
```powershell
Get-ChildItem -Path "C:\iplan-sisgen\capacidade1" -Include "*.py","*.html" -Recurse |
  ForEach-Object { Select-String -Path $_.FullName -Pattern "Capacity" } |
  Measure-Object | Select-Object Count
```

**Resultado:** 58 ocorrências

---

## Tradução: "Capacity" → "Capacidade"

### Arquivos a Modificar (59 locais)

1. **config.py** (2 locais)
   - Linha 24: `APP_NAME = "Capacity 1 - ..."`

2. **style.css** (1 local)
   - Linha 1: comentário de cabeçalho

3. **base.html** (3 locais)
   - Título, h1, footer

4. **index.html** (2 locais)
   - Título e h2

5. **49 templates HTML** (49 locais)
   - Cada um: `{% block title %}... - Capacity 1{% endblock %}`

6. **Comentários Python** (2 locais)
   - run.py, run_port8000.py

### Script de Tradução

```powershell
# Visualizar mudanças (sem fazer)
.\SCRIPT_TRADUZIR_CAPACITY_PARA_CAPACIDADE.ps1

# Executar mudanças
.\SCRIPT_TRADUZIR_CAPACITY_PARA_CAPACIDADE.ps1 -DryRun $false
```

---

## Arquivos Críticos

### Prioridade Alta (Definem F-00X)

```
✓ app/routes/bairro_routes.py (F-001)
✓ app/routes/unidade_routes.py (F-002)
✓ app/routes/grupo_routes.py (F-003)
✓ app/routes/fonte_routes.py (F-004)
✓ app/routes/conta_routes.py (F-005)
✓ app/routes/tipo_processo_routes.py (F-006)
✓ app/routes/periodo_routes.py (F-007)
✓ app/routes/feriado_routes.py (F-008)
✓ app/routes/projeto_routes.py (F-009)
✓ app/routes/vinculo_routes.py (F-010)
✓ app/routes/transferencia_routes.py (F-011)
✓ app/routes/transicao_routes.py (F-012)
✓ app/routes/consulta_routes.py (F-013/14)
```

### Prioridade Média (Exibem F-00X e "Capacity")

```
✓ app/templates/*/lista.html (todos exibem F-codes e "Capacity")
✓ app/templates/base.html (template base com "Capacity")
✓ app/templates/index.html (lista completa de F-codes)
```

### Prioridade Baixa (Apenas Referências)

```
✓ app/config.py (define APP_NAME com "Capacity")
✓ Modelos em app/models/ (referência a C-codes)
✓ Documentação em .md files
```

---

## Estatísticas

| Métrica | Valor |
|---------|-------|
| Arquivos routes com F-00X | 13 |
| Ocorrências de F-00X | 44 |
| Arquivos Python com "Capacity" | 9 |
| Arquivos HTML com "Capacity" | 49 |
| Total ocorrências "Capacity" | 58 |
| Funcionalidades implementadas | 14 |
| Total arquivos afetados | 71 |
| Linhas a traduzir | 59 |

---

## Checklist de Ações

- [ ] Revisar arquivo completo: `PROCURA_CODIGOS_F-00X_CAPACITY.md`
- [ ] Revisar resumo executivo: `RESUMO_EXECUTIVO_F-00X.txt`
- [ ] Revisar linhas exatas: `LINHAS_EXATAS_F-00X_CAPACITY.txt`
- [ ] Testar script de tradução em dry-run: `SCRIPT_TRADUZIR_CAPACITY_PARA_CAPACIDADE.ps1`
- [ ] Executar tradução (se aprovado)
- [ ] Verificar se todas as 59 ocorrências foram traduzidas
- [ ] Atualizar documentação
- [ ] Fazer commit no git (se aplicável)

---

## Contatos e Suporte

- **Arquivos de referência**: `C:\iplan-sisgen\` (este diretório)
- **Codebase**: `C:\iplan-sisgen\capacidade1\app\`
- **Documentação externa**: `resposta-capacidade1-fase3.md`

---

**Última atualização:** 03/10/2026  
**Gerado por:** Script de análise de codebase  
**Status:** Pronto para ação
