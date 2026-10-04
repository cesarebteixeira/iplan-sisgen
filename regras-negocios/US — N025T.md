# US — N025T — Consulta da nota fiscal

## Estória

Como **servidor de CRE que confere as notas fiscais lançadas**, quero **localizar
uma nota fiscal pelo seu número, pelo fornecedor e pelo ano de emissão, e ver o
que a nota registra**, para que **a conferência da nota e a continuação do
trabalho por item ou por dedução partam do registro certo**.

A nota fiscal é lançada por item, e cada item tem retenção e dedução próprias;
antes de descer ao item é preciso chegar à nota. Esta tela é o ponto em que a
nota é encontrada a partir do que está impresso nela — o número, o fornecedor e o
ano — e em que o sistema decide por onde o trabalho continua: pela situação com
que a nota foi consultada, o sistema leva à tela de consulta da nota ou à de
lançamento dela. Sem ela, quem tem a nota na mão não tem por onde chegar ao
registro — e o número de processo, que é o que a nota detalhada usa para se
identificar, não tem lugar para ser informado.

## Contexto

Jornada S000M → N000M → N060M → N025T.
Ator: servidor de CRE — localiza a nota fiscal pelo número, pelo fornecedor e pelo
ano de emissão e segue para o detalhe por item ou para as deduções.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra
de negócio.

A `N025T` não é menu: é tela de transação, mostra **12 linhas** por vez e não é
por onde se inclui nota — a inclusão e a alteração da nota vivem nas telas de
destino. O que se digita nela é o número da nota fiscal, o código do fornecedor,
o ano de emissão, a coordenação regional escolar e a situação do documento; o
nome do fornecedor, o valor da nota, as datas de entrada e a indicação de
acumulação vêm do registro consultado. A tela é alcançada pela opção 4 do menu
`N060M`, e **também** pelo retorno da tela de nota detalhada (`N026T`), que a
reabre com a consulta anterior e com o número da nota em branco.

As regras abaixo são só as da **tela desta jornada**. As da entrada estão em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md` e o que se apurou sobre
elas está no anexo de evidências.

---

## Regras de negócio

### RN-01 — A tela procura a nota por quatro campos e mostra o que achou

A busca é feita por **número da nota fiscal**, **código do fornecedor**, **ano de
emissão** e **coordenação regional escolar**. Achada a nota, a tela mostra o
**nome do fornecedor**, o **valor total da nota**, as **datas de entrada e de
atualização** do registro, o **número de processo** (quando houver), o **tipo de
contrato**, o **pedido e o ano de entrega** e a indicação de que a nota está
**acumulada**. O nome do fornecedor não é digitado: é o do cadastro de
fornecedores, e a tela o traz para a resposta mesmo quando o registro não é
encontrado.

[?] A coordenação regional escolar aparece entre os campos digitáveis e ao mesmo
tempo é sobrescrita pela da nota encontrada; e o nome por que a tela é conhecida
nos avisos é `N025E`, que não é o código dela. Se a coordenação se digita ou se é
sempre a da nota, e o que `N025E` designa, são perguntas ao site.

### RN-02 — A tela abre em consulta e não grava

Toda resposta da tela é tratada como **consulta (CON)**: a operação com que a
tela é aberta é substituída por consulta antes de qualquer decisão. A tela lê os
cadastros e apresenta o resultado; não inclui, não altera e não exclui nota
fiscal.

[?] A tela recusa a resposta com a mensagem "* Operacao nao disponivel. Use CON *"
quando a operação não é consulta, mas a própria tela acaba de fixar a operação em
consulta — a recusa não tem como acontecer. E os ramos que gravam e que apagam o
registro da nota existem, com as suas guardas, sem caminho que chegue até eles.
Se a tela é mesmo só de consulta, ou se a gravação foi desligada e o código
ficou, é pergunta ao site. As duas linhas estão no anexo.

### RN-03 — A nota de outro grupo não é mostrada

A coordenação regional escolar da nota é conferida contra a da sessão. Se a nota
consultada for de uma coordenação diferente da de quem está operando, a tela
recusa com a mensagem "* Usuario sem acesso a outro grupo *", posiciona o cursor
no campo da coordenação e não mostra o registro.

### RN-04 — Fornecedor não cadastrado é recusa

O código de fornecedor informado tem de existir no cadastro de fornecedores e não
estar excluído. Não estando, a tela recusa com a mensagem
"* Fornecedor nao cadastrado *", posiciona o cursor no campo do fornecedor e não
prossegue.

### RN-05 — A nota sem número é recusa

Sem o número da nota fiscal informado, a tela recusa com a mensagem
"* Informe o numero da nota fiscal *", posiciona o cursor no campo do número e
não prossegue. O número é conferido como número: o que se digita é convertido, os
zeros à esquerda caem e o campo em branco vira zero.

### RN-06 — A situação aceita é normal ou suspensa

O campo de situação do documento só admite os valores que significam **normal** e
**suspensa**. Qualquer outro valor é recusado com a mensagem
"* Inf consulta com numero de processo ou nao *", com o cursor no campo da
situação, e a resposta não prossegue.

[?] O que exatamente cada um dos dois valores gravados significa em política —
por que a consulta depende de haver número de processo — não está no acervo: o
dicionário só declara o campo de situação, de um caractere, sem domínio. Pergunta
ao site.

### RN-07 — O ano de emissão é obrigatório

Sem o ano de emissão da nota informado, a tela recusa com a mensagem
"* Informe o ano de entrega da nota fiscal *", posiciona o cursor no campo do ano
e não prossegue.

### RN-08 — Nota não cadastrada é aviso, e a tela para

Quando nem a nota nem o processo correspondentes são encontrados nos cadastros, a
tela avisa "* Nota fiscal nao cadastrada *" e encerra a resposta sem mostrar
registro nenhum.

### RN-09 — A situação do documento decide qual cadastro a tela lê

Se a situação da consulta é **suspensa**, a tela procura o processo: lê pelo
número de processo e, achando, mostra o que o cadastro do processo registra — o
número do processo montado em partes, as datas de emissão e de entrada montadas
como data, o tipo de contrato, o pedido e o ano de entrega, o valor da nota e a
indicação de acumulação. Se a situação é **normal**, a tela lê pelo número da
nota. Os dois caminhos fazem a mesma conferência da coordenação regional escolar.

[?] Os dois cadastros guardam o mesmo documento por chaves diferentes — um pelo
número de processo e o outro pelo número da nota — e a tela não explica por que a
escolha depende da situação. Pergunta ao site.

### RN-10 — A situação do documento decide para onde a tela encaminha

A tela encaminha a continuação sem passar por menu nenhum, e o destino depende da
**situação com que o documento foi consultado** e de o registro correspondente
ter sido achado: consulta em **suspensa**, achado o processo, segue-se para a
tela de consulta da nota; consulta em **normal**, achada a nota, segue-se para a
tela de lançamento da nota. Em qualquer dos casos o registro inteiro vai junto —
coordenação regional escolar, fornecedor, ano e datas de emissão, tipo de
contrato, pedido e valor. A tela de lançamento é a que exibe o código do
fornecedor; a de consulta, não.

A coordenação regional escolar **não** decide o destino: a mesma coordenação
aparece em qualquer dos dois caminhos, e quem decide é a situação consultada.

[?] Quando o registro não é encontrado em nenhum dos dois cadastros, a tela
termina sem encaminhar para lugar nenhum e sem gravar: o número da nota, o
fornecedor e o ano ficam como o operador os digitou, e nada acontece. Se é para
ser assim, ou se aí deveria haver uma tela de inclusão, é pergunta ao site.

### RN-11 — Voltar da tela de nota detalhada reabre a consulta anterior

Quando a tela de nota detalhada devolve o controle, a tela da consulta reabre com
o fornecedor, o ano e o nome do fornecedor que já estavam no registro anterior e
**com o número da nota apagado** — a consulta anterior é restabelecida e a tela
sai, sem mostrar nada e sem gravar.

[?] Na volta da tela de nota detalhada o número da nota é apagado de propósito,
mas o resto da consulta anterior é restaurado; se o objetivo é que o operador
informe outro número, ou que veja o resultado da consulta que fez, não se conclui
do acervo. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Consulta da nota fiscal por número, fornecedor e ano de emissão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N025T

  Cenário: Localizar a nota fiscal e ver o que ela registra
    Dado que existe uma nota fiscal do meu grupo
    Quando informo o número da nota, o código do fornecedor, o ano de emissão e a coordenação regional escolar
    Então a tela mostra o nome do fornecedor, o valor total da nota, as datas de entrada e de atualização
    E mostra o número de processo, o tipo de contrato, o pedido e o ano de entrega
    E indica se a nota está acumulada

  Cenário: A tela é só de consulta
    Dado que abri a tela N025T
    Quando respondo a tela
    Então nenhum cadastro é gravado
    E nenhuma nota fiscal é incluída, alterada ou excluída

  Cenário: Nota de outra coordenação regional escolar
    Dado que a nota consultada pertence a uma coordenação regional escolar diferente da minha
    Quando respondo a tela
    Então vejo a mensagem "* Usuario sem acesso a outro grupo *"
    E o cursor volta ao campo da coordenação regional escolar
    E o registro não é mostrado

  Cenário: Fornecedor não cadastrado
    Dado que o código de fornecedor que informei não existe no cadastro de fornecedores
    Quando respondo a tela
    Então vejo a mensagem "* Fornecedor nao cadastrado *"
    E o cursor volta ao campo do fornecedor
    E o registro não é mostrado

  Cenário: Número da nota fiscal não informado
    Dado que deixei o número da nota fiscal em branco
    Quando respondo a tela
    Então vejo a mensagem "* Informe o numero da nota fiscal *"
    E o cursor volta ao campo do número da nota
    E o registro não é mostrado

  Cenário: Situação do documento fora das aceitas
    Dado que informei uma situação de documento diferente de normal e de suspensa
    Quando respondo a tela
    Então vejo a mensagem "* Inf consulta com numero de processo ou nao *"
    E o cursor volta ao campo da situação
    E o registro não é mostrado

  Cenário: Ano de emissão não informado
    Dado que deixei o ano de emissão da nota em branco
    Quando respondo a tela
    Então vejo a mensagem "* Informe o ano de entrega da nota fiscal *"
    E o cursor volta ao campo do ano de emissão
    E o registro não é mostrado

  Cenário: Nota fiscal não cadastrada
    Dado que não existe nota fiscal nem processo com os dados que informei
    Quando respondo a tela
    Então vejo a mensagem "* Nota fiscal nao cadastrada *"
    E nenhum registro é mostrado
    E não sou encaminhado a tela nenhuma
    E nada é gravado

  Cenário: Consulta pela situação suspensa, com número de processo
    Dado que a situação da consulta é suspensa
    E a nota tem número de processo
    Quando respondo a tela
    Então a tela mostra o que o cadastro do processo registra
    E mostra o número do processo montado a partir das suas partes
    E mostra as datas de emissão e de entrada como data

  Cenário: Consulta pela situação normal
    Dado que a situação da consulta é normal
    Quando respondo a tela com o número da nota, o fornecedor e o ano
    Então a tela procura a nota pelo número dela

  Cenário: Continuar para a tela de consulta da nota
    Dado que consultei uma nota com a situação suspensa
    E o processo correspondente foi encontrado
    Quando respondo a tela
    Então sou encaminhado à tela de consulta da nota fiscal
    E o registro da nota vai comigo

  Cenário: Continuar para a tela de lançamento da nota
    Dado que consultei uma nota com a situação normal
    E a nota correspondente foi encontrada
    Quando respondo a tela
    Então sou encaminhado à tela de lançamento da nota fiscal
    E a coordenação regional escolar, o fornecedor e as datas de emissão vão comigo

  Cenário: Voltar da tela de nota detalhada
    Dado que estava consultando uma nota e fui para a tela de nota detalhada
    Quando a tela de nota detalhada devolve o controle
    Então a tela N025T reabre com o fornecedor, o ano e o nome do fornecedor da consulta anterior
    E o número da nota fiscal aparece em branco
    E nenhum registro é mostrado
```
