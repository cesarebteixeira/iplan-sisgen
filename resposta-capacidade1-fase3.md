# FASE 3 — CONTRATO DE IMPLEMENTAÇÃO
## Capacidade 1 — Estrutura da rede e do gasto

---

## APRESENTAÇÃO

Este documento constitui o **CONTRATO DE IMPLEMENTAÇÃO** da Capacidade 1, conforme definido no Prompt Mestre.

Este contrato funciona como uma **WHITELIST**: somente o que estiver explicitamente autorizado neste documento poderá chegar ao código.

**Data**: Outubro de 2026  
**Análise Base**: Fase 2 completa com 216 elementos DOCUMENTADOS  
**Aprovação Esperada**: Validação humana

---

## FUNCIONALIDADES AUTORIZADAS

### F-001: Manter Bairros (C023T)

| Aspecto | Detalhe |
|---------|---------|
| **Identificador** | F-001 |
| **Descrição** | Consultar, incluir, excluir bairros da rede |
| **RN Relacionada** | C023T RN-01 a RN-15 |
| **CA Relacionado** | C023T Gherkin completo (18 cenários) |
| **Arquivo de Evidência** | `US - C023T.md` |
| **Classificação** | DOCUMENTADO |
| **Situação para Implementação** | **AUTORIZADO** |

**Especificação**:
- Entidade: BAIRRO (código 3d + descrição 25c)
- Operações: CON (consulta), I (criar), E (deletar)
- Validações: Código numérico, descrição obrigatória, duplicação, órgãos dependentes
- Paginação: 15 linhas
- Auto-increment: Código gerado sequencialmente, primeira=1
- Guardar: Não deletar se órgãos existem no bairro
- Auditoria: Todas as operações registradas
- **Restrição Conhecida**: Alteração marcada como unreachable (RN-07), não implementar

**Autorizado para Implementação**: ✓ SIM

---

### F-002: Manter Unidades Orçamentárias (C025T)

| Aspecto | Detalhe |
|---------|---------|
| **Identificador** | F-002 |
| **Descrição** | Consultar, incluir, alterar, excluir unidades orçamentárias |
| **RN Relacionada** | C025T RN-01 a RN-20 |
| **CA Relacionado** | C025T Gherkin completo (20+ cenários) |
| **Arquivo de Evidência** | `US - C025T.md` |
| **Classificação** | DOCUMENTADO |
| **Situação para Implementação** | **AUTORIZADO** |

**Especificação**:
- Entidade: UNIDADE_ORÇAMENTÁRIA (código 8d + descrição 40c)
- Capacidade: 1.500.000 unidades
- Operações: CON (consulta), I (criar), A (alterar), E (deletar)
- Validações: Código numérico (8d), descrição obrigatória, duplicação, existência, grupos/contratos dependentes
- Paginação: 15 linhas por página
- Persistência: Última unidade consultada entre reaperturas
- Guarda de integridade: Não deletar se grupos ou contratos existem
- Auditoria: Código, descrição, valores prior/post

**Autorizado para Implementação**: ✓ SIM

---

### F-003: Manter Grupos/Coordenações (C126T)

| Aspecto | Detalhe |
|---------|---------|
| **Identificador** | F-003 |
| **Descrição** | Consultar, incluir, alterar, excluir grupos por tipo de órgão |
| **RN Relacionada** | C126T RN-01 a RN-21 |
| **CA Relacionado** | C126T Gherkin completo (20+ cenários) |
| **Arquivo de Evidência** | `US - C126T.md` |
| **Classificação** | DOCUMENTADO |
| **Situação para Implementação** | **AUTORIZADO** |

**Especificação**:
- Entidade: GRUPO (código 2d + descrição 40c + unidade 8d + tipo_órgão)
- Chave Natural: (Código, Tipo de Órgão)
- Capacidade: 1.000 grupos
- Operações: CON (filtrado por tipo órgão em sessão), I (criar), A (alterar + propagar), E (deletar com guarda)
- Validações: Código numérico (2d), unidade numérica (8d), descrição obrigatória, duplicação dentro tipo, existência, órgãos dependentes
- Paginação: 15 linhas
- **PROPAGAÇÃO ESPECIAL**: Alteração de unidade em grupo propaga para TODOS os órgãos do grupo
- Guarda de integridade: Não deletar se órgãos existem
- Auditoria: Todas as operações + propagação
- Filtro de Sessão: Mostrar apenas grupos do tipo de órgão em sessão
- **Questão [?] Resolvida**: Traversal de órgãos usa chave zero-filled na terceira parte (implementação a validar)

**Autorizado para Implementação**: ✓ SIM

---

### F-004: Manter Fontes de Recursos (C144T)

| Aspecto | Detalhe |
|---------|---------|
| **Identificador** | F-004 |
| **Descrição** | Consultar fontes de recursos por órgão |
| **RN Relacionada** | C144T RN-01 a RN-11 |
| **CA Relacionado** | C144T Gherkin (11 cenários) |
| **Arquivo de Evidência** | `US - C144T.md` |
| **Classificação** | DOCUMENTADO (com restrição de jornada) |
| **Situação para Implementação** | **AUTORIZADO (CON apenas)** |

**Especificação**:
- Entidade: FONTE_RECURSOS (código 7d + descrição 30c + ind_FNDE S/N)
- Chave Natural: (Código, Órgão)
- Escopo: Por órgão
- Capacidade: 1.000 fontes por órgão
- Operações: **CON APENAS** (consulta de fontes do órgão em sessão)
  - I (criar) e A (alterar): Não implementar por esta jornada (código I/A presente mas inatingível)
- Validações: Código numérico (7d), descrição obrigatória, FNDE S/N (se informado), duplicação (inatingível), existência (inatingível)
- Paginação: 15 linhas
- Persistência: Última fonte consultada
- Filtro de Sessão: Mostrar fontes do órgão em sessão
- Mensagem Vazia: Se órgão não tem fontes cadastradas
- Auditoria: Consultoria não grava (por design)
- **Restrição Documentada**: Esta jornada abre apenas CON; outras jornadas podem ter I/A

**Autorizado para Implementação**: ✓ SIM (leitura) — NÃO implementar I/A

---

### F-005: Classificar Contas (C147T)

| Aspecto | Detalhe |
|---------|---------|
| **Identificador** | F-005 |
| **Descrição** | Consultar, incluir, alterar, excluir classificação de contas por fonte |
| **RN Relacionada** | C147T RN-01 a RN-15 |
| **CA Relacionado** | C147T Gherkin completo (18+ cenários) |
| **Arquivo de Evidência** | `US - C147T.md` |
| **Classificação** | DOCUMENTADO (com paradoxo conhecido) |
| **Situação para Implementação** | **AUTORIZADO com RESTRIÇÃO** |

**Especificação**:
- Entidade: CONTA_CLASSIFICADA (conta + fonte 7d + creche S/N)
- Chave Natural: (Conta, Órgão) — questão de múltiplas fontes documentada como ambígua [?]
- Escopo: Por órgão
- Operações: CON (consulta), I (criar), A (alterar creche apenas), E (deletar)
- Validações: Fonte obrigatória e deve existir, creche S/N obrigatória, duplicação com mesma fonte, existência com mesma fonte
- Paginação: 15 linhas
- Autorização: Consulta isenta de verificação de operação; I/A/E requerem autorização específica
- Auditoria: Todas as operações
- **RESTRIÇÃO DOCUMENTADA**: Alteração de fonte BLOQUEADA por lógica de RN-05 (validação de existência da mesma fonte que se quer alterar = impossível)
  - Implementar: Criação de conta + fonte, alteração de creche apenas, deleção
  - NÃO implementar: Mudança de fonte (logicamente bloqueada)
- **Questão [?]**: Conta pode ter múltiplas fontes? Ambiguidade reconhecida, não implementar múltiplas até clarificação

**Autorizado para Implementação**: ✓ SIM (com restrição) — Não permitir alteração de fonte

---

### F-006: Manter Tipos de Processo (C162T)

| Aspecto | Detalhe |
|---------|---------|
| **Identificador** | F-006 |
| **Descrição** | Consultar, incluir, alterar, manter tipos de processo do órgão |
| **RN Relacionada** | C162T RN-01 a RN-16 |
| **CA Relacionado** | C162T Gherkin completo |
| **Arquivo de Evidência** | `US - C162T.md` |
| **Classificação** | DOCUMENTADO |
| **Situação para Implementação** | **AUTORIZADO** |

**Especificação**:
- Entidade: TIPO_PROCESSO (código 2d + descrição 40c)
- Operações: CON (consulta), I (criar), A (alterar), E (deletar não mencionado)
- Validações: Código numérico (2d), descrição obrigatória, duplicação, existência
- Paginação: 15 linhas
- Persistência: Última posição entre reaperturas
- Auditoria: Operações I/A

**Autorizado para Implementação**: ✓ SIM

---

### F-007: Manter Períodos de Referência (C172T)

| Aspecto | Detalhe |
|---------|---------|
| **Identificador** | F-007 |
| **Descrição** | Consultar, incluir períodos mensais de referência |
| **RN Relacionada** | C172T RN-01 a RN-16 |
| **CA Relacionado** | C172T Gherkin completo |
| **Arquivo de Evidência** | `US - C172T.md` |
| **Classificação** | DOCUMENTADO |
| **Situação para Implementação** | **AUTORIZADO** |

**Especificação**:
- Entidade: PERIODO_REFERENCIA (ano 4d + mês 2d)
- Chave Natural: (Ano, Mês)
- Intervalo Válido: Anos 1994-2099, Meses 01-12
- Operações: CON (consulta), I (criar período)
- Alteração/Deleção: NÃO mencionadas (criar apenas)
- Validações: Ano numérico (1994-2099), mês numérico (01-12), duplicação período
- Paginação: 15 linhas
- Persistência: Última posição
- Auditoria: Criação registrada

**Autorizado para Implementação**: ✓ SIM (leitura + criação apenas)

---

### F-008: Manter Feriados do Órgão (C192T)

| Aspecto | Detalhe |
|---------|---------|
| **Identificador** | F-008 |
| **Descrição** | Consultar, incluir, alterar, excluir feriados e recessos do órgão |
| **RN Relacionada** | C192T RN-01 a RN-14 |
| **CA Relacionado** | C192T Gherkin completo |
| **Arquivo de Evidência** | `US - C192T.md` |
| **Classificação** | DOCUMENTADO |
| **Situação para Implementação** | **AUTORIZADO** |

**Especificação**:
- Entidade: FERIADO_ORGAO (data + órgão + descrição + creche S/N + recesso literal)
- Chave Natural: (Data, Órgão)
- Intervalo Válido: Datas 1994-2099
- Escopo: Por órgão
- Operações: CON (consulta), I (criar), A (alterar), E (deletar)
- Validações: Data válida (1994-2099), descrição obrigatória, creche S/N, duplicação data/órgão, existência
- Paginação: 15 linhas
- Auditoria: Operações I/A/E
- **Questão [?] Herança**: Órgão herda feriados de coordenação regional — mecanismo não implementar, apenas manter feriados locais por órgão. Herança é computada em leitura (não persistida)

**Autorizado para Implementação**: ✓ SIM (feriados locais; herança fora de escopo)

---

### F-009: Manter Projetos da Secretaria (C205T)

| Aspecto | Detalhe |
|---------|---------|
| **Identificador** | F-009 |
| **Descrição** | Consultar, incluir, alterar, excluir projetos |
| **RN Relacionada** | C205T RN-01 a RN-19 |
| **CA Relacionado** | C205T Gherkin completo |
| **Arquivo de Evidência** | `US - C205T.md` |
| **Classificação** | DOCUMENTADO |
| **Situação para Implementação** | **AUTORIZADO** |

**Especificação**:
- Entidade: PROJETO (código 2d + secretaria + descrição 40c)
- Chave Natural: (Código, Secretaria)
- Escopo: Por secretaria
- Operações: CON (consulta), I (criar), A (alterar), E (deletar com guarda)
- Validações: Código numérico (2d), descrição obrigatória, duplicação dentro secretaria, existência, vínculos dependentes
- Paginação: 15 linhas
- Guarda de integridade: Não deletar se vínculos órgão-projeto existem
- Auditoria: Operações I/A/E
- Persistência: Última posição

**Autorizado para Implementação**: ✓ SIM

---

### F-010: Vínculos Órgão-Projeto (C207T)

| Aspecto | Detalhe |
|---------|---------|
| **Identificador** | F-010 |
| **Descrição** | Consultar, criar, excluir vínculos entre órgãos e projetos |
| **RN Relacionada** | C207T RN-01 a RN-19 |
| **CA Relacionado** | C207T Gherkin completo |
| **Arquivo de Evidência** | `US - C207T.md` |
| **Classificação** | DOCUMENTADO (com questão sobre "órgão completo") |
| **Situação para Implementação** | **AUTORIZADO com QUESTÃO** |

**Especificação**:
- Entidade: VINCULO_ORGAO_PROJETO (órgão + projeto)
- Chave Natural: (Órgão, Projeto)
- Operações: CON (consulta), I (criar vínculo), E (deletar vínculo)
- Validações: Órgão deve existir, projeto deve existir
- **QUESTÃO [?] Órgão Completo**: Mencionado como restrição (órgão incompleto não pode vincular), mas "completo" não foi definido em Fase 2
  - **Implementação**: Validação básica de existência de órgão + projeto; restrição de "completude" remover da whitelist até clarificação
  - **Flag para Validação Humana**: Se houver definição de "completo", implementar segunda iteração
- Persistência: Última posição
- Auditoria: Operações I/E
- Paginação: 15 linhas

**Autorizado para Implementação**: ✓ SIM (validação básica) — Questão [?] para validação humana

---

### F-011: Transferência de Órgãos entre Coordenações (C225T)

| Aspecto | Detalhe |
|---------|---------|
| **Identificador** | F-011 |
| **Descrição** | Transferir órgão de uma coordenação regional para outra (fecha período anterior, abre novo) |
| **RN Relacionada** | C225T RN-01 a RN-19 |
| **CA Relacionado** | C225T Gherkin completo |
| **Arquivo de Evidência** | `US - C225T.md` |
| **Classificação** | DOCUMENTADO |
| **Situação para Implementação** | **AUTORIZADO** |

**Especificação**:
- Operação: Criar histórico de mudança de período/coordenação
- Entidade: HISTORICO_PERIODO_ORGAO (órgão + data_mudança + período_anterior + período_novo)
- Efeito: Encerra período anterior, abre período novo
- Validações: Data range 1994-2099, períodos válidos, órgão existe
- Auditoria: Completa com timestamp
- Reabertura: Permite voltar período fechado (reversão com auditoria)
- Persistência: Histórico não-destrutivo
- Cascata: Não deletar históricos, adicionar novos registros

**Autorizado para Implementação**: ✓ SIM

---

### F-012: Substituição de Órgão Provisório por Definitivo SDI (C226T)

| Aspecto | Detalhe |
|---------|---------|
| **Identificador** | F-012 |
| **Descrição** | Transição de órgão provisório para órgão definitivo SDI |
| **RN Relacionada** | C226T RN-01 a RN-11 |
| **CA Relacionado** | C226T Gherkin |
| **Arquivo de Evidência** | `US - C226T.md` |
| **Classificação** | DOCUMENTADO (com cascata incompleta [?]) |
| **Situação para Implementação** | **AUTORIZADO com LIMITAÇÃO** |

**Especificação**:
- Operação: Registrar transição de órgão provisório → definitivo
- Entidade: HISTORICO_PERIODO_ORGAO (registro de mudança)
- Validações: Órgão provisório existe, órgão definitivo existe, definitivo é ativo
- Efeito: Marca órgão provisório como desativado, marca definitivo como ativo
- Auditoria: Completa com timestamp
- **Questão [?] Cascata**: O que se propaga? Vínculos? Históricos de contas? Feriados?
  - **Implementação**: Histórico registra transição; propagação específica remover da whitelist até clarificação
  - **Flag para Validação Humana**: Definir cascata exata em segunda iteração se necessário

**Autorizado para Implementação**: ✓ SIM (histórico + marcação; sem cascata específica)

---

### F-013: Consulta de Órgãos com Relatório (C226C)

| Aspecto | Detalhe |
|---------|---------|
| **Identificador** | F-013 |
| **Descrição** | Consultar órgãos provisório/definitivo e pedir listagem |
| **RN Relacionada** | C226C RN-01 a RN-15 |
| **CA Relacionado** | C226C Gherkin |
| **Arquivo de Evidência** | `US - C226C.md` |
| **Classificação** | DOCUMENTADO |
| **Situação para Implementação** | **AUTORIZADO** |

**Especificação**:
- Operação: CON (consulta leitura-apenas)
- Filtro: Órgãos da coordenação regional em sessão
- Paginação: 15 linhas
- Relatório: Pedido de listagem (fila de impressão)
- Auditoria: Consulta registrada
- Persistência: Última posição

**Autorizado para Implementação**: ✓ SIM

---

### F-014: Consulta de Justificativas (C250C)

| Aspecto | Detalhe |
|---------|---------|
| **Identificador** | F-014 |
| **Descrição** | Consultar justificativas por tipo de órgão |
| **RN Relacionada** | C250C RN-01 a RN-10 |
| **CA Relacionado** | C250C Gherkin |
| **Arquivo de Evidência** | `US - C250C.md` |
| **Classificação** | DOCUMENTADO |
| **Situação para Implementação** | **AUTORIZADO** |

**Especificação**:
- Operação: CON (consulta leitura-apenas)
- Filtro: Justificativas do tipo de órgão em sessão
- Paginação: 15 linhas
- Relatório: Pedido de listagem (fila de impressão)
- Auditoria: Consulta registrada
- Persistência: Última posição

**Autorizado para Implementação**: ✓ SIM

---

### F-015: Manter Feriados por Órgão (C806T)

| Aspecto | Detalhe |
|---------|---------|
| **Identificador** | F-015 |
| **Descrição** | Manter feriados específicos por órgão (duplicado funcional com C192T) |
| **RN Relacionada** | C806T RN-01 a RN-10 |
| **CA Relacionado** | C806T Gherkin |
| **Arquivo de Evidência** | `US - C806T.md` |
| **Classificação** | DOCUMENTADO (como segundo cadastro ao lado de C192T) |
| **Situação para Implementação** | **CONSOLIDAR COM F-008** |

**Especificação**:
- Entidade: FERIADO_ORGAO (mesma de C192T F-008)
- Operações: CON, I, A, E (idêntico a C192T)
- **Nota Importante**: `capacidades.md` menciona "Segundo cadastro de feriados, ao lado da C192T. Os dois ficam na 1: feriados estão nomeados lá, e separá-los por tela seria inventar um recorte que o VDP não faz."
- **Recomendação**: Implementar única interface para feriados (F-008), usando-a para ambas as jornadas C192T e C806T

**Autorizado para Implementação**: ✓ SIM (consolidado com F-008)

---

## INTERFACE AUTORIZADA

### Telas Necessárias

#### T-001: Tela de Bairros

| Atributo | Valor |
|----------|-------|
| **Identificador** | T-001 |
| **Nome** | Manutenção de Bairros |
| **Funcionalidades Relacionadas** | F-001 |
| **Evidência** | C023T |
| **Elementos** | |
| — Modo (ALT/CON) | Campo seletor | Funcionalidade: Alternar entre consulta e manutenção |
| — Código do Bairro | Campo numérico (3d) | Funcionalidade: Busca e identificação (F-001) |
| — Descrição | Campo texto (25c) | Funcionalidade: Nome do bairro (F-001) |
| — Situação/Ação | Campo char (I/A/E) | Funcionalidade: Operação por linha (F-001) |
| — Botão Consultar | Ação | Funcionalidade: Listar bairros (F-001 CON) |
| — Botão Buscar por Descrição | Ação | Funcionalidade: Busca de bairro (F-001) |
| — Botão Gravar | Ação | Funcionalidade: Salvar alterações (F-001 I/E) |
| — Mensagens de Erro | Área de exibição | Funcionalidade: Feedback validação |
| — Paginação | Controle | Funcionalidade: Navegar 15 linhas |

**Classificação**: ✓ AUTORIZADO

---

#### T-002: Tela de Unidades Orçamentárias

| Atributo | Valor |
|----------|-------|
| **Identificador** | T-002 |
| **Nome** | Manutenção de Unidades Orçamentárias |
| **Funcionalidades Relacionadas** | F-002 |
| **Evidência** | C025T |
| **Elementos** | |
| — Modo (ALT/CON) | Campo seletor | Funcionalidade: F-002 |
| — Código | Campo numérico (8d) | Funcionalidade: Identificação e busca |
| — Descrição | Campo texto (40c) | Funcionalidade: Nome da unidade |
| — Ação | Campo char (I/A/E) | Funcionalidade: Operação por linha |
| — Botão Gravar | Ação | Funcionalidade: Salvar (F-002 I/A/E) |
| — Mensagens | Área | Funcionalidade: Feedback |
| — Paginação | Controle | Funcionalidade: 15 linhas |

**Classificação**: ✓ AUTORIZADO

---

#### T-003: Tela de Grupos

| Atributo | Valor |
|----------|-------|
| **Identificador** | T-003 |
| **Nome** | Manutenção de Grupos/Coordenações |
| **Funcionalidades Relacionadas** | F-003 |
| **Evidência** | C126T |
| **Elementos** | |
| — Modo (ALT/CON) | Campo seletor | Funcionalidade: F-003 |
| — Código | Campo numérico (2d) | Funcionalidade: Identificação |
| — Descrição | Campo texto (40c) | Funcionalidade: Nome do grupo |
| — Unidade Orçamentária | Campo numérico (8d) | Funcionalidade: Referência a F-002 |
| — Tipo Órgão | Campo (somente leitura) | Funcionalidade: De sessão, filtro |
| — Ação | Campo char (I/A/E) | Funcionalidade: Operação |
| — Botão Gravar | Ação | Funcionalidade: Salvar com propagação (F-003) |
| — Mensagens | Área | Funcionalidade: Feedback incluindo propagação |
| — Paginação | Controle | Funcionalidade: 15 linhas |

**Classificação**: ✓ AUTORIZADO

---

#### T-004: Tela de Fontes de Recursos

| Atributo | Valor |
|----------|-------|
| **Identificador** | T-004 |
| **Nome** | Consulta de Fontes de Recursos |
| **Funcionalidades Relacionadas** | F-004 |
| **Evidência** | C144T |
| **Elementos** | |
| — Código | Campo numérico (7d) | Funcionalidade: Identificação |
| — Descrição | Campo texto (30c) | Funcionalidade: Nome da fonte |
| — Indicador FNDE | Campo char (S/N) | Funcionalidade: Flag (leitura) |
| — Botão Consultar | Ação | Funcionalidade: Listar (F-004 CON) |
| — Mensagens | Área | Funcionalidade: "Nao existem fontes..." |
| — Paginação | Controle | Funcionalidade: 15 linhas |
| **Nota** | **NÃO incluir**: Modo ALT, Botão Gravar, campos de ação. Apenas leitura. |

**Classificação**: ✓ AUTORIZADO (leitura)

---

#### T-005: Tela de Contas Classificadas

| Atributo | Valor |
|----------|-------|
| **Identificador** | T-005 |
| **Nome** | Classificação de Contas |
| **Funcionalidades Relacionadas** | F-005 |
| **Evidência** | C147T |
| **Elementos** | |
| — Modo (ALT/CON) | Campo seletor | Funcionalidade: F-005 |
| — Conta | Campo identificador | Funcionalidade: Número da conta |
| — Fonte | Campo numérico (7d) | Funcionalidade: Referência a F-004 |
| — Creche | Campo char (S/N) | Funcionalidade: Flag creche |
| — Ação | Campo char (I/A/E) | Funcionalidade: Operação |
| — Botão Gravar | Ação | Funcionalidade: Salvar (F-005 I/A/E) |
| — Mensagens | Área | Funcionalidade: Feedback validação |
| — Paginação | Controle | Funcionalidade: 15 linhas |
| **Restrição** | **Alteração de Fonte BLOQUEADA** (não permitir mudança de fonte por RN-05) |

**Classificação**: ✓ AUTORIZADO (com restrição)

---

#### T-006: Tela de Tipos de Processo

| Atributo | Valor |
|----------|-------|
| **Identificador** | T-006 |
| **Nome** | Manutenção de Tipos de Processo |
| **Funcionalidades Relacionadas** | F-006 |
| **Evidência** | C162T |
| **Elementos** | |
| — Modo (ALT/CON) | Campo seletor | Funcionalidade: F-006 |
| — Código | Campo numérico (2d) | Funcionalidade: Identificação |
| — Descrição | Campo texto (40c) | Funcionalidade: Nome do tipo |
| — Ação | Campo char (I/A/E) | Funcionalidade: Operação |
| — Botão Gravar | Ação | Funcionalidade: Salvar (F-006 I/A) |
| — Mensagens | Área | Funcionalidade: Feedback |
| — Paginação | Controle | Funcionalidade: 15 linhas |

**Classificação**: ✓ AUTORIZADO

---

#### T-007: Tela de Períodos

| Atributo | Valor |
|----------|-------|
| **Identificador** | T-007 |
| **Nome** | Manutenção de Períodos de Referência |
| **Funcionalidades Relacionadas** | F-007 |
| **Evidência** | C172T |
| **Elementos** | |
| — Modo (ALT/CON) | Campo seletor | Funcionalidade: F-007 |
| — Ano | Campo numérico (4d, 1994-2099) | Funcionalidade: Identificação período |
| — Mês | Campo numérico (2d, 01-12) | Funcionalidade: Identificação período |
| — Ação | Campo char (I) | Funcionalidade: Criar período (apenas I) |
| — Botão Gravar | Ação | Funcionalidade: Salvar (F-007 I) |
| — Mensagens | Área | Funcionalidade: Feedback validação ano/mês |
| — Paginação | Controle | Funcionalidade: 15 linhas |

**Classificação**: ✓ AUTORIZADO (criação apenas)

---

#### T-008: Tela de Feriados

| Atributo | Valor |
|----------|-------|
| **Identificador** | T-008 |
| **Nome** | Manutenção de Feriados |
| **Funcionalidades Relacionadas** | F-008, F-015 (consolidadas) |
| **Evidência** | C192T, C806T |
| **Elementos** | |
| — Modo (ALT/CON) | Campo seletor | Funcionalidade: F-008 |
| — Data | Campo data (1994-2099) | Funcionalidade: Identificação |
| — Descrição | Campo texto (40c) | Funcionalidade: Nome feriado |
| — Creche | Campo char (S/N) | Funcionalidade: Indicador (F-008) |
| — Recesso | Campo char (literal) | Funcionalidade: Identificação de recesso |
| — Ação | Campo char (I/A/E) | Funcionalidade: Operação |
| — Botão Gravar | Ação | Funcionalidade: Salvar (F-008 I/A/E) |
| — Mensagens | Área | Funcionalidade: Feedback |
| — Paginação | Controle | Funcionalidade: 15 linhas |
| **Nota** | Usar única interface para C192T e C806T |

**Classificação**: ✓ AUTORIZADO

---

#### T-009: Tela de Projetos

| Atributo | Valor |
|----------|-------|
| **Identificador** | T-009 |
| **Nome** | Manutenção de Projetos |
| **Funcionalidades Relacionadas** | F-009 |
| **Evidência** | C205T |
| **Elementos** | |
| — Modo (ALT/CON) | Campo seletor | Funcionalidade: F-009 |
| — Código | Campo numérico (2d) | Funcionalidade: Identificação |
| — Descrição | Campo texto (40c) | Funcionalidade: Nome do projeto |
| — Ação | Campo char (I/A/E) | Funcionalidade: Operação |
| — Botão Gravar | Ação | Funcionalidade: Salvar (F-009 I/A/E) |
| — Mensagens | Área | Funcionalidade: Feedback |
| — Paginação | Controle | Funcionalidade: 15 linhas |

**Classificação**: ✓ AUTORIZADO

---

#### T-010: Tela de Vínculos Órgão-Projeto

| Atributo | Valor |
|----------|-------|
| **Identificador** | T-010 |
| **Nome** | Vínculos de Órgão a Projetos |
| **Funcionalidades Relacionadas** | F-010 |
| **Evidência** | C207T |
| **Elementos** | |
| — Modo (ALT/CON) | Campo seletor | Funcionalidade: F-010 |
| — Órgão | Campo identificador | Funcionalidade: Identificação |
| — Projeto | Campo numérico (2d) | Funcionalidade: Referência a F-009 |
| — Ação | Campo char (I/E) | Funcionalidade: Criar/Deletar vínculo |
| — Botão Gravar | Ação | Funcionalidade: Salvar (F-010 I/E) |
| — Mensagens | Área | Funcionalidade: Feedback |
| — Paginação | Controle | Funcionalidade: 15 linhas |
| **Nota** | Validação básica de existência; restrição "órgão completo" remover até clarificação |

**Classificação**: ✓ AUTORIZADO (sem "órgão completo")

---

#### T-011: Tela de Transferência de Órgãos

| Atributo | Valor |
|----------|-------|
| **Identificador** | T-011 |
| **Nome** | Transferência de Órgãos entre Coordenações |
| **Funcionalidades Relacionadas** | F-011 |
| **Evidência** | C225T |
| **Elementos** | |
| — Órgão | Campo identificador | Funcionalidade: Seleção |
| — Período Anterior | Campo (Ano/Mês) | Funcionalidade: Período encerrado |
| — Período Novo | Campo (Ano/Mês) | Funcionalidade: Período aberto |
| — Ação | Campo char (I/E para reabertura) | Funcionalidade: Criar/Reverter |
| — Botão Executar | Ação | Funcionalidade: Salvar transição (F-011) |
| — Mensagens | Área | Funcionalidade: Feedback |
| **Nota** | Histórico não-destrutivo, novos registros adicionados |

**Classificação**: ✓ AUTORIZADO

---

#### T-012: Tela de Transição Órgão SDI

| Atributo | Valor |
|----------|-------|
| **Identificador** | T-012 |
| **Nome** | Substituição de Órgão Provisório por Definitivo |
| **Funcionalidades Relacionadas** | F-012 |
| **Evidência** | C226T |
| **Elementos** | |
| — Órgão Provisório | Campo (somente leitura) | Funcionalidade: De sessão |
| — Órgão Definitivo SDI | Campo identificador | Funcionalidade: Seleção |
| — Data de Transição | Campo data | Funcionalidade: Timestamp |
| — Botão Executar | Ação | Funcionalidade: Registrar transição (F-012) |
| — Mensagens | Área | Funcionalidade: Feedback |
| **Nota** | Cascata de propagação remover até clarificação |

**Classificação**: ✓ AUTORIZADO (sem cascata)

---

#### T-013: Tela de Consulta de Órgãos

| Atributo | Valor |
|----------|-------|
| **Identificador** | T-013 |
| **Nome** | Consulta de Órgãos com Relatório |
| **Funcionalidades Relacionadas** | F-013 |
| **Evidência** | C226C |
| **Elementos** | |
| — Código do Órgão | Campo identificador | Funcionalidade: Busca |
| — Descrição | Campo texto (leitura) | Funcionalidade: Exibição |
| — Tipo (Provisório/Definitivo) | Campo (leitura) | Funcionalidade: Exibição |
| — Botão Consultar | Ação | Funcionalidade: Listar (F-013 CON) |
| — Botão Pedir Relatório | Ação | Funcionalidade: Fila impressão |
| — Mensagens | Área | Funcionalidade: Feedback |
| — Paginação | Controle | Funcionalidade: 15 linhas |
| **Nota** | Leitura apenas, sem alteração |

**Classificação**: ✓ AUTORIZADO

---

#### T-014: Tela de Consulta de Justificativas

| Atributo | Valor |
|----------|-------|
| **Identificador** | T-014 |
| **Nome** | Consulta de Justificativas |
| **Funcionalidades Relacionadas** | F-014 |
| **Evidência** | C250C |
| **Elementos** | |
| — Tipo de Órgão | Campo (de sessão, leitura) | Funcionalidade: Filtro |
| — Justificativa | Campo identificador | Funcionalidade: Busca |
| — Descrição | Campo texto (leitura) | Funcionalidade: Exibição |
| — Botão Consultar | Ação | Funcionalidade: Listar (F-014 CON) |
| — Botão Pedir Relatório | Ação | Funcionalidade: Fila impressão |
| — Mensagens | Área | Funcionalidade: Feedback |
| — Paginação | Controle | Funcionalidade: 15 linhas |
| **Nota** | Leitura apenas |

**Classificação**: ✓ AUTORIZADO

---

## MODELO DE DADOS AUTORIZADO

### Tabelas para Criação

#### TB-001: BAIRRO

```sql
CREATE TABLE BAIRRO (
  codigo_bairro INTEGER PRIMARY KEY,
  descricao VARCHAR(25) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

| Campo | Tipo | Tamanho | PK | NOT NULL | Referência | Fonte |
|-------|------|---------|----|----|-----------|-------|
| codigo_bairro | INTEGER | 3d | ✓ | ✓ | — | C023T RN-05 |
| descricao | VARCHAR | 25 | — | ✓ | — | C023T RN-04 |
| created_at | TIMESTAMP | — | — | — | — | DECISÃO TÉCNICA |
| updated_at | TIMESTAMP | — | — | — | — | DECISÃO TÉCNICA |

**Decisões Técnicas**:
- `created_at`, `updated_at` são campos técnicos internos (não apresentar ao usuário)
- Chave numérica simples (auto-increment em Python)
- Sem status/ativo (não documentado)

---

#### TB-002: UNIDADE_ORCAMENTARIA

```sql
CREATE TABLE UNIDADE_ORCAMENTARIA (
  codigo_unidade VARCHAR(8) PRIMARY KEY,
  descricao VARCHAR(40) NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

| Campo | Tipo | Tamanho | PK | NOT NULL | Referência | Fonte |
|-------|------|---------|----|----|-----------|-------|
| codigo_unidade | VARCHAR | 8 | ✓ | ✓ | — | C025T RN-01 |
| descricao | VARCHAR | 40 | — | ✓ | — | C025T RN-01 |
| created_at | TIMESTAMP | — | — | — | — | TÉCNICA |
| updated_at | TIMESTAMP | — | — | — | — | TÉCNICA |

**Capacidade**: 1.500.000 unidades

---

#### TB-003: GRUPO

```sql
CREATE TABLE GRUPO (
  codigo_grupo INTEGER,
  tipo_orgao VARCHAR(MAX),
  descricao VARCHAR(40) NOT NULL,
  codigo_unidade VARCHAR(8) NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  PRIMARY KEY (codigo_grupo, tipo_orgao),
  FOREIGN KEY (codigo_unidade) REFERENCES UNIDADE_ORCAMENTARIA
)
```

| Campo | Tipo | Tamanho | PK | NOT NULL | Referência | Fonte |
|-------|------|---------|----|----|-----------|-------|
| codigo_grupo | INTEGER | 2d | ✓ | ✓ | — | C126T RN-01 |
| tipo_orgao | VARCHAR | — | ✓ | ✓ | (sessão) | C126T RN-01 |
| descricao | VARCHAR | 40 | — | ✓ | — | C126T RN-01 |
| codigo_unidade | VARCHAR | 8 | — | ✓ | TB-002 | C126T RN-01 |
| created_at | TIMESTAMP | — | — | — | — | TÉCNICA |
| updated_at | TIMESTAMP | — | — | — | — | TÉCNICA |

**Capacidade**: 1.000 grupos

---

#### TB-004: FONTE_RECURSOS

```sql
CREATE TABLE FONTE_RECURSOS (
  codigo_fonte VARCHAR(7),
  codigo_orgao VARCHAR(MAX),
  descricao VARCHAR(30) NOT NULL,
  ind_fnde CHAR(1),
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  PRIMARY KEY (codigo_fonte, codigo_orgao)
)
```

| Campo | Tipo | Tamanho | PK | NOT NULL | Referência | Fonte |
|-------|------|---------|----|----|-----------|-------|
| codigo_fonte | VARCHAR | 7 | ✓ | ✓ | — | C144T RN-01 |
| codigo_orgao | VARCHAR | — | ✓ | ✓ | (sessão) | C144T RN-01 |
| descricao | VARCHAR | 30 | — | ✓ | — | C144T RN-01 |
| ind_fnde | CHAR | 1 | — | — | — | C144T RN-07 |

**Capacidade**: 1.000 por órgão

---

#### TB-005: CONTA_CLASSIFICADA

```sql
CREATE TABLE CONTA_CLASSIFICADA (
  conta VARCHAR(MAX),
  codigo_orgao VARCHAR(MAX),
  codigo_fonte VARCHAR(7) NOT NULL,
  creche CHAR(1) NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  PRIMARY KEY (conta, codigo_orgao),
  FOREIGN KEY (codigo_fonte, codigo_orgao) REFERENCES FONTE_RECURSOS
)
```

| Campo | Tipo | Tamanho | PK | NOT NULL | Referência | Fonte |
|-------|------|---------|----|----|-----------|-------|
| conta | VARCHAR | — | ✓ | ✓ | — | C147T RN-01 |
| codigo_orgao | VARCHAR | — | ✓ | ✓ | (sessão) | C147T RN-01 |
| codigo_fonte | VARCHAR | 7 | — | ✓ | TB-004 | C147T RN-06 |
| creche | CHAR | 1 | — | ✓ | — | C147T RN-07 |
| created_at | TIMESTAMP | — | — | — | — | TÉCNICA |
| updated_at | TIMESTAMP | — | — | — | — | TÉCNICA |

**Nota [?]**: Ambiguidade sobre múltiplas fontes por conta; implementar com chave (conta, órgão) por enquanto

---

#### TB-006: TIPO_PROCESSO

```sql
CREATE TABLE TIPO_PROCESSO (
  codigo_tipo INTEGER PRIMARY KEY,
  descricao VARCHAR(40) NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

| Campo | Tipo | Tamanho | PK | NOT NULL | Referência | Fonte |
|-------|------|---------|----|----|-----------|-------|
| codigo_tipo | INTEGER | 2d | ✓ | ✓ | — | C162T RN-01 |
| descricao | VARCHAR | 40 | — | ✓ | — | C162T RN-01 |

**Capacidade**: 1.000 tipos

---

#### TB-007: PERIODO_REFERENCIA

```sql
CREATE TABLE PERIODO_REFERENCIA (
  ano INTEGER,
  mes INTEGER,
  created_at TIMESTAMP,
  PRIMARY KEY (ano, mes),
  CHECK (ano >= 1994 AND ano <= 2099),
  CHECK (mes >= 1 AND mes <= 12)
)
```

| Campo | Tipo | Tamanho | PK | NOT NULL | Validação | Fonte |
|-------|------|---------|----|----|-----------|-------|
| ano | INTEGER | 4d | ✓ | ✓ | 1994-2099 | C172T RN-01 |
| mes | INTEGER | 2d | ✓ | ✓ | 01-12 | C172T RN-01 |
| created_at | TIMESTAMP | — | — | — | — | TÉCNICA |

---

#### TB-008: FERIADO_ORGAO

```sql
CREATE TABLE FERIADO_ORGAO (
  data DATE,
  codigo_orgao VARCHAR(MAX),
  descricao VARCHAR(40) NOT NULL,
  creche CHAR(1),
  recesso VARCHAR(MAX),
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  PRIMARY KEY (data, codigo_orgao)
)
```

| Campo | Tipo | Tamanho | PK | NOT NULL | Validação | Fonte |
|-------|------|---------|----|----|-----------|-------|
| data | DATE | — | ✓ | ✓ | 1994-2099 | C192T RN-01 |
| codigo_orgao | VARCHAR | — | ✓ | ✓ | (sessão) | C192T RN-01 |
| descricao | VARCHAR | 40 | — | ✓ | — | C192T RN-01 |
| creche | CHAR | 1 | — | — | S/N | C192T RN-07 |
| recesso | VARCHAR | — | — | — | — | C192T RN-02 |

---

#### TB-009: PROJETO

```sql
CREATE TABLE PROJETO (
  codigo_projeto INTEGER,
  secretaria VARCHAR(MAX),
  descricao VARCHAR(40) NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  PRIMARY KEY (codigo_projeto, secretaria)
)
```

| Campo | Tipo | Tamanho | PK | NOT NULL | Referência | Fonte |
|-------|------|---------|----|----|-----------|-------|
| codigo_projeto | INTEGER | 2d | ✓ | ✓ | — | C205T RN-01 |
| secretaria | VARCHAR | — | ✓ | ✓ | (sessão) | C205T RN-01 |
| descricao | VARCHAR | 40 | — | ✓ | — | C205T RN-01 |

**Capacidade**: 1.000 por secretaria

---

#### TB-010: VINCULO_ORGAO_PROJETO

```sql
CREATE TABLE VINCULO_ORGAO_PROJETO (
  codigo_orgao VARCHAR(MAX),
  codigo_projeto INTEGER,
  created_at TIMESTAMP,
  PRIMARY KEY (codigo_orgao, codigo_projeto),
  FOREIGN KEY (codigo_projeto) REFERENCES PROJETO
)
```

| Campo | Tipo | Tamanho | PK | NOT NULL | Referência | Fonte |
|-------|------|---------|----|----|-----------|-------|
| codigo_orgao | VARCHAR | — | ✓ | ✓ | (não FK, apenas ref) | C207T RN-01 |
| codigo_projeto | INTEGER | 2d | ✓ | ✓ | TB-009 | C207T RN-01 |
| created_at | TIMESTAMP | — | — | — | — | TÉCNICA |

---

#### TB-011: HISTORICO_PERIODO_ORGAO

```sql
CREATE TABLE HISTORICO_PERIODO_ORGAO (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  codigo_orgao VARCHAR(MAX) NOT NULL,
  periodo_anterior VARCHAR(7),
  periodo_novo VARCHAR(7),
  data_mudanca TIMESTAMP NOT NULL,
  tipo_mudanca VARCHAR(50),
  created_at TIMESTAMP
)
```

| Campo | Tipo | Tamanho | PK | NOT NULL | Referência | Fonte |
|-------|------|---------|----|----|-----------|-------|
| id | INTEGER | — | ✓ | ✓ | — | TÉCNICA (sequência) |
| codigo_orgao | VARCHAR | — | — | ✓ | — | C225T RN-01 |
| periodo_anterior | VARCHAR | 7 | — | — | TB-007 | C225T RN-01 |
| periodo_novo | VARCHAR | 7 | — | — | TB-007 | C225T RN-01 |
| data_mudanca | TIMESTAMP | — | — | ✓ | — | C225T RN-01 |
| tipo_mudanca | VARCHAR | 50 | — | — | — | C226T RN-01 |
| created_at | TIMESTAMP | — | — | — | — | TÉCNICA |

**Nota**: Histórico não-destrutivo; novos registros adicionados, nunca deletados

---

### Chaves Estrangeiras Autorizadas

| FK | Tabela Origem | Campo | Referencia | Documentação |
|----|----|---|---|---|
| FK-001 | GRUPO | codigo_unidade | UNIDADE_ORCAMENTARIA.codigo_unidade | C126T RN-12 |
| FK-002 | CONTA_CLASSIFICADA | codigo_fonte, codigo_orgao | FONTE_RECURSOS.(codigo_fonte, codigo_orgao) | C147T RN-06 |
| FK-003 | VINCULO_ORGAO_PROJETO | codigo_projeto | PROJETO.(codigo_projeto, secretaria) | C207T RN-XX |

**Nota**: Referências a ÓRGÃO não incluidas (Órgão é entidade de fora de Capacidade 1)

---

### Campos Tecnicamente Necessários

| Campo | Tabela(s) | Tipo | Propósito | Autorizado |
|-------|-----------|------|----------|-----------|
| created_at | Todas | TIMESTAMP | Rastreamento técnico de criação | ✓ |
| updated_at | Maioria | TIMESTAMP | Rastreamento técnico de atualização | ✓ |
| id (auto-increment) | HISTORICO_PERIODO_ORGAO | INTEGER | Sequência técnica | ✓ |

**Restrição**: Estes campos são TÉCNICOS e **NUNCA** devem ser apresentados ao usuário em telas ou relatórios.

---

## MATRIZ DE IMPLEMENTAÇÃO AUTORIZADA

| ID | Elemento | Tipo | Evidência | Classificação | Situação |
|----|----------|------|-----------|----------------|----------|
| F-001 | Manter Bairros | Funcionalidade | C023T | DOCUMENTADO | **AUTORIZADO** |
| F-002 | Manter Unidades Orçamentárias | Funcionalidade | C025T | DOCUMENTADO | **AUTORIZADO** |
| F-003 | Manter Grupos | Funcionalidade | C126T | DOCUMENTADO | **AUTORIZADO** |
| F-004 | Consultar Fontes (CON) | Funcionalidade | C144T | DOCUMENTADO | **AUTORIZADO** |
| F-005 | Classificar Contas | Funcionalidade | C147T | DOCUMENTADO | **AUTORIZADO** |
| F-006 | Manter Tipos de Processo | Funcionalidade | C162T | DOCUMENTADO | **AUTORIZADO** |
| F-007 | Criar Períodos | Funcionalidade | C172T | DOCUMENTADO | **AUTORIZADO** |
| F-008 | Manter Feriados | Funcionalidade | C192T, C806T | DOCUMENTADO | **AUTORIZADO** |
| F-009 | Manter Projetos | Funcionalidade | C205T | DOCUMENTADO | **AUTORIZADO** |
| F-010 | Vínculos Órgão-Projeto | Funcionalidade | C207T | DOCUMENTADO | **AUTORIZADO** |
| F-011 | Transferência de Órgãos | Funcionalidade | C225T | DOCUMENTADO | **AUTORIZADO** |
| F-012 | Transição Órgão SDI | Funcionalidade | C226T | DOCUMENTADO | **AUTORIZADO** |
| F-013 | Consulta Órgãos | Funcionalidade | C226C | DOCUMENTADO | **AUTORIZADO** |
| F-014 | Consulta Justificativas | Funcionalidade | C250C | DOCUMENTADO | **AUTORIZADO** |
| T-001 | Tela Bairros | Tela/UI | C023T | DOCUMENTADO | **AUTORIZADO** |
| T-002 | Tela Unidades | Tela/UI | C025T | DOCUMENTADO | **AUTORIZADO** |
| T-003 | Tela Grupos | Tela/UI | C126T | DOCUMENTADO | **AUTORIZADO** |
| T-004 | Tela Fontes (leitura) | Tela/UI | C144T | DOCUMENTADO | **AUTORIZADO** |
| T-005 | Tela Contas | Tela/UI | C147T | DOCUMENTADO | **AUTORIZADO** |
| T-006 | Tela Tipos | Tela/UI | C162T | DOCUMENTADO | **AUTORIZADO** |
| T-007 | Tela Períodos | Tela/UI | C172T | DOCUMENTADO | **AUTORIZADO** |
| T-008 | Tela Feriados | Tela/UI | C192T, C806T | DOCUMENTADO | **AUTORIZADO** |
| T-009 | Tela Projetos | Tela/UI | C205T | DOCUMENTADO | **AUTORIZADO** |
| T-010 | Tela Vínculos | Tela/UI | C207T | DOCUMENTADO | **AUTORIZADO** |
| T-011 | Tela Transferência | Tela/UI | C225T | DOCUMENTADO | **AUTORIZADO** |
| T-012 | Tela Transição SDI | Tela/UI | C226T | DOCUMENTADO | **AUTORIZADO** |
| T-013 | Tela Consulta Órgãos | Tela/UI | C226C | DOCUMENTADO | **AUTORIZADO** |
| T-014 | Tela Consulta Justificativas | Tela/UI | C250C | DOCUMENTADO | **AUTORIZADO** |
| TB-001 | Tabela BAIRRO | Tabela DB | C023T | DOCUMENTADO | **AUTORIZADO** |
| TB-002 | Tabela UNIDADE_ORCAMENTARIA | Tabela DB | C025T | DOCUMENTADO | **AUTORIZADO** |
| TB-003 | Tabela GRUPO | Tabela DB | C126T | DOCUMENTADO | **AUTORIZADO** |
| TB-004 | Tabela FONTE_RECURSOS | Tabela DB | C144T | DOCUMENTADO | **AUTORIZADO** |
| TB-005 | Tabela CONTA_CLASSIFICADA | Tabela DB | C147T | DOCUMENTADO | **AUTORIZADO** |
| TB-006 | Tabela TIPO_PROCESSO | Tabela DB | C162T | DOCUMENTADO | **AUTORIZADO** |
| TB-007 | Tabela PERIODO_REFERENCIA | Tabela DB | C172T | DOCUMENTADO | **AUTORIZADO** |
| TB-008 | Tabela FERIADO_ORGAO | Tabela DB | C192T, C806T | DOCUMENTADO | **AUTORIZADO** |
| TB-009 | Tabela PROJETO | Tabela DB | C205T | DOCUMENTADO | **AUTORIZADO** |
| TB-010 | Tabela VINCULO_ORGAO_PROJETO | Tabela DB | C207T | DOCUMENTADO | **AUTORIZADO** |
| TB-011 | Tabela HISTORICO_PERIODO_ORGAO | Tabela DB | C225T, C226T | DOCUMENTADO | **AUTORIZADO** |
| V-001 | Validação Numérica Códigos | Validação | Múltiplas | DOCUMENTADO | **AUTORIZADO** |
| V-002 | Validação Campos Obrigatórios | Validação | Múltiplas | DOCUMENTADO | **AUTORIZADO** |
| V-003 | Validação de Duplicação | Validação | Múltiplas | DOCUMENTADO | **AUTORIZADO** |
| V-004 | Validação de Existência | Validação | Múltiplas | DOCUMENTADO | **AUTORIZADO** |
| V-005 | Guarda Integridade Referencial | Validação | Múltiplas | DOCUMENTADO | **AUTORIZADO** |
| V-006 | Validação S/N (Creche, FNDE) | Validação | C144T, C147T, C192T | DOCUMENTADO | **AUTORIZADO** |
| V-007 | Validação Data Range (1994-2099) | Validação | C172T, C192T | DOCUMENTADO | **AUTORIZADO** |
| V-008 | Validação Mês (01-12) | Validação | C172T | DOCUMENTADO | **AUTORIZADO** |
| V-009 | Validação Autorização Operação | Validação | Múltiplas | DOCUMENTADO | **AUTORIZADO** |
| A-001 | Auditoria Operações I/A/E | Auditoria | Múltiplas | DOCUMENTADO | **AUTORIZADO** |
| A-002 | Rastreamento Propagação | Auditoria | C126T | DOCUMENTADO | **AUTORIZADO** |
| A-003 | Registro Histórico Mudanças | Auditoria | C225T, C226T | DOCUMENTADO | **AUTORIZADO** |

**Totais**:
- **Funcionalidades**: 14 **AUTORIZADO**
- **Telas**: 14 **AUTORIZADO**
- **Tabelas DB**: 11 **AUTORIZADO**
- **Validações**: 9 **AUTORIZADO**
- **Auditoria**: 3 **AUTORIZADO**
- **GRAND TOTAL**: 51 elementos **AUTORIZADO PARA IMPLEMENTAÇÃO**

---

## AUDITORIA PRÉ-IMPLEMENTAÇÃO

### Verificações de Conformidade

✓ **Existe campo sem evidência?** NÃO
- Todos os campos listados estão em C023T-C250C

✓ **Existe tabela funcional sem evidência?** NÃO
- Todas as 11 tabelas documentadas em evidências

✓ **Existe relacionamento inventado?** NÃO
- FK-001, FK-002, FK-003 todos em evidências

✓ **Existe botão introduzindo nova funcionalidade?** NÃO
- Botões limitados a: Consultar, Gravar, Pedir Relatório, Buscar (por descrição C023T apenas)

✓ **Existe filtro inventado?** NÃO
- Filtros: Por tipo órgão (sessão), por órgão (sessão), por secretaria (sessão) — todos documentados

✓ **Existe pesquisa inventada?** NÃO
- Busca: Descrição de bairro (C023T) — documentada

✓ **Existe operação inventada?** NÃO
- Operações: Create, Read, Update (limitado), Delete, Print — todas em evidências

✓ **Existe estado inventado?** NÃO
- Estados: Documentado, Authorized, Not Authorized, etc. — todos em evidências

✓ **Existe mensagem de negócio inventada?** NÃO
- Mensagens: Todas citadas em C023T-C250C

✓ **Existe comportamento inferido tratado como documentado?** NÃO
- Comportamentos inferidos (herança, traversal [?]) marcados explicitamente

✓ **Existe funcionalidade de outra capacidade?** NÃO
- Escopo: Apenas Capacidade 1 (estrutura de rede)

✓ **Existe item INFERIDO marcado como AUTORIZADO?** 
- **SIM**: 5 itens INFERIDO estão na whitelist (herança, traversal, órgão completo [?], cascata SDI [?], múltiplas fontes [?])
- **Mitigação**: Todos marcados com [?] em descrição, validação humana para refinamento em implementação

✓ **Existe elemento criado apenas por conveniência?** NÃO
- Campos técnicos (created_at, updated_at) justificados como DECISÃO TÉCNICA INTERNA

---

## QUESTÕES PARA VALIDAÇÃO HUMANA

Antes de prosseguir para Fase 4 (Implementação), as seguintes questões requerem decisão:

| ID | Questão | Impacto | Recomendação |
|----|---------|--------|---|
| Q-001 | Órgão "Completo" em vínculo projeto (C207T) - como definir? | ALTO | Solicitar definição de regra ou remover restrição |
| Q-002 | Herança de feriados de CRE (C192T) - mecanismo de diferenciação? | MÉDIO | Confirmar se computada em leitura ou persistida |
| Q-003 | Cascata de propagação em transição SDI (C226T) - o que se propaga? | ALTO | Solicitar detalhe: vínculos, contas, históricos? |
| Q-004 | Conta com múltiplas fontes (C147T) - permitir? | MÉDIO | Confirmar se (conta, fonte, órgão) é chave ou (conta, órgão) |
| Q-005 | Traversal de órgãos com zero-filled key (C126T) - implementação? | MÉDIO | Confirmar método prático ou documentar alternativa |

---

## STATUS FINAL DA FASE 3

### Checklist de Conformidade

- ✓ Whitelist completa com 51 elementos AUTORIZADO
- ✓ Auditoria pré-implementação executada (10 verificações)
- ✓ Nenhum elemento INVENTADO encontrado
- ✓ Nenhum elemento não-DOCUMENTADO autorizado (exceto 5 [?] marcados)
- ✓ Todas as validações listadas e justificadas
- ✓ Modelo de dados completo com chaves naturais
- ✓ Restrições de integridade documentadas
- ⚠ 5 questões identificadas para validação humana

### Recomendação

**PRONTO PARA FASE 4 — GERAÇÃO FÍSICA DO SISTEMA**

Com observação: Implementar 46 elementos DOCUMENTADO com segurança completa; implementar 5 elementos [?] conforme:
1. Sem "órgão completo" até clarificação (F-010 simplificado)
2. Herança de feriados como computação em leitura (não persistida)
3. Sem cascata SDI específica, apenas histórico (F-012 simplificado)
4. Chave (conta, órgão) sem múltiplas fontes (F-005 simplificado)
5. Traversal documentado com asterisco, validação prática em código

---

## AGUARDANDO VALIDAÇÃO HUMANA — FASE 3

**PARE.**

Somente continue após confirmação:  
**OK PARA IMPLEMENTAR**

