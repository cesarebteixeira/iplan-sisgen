# US — E240C — Consulta de períodos de contrato do grupo

## Estória

Como **servidor da CRE que responde pelos contratos de fornecimento da alimentação
escolar da sua coordenadoria**, quero **consultar os períodos de contrato já cadastrados
para o meu grupo e escolher um deles**, para que **eu abra o período certo e veja a
situação dele sem ter de decorar o tipo de contrato, o fornecedor e a data de início que
o identificam**.

O período de contrato não tem número: ele é identificado pela combinação do grupo, da
data de início, do tipo de contrato, do fornecedor e do cadastro. Sem uma lista, quem
precisa abrir um período tem de digitar essa combinação inteira na tela de manutenção do
período, e é recusado quando erra uma parte dela. A lista é o que deixa o servidor
reconhecer o período pelo que ele mostra — as datas de início e limite, o tipo de
contrato, o fornecedor, a razão social e a situação — e escolhê-lo dali. Nada nesta tela
é gravado: ela só lê, e quem trata o período é a tela que ela abre.

## Contexto

Jornada S000M → E000M → E240M → E240C (a entrada, `LOGON` → `S000M`, é comum a todas as
jornadas).

Ator: servidor de CRE — consulta os períodos de contrato já cadastrados para o grupo da
sua coordenadoria e escolhe um deles, que a tela seguinte abre em consulta.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio. Os dois menus do caminho — `E000M` e `E240M` — não
gravam nada: só encaminham.

O que esta tela usa da sessão é a **secretaria (o tipo de órgão)**, a **coordenadoria
regional escolar do servidor** (o grupo), a **matrícula**, o **código de acesso**, o
**privilégio** e a **data do sistema**; a carga disso é regra da entrada e está no anexo
de evidências, em **Regras que se revelaram da entrada**. O **órgão filho** do servidor,
que a entrada também carrega, não limita esta tela: o alcance aqui é o período de contrato
do grupo.

Esta tela é uma passagem: ela lista os períodos do grupo e, escolhido um, **entrega o
registro e a operação de consulta à tela seguinte** (RN-09 e RN-13). É por isso que a
jornada não termina aqui — quem mostra o período por inteiro é a tela seguinte; a tela
desta jornada é o índice dela.

## Regras de negócio

### RN-01 — A tela é de consulta: a única opção aceita é a consulta

Esta é uma tela de **consulta**. A opção mostrada é reposta como consulta a cada abertura,
e qualquer outra opção de manutenção é recusada com
**\* Opcao nao disponivel. Use CON \***, com o cursor de volta ao campo da opção e **nada
lido** nesse caminho: a recusa vem antes de qualquer leitura do cadastro de períodos.

O valor aceito como consulta não é uma palavra escrita no programa: ele vem da **tabela de
mensagens do ambiente**, a mesma que dá o texto da recusa — é por isso que a mensagem
manda usar "CON" enquanto o programa compara um código interno. O que o programa fixa é só
o texto da recusa.

### RN-02 — O grupo consultado é o da própria coordenadoria

O grupo consultado é o da **sessão do servidor**. Informado um grupo diferente daquele que
a sessão carrega, a consulta para com **\* Usuario sem acesso a outro grupo \***, com o
cursor de volta ao campo do grupo, antes das conferências de obrigatoriedade e antes de
qualquer leitura do cadastro. Quando a sessão já traz o grupo, é ele que a tela mostra no
campo: o servidor não precisa informá-lo, e informar outro não é aceito.

[?] Quando a sessão **não** tem grupo — o vínculo do servidor não aponta nenhuma
coordenadoria —, a conferência não se aplica e a consulta aceita qualquer grupo. Se isso é
intencional ou é buraco de autorização, é pergunta ao site.

### RN-03 — O grupo é obrigatório

O grupo tem de ser informado. Em branco, a recusa é **\* Informe o grupo \***, com o
cursor de volta ao campo do grupo, e nada é lido do cadastro.

### RN-04 — A lista é a dos períodos de contrato do grupo, em treze linhas

A tela lê os períodos de contrato do **tipo de órgão da sessão** e do **grupo informado**
e mostra, de cada período, **uma linha** com os dados que o identificam: o **dia, o mês e
o ano de início do período**; o **dia, o mês e o ano limite**; o **tipo de contrato**; o
**código do fornecedor**; a **identificação do cadastro**; a **razão social do
fornecedor**; e a **situação**. No alto a tela mostra a **descrição do tipo de órgão da
sessão** (a secretaria) e a **data do sistema**.

A lista tem **treze linhas**, uma por período, na ordem da **data de início** (ano, mês,
dia) e, dentro dela, do **tipo de contrato**, do **fornecedor** e do **cadastro**. Quando
os períodos do grupo acabam, a leitura para e as linhas que sobram ficam em branco. O
cadastro declara capacidade para **cem mil** períodos — capacidade é parâmetro de
dimensionamento, não volume cadastrado.

[?] A descrição do tipo de órgão e a data do sistema são copiadas da sessão, e nenhum
programa deste caminho as preenche — a área comum só as apaga na inicialização. Se o
ambiente não as fornecer, o cabeçalho sai em branco. Pergunta ao site.

### RN-05 — A situação da linha marca o período cujo cadastro já foi gerado

A situação da linha recebe **"Gerado"** quando o período está marcado, no cadastro, como
já requisitado; nos demais períodos a situação sai em branco. É a única informação da
lista que diz ao servidor se aquele período já virou cadastro — as demais colunas só o
identificam.

### RN-06 — A razão social do período vem do cadastro de fornecedores

O código do fornecedor mostrado na linha é procurado no **cadastro de fornecedores**, e é
a **razão social** de lá que aparece ao lado dele. O que a linha mostra é o fornecedor do
período lido, e não um fornecedor informado.

[?] Se o fornecedor da linha não estiver no cadastro de fornecedores, a tela não avisa: a
razão social sai em branco e a lista continua normalmente. Se o esperado é um aviso, é
pergunta ao site.

### RN-07 — A consulta abre no período do ano corrente, e a data de início ancora a lista

Na abertura, a tela procura o primeiro período do grupo a partir do **começo do ano do
sistema** e adota a data de início dele como **ponto de partida** da lista: os períodos
anteriores a esse ponto não aparecem nessa abertura. Não achando nenhum período do grupo a
partir dali, o ponto de partida fica vazio e a lista começa no primeiro período cadastrado
para o grupo.

O ponto de partida é mostrado no alto da tela, nas três partes da data de início do
período, e é ele que a leitura seguinte usa: enchendo a página, a data do **último**
período exibido volta como ponto de partida; terminando a lista antes da última linha, o
ponto de partida guardado é limpo.

[?] Os três campos de data do alto não têm rótulo de negócio no fonte — o rótulo deles é o
próprio nome interno —, enquanto as mesmas três partes, nas linhas, se chamam "DIA INICIO
PERIO", "MES INICIO PERIO" e "ANO INICIO PERIO". Eles passam pela edição numérica e o
cursor volta a eles quando a digitação é recusada, o que indica que são digitáveis; se a
máscara os deixa visíveis, e se o servidor consegue assim recuar a lista para períodos
mais antigos, não se conclui do material lido. Pergunta ao site.

### RN-08 — Sem período para o grupo, a tela avisa que não existem registros cadastrados

Não achando nenhum período para o grupo na primeira posição da página, a tela avisa
**\* Nao existem registros cadastrados \*** e não lista nada. O aviso é montado na primeira
posição: ele sai uma vez, e não se repete a cada linha vazia. Quando o aviso sai, o ponto
de partida guardado é limpo.

[?] Quando a sessão não tem grupo, a tela abre com o cursor no campo do grupo e com esse
mesmo aviso — que sai antes de o servidor ter informado grupo nenhum. Se a intenção era
apenas pedir o grupo, o aviso está a mais. Pergunta ao site.

### RN-09 — Marcado um período, a tela o entrega à tela seguinte, que abre em consulta

Marcada a linha de um período — e preenchida a data de início dela —, a tela lê o período
pela combinação mostrada na linha e **passa o registro e a operação de consulta** para a
tela seguinte, a `E241T`, que abre o período **em consulta**. Nada é gravado por esta tela
nessa passagem.

A linha é marcada pelo **indicador de seleção** de cada linha. Sem marcá-lo, ou com o
indicador em branco, a tela apenas segue mostrando a lista e recolhe o ponto de partida do
último período exibido.

[?] A tela não confere se o período marcado existe no cadastro: ela lê pela combinação
mostrada na linha e, não achando, entrega assim mesmo o que a linha tem — quem recusa é a
tela seguinte, com **\* Requisicao nao cadastrada \***. Se a intenção era recusar aqui, a
conferência não existe. Pergunta ao site.

### RN-10 — A linha marcada e vazia é recusada

Marcada uma linha **sem período** — sem a data de início —, a consulta é recusada com
**\* Consulte linha preenchida \***, com o cursor de volta ao indicador de seleção daquela
linha, e nada é entregue à tela seguinte. A recusa existe para que o servidor marque uma
linha com período, e não uma das linhas que sobram em branco no fim da lista.

### RN-11 — Os dados da linha não escolhem a consulta

O **tipo de contrato**, o **código do fornecedor**, a **identificação do cadastro** e as
**datas** que a linha mostra são dados de **resultado**: quem os define é o período lido,
não o servidor. A consulta continua sendo a do **grupo** e a do **ponto de partida** — não
há filtro por tipo de contrato nem por fornecedor, e a lista não relaciona por nenhum outro
caminho.

[?] Esses campos passam pela edição numérica, como se fossem digitáveis, embora a tela os
substitua pelo que leu. Ou a máscara permite digitá-los, ou a edição é sobra do gerador.
Como a máscara não está neste lote, não se sabe quais campos desta tela o servidor consegue
digitar. Pergunta ao site.

### RN-12 — A digitação passa pela edição numérica antes de qualquer leitura

Os **treze campos numéricos** da tela — o grupo, as três partes do ponto de partida, as
três partes da data de início, as três da data limite, o tipo de contrato, o fornecedor e a
identificação do cadastro — são tratados como número: o que estiver em branco vira zero, os
zeros à esquerda caem e o que não for número é recusado antes de qualquer leitura do
cadastro. Na recusa, o cursor volta a apenas **quatro** deles: o grupo e as três partes do
ponto de partida. Nos outros nove o tratamento é interrompido com o campo ainda em erro.

[?] O texto da recusa da edição numérica não está nos fontes desta jornada: quem edita é
uma rotina comum, importada, sem corpo no acervo. E como o cursor só volta a quatro campos,
o servidor pode ser recusado sem saber em qual campo errou. Pergunta ao site.

### RN-13 — O que a tela entrega à seguinte depende de quem a chamou

A tela registra na sessão, junto com o período escolhido, a **sua própria identidade** e a
**operação de consulta**; é por essa marca que a tela seguinte aceita abrir o período. A
`E241T` é aberta por três caminhos — a tela de manutenção do período (`E240T`), esta lista
(`E240C`) e a `E242T` — e, quando chega por qualquer outro, não processa o período e devolve
o servidor ao menu `E240M`. Sem a marca desta tela, portanto, o período escolhido não se
abre.

A tela deixa ainda ligada a **marca de retorno**, que faz a tela seguinte devolver o
controle a quem a chamou. Nada disso aparece em campo nenhum desta tela: é a parte da
passagem que só se lê no caminho.

### RN-14 — A consulta não grava nada

Nenhuma das operações de gravação, de exclusão ou de travamento que o programa carrega é
executada por esta tela. As declarações existem para todos os cadastros que ela enxerga —
é assim que o gerador monta o programa —, mas a tela não as aciona: a única execução é a de
**consulta**. O travamento de registro aparece apenas dentro dos caminhos de exclusão, que
esta tela não percorre. A tela também não gera trilha de auditoria: o cadastro de auditoria
não está entre os que ela enxerga.

## Cenários BDD

```gherkin
Funcionalidade: Consultar os períodos de contrato de um grupo e abrir o período escolhido

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E240C

  Cenário: RN-01 — consultar os períodos do meu grupo
    Dado que a minha sessão tem uma coordenadoria
    Quando abro a tela E240C
    Então vejo a lista dos períodos de contrato daquele grupo
    E a opção mostrada é a consulta

  Cenário: RN-01 — opção diferente de consulta
    Dado que estou na tela E240C
    Quando informo uma opção diferente da consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use CON *"
    E o cursor volta ao campo da opção
    E nada é lido do cadastro de períodos nesse caminho

  Cenário: RN-02 — o grupo da consulta é o da minha sessão
    Dado que a minha sessão tem uma coordenadoria
    Quando abro a tela E240C
    Então o grupo consultado é o da minha sessão
    E não preciso informá-lo

  Cenário: RN-02 — grupo de outra coordenadoria
    Dado que a minha sessão tem uma coordenadoria
    Quando informo o grupo de outra coordenadoria
    Então vejo a mensagem "* Usuario sem acesso a outro grupo *"
    E o cursor volta ao campo do grupo

  Cenário: RN-02 — sessão sem coordenadoria
    Dado que a minha sessão não tem coordenadoria
    Quando informo qualquer grupo
    Então a consulta é feita para esse grupo

  Cenário: RN-03 — grupo não informado
    Quando deixo o grupo em branco
    Então vejo a mensagem "* Informe o grupo *"
    E o cursor volta ao campo do grupo
    E nada é lido do cadastro

  Cenário: RN-04 — os dados de cada período na lista
    Dado que existem períodos de contrato para o meu grupo
    Quando abro a tela E240C
    Então de cada período vejo a data de início, a data limite, o tipo de contrato,
          o código do fornecedor, a identificação do cadastro, a razão social e a situação
    E a lista mostra no máximo treze períodos
    E as linhas que sobram ficam em branco

  Cenário: RN-04 — o cabeçalho da lista
    Dado que entrei no sistema
    Quando abro a tela E240C
    Então vejo a descrição do tipo de órgão da minha sessão
    E vejo a data do sistema

  Cenário: RN-05 — período cujo cadastro já foi gerado
    Dado que um período do meu grupo está marcado como já requisitado no cadastro
    Quando vejo a linha desse período
    Então a situação dela é "Gerado"
    E nos demais períodos a situação sai em branco

  Cenário: RN-06 — a razão social vem do cadastro de fornecedores
    Dado que o fornecedor do período está no cadastro de fornecedores
    Quando vejo a linha desse período
    Então ao lado do código do fornecedor vejo a razão social do cadastro

  Cenário: RN-07 — a lista abre no período do ano corrente
    Dado que o meu grupo tem períodos anteriores e posteriores ao ano do sistema
    Quando abro a tela E240C
    Então a lista começa no primeiro período a partir do começo do ano do sistema
    E os períodos anteriores a esse ponto não aparecem

  Cenário: RN-07 — grupo sem período a partir do ano corrente
    Dado que o meu grupo não tem período a partir do ano do sistema
    Quando abro a tela E240C
    Então a lista começa no primeiro período cadastrado para o grupo

  Cenário: RN-08 — nenhum período para o grupo
    Dado que não existe período de contrato para o grupo informado
    Quando a lista é montada
    Então vejo a mensagem "* Nao existem registros cadastrados *"
    E nenhuma linha é preenchida

  Cenário: RN-09 — marcar um período e abrir o detalhe dele
    Dado que a lista mostra os períodos do meu grupo
    E marco o indicador de seleção de um período
    Quando confirmo
    Então o detalhe daquele período se abre em consulta
    E nada é gravado por esta tela

  Cenário: RN-09 — a lista sem período marcado não abre nada
    Dado que a lista mostra os períodos do meu grupo
    Quando confirmo sem marcar nenhum período
    Então a tela segue mostrando a lista
    E nenhum período se abre

  Cenário: RN-10 — linha marcada sem período
    Dado que a lista mostra os períodos do meu grupo
    E marco uma linha que está em branco
    Quando confirmo
    Então vejo a mensagem "* Consulte linha preenchida *"
    E o cursor volta ao indicador de seleção daquela linha
    E nenhum período se abre

  Cenário: RN-11 — os dados da linha não filtram a lista
    Dado que a lista mostra os períodos do meu grupo
    Quando digito um tipo de contrato ou um fornecedor diferente nas linhas
    Então a lista continua sendo a dos períodos do grupo e do ponto de partida
    E o que digitei nesses campos não escolhe o que aparece

  Cenário: RN-12 — digitação que não é número
    Quando digito num campo numérico algo que não é número
    Então o sistema recusa a digitação antes de ler qualquer período
    E o cursor volta ao campo recusado quando é o grupo ou o ponto de partida

  Cenário: RN-13 — o período aberto por outro caminho
    Dado que o período é aberto sem passar por esta lista nem pela tela de manutenção
    Quando a tela seguinte recebe o registro
    Então ela não processa o período
    E o servidor volta ao menu E240M

  Cenário: RN-14 — a consulta não grava nada
    Dado que abro a tela E240C e consulto os períodos do meu grupo
    Quando a lista é mostrada
    Então nenhum período de contrato nem fornecedor é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado
```
