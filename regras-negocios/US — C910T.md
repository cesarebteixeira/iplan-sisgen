# US — C910T — Consulta da composição do cardápio

## Estória

Como **servidor de CRE**, quero **consultar quais gêneros compõem o cardápio de um
segmento num período de validade, com a quantidade de cada um**, para que **eu confira o
que aquele segmento tem previsto para o período e possa seguir para as refeições ligadas
àquele cardápio**.

O cardápio de um período é montado gênero a gênero, segmento por segmento: é a lista dos
gêneros, com a quantidade de cada um, que diz o que será servido. Sem essa lista, o
cardápio é apenas um código com uma data — não há como saber o que ele prevê, nem
conferir quanto cada segmento recebe. É também desta tela que sai a passagem para as
refeições do período, para que as refeições sejam ligadas ao cardápio que já está montado.

## Contexto

Jornada S000M → C000M → C800M → C900M → C910T.
Ator: servidor de CRE — consulta a composição do cardápio de um segmento num período e,
quando é o caso, segue para as refeições daquele cardápio.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção
de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

O caminho até aqui é todo por menu: o C000M, o C800M e o C900M são menus, não gravam nada
e só encaminham. O contexto que esta tela usa — o tipo de órgão, a coordenação regional
escolar, a matrícula, o código de acesso, o privilégio e a data do sistema — é o que a
entrada deixou na sessão; isso é regra da entrada e está no anexo de evidências, em
**Regras que se revelaram da entrada**.

Esta tela é só de consulta (RN-02): ela não inclui, não altera e não exclui nada. O que
ela tem de próprio é a passagem: quando o servidor pede as refeições, ela entrega o
cardápio à tela das refeições (`C915T`), que abre em consulta com esse cardápio carregado
(RN-08).

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela consulta os gêneros que compõem o cardápio de um segmento e de um período

A tela mostra a composição do cardápio: para um código de cardápio, um segmento e um
período de validade, ela lista os gêneros que entram naquele segmento, um a um, com a
quantidade de cada um. A composição é guardada **gênero a gênero** — cada gênero do
cardápio é um registro do cadastro, identificado pelo tipo de órgão, pelo cardápio, pelo
segmento, pelo período e pelo par subclasse–gênero —, e esse cadastro tem **treze campos**
e capacidade para **100.000 registros** (capacidade é o máximo esperado que o dicionário
declara, parâmetro de dimensionamento, não o volume cadastrado).

A tela enxerga **seis** cadastros e não grava nenhum: o título das telas (2.000), o gênero
do cardápio (100.000), o cardápio do período (100.000), o segmento (200.000), o cadastro
de gêneros (150.000) e o cadastro de conversão dos gêneros da subclasse 99 (100.000).

### RN-02 — A tela abre em consulta e só aceita consulta

Ao abrir, se a área de trabalho da sessão não trouxer operação nenhuma, a tela assume
**consulta (CON)** e não carrega cardápio nenhum. Informada qualquer operação que não seja
a consulta, o sistema recusa com **\* Opcao nao disponivel. Use CON \***, devolve o cursor
ao campo da operação e não lê cadastro nenhum por causa disso.

[?] A recusa só é alcançada numa mensagem do servidor, porque a abertura da tela já repõe
a consulta sozinha. Se a máscara não oferecer ao servidor o campo da operação, a recusa é
trecho sem uso. Pergunta ao site.

[?] A área de trabalho é a mesma para todas as telas da sessão e nenhum dos menus deste
caminho a zera: se ela chegar com resíduo de outra tela — uma operação de alteração, por
exemplo —, esta tela abre com aquela operação e com o cardápio daquele resíduo, e a
alteração é recusada por esta guarda. Se o ambiente limpa essa área a cada transação, o
material não diz. Pergunta ao site.

### RN-03 — A grade tem doze linhas, uma por gênero do cardápio naquele segmento

A lista é uma página de **doze** linhas, uma por gênero do cardápio naquele segmento e
naquele período. Cada linha traz **sete** informações: a subclasse (2 dígitos), o código
do gênero (5), a quantidade do gênero no cardápio (quatro inteiros e seis decimais,
mostrada com vírgula), a descrição resumida do gênero (15 caracteres), a marca da linha
(1 caractere), a conversão do gênero (cinco inteiros e três decimais, também com vírgula)
e o padrão de conversão (2 caracteres).

A tela percorre o cadastro do cardápio e vai montando as linhas, uma leitura por linha,
pela chave do cadastro. Não achando gênero nenhum, a tela avisa
**\* Cardapio sem generos cadastrados \*** e não monta linha nenhuma; o aviso é decidido na
montagem da primeira linha e não se repete nas demais.

### RN-04 — A descrição e a conversão de cada gênero vêm do cadastro de gêneros

A descrição resumida e a conversão não ficam no cardápio: a tela vai buscá-las no cadastro
de gêneros, pela subclasse e pelo gênero, **na data limite do período**. Não achando o
gênero, a linha mostra **Nao cadastrado** no lugar da descrição.

Há um cadastro de conversão separado, usado quando a subclasse do gênero é a de código
**99**: nesse caso a descrição e a conversão vêm dele, e a linha recebe um asterisco.

[?] O que a subclasse de código 99 significa no negócio — e por que ela usa um cadastro de
conversão próprio — não vem do material lido; nem o que o asterisco quer dizer. Pergunta ao
site.

[?] O gênero é procurado com a **data limite** do período no lugar da data de início dele:
se o cadastro de gêneros guarda versões por data, um gênero cadastrado depois do início do
período e antes do limite é achado, e o que valia no início não. Se é isso o pretendido, o
material não diz. Pergunta ao site.

### RN-05 — Fora da grade a tela mostra o tipo de órgão, a data do sistema, o segmento e as marcas

Fora da grade, a tela exibe a descrição do tipo de órgão da sessão, a data do sistema, a
descrição do segmento do período em tela e as marcas de sobremesa e de fruta, escritas por
extenso como **Sim** ou **Nao**; a marca que não vier preenchida aparece como **Nao**.

[?] Nem a descrição do tipo de órgão nem a data do sistema são preenchidas por nenhum
caminho que o acervo deste lote mostre: as duas aparecem sempre como origem de cópia, e a
entrada guarda os dois valores na área da sessão. Se o ambiente transporta um valor para o
outro, é pergunta ao site; se não transportar, os dois campos saem em branco.

### RN-06 — A consulta é pelo código do cardápio, pelo segmento e pela data limite, dentro do tipo de órgão da sessão

O servidor informa **o código do cardápio**, **o código do segmento** e **o dia, o mês e o
ano limite** do período; a procura é sempre dentro do **tipo de órgão da sessão**. Reenviar
exatamente o que já está em tela não provoca nova procura: os valores informados são
aceitos como estão.

Se a chave mudou e o código do cardápio está zerado, a recusa é
**\* Informe o codigo do cardapio \***, com o cursor no campo do cardápio. Passando, o
segmento tem de existir no cadastro de segmentos — não existindo,
**\* Segmento nao cadastrado \***, com o cursor no campo do segmento. A data limite tem de
estar informada nos três componentes — dia, mês ou ano zerado é
**\* Informe a data limite de validade \***, com o cursor no dia do limite. O cardápio tem
de existir naquele período — não existindo, **\* Cardapio nao cadastrado \***, com o
cursor no campo do cardápio. E o segmento tem de estar previsto naquele cardápio — não
estando, **\* Segmento nao cadastrado neste cardapio \***, com o cursor no campo do
segmento. Em todas as recusas nada é gravado.

Passando por todas, o cardápio fica carregado na área de trabalho da sessão e a tela passa
a mostrar a descrição daquele cardápio. O cardápio é procurado pelo **tipo de órgão, pela
data limite e pelo código**: a **data de início** não entra na procura — ela vem do
registro achado.

[?] A procura usa o recurso de posicionamento do dicionário de dados e a tela confere de
volta a chave lida. Se a leitura exige a chave exata, só consulta o cardápio quem sabe a
data limite; se ela apenas posiciona, o registro vizinho é recusado pela conferência. Os
dois comportamentos são compatíveis com o que o material mostra. Pergunta ao site.

[?] A lista de gêneros é montada na apresentação da tela, e o acervo não mostra o que a
remonta quando a chave é informada dentro da mesma transação: o caminho da consulta carrega
a chave na área da sessão e não relê as linhas. Se o servidor precisa reabrir a tela para
ver a lista do cardápio novo, é pergunta ao site.

### RN-07 — O que se digita é conferido como número antes de qualquer leitura

**Onze** campos passam pela edição numérica antes de qualquer leitura de cadastro, com o
cursor de volta ao campo recusado: o código do cardápio (5 posições), o código do segmento
(2), o dia, o mês e o ano de início (2, 2 e 4), o dia, o mês e o ano limite (2, 2 e 4), a
subclasse (2), o gênero (5) e a quantidade do gênero no cardápio (quatro inteiros e seis
decimais). Campo em branco vale zero. A quantidade admite **vírgula** como separador
decimal. Não passam por essa edição: a operação, a marca de sobremesa e a marca de fruta.

[?] O texto dessa recusa não está no material: a edição é uma rotina de biblioteca, cujo
corpo não faz parte do lote, e o texto sai da tabela de mensagens do idioma, que também não
está no lote. Pergunta ao site.

### RN-08 — Quando o servidor pede as refeições, a tela não consulta: ela entrega o cardápio

Quando a marca de passagem para as refeições está posta, esta tela **não faz a consulta**:
ela confere que o cardápio existe naquele segmento e naquele período — não existindo,
recusa com **\* Cardapio nao cadastrado \*** e o cursor no código do cardápio — e entrega a
transação à tela das refeições (`C915T`).

O que ela entrega: a identificação de que a tela de origem é ela, a operação de
**consulta**, o cardápio e a sua descrição, o segmento e a sua descrição, as duas datas do
período, as marcas de sobremesa, fruta e estimativa, as quatro marcas de um caractere do
cardápio (que a tela das refeições acende como **X** quando vêm preenchidas) e o código do
cardápio de sobremesa. A tela das refeições abre em **consulta** com esse cardápio
carregado e, porque a origem é esta tela, **sem nenhuma refeição escolhida** — é esse o
efeito de encadear tela em tela, sem menu no meio.

[?] A marca de passagem é um campo de um caractere que a tela só escreve como **N**, na
montagem da última linha da grade, e nunca como **S**; nenhum rótulo da ficha da tela
corresponde a ele. Quem a preenche com **S** — o formulário, um comando, ou outra tela — o
material não diz. Pergunta ao site.

### RN-09 — A tela não lê a tela de origem; ela é que decide a origem da seguinte

A tela não consulta de onde veio: ela não lê o código da tela de origem em ponto nenhum —
só o escreve, e só para a tela das refeições ler (RN-08). O modo em que ela abre vem da
operação que a área de trabalho da sessão guardar (RN-02), e não de um código de tela. Quem
decide a origem é ela: a tela das refeições é que reage ao código desta tela (RN-08).

[?] A tela recebe, exibe e repassa adiante um campo de **próxima tela** (5 posições) que,
quando preenchido, encerra a transação sem processar nada. Nenhum menu deste caminho o
preenche, e o acervo não traz o rótulo que o servidor vê nele nem o que ele deve digitar.
Pergunta ao site.

### RN-10 — A consulta não grava nada e não deixa rastro

A tela só lê. Nenhum registro é incluído, alterado ou excluído, e nenhum registro de
auditoria é gerado. As operações de gravação, de exclusão e de travamento de registro
existem declaradas para os cadastros que a tela enxerga, mas **não são executadas em
nenhum caminho**: declarar não é executar. A passagem de gravação da transação existe e
não faz outra coisa senão devolver a área de trabalho.

### RN-11 — O cadastro dos gêneros do cardápio não tem tela de manutenção no acervo lido

O cadastro dos gêneros do cardápio, que esta tela lista, não é gravado por nenhuma tela do
acervo lido: nenhuma inclui, altera ou exclui registro nele. Os únicos outros programas que
o mencionam são programas de trabalho em lote dos relatórios do módulo — um deles apaga
registros dele. O mesmo tipo de cadastro, na outra linha de menu do módulo, tem tela de
manutenção no acervo lido; este, não.

[?] Quem alimenta o cadastro dos gêneros do cardápio no dia a dia — e por qual caminho —
não se conclui das telas do acervo lido. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar a composição do cardápio de um segmento e passar para as refeições

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C910T

  Cenário: RN-01, RN-03 — consultar a composição do cardápio de um segmento
    Dado que a tela recebe apontados o cardápio, o segmento e a data limite do período
    Quando a tela abre
    Então vejo até doze linhas, uma por gênero daquele cardápio naquele segmento
    E cada linha traz a subclasse, o gênero, a descrição resumida, a conversão e a quantidade do gênero no cardápio
    E nada é gravado

  Cenário: RN-02, RN-09 — abrir a tela sem operação guardada
    Dado que nenhuma tela desta sessão deixou operação na área de trabalho
    Quando abro a tela C910T pela opção do menu
    Então ela abre em consulta
    E não traz cardápio carregado
    E o modo de abertura não depende de qual tela me mandou

  Cenário: RN-02 — operação diferente de consulta
    Quando informo no campo da operação uma operação que não é a consulta
    Então vejo "* Opcao nao disponivel. Use CON *"
    E o cursor volta para o campo da operação
    E nenhum cadastro é lido

  Cenário: RN-03 — a página de doze linhas
    Dado que o cardápio tem gêneros naquele segmento e naquele período
    Quando a tela é apresentada
    Então vejo até doze linhas, uma por gênero, e as demais ficam em branco
    E a quantidade de cada gênero aparece com vírgula decimal

  Cenário: RN-03 — cardápio sem gêneros
    Dado que o cardápio não tem gênero nenhum naquele segmento e naquele período
    Quando a tela é apresentada
    Então vejo "* Cardapio sem generos cadastrados *"
    E nenhuma linha da grade é montada

  Cenário: RN-04 — gênero fora do cadastro de gêneros
    Dado que a subclasse e o gênero de uma linha não existem no cadastro de gêneros
    Quando a tela monta aquela linha
    Então a descrição da linha aparece como "Nao cadastrado"

  Cenário: RN-04 — gênero da subclasse 99
    Dado que a subclasse de uma linha é a de código 99
    Quando a tela monta aquela linha
    Então a descrição e a conversão vêm do cadastro de conversão próprio
    E a linha fica marcada com um asterisco

  Cenário: RN-05 — o que a tela mostra fora da grade
    Dado que há um cardápio carregado
    Quando a tela é apresentada
    Então vejo a descrição do tipo de órgão, a data do sistema e a descrição do segmento
    E a marca de sobremesa e a de fruta aparecem por extenso, como "Sim" ou "Nao"

  Cenário: RN-06 — consultar por uma chave informada
    Dado que informo outro código de cardápio, com o segmento e o dia, o mês e o ano limite
    Quando confirmo a consulta
    Então o sistema confere que o segmento existe, que o cardápio existe naquele período e que o segmento está previsto nele
    E o cardápio fica carregado como o cardápio da consulta
    E nada é gravado

  Cenário: RN-06 — consulta sem o código do cardápio
    Dado que mudei a chave e deixei o código do cardápio zerado
    Quando confirmo a consulta
    Então vejo "* Informe o codigo do cardapio *"
    E o cursor volta para o campo do cardápio
    E nada é gravado

  Cenário: RN-06 — segmento não cadastrado
    Dado que informo um código de segmento que não existe no cadastro de segmentos
    Quando confirmo a consulta
    Então vejo "* Segmento nao cadastrado *"
    E o cursor volta para o campo do segmento
    E nada é gravado

  Cenário: RN-06 — consulta sem a data limite
    Dado que deixo zerado o dia, o mês ou o ano da data limite
    Quando confirmo a consulta
    Então vejo "* Informe a data limite de validade *"
    E o cursor volta para o dia da data limite
    E nada é gravado

  Cenário: RN-06 — cardápio não cadastrado naquele período
    Dado que não existe cardápio com aquele código naquela data limite
    Quando confirmo a consulta
    Então vejo "* Cardapio nao cadastrado *"
    E o cursor volta para o campo do cardápio
    E nada é gravado

  Cenário: RN-06 — segmento não previsto naquele cardápio
    Dado que o cardápio existe, mas não tem aquele segmento
    Quando confirmo a consulta
    Então vejo "* Segmento nao cadastrado neste cardapio *"
    E o cursor volta para o campo do segmento
    E nada é gravado

  Cenário: RN-07 — campo com texto
    Quando preencho o código do cardápio, o segmento, uma das datas, a subclasse, o gênero ou a quantidade com letra
    Então a tela recusa o campo antes de qualquer leitura de cadastro
    E o cursor volta para o campo recusado
    E nada é consultado por causa dele

  Cenário: RN-08 — a passagem para as refeições
    Dado que a marca de passagem para as refeições está posta e o cardápio existe naquele segmento e naquele período
    Quando confirmo
    Então a transação passa para a tela C915T
    E ela abre em consulta, com o cardápio, o segmento, as duas datas e as marcas que esta tela entregou
    E a tela das refeições abre sem nenhuma refeição escolhida
    E nenhuma consulta é feita nesta confirmação

  Cenário: RN-08 — passagem com cardápio que não existe
    Dado que a marca de passagem está posta e o cardápio não existe naquele segmento e naquele período
    Quando confirmo
    Então vejo "* Cardapio nao cadastrado *"
    E o cursor volta para o campo do cardápio
    E nada é gravado

  Cenário: RN-10 — a consulta não grava nada e não deixa rastro
    Dado que consulto a composição de um cardápio
    Quando a consulta se conclui
    Então nenhum registro é incluído, alterado ou excluído
    E nenhuma linha nova aparece na trilha de auditoria por causa desta tela
```
