# US — S016T — Conferência da matrícula funcional do servidor

## Estória

Como **servidor de CRE que atende a inclusão de quem vai usar o sistema**, quero
**conferir a situação do servidor pela matrícula funcional antes de abrir a inclusão — se
já tem cadastro de usuário e se o registro funcional dele existe —**, para que **a
inclusão só comece sobre quem realmente pode ser cadastrado, sem criar cadastro dobrado
nem cadastro de quem não consta do registro de pessoal**.

Esta tela é a primeira porta da inclusão de usuário: ela confere, antes de qualquer
gravação, se a matrícula informada já tem cadastro no sistema e se o registro funcional
daquela pessoa existe no sistema de pessoal. Sem essa conferência, a inclusão abriria
sobre qualquer matrícula digitada — inclusive sobre alguém que já entra no sistema, o que
duplicaria o acesso, ou sobre um número que não corresponde a ninguém. A tela também
lista os usuários já cadastrados, para que quem atende escolha a pessoa certa em vez de
digitar um número de memória.

## Contexto

Jornada S000M → S001M → S004M → S016T.
Ator: servidor de CRE — confere, pela matrícula funcional, se o servidor já tem cadastro
de usuário e se o registro funcional dele existe, e daí encaminha a inclusão do usuário.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O encaminhamento até esta tela não passa por nenhuma decisão de negócio: os dois passos
anteriores da jornada são menus e, no caminho desta jornada, **nenhum deles escolhe a
operação desta tela** — nem o menu que a abre, nem o menu antes dele. A tela abre, por
isso, na operação de consulta, que é a operação que ela assume quando não lhe dizem
outra coisa. É esta tela que decide o que a tela seguinte abre para fazer: ao confirmar a
conferência com a inclusão, ela **troca a operação para alteração** e entrega a matrícula,
o nome e a origem do servidor.

## Regras de negócio

### RN-01 — A tela é a conferência que antecede a inclusão do usuário

Esta tela não é o cadastro de usuários: ela é a conferência que antecede a inclusão.
Ela lê o cadastro de usuários, lê o cadastro de telas e conversa com o sistema de pessoal;
por ela mesma, **não grava nada** — não inclui, não altera e não exclui cadastro nenhum.
A inclusão propriamente dita acontece na tela seguinte, que esta tela abre.

### RN-02 — Abrir a tela não lê cadastro de usuário nenhum

Enquanto a tela é apenas aberta, nenhum cadastro de usuário é lido e o único cadastro
consultado é o de telas, para confirmar que esta tela existe. A abertura também passa a
conferência de acesso e mostra a descrição do tipo de órgão da sessão e a data do sistema.
O cadastro de usuários só é lido depois de uma mensagem respondida por quem opera.

### RN-03 — A tela abre na consulta e só aceita incluir ou consultar

A tela assume a operação de consulta por padrão. Com a operação confirmada, ela só
reconhece duas: **incluir** e **consultar**. Qualquer outra operação é recusada com a
mensagem **\* Operacao nao disponivel. Use INC ou CON \***, o cursor volta ao campo da
operação e nada mais acontece: a tela não lê o cadastro de usuários e não encaminha para
a tela seguinte.

### RN-04 — Quem abre esta tela não escolhe a operação

No caminho desta jornada, nenhum dos dois menus anteriores deixa operação alguma para
esta tela. Ela abre, portanto, na consulta, e é essa consulta que a tela repassa adiante
quando nada mais acontece. Trocar a operação para incluir depende de o campo da operação
ser preenchido por quem está atendendo, na própria tela.

[?] Se o operador consegue trocar a operação nesta tela não se conclui dos fontes desta
jornada: os fontes do lote não trazem a definição da tela, e são eles que dizem quais
campos o operador pode preencher. Se a operação não puder ser trocada aqui, a única
operação que chega à tela seguinte é a consulta. Pergunta ao site.

### RN-05 — A tela mostra os usuários já cadastrados na própria mensagem

A tela exibe, na mesma mensagem em que o operador trabalha, os usuários já cadastrados no
sistema: **onze** linhas, e em cada linha o nome do servidor, a matrícula funcional e a
marca da situação do cadastro. A tela não tem operação própria de virar página: ela
mostra as onze primeiras linhas do cadastro de usuários e não oferece caminho para as
seguintes.

[?] O que acontece quando o cadastro de usuários tem mais de onze usuários não se conclui
dos fontes desta jornada: a tela lê as onze primeiras linhas e não tem ação que recomece
a leitura a partir de uma matrícula ou de uma página. Se os usuários seguintes ficam
inalcançáveis por esta tela, o fonte não diz. Pergunta ao site.

### RN-06 — Onde a tela procura o nome digitado

O nome que o operador vê e informa nessa faixa é também o critério pelo qual a tela
percorre o cadastro de usuários: ela procura a matrícula funcional cujo nome é o
informado, e não a matrícula pelo número. O nome não é recusado se tiver espaços à
direita.

### RN-07 — Cada linha mostra a situação do cadastro de usuário

Cada uma das onze linhas traz a marca da situação do cadastro daquele usuário: cadastro
**incluído**, cadastro **alterado** ou cadastro **excluído**. É essa marca que diz, sem
abrir o cadastro, se o usuário está ativo ou se já foi desligado.

### RN-08 — Sem usuário cadastrado, a tela avisa e não encaminha

Quando o nome informado não corresponde a nenhum usuário do cadastro, a tela devolve em
branco o campo do nome e as onze linhas da faixa e mostra a mensagem
**\* Nao existem usuarios cadastrados \***; a mensagem termina ali, sem encaminhar para a
tela seguinte.

[?] O aviso de que não existem usuários aparece mesmo quando existem outros usuários no
cadastro: ele diz respeito ao nome que foi informado, e não ao cadastro inteiro. Se este
aviso deveria ser diferente — "usuário não cadastrado", por exemplo —, o fonte não diz.
Pergunta ao site.

### RN-09 — A situação do cadastro tem de ser uma das três

Antes de encaminhar, a tela confere a marca de situação do cadastro do usuário escolhido.
Não sendo uma das três — incluído, alterado ou excluído —, a tela **reabre a si mesma**
com a matrícula e o nome que o operador informou, sem encaminhar e sem gravar nada.

### RN-10 — Cadastro excluído não é encaminhado

Quando o usuário escolhido tem o cadastro marcado como **excluído**, a tela recusa o
encaminhamento com a mensagem **\* Usuario nao cadastrado \***, o cursor volta à linha
daquele usuário e a mensagem termina sem passar para a tela seguinte.

### RN-11 — A inclusão confere se a matrícula já tem cadastro

Confirmada a mensagem com a operação de **incluir**, sobre a matrícula mostrada na linha
do usuário, a tela procura essa matrícula no cadastro de usuários. Achando, a inclusão é
recusada com **\* Matricula ja cadastrada \***, o cursor volta ao campo da matrícula e
nada é gravado nem encaminhado.

[?] A recusa por matrícula já cadastrada exige, no fonte, que a linha escolhida seja a
décima primeira da faixa, e a tela escolhe a linha da décima primeira posição justamente
quando já encontrou o usuário procurado. As duas condições não fecham: ou a recusa vale
para outro caso, ou esse caminho ficou inalcançável. Pergunta ao site.

### RN-12 — A inclusão confere se o registro funcional existe no sistema de pessoal

Não achando cadastro de usuário para aquela matrícula, a tela consulta o sistema de
pessoal e pergunta se aquela pessoa existe lá. A resposta tem de ser a de que a pessoa
**existe**: sendo, a tela recusa o encaminhamento mostrando a mensagem devolvida pelo
próprio sistema de pessoal, com o cursor de volta ao campo da matrícula, e a mensagem
termina sem passar para a tela seguinte. Se a consulta ao sistema de pessoal falhar — sem
resposta válida —, a mensagem também termina sem encaminhar.

### RN-13 — A confirmação da inclusão entrega a matrícula e o nome à tela de alteração

Só depois das duas conferências — a de que a matrícula não tem cadastro de usuário e a de
que o registro funcional existe no sistema de pessoal — a tela passa adiante. Ela entrega
à tela seguinte a **matrícula funcional**, o **nome** e a **origem** do servidor que o
sistema de pessoal devolveu, e converte a operação para **alteração**. É por causa disso
que a tela seguinte abre o cadastro daquela matrícula em modo de alteração e não em
consulta.

[?] A operação que esta tela entrega é a de alteração, mesmo quando a matrícula ainda não
tem cadastro de usuário — que é justamente o caso em que se quer incluir. Se a tela
seguinte aceita incluir um cadastro que não existe quando recebe a operação de alteração,
os fontes desta jornada não dizem: é a tela seguinte que decide. Pergunta ao site.

### RN-14 — A consulta mostra o cadastro e não grava nada

Com a operação de consulta sobre uma matrícula que tem cadastro de usuário, a tela
apenas mostra o que está gravado e termina. Nenhum cadastro é incluído, alterado ou
excluído e nenhum registro de auditoria é escrito: a tela desta jornada não tem caminho
que grave.

### RN-15 — As conferências comuns de tela, operação e acesso valem aqui

Toda mensagem passa pelas conferências comuns. A da rota exige que a tela esteja no
cadastro de telas — tendo sido retirada, a recusa é **\* Tela nao cadastrada \*** — e
reconhece como operação a inclusão, a alteração, a exclusão, a consulta, o retorno, o
menu e a saída; não reconhecendo, o aviso é **\* Operacao nao disponivel \***. A do
acesso exige esta tela no cadastro de telas por código de acesso da matrícula que opera —
não estando, a recusa é **\* Acesso negado para esta matricula \*** — e, para a inclusão,
a alteração e a exclusão, a liberação daquela operação no mesmo cadastro — não tendo, a
recusa é **\* Acesso negado para esta operacao \***. Ao abrir, a conferência ainda exige
que a tela exista no cadastro de telas — não existindo, o aviso é
**\* Tela nao disponivel \***.

## Cenários BDD

```gherkin
Funcionalidade: Conferência da matrícula funcional antes da inclusão do usuário do sistema

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela S016T

  Cenário: Abrir a tela não lê nem grava cadastro de usuário
    Dado que abro a tela S016T pelo menu
    Quando a tela aparece
    Então vejo a descrição do tipo de órgão da sessão e a data do sistema
    E a tela apenas confere se ela está cadastrada e se a minha matrícula tem acesso
    E nenhum cadastro de usuário foi lido ou gravado

  Cenário: Consulta de um usuário cadastrado
    Dado que informo o nome de um servidor que tem cadastro de usuário
    Quando confirmo a mensagem com a operação de consulta
    Então vejo o cadastro daquele usuário com a situação dele
    E nada é gravado

  Cenário: A lista dos usuários já cadastrados aparece na própria mensagem
    Dado que o cadastro de usuários tem usuários incluídos
    Quando a tela aparece
    Então vejo até onze linhas, cada uma com o nome do servidor, a matrícula funcional e a situação do cadastro
    E não há operação nesta tela para ver as linhas seguintes

  Cenário: Nenhum usuário com o nome informado
    Dado que informo um nome que não corresponde a nenhum usuário cadastrado
    Quando confirmo a mensagem
    Então o campo do nome e as onze linhas voltam em branco
    E vejo a mensagem "* Nao existem usuarios cadastrados *"
    E a mensagem termina sem passar para a tela seguinte

  Cenário: Cada linha mostra se o cadastro foi incluído, alterado ou excluído
    Dado que o cadastro de um usuário está marcado como alterado
    Quando a tela aparece
    Então aquela linha mostra a marca de cadastro alterado
    E um cadastro marcado como excluído aparece marcado como excluído

  Cenário: Operação que não é incluir nem consultar
    Dado que informo uma operação que não é a de incluir nem a de consultar
    Quando confirmo a mensagem
    Então vejo a mensagem "* Operacao nao disponivel. Use INC ou CON *"
    E o cursor volta para o campo da operação
    E nada é lido do cadastro de usuários e nada é encaminhado

  Cenário: Situação do cadastro desconhecida
    Dado que a linha escolhida do usuário está com a situação do cadastro fora das três previstas
    Quando confirmo a mensagem
    Então a tela é reaberta com a matrícula e o nome que informei
    E nada é gravado e nada é encaminhado

  Cenário: Cadastro de usuário marcado como excluído
    Dado que a linha escolhida do usuário está com o cadastro marcado como excluído
    Quando confirmo a mensagem
    Então vejo a mensagem "* Usuario nao cadastrado *"
    E o cursor volta à linha daquele usuário
    E a mensagem termina sem passar para a tela seguinte

  Cenário: Inclusão de matrícula que já tem cadastro de usuário
    Dado que a matrícula mostrada na linha escolhida já tem cadastro de usuários
    Quando confirmo a mensagem com a operação de incluir
    Então vejo a mensagem "* Matricula ja cadastrada *"
    E o cursor volta ao campo da matrícula
    E nada é gravado e nada é encaminhado

  Cenário: Inclusão de matrícula cujo registro funcional não existe no sistema de pessoal
    Dado que a matrícula mostrada na linha escolhida não tem cadastro de usuários
    E o sistema de pessoal responde que aquela pessoa não existe
    Quando confirmo a mensagem com a operação de incluir
    Então vejo a mensagem que o sistema de pessoal devolveu, junto ao campo da matrícula
    E o cursor volta ao campo da matrícula
    E a mensagem termina sem passar para a tela seguinte

  Cenário: A consulta ao sistema de pessoal não responde
    Dado que a matrícula mostrada na linha escolhida não tem cadastro de usuários
    E a consulta ao sistema de pessoal não devolve resposta válida
    Quando confirmo a mensagem com a operação de incluir
    Então a mensagem termina sem passar para a tela seguinte
    E nada é gravado

  Cenário: Inclusão de quem consta do sistema de pessoal e não tem cadastro de usuário
    Dado que a matrícula mostrada na linha escolhida não tem cadastro de usuários
    E o sistema de pessoal responde que aquela pessoa existe
    Quando confirmo a mensagem com a operação de incluir
    Então a tela entrega à tela seguinte a matrícula funcional, o nome e a origem do servidor
    E a tela seguinte abre o cadastro daquela matrícula em modo de alteração

  Cenário: Sem autorização para a tela
    Dado que o meu código de acesso não tem a tela S016T
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Sem autorização para a operação
    Dado que o meu código de acesso tem a tela S016T sem a inclusão liberada
    E informo a operação de incluir
    Quando confirmo a mensagem
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: Tela não disponível
    Dado que a tela S016T não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E não consigo operar

  Cenário: Tela retirada do cadastro
    Dado que a tela S016T foi retirada do cadastro de telas
    Quando confirmo uma mensagem
    Então vejo a mensagem "* Tela nao cadastrada *"
    E nada é encaminhado

  Cenário: Operação não reconhecida
    Dado que informo uma operação que a tela não reconhece
    Quando confirmo a mensagem
    Então vejo a mensagem "* Operacao nao disponivel *"
```
