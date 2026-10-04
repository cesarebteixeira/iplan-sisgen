# US — C692C — Consultar os valores do contrato e das permissões da coordenação regional escolar

## Estória

Como **servidor da coordenação regional escolar (CRE)**, quero **consultar, contrato
a contrato, o valor contratado e os seus aditivos ao lado do total já lançado nas
permissões daquela coordenação**, para que **eu saiba quanto do contrato já está
comprometido e quanto ainda resta, antes de autorizar qualquer gasto**.

O mesmo contrato vive em dois lugares: no registro do contrato no FINCON, com o
valor contratado e os aditivos, e nas permissões lançadas contra ele, cada uma com
os seus valores. Enquanto os dois lados não fecham, ninguém sabe quanto do contrato
já foi usado — e é essa diferença que a tela põe na frente de quem opera. A tela é
só de leitura: nenhum contrato, permissão ou fornecedor é incluído, alterado ou
apagado por aqui.

## Contexto

Jornada S000M → C000M → C050M → C690M → C692C.

Ator: servidor de CRE — consulta, contrato a contrato, os valores registrados no
FINCON e o quanto já foi comprometido nas permissões da sua coordenação regional
escolar.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

A C692C trata **um contrato por vez**, e a resposta fica nela mesma: é a própria
tela que ela reabre depois de cada consulta, e não há tela seguinte para onde a
resposta seja entregue. Quem a abre é uma opção do menu C690M, e esse menu não leva
registro nem operação junto — o contrato a consultar é o que se digita na própria
C692C. O C000M, o C050M e o C690M são menus: não leem cadastro de negócio e não
deixam dado de negócio para a C692C; a coordenação regional escolar e o tipo de
órgão com que a tela situa o contrato são os que a sessão já trazia (ver a dúvida
em RN-04).

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela identifica o contrato pela coordenação, pelo número e pelo ano

A tela tem **onze campos digitáveis**, todos numéricos: a **coordenação regional
escolar** (2 dígitos), o **número do contrato** (6), o **tipo de contrato** (3), o
**ano do contrato** (4), o **dia**, o **mês** e o **ano do início do período**, o
**dia**, o **mês** e o **ano limite** e o **código do fornecedor** (4).

O contrato é procurado por **três** desses campos — a coordenação regional escolar,
o número do contrato e o ano do contrato — mais o **tipo de órgão da sessão**. Os
outros oito não escolhem contrato nenhum (RN-02). O cadastro dos contratos comporta
**10.000** contratos: capacidade, o máximo esperado no dimensionamento, não o
volume de contratos existentes.

[?] O texto da máscara não veio no lote: o que a tela escreve ao lado de cada campo
é pergunta ao site. Os nomes usados nesta estória são os rótulos de negócio que o
próprio sistema carrega ao conferir cada campo; os dois totais de que a RN-08 fala
foram nomeados pelo significado dos valores somados.

### RN-02 — Tipo de contrato, períodos e fornecedor são digitáveis, mas quem manda é o contrato

O tipo de contrato, as seis partes das duas datas do período e o código do
fornecedor também são digitados e também passam pela conferência numérica — mas a
tela não os usa para procurar nada: achado o contrato, ela **substitui** os oito
pelo que está gravado no próprio contrato. Informar um tipo de contrato, um período
ou um fornecedor diferente do cadastrado não muda a consulta: o que aparece é o do
contrato.

[?] Se a máscara deixa o operador digitar esses campos, a tela ignora o que ele
digita; se ela os marca apenas para exibição, a conferência numérica deles é
trabalho perdido. Qual dos dois, pergunta ao site.

### RN-03 — A tela é só de consulta

Ao abrir, a tela assume a **consulta**, e é esse valor que aparece no campo da
opção. Qualquer outra opção é recusada com **\* Opcao nao disponivel. Use CON \***,
com o cursor de volta ao campo da opção, e nada é conferido nem mostrado.

[?] A mensagem nomeia a opção pela abreviatura **CON**, enquanto a conferência
compara o informado com a sigla de consulta que o sistema carrega da biblioteca de
mensagens do idioma — biblioteca que não veio no lote. Se a sigla que o sistema
carrega não for **CON**, a mensagem pede um valor que a própria conferência recusa,
e nenhuma consulta é feita nesta tela. Pergunta ao site.

### RN-04 — Quem tem coordenação na sessão não consulta contrato de outra

Se a sessão traz uma **coordenação regional escolar**, a informada tem de ser
exatamente essa; sendo outra, a recusa é **\* Usuario sem acesso a este grupo \***,
com o cursor de volta ao campo da coordenação, e nada é consultado. Se a sessão
**não** traz coordenação, a tela não faz essa conferência e aceita qualquer uma.

[?] De onde vem a coordenação regional escolar que a tela usa é pergunta ao site:
nenhum programa desta jornada a preenche — a entrada guarda o vínculo do usuário com
a secretaria em outra área —, e o material lido não mostra a passagem de uma área
para a outra. Se ela chegar zerada, a conferência nunca recusa e o servidor consulta
contrato de qualquer coordenação; se chegar com a coordenação de outro contexto, ela
recusa quem tem direito. Pergunta ao site.

### RN-05 — Sem número e sem ano do contrato, a tela não consulta

O número do contrato e o ano do contrato são os dois obrigatórios, juntos: faltando
qualquer um dos dois, a recusa é **\* Informe o Contrato FINCON \***, com o cursor
no campo do número, e nenhum valor é mostrado.

### RN-06 — O contrato tem de estar registrado no FINCON

Procurado o contrato pelo tipo de órgão da sessão, pela coordenação regional
escolar, pelo número e pelo ano, se ele não estiver registrado no FINCON a recusa é
**\* Contrato FINCON nao cadastrado \***, com o cursor no campo do número, e nenhum
valor é mostrado. Contrato de outro tipo de órgão não é encontrado.

### RN-07 — O contrato tem de ter permissão lançada, e as permissões excluídas não contam

Achado o contrato, a tela procura as **permissões** lançadas contra ele — mesmo tipo
de órgão, mesmo período limite, mesma coordenação, mesmo fornecedor e mesmo tipo de
contrato. Não achando nenhuma, a recusa é **\* Permissao nao cadastrada \***, com o
cursor no campo da coordenação regional escolar, e nenhum valor é mostrado.

Só entram nessa procura as permissões **vigentes**: as marcadas como excluídas e as
que estão sem a classificação preenchida ficam de fora. Uma permissão nesse estado
não conta como permissão lançada nem entra em nenhuma soma.

[?] A tela procura a permissão sem informar a classificação — o material lido deixa
a classificação em branco na busca —, mas o conjunto de permissões que ela varre
exclui justamente as que estão sem classificação. Se a busca exigir a classificação,
nenhuma permissão é achada e a tela recusa toda consulta com "permissão não
cadastrada"; se o campo em branco valer como "qualquer classificação", a busca é a
que se descreveu. Qual dos dois, o material lido não explica: pergunta ao site.

### RN-08 — As permissões são somadas em dois totais

Para cada permissão encontrada a tela acumula **dois totais**: o **total dos valores
iniciais** — um valor de cada permissão — e o **total dos acréscimos**, formado por
**três** valores de cada permissão. Os dois totais começam zerados a cada consulta.

[?] A tela percorre as permissões uma a uma até a leitura deixar de devolver
registro do mesmo contrato; o que faz a leitura avançar de uma permissão para a
seguinte é do dialeto e não está explicado no material lido. Se a leitura repetir o
mesmo registro, a soma não termina; se ela pular registros, o total fica menor que o
devido. As duas hipóteses mudam o que a tela mostra. Pergunta ao site.

### RN-09 — A tela mostra os valores dos dois lados e a diferença entre eles

Terminada a soma, a tela mostra **seis valores**: o **valor contratado** registrado
no FINCON, o **total dos valores iniciais** das permissões e a **diferença** entre
os dois; e, para os aditivos, o **valor dos aditivos** do contrato, o **total dos
acréscimos** das permissões e a **diferença** entre os dois. A diferença é sempre o
valor do contrato **menos** o total das permissões.

[?] A tela guarda ainda **dois** valores que nunca calcula nem mostra: dois campos
que ela zera ao abrir e não volta a tocar. Ou ficaram de fora da exibição, ou são
resto de uma versão anterior. Pergunta ao site.

### RN-10 — O fornecedor, o tipo de órgão e a data do sistema

O cabeçalho traz a **descrição do tipo de órgão** e a **data do sistema** que a
sessão carrega, e a tela mostra a **razão social do fornecedor** gravada no
contrato, buscada pelo código de fornecedor que o contrato traz. Fornecedor não
cadastrado não gera recusa nem mensagem: a razão social fica em branco.

[?] De onde vêm a descrição do tipo de órgão e a data do sistema que o cabeçalho
mostra é pergunta ao site: nenhum programa desta jornada as calcula, e o material
lido só as mostra sendo apagadas. Se elas não chegarem, o cabeçalho abre sem
descrição e sem data. Pergunta ao site.

[?] A tela chega a ler o cadastro dos tipos de órgão para descobrir a descrição, mas
guarda o resultado numa área de trabalho que **não** é a que aparece — e essa mesma
área é a que as telas anteriores devolvem à sessão, de modo que um resto deixado
pelo menu pode fazer a tela pular a leitura. Ou a leitura é resto da geração, ou a
tela deveria mostrar o que leu. Pergunta ao site.

### RN-11 — A data de atualização do contrato, quando existe

Quando o contrato tem **data de atualização**, a tela escreve, junto aos valores,
**Dados Atualizados** e **em** seguido da data. Quando essa data está zerada, a
legenda não aparece.

### RN-12 — Campo que não for número é recusado antes da consulta

Os onze campos digitáveis passam pela conferência numérica do sistema antes de
qualquer leitura: o campo que não for número é recusado, com o erro marcado. O
cursor só tem posição definida para **três** deles — a coordenação regional escolar,
o número e o ano do contrato; nos demais a tela não reposiciona o cursor.

[?] A mensagem que o operador lê nesse caso é da rotina de conferência do ambiente,
que não veio no lote, e o material lido também não permite concluir se a consulta
chega a acontecer depois de um campo recusado: o programa apenas testa o
sinalizador de interrupção, e quem o marca é essa mesma rotina. Pergunta ao site.

### RN-13 — A consulta não grava nada

Esta tela não grava. Ela enxerga **cinco cadastros** — o dos contratos, o das
permissões, o dos fornecedores, o dos tipos de órgão e o das telas — e, desses
cinco, só **lê**: nenhum contrato, permissão, fornecedor ou tipo de órgão é
incluído, alterado ou apagado, e nenhuma trilha de auditoria é gerada. Quem lança e
corrige o contrato são outras telas do sistema: o que esta mostra é o retrato do que
já estava gravado.

### RN-14 — A tela não muda conforme quem a chamou, e a resposta volta para ela mesma

A tela abre com o mesmo comportamento, venha de onde vier: ela não compara a tela de
origem com código de tela nenhum, e nenhum programa do sistema informa a tela de
origem para ela. Terminada a consulta, a resposta volta para a própria C692C — é ela
que a tela reabre, e não uma tela seguinte. A camada comum do sistema devolve a
transação à tela de origem quando a origem vem informada; de onde essa informação
viria, quando vem, é pergunta ao site.

[?] De onde vem a tela de origem que a C692C publica para a camada comum é pergunta
ao site: nenhum programa do lote a informa para esta tela, e o menu que a abre
também não. Se a camada comum a receber preenchida, a transação volta para a tela de
origem em vez de ser tratada na C692C — e nenhuma consulta acontece. Pergunta ao
site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar os valores do contrato e das permissões da coordenação regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega a coordenação regional escolar e o tipo de órgão
    E tenho acesso à tela C692C

  Cenário: Abrir a tela não consulta contrato nenhum
    Dado que cheguei à tela C692C
    Quando a tela abre
    Então ela aparece na opção de consulta
    E o campo da coordenação regional escolar vem preenchido com o da minha sessão
    E nenhum valor de contrato é mostrado
    E nada é gravado

  Cenário: Consultar um contrato que tem permissões lançadas
    Dado que o contrato está registrado no FINCON para a minha coordenação regional escolar
    E que há permissões lançadas contra esse contrato
    Quando informo o número e o ano do contrato e confirmo
    Então vejo o valor contratado e o valor dos aditivos registrados no contrato
    E vejo o total dos valores iniciais das permissões e o total dos seus acréscimos
    E vejo a diferença entre o valor do contrato e o total das permissões, nos dois casos
    E vejo a razão social do fornecedor do contrato
    E nada é gravado

  Cenário: Os totais são a soma de todas as permissões do contrato
    Dado que há mais de uma permissão lançada contra o contrato
    Quando consulto o contrato
    Então o total dos valores iniciais é a soma dos valores iniciais de todas elas
    E o total dos acréscimos é a soma dos acréscimos de todas elas

  Cenário: Permissão excluída ou sem classificação fica fora da soma
    Dado que o contrato tem uma permissão marcada como excluída
    E uma permissão sem a classificação preenchida
    Quando consulto o contrato
    Então nenhuma das duas entra nos totais
    E nenhuma das duas conta como permissão lançada

  Cenário: Tipo de contrato, período e fornecedor digitados não mudam a consulta
    Dado que o contrato está registrado no FINCON
    Quando informo, além do número e do ano, um tipo de contrato, um período e um fornecedor diferentes dos do contrato
    Então a tela mostra os dados do contrato, e não os que digitei

  Cenário: Opção de manutenção diferente de consulta
    Quando informo, no campo da opção, algo que não é a consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use CON *"
    E o cursor volta ao campo da opção
    E nada é consultado

  Cenário: Consultar contrato de outra coordenação
    Dado que a minha sessão carrega uma coordenação regional escolar
    Quando informo a coordenação de outra e confirmo
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"
    E o cursor volta ao campo da coordenação regional escolar
    E nenhum valor é mostrado

  Cenário: Sem coordenação na sessão, qualquer coordenação pode ser consultada
    Dado que a minha sessão não carrega coordenação regional escolar
    Quando informo a coordenação de um contrato que existe e confirmo
    Então a consulta é feita normalmente
    E nada é gravado

  Cenário: Falta o número ou o ano do contrato
    Quando deixo o número do contrato em branco, ou o ano, e confirmo
    Então vejo a mensagem "* Informe o Contrato FINCON *"
    E o cursor volta ao campo do número do contrato
    E nenhum valor é mostrado

  Cenário: Contrato não registrado no FINCON
    Dado que não existe contrato com o tipo de órgão, a coordenação, o número e o ano informados
    Quando confirmo
    Então vejo a mensagem "* Contrato FINCON nao cadastrado *"
    E o cursor volta ao campo do número do contrato
    E nenhum valor é mostrado

  Cenário: Contrato sem permissão lançada
    Dado que o contrato está registrado no FINCON
    E que não há permissão vigente lançada contra ele
    Quando confirmo
    Então vejo a mensagem "* Permissao nao cadastrada *"
    E o cursor volta ao campo da coordenação regional escolar
    E nenhum valor é mostrado

  Cenário: Contrato sem data de atualização
    Dado que o contrato está registrado e tem permissões lançadas
    E que ele não tem data de atualização
    Quando consulto o contrato
    Então os valores são mostrados
    E a legenda de data de atualização não aparece

  Cenário: Fornecedor do contrato não cadastrado
    Dado que o contrato está registrado e tem permissões lançadas
    E que o código de fornecedor do contrato não está no cadastro de fornecedores
    Quando consulto o contrato
    Então os valores são mostrados
    E a razão social do fornecedor aparece em branco
    E nenhuma mensagem de recusa é mostrada

  Cenário: Campo numérico com valor que não é número
    Quando informo letras no campo da coordenação regional escolar e confirmo
    Então a tela marca o erro naquele campo
    E o cursor volta ao campo da coordenação regional escolar

  Cenário: A resposta volta para a própria tela C692C
    Dado que consultei um contrato com permissões lançadas
    Quando a resposta volta
    Então ela aparece na própria tela C692C
    E não sou levado a outra tela

  Cenário: A consulta não grava nada
    Dado que consultei um contrato com permissões lançadas
    Quando a resposta volta
    Então o contrato, as permissões, o fornecedor e o tipo de órgão continuam como estavam
    E nenhuma trilha de auditoria é gerada
```
