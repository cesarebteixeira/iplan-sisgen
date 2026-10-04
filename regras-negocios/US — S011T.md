# US — S011T — Troca da senha de acesso

## Estória

Como **servidor de CRE**, quero **trocar a senha de acesso de um usuário do sistema, informando a senha atual e confirmando a nova**, para que **o acesso continue valendo quando a senha vence ou ainda é a senha inicial, sem depender de outra pessoa para liberá-lo**.

A senha é o que a entrada do sistema confere para deixar alguém entrar, e uma senha vencida ou ainda inicial não deixa ninguém passar. É esta tela que troca a senha de quem já está cadastrado, guardando as anteriores para que não voltem a ser usadas. Sem isto, quem está com a senha vencida fica trancado do lado de fora — e quem entra pela primeira vez nunca deixa a senha inicial.

## Contexto

Jornada LOGON → S011T.
Ator: servidor de CRE — troca a senha de acesso do cadastro do usuário, confirmando a senha atual.

A entrada — o `LOGON` e o menu principal `S000M` — está em `Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de negócio.

Esta jornada chega à tela pela própria entrada e **sem menu**: quando a senha do servidor precisa ser trocada — por prazo ou porque ainda é a inicial —, o `LOGON` o manda direto para cá. O que a tela usa da sessão — a matrícula de quem opera, o código de acesso, o privilégio, o tipo de órgão com a sua descrição, a CRE, a estação e a data do sistema — é o que a entrada deixou. A matrícula que o servidor informa aqui é a do cadastro que ele vai alterar, e não necessariamente a dele.

As regras abaixo são só as da tela desta jornada. As regras da entrada não se repetem aqui: o que se reconheceu como delas está no anexo de evidências.

---

## Regras de negócio

### RN-01 — A tela troca a senha e mexe em um único cadastro

O cadastro do usuário guarda a senha de acesso, as quatro senhas anteriores e a data de atualização da senha. Esta tela troca a senha desse cadastro: o servidor informa a matrícula funcional, a senha atual, a nova senha e a confirmação, e a troca grava a senha nova, empurra a senha que estava em uso para o registro das anteriores — descartando a mais antiga — e passa a data de atualização da senha para a data do dia.

A troca não inclui nem exclui cadastro nenhum, não toca em outro cadastro e não deixa registro de auditoria. O único cadastro alterado é o da matrícula informada.

### RN-02 — Abrir a tela não grava e avisa sobre o prazo da senha

Ao abrir, a tela mostra o nome de quem está operando, a descrição do tipo de órgão da sessão e a data do sistema, e calcula o prazo da senha **pelo cadastro de quem opera** — não pelo cadastro da matrícula que ele pretende alterar, que ainda está em branco. Abrir não grava nada.

Quando a senha merece aviso, o servidor vê **um** aviso, e vale o primeiro que servir, nesta ordem:

- a senha ainda é a senha inicial do sistema: **\* Para usar o Sistema, altere antes esta senha \***;
- a senha está marcada como vencida: **\* Para usar o Sistema, altere antes esta senha que expirou \***;
- a senha passou de **34 dias**: **\* Sua senha vai expirar em N DIAS - ela deve ser alterada \***, com a palavra no singular quando o número for um dia.

Em cada resposta, o nome, a descrição do tipo de órgão, a data do sistema e o aviso voltam **em branco**; as senhas informadas continuam na tela.

[?] O número de dias do aviso é o resultado de tirar 46 da diferença entre a data de atualização da senha e o dia. A conversão de datas é de uma rotina do ambiente e não tem corpo no lote; como está escrito, a conta só dá número positivo depois de 46 dias, e na faixa em que a entrada manda o servidor para cá (de 35 a 45 dias) o aviso sairia com número negativo. Se o aviso deveria mostrar os dias que faltam, o fonte não diz. Pergunta ao site.

### RN-03 — A tela só abre para quem tem a tela liberada, e na estação da sessão

Para abrir e para tratar cada mensagem, o sistema passa pelas conferências comuns do ambiente:

- a tela tem de estar no cadastro de telas: não estando, a recusa é **\* Tela nao cadastrada \***;
- a estação registrada na sessão tem de ser a do cadastro de quem opera: não sendo, a sessão é encerrada e a tela não abre;
- o código de acesso de quem opera tem de ter a tela `S011T`: não tendo, a recusa é **\* Acesso negado para esta matricula \***; e, para o código de acesso sem nenhum registro daquela tela, **\* Tela nao disponivel \***;
- a operação informada tem de ser reconhecida — a inclusão, a alteração, a exclusão (com a manutenção liberada), a consulta e a operação em branco passam; não reconhecendo, a recusa é **\* Operacao nao disponivel \***;
- a operação tem de estar liberada para aquela tela no código de acesso. A troca de senha conta como **alteração**: com a operação em branco, o sistema exige que a alteração esteja liberada naquela tela; não estando, a recusa é **\* Acesso negado para esta operacao \***.

### RN-04 — A matrícula funcional passa pela edição numérica e aponta o cadastro a alterar

A matrícula informada é editada como número antes de qualquer consulta: o que estiver em branco vale zero, os zeros à esquerda são descartados e o separador volta na exibição; o que não for número é recusado antes da consulta, com o cursor de volta ao campo. É por essa matrícula que a tela lê o cadastro que vai alterar, e é a senha guardada nesse cadastro que a senha atual informada tem de conferir.

Encontrado o cadastro marcado como excluído — ou expurgado —, o aviso **"Key deleted"** é emitido junto ao campo da matrícula.

[?] O texto que o servidor vê quando a digitação é recusada não está no lote: a conferência é de uma rotina do ambiente, sem corpo no acervo. Pergunta ao site.

[?] Não achando cadastro para a matrícula informada, a tela **não para**: ela segue e compara a senha atual informada com o que estiver na área do cadastro, e a conferência de que a matrícula existe só é feita depois. O que o servidor vê primeiro — a recusa da senha ou a da matrícula — depende de a rotina de mensagem do ambiente marcar a falha, e ela não tem corpo no lote. Pergunta ao site.

### RN-05 — A senha atual tem de conferir com a guardada no cadastro

A senha não é guardada como foi digitada: ela passa por um embaralhamento — o mesmo que a entrada usa — antes de ser comparada e antes de ser gravada. A senha atual informada é embaralhada e comparada com a senha guardada no cadastro da matrícula informada. Não conferindo, a troca é recusada com **\* Senha atual nao confere com a cadastrada \***, com o cursor de volta ao campo da senha atual, e o servidor continua na tela.

### RN-06 — A nova senha é obrigatória, não pode ser a inicial e tem de ser confirmada

Passando a senha atual, a tela exige a nova senha e a confirmação, nesta ordem:

- nova senha em branco: **\* Informe uma nova senha \***;
- nova senha igual à **senha inicial** do sistema: **\* SENHA nao e uma senha valida para alteracao \***;
- confirmação diferente da nova senha: **\* Nova senha nao confere com a confirmacao \***.

Nas três, o cursor volta ao campo da nova senha e o servidor continua na tela.

### RN-07 — A nova senha não pode repetir a atual nem as quatro anteriores

A nova senha é embaralhada e comparada com a senha em uso e com as quatro anteriores guardadas no cadastro. Sendo igual a qualquer uma delas, a troca é recusada com **\* Senha deve ser diferente das ultimas 5 senhas \***, com o cursor de volta ao campo da nova senha.

### RN-08 — A operação informada não decide a troca, mas a alteração tem de estar liberada

A tela usa a operação informada só nas conferências comuns de acesso; a gravação não pergunta de novo pela operação. Por isso, informar a **consulta** — que as conferências aceitam sem exigir a liberação da alteração — leva à mesma troca, e não a uma leitura.

O caminho comum, com a operação em branco, exige que a **alteração** esteja liberada para a tela `S011T` no código de acesso de quem opera (RN-03).

[?] Se a intenção era que a troca de senha só acontecesse com a operação de alteração, ou que a consulta apenas lesse, o fonte não diz: o que grava não relê a operação. Pergunta ao site.

### RN-09 — Passando por tudo, a troca grava e entrega o servidor ao menu

Passando por todas as conferências, a tela trava o cadastro, relê o registro corrente, empurra a senha em uso para o registro das anteriores — descartando a mais antiga —, grava a senha nova e passa a data de atualização da senha para a data do dia.

Terminada a gravação, a tela não fica na tela: deixa registrado, na área de trabalho da sessão, que a passagem veio dela — é esse registro que faz o menu principal acusar a troca — e entrega o servidor ao menu principal `S000M`. Não há pergunta de confirmação: conferida a nova senha, a troca é imediata.

[?] A gravação está numa passagem separada da conferência, e quem decide se ela roda é a marca de falha da transação, que só a rotina de mensagem do ambiente põe. As recusas da tela (RN-05 a RN-07) anunciam a mensagem e voltam, sem marcar a falha por conta própria. Se a rotina não marcar, uma recusa ainda assim grava. Pergunta ao site.

### RN-10 — Cinco recusas travam o cadastro e devolvem o servidor à entrada

Cada recusa conta uma tentativa: a senha atual que não confere e qualquer uma das recusas da nova senha entram na mesma conta. Enquanto a conta não passar de quatro, a tela continua conferindo; depois da quinta recusa, **a mensagem seguinte** não confere mais nada — a tela trava o cadastro que estiver sendo lido, com a marca de senha travada (a mesma que a entrada grava), e devolve o servidor ao `LOGON`, terminando a passagem por aqui.

[?] A conta não é da matrícula: a tela não zera o contador quando a matrícula informada muda, como a entrada faz. Depois da quinta recusa, o travamento cai sobre o cadastro que estiver sendo lido naquela mensagem, ainda que seja de outra matrícula. Se era para ser assim, o fonte não diz. Pergunta ao site.

### RN-11 — A ordem de encerrar a sessão

Se o servidor informa a operação `FIM`, a tela não troca senha nenhuma: a passagem é entregue ao roteamento comum, que fecha o registro da sessão e devolve o terminal à entrada. Vale em qualquer situação da tela.

### RN-12 — A troca obrigatória descarta os outros pedidos

Quando o cadastro da matrícula informada está com a senha inicial ou marcado como vencido, a troca é obrigatória e a tela **descarta os pedidos de navegação**: a operação informada é apagada e o código de outra tela é apagado, a não ser que seja o `LOGON`. Em qualquer outro estado do cadastro, nada disso é apagado.

Quem decide o regime é o **estado do cadastro**, e não a tela que chamou: a tela não compara nada com a origem. O mesmo regime vale para quem chegou pelo `LOGON` e para quem chegou pelo menu.

### RN-13 — O pedido de outra tela desvia a mensagem e nada é gravado

Se o campo do código de outra tela chega preenchido e sobrevive (RN-12), a mensagem é desviada para a tela pedida e a troca é abandonada: nenhuma senha chega a ser conferida e nada é gravado.

---

## Cenários BDD

```gherkin
Funcionalidade: Troca da senha de acesso do usuário na tela S011T

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela S011T

  Cenário: Abrir a tela não grava nada e mostra quem opera
    Dado que a minha senha está dentro do prazo
    Quando abro a S011T
    Então vejo o meu nome, a descrição do tipo de órgão da minha sessão e a data do sistema
    E o cadastro da matrícula que eu vá alterar não é lido, porque ele ainda está em branco
    E nada é gravado

  Cenário: Aviso de que a senha vai expirar
    Dado que a minha senha passou de 34 dias sem ser trocada
    Quando abro a S011T
    Então vejo o aviso "* Sua senha vai expirar em N DIAS - ela deve ser alterada *"

  Cenário: Aviso de que a senha venceu
    Dado que a minha senha está marcada como vencida
    Quando abro a S011T
    Então vejo o aviso "* Para usar o Sistema, altere antes esta senha que expirou *"

  Cenário: Aviso de que a senha ainda é a inicial
    Dado que a minha senha ainda é a senha inicial do sistema
    Quando abro a S011T
    Então vejo o aviso "* Para usar o Sistema, altere antes esta senha *"

  Cenário: A resposta volta sem os campos de exibição
    Dado que abri a S011T e vi o meu nome, a descrição do tipo de órgão, a data do sistema e o aviso
    Quando confirmo uma mensagem
    Então esses campos voltam em branco
    E as senhas que digitei continuam na tela

  Cenário: Troca de senha bem-sucedida
    Dado que a senha atual da matrícula informada é a que eu digitei
    E digito uma nova senha diferente das últimas cinco, com a confirmação igual
    Quando confirmo a mensagem
    Então o cadastro daquela matrícula fica com a senha nova
    E a senha que estava em uso passa para o registro das anteriores
    E a data de atualização da senha passa a ser a do dia
    E sou levado ao menu principal S000M, que acusa a troca
    E nenhum outro cadastro é tocado

  Cenário: Senha atual que não confere
    Dado que digito uma senha atual diferente da guardada no cadastro
    Quando confirmo a mensagem
    Então vejo "* Senha atual nao confere com a cadastrada *"
    E o cursor volta para o campo da senha atual
    E o cadastro fica como estava

  Cenário: Nova senha em branco
    Dado que deixo a nova senha em branco
    Quando confirmo a mensagem
    Então vejo "* Informe uma nova senha *"
    E o cursor volta para o campo da nova senha

  Cenário: Nova senha igual à senha inicial
    Dado que informo a senha inicial do sistema como nova senha
    Quando confirmo a mensagem
    Então vejo "* SENHA nao e uma senha valida para alteracao *"
    E o cursor volta para o campo da nova senha

  Cenário: Confirmação diferente da nova senha
    Dado que confirmo a nova senha com outro valor
    Quando confirmo a mensagem
    Então vejo "* Nova senha nao confere com a confirmacao *"
    E o cursor volta para o campo da nova senha

  Cenário: Nova senha repetida das últimas cinco
    Dado que informo como nova senha uma das cinco senhas guardadas no cadastro
    Quando confirmo a mensagem
    Então vejo "* Senha deve ser diferente das ultimas 5 senhas *"
    E o cursor volta para o campo da nova senha

  Cenário: Matrícula que não é número
    Dado que informo uma matrícula que não é número
    Quando confirmo a mensagem
    Então o campo é recusado antes de qualquer consulta
    E o cursor volta para o campo da matrícula

  Cenário: Matrícula que não tem cadastro
    Dado que informo uma matrícula que não tem cadastro de usuário
    Quando confirmo a mensagem
    Então a tela não acha o cadastro e segue adiante, sem parar
    E a recusa que eu vejo depende da conferência que chegar primeiro

  Cenário: Cadastro marcado como excluído
    Dado que o cadastro da matrícula informada está marcado como excluído
    Quando confirmo a mensagem
    Então vejo o aviso "Key deleted" junto ao campo da matrícula

  Cenário: A operação de consulta também troca a senha
    Dado que a senha atual confere e a nova senha é válida
    Quando informo a operação de consulta e confirmo a mensagem
    Então a senha do cadastro é trocada, como na troca comum

  Cenário: Cinco recusas travam o cadastro
    Dado que já errei a senha atual cinco vezes
    Quando confirmo mais uma mensagem
    Então o cadastro que está sendo lido é travado como senha travada
    E sou devolvido ao LOGON

  Cenário: Encerrar a sessão pela tela
    Dado que informo a operação FIM
    Quando confirmo a mensagem
    Então a minha sessão é encerrada
    E a senha não é trocada

  Cenário: A troca obrigatória descarta o pedido de outra tela
    Dado que o cadastro da matrícula informada está com a senha inicial ou marcado como vencido
    Quando informo o código de outra tela e confirmo a mensagem
    Então o código é descartado
    E a tela continua na troca da senha

  Cenário: A troca obrigatória descarta a operação informada
    Dado que o cadastro da matrícula informada está com a senha inicial ou marcado como vencido
    Quando informo uma operação que não é FIM e confirmo a mensagem
    Então a operação é descartada
    E a tela continua na troca da senha

  Cenário: O pedido de outra tela desvia a mensagem
    Dado que o cadastro da matrícula informada não está em troca obrigatória
    Quando informo o código de outra tela e confirmo a mensagem
    Então sou levado à tela pedida
    E nenhuma senha é conferida e nada é gravado

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não tem a tela S011T
    Quando confirmo uma mensagem
    Então vejo "* Acesso negado para esta matricula *"

  Cenário: Sem autorização para a operação
    Dado que o meu código de acesso tem a tela S011T sem a alteração liberada
    Quando confirmo uma mensagem com a operação em branco
    Então vejo "* Acesso negado para esta operacao *"

  Cenário: Operação não reconhecida
    Dado que informo uma operação que a tela não reconhece
    Quando confirmo a mensagem
    Então vejo "* Operacao nao disponivel *"

  Cenário: Tela fora do cadastro de telas
    Dado que a tela S011T não está no cadastro de telas
    Quando confirmo uma mensagem
    Então vejo "* Tela nao cadastrada *"

  Cenário: Tela sem registro para o meu código de acesso
    Dado que o meu código de acesso não tem registro nenhum da tela S011T
    Quando confirmo uma mensagem
    Então vejo "* Tela nao disponivel *"

  Cenário: Estação da sessão diferente da do meu cadastro
    Dado que a minha sessão está numa estação diferente da registrada no meu cadastro
    Quando abro a S011T
    Então a minha sessão é encerrada
    E a tela não abre
```
