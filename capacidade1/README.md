# Capacidade 1 — Estrutura da Rede e do Gasto

**Sistema Web de Gestão de Infraestrutura Escolar**

Uma aplicação web construída a partir da reconstrução de um sistema legado EAE/COBOL Unisys para a Secretaria de Educação.

---

## 📋 Visão Geral

Este sistema implementa a **Capacidade 1** de um projeto maior de modernização de infraestrutura escolar, focando na estrutura organizacional e financeira da rede.

### O que a Capacidade 1 faz

Mantém e consulta os dados fundamentais da rede escolar:

- **Bairros** — Localização geográfica das unidades
- **Unidades Orçamentárias** — Estrutura de alocação de recursos financeiros
- **Grupos/Coordenações** — Agrupamento administrativo de órgãos
- **Fontes de Recursos** — Classificação de recursos financeiros (por órgão)
- **Contas Classificadas** — Mapeamento de contas por fonte de recurso
- **Tipos de Processo** — Classificação de processos administrativos
- **Períodos de Referência** — Períodos mensais para planejamento
- **Feriados** — Calendário de feriados por unidade
- **Projetos** — Agrupamento de atividades por secretaria
- **Vínculos Órgão-Projeto** — Associação de órgãos a projetos
- **Transferências de Órgãos** — Histórico de mudanças de coordenação
- **Transições de Órgão SDI** — Promoção de órgão provisório para definitivo

---

## 🚀 Quick Start (5 minutos)

### Pré-requisitos

- **Windows 11**
- **Python 3.11** ou superior
- **pip** (gerenciador de pacotes Python)

### Instalação e Execução

**1. Abra o PowerShell (como administrador recomendado)**

```powershell
# Ou use: Start-Process pwsh -Verb RunAs
powershell
```

**2. Navegue para o projeto**

```powershell
cd C:\iplan-sisgen\capacidade1
```

**3. (Opcional) Crie um ambiente virtual**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**4. Instale as dependências**

```powershell
pip install -r requirements.txt
```

**5. Execute a aplicação**

```powershell
python run.py
```

**Esperado:**
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://localhost:5000
* Press CTRL+C to quit
```

**6. Abra seu navegador**

```
http://localhost:5000
```

Você verá a página inicial com as 14 funcionalidades disponíveis.

---

## 📖 Guia de Uso

### Home Page

Ao abrir `http://localhost:5000`, você verá um menu com 14 módulos:

1. **Bairros** — Cadastro de bairros
2. **Unidades Orçamentárias** — Gestão de unidades financeiras
3. **Grupos** — Coordenações regionais
4. **Fontes de Recursos** — Classificação de recursos
5. **Contas Classificadas** — Mapeamento de contas
6. **Tipos de Processo** — Classificação de processos
7. **Períodos** — Períodos mensais
8. **Feriados** — Calendário de feriados
9. **Projetos** — Agrupamento de atividades
10. **Vínculos Órgão-Projeto** — Associações de órgãos a projetos
11. **Transferência de Órgãos** — Histórico de transições
12. **Transição Órgão SDI** — Promoção de órgãos
13. **Consulta de Órgãos** — Busca de órgãos provisório/definitivo
14. **Consulta de Justificativas** — Busca de justificativas

### Operações em Cada Módulo

Cada módulo suporta as seguintes operações:

#### **Consultar (CON)**
- Clique no módulo
- Vê lista de registros (paginado em 15 itens)
- Pode navegar entre páginas

#### **Novo (Incluir - I)**
- Clique no botão "Novo [Entidade]"
- Preencha o formulário
- Clique "Salvar"
- Registro é criado e adicionado à lista

#### **Editar (Alterar - A)**
- Na lista, clique no botão "Editar" do registro
- Modifique os campos permitidos
- Clique "Salvar"
- Registro é atualizado

#### **Deletar (Excluir - E)**
- Na lista, clique no botão "Deletar" do registro
- Confirme a exclusão na modal
- Registro é removido

#### **Restrições**
- **Bairros**: Não pode deletar se existem órgãos no bairro
- **Unidades**: Não pode deletar se existem grupos ou contratos
- **Grupos**: Não pode deletar se existem órgãos no grupo
- **Contas**: Não pode alterar a fonte (bloqueio intencional por regra de negócio)
- **Fontes**: Apenas consulta (inclusão/alteração não disponível nesta jornada)
- **Períodos**: Apenas criar (consulta e criação)
- **Projetos**: Não pode deletar se existem vínculos órgão-projeto

### Exemplo Prático: Cadastrar um Bairro

1. Clique em **"Bairros"** na home
2. Clique em **"Novo Bairro"**
3. Digite uma descrição, ex: **"Centro"**
4. Clique **"Salvar"**
5. Você voltará à lista e verá o novo bairro com um código sequencial (1, 2, 3...)

### Exemplo Prático: Alterar uma Unidade Orçamentária

1. Clique em **"Unidades Orçamentárias"** na home
2. Na lista, encontre uma unidade e clique **"Editar"**
3. Modifique a descrição
4. Clique **"Salvar"**
5. A alteração é registrada (você verá confirmação)

---

## 🏗️ Arquitetura Técnica

### Stack de Tecnologias

| Componente | Versão | Uso |
|-----------|--------|-----|
| **Python** | 3.11+ | Linguagem |
| **Flask** | 3.0.0 | Framework Web |
| **SQLAlchemy** | 2.0.23 | ORM (Mapeamento Objeto-Relacional) |
| **SQLite** | Built-in | Banco de Dados |
| **Jinja2** | Built-in | Template Engine |
| **HTML5** | Standard | Frontend |
| **CSS3** | Standard | Estilos |

### Estrutura de Diretórios

```
C:\iplan-sisgen\capacidade1\
├── app/                          # Aplicação Flask
│   ├── __init__.py               # Factory pattern
│   ├── config.py                 # Configurações
│   ├── database.py               # Gerenciamento de banco
│   │
│   ├── models/                   # Modelos de Dados (ORM)
│   │   ├── bairro.py             # Tabela BAIRRO
│   │   ├── unidade.py            # Tabela UNIDADE_ORCAMENTARIA
│   │   ├── grupo.py              # Tabela GRUPO
│   │   ├── fonte.py              # Tabela FONTE_RECURSOS
│   │   ├── conta.py              # Tabela CONTA_CLASSIFICADA
│   │   ├── tipo_processo.py      # Tabela TIPO_PROCESSO
│   │   ├── periodo.py            # Tabela PERIODO_REFERENCIA
│   │   ├── feriado.py            # Tabela FERIADO_ORGAO
│   │   ├── projeto.py            # Tabela PROJETO
│   │   ├── vinculo.py            # Tabela VINCULO_ORGAO_PROJETO
│   │   ├── historico.py          # Tabela HISTORICO_PERIODO_ORGAO
│   │   ├── auditoria.py          # Tabela AUDITORIA
│   │   └── __init__.py
│   │
│   ├── routes/                   # Rotas (Controllers)
│   │   ├── bairro_routes.py      # Rotas para Bairros
│   │   ├── unidade_routes.py     # Rotas para Unidades
│   │   ├── grupo_routes.py       # Rotas para Grupos
│   │   ├── fonte_routes.py       # Rotas para Fontes
│   │   ├── conta_routes.py       # Rotas para Contas
│   │   ├── tipo_processo_routes.py
│   │   ├── periodo_routes.py
│   │   ├── feriado_routes.py
│   │   ├── projeto_routes.py
│   │   ├── vinculo_routes.py
│   │   ├── transferencia_routes.py
│   │   ├── transicao_routes.py
│   │   ├── consulta_routes.py
│   │   └── __init__.py
│   │
│   ├── templates/                # Templates HTML
│   │   ├── base.html             # Template base
│   │   ├── index.html            # Home page
│   │   ├── error.html            # Página de erro
│   │   ├── bairro/
│   │   │   ├── list.html
│   │   │   ├── create.html
│   │   │   └── edit.html
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
│   │   └── consulta/
│   │
│   ├── static/                   # Arquivos estáticos
│   │   └── css/
│   │       └── style.css         # Estilos CSS
│   │
│   ├── validations/              # Validações de Negócio
│   │   ├── common_validations.py
│   │   ├── bairro_validations.py
│   │   └── __init__.py
│   └── __init__.py
│
├── tests/                        # Testes Automatizados
│   ├── test_bairro.py
│   ├── test_validations.py
│   └── ...
│
├── run.py                        # Entry Point
├── requirements.txt              # Dependências Python
├── app.db                        # Banco SQLite (criado ao rodar)
├── README.md                     # Este arquivo
├── QUICK_START.md               # Guia rápido
└── COMPLETION_SUMMARY.md        # Detalhes técnicos
```

### Fluxo de Requisição

```
1. Usuário acessa http://localhost:5000
                    ↓
2. Flask recebe requisição em run.py
                    ↓
3. Route em routes/*.py processa
                    ↓
4. Model acessa banco de dados (SQLite)
                    ↓
5. Validação em validations/ é aplicada
                    ↓
6. Template HTML renderizado
                    ↓
7. Resposta retornada ao navegador
```

---

## 💾 Banco de Dados

### Arquivo do Banco

O banco SQLite é criado automaticamente na primeira execução:

```
C:\iplan-sisgen\capacidade1\app.db
```

### Tabelas Criadas

| Tabela | Chave | Propósito |
|--------|-------|----------|
| `bairro` | codigo_bairro | Localização geográfica |
| `unidade_orcamentaria` | codigo_unidade | Alocação financeira |
| `grupo` | (codigo_grupo, tipo_orgao) | Agrupamento administrativo |
| `fonte_recursos` | (codigo_fonte, codigo_orgao) | Classificação de recursos |
| `conta_classificada` | (conta, codigo_orgao) | Mapeamento de contas |
| `tipo_processo` | codigo_tipo | Classificação de processos |
| `periodo_referencia` | (ano, mes) | Períodos mensais |
| `feriado_orgao` | (data, codigo_orgao) | Calendário |
| `projeto` | (codigo_projeto, secretaria) | Agrupamento de atividades |
| `vinculo_orgao_projeto` | (codigo_orgao, codigo_projeto) | Associações |
| `historico_periodo_orgao` | id | Histórico de transições |
| `auditoria` | id | Log de todas as operações |

### Validações de Banco

- Chaves primárias garantem unicidade
- Chaves estrangeiras garantem integridade referencial
- Campos obrigatórios impedindo valores nulos
- Constraints de valores (S/N, data range)

---

## 🔐 Segurança

### Implementado

- ✅ **SQL Injection Prevention** — SQLAlchemy ORM previne injeção SQL
- ✅ **XSS Prevention** — Jinja2 auto-escaping de templates
- ✅ **CSRF Ready** — Estrutura pronta para Flask-WTF
- ✅ **Audit Trail** — Todas operações registradas (CREATE, UPDATE, DELETE)
- ✅ **Imutable Logs** — Auditoria nunca é alterada ou deletada
- ✅ **Business Rules** — Validações de negócio em nível de aplicação

### Não Implementado (Escopo Futuro)

- Autenticação de usuários
- Autorização por perfil (RBAC)
- SSL/TLS (para produção: adicionar certificado)
- Rate limiting

---

## 🧪 Testes

### Executar Testes

```powershell
pip install pytest
pytest tests/
```

### Testes Inclusos

- `test_bairro.py` — Testes do módulo Bairros
- `test_validations.py` — Testes das validações
- `test_models.py` — Testes dos modelos ORM
- `test_routes.py` — Testes das rotas HTTP

---

## 📊 Auditoria e Logging

### Tabela de Auditoria

Todas as operações são registradas:

```sql
SELECT * FROM auditoria
ORDER BY timestamp DESC
LIMIT 10;
```

Exemplo de registro:

```json
{
  "id": 1,
  "tabela": "bairro",
  "operacao": "INSERT",
  "usuario": "usuario_sessao",
  "dados_antes": null,
  "dados_depois": "{\"codigo_bairro\": 1, \"descricao\": \"Centro\"}",
  "timestamp": "2024-10-03 14:32:15"
}
```

### Consultar Auditoria

Na aplicação, as operações são registradas automaticamente. Para análise:

```powershell
# Abrir SQLite CLI
sqlite3 C:\iplan-sisgen\capacidade1\app.db

# Queries úteis:
SELECT * FROM auditoria WHERE tabela = 'bairro';
SELECT * FROM auditoria WHERE operacao = 'UPDATE';
SELECT * FROM auditoria ORDER BY timestamp DESC LIMIT 20;
```

---

## ⚙️ Configuração

### Arquivo: `app/config.py`

```python
# Diretório da aplicação
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# URI do banco SQLite
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, '..', 'app.db')

# Chave secreta (alterar em produção)
SECRET_KEY = 'dev-secret-key-change-in-production'

# Echo SQL (para debug)
SQLALCHEMY_ECHO = False
```

### Alterar Configurações

Edite `app/config.py` para:
- Mudar localização do banco
- Alterar chave secreta
- Ativar/desativar echo SQL

---

## 🚨 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'flask'"

**Solução**: Instale dependências

```powershell
pip install -r requirements.txt
```

### Erro: "Port 5000 already in use"

**Solução**: Ou mate o processo anterior, ou use porta diferente

```powershell
# Altere app/config.py ou execute:
python run.py --port 5001
```

### Banco de Dados Corrompido

**Solução**: Delete o arquivo `app.db` (ele será recriado)

```powershell
Remove-Item app.db
python run.py
```

### Alterações no Código Não Refletem

**Solução**: Flask reconstrói automaticamente em debug. Se não, reinicie:

```powershell
# CTRL+C para parar
python run.py
```

---

## 📝 Operações Detalhadas por Módulo

### 1. Bairros (F-001)

**Operações**:
- **Consultar**: Listar todos os bairros (paginado)
- **Novo**: Criar bairro (código auto-gerado sequencial)
- **Deletar**: Remover bairro (bloqueado se órgãos existem)

**Validações**:
- Descrição obrigatória (max 25 caracteres)
- Código gerado automaticamente (iniciando em 1)
- Não permite duplicação de descrição

**Exemplo**: Cadastrar bairro "Centro", recebe código 1

---

### 2. Unidades Orçamentárias (F-002)

**Operações**:
- **Consultar**: Listar (paginado, remembers position)
- **Novo**: Criar unidade
- **Editar**: Alterar descrição
- **Deletar**: Remover (bloqueado se grupos/contratos)

**Validações**:
- Código numérico obrigatório (8 dígitos)
- Descrição obrigatória (max 40 caracteres)
- Não permite duplicação de código

**Capacidade**: 1.500.000 unidades

---

### 3. Grupos/Coordenações (F-003)

**Operações**:
- **Consultar**: Listar (filtrado por tipo órgão em sessão)
- **Novo**: Criar grupo
- **Editar**: Alterar descrição/unidade (com propagação)
- **Deletar**: Remover (bloqueado se órgãos)

**Validações**:
- Código numérico (2 dígitos), único por tipo
- Descrição obrigatória (max 40 caracteres)
- Unidade obrigatória (8 dígitos)

**Comportamento Especial**: 
- Ao alterar unidade, propaga para todos órgãos do grupo

---

### 4. Fontes de Recursos (F-004)

**Operações**:
- **Consultar**: Listar (por órgão em sessão)

**Validações**:
- Código numérico (7 dígitos)
- Descrição (max 30 caracteres)
- FNDE S/N (opcional)

**Nota**: Esta jornada é read-only. Inclusão/alteração não disponível.

---

### 5. Contas Classificadas (F-005)

**Operações**:
- **Consultar**: Listar contas (por órgão)
- **Novo**: Criar classificação (conta + fonte + creche)
- **Editar**: Alterar creche (fonte **não** pode ser alterada)
- **Deletar**: Remover classificação

**Validações**:
- Fonte obrigatória e deve existir
- Creche obrigatória (S/N)
- Não permite duplicação (conta + fonte)

**Restrição**: Alteração de fonte é bloqueada por regra de negócio

---

### 6. Tipos de Processo (F-006)

**Operações**:
- **Consultar**: Listar tipos
- **Novo**: Criar tipo
- **Editar**: Alterar descrição
- **Deletar**: Remover

**Validações**:
- Código numérico (2 dígitos)
- Descrição obrigatória (max 40 caracteres)
- Não permite duplicação

---

### 7. Períodos (F-007)

**Operações**:
- **Consultar**: Listar períodos (paginado)
- **Novo**: Criar período (ano/mês)

**Validações**:
- Ano: 1994-2099
- Mês: 01-12
- Não permite duplicação (ano, mês)

**Nota**: Sem alteração ou deleção (imutável)

---

### 8. Feriados (F-008)

**Operações**:
- **Consultar**: Listar (por órgão)
- **Novo**: Criar feriado
- **Editar**: Alterar descrição/creche/recesso
- **Deletar**: Remover feriado

**Validações**:
- Data: 1994-2099
- Descrição obrigatória
- Creche S/N (opcional)
- Recesso (literal)
- Não permite duplicação (data, órgão)

---

### 9. Projetos (F-009)

**Operações**:
- **Consultar**: Listar (por secretaria)
- **Novo**: Criar projeto
- **Editar**: Alterar descrição
- **Deletar**: Remover (bloqueado se vínculos)

**Validações**:
- Código numérico (2 dígitos)
- Descrição obrigatória (max 40 caracteres)
- Não permite duplicação por secretaria

---

### 10. Vínculos Órgão-Projeto (F-010)

**Operações**:
- **Consultar**: Listar vínculos
- **Novo**: Criar vínculo (órgão + projeto)
- **Deletar**: Remover vínculo

**Validações**:
- Órgão deve existir
- Projeto deve existir
- Não permite duplicação

---

### 11. Transferência de Órgãos (F-011)

**Operações**:
- **Novo**: Registrar transferência (fecha período anterior, abre novo)
- **Reabertura**: Reverter período anterior

**Efeito**:
- Cria histórico não-destrutivo
- Período anterior encerrado
- Período novo aberto

---

### 12. Transição Órgão SDI (F-012)

**Operações**:
- **Novo**: Registrar transição (órgão provisório → definitivo)

**Efeito**:
- Marca órgão provisório como desativado
- Marca órgão definitivo como ativo
- Registra em histórico com tipo "transicao_sdi"

---

### 13-14. Consultas (F-013, F-014)

**Operações**:
- **Consultar Órgãos**: Listar órgãos provisório/definitivo
- **Consultar Justificativas**: Listar justificativas por tipo

**Efeito**:
- Listagem apenas (read-only)
- Pedido de relatório (registra em fila)

---

## 📞 Suporte e Documentação

### Arquivos de Documentação

- **README.md** (este arquivo) — Guia completo
- **QUICK_START.md** — Início rápido em 5 minutos
- **COMPLETION_SUMMARY.md** — Detalhes técnicos de implementação
- **FILES_MANIFEST.txt** — Lista completa de arquivos

### Referência de Implementação

Toda a implementação é baseada em:

**Evidências**: `C:\iplan-sisgen\regras-negocios\US - C*.md` (15 arquivos)

**Contrato**: `C:\iplan-sisgen\resposta-capacidade1-fase3.md`

**Cada função tem comentário RN-XX** citando a regra de negócio de origem.

---

## 🔄 Ciclo de Vida de Desenvolvimento

### Fases Completadas

- ✅ **Fase 1**: Identificação das Evidências (15 estórias)
- ✅ **Fase 2**: Análise Funcional (216 RN documentadas)
- ✅ **Fase 3**: Contrato de Implementação (51 elementos autorizados)
- ✅ **Fase 4**: Geração Física (89 arquivos, 8.650 linhas de código)

### Status Atual

**Aguardando validação humana** da aplicação executada.

### Próximos Passos

1. Execute a aplicação
2. Teste as 14 funcionalidades
3. Valide conforme evidências originais
4. Reporte problemas (defeito, interpretação, novo requisito)
5. Se tudo OK: **CAPACIDADE APROVADA**

---

## 📄 Licença

Trabalho em progresso para Secretaria de Educação.

---

## 👥 Autores

Gerado automaticamente por OpenCode (Inteligência Artificial) baseado em:
- Análise de evidências do sistema legado
- Contrato de implementação aprovado
- Validações de negócio documentadas

**Data**: Outubro de 2026

---

## 🎯 Objetivo da Capacidade 1

Fornecer a infraestrutura de dados fundamental para a rede escolar, permitindo:

1. **Planejamento Orçamentário** — Estrutura de unidades e fontes
2. **Organização Administrativa** — Bairros, grupos, órgãos
3. **Gestão Financeira** — Contas classificadas, processos
4. **Calendário Operacional** — Períodos, feriados
5. **Rastreabilidade** — Auditoria completa de todas operações

---

**Pronto para usar. Divirta-se! 🚀**

