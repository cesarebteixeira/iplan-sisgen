# US — E065T — Percentual de arredondamento por subclasse e gênero

## Estória

Como **servidor de CRE**, quero **manter, para o tipo de órgão da minha sessão, o
percentual de arredondamento de cada gênero de material**, para que **a quantidade
pedida nas requisições feche sempre no mesmo múltiplo, sem depender de quem opera**.

O percentual é o que decide se a quantidade pedida de um item sobe ou não para o
múltiplo seguinte da fração com que o gênero é pedido. O tipo de órgão já tem um
percentual próprio, mantido na tela de parâmetros do módulo; o que se define aqui é
o do gênero, e ele prevalece sobre o do tipo de órgão. Sem esse ajuste fino, gêneros
que se pedem em frações diferentes acabam arredondados pelo mesmo número, e a
requisição sai com quantidade a mais ou a menos.

A tela trabalha como lista: mostra de uma vez os percentuais que aquele tipo de
órgão já tem e recebe, linha a linha, o que fazer com cada um.

## Contexto

Jornada S000M → E000M → E060M → E065T.

Ator: servidor de CRE — mantém, para o tipo de órgão da sua sessão, o percentual de
arredondamento de cada gênero de material.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O tipo de órgão, a CRE, a matrícula e a data do sistema não são informados nesta
tela: são o que a entrada deixou na sessão. A tela encerra a jornada: não encaminha
para outra tela.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — O que a tela mantém: um percentual por gênero, dentro da subclasse, para o tipo de órgão da sessão

Cada combinação de subclasse e gênero tem **um** percentual de arredondamento, e o
conjunto é sempre do **tipo de órgão da sessão** — a tela não pergunta qual é o
órgão e não há como manter percentuais de outro.

O percentual vai de **1 a 100**. A subclasse tem duas posições e o gênero, cinco. Ao
lado do código do gênero a tela mostra a **descrição** e a **unidade de medida** do
gênero, que vêm do cadastro de gêneros.

O cadastro por trás da tela é o `E066T`, e não existe cadastro `E065T`: o nome da
tela é só o nome da transação.

[?] O cadastro admite mais de um registro para a mesma subclasse e o mesmo gênero:
quem impede o segundo é a conferência da própria tela, não o cadastro. Se a intenção
era o cadastro garantir isso, ele não garante. Pergunta ao site.

### RN-02 — A tela abre em consulta, com a lista do que o tipo de órgão já tem

Ao ser aberta, a tela assume a consulta e mostra, em **doze linhas**, os percentuais
já cadastrados para o tipo de órgão da sessão: o código da subclasse, o código e a
descrição do gênero, a unidade de medida, o percentual e a marca de ação de cada
linha. Fora da lista, mostra a descrição do tipo de órgão e a data do sistema.

Quando o tipo de órgão ainda não tem nenhum percentual, a tela avisa
**\* Nao existem generos cadastrados \*** e devolve o cursor à coluna da subclasse
da primeira linha.

[?] O que a tela guarda de uma passagem para a outra — a opção usada e a última
chave lida para montar a lista — fica na área da sessão, e o acervo lido não diz se
isso sobrevive de uma transação para a outra, nem de quem é essa área: do terminal,
do servidor ou só da tela. Pergunta ao site.

[?] Fora da lista a tela tem dois campos de código, com a descrição do gênero ao
lado. Eles guardam a última chave lida da lista e voltam preenchidos, mas o acervo
lido não mostra o operador usando-os para nada: não há comando de próxima página
entre as opções que a tela aceita. Pergunta ao site.

### RN-03 — A tela só aceita alteração e consulta

A tela faz duas coisas: **alteração** e **consulta**. Qualquer outra opção é recusada
com **\* Opcao nao disponivel. User ALT ou CON \***, e o cursor volta ao campo da
opção.

Incluir e excluir não são opções da tela: elas são o que cada linha pede (RN-04), e
para usá-las o operador escolhe a alteração.

[?] A mensagem nomeia as opções como **ALT** e **CON**, mas a tela confere a opção
contra os códigos internos de alteração e de consulta do sistema. Nenhum fonte do
lote mostra quem traduz o que o operador digita no código conferido; se não houver
tradução, a guarda recusa toda opção — inclusive as que a mensagem pede — e a tela
só serviria para consultar. Pergunta ao site.

[?] As recusas da própria tela — esta, a da opção, e as das linhas (RN-06 a RN-08) —
mostram a mensagem e devolvem o cursor, mas não marcam a falha que interrompe a
transação. A passagem que grava (RN-10) não relê nenhuma dessas marcas: pelos
fontes, a linha recusada ainda é gravada, a menos que a rotina comum de mensagem,
que não faz parte do acervo lido, aborte a transação. A recusa de acesso é a
exceção: ela marca a falha que interrompe, e é por isso que, nela, a operação não
acontece. Pergunta ao site.

### RN-04 — Cada linha diz o que fazer com ela

Cada linha da lista tem uma marca de ação, de uma posição: **I** inclui, **A** altera
e **E** exclui o percentual daquela linha. A linha sem subclasse informada, ou sem
uma dessas três marcas, é simplesmente ignorada: nada é conferido nem gravado para
ela.

### RN-05 — Os códigos e o percentual passam por edição numérica

A subclasse, o gênero, o percentual e os dois campos de código de fora da lista são
tratados como número: o que não for número é recusado e o cursor volta ao campo
recusado.

[?] O que o operador vê quando a digitação é recusada não está nos fontes desta
jornada: a rotina que faz a edição não faz parte do acervo lido. E o cursor pode ser
devolvido ao campo recusado por dois caminhos, que calculam a posição da linha de
maneiras diferentes — um com passo 6, outro com passo 5. Para a subclasse, na
primeira linha os dois dão o mesmo resultado e da segunda em diante não; para o
percentual, nem na primeira. Qual deles cai na linha certa depende do espaçamento da
máscara, que não está no acervo. Pergunta ao site.

### RN-06 — Na inclusão o gênero não pode ter percentual, precisa estar cadastrado e ativo, e o percentual vai de 1 a 100

Na linha marcada com **I**, nesta ordem: se o gênero já tem percentual, a recusa é
**\* Percentual ja cadastrado para este genero \***, com o cursor na marca de ação da
linha; se o gênero não existe no cadastro de gêneros, está inativo ou está marcado
como excluído, a recusa é **\* Genero inativo ou nao cadastrado \***, com o cursor na
coluna da subclasse; sem percentual informado, a recusa é
**\* Informe o percentual de arredondamento \***; e acima de **100**, a recusa é
**\* Maximo percentual = 100 \***. Nas duas últimas o cursor volta à coluna do
percentual.

[?] O sistema prepara a data de início de vigência do gênero — ano, mês e dia do
sistema — antes de ler o cadastro de gêneros, e o índice desse cadastro é chaveado
também por essa data. O acervo não permite decidir se a leitura exige o gênero
vigente no dia ou apenas a subclasse e o gênero, porque a conferência que vem depois
só compara subclasse e gênero. Se exigir a vigência do dia, só entram gêneros cuja
vigência começa hoje. Pergunta ao site.

### RN-07 — Na alteração o gênero precisa ter percentual, e o percentual vai de 1 a 100

Na linha marcada com **A**, o gênero tem de já ter percentual; não tendo, a recusa é
**\* Percentual nao cadastrado para este genero \***, com o cursor na marca de ação
da linha. Sem percentual informado e acima de 100 valem as mesmas recusas da
inclusão, com o cursor na coluna do percentual.

A alteração **não** confere o cadastro de gêneros: é possível alterar o percentual de
um gênero que já não existe, que está inativo ou que está marcado como excluído. Só a
inclusão faz essa conferência.

### RN-08 — Na exclusão o gênero precisa ter percentual

Na linha marcada com **E**, o gênero tem de já ter percentual; não tendo, a recusa é
**\* Percentual nao cadastrado para este genero \***, com o cursor na marca de ação
da linha. Nada mais é conferido.

### RN-09 — Cada linha exige a liberação daquela operação

Antes de conferir qualquer dado, a marca da linha é levada à segurança: incluir,
alterar e excluir exigem, cada uma, a sua liberação para o código de acesso do
operador naquela tela. Não estando liberada, a recusa é
**\* Acesso negado para esta operacao \***, o servidor volta ao menu principal e
nada é lido nem gravado.

[?] A conferência não olha a liberação da consulta, e uma linha sem marca de ação
passa por ela sem conferência nenhuma — a consulta, aliás, nem chega a essa
conferência. Se a intenção era exigir a liberação da consulta por tela, o caminho
não a exige. Pergunta ao site.

### RN-10 — A inclusão cria, a alteração regrava e a exclusão apaga; a consulta não grava nada

Passando nas conferências, a linha marcada com **I** cria o percentual daquela
subclasse e daquele gênero para o tipo de órgão da sessão; a marcada com **A**
regrava o percentual existente — só o percentual muda; e a marcada com **E** apaga o
percentual. Na consulta não se cria, não se regrava e não se apaga nada.

A tela **não** grava o cadastro de telas nem o cadastro de gêneros: ela lê os dois, e
só escreve o percentual e a auditoria.

### RN-11 — Toda operação fica registrada na auditoria

Inclusão, alteração e exclusão deixam um registro de auditoria com o cadastro
auditado, a operação, os valores **antes** e **depois**, a matrícula, o terminal, a
CRE, o tipo de órgão e a data e a hora da sessão. Na inclusão o "antes" vai em
branco; na exclusão, o "depois". A consulta não gera registro.

[?] A inclusão só monta o registro de auditoria quando o processamento automático do
percentual não devolve o seu marcador de sucesso; se esse marcador aparecer
justamente na gravação que deu certo, a inclusão não deixa rastro. O que faz o
marcador aparecer não está nos fontes desta jornada. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Percentual de arredondamento por subclasse e gênero

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E065T

  Cenário: Abertura da tela com os percentuais do tipo de órgão da sessão
    Dado que o tipo de órgão da minha sessão já tem percentuais cadastrados
    Quando abro a tela
    Então ela abre em consulta
    E vejo até doze linhas com a subclasse, o gênero, a descrição e a unidade do gênero,
      o percentual e a marca de ação de cada uma
    E vejo a descrição do tipo de órgão e a data do sistema

  Cenário: Tipo de órgão sem nenhum percentual
    Dado que o tipo de órgão da minha sessão não tem nenhum percentual cadastrado
    Quando abro a tela
    Então vejo a mensagem "* Nao existem generos cadastrados *"
    E o cursor volta à coluna da subclasse da primeira linha

  Cenário: A consulta não grava nada
    Dado que o tipo de órgão da minha sessão já tem percentuais cadastrados
    Quando consulto a lista
    Então nenhum percentual é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado

  Cenário: Opção de manutenção fora de alteração e consulta
    Quando informo uma opção que não é alteração nem consulta
    Então vejo a mensagem "* Opcao nao disponivel. User ALT ou CON *"
    E o cursor volta ao campo da opção

  Cenário: Linha sem subclasse ou sem marca de ação é ignorada
    Quando deixo uma linha sem a subclasse, ou sem a marca de ação
    Então essa linha não é conferida nem gravada

  Cenário: Código ou percentual que não é número
    Quando digito na subclasse, no gênero ou no percentual algo que não é número
    Então o cursor volta ao campo recusado

  Cenário: Inclusão de um percentual novo
    Dado que o gênero informado não tem percentual cadastrado
    E o gênero está cadastrado e ativo
    Quando marco a linha com I e informo um percentual de 1 a 100
    Então o sistema grava o percentual daquele gênero para o tipo de órgão da minha sessão
    E registra a operação na auditoria

  Cenário: Inclusão recusada porque o gênero já tem percentual
    Dado que o gênero informado já tem percentual cadastrado
    Quando marco a linha com I
    Então vejo a mensagem "* Percentual ja cadastrado para este genero *"
    E o cursor volta à marca de ação da linha

  Cenário: Inclusão de gênero inativo ou não cadastrado
    Dado que o gênero informado não está cadastrado, está inativo ou está excluído
    Quando marco a linha com I e informo o percentual
    Então vejo a mensagem "* Genero inativo ou nao cadastrado *"
    E o cursor volta à coluna da subclasse da linha

  Cenário: Inclusão ou alteração sem o percentual
    Quando marco a linha com I ou com A e deixo o percentual em branco
    Então vejo a mensagem "* Informe o percentual de arredondamento *"
    E o cursor volta à coluna do percentual da linha

  Cenário: Percentual acima de 100
    Quando marco a linha com I ou com A e informo um percentual maior que 100
    Então vejo a mensagem "* Maximo percentual = 100 *"
    E o cursor volta à coluna do percentual da linha

  Cenário: Alteração de um percentual existente
    Dado que o gênero informado já tem percentual cadastrado
    Quando marco a linha com A e informo outro percentual
    Então o sistema regrava o percentual daquele gênero
    E registra a operação na auditoria

  Cenário: Alteração ou exclusão de gênero sem percentual
    Dado que o gênero informado não tem percentual cadastrado
    Quando marco a linha com A ou com E
    Então vejo a mensagem "* Percentual nao cadastrado para este genero *"
    E o cursor volta à marca de ação da linha

  Cenário: Alteração do percentual de gênero que já não está ativo
    Dado que o gênero informado tem percentual cadastrado e não está ativo no cadastro de gêneros
    Quando marco a linha com A e informo outro percentual
    Então o sistema regrava o percentual, sem conferir o cadastro de gêneros
    E registra a operação na auditoria

  Cenário: Exclusão de um percentual
    Dado que o gênero informado já tem percentual cadastrado
    Quando marco a linha com E
    Então o sistema apaga o percentual daquele gênero
    E registra a operação na auditoria

  Cenário: Operação não autorizada para o meu código de acesso
    Dado que o meu código de acesso não tem a liberação da operação marcada na linha
    Quando tento incluir, alterar ou excluir
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E volto ao menu principal
    E nada é gravado

  Cenário: Toda operação deixa rastro de auditoria
    Dado que a operação passou em todas as conferências
    Quando incluo, altero ou excluo um percentual
    Então um registro de auditoria é gravado com o cadastro auditado, a operação,
      os valores antes e depois, a matrícula, o terminal, a CRE, o tipo de órgão e
      a data e a hora da sessão
    E na inclusão o "antes" fica em branco
    E na exclusão o "depois" fica em branco
```
