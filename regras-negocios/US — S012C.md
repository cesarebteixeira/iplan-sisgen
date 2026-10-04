# US — S012C — Consulta de usuários pela origem

## Estória

Como **servidor de CRE**, quero **consultar a relação de usuários do sistema
agrupada pela origem de cada um e abrir a ficha do usuário que eu escolher**, para
que **eu veja quem tem acesso ao sistema e de que origem cada um é, sem precisar
saber a matrícula de antemão**.

O cadastro de usuários é o que a entrada do sistema consulta para reconhecer quem
chega, e é nele que ficam a senha, o privilégio e a situação de sessão de cada
servidor. Esta tela é a leitura desse cadastro pela origem: sem ela, quem
administra o acesso não tem como ver os servidores de uma mesma origem lado a
lado, e só alcança a ficha de um usuário sabendo a matrícula dele de antemão.

## Contexto

Jornada S000M → S001M → S005M → S012C.
Ator: servidor de CRE — consulta a relação de usuários do sistema pela origem e
abre a ficha do usuário que escolher.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra
de negócio.

A tela desta jornada é a **S012C**, e ela não termina em si: escolhido um usuário,
ela passa esse usuário adiante, para a tela do usuário (`S010T`), sem passar por
menu.

As duas telas do meio da jornada são menus, e a tela desta jornada é aberta por
uma opção de menu — não por encadeamento de tela.

As regras abaixo são só as da tela desta jornada. As regras da entrada não se
repetem aqui: o que se reconheceu como delas está no anexo de evidências.

---

## Regras de negócio

### RN-01 — A tela só abre para quem tem autorização, e na estação da sessão

A `S012C` é tela autorizada: para ela abrir, o sistema confere se o servidor tem
autorização de acesso àquela tela, pelo código de acesso do seu perfil. Sem essa
autorização, a tela não abre, a lista não chega a ser montada e o servidor vê a
mensagem do sistema. O sistema confere também a estação: a estação registrada na
sessão precisa ser a mesma do cadastro do servidor; não sendo, a sessão é
encerrada. Os dados dessa conferência — matrícula, código de acesso, privilégio,
tipo de órgão e CRE — são os que a entrada deixou na sessão.

[?] O texto que o servidor lê quando não tem autorização vem de uma rotina de
mensagens que não é desta jornada; o que aparece na linha de mensagem é pergunta
ao site.

[?] A recusa por estação desvia para uma tela de encerramento que não é desta
jornada; o que o servidor vê nela, e se a sessão é apenas encerrada, é pergunta ao
site.

### RN-02 — A tela abre em consulta e não grava nada

A tela é de consulta: quaisquer que sejam o modo e a tela de destino informados no
pedido que a abre, ela se apresenta em consulta — e quem chega por uma opção de
menu não muda isso. Da tela não sai inclusão, alteração nem exclusão do cadastro
de usuários: ela lista e, no máximo, passa adiante o usuário escolhido. Confirmar
a tela sem marcar nenhuma linha não altera nada.

A tela também não muda de comportamento conforme quem a chamou: ela não lê a tela
de origem para decidir nada, e o modo que o pedido traz é trocado por consulta
antes de qualquer leitura do cadastro. O que a tela entrega adiante, isso sim,
depende do que o operador marcou: a tela seguinte recebe o usuário escolhido e a
operação de consulta.

[?] A tela não oferece operação de manutenção, mas o pedido que a abre carrega um
modo e uma tela de destino: se algum chamador pretende abrir a `S012C` em outro
modo, ele não é atendido — a tela sempre responde em consulta. Quem a chamaria
assim é pergunta ao site.

### RN-03 — A tela lista os usuários cadastrados pela origem, 13 por vez

Ao abrir, a tela percorre o cadastro de usuários e preenche **13 linhas**, cada
uma com a origem, a matrícula, o nome do funcionário e a coluna de ação. A lista
começa pela origem e, dentro da mesma origem, pela matrícula. Usuário marcado como
excluído não entra na lista.

[?] Os sinalizadores que o programa passa na leitura do cadastro são do dialeto e
não estão explicados no material desta jornada; que a lista saia na ordem do
cadastro, começando pela origem, é o que a chave do cadastro indica, mas como o
sistema ordena os textos e o que a virada de página mostra não foi verificado.

[?] O que a origem representa para o cadastro — unidade, órgão, coordenadoria — e
de onde ela é trazida quando o usuário é cadastrado não se decide nos fontes desta
jornada: a origem chega ao cadastro por rotina que não é desta tela.

### RN-04 — Sem nenhum usuário, a tela avisa

Se a lista não encontrar nenhum usuário, a tela avisa
**\* Nao existem usuarios cadastrados \*** e o ponto de partida da lista fica em
branco.

### RN-05 — O ponto de partida da lista é a origem e a matrícula

No pé da tela há o par **origem e matrícula de onde a lista começa**. Informado
pelo operador, é dele que a lista parte. Preenchendo a 13ª linha, esse par recebe
a origem e a matrícula do último usuário mostrado — é assim que a tela continua a
lista de onde parou. Chegando ao fim dos usuários, o par é limpo.

[?] Reenviando a tela com o par preenchido: o último usuário mostrado reaparece ou
a lista já começa no seguinte? Os sinalizadores da leitura não estão explicados no
material, e é isso que decide o que o operador vê na virada de página.

### RN-06 — A matrícula do ponto de partida precisa ser número

O par do pé da tela é editado como número na parte da matrícula: o que estiver em
branco vale zero — a lista começa do início —, os zeros à esquerda são descartados
e o que não for número é recusado, com o cursor de volta ao campo da matrícula. O
que não passa por essa edição não chega à consulta do cadastro.

[?] O texto que o operador lê nessa recusa vem de uma rotina de edição de dados
que não é desta jornada; a mensagem é pergunta ao site.

### RN-07 — Marcar uma linha sem matrícula é recusado

A coluna de ação é o que seleciona a linha: é marcando-a que o operador diz que é
aquele usuário. Se a linha marcada não tem matrícula — uma das linhas vazias, que
sobram quando há menos de 13 usuários —, a tela recusa com
**\* Usuario nao cadastrado \*** e devolve o cursor à coluna de ação daquela
linha. Nada é gravado.

[?] A máscara da tela não está no lote: o que a coluna de ação aceita como marca,
e qual é o rótulo dela, é pergunta ao site.

### RN-08 — Marcar a linha de um usuário entrega esse usuário à tela do usuário

Marcada a linha de um usuário que existe, o sistema carrega o cadastro daquele
usuário — nome, origem, correio eletrônico, privilégio, situação de sessão,
terminal e estação — e passa para a tela do usuário, a `S010T`, sem menu. A
matrícula marcada e a operação de consulta seguem junto com a passagem, e é em
**consulta** que a `S010T` abre por causa disso. Nada é gravado na passagem.

[?] Se a máscara deixar digitar por cima da matrícula mostrada e a matrícula
digitada não existir no cadastro, a tela não recusa: ela encaminha assim mesmo
para a tela do usuário, com o que já estava no registro. Se as colunas de
matrícula são protegidas contra digitação é pergunta ao site.

### RN-09 — A lista não é filtrada pela sessão

O cadastro de usuários não guarda secretaria, CRE nem órgão, e a lista não é
filtrada por nada da sessão: qualquer servidor autorizado, de qualquer secretaria
ou CRE, vê a mesma relação de usuários — ordenada pela origem que cada usuário tem
no próprio cadastro, e não pela origem de quem consulta.

[?] Se a base de usuários é única para todas as secretarias é pergunta ao site — é
o que o cadastro sugere, por não ter campo de secretaria.

---

## Cenários BDD

```gherkin
Funcionalidade: Consulta dos usuários do sistema pela origem na tela S012C

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela S012C

  Cenário: A tela lista os usuários cadastrados pela origem, 13 por vez
    Dado que existem usuários cadastrados
    Quando abro a S012C
    Então vejo até 13 usuários por vez, cada um com a origem, a matrícula, o nome
      e a coluna de ação
    E a lista vem ordenada pela origem e, dentro dela, pela matrícula
    E nada é gravado

  Cenário: Consulta não grava nada
    Dado que estou na S012C
    Quando confirmo a tela sem marcar nenhuma linha
    Então o cadastro de usuários fica como estava
    E nenhuma inclusão, alteração ou exclusão é registrada

  Cenário: Usuário excluído não aparece na lista
    Dado que um usuário está marcado como excluído
    Quando abro a S012C
    Então ele não aparece entre os usuários listados

  Cenário: Cadastro de usuários vazio
    Dado que não há nenhum usuário cadastrado
    Quando abro a S012C
    Então vejo a mensagem "* Nao existem usuarios cadastrados *"
    E o ponto de partida da lista fica em branco

  Cenário: A lista continua a partir do último usuário mostrado
    Dado que a lista preencheu as 13 linhas da tela
    Quando confirmo a tela
    Então a origem e a matrícula do último usuário mostrado ficam no ponto de
      partida
    E a lista continua a partir dali

  Cenário: Matrícula do ponto de partida não numérica
    Dado que informo uma matrícula que não é número no ponto de partida da lista
    Quando confirmo a tela
    Então a tela recusa o campo antes de consultar o cadastro
    E o cursor volta para o campo da matrícula

  Cenário: Marcar uma linha sem usuário é recusado
    Dado que marco a coluna de ação de uma linha sem matrícula
    Quando confirmo a tela
    Então vejo a mensagem "* Usuario nao cadastrado *"
    E o cursor volta para a coluna de ação daquela linha

  Cenário: Abrir a ficha do usuário marcado
    Dado que marco a linha de um usuário cadastrado
    Quando confirmo a tela
    Então o sistema me leva à tela do usuário, a S010T
    E a S010T abre em consulta, sobre o usuário que marquei
    E nada é gravado

  Cenário: Tela não autorizada para o meu perfil
    Dado que o meu perfil não tem autorização para a tela S012C
    Quando a tela tenta abrir
    Então o acesso é negado com a mensagem do sistema
    E a lista não é mostrada

  Cenário: Estação da sessão diferente da registrada
    Dado que a minha sessão está em estação diferente da registrada no meu cadastro
    Quando abro a S012C
    Então a minha sessão é encerrada
    E a lista não é mostrada

  Cenário: A lista é a mesma para qualquer servidor autorizado
    Dado que outro servidor, de outra CRE, abre a S012C
    Então ele vê a mesma relação de usuários
    E a lista não é filtrada por secretaria, CRE ou órgão
```
