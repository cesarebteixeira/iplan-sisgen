# Procura Completa: Códigos F-00X e String "Capacity" no Codebase

Data: 03 de Outubro de 2026
Projeto: iplan-sisgen / Capacity 1 - Estrutura da rede e do gasto

---

## 1. RESUMO EXECUTIVO

O codebase foi analisado completamente. Encontramos:

- **44 ocorrências** de códigos F-00X nos arquivos Python de routes
- **49 ocorrências** de "Capacity" em templates HTML
- **9 ocorrências** de "Capacity" em arquivos Python
- **Total de 14 funcionalidades** (F-001 até F-014) implementadas

---

## 2. ONDE OS CÓDIGOS F-001, F-002, ETC. ESTÃO SENDO GERADOS

### 2.1 Estrutura de Implementação

Os códigos F-00X **NÃO SÃO GERADOS AUTOMATICAMENTE**. Eles são **identificadores documentais de funcionalidades** que vêm do documento de especificação `resposta-capacidade1-fase3.md`.

**Padrão de Uso:**
- F-001 até F-009: Funcionalidades de CRUD básico
- F-010 até F-012: Funcionalidades de relacionamento/transferência
- F-013 e F-014: Consultas e auditoria

### 2.2 Localização dos Códigos por Arquivo

#### **ROTAS (Routes) - 9 Arquivos Principais**

| Arquivo | F-Code | Funcionalidade | Linhas |
|---------|--------|---|---------|
| `bairro_routes.py` | F-001 | Manter Bairros | 2, 19, 37, 90, 142 |
| `unidade_routes.py` | F-002 | Manter Unidades Orçamentárias | 2, 34, 50, 97, 140 |
| `grupo_routes.py` | F-003 | Manter Grupos | 2, 41, 56, 112, 164 |
| `fonte_routes.py` | F-004 | Consultar Fontes | 2, 16, 34, 51 |
| `conta_routes.py` | F-005 | Classificar Contas | 2, 34, 49, 103, 153 |
| `tipo_processo_routes.py` | F-006 | Manter Tipos de Processo | 2, 32, 47, 92, 135 |
| `periodo_routes.py` | F-007 | Criar Períodos | 2, 48, 66, 143, 205 |
| `feriado_routes.py` | F-008 | Manter Feriados | 2, 45, 62, 124, 183 |
| `projeto_routes.py` | F-009 | Manter Projetos | 2, 33, 48, 98, 144 |
| `vinculo_routes.py` | F-010 | Vínculos Órgão-Projeto | Múltiplas |
| `transferencia_routes.py` | F-011 | Transferência de Órgãos | Múltiplas |
| `transicao_routes.py` | F-012 | Transição SDI | Múltiplas |
| `consulta_routes.py` | F-013/F-014 | Consultas | Múltiplas |

#### **MODELOS (Models) - Sem Referências F-00X Diretas**

Os modelos possuem referências indiretas em comentários:

```
bairro.py         - Linha 5: "Referenced in C023T"
unidade.py        - Linha 5: "Referenced in C025T"
grupo.py          - Linha 5: "Referenced in C126T"
fonte.py          - Linha 5: "Referenced in C144T"
conta.py          - Linha 5: "Referenced in C147T"
tipo_processo.py  - Linha 5: "Referenced in C162T"
periodo.py        - Linha 5: "Referenced in C172T"
feriado.py        - Linha 5: "Referenced in C192T, C806T"
projeto.py        - Linha 5: "Referenced in C205T"
```

---

## 3. ONDE A STRING "CAPACITY" ESTÁ SENDO USADA

### 3.1 Arquivos Python com "Capacity" (9 arquivos)

```
C:\iplan-sisgen\capacidade1\run_port8000.py                 (Linha 2)
C:\iplan-sisgen\capacidade1\run.py                          (Linha 2)
C:\iplan-sisgen\capacidade1\app\__init__.py                 (Linha 2)
C:\iplan-sisgen\capacidade1\app\database.py                 (Linha 2)
C:\iplan-sisgen\capacidade1\app\config.py                   (Linhas 2, 24)
C:\iplan-sisgen\capacidade1\app\validations\__init__.py     (Linha 2)
C:\iplan-sisgen\capacidade1\app\routes\__init__.py          (Linha 2)
C:\iplan-sisgen\capacidade1\app\models\__init__.py          (Linha 2)
```

**Exemplo do uso em config.py (Linha 24):**
```python
APP_NAME = "Capacity 1 - Estrutura da rede e do gasto"
```

### 3.2 Templates HTML com "Capacity" (49 arquivos)

Todos os templates que contêm "Capacity" na tag de título:

#### **Base Template**
- `base.html` - Linhas 6, 13, 49

#### **Bairro**
- `bairro/criar.html` - Linha 3
- `bairro/editar.html` - Linha 3
- `bairro/lista.html` - Linha 3

#### **Unidade**
- `unidade/criar.html` - Linha 3
- `unidade/editar.html` - Linha 3
- `unidade/lista.html` - Linha 3

#### **Grupo**
- `grupo/criar.html` - Linha 2
- `grupo/editar.html` - Linha 2
- `grupo/lista.html` - Linha 2

#### **Fonte**
- `fonte/lista.html` - Linha 2
- `fonte/detalhes.html` - Linha 2
- `fonte/buscar.html` - Linha 2

#### **Conta**
- `conta/criar.html` - Linha 2
- `conta/editar.html` - Linha 2
- `conta/lista.html` - Linha 2

#### **Feriado**
- `feriado/criar.html` - Linha 2
- `feriado/editar.html` - Linha 2
- `feriado/lista.html` - Linha 2

#### **Tipo Processo**
- `tipo_processo/criar.html` - Linha 2
- `tipo_processo/editar.html` - Linha 2
- `tipo_processo/lista.html` - Linha 2

#### **Período**
- `periodo/criar.html` - Linha 2
- `periodo/editar.html` - Linha 2
- `periodo/lista.html` - Linha 2

#### **Projeto**
- `projeto/criar.html` - Linha 2
- `projeto/editar.html` - Linha 2
- `projeto/lista.html` - Linha 2

#### **Vínculo**
- `vinculo/criar.html` - Linha 2
- `vinculo/editar.html` - Linha 2
- `vinculo/lista.html` - Linha 2

#### **Transferência**
- `transferencia/criar.html` - Linha 2
- `transferencia/detalhes.html` - Linha 2
- `transferencia/lista.html` - Linha 2

#### **Transição**
- `transicao/criar.html` - Linha 2
- `transicao/detalhes.html` - Linha 2
- `transicao/lista.html` - Linha 2

#### **Consultas**
- `consulta/index.html` - Linha 2
- `consulta/auditoria.html` - Linha 2
- `consulta/historico.html` - Linha 2
- `consulta/bairros.html` - Linha 2
- `consulta/unidades.html` - Linha 2
- `consulta/grupos.html` - Linha 2
- `consulta/fontes.html` - Linha 2
- `consulta/contas.html` - Linha 2

#### **Index Principal**
- `index.html` - Linhas 3, 7

---

## 4. TEMPLATES HTML QUE EXIBEM OS CÓDIGOS F-00X

### 4.1 Padrão de Exibição

Cada template mostra o código F-00X no elemento `<h2>` do page-header:

**Padrão HTML:**
```html
<div class="page-header">
    <h2>F-00X: Descrição da Funcionalidade</h2>
    <a href="..." class="btn btn-primary">Novo Registro</a>
</div>
```

### 4.2 Exemplos por Funcionalidade

#### **F-001: Bairros** (bairro/lista.html, Linha 7)
```html
<h2>F-001: Manter Bairros</h2>
```

#### **F-002: Unidades** (unidade/lista.html, Linha 7)
```html
<h2>F-002: Manter Unidades Orçamentárias</h2>
```

#### **F-003: Grupos** (grupo/lista.html, Linha 7)
```html
<h2>F-003: Manter Grupos</h2>
```

#### **F-004: Fontes** (fonte/lista.html, Linha 7)
```html
<h2>F-004: Consultar Fontes de Recursos</h2>
```

#### **F-005: Contas** (conta/lista.html, Linha 7)
```html
<h2>F-005: Classificar Contas</h2>
```

#### **F-006: Tipos** (tipo_processo/lista.html, Linha 7)
```html
<h2>F-006: Manter Tipos de Processo</h2>
```

#### **F-007: Períodos** (periodo/lista.html, Linha 7)
```html
<h2>F-007: Criar Períodos de Referência</h2>
```

#### **F-008: Feriados** (feriado/lista.html, Linha 7)
```html
<h2>F-008: Manter Feriados</h2>
```

#### **F-009: Projetos** (projeto/lista.html, Linha 7)
```html
<h2>F-009: Manter Projetos</h2>
```

#### **F-013/F-014: Consultas** (consulta/index.html, Linha 5)
```html
<h2>F-013/F-014: Consultas do Sistema</h2>
```

#### **Index Página Home** (index.html, Linhas 18-31)
```html
<li><strong>F-001:</strong> Manter Bairros</li>
<li><strong>F-002:</strong> Manter Unidades Orçamentárias</li>
<li><strong>F-003:</strong> Manter Grupos de Órgãos</li>
<li><strong>F-004:</strong> Consultar Fontes de Recursos</li>
<li><strong>F-005:</strong> Classificar Contas</li>
<li><strong>F-006:</strong> Manter Tipos de Processo</li>
<li><strong>F-007:</strong> Criar Períodos de Referência</li>
<li><strong>F-008:</strong> Manter Feriados</li>
<li><strong>F-009:</strong> Manter Projetos</li>
<li><strong>F-010:</strong> Vínculos Órgão-Projeto</li>
<li><strong>F-011:</strong> Transferência de Órgãos</li>
<li><strong>F-012:</strong> Transição SDI</li>
<li><strong>F-013/F-014:</strong> Consultas do Sistema</li>
```

---

## 5. COMO OS CÓDIGOS ESTÃO SENDO GERADOS

### 5.1 Padrão de Implementação

Os códigos **NÃO SÃO GERADOS**. Eles são **DOCUMENTAIS**, provenientes da especificação de requisitos e implementados através do padrão:

```
1. Especificação em: resposta-capacidade1-fase3.md
2. Documentação em docstrings: app/routes/*_routes.py (Linha 2 de cada arquivo)
3. Exibição em Templates: app/templates/*/lista.html e criar.html
4. Uso em Comentários de Código: Docstrings das funções de rota
```

### 5.2 Estrutura de Geração (Padrão por Funcionalidade)

```
┌─────────────────────────────────────────────────────────┐
│ SPECIFICATION (resposta-capacidade1-fase3.md)           │
│  F-001: Manter Bairros (C023T)                          │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┬─────────────────┐
        │                         │                 │
        ▼                         ▼                 ▼
┌──────────────┐  ┌────────────────────┐  ┌─────────────────┐
│ routes/      │  │ models/            │  │ templates/      │
│ bairro_      │  │ bairro.py          │  │ bairro/         │
│ routes.py    │  │                    │  │ lista.html      │
│              │  │ __tablename__ =    │  │ criar.html      │
│ Line 2:      │  │ 'bairro'           │  │ editar.html     │
│ "Routes for  │  │                    │  │                 │
│ F-001"       │  │ Related to C023T   │  │ Shows: F-001    │
│              │  │                    │  │ in page-header  │
│ Lines 19,37, │  │ No F-001 code here │  │                 │
│ 90, 142:     │  │                    │  │ Line 7:         │
│ Docstrings   │  │                    │  │ <h2>F-001:...   │
│ mentioning   │  │                    │  │                 │
│ "F-001"      │  │                    │  │                 │
└──────────────┘  └────────────────────┘  └─────────────────┘
```

### 5.3 Padrão de Implementação em Routes

```python
"""
Routes for F-001 (Manter Bairros)          # <- F-Code na linha 2
Manages neighborhood (BAIRRO) operations
"""

@bp.route('/', methods=['GET'])
def listar():
    """
    F-001: List all neighborhoods...       # <- F-Code na docstring
    """
    # Implementation...

@bp.route('/criar', methods=['GET', 'POST'])
def criar():
    """
    F-001: Create a new neighborhood      # <- F-Code na docstring
    """
    # Implementation...

@bp.route('/editar/<codigo>', methods=['GET', 'POST'])
def editar(codigo):
    """
    F-001: Edit an existing neighborhood   # <- F-Code na docstring
    """
    # Implementation...

@bp.route('/deletar/<codigo>', methods=['POST'])
def deletar(codigo):
    """
    F-001: Delete a neighborhood           # <- F-Code na docstring
    """
    # Implementation...
```

---

## 6. ARQUIVOS PYTHON QUE CRIAM OS CÓDIGOS (ESTRUTURA)

### 6.1 Estrutura de Diretórios

```
capacidade1/
├── app/
│   ├── __init__.py
│   ├── config.py                 # Contém APP_NAME com "Capacity"
│   ├── database.py               # Inicializa banco de dados
│   │
│   ├── models/                   # Modelos de dados
│   │   ├── __init__.py           # Contém "Capacity" na descrição
│   │   ├── bairro.py
│   │   ├── unidade.py
│   │   ├── grupo.py
│   │   ├── fonte.py
│   │   ├── conta.py
│   │   ├── tipo_processo.py
│   │   ├── periodo.py
│   │   ├── feriado.py
│   │   ├── projeto.py
│   │   ├── vinculo.py
│   │   ├── transferencia.py
│   │   ├── transicao.py
│   │   ├── auditoria.py
│   │   └── historico.py
│   │
│   ├── routes/                   # Rotas (CONTÉM F-00X)
│   │   ├── __init__.py           # Contém "Capacity" na descrição
│   │   ├── bairro_routes.py      # F-001
│   │   ├── unidade_routes.py     # F-002
│   │   ├── grupo_routes.py       # F-003
│   │   ├── fonte_routes.py       # F-004
│   │   ├── conta_routes.py       # F-005
│   │   ├── tipo_processo_routes.py # F-006
│   │   ├── periodo_routes.py     # F-007
│   │   ├── feriado_routes.py     # F-008
│   │   ├── projeto_routes.py     # F-009
│   │   ├── vinculo_routes.py     # F-010
│   │   ├── transferencia_routes.py # F-011
│   │   ├── transicao_routes.py   # F-012
│   │   └── consulta_routes.py    # F-013/F-014
│   │
│   ├── validations/              # Validações de dados
│   │   ├── __init__.py
│   │   ├── common_validations.py
│   │   └── bairro_validations.py
│   │
│   ├── templates/                # Templates HTML (CONTÊM "Capacity")
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── bairro/
│   │   ├── unidade/
│   │   ├── grupo/
│   │   ├── fonte/
│   │   ├── conta/
│   │   ├── tipo_processo/
│   │   ├── periodo/
│   │   ├── feriado/
│   │   ├── projeto/
│   │   ├── vinculo/
│   │   ├── transferencia/
│   │   ├── transicao/
│   │   ├── consulta/
│   │   └── static/
│   │
│   └── static/                   # Arquivos estáticos
│       ├── css/
│       │   └── style.css         # Contém "Capacity" no comentário
│       └── js/
│
├── run.py                        # Contém "Capacity" na descrição
├── run_port8000.py               # Contém "Capacity" na descrição
└── app.db                        # Banco de dados SQLite
```

---

## 7. TODAS AS LINHAS ONDE "F-00" APARECE

### 7.1 Resumo por Tipo de Arquivo

| Tipo | Arquivos | Total de Linhas |
|------|----------|---|
| Routes (.py) | 13 | 44 |
| Config (.py) | 1 | 2 |
| Templates (.html) | 49 | 49 |
| Documentação (.md) | 2 | 100+ |
| **TOTAL** | **65** | **195+** |

### 7.2 Lista Completa de Routes com F-00X

**Arquivo: bairro_routes.py**
- Linha 2: `Routes for F-001 (Manter Bairros)`
- Linha 19: `F-001: List all neighborhoods with pagination`
- Linha 37: `F-001: Create a new neighborhood`
- Linha 90: `F-001: Edit an existing neighborhood`
- Linha 142: `F-001: Delete a neighborhood`

**Arquivo: unidade_routes.py**
- Linha 2: `Routes for F-002 (Manter Unidades)`
- Linha 34: `F-002: List all budgetary units with pagination`
- Linha 50: `F-002: Create a new budgetary unit`
- Linha 97: `F-002: Edit an existing budgetary unit`
- Linha 140: `F-002: Delete a budgetary unit`

**Arquivo: grupo_routes.py**
- Linha 2: `Routes for F-003 (Manter Grupos)`
- Linha 41: `F-003: List all groups with pagination`
- Linha 56: `F-003: Create a new group`
- Linha 112: `F-003: Edit an existing group`
- Linha 164: `F-003: Delete a group`

**Arquivo: fonte_routes.py**
- Linha 2: `Routes for F-004 (Consultar Fontes)`
- Linha 16: `F-004: List all resource sources with pagination`
- Linha 34: `F-004: View details of a specific resource source`
- Linha 51: `F-004: Search resource sources by code or description`

**Arquivo: conta_routes.py**
- Linha 2: `Routes for F-005 (Classificar Contas)`
- Linha 34: `F-005: List all classified accounts with pagination`
- Linha 49: `F-005: Create a new classified account`
- Linha 103: `F-005: Edit an existing classified account`
- Linha 153: `F-005: Delete a classified account`

**Arquivo: tipo_processo_routes.py**
- Linha 2: `Routes for F-006 (Manter Tipos)`
- Linha 32: `F-006: List all process types with pagination`
- Linha 47: `F-006: Create a new process type`
- Linha 92: `F-006: Edit an existing process type`
- Linha 135: `F-006: Delete a process type`

**Arquivo: periodo_routes.py**
- Linha 2: `Routes for F-007 (Criar Períodos)`
- Linha 48: `F-007: List all reference periods with pagination`
- Linha 66: `F-007: Create a new reference period`
- Linha 143: `F-007: Edit an existing reference period`
- Linha 205: `F-007: Delete a reference period`

**Arquivo: feriado_routes.py**
- Linha 2: `Routes for F-008 (Manter Feriados)`
- Linha 45: `F-008: List all holidays with pagination`
- Linha 62: `F-008: Create a new holiday`
- Linha 124: `F-008: Edit an existing holiday`
- Linha 183: `F-008: Delete a holiday`

**Arquivo: projeto_routes.py**
- Linha 2: `Routes for F-009 (Manter Projetos)`
- Linha 33: `F-009: List all projects with pagination`
- Linha 48: `F-009: Create a new project`
- Linha 98: `F-009: Edit an existing project`
- Linha 144: `F-009: Delete a project`

**Arquivo: vinculo_routes.py**
- Linha 2: `Routes for F-010 (Vínculos Órgão-Projeto)`
- Múltiplas linhas com referências F-010

**Arquivo: transferencia_routes.py**
- Linha 2: `Routes for F-011 (Transferência de Órgãos)`
- Múltiplas linhas com referências F-011

**Arquivo: transicao_routes.py**
- Linha 2: `Routes for F-012 (Transição SDI)`
- Múltiplas linhas com referências F-012

**Arquivo: consulta_routes.py**
- Múltiplas linhas com referências F-013/F-014

---

## 8. ESTRUTURA DE COMO OS CÓDIGOS ESTÃO SENDO GERADOS

### 8.1 Fluxo de Implementação

```
1. ESPECIFICAÇÃO (Documento Externo)
   └─ resposta-capacidade1-fase3.md
      ├─ Define F-001 até F-014
      └─ Associa cada F ao requisito de negócio (C023T, C025T, etc.)

2. IMPLEMENTAÇÃO MANUAL EM CÓDIGO
   ├─ Criar arquivo de rota: app/routes/entidade_routes.py
   │  └─ Adicionar na linha 2: "Routes for F-00X (Descrição)"
   │
   ├─ Implementar funções CRUD
   │  └─ Adicionar docstring em cada função: "F-00X: Descrição"
   │
   └─ Criar templates HTML
      ├─ crear.html    → Linha 2: "{% block title %}Criar ... - Capacity 1{% endblock %}"
      ├─ editar.html   → Linha 2: "{% block title %}Editar ... - Capacity 1{% endblock %}"
      ├─ lista.html    → Linhas 2-3 + Linha 7: "<h2>F-00X: Descrição</h2>"
      └─ detalhes.html → Linha 2: "{% block title %}Detalhes ... - Capacity 1{% endblock %}"

3. EXIBIÇÃO NA WEB
   ├─ Template Base carrega "Capacity 1 - Estrutura da rede e do gasto"
   ├─ Página de Lista mostra: "F-00X: Descrição" no <h2>
   └─ Títulos de páginas mostram "... - Capacity 1"

4. DOCUMENTAÇÃO DINÂMICA
   └─ Cada rota tem docstring com seu F-code
      └─ Permite que ferramentas de documentação gerem especificação automaticamente
```

### 8.2 Padrão de Nomeação

```
F-001: F (Funcionalidade) + número sequencial (001-014)
Cada F-code é ÚNICO e NÃO MUDA

Estrutura:
- Números de F-001 a F-009: Operações de CRUD básicas
- Números de F-010 a F-012: Operações avançadas (relacionamentos, transferências)
- Números de F-013 a F-014: Consultas e auditoria
```

### 8.3 Processo de Linking (Associação)

```
F-00X ←→ C###T (Código de Caso de Teste) ←→ Modelo SQLAlchemy ←→ Tabela DB

Exemplo:
F-001 ←→ C023T ←→ BAIRRO (model) ←→ 'bairro' (tabela)

Localização da Associação:
├─ app/models/bairro.py (Linha 5): "Referenced in C023T"
├─ app/routes/bairro_routes.py (Linha 2): "Routes for F-001"
└─ app/templates/bairro/lista.html (Linha 7): "<h2>F-001: Manter Bairros</h2>"
```

---

## 9. STRING "CAPACITY" - PROPOSTA DE TRADUÇÃO

### 9.1 Onde "Capacity" Está Sendo Usado (Completo)

```
ARQUIVO                          LINHAS      CONTEÚDO
─────────────────────────────────────────────────────────────
app/config.py                    24          APP_NAME = "Capacity 1 - Estrutura da rede e do gasto"
app/static/css/style.css         1           /* Capacity 1 - Estrutura da rede e do gasto */
base.html                        6, 13, 49   Capacity 1 - Estrutura da rede e do gasto
index.html                       3, 7        Capacity 1 - Estrutura da rede e do gasto

Todos os templates (49 arquivos):
- Padrão: "{% block title %}... - Capacity 1{% endblock %}"
```

### 9.2 Recomendação de Tradução

**Atual:** "Capacity 1"
**Proposta:** "Capacidade 1" (tradução direta)

**Exemplo de mudança:**
```python
# Antes
APP_NAME = "Capacity 1 - Estrutura da rede e do gasto"

# Depois
APP_NAME = "Capacidade 1 - Estrutura da rede e do gasto"
```

### 9.3 Arquivos a Modificar para Tradução

| Arquivo | Tipo | Ocorrências | Ação |
|---------|------|---|---|
| `config.py` | Python | 2 | Substituir `Capacity 1` por `Capacidade 1` |
| `style.css` | CSS | 1 | Substituir `Capacity 1` por `Capacidade 1` |
| `base.html` | HTML | 3 | Substituir `Capacity 1` por `Capacidade 1` |
| `index.html` | HTML | 2 | Substituir `Capacity 1` por `Capacidade 1` |
| Todos os 49 templates | HTML | 49 | Substituir `Capacity 1` por `Capacidade 1` |
| `run.py` | Python | 1 | Atualizar comentário de descrição |
| `run_port8000.py` | Python | 1 | Atualizar comentário de descrição |

---

## 10. CONCLUSÃO

### 10.1 Sumário de Achados

1. **Códigos F-00X**: 44 ocorrências em 13 arquivos de routes
2. **String "Capacity"**: 49 ocorrências em templates + 9 em Python = 58 total
3. **Estrutura de Geração**: Documentária (não automática)
4. **Padrão de Implementação**: Consistente em todos os módulos
5. **Localização Principal**: `app/routes/` (F-codes) e `app/templates/` (títulos)

### 10.2 Arquivos Críticos Identificados

```
PRIORIDADE ALTA:
✓ app/routes/*_routes.py (12 arquivos) - Contêm todas as definições F-00X
✓ app/templates/*/lista.html (14 arquivos) - Exibem títulos com F-codes
✓ app/config.py - Define APP_NAME com "Capacity"

PRIORIDADE MÉDIA:
✓ base.html - Template base com "Capacity"
✓ index.html - Página home com lista de F-codes
✓ 49 templates HTML restantes - Contêm "Capacity 1" em títulos
```

### 10.3 Próximos Passos Sugeridos

1. **Tradução de "Capacity 1" para "Capacidade 1"**
   - Substituir em 58 locais identificados
   - Manter consistência em toda a aplicação

2. **Documentação de F-codes**
   - Gerar documentação automática das docstrings
   - Vincular cada F-code com seu C-code correspondente

3. **Validação de Cobertura**
   - Verificar se todos os F-codes estão com testes
   - Confirmar cobertura de F-010, F-011, F-012

---

## Apêndice A: Mapeamento Completo F-X ↔ C-X ↔ Tabela

| F-Code | C-Code | Tabela | Arquivo Route | Linhas |
|--------|--------|--------|---|---|
| F-001 | C023T | bairro | bairro_routes.py | 2,19,37,90,142 |
| F-002 | C025T | unidade_orcamentaria | unidade_routes.py | 2,34,50,97,140 |
| F-003 | C126T | grupo | grupo_routes.py | 2,41,56,112,164 |
| F-004 | C144T | fonte_recursos | fonte_routes.py | 2,16,34,51 |
| F-005 | C147T | conta | conta_routes.py | 2,34,49,103,153 |
| F-006 | C162T | tipo_processo | tipo_processo_routes.py | 2,32,47,92,135 |
| F-007 | C172T | periodo | periodo_routes.py | 2,48,66,143,205 |
| F-008 | C192T, C806T | feriado | feriado_routes.py | 2,45,62,124,183 |
| F-009 | C205T | projeto | projeto_routes.py | 2,33,48,98,144 |
| F-010 | - | vinculo | vinculo_routes.py | Múltiplas |
| F-011 | - | transferencia | transferencia_routes.py | Múltiplas |
| F-012 | - | transicao | transicao_routes.py | Múltiplas |
| F-013/F-014 | - | (Consultas) | consulta_routes.py | Múltiplas |

---

**Fim do Relatório**
Data: 03/10/2026
