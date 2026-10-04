# US — M022C — Escolher o mês de referência do órgão

## Estória

Como **servidor de CRE**, quero **escolher um dos meses de referência já existentes para o tipo de
órgão da minha sessão e informar a coordenação regional escolar**, para que **eu chegue aos registros
daquele mês daquela coordenação sem digitar a referência de cor e sem adivinhar quais meses estão
abertos**.

Os registros de um mês são mantidos por **coordenação regional escolar**, e é por coordenação e por
mês que se chega a eles: quem não sabe quais meses existem erra a referência e não chega a registro
nenhum. Esta tela é o índice dos meses já existentes para o tipo de órgão do servidor — mostra quais
são e quando foram atualizados — e leva à relação daquele mês daquela coordenação. Nada aqui é
gravado: os registros do mês são mantidos na tela seguinte.

## Contexto

Jornada S000M → M000M → M022C.

Ator: servidor de CRE — escolhe um dos meses de referência do órgão, informa a coordenação regional
escolar da linha e abre a relação dos registros daquele mês daquela coordenação.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual menu
a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de
negócio.

As regras abaixo são só as da tela desta jornada. Os dois menus do caminho não gravam nada: só
encaminham. Esta tela também não grava — ela consulta e **encadeia** para a relação dos registros do
mês, a M019T; o que ela deixa para a tela seguinte está na RN-06. **Nada nesta tela muda conforme a
tela que a abriu**: não há no fonte nenhuma conferência da tela de origem, e a única coisa que pode
vir de outra tela é a operação guardada na área da sessão, que é a RN-02. As conferências de tela, de
estação, de rota e de permissão que a M022C executa antes de aceitar a operação são as mesmas de
todas as telas e já estão no documento da entrada: ficam no anexo de evidências, em **Regras que se
revelaram da entrada**.

---

## Regras de negócio

### RN-01 — A tela relaciona os meses de referência do órgão e não grava nada

A M022C é uma tela de **consulta**. Ela relaciona os **meses de referência** já existentes para o
**tipo de órgão** da sessão — um mês por linha — e, de cada mês, mostra a **referência** (mês e ano) e
a **data de atualização**. Cada linha tem ainda duas colunas que a relação não preenche e que o
servidor usa na linha escolhida: a **coordenação regional escolar** e o **indicador de seleção**. O
cabeçalho mostra a **operação**, a descrição do **tipo de órgão** da sessão e a **data do sistema**.

Nada nesta tela é gravado: nem cadastro, nem travamento de registro, nem linha de auditoria. São
**sete** as mensagens que a tela sabe mostrar, e todas são recusas ou avisos — não há aviso de
sucesso.

[?] O que são, em negócio, esses meses de referência. O cadastro que a tela lê **não está no
dicionário de dados lido**: o dicionário da base não traz esse cadastro, nem os seus campos, nem a
sua chave, nem a sua capacidade. O que se sabe dele é o formato trazido pelo próprio programa, e as
mensagens da tela o tratam como cadastro. Pergunta ao site.

[?] Em que ordem a relação vem. A tela começa pelo mês de **maior** referência do órgão, mas o
sentido em que caminha a partir dele depende de sinalizadores de leitura cuja semântica não está no
material lido: não se confirma se a relação vem do mês mais recente para o mais antigo. Pergunta ao
site.

### RN-02 — Só a consulta é aceita

A tela só trabalha em **consulta**. Confirmando com qualquer outra operação no campo da operação, a
recusa é **\* Operacao nao disponivel. Use CON \***, com o cursor de volta nesse campo, e nada é
conferido nem gravado.

A operação que a tela mostra ao abrir é a que ficou guardada na **área da sessão** — a mesma área em
que as telas deixam o que passam adiante; chegando em branco, é reposta como **consulta**. Quando a
operação aceita é a consulta, ela volta para essa área, e é ela que a tela seguinte lê.

[?] Se a operação guardada vem da última utilização ou só da tela que abriu esta. A marca que decide
se a área da sessão é reiniciada vive numa área comum a todas as telas do sistema, e o que ela faz de
um acesso do servidor para o outro não está no material lido: se a área sobrevive, a tela reabre com
a operação da última utilização — inclusive uma que ela mesma vai recusar; se é reiniciada, abre
sempre em consulta. Pergunta ao site.

[?] O que a máscara mostra no campo da operação: a tela confere o código interno da consulta e a
mensagem manda usar **CON**. O que o servidor vê nesse campo não está no material lido. Pergunta ao
site.

### RN-03 — A passagem só acontece pela linha marcada, e a linha tem de estar preenchida

A tela só abre a relação do mês pela **linha marcada**. Marcando uma linha **sem referência** e
confirmando, a recusa é **\* Informe linha preenchida \***, com o cursor no **indicador de seleção**
daquela linha, e nada é aberto.

Confirmando **sem** marcar nenhuma linha, a tela não abre nada e não grava nada: ela aproveita a
confirmação para guardar a referência em que a página parou — que é por onde a relação continua — e
segue mostrando a relação. É o caminho de quem está só percorrendo a lista.

[?] O que marca a linha. O indicador de seleção é lido e exibido, mas o material lido só mostra o
literal que dispara a passagem ("S", a mesma letra de "sim"): a tela não tem conferência de valor
para esse campo, não tem mensagem própria para ele e não traz o rótulo que o servidor vê. Pergunta ao
site.

### RN-04 — A coordenação regional escolar é obrigatória, tem de estar cadastrada e tem de ser a do vínculo

A **coordenação regional escolar** da linha marcada é o filtro da passagem, e passa por três
conferências:

- **em branco** — recusa **\* Informe o grupo \***, com o cursor no campo da coordenação daquela
  linha;
- **não cadastrada** para o tipo de órgão da sessão — recusa **\* Grupo nao cadastrado \***, com o
  cursor no mesmo campo;
- **diferente da coordenação do vínculo** do servidor — recusa
  **\* Usuario sem acesso a este grupo \***, com o cursor no mesmo campo.

Em qualquer das três, nada é consultado e nada é aberto. As mensagens chamam a coordenação de
**"grupo"**.

[?] A terceira conferência só acontece quando o vínculo do servidor **tem** uma coordenação: com o
vínculo sem coordenação, qualquer coordenação cadastrada passa. Se o vínculo sem coordenação deveria
ser recusado, falta a recusa. Pergunta ao site.

### RN-05 — A referência marcada tem de ter registros daquela coordenação naquele mês

Escolhido o mês, aquele mês tem de ter **registros cadastrados** daquela coordenação. A procura usa a
**coordenação informada**, a **referência da linha** (mês e ano, lidos do que a linha mostra) e a
**data de atualização que a linha mostra**: não achando, a recusa é
**\* Grupo sem registros cadastrados \***, com o cursor de volta no campo da coordenação, e nada é
aberto.

[?] A data de atualização da linha entra na procura. A tela mostra a data que veio do cadastro do mês
e procura os registros com aquela mesma data; se a data do mês e a data das linhas daquele mês não
forem a mesma, a tela recusa como se não houvesse registro. Quem mantém as duas iguais não está no
material lido. Pergunta ao site.

### RN-06 — A linha marcada abre a relação dos registros do mês, em consulta

Passando as conferências, a M022C não segue com operação própria: ela deixa na área da sessão a
**coordenação informada**, a **referência da linha** (mês e ano) e a **data de atualização** daquele
mês, com a operação em **consulta**, descarta o **órgão filho** que a tela tinha, e passa para a
**relação dos registros do mês** (M019T) — que abre, por isso, em **consulta** naquele mês. É por
essa passagem que a jornada termina.

[?] A coordenação que esta tela entrega é a mesma que a tela seguinte confere contra o vínculo, e a
tela seguinte a substitui pela do vínculo quando ela existe. Por este caminho, a coordenação
informada só vale se for a do vínculo. Se a passagem deveria alcançar outra coordenação, falta a
conferência. Pergunta ao site.

### RN-07 — A relação vem em quatorze linhas por página

A relação é montada em **quatorze** linhas por vez, e cada linha é um mês de referência com a sua
data de atualização. Chegando ao fim da página, a tela pede ao ambiente a linha seguinte, uma a uma,
até preencher a página; a relação **para no primeiro mês em que não encontra registro** — ou quando o
registro achado é de outro tipo de órgão. O rodapé guarda a referência da última linha da página, que
é por onde a página seguinte continua.

[?] A continuação da página. A tela guarda a referência da última linha lida e recomeça a leitura por
ela, mas os sinalizadores com que pede a linha seguinte não têm semântica no material lido: não se
confirma que a página seguinte continue exatamente depois da última linha. Pergunta ao site.

### RN-08 — Sem mês de referência para o órgão, a tela avisa

Não havendo **nenhum mês de referência** cadastrado para o tipo de órgão da sessão, a tela avisa
**\* Nao existem registros cadastrados \*** e não relaciona nada. É a primeira linha da página que
decide o aviso: a falta só é anunciada quando a relação não achou o primeiro mês.

### RN-09 — Os campos de código desta tela passam pela conferência de número

Três campos — a **coordenação da linha** e as duas **referências do rodapé** (o mês e o ano por onde
a página continua) — passam por uma conferência de **número** antes de a tela procurar os registros:
o que não for número é recusado no próprio campo. Nos três, o que chega em branco é tratado como
zero.

A **referência da linha**, que a tela mostra como texto, **não** passa por essa conferência: ela é
conferida apenas por não estar em branco e depois convertida de volta a número, sem conferência de
formato.

[?] O que a tela faz depois da recusa e para onde o cursor volta. A conferência de número é uma
rotina externa, e o corpo dela não está no material lido: não se sabe a mensagem que o servidor vê
nem como a tela segue depois dela. A rotina desta tela posiciona o cursor nos três campos citados.
Pergunta ao site.

[?] A referência da linha lida como texto. Não havendo conferência de formato, um texto fora do
formato mês/ano passa pela guarda de linha preenchida e vira a chave da procura. Se a referência
deveria ser conferida aqui, falta a conferência. Pergunta ao site.

### RN-10 — A tela não processa a confirmação quando chega prefixada por outra

Chegando a confirmação com o **campo da tela seguinte** preenchido — a marca de que ela foi aberta
por outra tela como tela encadeada —, a M022C não processa a confirmação: nada é conferido, nada é
aberto e nada é gravado. A confirmação também para quando a **marca de erro** que a própria tela
escreve ao passar adiante já está posta, o que encerra o processamento das linhas restantes da mesma
confirmação.

[?] O que preenche o campo da tela seguinte não está no material lido, e nada na jornada o preenche:
não se sabe qual tela o manda nem o que o servidor vê quando isso acontece. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Escolher um mês de referência do órgão e a coordenação regional escolar para abrir os registros daquele mês

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela M022C

  Cenário: RN-01 — consultar os meses de referência do tipo de órgão
    Dado que o tipo de órgão da minha sessão tem meses de referência existentes
    Quando abro a tela M022C
    Então vejo a relação dos meses de referência daquele órgão
    E vejo, de cada mês, a referência e a data de atualização
    E vejo a operação, a descrição do tipo de órgão e a data do sistema no cabeçalho
    E cada linha tem a coluna da coordenação regional escolar e o indicador de seleção para eu preencher

  Cenário: RN-01 — a consulta não grava nada
    Dado que abro a tela e percorro a relação
    Quando a relação é montada
    Então nenhum registro é travado
    E nenhum cadastro é gravado
    E nenhuma linha nova aparece na trilha de auditoria

  Cenário: RN-02 — a tela abre em consulta
    Dado que a área da sessão não tem operação guardada
    Quando abro a tela M022C
    Então a tela abre em consulta

  Cenário: RN-02 — a tela abre com a operação que ficou guardada
    Dado que a área da sessão tem uma operação guardada
    Quando abro a tela M022C
    Então o campo da operação já está preenchido com a operação guardada

  Cenário: RN-02 — operação diferente de consulta é recusada
    Dado que estou na tela M022C
    Quando a tela chega com uma operação que não é a consulta
    Então vejo "* Operacao nao disponivel. Use CON *"
    E o cursor fica no campo da operação
    E nada é conferido e nada é gravado

  Cenário: RN-03 — linha marcada sem referência
    Dado que marco o indicador de seleção de uma linha sem referência
    Quando confirmo
    Então vejo "* Informe linha preenchida *"
    E o cursor fica no indicador de seleção daquela linha
    E nada é aberto

  Cenário: RN-03 — confirmar sem marcar nenhuma linha
    Dado que a relação mostra os meses do órgão
    Quando confirmo sem marcar nenhuma linha
    Então nenhuma tela se abre
    E nada é gravado
    E a tela segue mostrando a relação

  Cenário: RN-04 — coordenação em branco
    Dado que marco uma linha preenchida
    Quando deixo a coordenação regional escolar em branco e confirmo
    Então vejo "* Informe o grupo *"
    E o cursor fica no campo da coordenação daquela linha
    E nada é consultado e nada é aberto

  Cenário: RN-04 — coordenação não cadastrada
    Dado que marco uma linha preenchida
    Quando informo uma coordenação que não existe para o tipo de órgão da sessão
    Então vejo "* Grupo nao cadastrado *"
    E o cursor fica no campo da coordenação daquela linha
    E nada é consultado e nada é aberto

  Cenário: RN-04 — coordenação que não é a do vínculo
    Dado que marco uma linha preenchida
    E a minha sessão tem uma coordenação no vínculo
    Quando informo outra coordenação cadastrada
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor fica no campo da coordenação daquela linha
    E nada é consultado e nada é aberto

  Cenário: RN-05 — a coordenação não tem registros naquele mês
    Dado que marco a linha de um mês
    E informo uma coordenação cadastrada que não tem registros naquele mês
    Quando confirmo
    Então vejo "* Grupo sem registros cadastrados *"
    E o cursor fica no campo da coordenação daquela linha
    E nada é aberto

  Cenário: RN-06 — a linha marcada abre a relação dos registros do mês
    Dado que marco a linha de um mês
    E informo a coordenação do meu vínculo
    E aquela coordenação tem registros naquele mês
    Quando confirmo
    Então a relação dos registros do mês abre, em consulta, naquele mês daquela coordenação
    E nada é gravado por esta tela

  Cenário: RN-06 — o que a tela entrega à tela seguinte
    Dado que marco a linha de um mês preenchido
    Quando confirmo
    Então a tela seguinte abre com a coordenação informada, a referência daquele mês e a data de atualização da linha
    E ela abre em consulta
    E o órgão filho que esta tela tinha é descartado

  Cenário: RN-07 — a relação em páginas de quatorze linhas
    Dado que o órgão tem mais meses de referência do que cabem na página
    Quando abro a tela M022C
    Então vejo os quatorze primeiros
    E o rodapé guarda a referência da última linha da página
    E a relação continua a partir dali

  Cenário: RN-07 — a relação para no primeiro mês sem registro
    Dado que os meses de referência do órgão acabam antes do fim da página
    Quando abro a tela M022C
    Então a relação para naquela altura
    E nenhuma linha sem registro é mostrada

  Cenário: RN-08 — o órgão não tem mês de referência
    Dado que o tipo de órgão da minha sessão não tem nenhum mês de referência
    Quando abro a tela M022C
    Então vejo "* Nao existem registros cadastrados *"
    E nenhuma linha é relacionada

  Cenário: RN-09 — campo com texto em vez de número
    Quando informo texto em um dos códigos desta tela
    Então o campo é recusado no próprio campo, pela conferência de número
    E a tela não procura os registros com esse texto

  Cenário: RN-10 — a tela chega prefixada por outra
    Dado que a tela chega com o campo da tela seguinte preenchido
    Quando confirmo
    Então nada é conferido, nada é aberto e nada é gravado
```
