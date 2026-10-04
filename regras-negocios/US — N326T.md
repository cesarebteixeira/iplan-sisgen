# US — N326T — Consultar a nota fiscal e os gêneros entregues

## Estória

Como **servidor de CRE**, quero **consultar a nota fiscal recebida, com os gêneros e as
quantidades que ela entregou**, para que **eu confira a entrega do fornecedor contra o
pedido e o contrato**.

A nota fiscal é a peça que amarra o fornecedor, o pedido, o contrato e o que de fato foi
entregue. Quem escolhe a nota é a consulta de notas fiscais do contrato; esta tela é a
que mostra o conteúdo dela, gênero por gênero, com a quantidade — e é por isso que ela é
**somente de leitura**: a nota que chega aqui já foi lançada, e nada do que se vê nesta
tela pode ser corrigido por ela. Sem esta conferência, a secretaria teria o pedido e o
saldo do contrato, mas não teria como ver o que a nota entregou.

## Contexto

Jornada S000M → N000M → N050M → N300M → N317T → N326T.

Ator: servidor de CRE — abre a nota fiscal escolhida na consulta anterior e confere os
gêneros e as quantidades que ela entregou.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As telas anteriores da jornada — a `N000M`, a `N050M` e a `N300M` — só encaminham; o que
esta tela usa da sessão é o que a entrada deixou. Mas a `N317T`, que é a tela
imediatamente anterior, **não é menu**: ela encadeia na `N326T` sem passar por menu
nenhum, e por isso o que ela deixa na sessão — a nota escolhida, a marca de origem e o
modo da operação — é **regra desta tela**, e não contexto: é o que a RN-02, a RN-03 e a
RN-04 descrevem.

Esta é a última tela da jornada: dela não se passa para outra tela. A única saída que ela
nomeia é o menu `N300M`, no caminho de recusa (RN-09).

As regras abaixo são só as da tela desta jornada. A conferência de autorização da tela é
regra da entrada, e está no anexo de evidências.

---

## Regras de negócio

### RN-01 — A tela é de consulta: não inclui, não altera e não exclui

A tela mostra a nota e os gêneros que ela entregou; não é tela de manutenção. Sobre os
três cadastros que ela enxerga — o perfil da tela, os itens da nota e o cadastro de
gêneros — ela faz **quatro leituras** e **nenhuma gravação**. As rotinas de gravar e de
excluir existem escritas para esses três cadastros, mas não são chamadas em caminho
nenhum: quem conta, conta quatro pontos de leitura e zero de escrita.

A única opção que a tela aceita é a de consulta; qualquer outra é recusada (RN-08) — e,
fora da consulta, ela nem chega a procurar os gêneros da nota (RN-03).

### RN-02 — A nota só é montada quando a tela reconhece a origem

Esta tela não se abre pelo menu como as outras: para ela montar a nota, a área que a
consulta anterior deixou na sessão tem de estar marcada com o código `N314T`. Sem essa
marcação, a tela **não mostra nada**, marca a operação como falha e devolve o servidor ao
menu `N300M`; chegando assim ao menu, o menu avisa
**\* Acesso deve ser feito pela tela N314T \***.

A marcação é a mesma nos **dois** programas do acervo que chamam esta tela — a consulta
de notas fiscais do contrato (`N317T`) e a consulta de notas fiscais por número (`N325T`)
—, e **nenhum** programa chamado `N314T` chama esta tela: são as duas consultas que
escrevem o código `N314T` na sessão, antes de entregar a nota.

[?] A marcação e a conferência não fecham. Ao inicializar, a tela apaga a marcação na sua
própria área de trabalho e só volta a lê-la no caminho em que copia a área deixada por
quem a chamou — e é nesse mesmo caminho que a marcação é conferida. Entrando pelo seu
próprio código de transação, a tela segue por outro caminho, em que a marcação não é
conferida e os gêneros não são lidos. Ou a conferência é o que faz a entrega funcionar (e
as duas consultas escrevem a marcação exatamente para isso), ou ela não roda no
encadeamento e não serve para nada. O fonte não decide qual dos dois. Pergunta ao site.

### RN-03 — O modo da operação vem de quem chama

Quem chama decide em que modo a nota abre, e o **único** modo em que a tela mostra os
gêneros é a **consulta**. Fora da consulta, a tela não procura item nenhum: segue direto
para a saída, sem mostrar a lista.

No caminho desta jornada, quem chama já entrega a nota em consulta: a consulta de notas
fiscais do contrato escreve o modo de consulta na área da sessão antes de passar o
controle.

### RN-04 — A nota chega pronta: esta tela não procura a nota fiscal

Esta tela não vai ao cadastro de notas fiscais. Ela recebe da consulta anterior **21
campos** já preenchidos e só daí monta o cabeçalho: o modo da operação, o número da nota,
o código e a descrição do **modelo da nota fiscal**, o dia, o mês e o ano da nota, o dia,
o mês e o ano de emissão, o código do fornecedor e a sua razão social, a coordenadoria
regional escolar, o tipo de contrato, o código e o nome do operador logístico, o número
do pedido, o ano da entrega, o código e o nome do órgão filho e a **chave de acesso** da
nota. Do que a tela mostra fora desses 21 campos, só a descrição do tipo de órgão e a
data do sistema não vêm da consulta: vêm da sessão.

### RN-05 — Os gêneros entregues: até 8 linhas, com a descrição vinda do cadastro

Para a nota escolhida, a tela mostra os gêneros entregues em **até 8 linhas**. Cada linha
traz o **código da subclasse** (2 dígitos), o **código do gênero** (5), a **descrição do
gênero** (15 posições) e a **quantidade entregue** (5 dígitos inteiros e 3 decimais).

A subclasse, o gênero e a quantidade saem do **cadastro de itens da nota**, procurado
pelos dados que identificam a nota — o órgão, o operador logístico, o número e o ano —
mais a posição em que a leitura ficou. A descrição sai do **cadastro de gêneros**,
procurado pela subclasse e pelo gênero e **apenas entre os gêneros não excluídos**; nessa
procura a data da nota entra como início de vigência do gênero.

A leitura é encadeada: a posição da última linha lida viaja na área da sessão, e quando a
lista da nota acaba essa posição é zerada. Do que a leitura devolve, a tela confere
apenas parte da chave — no cadastro de itens, o órgão, o operador, o número e o ano, mas
**não** a subclasse nem o gênero; no cadastro de gêneros, a subclasse e o gênero, mas
**não** a data.

[?] Como a data da nota é posta na procura do gênero mas não entra na conferência do que
volta, não se sabe se a descrição mostrada é a vigente na data da nota ou outra qualquer
do par subclasse/gênero. Pergunta ao site.

[?] A coluna da unidade de medida existe na tela e é limpa a cada entrada, mas a tela
nunca a preenche: nenhuma das leituras devolve unidade para a linha. A quantidade aparece
sem unidade. Pergunta ao site.

### RN-06 — Nota sem gênero nenhum avisa

Quando a tela não encontra **nenhum** item para a nota escolhida, ela avisa
**\* Nota fiscal sem generos cadastrados \***, zera os códigos de subclasse e de gênero
da primeira linha e não mostra linha nenhuma. O aviso é dado **uma vez**, na primeira
linha da tela: uma nota com poucos gêneros — menos de oito — não recebe aviso nenhum.

### RN-07 — A tela confere 17 campos e limpa 8 antes de qualquer leitura

Ao confirmar, a tela confere **17 campos**, um a um, exigindo que sejam números e que
caibam no tamanho de cada um:

- o número da nota fiscal (9 dígitos);
- o dia, o mês e o ano da nota fiscal (2, 2 e 4);
- o dia, o mês e o ano de emissão (2, 2 e 4);
- a coordenadoria regional escolar (2), o número do pedido (6) e o ano da entrega (4);
- o tipo de contrato (3), o código do fornecedor (4) e o código do órgão filho (8);
- o código do operador logístico (4);
- o código da subclasse (2), o código do gênero (5) e a quantidade do gênero (5 inteiros
  e 3 decimais, separadas por vírgula).

Campo em branco entra como zero, e os zeros à esquerda não contam para o tamanho. O que
for recusado é marcado e o cursor volta para o campo — **na linha certa**, quando o campo
é de uma das 8 linhas de gênero.

Os campos que a tela mesma preenche a partir das leituras e da sessão — a descrição do
gênero, a unidade de medida, a razão social do fornecedor, os nomes do órgão e do
operador, a descrição do modelo da nota, a descrição do tipo de órgão e a data do sistema
— são limpos a cada entrada, **8 campos** ao todo, para que a tela mostre sempre o que a
leitura desta vez achou, e nunca o resto da leitura anterior.

[?] Dos 17 campos, **um** — o do operador logístico — é conferido pelo próprio
identificador interno, sem rótulo em português; os outros dezesseis são conferidos pelo
rótulo que o servidor lê na tela. Se a tela mostra esse identificador no lugar do rótulo,
o fonte não diz. Pergunta ao site.

### RN-08 — Opção diferente da de consulta é recusada

Confirmando com qualquer opção que não seja a de consulta, a tela recusa com
**\* Opcao nao disponivel. Use CON \***, com o cursor de volta ao campo da opção, e nada
é lido nem gravado.

[?] A tela aceita **um único** código de opção — o código interno de consulta —, o
gerador mostra a consulta como a letra **I** quando converte os modos, e o aviso manda
usar **CON**. As três formas não coincidem, e o acervo não traz a máscara da tela: o que
o servidor precisa digitar para ser aceito fica sem resposta. Pergunta ao site.

### RN-09 — A tela não encadeia em outra

Esta é a última tela da jornada: ela não passa a nota adiante. O único destino que ela
nomeia é o menu `N300M`, e só no caminho em que não reconhece a origem (RN-02). No
caminho normal, confirmar em consulta não grava, não transfere e não aponta tela nenhuma.

[?] O que o servidor vê depois de confirmar em consulta — se a tela se redesenha, se o
controle volta para a consulta de notas fiscais que a chamou, ou se o sistema o devolve
ao menu — depende do ambiente de execução, e o fonte não diz. A extração do acervo
registra a saída desta tela como "passa para N300M". Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar a nota fiscal e os gêneros entregues

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N326T

  Cenário: Consultar a nota escolhida na consulta de notas fiscais
    Dado que escolhi uma nota fiscal na tela N317T
    Quando a tela N326T abre
    Então vejo o número da nota, a data da nota e as duas datas de emissão
    E vejo o modelo da nota fiscal, a chave de acesso e o fornecedor com a razão social
    E vejo a coordenadoria regional escolar, o tipo de contrato, o operador logístico,
      o número do pedido, o ano da entrega e o órgão filho com o seu nome
    E vejo os gêneros entregues, em até 8 linhas, com a descrição e a quantidade de cada um
    E nada é gravado

  Cenário: Cada linha de gênero mostra o que veio da nota e do cadastro
    Dado que a nota escolhida tem gêneros entregues
    Quando a tela N326T abre
    Então cada linha mostra o código da subclasse, o código do gênero e a quantidade
      entregue, vindos do cadastro de itens da nota
    E mostra a descrição do gênero, vinda do cadastro de gêneros

  Cenário: O gênero excluído não empresta a sua descrição
    Dado que a nota escolhida tem um gênero cujo cadastro está excluído
    Quando a tela N326T abre
    Então esse gênero não é encontrado no cadastro de gêneros
    E a linha fica sem a descrição

  Cenário: Nota sem gênero nenhum avisa
    Dado que a nota escolhida não tem nenhum item cadastrado
    Quando a tela N326T abre
    Então vejo "* Nota fiscal sem generos cadastrados *"
    E nenhuma linha de gênero é mostrada
    E nada é gravado

  Cenário: A nota que chega pronta não é procurada de novo
    Dado que escolhi uma nota fiscal na tela N317T
    Quando a tela N326T abre
    Então o cabeçalho mostra exatamente os dados que a consulta entregou
    E a tela não vai ao cadastro de notas fiscais buscar nada

  Cenário: A nota entregue chega marcada como consulta
    Dado que escolhi uma nota fiscal na tela N317T
    Quando a nota chega à tela N326T
    Então o modo da operação já vem como consulta
    E é esse modo que deixa a tela mostrar os gêneros

  Cenário: Fora da consulta os gêneros não são lidos
    Dado que a nota chega à tela N326T em modo diferente da consulta
    Quando a tela abre
    Então ela não procura os gêneros da nota
    E nenhuma linha de gênero é mostrada

  Cenário: Confirmar em consulta não grava nada
    Dado que estou na tela N326T em consulta
    Quando confirmo
    Então nenhum item da nota e nenhum gênero é incluído, alterado ou excluído
    E nenhum registro de auditoria é criado

  Cenário: A tela não oferece inclusão, alteração nem exclusão
    Dado que estou na tela N326T
    Quando procuro uma operação de gravação
    Então não existe nenhuma: as únicas operações que a tela executa sobre os cadastros
      que enxerga são leituras

  Cenário: Opção diferente da de consulta é recusada
    Dado que estou na tela N326T
    Quando confirmo com uma opção diferente da de consulta
    Então vejo "* Opcao nao disponivel. Use CON *"
    E o cursor volta ao campo da opção
    E nada é lido e nada é gravado

  Cenário: Sem a marcação de origem, a nota não é montada
    Dado que chego à tela N326T sem a marcação de origem da consulta de notas fiscais
    Quando a tela é chamada
    Então ela não mostra a nota
    E sou devolvido ao menu N300M
    E o menu avisa "* Acesso deve ser feito pela tela N314T *"

  Cenário: Valor não numérico é recusado antes das leituras
    Dado que estou na tela N326T
    Quando informo letras em um dos 17 campos conferidos
    Então a tela recusa o campo antes de procurar qualquer cadastro
    E o cursor volta para o campo
    E nada é gravado

  Cenário: Campo em branco entra como zero
    Dado que estou na tela N326T
    Quando deixo um dos 17 campos conferidos em branco e confirmo
    Então a tela o trata como zero
    E não o recusa por estar em branco

  Cenário: A tela não encadeia em outra
    Dado que estou na tela N326T em consulta
    Quando confirmo
    Então a nota não é passada para nenhuma outra tela
    E nenhuma tela de destino é apontada
```
