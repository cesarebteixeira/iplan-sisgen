# US — C241C — Consultar os grupamentos de classificação de licitação

## Estória

Como **servidor de CRE**, quero **consultar os grupamentos de classificação de
licitação já cadastrados, com o código, a descrição e a vigência de cada um**,
para que **eu saiba em que grupamento um item é classificado e desde quando a
descrição que estou vendo vale**.

O grupamento é a classificação de licitação que agrupa os itens, e o cadastro
guarda **mais de uma versão do mesmo grupamento**, cada uma com a sua data de
vigência: a mesma descrição muda com o tempo. Quem classifica, mede ou confere um
item precisa do código e da descrição que vale naquele momento — uma consulta que
não mostre a vigência não deixa saber qual das versões está valendo. Esta tela é
só de leitura: quem mantém o cadastro é outra tela.

## Contexto

Jornada S000M → C000M → C055M → C241C.

Ator: servidor de CRE — consulta a lista dos grupamentos de classificação de
licitação e a vigência de cada um.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e
menus.md`: é **dado de navegação**, não regra de negócio.

As regras abaixo são só as da tela desta jornada. O C000M e o C055M são menus:
têm opções e apenas encaminham, sem gravar nada. Esta tela é a última da jornada
— não encaminha nada adiante — e **não** muda de comportamento conforme a tela
que a chamou, porque não compara a tela de origem com código nenhum. O contexto
que ela usa — matrícula, código de acesso, privilégio, tipo de órgão e CRE — é o
que a entrada deixou na sessão; a rotina comum de segurança o recarrega sozinha,
e esta tela não o recalcula nem o recorta.

## Regras de negócio

### RN-01 — A tela é de consulta: qualquer outra opção é recusada

A tela abre em modo de consulta e repõe esse modo a cada apresentação, de modo
que a opção mostrada volta a ser sempre a consulta. Se o operador informar outra
opção de manutenção, o sistema recusa com
**\* Opcao nao disponivel. Use CON \*** e devolve o cursor ao campo da opção. A
recusa vem depois das conferências de acesso e de digitação e **antes de ler o
cadastro de grupamentos**: nenhum grupamento é lido nem mostrado nesse caminho.

[?] A recusa só existe se a máscara oferecer ao operador um campo de opção. Como
a abertura da tela repõe a consulta sozinha, essa recusa só pode ser alcançada
numa mensagem seguinte do operador; se a máscara não tem esse campo, a recusa é
trecho sem uso. Pergunta ao site.

### RN-02 — A tela lista os grupamentos cadastrados numa grade de 16 linhas

A tela é a listagem dos grupamentos de classificação de licitação já cadastrados.
Cada uma das **16 linhas** da grade tem **3 campos**: o **código do grupamento**
(4 dígitos), a **descrição** (30 caracteres) e a **data de vigência** (10
caracteres). Os dados vêm do cadastro de grupamentos, que tem **6 campos**, tem a
descrição de preenchimento obrigatório e capacidade para **500** grupamentos —
capacidade é o máximo esperado, parâmetro de dimensionamento, não o que está
cadastrado. Quem mantém esse cadastro é a tela C240T, não esta.

[?] O cadastro de grupamentos não tem campo de secretaria, de CRE nem de órgão:
se a base é compartilhada entre as secretarias, o mesmo grupamento e a mesma
descrição valem para todas, e o único recorte é a autorização da tela. Se deveria
haver recorte por secretaria, é pergunta ao site.

### RN-03 — A listagem percorre os grupamentos em ordem crescente de código

A lista não é digitada pelo operador: a tela percorre os códigos de grupamento em
ordem crescente, começando pelo primeiro, e ocupa uma linha com o grupamento de
cada código. A grade para nas 16 linhas; não havendo mais grupamento para
mostrar, a listagem para e as linhas restantes ficam em branco.

[?] A leitura que procura o grupamento de cada código usa o recurso de
posicionamento do dicionário de dados, cujo efeito exato não está no acervo nem
no manual: se ele posiciona no **código exato**, a lista para no primeiro código
sem grupamento e omite o que estiver cadastrado em códigos maiores; se posiciona
no **primeiro código igual ou maior**, a lista pula os códigos vazios e mostra
todos os grupamentos. Os dois comportamentos são compatíveis com o que o fonte
mostra, e o site precisa dizer qual é o esperado.

[?] Ao encher a grade, a tela decide se reinicia a contagem pelo primeiro código:
a decisão depende de uma marca que este programa **nunca liga**. Como está, a
contagem não é reiniciada e a apresentação seguinte continua do código onde a
anterior parou. Se essa continuidade é a paginação pretendida ou um defeito
herdado do gerador, é pergunta ao site.

### RN-04 — De cada grupamento a tela mostra a versão de vigência mais recente

Cada linha mostra a descrição e a vigência da versão **mais recente** cadastrada
para aquele código — é a versão que está valendo. A data sai no formato
**dia/mês/ano**, com o dia e o mês em dois dígitos e o ano em quatro.

[?] A conclusão de que a linha traz a versão de vigência mais recente sai do
valor máximo com que as três partes da data são preenchidas antes da leitura —
o mesmo recurso de posicionamento da dúvida da RN-03. A leitura confere o código
do grupamento que voltou, mas **não** confere a data. Se o que a tela mostra é a
vigência mais recente ou outra versão, o site precisa confirmar.

### RN-05 — Não havendo grupamento para mostrar, a tela avisa

Não havendo grupamento nenhum para mostrar, a tela avisa
**\* Nao existem grupamentos cadastrados \*** e não preenche nenhuma linha. O
aviso é decidido pela leitura de abertura, antes de a grade ser montada, e é
decidido **só na primeira linha**.

[?] Como o aviso é decidido uma única vez, na montagem da primeira linha, e não é
recalculado depois, uma grade que esvazie mais adiante fica em branco sem
explicação. Se o cadastro tiver grupamentos só em códigos maiores, o que o
operador vê depende de qual das duas leituras da RN-03 vale. Pergunta ao site.

### RN-06 — A tela mostra a data do sistema e a descrição do tipo de órgão da sessão

Fora da grade, a tela exibe a **data do sistema** e a **descrição do tipo de
órgão** da sessão.

[?] Nem a data do sistema nem a descrição do tipo de órgão são preenchidas por
nenhum programa do acervo lido: as duas só aparecem como origem de cópia e são
inicializadas em branco pelo ambiente comum. De onde vêm os valores é pergunta ao
site; se não vierem do ambiente, os dois campos saem em branco.

### RN-07 — Cada consulta começa com os campos de resultado limpos

Antes de conferir a digitação e de ler qualquer grupamento, a tela apaga a
descrição e a vigência que a consulta anterior havia mostrado. Uma consulta
recusada, portanto, não deixa na tela o resultado da consulta anterior.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se
existe um caminho de entrada em que os campos não são limpos, é pergunta ao site.

### RN-08 — O código de grupamento digitado não comanda a consulta

O campo do código do grupamento aceita digitação e passa por edição numérica:
campo em branco vira zero, o que não for número é recusado antes de qualquer
leitura, e o erro interrompe o tratamento. Mas o código digitado **não escolhe
nada**: quando a listagem acha o grupamento, a tela reescreve o campo com o
código que achou. Quem decide o que aparece é a ordem da listagem, não a
digitação.

[?] O que o operador vê quando a digitação do código é recusada — se há mensagem,
e qual — não está nos fontes desta jornada: a rotina que faz a edição não faz
parte do acervo lido, e esta tela não devolve o cursor a nenhum campo nessa
recusa, ao contrário das telas irmãs que validam o mesmo tipo de campo.

[?] Se o campo do código deveria servir de filtro — consultar um grupamento só
pelo seu código — ou se é apenas um campo de saída que a máscara deixa digitar, é
pergunta ao site.

### RN-09 — Antes de mostrar a lista, o sistema confere o acesso

A abertura da tela passa por três conferências, com o contexto da sessão —
matrícula, código de acesso, privilégio, tipo de órgão e CRE. A tela precisa
estar cadastrada no cadastro de telas: não estando, o acesso é recusado com
**\* Tela nao disponivel \***. A matrícula precisa ter a tela autorizada no seu
código de acesso: não tendo, a recusa é
**\* Acesso negado para esta matricula \***. Por fim a transação passa pela
lógica de rota, que decide o encaminhamento a partir do que a máscara manda. O
contexto da sessão não é recalculado aqui: é o que a entrada deixou.

[?] A conferência da operação procura os flags de inclusão, de alteração e de
exclusão, mas **não** o de consulta: quem tem a tela autorizada consulta sem
precisar do flag de consulta. Se a intenção era exigir esse flag por tela, o
caminho não o exige. Pergunta ao site.

### RN-10 — A consulta não grava nada e não deixa rastro de auditoria

A tela e as rotinas comuns que ela chama só leem. Nenhum registro é incluído,
alterado ou excluído, e nenhum registro de auditoria é gerado. As operações de
gravação, de exclusão e de travamento de registro existem declaradas para os
cadastros que a tela enxerga, mas **não são executadas em nenhum caminho**:
declarar não é executar.

## Cenários BDD

```gherkin
Funcionalidade: Consultar os grupamentos de classificação de licitação

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C241C

  Cenário: Consulta dos grupamentos cadastrados
    Dado que existem grupamentos cadastrados
    Quando abro a tela C241C
    Então vejo os grupamentos em linhas, cada uma com o código, a descrição e a vigência

  Cenário: A lista sai em ordem de código, uma linha por grupamento
    Dado que existem grupamentos cadastrados
    Quando abro a tela C241C
    Então cada linha traz um grupamento diferente, em ordem crescente de código
    E a grade mostra no máximo 16 linhas

  Cenário: A vigência mostrada é a mais recente daquele código
    Dado que um mesmo código de grupamento tem mais de uma vigência cadastrada
    Quando abro a tela C241C
    Então vejo a descrição e a vigência da versão mais recente daquele código
    E a data aparece no formato dia/mês/ano

  Cenário: Não há grupamento nenhum cadastrado
    Dado que não existe nenhum grupamento cadastrado
    Quando abro a tela C241C
    Então vejo a mensagem "* Nao existem grupamentos cadastrados *"
    E nenhuma linha da grade é preenchida

  Cenário: A data do sistema e o tipo de órgão da sessão
    Dado que entrei no sistema
    Quando abro a tela C241C
    Então vejo a data do sistema
    E vejo a descrição do tipo de órgão da minha sessão

  Cenário: O resultado da consulta anterior não fica na tela
    Dado que já abri a tela e ela mostrou grupamentos
    Quando volto a abrir a tela
    Então a descrição e a vigência da consulta anterior não ficam na tela

  Cenário: Opção de manutenção diferente de consulta
    Dado que estou na tela C241C
    Quando informo uma opção diferente da consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use CON *"
    E o cursor volta ao campo da opção
    E nenhum grupamento é lido nesse caminho

  Cenário: Código de grupamento digitado que não é número
    Dado que digito no campo do código de grupamento algo que não é número
    Quando envio a tela
    Então o sistema recusa a digitação antes de listar qualquer grupamento

  Cenário: O código digitado não comanda a consulta
    Dado que digito um código de grupamento no campo
    Quando envio a tela
    Então a lista continua sendo a dos grupamentos cadastrados, em ordem de código
    E o código que digitei não escolhe o que aparece

  Cenário: A consulta não grava nada
    Dado que abro a tela C241C
    Quando a lista é mostrada
    Então nenhum grupamento é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado

  Cenário: Tela não cadastrada
    Dado que a tela C241C não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo consultar

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não tem a tela C241C autorizada
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo consultar
```
