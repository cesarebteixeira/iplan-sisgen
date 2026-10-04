# PROMPT MESTRE — RECONSTRUÇÃO FUNCIONAL EAE/COBOL PARA SISTEMA WEB

## Versão 2.1

======================================================================
1. OBJETIVO
======================================================================

Este Prompt Mestre controla a reconstrução progressiva de um sistema legado
desenvolvido utilizando EAE/COBOL Unisys para uma aplicação Web.

A aplicação deverá utilizar:

- Sistema operacional alvo: Windows 11
- Backend: Python
- Banco de dados: SQLite
- Interface: Web

IMPORTANTE:

Este prompt NÃO tem como finalidade apenas analisar ou documentar o sistema.

Após as fases obrigatórias de análise e validação humana, sua finalidade é
GERAR FISICAMENTE UMA APLICAÇÃO WEB EXECUTÁVEL.

A construção deverá ocorrer capacidade por capacidade.

O objetivo NÃO é realizar tradução sintática:

COBOL → Python

O objetivo é reconstruir funcionalidades comprovadamente identificadas nas
evidências extraídas anteriormente do sistema legado.


======================================================================
2. CONTEXTO DAS EVIDÊNCIAS
======================================================================

Em etapa anterior, programas/fontes COBOL/EAE foram analisados.

Como resultado dessa análise foram produzidos arquivos de evidência contendo,
entre outras informações:

- regras de negócio;
- critérios de aceite;
- funcionalidades;
- dados;
- relacionamentos;
- validações;
- cálculos;
- operações;
- fluxos;
- comportamentos identificados.

Esses arquivos NÃO são programas COBOL.

Eles representam conhecimento funcional anteriormente extraído do sistema
legado.

Neste experimento, esses arquivos constituem a base documental para a
reconstrução do sistema.


======================================================================
3. ARQUIVO MESTRE DE CAPACIDADES
======================================================================

Utilize como índice mestre:

C:\projetos\capacidades.md

Esse arquivo possui duas funções:

1. identificar quais evidências pertencem a cada capacidade;
2. definir a ordem em que as capacidades deverão ser construídas.

A ordem atualmente identificada é:

1 → 2 → 3 → 12 → 5 → 9 → 4 → 6 → 7 → 8 → 10 → 11

Entretanto:

A FONTE DE VERDADE PARA A ORDEM É:

C:\projetos\capacidades.md

Caso exista divergência entre a sequência escrita neste prompt e a sequência
existente em capacidades.md, PREVALECE capacidades.md.

NUNCA determine a próxima capacidade utilizando:

CAPACIDADE ATUAL + 1


======================================================================
4. COMANDO PARA INICIAR UMA CAPACIDADE
======================================================================

Uma capacidade somente poderá ser iniciada por comando humano explícito:

GERE CAPACIDADE X

Exemplo:

GERE CAPACIDADE 1

Ao receber esse comando:

1. consulte capacidades.md;
2. confirme que a capacidade existe;
3. verifique sua posição na ordem definida;
4. verifique se a solicitação é compatível com o estado atual do projeto;
5. inicie exclusivamente a FASE 1 dessa capacidade.

NÃO inicie outra capacidade automaticamente.


======================================================================
5. CAPACIDADE INICIAL
======================================================================

Na primeira execução deverá ser utilizada:

Capacidade 1 — Estrutura da rede e do gasto

Somente uma capacidade poderá estar em construção por vez.


======================================================================
6. REGRA DE OURO — FONTE DE VERDADE
======================================================================

Os arquivos de evidência associados à capacidade atualmente em desenvolvimento
são a ÚNICA FONTE AUTORIZADA para determinar requisitos funcionais.

Utilize-os para identificar:

- regras de negócio;
- critérios de aceite;
- funcionalidades;
- entidades;
- dados;
- campos;
- relacionamentos;
- validações;
- cálculos;
- operações;
- fluxos;
- estados;
- comportamentos.

SOMENTE IMPLEMENTE O QUE ESTIVER SUSTENTADO PELAS EVIDÊNCIAS.

NÃO INVENTE.


======================================================================
7. FONTES NÃO AUTORIZADAS
======================================================================

NÃO utilize conhecimento externo para completar requisitos ausentes.

NÃO pesquise na Internet para descobrir como o sistema deveria funcionar.

NÃO utilize convenções de outros sistemas como requisitos.

NÃO utilize conhecimento geral do domínio para preencher lacunas.

NÃO utilize telas originais do sistema legado como fonte para reconstrução.

NÃO solicite telas originais para descobrir requisitos ausentes.

NÃO tente reproduzir visualmente o sistema legado.

As telas originais poderão ser utilizadas EXTERNAMENTE pelos humanos para
validar o resultado produzido.

Elas NÃO constituem fonte de entrada deste processo.


======================================================================
8. REGRA ABSOLUTA — NÃO INVENTAR
======================================================================

É PROIBIDO inventar, completar, presumir ou deduzir silenciosamente requisitos
não existentes nas evidências.

Não crie sem evidência:

- regras;
- critérios;
- campos;
- atributos;
- entidades;
- relacionamentos;
- validações;
- cálculos;
- estados;
- operações;
- permissões;
- exceções;
- mensagens de negócio;
- filtros;
- pesquisas;
- funcionalidades;
- comportamentos;
- dados complementares.

O fato de algo parecer:

- útil;
- óbvio;
- necessário;
- intuitivo;
- comum em aplicações Web;
- uma boa prática;
- conveniente tecnicamente;

NÃO constitui evidência.

Quando não existir sustentação documental, registre:

INFORMAÇÃO NÃO IDENTIFICADA NAS EVIDÊNCIAS


======================================================================
9. REGRA ESPECIAL — INTERFACE WEB
======================================================================

A aplicação será Web.

Existe liberdade para decisões VISUAIS e TÉCNICAS, mas NÃO para decisões
FUNCIONAIS.

É permitido decidir, por exemplo:

- HTML;
- CSS;
- disposição visual;
- espaçamento;
- tipografia;
- estrutura visual;
- organização técnica dos templates.

Essas decisões não podem alterar a semântica funcional.

É PROIBIDO criar arbitrariamente:

- campos;
- botões com novas funcionalidades;
- menus funcionais;
- filtros;
- pesquisas;
- dashboards;
- abas funcionais;
- ações;
- estados;
- mensagens de negócio;
- informações adicionais;
- funcionalidades auxiliares.

"É comum em aplicações Web" NÃO é evidência.


======================================================================
10. CONTROLES MÍNIMOS DE INTERFACE
======================================================================

Quando uma funcionalidade estiver DOCUMENTADA, poderá ser criado o controle
visual mínimo necessário para permitir sua utilização na aplicação Web.

Exemplo:

Se a evidência comprovar explicitamente uma operação de inclusão, poderá ser
criado um controle Web que permita executar essa inclusão.

Esse controle:

- não cria nova regra;
- não cria nova funcionalidade;
- apenas disponibiliza a funcionalidade documentada.

Sempre que possível, utilize a terminologia existente nas evidências.

A criação do componente visual deverá permanecer rastreável à funcionalidade
documentada.


======================================================================
11. CLASSIFICAÇÃO OBRIGATÓRIA
======================================================================

Cada informação funcional encontrada deverá receber uma das classificações:

DOCUMENTADO

Existe sustentação explícita nas evidências.

INFERIDO

A evidência sugere a informação, mas sua conclusão exige interpretação.

NÃO IDENTIFICADO

Não existe evidência suficiente.

REGRA:

DOCUMENTADO poderá ser proposto para implementação.

INFERIDO não poderá ser implementado automaticamente.

NÃO IDENTIFICADO não poderá ser implementado automaticamente.


======================================================================
12. RASTREABILIDADE
======================================================================

Mantenha rastreabilidade, sempre que aplicável, utilizando:

ARQUIVO DE EVIDÊNCIA
        ↓
REGRA DE NEGÓCIO
        ↓
CRITÉRIO DE ACEITE
        ↓
FUNCIONALIDADE
        ↓
TELA/OPERAÇÃO
        ↓
CAMPO/AÇÃO/ELEMENTO
        ↓
CÓDIGO
        ↓
TESTE

Nenhuma funcionalidade deverá aparecer no código sem origem identificável.


======================================================================
13. ISOLAMENTO ENTRE CAPACIDADES
======================================================================

Trabalhe exclusivamente na capacidade atual.

Enquanto ela não receber:

CAPACIDADE APROVADA

é PROIBIDO:

- iniciar outra capacidade;
- analisar evidências de capacidade futura;
- antecipar funcionalidade futura;
- utilizar evidências futuras;
- misturar requisitos entre capacidades.

Se uma informação aparentemente necessária pertencer a outra capacidade,
registre:

DEPENDÊNCIA DE CAPACIDADE FUTURA

Não implemente antecipadamente.


======================================================================
14. FLUXO OBRIGATÓRIO DA CAPACIDADE
======================================================================

Toda capacidade deverá seguir:

FASE 1 — IDENTIFICAÇÃO DAS EVIDÊNCIAS
        ↓
VALIDAÇÃO HUMANA
        ↓
OK
        ↓
FASE 2 — ANÁLISE FUNCIONAL
        ↓
VALIDAÇÃO HUMANA
        ↓
OK
        ↓
FASE 3 — CONTRATO DE IMPLEMENTAÇÃO
        ↓
VALIDAÇÃO HUMANA
        ↓
OK PARA IMPLEMENTAR
        ↓
FASE 4 — GERAÇÃO FÍSICA DO SISTEMA
        ↓
AUDITORIA
        ↓
VALIDAÇÃO HUMANA DO SISTEMA EXECUTADO
        ↓
CORREÇÃO, SE NECESSÁRIA
        ↓
NOVA VALIDAÇÃO HUMANA
        ↓
REPETIR ATÉ:
        ↓
CAPACIDADE APROVADA
        ↓
PARAR
        ↓
AGUARDAR:
GERE CAPACIDADE X


======================================================================
15. FASE 1 — IDENTIFICAÇÃO DAS EVIDÊNCIAS
======================================================================

Ao receber:

GERE CAPACIDADE X

leia:

C:\projetos\capacidades.md

Identifique exclusivamente os arquivos pertencentes à capacidade solicitada.

Verifique fisicamente a existência desses arquivos.

NÃO leia evidências pertencentes a outras capacidades.

NÃO realize implementação.

NÃO gere código.

NÃO altere arquivos do sistema.


======================================================================
16. SAÍDA DA FASE 1
======================================================================

Apresente:

CAPACIDADE EM PROCESSAMENTO

- número;
- nome.

ARQUIVOS DE EVIDÊNCIA

Para cada arquivo:

- número sequencial;
- nome;
- caminho;
- referência encontrada em capacidades.md;
- situação física: ENCONTRADO / NÃO ENCONTRADO.

Apresente:

Total de arquivos referenciados: X
Total encontrados: X
Total não encontrados: X

Identifique também:

- referências ambíguas;
- arquivos ausentes;
- inconsistências.

Depois apresente:

AGUARDANDO VALIDAÇÃO HUMANA — FASE 1

PARE.

Somente continue após:

OK


======================================================================
17. FASE 2 — ANÁLISE FUNCIONAL
======================================================================

Após o OK da FASE 1:

Leia integralmente TODOS os arquivos de evidência aprovados da capacidade.

Extraia exclusivamente o que estiver sustentado pelos documentos.

Identifique:

- regras de negócio;
- critérios de aceite;
- funcionalidades;
- entidades;
- campos;
- dados;
- relacionamentos;
- validações;
- cálculos;
- operações;
- fluxos;
- estados;
- mensagens;
- dependências;
- lacunas;
- ambiguidades.

Classifique cada informação como:

DOCUMENTADO
INFERIDO
NÃO IDENTIFICADO


======================================================================
18. SAÍDA DA FASE 2
======================================================================

Apresente:

REGRAS DE NEGÓCIO

CRITÉRIOS DE ACEITE

FUNCIONALIDADES

ENTIDADES E DADOS

RELACIONAMENTOS

VALIDAÇÕES

CÁLCULOS

OPERAÇÕES

FLUXOS

ESTADOS

DEPENDÊNCIAS

LACUNAS

AMBIGUIDADES

ITENS INFERIDOS

ITENS NÃO IDENTIFICADOS

Para cada elemento relevante informe sua evidência de origem.

Depois apresente:

AGUARDANDO VALIDAÇÃO HUMANA — FASE 2

PARE.

Somente continue após:

OK


======================================================================
19. FASE 3 — CONTRATO DE IMPLEMENTAÇÃO
======================================================================

Após o OK da FASE 2:

NÃO programe imediatamente.

Primeiro produza:

CONTRATO DE IMPLEMENTAÇÃO DA CAPACIDADE

Esse contrato funcionará como uma WHITELIST.

Somente o que estiver explicitamente autorizado nesse contrato poderá chegar
ao código.


======================================================================
20. FUNCIONALIDADES AUTORIZADAS
======================================================================

Para cada funcionalidade informe:

- identificador;
- descrição;
- RN relacionada;
- CA relacionado;
- arquivo de evidência;
- classificação;
- situação para implementação.


======================================================================
21. INTERFACE AUTORIZADA
======================================================================

Identifique as telas ou visões Web necessárias para disponibilizar as
funcionalidades DOCUMENTADAS.

Para cada uma informe:

- identificador;
- finalidade;
- funcionalidade relacionada;
- evidência.

Para cada elemento funcional da interface informe:

- tela;
- elemento;
- tipo;
- finalidade;
- funcionalidade que o justifica;
- evidência;
- classificação.

Nenhum campo ou ação poderá existir apenas para "melhorar a tela".


======================================================================
22. MODELO DE DADOS AUTORIZADO
======================================================================

Antes de criar SQLite, apresente:

- entidades;
- tabelas;
- campos;
- tipos necessários;
- chaves documentadas;
- relacionamentos documentados;
- evidência de origem.

NÃO crie automaticamente campos como:

created_at
updated_at
status
ativo
observacao
descricao

apenas porque são comuns em aplicações.

Se a evidência possuir chave natural, preserve-a sempre que tecnicamente
adequado.

Se uma chave técnica interna for indispensável ao mecanismo utilizado,
classifique-a como:

DECISÃO TÉCNICA INTERNA

Ela:

- não deverá criar comportamento funcional;
- não deverá ser apresentada ao usuário;
- não deverá substituir a chave funcional documentada;
- deverá ser registrada no contrato.


======================================================================
23. MATRIZ DE IMPLEMENTAÇÃO AUTORIZADA
======================================================================

Crie obrigatoriamente:

| ID | Elemento | Tipo | Evidência | Classificação | Situação |

Situações:

AUTORIZADO
NÃO AUTORIZADO
AGUARDANDO VALIDAÇÃO

Regras:

DOCUMENTADO
→ poderá ser AUTORIZADO.

INFERIDO
→ AGUARDANDO VALIDAÇÃO.

NÃO IDENTIFICADO
→ NÃO AUTORIZADO.

Somente:

AUTORIZADO

poderá ser implementado.


======================================================================
24. AUDITORIA PRÉ-IMPLEMENTAÇÃO
======================================================================

Antes de solicitar autorização para programar, verifique:

Existe campo sem evidência?

Existe tabela funcional sem evidência?

Existe relacionamento inventado?

Existe botão introduzindo nova funcionalidade?

Existe filtro inventado?

Existe pesquisa inventada?

Existe operação inventada?

Existe estado inventado?

Existe mensagem de negócio inventada?

Existe comportamento inferido tratado como documentado?

Existe funcionalidade de outra capacidade?

Existe item INFERIDO marcado como AUTORIZADO?

Existe elemento criado apenas por conveniência?

Se SIM:

NÃO autorize esse elemento.

Registre-o para decisão humana.


======================================================================
25. PARADA DA FASE 3
======================================================================

Apresente:

CONTRATO DE IMPLEMENTAÇÃO CONCLUÍDO

AGUARDANDO VALIDAÇÃO HUMANA — FASE 3

Nenhum código referente à capacidade deverá ser criado antes da autorização.

PARE.

Somente continue após:

OK PARA IMPLEMENTAR


======================================================================
26. FASE 4 — GERAÇÃO FÍSICA DO SISTEMA
======================================================================

Após receber exatamente:

OK PARA IMPLEMENTAR

INICIE A IMPLEMENTAÇÃO FÍSICA.

IMPORTANTE:

NÃO apenas apresente exemplos de código.

NÃO apenas descreva como implementar.

NÃO apenas produza documentação.

CRIE E ALTERE FISICAMENTE OS ARQUIVOS DO PROJETO.

O resultado deverá ser uma aplicação executável no Windows 11.


======================================================================
27. TECNOLOGIAS
======================================================================

Utilize:

Sistema operacional alvo:
Windows 11

Backend:
Python

Banco:
SQLite

Interface:
Web

Priorize dependências simples e adequadas ao experimento.

Não introduza infraestrutura desnecessária.


======================================================================
28. IMPLEMENTAÇÃO
======================================================================

Implemente todos os itens:

AUTORIZADO

da Matriz de Implementação Autorizada.

Quando documentado e autorizado, implemente:

- estrutura da aplicação;
- backend Python;
- SQLite;
- tabelas;
- campos;
- relacionamentos;
- regras de negócio;
- critérios de aceite;
- validações;
- cálculos;
- operações;
- interface Web;
- telas;
- controles necessários;
- navegação necessária;
- mensagens documentadas.

A aplicação deverá ser realmente executável.


======================================================================
29. WINDOWS 11
======================================================================

Todos os comandos e instruções de execução deverão ser compatíveis com
Windows 11.

Quando apresentar comandos de terminal, priorize PowerShell.

Utilize caminhos compatíveis com Windows.

Não presuma:

Linux
bash
apt
sudo

Não exija Docker para executar a aplicação, salvo se houver autorização
humana explícita.

A aplicação deverá possuir instruções suficientes para execução local em
Windows 11.


======================================================================
30. DECISÕES TÉCNICAS
======================================================================

Decisões puramente técnicas necessárias à execução são permitidas.

Exemplos:

- organização de módulos Python;
- diretórios;
- templates;
- arquivos estáticos;
- CSS;
- biblioteca SQLite;
- configuração da aplicação;
- tratamento técnico de exceções;
- dependências Python.

Essas decisões NÃO podem criar:

- regra de negócio;
- novo campo funcional;
- estado funcional;
- operação;
- relacionamento funcional;
- validação de negócio;
- funcionalidade não documentada.


======================================================================
31. BLOQUEIO DURANTE A IMPLEMENTAÇÃO
======================================================================

Se durante a implementação surgir necessidade de informação funcional não
existente no Contrato:

NÃO INVENTE.

NÃO improvise.

NÃO transforme uma decisão técnica em decisão funcional.

Registre:

BLOQUEIO FUNCIONAL — INFORMAÇÃO NÃO IDENTIFICADA NAS EVIDÊNCIAS

Informe:

- funcionalidade afetada;
- informação ausente;
- evidência consultada;
- impacto.

Continue implementando os demais itens independentes sempre que possível.


======================================================================
32. TESTES
======================================================================

Gere testes para validar as funcionalidades implementadas sempre que houver
critérios de aceite suficientes para isso.

Cada teste deverá ser rastreável ao respectivo:

- critério de aceite;
- regra de negócio;
- funcionalidade.

Não invente critérios de teste que introduzam comportamento funcional novo.


======================================================================
33. AUDITORIA PÓS-IMPLEMENTAÇÃO
======================================================================

Antes de entregar o sistema para validação humana, confronte:

EVIDÊNCIAS
        ×
CONTRATO DE IMPLEMENTAÇÃO
        ×
MATRIZ AUTORIZADA
        ×
CÓDIGO GERADO
        ×
TESTES

Verifique:

- todo campo implementado está autorizado?
- toda tabela funcional está autorizada?
- toda operação está autorizada?
- toda funcionalidade está autorizada?
- todo comportamento possui sustentação?
- existe funcionalidade extra?
- existe requisito de outra capacidade?
- algum item NÃO AUTORIZADO foi implementado?
- algum item AGUARDANDO VALIDAÇÃO foi implementado?
- existe código funcional sem rastreabilidade?

Se existir implementação funcional não autorizada:

REMOVA-A antes da entrega.


======================================================================
34. ENTREGA PARA VALIDAÇÃO HUMANA
======================================================================

Ao final da implementação apresente:

CAPACIDADE IMPLEMENTADA — AGUARDANDO VALIDAÇÃO HUMANA

Informe:

1. capacidade implementada;
2. arquivos criados;
3. arquivos alterados;
4. estrutura principal do projeto;
5. banco SQLite criado;
6. tabelas criadas;
7. funcionalidades implementadas;
8. telas implementadas;
9. testes executados e resultados;
10. itens não implementados;
11. bloqueios;
12. instruções para execução no Windows 11.

As instruções deverão permitir que o humano:

- inicie a aplicação;
- acesse a interface Web;
- execute as funcionalidades;
- valide o comportamento.

PARE.


======================================================================
35. VALIDAÇÃO HUMANA DO SISTEMA
======================================================================

O humano executará a aplicação e comparará seu comportamento com o esperado.

A aplicação NÃO será considerada aprovada apenas porque:

- foi gerada;
- iniciou corretamente;
- os testes automatizados passaram.

A decisão final pertence ao humano.


======================================================================
36. CORREÇÕES SOLICITADAS PELO HUMANO
======================================================================

Quando o humano informar um problema, analise cada solicitação antes de
alterar o código.

Classifique-a como:

A — DEFEITO DE IMPLEMENTAÇÃO

O código não corresponde às evidências ou ao contrato aprovado.

AÇÃO:
Corrigir.


B — INTERPRETAÇÃO INCORRETA

A evidência foi interpretada incorretamente.

AÇÃO:
Corrigir e atualizar a rastreabilidade.


C — AJUSTE TÉCNICO OU VISUAL SEM ALTERAÇÃO FUNCIONAL

Não altera requisito ou comportamento funcional.

AÇÃO:
Pode ser realizado.


D — LACUNA DOCUMENTAL

A correção exigiria informação que não existe nas evidências.

AÇÃO:
Não inventar.
Apresentar ao humano.


E — NOVO REQUISITO

A solicitação introduz comportamento não existente nas evidências.

AÇÃO:
Não tratar como requisito recuperado do legado.

Registrar:

NOVO REQUISITO — NÃO ORIGINADO DAS EVIDÊNCIAS

Aguardar autorização humana específica antes de implementá-lo.


======================================================================
37. NOVOS REQUISITOS AUTORIZADOS PELO HUMANO
======================================================================

Caso o humano decida conscientemente adicionar um novo requisito que não
existe nas evidências, ele deverá ser identificado separadamente como:

AUTORIZAÇÃO HUMANA — REQUISITO NOVO

Esse requisito poderá ser implementado somente após autorização explícita.

Sua rastreabilidade deverá indicar:

ORIGEM: DECISÃO HUMANA

e nunca:

ORIGEM: EVIDÊNCIA DO LEGADO

Isso é necessário para preservar a integridade do experimento.


======================================================================
38. CICLO DE CORREÇÃO
======================================================================

Após cada correção:

1. altere os arquivos necessários;
2. execute novamente os testes aplicáveis;
3. execute novamente a auditoria;
4. apresente o que foi corrigido;
5. disponibilize novamente a aplicação para validação humana;
6. PARE.

Repita esse ciclo quantas vezes forem necessárias.

NÃO existe limite de ciclos.

Durante esse processo continue trabalhando EXCLUSIVAMENTE na mesma capacidade.


======================================================================
39. CAPACIDADE APROVADA
======================================================================

A capacidade somente será encerrada quando o humano escrever explicitamente:

CAPACIDADE APROVADA

Nenhuma outra expressão deverá produzir esse efeito.

"OK" NÃO significa capacidade aprovada.

"PODE CONTINUAR" NÃO significa capacidade aprovada.

"FUNCIONOU" NÃO significa capacidade aprovada.

Somente:

CAPACIDADE APROVADA


======================================================================
40. ENCERRAMENTO DA CAPACIDADE
======================================================================

Ao receber:

CAPACIDADE APROVADA

registre:

CAPACIDADE X — APROVADA

Apresente um resumo final contendo:

- regras implementadas;
- critérios atendidos;
- funcionalidades implementadas;
- testes;
- eventuais decisões humanas;
- novos requisitos autorizados, se existirem;
- pendências conhecidas, se existirem.

Depois:

PARE.

NÃO inicie outra capacidade.


======================================================================
41. PRÓXIMA CAPACIDADE
======================================================================

Após uma capacidade ser aprovada, aguarde novo comando humano:

GERE CAPACIDADE X

NÃO escolha automaticamente a próxima capacidade.

Ao receber o novo comando:

1. consulte capacidades.md;
2. consulte a ordem oficial;
3. verifique se X corresponde à próxima capacidade prevista.

Se corresponder:

inicie a FASE 1.

Se NÃO corresponder:

NÃO inicie.

Informe:

A ORDEM DEFINIDA EM capacidades.md INDICA QUE A PRÓXIMA CAPACIDADE É Y.

Aguarde decisão humana.


======================================================================
42. CAPACIDADES JÁ APROVADAS
======================================================================

Funcionalidades pertencentes a capacidades anteriormente aprovadas poderão
permanecer no sistema e ser reutilizadas tecnicamente.

Entretanto:

NÃO altere silenciosamente comportamento funcional de capacidade já aprovada.

Se a nova capacidade exigir alteração de comportamento anteriormente aprovado,
registre:

IMPACTO EM CAPACIDADE JÁ APROVADA

Identifique:

- capacidade afetada;
- funcionalidade afetada;
- evidência nova;
- impacto.

Aguarde decisão humana quando houver conflito funcional.


======================================================================
43. TRATAMENTO DO MARCADOR [?]
======================================================================

Quando encontrar [?] nas evidências:

NÃO invente seu conteúdo.

NÃO complete automaticamente.

Considere-o informação ainda não determinada ou prevista para tratamento
posterior, conforme o contexto documental.

Quando afetar a capacidade atual, registre-o como lacuna.

Não utilize [?] como autorização para criar comportamento.


======================================================================
44. PRINCÍPIO DE IMPLEMENTAÇÃO
======================================================================

O processo correto é:

CAPACIDADES.MD
        ↓
CAPACIDADE SOLICITADA PELO HUMANO
        ↓
EVIDÊNCIAS
        ↓
VALIDAÇÃO HUMANA
        ↓
REGRAS / CRITÉRIOS / FUNCIONALIDADES
        ↓
VALIDAÇÃO HUMANA
        ↓
CONTRATO DE IMPLEMENTAÇÃO
        ↓
VALIDAÇÃO HUMANA
        ↓
IMPLEMENTAÇÃO
        ↓
TESTES
        ↓
AUDITORIA
        ↓
VALIDAÇÃO HUMANA DO SISTEMA
        ↓
CORREÇÕES
        ↓
VALIDAÇÃO HUMANA
        ↓
CAPACIDADE APROVADA

NUNCA:

SUPOSIÇÃO
        ↓
IMPLEMENTAÇÃO


======================================================================
45. REGRA FINAL
======================================================================

NA DÚVIDA:

NÃO INVENTE.

Se faltar informação:

REGISTRE A LACUNA.

Se houver interpretação:

CLASSIFIQUE COMO INFERIDO.

Se não houver sustentação:

CLASSIFIQUE COMO NÃO IDENTIFICADO.

Se houver conflito:

APRESENTE O CONFLITO.

Se a decisão alterar comportamento funcional:

AGUARDE O HUMANO.

Se houver evidência suficiente:

IMPLEMENTE SOMENTE APÓS O GATE HUMANO CORRESPONDENTE.

É preferível produzir uma aplicação funcionalmente incompleta e fiel às
evidências do que uma aplicação aparentemente completa baseada em
funcionalidades inventadas.


======================================================================
46. COMANDO DA PRIMEIRA EXECUÇÃO
======================================================================

Considere como comando inicial:

GERE CAPACIDADE 1

Execute SOMENTE:

FASE 1 — IDENTIFICAÇÃO DAS EVIDÊNCIAS

para:

Capacidade 1 — Estrutura da rede e do gasto

Utilize:

C:\projetos\capacidades.md

Apresente os arquivos encontrados.

NÃO execute a FASE 2 ainda.

NÃO gere código.

NÃO altere o sistema.

PARE.

Aguarde:

OK