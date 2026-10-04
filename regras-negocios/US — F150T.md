# US — F150T — Registro da capa da nota fiscal da despesa

## Estória

Como **servidor de CRE que lança a despesa da secretaria**, quero **registrar a capa
da nota fiscal — número, datas de emissão e de entrega, grupo, convênio, instituição
beneficente, fornecedor, valor total e recursos próprios — e encaminhá-la para o
lançamento dos gêneros**, para que **a nota entre no sistema presa ao grupo, ao
fornecedor e ao convênio certos, e possa receber os itens que a compõem**.

A nota fiscal é a despesa da secretaria: é por ela que o que foi comprado entra no
sistema e é conferido contra o que foi pago. Esta tela reúne os dados que identificam
a nota e confere cada um deles contra os cadastros — grupo, convênio, instituição
beneficente, fornecedor, modelo e datas. Sem essa conferência a nota não existe: o
valor lançado ficaria sem fornecedor e sem convênio a que se prender, e o lançamento
dos itens não teria por onde começar.

## Contexto

Jornada S000M → F000M → F100M → F150T.
Ator: servidor de CRE — registra a capa da nota fiscal da despesa e a encaminha para o
lançamento dos gêneros.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

A `F150T` não é menu: é a tela da capa da nota fiscal. As duas telas antes dela,
`F000M` e `F100M`, são menus e **não deixam nada na sessão que esta tela use**: o que ela
usa — o grupo de coordenação regional e a secretaria do servidor — vem da entrada, e a
tela ainda consulta o cadastro de telas. O que ela também aproveita é o que a tela de
lançamento dos gêneros deixa quando o servidor é trazido de volta para uma nota nova.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela abre em inclusão, e é a única operação que este caminho oferece

A nota fiscal não é digitada em modo nenhum: abrindo a tela — pelo menu de despesas ou
logo depois do lançamento dos gêneros — ela entra em **inclusão** e assim permanece. As
duas origens conhecidas gravam a operação **incluir** por cima da que veio de trás, de
modo que não há, nesta jornada, como abrir a tela para alterar, excluir ou consultar
uma nota já existente.

Ao abrir pelo menu, a tela parte com o **grupo da sessão** já preenchido e com o modelo
de nota fiscal que ela mesma assume. Ao ser reaberta logo depois do lançamento dos
gêneros, ela não parte em branco: assume como seus o grupo, o fornecedor, a instituição,
as datas, o convênio e os valores que aquela tela deixou, e apresenta em branco apenas
o número da nota, que é o que se vai lançar.

[?] O programa tem caminhos de **alterar**, **excluir** e **consultar** uma nota, com
avisos próprios (as confirmações de alteração e de exclusão da nota fiscal, "Nota fiscal
nao cadastrada", "Nota fiscal de desconto", "Informe o ano de entrega" e "Informe o
CNPJ / CPF do fornecedor"), e nenhuma das duas origens conhecidas deixa a operação
diferente de incluir: as duas gravam incluir por cima. Ou esses caminhos são abertos por
uma origem que não está neste acervo, ou são inalcançáveis. Pergunta ao site.

### RN-02 — O grupo (CORD.REG.ESCOLAR) é obrigatório e só vale o do servidor

A nota pertence a um grupo de coordenação regional, e é o grupo que diz de quem é a
nota e por qual recorte ela vai ser procurada nos cadastros. Sem grupo informado, a
recusa é **\* Informe o grupo \***. Com grupo diferente daquele a que o servidor está
vinculado, a recusa é **\* Usuario sem acesso a este grupo \***, com o cursor de volta ao
campo do grupo. Só o grupo do próprio servidor segue para as leituras seguintes; o
grupo da sessão é o que a tela escreve no campo ao abrir.

### RN-03 — O número da nota fiscal é obrigatório

Na inclusão, o número da nota fiscal tem de ser informado. Em branco — ou zero —, a
recusa é **\* Informe o numero da nota fiscal \***, com o cursor de volta ao campo do
número, e a tela não segue.

### RN-04 — As duas datas da nota são conferidas, uma contra a outra e contra hoje

A capa trabalha com duas datas: a de **emissão** e a de **entrega dos gêneros**. Cada
uma precisa ser uma data completa e válida (dia, mês e ano, com o ano entre 1994 e 2099)
e, além disso:

- a **data de emissão** não pode ser posterior ao dia de hoje;
- o **ano de entrega** tem de ser o mesmo ano da emissão;
- a **data de entrega** não pode ser anterior à data de emissão.

As recusas são, na ordem em que o servidor as encontra: **\* Data de emissao invalida \***,
**\* Data de emissao > que a data atual \***, **\* Data de entrega invalida \***,
**\* Ano de entrega diferente de ano emissao \*** e **\* Data de entrega < que data
emissao \***, cada uma com o cursor de volta a um dos campos de data.

### RN-05 — O convênio é obrigatório, e a instituição tem de ser do grupo e da secretaria

O convênio é o instrumento pelo qual a despesa corre, e vem com o seu ano. Em branco, a
recusa é **\* Informe numero do convenio \***, com o cursor no campo do convênio.

Informado, o sistema procura o convênio naquele ano e, dentro dele, a instituição
beneficente:

- convênio que não existe naquele ano, ou que não tem nenhuma instituição vinculada ao
  **grupo informado**, é recusado com **\* Convenio nao cadastrado \***, com o cursor no
  campo do convênio;
- a instituição vinculada ao convênio precisa estar cadastrada — não estando, a recusa é
  **\* Instituicao beneficente nao cadastrada \***;
- a instituição precisa pertencer à **mesma secretaria** do servidor — não pertencendo, a
  recusa é **\* Inst.benef nao pertence a esta secretaria \***;
- e, quando o servidor tem grupo, a instituição precisa ser do **grupo dele** — não sendo,
  a recusa é **\* Usuario sem acesso a outro grupo \***.

Todas as recusas desta regra devolvem o cursor ao campo do convênio.

[?] O aviso de instituição beneficente não cadastrada é lido logo depois de a mesma
instituição ter sido encontrada na conferência anterior, pela mesma chave (o código da
instituição que veio do convênio). Se a primeira conferência achou o registro, a segunda
acha o mesmo registro de novo — e o aviso fica inalcançável por esse caminho. Se ele é
para outro caso, pergunta ao site.

### RN-06 — O modelo da nota fiscal e o fornecedor precisam estar cadastrados

A tela trabalha com um modelo de nota fiscal fixo, que ela mesma assume ao abrir (o
modelo 55), e confere se esse modelo está cadastrado: não estando, a recusa é
**\* Modelo de nota fiscal nao cadastrado \***, com o cursor de volta ao campo.

O fornecedor, identificado pelo CNPJ/CPF informado, também precisa estar cadastrado:
não estando, a recusa é **\* Fornecedor nao cadastrado \***, com o cursor de volta ao
campo do fornecedor.

[?] O número do modelo é fixado pela própria tela e não vem de campo informado pelo
servidor; se esse é o modelo único do sistema ou se depende do tipo de despesa, é
pergunta ao site.

[?] Na inclusão, nada preenche a descrição do modelo, a razão social do fornecedor nem o
nome da instituição: quem copia esses nomes dos cadastros são os caminhos de alteração.
Se a máscara deixa digitar nesses campos na inclusão, eles não são conferidos contra
nenhum cadastro. Pergunta ao site.

### RN-07 — A nota não pode repetir uma já cadastrada

Antes de seguir, a tela procura a nota pela combinação **secretaria, fornecedor, ano de
entrega e número da nota** — o grupo não entra nessa identificação. Achando a nota:

- se ela está no **grupo do servidor** (ou se ele não tem grupo definido), a recusa é
  **\* Nota ja cadastrada \***, com o cursor no campo do número da nota;
- se ela está em **outro grupo**, a recusa é **\* Usuario sem acesso ao grupo desta
  nota \***, também com o cursor no número da nota.

Em qualquer dos casos nada é gravado, e a nota repetida não é alterada.

### RN-08 — O valor total da nota e os recursos próprios

O valor total da nota é obrigatório: em branco — ou zero —, a recusa é
**\* Informe o valor total da nota \***, com o cursor no campo do valor. E os **recursos
próprios** têm de ser menores que o valor total da nota: sendo iguais ou maiores, a
recusa é **\* Rec.proprios deve ser < valor da nota \***, com o cursor no campo dos
recursos próprios.

Os dois são valores em dinheiro, com duas casas decimais.

### RN-09 — A inclusão é confirmada antes de seguir

Passando por todas as conferências, a tela não grava e não segue: ela mostra
**\* Confirma inclusao da nota <S/N> ? \***, posiciona o cursor no campo de resposta e
espera. Respondendo que **sim**, e continuando os campos iguais ao que a tela guardou, a
nota segue para o lançamento dos gêneros.

Respondendo que **não**, a tela limpa o aviso e o que guardou e volta ao mesmo ponto: as
conferências são refeitas e a confirmação é armada outra vez. A resposta negativa não
tem caminho próprio de saída — para desistir, o servidor sai da tela ou muda um dado que
a recuse.

### RN-10 — Esta tela não grava nada: quem grava a nota é o lançamento dos gêneros

Esta tela **não grava a nota fiscal**. Ela confere, pede a confirmação e entrega: a nota
segue para o lançamento dos gêneros com o registro completo — grupo, fornecedor,
instituição, modelo, datas, convênio, valor total e recursos próprios — e com a operação
**incluir**. É na tela de lançamento dos gêneros que a nota e os seus itens são criados.

Nenhuma resposta desta tela, no caminho da inclusão, altera ou apaga cadastro algum: as
gravações que o programa tem declaradas só são alcançadas nos caminhos de alteração, de
exclusão e de manutenção dos totais por convênio, que este caminho não abre. Também não
há gravação de trilha de auditoria por esta tela na inclusão.

### RN-11 — De volta do lançamento dos gêneros, o menu de despesas já aponta a opção desta tela

Enquanto o servidor está no fluxo da nota fiscal, o menu de despesas `F100M` se comporta
de acordo com a tela de onde a sessão vem: quando a tela de lançamento dos gêneros marca
a passagem, o menu **deixa a opção que abre a F150T já marcada** e avisa
**\* Acesso deve ser feito pela tela F150T \***. Com a marca do fluxo da nota de
dedução, o mesmo acontece com a outra opção, e o aviso é **\* Acesso deve ser feito pela
tela F152T \***. Respondendo o menu, o servidor é levado à tela que a marca indica — é
assim que o sistema o devolve ao ponto em que estava.

### RN-12 — A tela precisa estar cadastrada, e o perfil do servidor autorizar

Na abertura, a tela procura a si mesma no cadastro de telas e passa pela conferência de
acesso. Não constando do cadastro de telas — ou estando a tela desativada —, ou não
estando liberada para o código de acesso da sessão, a tela é abandonada com aviso e nada
é mostrado. A mesma conferência de acesso se repete a cada resposta, junto com a lógica
de rota (que confere se a operação está disponível para a tela) e com a data e a hora do
sistema, que são as usadas nas comparações de data.

A conferência recebe o contexto da sessão: a matrícula, o código de acesso, o privilégio,
a secretaria e o grupo do servidor, além da operação e da tela.

### RN-13 — Os campos de número são editados, e o cursor volta ao primeiro campo recusado

A cada resposta, antes de qualquer conferência, a tela edita os seus **14 campos de
número**: o número da nota fiscal, o grupo, o dia, o mês e o ano de emissão, o dia, o mês
e o ano de entrega, o ano de competência, o número e o ano do convênio, o código da
instituição beneficente, o valor total da nota e os recursos próprios. Cada um é tratado
como número (o que estiver em branco vira zero e os zeros à esquerda caem) e reescrito; os
dois valores usam a vírgula como separador decimal. No primeiro campo que não passar pela
edição, o cursor volta para ele e a tela não segue.

[?] Dois desses campos — o ano de competência e o código da instituição beneficente — são
editados, mas não têm posição de cursor na tabela da tela; recusados na edição, o cursor
não é posicionado. Se isso deixa o servidor sem saber qual campo corrigir, pergunta ao
site.

---

## Cenários BDD

```gherkin
Funcionalidade: Registrar a capa da nota fiscal da despesa da secretaria

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F150T

  Cenário: A tela abre em inclusão, com o grupo da sessão preenchido
    Dado que chego à F150T pelo menu de despesas
    Quando a tela abre
    Então ela está em inclusão
    E o campo do grupo já vem preenchido com o grupo a que estou vinculado
    E o modelo de nota fiscal já vem assumido pela tela
    E nada é gravado

  Cenário: A tela reaberta depois do lançamento dos gêneros aproveita os dados
    Dado que venho do lançamento dos gêneros
    Quando a tela F150T abre
    Então ela está em inclusão
    E o grupo, o fornecedor, a instituição, as datas, o convênio e os valores vêm preenchidos com o que aquela tela deixou
    E só o número da nota fiscal vem em branco

  Cenário: Inclusão de uma nota fiscal com todos os dados válidos
    Dado que preenchi número da nota, datas, grupo, convênio, instituição e fornecedor válidos
    E informei o valor total da nota e recursos próprios menores que ele
    Quando respondo a tela
    Então vejo "* Confirma inclusao da nota <S/N> ? *"
    E respondendo que sim sou levado ao lançamento dos gêneros daquela nota

  Cenário: Resposta negativa à confirmação da inclusão
    Dado que a tela me pediu a confirmação da inclusão
    Quando respondo que não
    Então o aviso é limpo
    E a tela volta a conferir os mesmos dados
    E me pede a confirmação outra vez

  Cenário: Grupo não informado
    Dado que deixei o grupo em branco
    Quando respondo a tela
    Então vejo "* Informe o grupo *"
    E o cursor volta ao campo do grupo
    E nada é gravado

  Cenário: Grupo diferente do meu
    Dado que informei um grupo diferente daquele a que estou vinculado
    Quando respondo a tela
    Então vejo "* Usuario sem acesso a este grupo *"
    E o cursor volta ao campo do grupo
    E nada é gravado

  Cenário: Número da nota fiscal não informado
    Dado que deixei o número da nota fiscal em branco
    Quando respondo a tela
    Então vejo "* Informe o numero da nota fiscal *"
    E o cursor volta ao campo do número
    E nada é gravado

  Cenário: Data de emissão inválida
    Dado que informei uma data de emissão que não existe, ou com o ano fora de 1994 a 2099
    Quando respondo a tela
    Então vejo "* Data de emissao invalida *"
    E o cursor volta ao campo da data de emissão
    E nada é gravado

  Cenário: Data de emissão posterior a hoje
    Dado que informei uma data de emissão depois do dia de hoje
    Quando respondo a tela
    Então vejo "* Data de emissao > que a data atual *"
    E nada é gravado

  Cenário: Data de entrega inválida
    Dado que informei uma data de entrega que não existe, ou com o ano fora de 1994 a 2099
    Quando respondo a tela
    Então vejo "* Data de entrega invalida *"
    E o cursor volta ao campo da data de entrega
    E nada é gravado

  Cenário: Ano de entrega diferente do ano de emissão
    Dado que o ano da data de entrega é diferente do ano da data de emissão
    Quando respondo a tela
    Então vejo "* Ano de entrega diferente de ano emissao *"
    E nada é gravado

  Cenário: Data de entrega anterior à data de emissão
    Dado que informei a data de entrega antes da data de emissão
    Quando respondo a tela
    Então vejo "* Data de entrega < que data emissao *"
    E nada é gravado

  Cenário: Convênio não informado
    Dado que deixei o número do convênio em branco
    Quando respondo a tela
    Então vejo "* Informe numero do convenio *"
    E o cursor volta ao campo do convênio
    E nada é gravado

  Cenário: Convênio não cadastrado no ano informado
    Dado que informei um convênio que não existe naquele ano
    Quando respondo a tela
    Então vejo "* Convenio nao cadastrado *"
    E o cursor volta ao campo do convênio
    E nada é gravado

  Cenário: Convênio sem instituição no meu grupo
    Dado que informei um convênio que existe, mas nenhuma instituição dele está no grupo informado
    Quando respondo a tela
    Então vejo "* Convenio nao cadastrado *"
    E nada é gravado

  Cenário: Instituição beneficente de outra secretaria
    Dado que a instituição vinculada ao convênio pertence a outra secretaria
    Quando respondo a tela
    Então vejo "* Inst.benef nao pertence a esta secretaria *"
    E nada é gravado

  Cenário: Instituição beneficente de outro grupo
    Dado que a instituição vinculada ao convênio é de outro grupo que não o meu
    Quando respondo a tela
    Então vejo "* Usuario sem acesso a outro grupo *"
    E nada é gravado

  Cenário: Modelo de nota fiscal não cadastrado
    Dado que o modelo de nota fiscal que a tela assume não está cadastrado
    Quando respondo a tela
    Então vejo "* Modelo de nota fiscal nao cadastrado *"
    E nada é gravado

  Cenário: Fornecedor não cadastrado
    Dado que informei um CNPJ / CPF de fornecedor que não está cadastrado
    Quando respondo a tela
    Então vejo "* Fornecedor nao cadastrado *"
    E o cursor volta ao campo do fornecedor
    E nada é gravado

  Cenário: Nota já cadastrada
    Dado que já existe uma nota com a mesma secretaria, fornecedor, ano de entrega e número, no meu grupo
    Quando respondo a tela
    Então vejo "* Nota ja cadastrada *"
    E o cursor volta ao campo do número da nota
    E nada é gravado

  Cenário: Nota já cadastrada em outro grupo
    Dado que já existe uma nota com a mesma secretaria, fornecedor, ano de entrega e número, em outro grupo
    Quando respondo a tela
    Então vejo "* Usuario sem acesso ao grupo desta nota *"
    E nada é gravado

  Cenário: Valor total da nota não informado
    Dado que deixei o valor total da nota em branco
    Quando respondo a tela
    Então vejo "* Informe o valor total da nota *"
    E o cursor volta ao campo do valor
    E nada é gravado

  Cenário: Recursos próprios iguais ou maiores que o valor da nota
    Dado que informei recursos próprios iguais ou maiores que o valor total da nota
    Quando respondo a tela
    Então vejo "* Rec.proprios deve ser < valor da nota *"
    E o cursor volta ao campo dos recursos próprios
    E nada é gravado

  Cenário: A tela não grava nada por si
    Dado que percorri a tela com dados válidos e confirmei a inclusão
    Quando a tela encaminha a nota ao lançamento dos gêneros
    Então nenhum cadastro foi gravado, alterado ou apagado por esta tela
    E nenhuma trilha de auditoria foi gerada por esta tela
    E a nota só existe depois de gravada no lançamento dos gêneros

  Cenário: Campo de número recusado na edição
    Dado que informei letras em um dos campos de número da tela
    Quando respondo a tela
    Então a edição recusa aquele campo
    E o cursor volta ao primeiro campo recusado
    E a tela não segue

  Cenário: Voltando do lançamento dos gêneros, o menu aponta a opção desta tela
    Dado que a sessão volta do fluxo da nota fiscal
    Quando chego ao menu de despesas F100M
    Então vejo o aviso "* Acesso deve ser feito pela tela F150T *"
    E a opção que abre a F150T já vem marcada
    E respondendo o menu sou levado à F150T

  Cenário: A tela não consta do cadastro de telas
    Dado que a tela F150T não consta do cadastro de telas, ou está desativada
    Quando abro a tela F150T
    Então sou avisado de que a tela não está disponível
    E nada é mostrado

  Cenário: Meu código de acesso não tem a tela
    Dado que o meu código de acesso não tem a tela F150T liberada
    Quando abro a tela F150T
    Então sou avisado de que o acesso à tela foi negado
    E nada é mostrado
```
