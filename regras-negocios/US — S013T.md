# US — S013T — Redefinição da senha inicial de acesso do funcionário

## Estória

Como **servidor de CRE com a tela S013T autorizada**, quero **devolver a senha de
acesso de um funcionário à senha inicial do sistema, informando a matrícula funcional
dele**, para que **quem perdeu, esqueceu ou teve a senha bloqueada volte a entrar e a
trabalhar sem depender de um recurso que ninguém consegue fazer de outro jeito**.

A senha de acesso é o que abre a porta do sistema para o servidor: sem ela ele não
entra, e ninguém consegue dizer qual é, porque o sistema não a guarda de um jeito que
se leia. O que esta tela faz é recolocar a senha no estado em que o funcionário a
recebeu quando foi incluído, e registrar o dia em que isso aconteceu — é esse registro
que faz a senha antiga deixar de valer. Sem ela, cada senha esquecida viraria um
cadastro refeito.

## Contexto

Jornada S000M → S001M → S004M → S013T.
Ator: servidor de CRE — devolve, pela matrícula funcional, a senha inicial de acesso
de um funcionário.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As telas anteriores da jornada são menus: elas só encaminham e não deixam dado de
negócio para esta tela. O que a `S013T` usa da sessão — a matrícula de quem opera, o
privilégio dela, o tipo de órgão e a data do sistema — é o que a entrada deixou; o
nível de acesso, de cada lado, ela lê do cadastro de acessos. A matrícula funcional
que o operador informa não é a dele: é o alvo da redefinição.

A tela abre em modo próprio, decidido por ela mesma: a opção e a próxima tela que ela
confere vêm da máscara dela, não da tela anterior, e ela não compara a tela de origem
com código nenhum. Nenhum dos menus da jornada deixa para esta tela o modo de operação.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela redefine a senha, e só isso

Desta tela sai uma redefinição de senha de acesso e nada mais: nenhum cadastro é
incluído, nenhum é excluído e nenhum outro é alterado. O único cadastro tocado é o do
funcionário — e, dentro dele, só a senha e o que o sistema registra junto com ela. A
tela tampouco grava registro de auditoria próprio.

### RN-02 — Abrir a tela não redefine senha nenhuma

Enquanto a tela é apenas aberta, nada é redefinido. A abertura mostra a descrição do
tipo de órgão da sessão e a data do sistema, procura a própria tela no cadastro de
telas para confirmar que ela existe e passa a conferência de acesso. A redefinição só
acontece depois de uma mensagem do operador.

### RN-03 — A redefinição é pela matrícula funcional, na mesma mensagem, sem confirmação

Para redefinir, o operador informa a matrícula funcional. É o único dado de negócio da
tela: não há escolha de senha, não há escolha de prazo e não há etapa de confirmação —
a redefinição acontece na mesma mensagem em que a matrícula é informada. A tela também
não devolve a senha nova nem a lista do que foi alterado.

[?] Pelos fontes desta jornada não se sabe o que o operador vê quando a redefinição dá
certo: a tela não tem aviso de sucesso próprio nem campo de retorno com a senha. Se o
funcionário não souber de antemão qual é a senha inicial, o atendimento termina sem
que ninguém saiba o que foi gravado. Pergunta ao site.

### RN-04 — A matrícula é editada como número de nove dígitos

A matrícula informada é tratada como número: o que estiver em branco vale zero, os
separadores são repostos na exibição e o que não for número é recusado antes da
consulta ao cadastro, com o cursor devolvido ao próprio campo.

[?] A matrícula em branco vira zero e a consulta é feita com zero: não há guarda que
recuse o campo vazio. Se existir cadastro com matrícula zero, é a senha dele que é
redefinida; se não existir, nada acontece. Pergunta ao site.

### RN-05 — Só há redefinição para matrícula cadastrada

A matrícula informada é procurada no cadastro de funcionários e a busca é por ela
sozinha — um único registro por matrícula. Não existindo o cadastro, nada é
redefinido: o sistema marca que não achou o registro e a mensagem termina sem gravar.

### RN-06 — O que a redefinição grava

A redefinição recoloca a senha de acesso do funcionário na senha inicial do sistema —
o mesmo valor que o cadastro dele recebe no dia em que é incluído — e não em uma senha
nova, escolhida ou sorteada a cada atendimento: toda redefinição devolve a mesma senha
inicial, para qualquer funcionário. A senha que estava valendo entra no histórico das
últimas senhas do cadastro, que guarda as quatro anteriores, e a data de atualização
da senha passa a ser a data do dia. Nenhum outro dado do cadastro do funcionário é
montado pela tela: ela lê o registro e devolve o mesmo registro, com esses campos
trocados.

[?] O fonte mostra que a senha gravada é sempre a mesma senha inicial, mas não diz como
o funcionário fica sabendo dela: a tela não a mostra e não há aviso de sucesso próprio.
Se quem não deveria conhece a senha inicial, toda senha redefinida fica exposta entre o
atendimento e a primeira troca. Pergunta ao site.

### RN-07 — O aviso para cadastro marcado como excluído

Antes de redefinir, o sistema procura a matrícula informada como código de usuário.
Quando o cadastro está marcado como excluído (ou baixado), o sistema responde com o
aviso **"Key deleted"** junto ao campo da matrícula.

[?] Não é possível determinar pelos fontes desta jornada se esse aviso apenas avisa ou
se interrompe a redefinição: quem o emite é uma rotina do ambiente e o que a emissão
faz com o andamento da mensagem não está no acervo. O caminho que grava relê o cadastro
e volta a conferir apenas se ele existe — não volta a conferir o estado dele.
Pergunta ao site.

### RN-08 — O operador não redefine a própria senha sem o privilégio

Quando a matrícula informada é a do próprio operador, a redefinição só é permitida se
ele tiver o privilégio especial da sessão. Sem ele, a recusa é
**\* Nao atualize seu proprio cadastro \***, com o cursor de volta no campo da
matrícula, e nada é gravado.

### RN-09 — Quem o operador alcança: o nível de acesso do alvo

A redefinição também depende do nível de acesso. O sistema toma o maior nível
registrado para a matrícula de quem opera e o maior nível registrado para a matrícula
informada, e deixa passar quando o alvo tem nível **menor**. Quando os dois níveis são
iguais, a operação só passa se o operador tiver o privilégio especial; quando o nível
do alvo é **maior**, a recusa é **\* Seu nivel de acesso nao permite esta operacao \***,
com o cursor no campo da opção.

[?] A conferência do nível aparece duas vezes com desfechos opostos para o mesmo caso:
uma recusa o nível igual de quem não tem o privilégio, e a outra o admitiria. O
desfecho observável é a recusa, mas não se sabe qual das duas expressa a intenção: ou o
nível igual deveria ser permitido, ou a segunda conferência é um resto. Pergunta ao
site.

### RN-10 — Antes de redefinir, o sistema confere a tela, a opção e o acesso

Toda mensagem passa pelas conferências comuns. A da rota exige que a tela esteja no
cadastro de telas — tendo sido retirada, a recusa é **\* Tela nao cadastrada \*** — e
reconhece como opção a inclusão, a alteração, a exclusão, o retorno, o menu, a consulta
e a saída; não reconhecendo, o aviso é **\* Operacao nao disponivel \***. A do acesso
exige a tela `S013T` no cadastro de telas por código de acesso da matrícula que opera —
não estando, a recusa é **\* Acesso negado para esta matricula \*** — e, conforme a
opção informada, a autorização daquela operação no mesmo cadastro — não tendo, a recusa
é **\* Acesso negado para esta operacao \***. Ao abrir, a conferência ainda exige que a
tela exista no cadastro de telas — não existindo, o aviso é
**\* Tela nao disponivel \***.

A opção informada serve só a essas conferências: o caminho que redefine não a lê. Com a
opção de consulta nenhuma autorização de operação é exigida e a senha é redefinida do
mesmo jeito; com a opção em branco exige-se a autorização de alteração; e com a opção de
saída do sistema quem sai é o operador, sem que a senha da matrícula informada seja
redefinida.

[?] O aviso **\* Operacao nao disponivel \*** não marca a falha que interromperia a
mensagem, ao contrário dos avisos de acesso e dos de tela. Nada nos fontes desta jornada
diz se, depois dele, a redefinição continua acontecendo — e o caminho que grava não
confere a opção. Ou a recusa da opção deveria interromper a mensagem, ou o caminho da
redefinição deveria conferi-la. Pergunta ao site.

### RN-11 — A resposta de cada mensagem volta com dois campos em branco

A descrição do tipo de órgão da sessão e a data do sistema, que a tela mostra ao abrir,
são apagadas a cada mensagem respondida e não são repostas: a resposta sai com os dois
campos em branco.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se existe um
caminho de entrada em que os campos não são limpos, não foi possível determinar.
Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Redefinição da senha inicial de acesso do funcionário

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela S013T

  Cenário: Redefinição da senha de um funcionário cadastrado
    Dado que a matrícula informada é de um funcionário cadastrado
    E o nível de acesso dele é menor que o meu
    Quando informo a matrícula funcional e confirmo a mensagem
    Então a senha de acesso dele volta a ser a senha inicial do sistema
    E a senha que estava valendo entra no histórico das últimas senhas
    E a data de atualização da senha passa a ser a data do dia

  Cenário: Toda redefinição devolve a mesma senha inicial
    Dado que redefini a senha de um funcionário cadastrado
    Quando redefino a senha de outro funcionário cadastrado
    Então os dois ficam com a mesma senha inicial do sistema
    E nenhum deles recebe uma senha escolhida no atendimento

  Cenário: Abrir a tela não redefine senha nenhuma
    Dado que abro a tela S013T
    Então nenhuma senha é redefinida
    E vejo a descrição do tipo de órgão da sessão e a data do sistema
    E a tela apenas confere se ela está cadastrada e se a minha matrícula tem acesso

  Cenário: A redefinição é na mesma mensagem, sem confirmação
    Dado que a matrícula informada é de um funcionário cadastrado
    Quando informo a matrícula funcional
    Então a senha é redefinida nessa mesma mensagem
    E não vejo a senha nova nem a lista do que foi alterado

  Cenário: Matrícula não cadastrada
    Dado que informo uma matrícula que não existe no cadastro de funcionários
    Quando confirmo a mensagem
    Então nada é redefinido
    E o sistema fica marcado como não tendo encontrado o registro

  Cenário: Matrícula não numérica
    Dado que informo uma matrícula que não é número
    Quando confirmo a mensagem
    Então o campo é recusado antes da consulta ao cadastro
    E o cursor volta para o campo da matrícula

  Cenário: Cadastro marcado como excluído
    Dado que o cadastro da matrícula informada está marcado como excluído
    Quando confirmo a mensagem
    Então vejo o aviso "Key deleted" junto ao campo da matrícula

  Cenário: Redefinir a própria senha
    Dado que a matrícula informada é a minha e não tenho o privilégio especial
    Quando confirmo a mensagem
    Então vejo a mensagem "* Nao atualize seu proprio cadastro *"
    E nada é redefinido

  Cenário: Redefinir a senha de quem tem nível de acesso maior
    Dado que a matrícula informada é de um funcionário com nível de acesso maior que o meu
    Quando confirmo a mensagem
    Então vejo a mensagem "* Seu nivel de acesso nao permite esta operacao *"
    E nada é redefinido

  Cenário: A opção de consulta também redefine a senha
    Dado que informo a matrícula de um funcionário cadastrado junto com a opção de consulta
    Quando confirmo a mensagem
    Então a senha é redefinida do mesmo jeito
    E nenhuma autorização de operação me é exigida

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não tem a tela S013T
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Sem autorização para a operação
    Dado que o meu código de acesso tem a tela S013T sem a alteração liberada
    E informo a opção de alteração com a matrícula de um funcionário cadastrado
    Quando confirmo a mensagem
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é redefinido

  Cenário: Tela não disponível
    Dado que a tela S013T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Tela retirada do cadastro
    Dado que a tela S013T foi retirada do cadastro de telas
    Quando confirmo uma mensagem
    Então vejo a mensagem "* Tela nao cadastrada *"

  Cenário: Opção não reconhecida
    Dado que informo uma opção que a tela não reconhece
    Quando confirmo a mensagem
    Então vejo a mensagem "* Operacao nao disponivel *"

  Cenário: A resposta volta com dois campos em branco
    Dado que a tela abriu mostrando a descrição do tipo de órgão da sessão e a data do sistema
    Quando respondo uma mensagem
    Então a resposta vem com esses dois campos em branco
```
