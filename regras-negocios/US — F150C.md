# US — F150C — Consultar notas fiscais do grupo e do fornecedor

## Estória

Como **servidor da CRE que acompanha as notas fiscais lançadas**, quero
**conferir, por grupo, ano de competência, instituição e fornecedor, os valores das
notas fiscais registradas e o que ficou retido ou descontado**, para que **a
conferência da nota e a chegada às telas de item e de dedução partam do número
certo, e o que foi lançado não fique sem ser visto**.

A nota fiscal é lançada por item, e cada item pode ter retenção e dedução; quem
recebe a nota e quem paga precisa somar o que foi retido e o que foi deduzido para
chegar ao valor da nota. Esta tela é o ponto em que esse resumo é visto antes de
descer ao detalhe: ela mostra as notas do grupo e da competência, com o valor de
cada uma, e aponta a diferença quando a conta não fecha. Sem ela, a nota só existe
no lançamento — não há por onde conferir o total contra os itens, e a retenção ou
a dedução de uma nota fica sem caminho para ser examinada.

## Contexto

Jornada S000M → F000M → F100M → F150C.
Ator: servidor de CRE — confere, por grupo e competência, as notas fiscais de uma
instituição e de um fornecedor, e daí segue para o detalhe dos itens ou das
deduções.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`:
é dado de navegação, não regra de negócio.

A `F150C` não é um menu: é uma tela de consulta, mostra **11 notas por vez** e não
grava em cadastro nenhum. Ela recebe da tela que a chamou o grupo, o ano de
competência, a instituição e o fornecedor já escolhidos, e trabalha em cima desse
recorte. Chamada pelo menu de despesas ela vem do próprio menu; chamada pela tela
de consulta de notas ela vem de lá — em qualquer dos dois casos o recorte é o que
veio de trás, e não o que se digita.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O servidor só vê as notas do grupo a que está vinculado

A tela trabalha sobre o grupo de coordenação regional da sessão. Informado um
grupo diferente daquele a que o servidor está vinculado, a consulta é recusada com
**\* Usuario sem acesso a outro grupo \***, com o cursor de volta ao campo do
grupo, e nada é mostrado. Só quando o grupo informado é o da sessão é que a tela
segue adiante — e é esse grupo que ela passa a usar no recorte da consulta.

[?] O grupo que a sessão carrega é também o que a tela escreve de volta no campo
do grupo ao abrir; se a máscara deixa digitar ali, o servidor não alcança outro
grupo, o que é o esperado da recusa. O que não se conseguiu determinar foi onde a
sessão é preenchida com esse grupo — a atribuição não está em nenhum dos programas
desta jornada, e a tela apenas copia o que já estava lá. Pergunta ao site.

### RN-02 — A tela é só de consulta

Ao abrir, a tela assume a consulta e permanece nela: não há caminho que inclua,
altere ou exclua nada. Nenhum cadastro é gravado, nenhum registro é travado e
nenhuma trilha de auditoria é gerada por esta tela, em nenhuma das suas respostas.
A consulta mostra; não decide situação de nota.

### RN-03 — O recorte da consulta vem de trás, não da digitação

O grupo, o ano de competência, a instituição e o fornecedor chegam definidos pela
tela que chamou esta, e a tela **reconfere** cada um deles ao ser respondida:

- **a instituição** — não havendo instituição cadastrada para o código
  informado, a recusa é **\* Instituicao beneficente nao cadastrada \***, com o
  cursor no campo da instituição, e nada é mostrado (o código em branco cai nessa
  recusa);
- **o ano de competência** — em branco, a recusa é **\* Informe o ano de
  competencia \***, com o cursor no campo do ano, e nada é mostrado;
- **o fornecedor** — não havendo fornecedor cadastrado para o número
  informado, a recusa é **\* Fornecedor nao cadastrado \***, com o cursor no
  campo do fornecedor, e nada é mostrado (o número em branco cai nessa recusa).

Além de preenchidos, os quatro valores têm de ser coerentes entre si: a
combinação grupo, ano de competência, instituição e fornecedor é a chave de uma
nota fiscal, e é com ela que a tela vai ler o cadastro no passo seguinte.

### RN-04 — A tela lista as notas fiscais do recorte, 11 por vez

Preenchido o recorte, a tela percorre o cadastro de notas fiscais pela combinação
grupo, instituição, ano de competência, fornecedor e número da nota, e preenche
**11 linhas** por página — o mesmo número, em todas as páginas. Cada linha traz o
número da nota, o ano, os valores de retenção, dedução, desconto e item, e a
situação da linha. A descrição do modelo da nota e o nome do órgão, que aparecem
junto da nota, vêm de outros dois cadastros, pelo modelo e pela instituição da
própria nota.

A leitura começa pela primeira nota do recorte e continua nota a nota; cada
página começa na nota seguinte à última que a página anterior mostrou.

[?] A tela não mostra em lugar nenhum a quantidade total de notas do recorte, nem
marca em que página está. Quem lê a tela isolada não tem como saber se há mais
notas depois das 11 — nem pelo que ela escreve, nem pelo que ela guarda. Se o
usuário espera ver essa informação, ela não está nesta tela nem no cadastro que
ela lê. Pergunta ao site.

### RN-05 — O que a tela mostra de valores e o sinal de diferença

Para cada nota, a tela mostra o **valor da nota**, o **valor retido**, o **valor
deduzido** e o **valor do item**. Ao lado delas ela calcula e mostra o **valor
retido mais o valor do item, menos o valor deduzido** — é a conta do que deveria
fechar com o valor da nota. Fechando, a linha fica limpa; não fechando, a tela
marca a linha com um asterisco, que é o aviso de que a nota tem diferença entre o
lançado e o calculado.

[?] A tela calcula esses valores ao abrir e ao responder, mas não os regrava em
lugar nenhum: se o item, a retenção ou a dedução de uma nota mudarem por outra
tela, o valor que aparece aqui só se refaz se a nota for lida de novo por este
caminho. Se o acervo espera que algum outro ponto recalcule esse resumo, ele não
está nesta tela nem no cadastro de notas. Pergunta ao site.

### RN-06 — A tela devolve a nota seguinte à última da página

Ao fechar uma página cheia, a tela guarda o recorte da página seguinte: grupo, ano
de competência, instituição, fornecedor e **o número da nota seguinte à última que
apareceu**. É esse número que a página seguinte usa para começar a leitura, e é
ele que a tela devolve para quem a chamou.

[?] Quando a página fecha sem que as notas do recorte tenham acabado, a tela zera
esse número em vez de guardar o da nota seguinte. A leitura seguinte, sem número,
pode recomeçar da primeira nota do recorte e repetir a página já vista. Se o
acerto de contas entre as páginas é feito por outro ponto do sistema, ele não está
neste acervo. Pergunta ao site.

### RN-07 — Sem nota fiscal no recorte, a tela avisa e não desce

Não havendo nenhuma nota fiscal para o grupo, a instituição, a competência e o
fornecedor informados, a tela avisa **\* Notas fiscais nao cadastradas \*** e
zera o número da nota inicial e o da nota seguinte. Nesse caso ela não leva às
telas de detalhe: a nota que não existe não tem item nem dedução para mostrar.

[?] O aviso só aparece quando o recorte é lido pela primeira vez. Numa página
seguinte sem notas o aviso não é dado, e a tela devolve o número da nota inicial
zerado — o mesmo que o caminho de página seguinte usa para dizer que há mais
notas a ler. Se o usuário vê o recorte vazio ou o fim do recorte, perguntou-se ao
site.

### RN-08 — Vale o ano da própria nota, e o contexto volta por cima

Depois de ler a nota, a tela volta a completar o recorte com o que está na própria
nota — o grupo do servidor, a instituição da nota, o nome do órgão, o fornecedor,
a razão social, o modelo da nota e o seu ano de competência. O contexto que a tela
devolve para quem a chamou fica sendo, portanto, o da nota lida e não o que veio
de trás, quando os dois divergem.

### RN-09 — A tela decide a continuação pela última linha da página

Terminando a página, a tela escolhe a tela seguinte pela **última linha que leu**:
se o valor deduzido daquela nota é zero e não há valor retido, ela encaminha para
o **detalhe dos itens da nota**; se há dedução ou há retenção, ela encaminha para
o **detalhe das deduções da nota**. Em qualquer dos casos ela leva junto o número
da nota lida e a descrição da tela de destino.

[?] A escolha é feita por uma única linha — a última da página — e não pelo
recorte nem pela nota que o usuário está olhando. A tela ainda encaminha ao
detalhe mesmo quando a última linha não tem número de nota e o recorte é o de uma
consulta sem nota nenhuma, porque o encaminhamento não reconfere o número
preenchido: ele passa pela mesma leitura da notificação de linha não preenchida.
Se o encaminhamento deveria parar quando não há nota, ou deveria seguir a nota
selecionada, pergunta ao site.

### RN-10 — A linha com situação de preenchimento e sem número de nota é recusada

A leitura da nota traz a situação da linha. Quando a situação é a de linha a
preencher e o número da nota está zerado, a tela recusa com **\* Linha nao
preenchida \***, com o cursor na linha, e nada é mostrado. Quando a situação é
qualquer outra, a tela segue e não recusa: a conferência do número só é feita
para a linha marcada como a preencher.

[?] A tela não preenche a situação da linha em nenhum ponto — ela lê a situação
do cadastro de notas e o número da nota da mesma linha, e a recusa só acontece com
a situação marcada como a preencher. Se o cadastro não guarda essa marca, o
caminho de recusa por linha não preenchida nunca é alcançado, e uma linha sem
número de nota passa direto para o encaminhamento ao detalhe. Pergunta ao site.

### RN-11 — Só o perfil autoriza, e a tela diz isso na abertura e a cada resposta

Na abertura, a tela consulta o cadastro de telas pela sua identificação e passa
pela conferência de acesso; não achando a tela no cadastro de telas, ou não tendo
o código de acesso de quem opera a tela liberada, a tela é abandonada com aviso e
nada é mostrado. A mesma conferência de acesso é repetida a cada resposta, sempre
com a descrição da tela e o código de acesso da sessão.

[?] O texto dos avisos de acesso negado e a identificação por que a tela é
conhecida no cadastro de telas não estão no acervo: a tela copia o que leu do
cadastro, e o conteúdo do cadastro de telas não veio no lote. Os nomes usados
aqui vêm do próprio programa e do cadastro de dados, não da máscara da tela.
Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar as notas fiscais do grupo, da instituição e do fornecedor

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F150C

  Cenário: Abrir a tela mostra as notas fiscais do recorte, 11 por vez
    Dado que recebi da tela anterior o grupo, o ano de competência, a instituição e o fornecedor
    E há notas fiscais para esse recorte
    Quando abro a tela F150C
    Então vejo as notas do recorte, até 11 por vez, com o número e o ano de cada uma
    E a tela abre em consulta
    E nada é gravado

  Cenário: A consulta não grava nada
    Dado que abri a tela e ela mostra as notas fiscais do recorte
    Quando respondo a tela quantas vezes forem necessárias
    Então o cadastro de notas é apenas lido
    E nenhuma nota é incluída, alterada ou apagada
    E nenhuma trilha de auditoria é gerada

  Cenário: Os valores da nota e o sinal de diferença
    Dado que abri a tela F150C
    Quando olho uma linha
    Então vejo o valor da nota, o valor retido, o valor deduzido e o valor do item
    E vejo o valor retido mais o valor do item, menos o valor deduzido
    E a linha aparece com um asterisco quando essa conta não fecha com o valor da nota

  Cenário: O recorte sem nenhuma nota fiscal
    Dado que recebi um recorte para o qual não existe nota fiscal
    Quando abro a tela F150C
    Então vejo a mensagem "* Notas fiscais nao cadastradas *"
    E não sou levado ao detalhe da nota

  Cenário: Grupo diferente do meu
    Dado que recebi um recorte cujo grupo é diferente do grupo da minha sessão
    Quando abro a tela F150C
    Então vejo a mensagem "* Usuario sem acesso a outro grupo *"
    E o cursor volta ao campo do grupo
    E nada é mostrado

  Cenário: Instituição não informada no recorte
    Dado que recebi um recorte sem a instituição
    Quando abro a tela F150C
    Então vejo a mensagem "* Instituicao beneficente nao cadastrada *"
    E o cursor volta ao campo da instituição
    E nada é mostrado

  Cenário: Ano de competência não informado no recorte
    Dado que recebi um recorte sem o ano de competência
    Quando abro a tela F150C
    Então vejo a mensagem "* Informe o ano de competencia *"
    E o cursor volta ao campo do ano de competência
    E nada é mostrado

  Cenário: Fornecedor não informado no recorte
    Dado que recebi um recorte sem o fornecedor
    Quando abro a tela F150C
    Então vejo a mensagem "* Fornecedor nao cadastrado *"
    E o cursor volta ao campo do fornecedor
    E nada é mostrado

  Cenário: Linha marcada para preencher e sem número de nota
    Dado que abri a tela F150C
    E uma linha veio marcada como linha a preencher e sem número de nota
    Quando respondo a tela
    Então vejo a mensagem "* Linha nao preenchida *"
    E o cursor volta para essa linha
    E nada é mostrado

  Cenário: Continuar pelo detalhe dos itens da nota
    Dado que abri a tela F150C com um recorte que tem notas
    E a última linha da página é de uma nota sem valor deduzido e sem valor retido
    Quando respondo a tela
    Então sou encaminhado ao detalhe dos itens dessa nota

  Cenário: Continuar pelo detalhe das deduções da nota
    Dado que abri a tela F150C com um recorte que tem notas
    E a última linha da página é de uma nota com dedução ou com retenção
    Quando respondo a tela
    Então sou encaminhado ao detalhe das deduções dessa nota

  Cenário: A tela não consta do cadastro de telas
    Dado que a tela F150C não consta do cadastro de telas
    Quando abro a tela F150C
    Então sou avisado de que a tela não está disponível
    E não consigo consultar as notas

  Cenário: Meu código de acesso não tem a tela
    Dado que o meu código de acesso não tem a tela F150C liberada
    Quando abro a tela F150C
    Então sou avisado de que o acesso à tela foi negado
    E não consigo consultar as notas
```
