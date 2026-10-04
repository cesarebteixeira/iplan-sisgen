# US — ENTRADA — Entrada no sistema

## Estória

Como **servidor da Secretaria**, quero **entrar no sistema com a minha matrícula,
a minha senha e a secretaria em que atuo**, para que o sistema saiba quem sou e me
deixe alcançar apenas o que é do meu órgão e da minha coordenadoria.

A entrada é o portão de tudo: é ela que confere a senha, aplica a política de
prazo, escolhe a secretaria e deixa na sessão o tipo de órgão, a CRE e o órgão
filho. **Tudo o que as telas seguintes permitem ou recusam sai daqui** — e é por
isso que esta jornada é comum a todas as outras.

## Contexto

Jornada LOGON → S000M (2 passos).
Ator: servidor de CRE — entra no sistema e escolhe o módulo por onde segue.

Esta é a **entrada comum às demais jornadas**: das 339 trilhas do grafo, 338
começam em `LOGON > S000M`; a única que não passa pelo menu é a da troca de senha
(`S011T`), que sai direto da entrada. As estórias das telas começam no menu e
**não repetem** estas regras — elas apontam para este documento. Regra da entrada
descoberta ao analisar uma tela entra aqui, e não na estória da tela.

---

## Regras de negócio

### RN-01 — O servidor se identifica por cinco dados

Para entrar, o servidor informa cinco dados: a **secretaria** em que atua (2
dígitos), a **matrícula funcional** (9), a **senha** (6), a **tela por onde quer
entrar** (6) e uma **opção** (1). A tela mostra a matrícula sob o rótulo
**MATR.FUNCIONARIO**. Só a secretaria, a matrícula e a senha são conferidas contra
os cadastros; a tela pedida só é conferida se foi informada; o campo de opção,
quando preenchido, encerra o acesso (RN-14).

### RN-02 — Matrícula e secretaria passam pela edição numérica

Os dois códigos são tratados como número: o que estiver em branco vira zero, os
zeros à esquerda são descartados e o que não for número é recusado, com o cursor
de volta ao campo — a secretaria com 2 dígitos e a matrícula com 9. O que não
passa por essa edição não chega à consulta do cadastro.

### RN-03 — A segunda página da tela de entrada é negada

A entrada não tem página 2. Quando a requisição chega marcada como resposta de
paginação — a marca que o próprio sistema põe quando devolve uma tela e espera a
continuação —, a entrada é recusada com **\* Acesso a pagina 2 negado \*** e o
acesso termina ali, antes de qualquer conferência.

### RN-04 — Cinco erros de senha na mesma sessão travam o cadastro

A senha digitada é codificada pela rotina de senha do sistema e comparada com a
senha guardada no cadastro do funcionário. Cada erro conta uma tentativa; o
contador é **por matrícula dentro da sessão** — quando a matrícula digitada muda,
ele volta a zero. Na **quinta** tentativa errada o cadastro é travado (a data de
atualização da senha recebe o marcador **20000101**) e gravado. A cada erro,
inclusive no quinto, o servidor vê **\* Senha Invalida. Sera bloqueada na 5a
tentativa \***, com o cursor de volta à senha, e nada mais é conferido.

[?] O contador de tentativas vive na área de trabalho da sessão. Se o servidor se
desconectar e voltar, ou trocar de terminal, ele reinicia ou continua de onde
estava? A política de segurança depende disso e o acervo não decide.

### RN-05 — Cadastro travado por tentativas não entra, nem com a senha certa

Antes de conferir a senha, o sistema olha a data da última atualização do
cadastro: quando ela é o marcador de bloqueio **20000101** e a diferença de dias
entre essa data e o dia corrente é maior que **45** (a mesma conta da RN-06), o
acesso é recusado com **\* Senha bloqueada. Contate o Sub-Gestor da area. \***,
com o cursor de volta à matrícula. As duas condições são as do fonte; a segunda
está em questão na RN-06.

### RN-06 — O prazo da senha: 34 dias desviam, 45 dias travam

Passada a conferência da senha, o sistema usa a diferença de dias entre a data do
cadastro e o dia corrente para decidir o destino da entrada:

| diferença apurada | o que acontece |
| --- | --- |
| até 34 | a entrada segue para a tela pedida, ou para o menu |
| 35 a 45 | a entrada é desviada para a **troca de senha** (`S011T`), sem travar o cadastro |
| mais de 45 | a entrada é desviada para a troca de senha **e** o cadastro é travado, com o marcador **20040101** gravado antes do desvio |

[?] A diferença é calculada como **a data do cadastro menos a data do dia**, e o
acervo não traz a rotina que converte cada data no número de dia usado nessa
conta. Se esse número cresce com o tempo, a diferença é negativa para toda senha
trocada no passado e as três faixas acima não acontecem — nem a recusa da RN-05,
que exige mais de 45; a única troca forçada seria a da senha-padrão (RN-07). Se
ele decresce com o tempo — é o que o nome do campo de data do sistema, "data
invertida", sugere —, a diferença é a idade da senha e as faixas valem. O fonte
lê a mesma diferença nos dois pontos e não decide entre as duas leituras; pergunta
ao site.

### RN-07 — A senha-padrão obriga a troca

O próprio LOGON carrega a palavra **SENHA** como referência e compara a senha
guardada com a codificação dela: se forem iguais, a senha ainda é a de fábrica e a
entrada é desviada para a troca, antes de o servidor chegar ao menu — mesmo com a
senha em dia. Essa conferência é feita na faixa de até 34 dias da RN-06; acima
disso o desvio da própria RN-06 já levou o servidor para a troca.

[?] A entrada só **compara**: o que grava a senha de fábrica no cadastro de um
funcionário novo não está nesta jornada. Confirme com o site quem dá a senha
inicial.

### RN-08 — A secretaria informada precisa existir

A secretaria digitada é procurada no cadastro de secretarias. Não existindo — ou
estando marcada como excluída — a entrada é recusada com **\* Secretaria nao
cadastrada \***, com o cursor de volta à secretaria, e nada mais é conferido. Do
cadastro sai o nome da secretaria que o menu mostra depois.

### RN-09 — A matrícula precisa constar do cadastro do funcionário

A matrícula é procurada no cadastro de funcionários. Não existindo — ou estando
marcada como excluída — a entrada é recusada com **\* Matricula nao cadastrada \***,
com o cursor de volta à matrícula. É desse cadastro que saem a estação da sessão
(quando o acesso vem pelo serviço WEB) e o privilégio do servidor.

### RN-10 — Sem nenhuma secretaria não entra; com mais de uma, o servidor escolhe

Quando o servidor deixa a secretaria em branco, o sistema conta os vínculos da
matrícula nos órgãos:

- **nenhum** — recusa com **\* Usuario nao cadastrado em nenhuma Secretaria \***;
- **mais de um** — recusa com **\* Informe Secretaria \***, porque o sistema não
  escolhe pelo servidor;
- **exatamente um** — adota esse vínculo e segue.

### RN-11 — O vínculo define o alcance do servidor na sessão

Do vínculo entre a matrícula e a secretaria saem quatro coisas que a jornada
inteira usa depois: o **tipo de órgão**, o **código de acesso**, a **CRE** e o
**órgão filho** do servidor — e, com eles, o nome da secretaria. São esses
valores que limitam o que as telas seguintes deixam consultar e gravar. A
secretaria informada e a matrícula precisam ter esse vínculo: sem ele, a recusa é
**\* Usuario sem acesso a esta Secretaria \***.

### RN-12 — A tela inicial só abre se estiver autorizada

Se o servidor pediu uma tela inicial, o sistema confere a autorização dele no
cadastro de telas por código de acesso — que guarda, por operação, se a consulta,
a inclusão, a alteração e a exclusão estão liberadas. Sem o registro, a recusa é
**\* Usuario sem acesso a esta tela \***. Não informando tela inicial, o destino é
o menu principal `S000M`.

### RN-13 — A entrada registra a sessão aberta

Passando por todas as conferências, o sistema grava no cadastro do funcionário que
a sessão está **aberta**, com a estação, a data e a hora. A estação é a do
terminal; quando o acesso vem pelo serviço WEB, ela é trocada pela estação do
cadastro do funcionário — e é essa estação que a abertura do menu confere depois:
não coincidindo com a do cadastro, a sessão é encerrada.

[?] O que faz a estação do acesso chegar como **WEB** — que terminal ou serviço é
esse — não está nesta jornada; o campo de estação do sistema é que traz a marca.

### RN-14 — A opção preenchida encerra o acesso

Se o servidor preencheu o campo de opção, o LOGON não abre o menu: encerra a
sessão e devolve o terminal à tela de entrada. É a saída do sistema, e é o que o
grafo de navegação registra como destino dessa opção.

### RN-15 — A entrada limpa requisições e arquivos vencidos

Quando a tela de entrada é aberta — antes de conferir a senha —, ela apaga o que
venceu, em duas varreduras independentes:

- no **cadastro de requisições**, apaga os registros cuja data da requisição é
  anterior à data do dia, **exceto** os marcados com tipo de impressão "B", que
  ficam;
- no **cadastro de arquivos**, apaga os registros com data anterior a um mês
  atrás.

É manutenção por efeito colateral da entrada, feita em laço até o fim de cada
conjunto.

[?] Por que as requisições do tipo "B" ficam de fora da limpeza? O que essa marca
quer dizer não está nesta jornada.

[?] As duas varreduras são abertas sem que a entrada informe a chave do vínculo —
o código da requisição, de um lado, e o tipo de órgão, a CRE, a data e o número
do processo, do outro. Como as duas fichas de vínculo ocupam a mesma área, a
chave que a varredura usa é o que tiver ficado ali, e o corpus não diz o que o
módulo de dados alcança com ela em branco. Pergunta ao site se a limpeza é de
todos os registros vencidos ou só dos do vínculo que ficou na área.

### RN-16 — O S000M é o menu principal: 7 opções, uma por módulo

O menu principal mostra a **secretaria** (o tipo de órgão da sessão) e a **data do
sistema**, lê o próprio nome no cadastro de telas e **não grava nada**. Ao voltar
da troca de senha, mostra **\* Senha alterada com sucesso \***. Cada uma das suas 7
opções abre um módulo:

| opção | módulo |
| --- | --- |
| 1 | C000M |
| 2 | E000M |
| 3 | F000M |
| 4 | N000M |
| 5 | M000M |
| 6 | P000M |
| 7 | S001M |

Antes de encaminhar, o menu passa pela lógica de rota e pela conferência da
permissão do servidor para a tela de destino. Opção não informada simplesmente não
faz nada; com mais de uma opção preenchida, o menu encaminha pela primeira, na
ordem das opções.

---

## Cenários BDD

```gherkin
Funcionalidade: Entrada no sistema

  Cenário: Entrada com matrícula, senha e secretaria válidas
    Quando informo a matrícula, a senha e a secretaria corretas
    Então o sistema registra a minha sessão
    E me coloca no menu principal S000M

  Cenário: Matrícula ou secretaria não numérica
    Quando informo uma matrícula ou uma secretaria que não é número
    Então a entrada recusa o campo antes de consultar o cadastro
    E o cursor volta para o campo

  Cenário: Segunda página da entrada negada
    Quando a entrada chega marcada como resposta de paginação
    Então vejo a mensagem "* Acesso a pagina 2 negado *"
    E não entro no sistema

  Cenário: Senha errada até a quarta tentativa
    Dado que informo a matrícula de um servidor cadastrado
    Quando digito uma senha diferente da senha guardada
    Então vejo "* Senha Invalida. Sera bloqueada na 5a tentativa *"
    E ainda posso tentar de novo

  Cenário: Senha errada na quinta tentativa trava o cadastro
    Dado que já errei a senha quatro vezes
    Quando erro a senha pela quinta vez
    Então o meu cadastro é travado, com o marcador de bloqueio na data da senha
    E não entro no sistema

  Cenário: Cadastro travado por tentativas é recusado, mesmo com a senha certa
    Dado que o meu cadastro está marcado com o bloqueio por tentativas
    Quando informo a senha correta
    Então vejo "* Senha bloqueada. Contate o Sub-Gestor da area. *"
    E o acesso é recusado

  Cenário: Senha com mais de 34 dias obriga a troca
    Dado que a minha senha não é atualizada há mais de 34 dias
    Quando informo a senha correta
    Então sou levado à tela de troca de senha S011T
    E não sigo direto para o menu

  Cenário: Senha com mais de 45 dias obriga a troca e trava o cadastro
    Dado que a minha senha não é atualizada há mais de 45 dias
    Quando informo a senha correta
    Então sou levado à troca de senha
    E o meu cadastro fica marcado como travado

  Cenário: Senha ainda é a senha-padrão
    Dado que a minha senha guardada ainda é a senha-padrão do sistema
    Quando informo a senha correta
    Então sou obrigado a trocá-la antes de entrar

  Cenário: Secretaria não cadastrada
    Quando informo uma secretaria que não existe
    Então vejo "* Secretaria nao cadastrada *"
    E o cursor volta para o campo da secretaria

  Cenário: Matrícula não cadastrada
    Quando informo uma matrícula que não existe
    Então vejo "* Matricula nao cadastrada *"
    E o cursor volta para o campo da matrícula

  Cenário: Servidor sem nenhuma secretaria
    Dado que a minha matrícula não tem vínculo com nenhuma secretaria
    Quando deixo a secretaria em branco
    Então vejo "* Usuario nao cadastrado em nenhuma Secretaria *"

  Cenário: Servidor com mais de uma secretaria precisa escolher
    Dado que tenho vínculo em mais de uma secretaria
    Quando deixo a secretaria em branco
    Então vejo "* Informe Secretaria *"

  Cenário: Servidor com uma única secretaria não precisa informá-la
    Dado que tenho vínculo em exatamente uma secretaria
    Quando deixo a secretaria em branco
    Então o sistema adota essa secretaria
    E entro normalmente

  Cenário: Servidor sem acesso à secretaria informada
    Quando informo uma secretaria com a qual não tenho vínculo
    Então vejo "* Usuario sem acesso a esta Secretaria *"

  Cenário: A entrada deixa na sessão o alcance do servidor
    Dado que entro com um vínculo válido entre a matrícula e a secretaria
    Então a sessão fica com o tipo de órgão, o código de acesso, a CRE e o órgão filho
    E fica com o privilégio do servidor

  Cenário: Tela inicial não autorizada
    Quando informo uma tela inicial para a qual não tenho autorização
    Então vejo "* Usuario sem acesso a esta tela *"

  Cenário: Tela inicial autorizada abre direto nela
    Dado que tenho autorização para a tela que informei
    Quando confirmo a entrada
    Então o sistema abre essa tela
    E não passa pelo menu principal

  Cenário: A entrada registra a sessão aberta
    Dado que entrei com credenciais válidas
    Então a minha sessão fica registrada como aberta, com estação, data e hora

  Cenário: A estação do acesso WEB é a do cadastro
    Dado que o meu acesso chega identificado como WEB
    Quando entro com credenciais válidas
    Então a sessão fica com a estação registrada no meu cadastro
    E não com a marca WEB

  Cenário: A opção preenchida encerra o acesso
    Dado que preenchi o campo de opção
    Quando confirmo a entrada
    Então o sistema encerra a sessão
    E não me leva ao menu

  Cenário: A entrada apaga o que venceu
    Dado que a tela de entrada é aberta
    Quando a limpeza de vencidos é executada
    Então as requisições anteriores à data do dia são apagadas
    Mas as requisições marcadas com tipo de impressão "B" permanecem
    E os arquivos anteriores a um mês são apagados

  Cenário: Aviso de troca de senha no menu principal
    Dado que vim da tela de troca de senha S011T
    Quando chego ao menu principal
    Então vejo o aviso "* Senha alterada com sucesso *"

  Esquema do Cenário: Do menu principal para cada módulo
    Dado que estou no menu principal
    Quando escolho a opção <opção>
    Então chego ao módulo <módulo>
    E o menu não grava nada

    Exemplos:
      | opção | módulo |
      | 1 | C000M |
      | 2 | E000M |
      | 3 | F000M |
      | 4 | N000M |
      | 5 | M000M |
      | 6 | P000M |
      | 7 | S001M |

  Cenário: Opção do menu não informada
    Dado que estou no menu principal
    Quando não informo nenhuma opção
    Então o sistema não me encaminha para lugar nenhum
```
