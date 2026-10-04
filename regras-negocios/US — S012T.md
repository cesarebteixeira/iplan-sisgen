# US — S012T — Encerramento da sessão de um servidor

## Estória

Como **servidor de CRE com a tela S012T autorizada**, quero **dar por encerrada a
sessão de um servidor informando a matrícula funcional dele**, para que **o registro
de presença de quem já não está trabalhando deixe de ficar aberto, sem depender de o
próprio servidor voltar ao sistema só para sair**.

Entrar no sistema registra a sessão daquele servidor como aberta, com a estação, o
dia e a hora. Quem sai sem fechar, ou precisa ser tirado do sistema, deixa esse
registro aberto: o cadastro passa a mostrar como presente quem já não está. É esta
tela que corrige isso — ela grava, para a matrícula informada, que a sessão terminou,
com o dia, o mês, o ano e a hora do encerramento. Sem ela, a única saída seria o
próprio servidor voltar ao sistema apenas para sair.

## Contexto

Jornada S000M → S001M → S004M → S012T.
Ator: servidor de CRE — encerra, pela matrícula funcional, a sessão de um servidor.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. Não escrevo aqui regra do tipo "a opção
4 de um menu abre esta tela".

As duas telas anteriores da jornada são menus (`S001M` e `S004M`): elas só
encaminham, não passam registro nem operação para esta tela e não deixam dado de
negócio para ela. O caminho não é uma tela chamando a outra — é o menu que pede a
abertura. O que a `S012T` usa da sessão — a matrícula de quem opera, o acesso, o
privilégio, o tipo de órgão e a CRE — é o que a entrada deixou, e a tela apenas o
repassa às conferências de rota e de acesso. A matrícula funcional que o operador
informa **não** é a dele: é o alvo do encerramento.

A tela não encadeia para nenhuma outra: ela é a última da jornada e não entrega
registro nem operação adiante. A tela `S012C` tem nome de tela igual, mas é
**consulta** de dados do servidor, não esta operação.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — Encerrar a sessão é a única operação da tela

Desta tela sai um encerramento de sessão e nada mais. Nada é incluído e nada é
excluído — nem o cadastro do servidor, nem o catálogo de telas. Ela não toca em
nenhum outro cadastro e não escreve nada do seu próprio, como um registro de quem
encerrou ou de quantas sessões fechou.

### RN-02 — A abertura não encerra sessão nenhuma

Enquanto a tela é apenas aberta, nada é encerrado. A abertura procura a própria tela
no catálogo de telas para confirmar que ela existe, mostra a descrição do órgão da
sessão e a data do sistema e passa a conferência de acesso. O encerramento só
acontece depois de uma mensagem do operador.

### RN-03 — O encerramento é pela matrícula funcional

Para encerrar, o operador informa a matrícula funcional do servidor alvo. É o único
dado de negócio que a tela pede: não há escolha de estação, de período nem de
sessão, e não há como escolher qual sessão encerrar — a sessão é uma só por
matrícula, e é ela que termina.

### RN-04 — A matrícula é editada como número de nove dígitos

A matrícula informada é tratada como número de nove dígitos: o que estiver em branco
vale zero, os separadores são repostos na exibição e o que não for número é recusado
antes da consulta ao cadastro, com o cursor devolvido ao próprio campo.

[?] A matrícula em branco vira zero e a consulta é feita com zero: não há guarda que
recuse o campo vazio. Se existir cadastro com matrícula zero, é a sessão dele que é
encerrada; se não existir, nada acontece. Pergunta ao site.

### RN-05 — Todo dado vem da matrícula: não há outro campo

Nenhum outro campo de negócio acompanha o encerramento. O que o operador informa na
tela é a matrícula; o resto do que a tela envia às conferências é posição fixa do
protocolo de tela — a operação usada e o código da tela anterior — , não escolha
dele. A matrícula é a chave: a consulta ao cadastro do servidor é feita por ela
sozinha, sem comportamento definido para chave repetida.

### RN-06 — O encerramento acontece na mesma mensagem, sem confirmação

Não há etapa de confirmação nem tela intermediária: a mensagem em que a matrícula é
informada é a mesma em que a sessão termina. A tela não relê o cadastro entre a
conferência e a gravação e não pergunta nada antes de gravar.

### RN-07 — Só há encerramento para matrícula cadastrada

A matrícula informada é procurada no cadastro de funcionários. Não existindo o
cadastro, nada é encerrado: o sistema fica marcado como não tendo encontrado o
registro e a mensagem termina sem gravar.

### RN-08 — Cadastro marcado como excluído não é encerrado

Quando o cadastro da matrícula existe, mas está marcado como excluído (ou baixado),
a tela não segue para a gravação: a mensagem termina ali e a sessão daquela matrícula
continua como estava.

### RN-09 — O que o encerramento grava

O encerramento marca a sessão daquela matrícula como terminada e grava nela o dia, o
mês, o ano e a hora do momento do encerramento. Nenhum outro dado do cadastro do
servidor é montado pela tela: ela lê o registro e devolve o mesmo registro, com
esses campos trocados. A tela também não confere se a sessão estava aberta: ela
grava o estado de terminada para qualquer matrícula cadastrada, tenha ou não uma
sessão em andamento.

A data de atualização do cadastro — a mesma que o prazo da senha usa — **não** é
tocada por esta tela; o dia do encerramento fica no próprio campo de sessão.

### RN-10 — O encerramento não avisa que deu certo

A tela não tem mensagem de sucesso própria e não devolve nada do que gravou: nem a
matrícula, nem o estado novo da sessão, nem a quantidade de sessões encerradas. O
que o operador vê depois de confirmar é a tela respondida, sem lista e sem
comprovação do que foi gravado.

[?] Como o texto que o operador vê é montado pelo ambiente, pelos fontes desta
jornada não dá para dizer se algum aviso aparece na linha de mensagem depois de um
encerramento aceito. Pergunta ao site.

### RN-11 — A resposta da mensagem volta com os campos de contexto em branco

A descrição do órgão da sessão e a data do sistema, que a tela mostra ao abrir, são
apagadas antes de a resposta ser montada, e não são repostas. A resposta sai com os
dois campos em branco.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se existe
um caminho de entrada em que os campos não são limpos, não foi possível determinar
pelos fontes desta jornada. Pergunta ao site.

### RN-12 — Sem cadastro de tela não há operação

A tela precisa estar no catálogo de telas, e não marcada como excluída. Não estando —
ou estando retirada — a tela fecha e o operador vê **\* Tela nao cadastrada \***, na
abertura e em qualquer mensagem.

### RN-13 — Toda mensagem passa pela conferência de acesso do operador

O acesso é conferido pelo contexto da sessão, não pelo que se digita na tela: a
matrícula da sessão precisa estar cadastrada; a estação em que o operador está
precisa ser a mesma registrada para ele no cadastro — não sendo, a sessão termina e o
terminal volta à entrada; e o código de acesso da sessão precisa ter a tela `S012T`.
Sem essa tela, a recusa é **\* Acesso negado para esta matricula \***. Como a tela
sempre pede a mesma operação, ela **não** exige autorização de operação nenhuma.

### RN-14 — A tela só recusa o que ela mesma não sabe fazer

Como a operação pedida é sempre a mesma, a tela não oferece escolha de operação ao
operador e não tem como recusar "operação não disponível" por escolha dele. O aviso
**\* Operacao nao disponivel \*** só apareceria se a operação enviada fosse outra, o
que esta tela não faz.

### RN-15 — O operador pode encerrar a própria sessão

A tela não confere se a matrícula informada é a de quem está operando: não há
impedimento para encerrar a própria sessão, e o encerramento é gravado do mesmo
jeito. Se isso termina o atendimento na hora ou só deixa o registro fechado é o
ambiente que decide.

[?] Pelos fontes desta jornada não dá para dizer se o operador continua atendendo
depois de encerrar a própria sessão, nem se a mensagem seguinte dele ainda passa
pela conferência de estação sem a sessão ser desviada. Pergunta ao site.

### RN-16 — Quem operou fica registrado no próprio cadastro da sessão

O sistema registra, no próprio cadastro da sessão encerrada, a marca-padrão de que o
registro foi lido e gravado, com a matrícula de quem operou. Quem ler o cadastro
depois pode ver que ele foi atualizado; a tela não grava nenhum registro separado
para contar essa história.

---

## Cenários BDD

```gherkin
Funcionalidade: Encerramento da sessão de um servidor

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela S012T

  Cenário: Encerramento da sessão de um servidor cadastrado
    Dado que a matrícula informada é de um servidor cadastrado
    Quando informo a matrícula funcional e confirmo a mensagem
    Então a sessão dessa matrícula fica registrada como terminada
    E ela recebe o dia, o mês, o ano e a hora do encerramento

  Cenário: Só o estado da sessão muda no cadastro
    Dado que a matrícula informada é de um servidor cadastrado
    Quando informo a matrícula funcional e confirmo a mensagem
    Então o estado da sessão e a data e a hora do encerramento são gravados
    E nenhum outro dado do cadastro é incluído, alterado ou excluído
    E a data de atualização do cadastro continua a que era

  Cenário: Abrir a tela não encerra sessão nenhuma
    Dado que abro a tela S012T
    Então nenhuma sessão é encerrada
    E vejo a descrição do órgão da sessão e a data do sistema
    E a tela apenas confere se ela está cadastrada e se a minha matrícula tem acesso

  Cenário: O encerramento acontece na mesma mensagem, sem confirmação
    Dado que a matrícula informada é de um servidor cadastrado
    Quando informo a matrícula funcional
    Então o encerramento acontece nessa mesma mensagem
    E nada me é perguntado antes de gravar

  Cenário: Encerrar uma sessão que já estava terminada
    Dado que a sessão da matrícula informada já estava registrada como terminada
    Quando informo essa matrícula e confirmo a mensagem
    Então o estado de terminada é gravado de novo, com o dia e a hora do momento

  Cenário: Matrícula não cadastrada
    Dado que informo uma matrícula que não existe no cadastro de funcionários
    Quando confirmo a mensagem
    Então nada é encerrado
    E o sistema fica marcado como não tendo encontrado o registro

  Cenário: Matrícula não numérica
    Dado que informo uma matrícula que não é número
    Quando confirmo a mensagem
    Então o campo é recusado antes da consulta ao cadastro
    E o cursor volta para o campo da matrícula

  Cenário: Cadastro marcado como excluído
    Dado que o cadastro da matrícula informada está marcado como excluído
    Quando confirmo a mensagem
    Então nada é encerrado
    E a mensagem termina ali

  Cenário: A resposta volta com os campos de contexto em branco
    Dado que a tela abriu mostrando a descrição do órgão da sessão e a data do sistema
    Quando respondo uma mensagem
    Então a resposta vem com esses dois campos em branco

  Cenário: O encerramento não avisa que deu certo
    Dado que a matrícula informada é de um servidor cadastrado
    Quando confirmo o encerramento
    Então a tela me responde sem aviso de sucesso
    E não vejo a lista nem a quantidade das sessões encerradas

  Cenário: Tela não cadastrada
    Dado que a tela S012T não está no catálogo de telas, ou foi retirada dele
    Quando abro a tela
    Então vejo a mensagem "* Tela nao cadastrada *"
    E não opero a tela

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não tem a tela S012T
    Quando abro a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não opero a tela

  Cenário: Matrícula de quem opera não cadastrada
    Dado que a matrícula da minha sessão não está no cadastro de funcionários
    Quando abro a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não opero a tela

  Cenário: Estação diferente da registrada para quem opera
    Dado que estou numa estação diferente da registrada no meu cadastro
    Quando abro a tela
    Então a minha sessão termina
    E o terminal volta à entrada

  Cenário: A tela não exige autorização de operação
    Dado que o meu código de acesso tem a tela S012T sem nenhuma operação liberada
    Quando informo a matrícula de um servidor cadastrado e confirmo a mensagem
    Então a sessão dele é encerrada do mesmo jeito
    E nenhuma autorização de operação me é exigida

  Cenário: A tela não oferece escolha de operação
    Dado que estou na tela S012T
    Então não há campo de operação para eu preencher
    E não há como eu provocar a recusa "* Operacao nao disponivel *"

  Cenário: Encerrar a própria sessão
    Dado que informo a matrícula da minha própria sessão
    Quando confirmo a mensagem
    Então a minha sessão é registrada como terminada
    E nada na tela me impede de fazer isso
```
