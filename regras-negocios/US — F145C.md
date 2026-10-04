# US — F145C — Consulta de fornecedores e totais por coordenação

## Estória

Como **servidor da CRE**, quero **consultar, por grupo, ano de competência e
instituição beneficente, os fornecedores conveniados e os totais de empenho,
repasse, despesa e item de cada um**, para que eu confira, sem abrir processo,
se os valores que a entidade apresenta fecham com o que a secretaria tem
registrado.

Esta consulta é o primeiro filtro do acompanhamento da prestação de contas: é
por ela que se enxerga o conjunto de fornecedores de um grupo antes de descer ao
detalhe de cada nota fiscal. Sem ela, a conferência só existiria no papel, e uma
divergência entre o valor da nota e a soma das parcelas — que é o que denuncia
um repasse ou uma despesa lançados a menor — passaria despercebida.

## Contexto

Jornada S000M → F000M → F100M → F145C.

Ator: servidor de CRE — consulta os fornecedores e os totais de um grupo de
coordenação, por ano de competência e instituição beneficente.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e
menus.md`: é **dado de navegação**, não regra de negócio.

A tela desta jornada não é uma folha solta: ela é o último passo de uma cadeia
em que cada tela entrega a seguinte sem passar por menu. O menu de notas fiscais
encaminha para ela, e ela encaminha para a tela de notas fiscais por
fornecedor. Por isso o filtro que o servidor informa aqui — grupo, ano de
competência e instituição beneficente — é o que determina o que ele vai ver na
tela seguinte.

As regras abaixo são só as da **tela desta jornada**.

---

## Regras de negócio

### RN-01 — A tela mostra a coordenação, o filtro e até 12 fornecedores com seus totais

A tela se identifica como COORD.REG.ESCOLA e abre mostrando o filtro que a
alimenta — a coordenação regional (o grupo), o ano de competência e a
instituição beneficente — e mais três rótulos de situação: a data do sistema, a
instituição beneficente consultada e a data do último processamento. Abaixo,
lista até **12 fornecedores** por vez. De cada fornecedor a tela mostra o
número do CNPJ, a razão social e **quatro valores**: o total da nota fiscal, o
total do repasse, o total da despesa e o total do item.

A lista sai do cadastro dos acumulados do convênio por fornecedor, que é
chaveado exatamente pela combinação consultada — tipo de órgão, coordenação
regional, instituição beneficente, ano de competência e CNPJ do fornecedor —, de
modo que os fornecedores de um grupo saem agrupados e na ordem do CNPJ.

### RN-02 — Para consultar é preciso informar o grupo e o ano de competência

A consulta não abre sem o grupo e sem o ano de competência. Faltando o grupo, o
sistema recusa e pede que ele seja informado, devolvendo o cursor para esse
campo. Faltando o ano de competência, a recusa é a mesma e o cursor vai para o
ano.

O grupo não é digitado à toa: ele é conferido contra a coordenação a que o
usuário tem acesso, e essa conferência é a regra seguinte. A instituição
beneficente é o terceiro elemento do filtro, mas não é exigida para a tela
abrir; sem ela o sistema mostra os fornecedores de todos os grupos de
instituições do ano informado.

### RN-03 — O usuário só vê o grupo a que tem acesso

Informado o grupo, o sistema confere se ele é o mesmo grupo do usuário. Sendo
diferente, a consulta é recusada com o aviso de que o usuário não tem acesso a
outro grupo, e o cursor volta para o campo do grupo. Se o usuário não tem grupo
próprio atribuído, a conferência não é feita e qualquer grupo é aceito — a
restrição depende de o perfil trazer o grupo.

### RN-04 — A instituição beneficente informada precisa estar cadastrada

A instituição beneficente informada é procurada no cadastro de instituições pelo
código INEP. Não existindo, a consulta é recusada com a mensagem de que a
instituição beneficente não está cadastrada, e o cursor fica no campo do código
INEP.

### RN-05 — Cada fornecedor da lista precisa existir no cadastro de fornecedores

Para cada fornecedor que a lista traz, o sistema procura o CNPJ no cadastro de
fornecedores para obter a razão social. Não encontrando, a consulta é recusada
com a mensagem de fornecedor não cadastrado, e a tela não apresenta a lista.

### RN-06 — O sinal ao lado dos valores denuncia a divergência

A tela fecha a conta de cada fornecedor: soma o total do repasse com o total do
item e subtrai o total da despesa. Se o resultado for igual ao total da nota
fiscal, o fornecedor aparece sem marca. Se for diferente, o sistema marca o
fornecedor com um asterisco, que é o sinal de que os valores não fecham. O
asterisco não bloqueia nada: é indicação para quem confere.

### RN-07 — Grupo sem fornecedores com totais é avisado, sem lista

Quando a consulta não encontra nenhum total para o grupo, o ano e a instituição
informados, o sistema avisa que os totais não estão cadastrados e não apresenta
lista.

### RN-08 — Linha apontada sem CNPJ é recusada

A tela trabalha com uma marca de linha preenchida, linha a linha. Se a linha
apontada estiver marcada como preenchida e o CNPJ do fornecedor estiver zerado,
o sistema recusa com o aviso de linha não preenchida e o cursor vai para o
campo do CNPJ daquela linha, na coluna do CNPJ.

### RN-09 — Confirmar um fornecedor entrega o filtro à tela seguinte, que abre em consulta

Confirmada a linha de um fornecedor que tenha CNPJ preenchido, a tela entrega
esse fornecedor e o filtro à tela seguinte: vai o CNPJ do fornecedor, a
coordenação regional, o ano de competência, a instituição beneficente, o código
do órgão e o tipo de órgão, e a operação vai como **consulta**. A tela seguinte
abre, portanto, já filtrada por aquele fornecedor, e não há menu entre as duas.
É por essa passagem que a tela desta jornada alcança as telas de nota fiscal.

### RN-10 — A consulta não grava nada

A tela é de consulta: ela lê os cadastros e apresenta. Não há inclusão,
alteração nem exclusão, e não há registro de auditoria gerado por ela. O que
existe no programa são as rotinas de gravação e exclusão dos cadastros que ele
enxerga, declaradas de forma genérica e nunca executadas pela tela.

### RN-11 — Em uso normal só há consulta disponível

A tela admite uma única operação: a consulta. Chegando uma operação diferente na
primeira linha, o sistema recusa e diz que a opção não está disponível, devendo
ser usada a consulta, e o cursor vai para o campo da operação.

[?] A tela sempre se apresenta em consulta — ela mesma fixa a operação como
consulta antes de exibir —, e a máscara não oferece campo de operação para o
usuário digitar outra coisa. Se o usuário pode ver essa recusa por algum
caminho, ou se ela é só uma guarda de proteção, é pergunta ao site.

### RN-12 — A marca de "linha preenchida" e a conferência de três campos não fecham com os dados da tela

Duas guardas da tela comparam valores que a própria tela nunca põe ali: uma
delas exige que o grupo da linha, o ano de competência da linha e a instituição
beneficente da linha sejam iguais aos do filtro informado, e a outra exige que
o grupo da linha seja igual ao número da nota fiscal. Nenhum desses campos é
carregado com o valor contra o qual são comparados, de modo que as duas
comparações passam sempre, sem conferir nada.

[?] A conferência que compara o grupo da linha com o número da nota fiscal lê um
campo que a tela nunca preenche, de modo que a comparação é sempre verdadeira e
a regra não distingue grupo nenhum. Se a intenção era conferir o grupo do
fornecedor, o campo comparado está errado; se era outra conferência, ela não
existe. Pergunta ao site.

[?] Não está no acervo desta jornada o que faz a marca de "linha preenchida"
valer "X" para uma linha da lista; a tela apenas a testa e a limpa. Sem saber
quem a preenche, não se sabe se a recusa de linha não preenchida é alcançável
pelo usuário. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Consultar fornecedores e totais por coordenação regional

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F145C

  Cenário: Consulta de um grupo e ano de competência com fornecedores cadastrados
    Dado que informo a coordenação regional, o ano de competência e a instituição beneficente
    Quando a tela abre
    Então vejo a lista dos fornecedores daquele grupo, com CNPJ, razão social e os totais de nota, repasse, despesa e item
    E vejo até 12 fornecedores por vez
    E a data do sistema e a data do último processamento aparecem no alto da tela

  Cenário: Fornecedores com valores que não fecham
    Dado que a soma do repasse com o item, menos a despesa, é diferente do total da nota de um fornecedor
    Quando a lista é apresentada
    Então aquele fornecedor aparece marcado com um asterisco
    E os demais aparecem sem marca

  Cenário: Grupo sem fornecedores com totais cadastrados
    Dado que não há nenhum total cadastrado para o grupo, o ano e a instituição informados
    Quando peço a consulta
    Então vejo a mensagem "* Totais nao cadastrados *"
    E nenhuma lista é apresentada

  Cenário: Importância do grupo para a consulta
    Dado que deixo o campo da coordenação regional em branco
    Quando confirmo a consulta
    Então vejo a mensagem "* Informe o grupo *"
    E o cursor volta para o campo da coordenação regional

  Cenário: Ano de competência não informado
    Dado que informo a coordenação regional mas deixo o ano de competência em branco
    Quando confirmo a consulta
    Então vejo a mensagem "* Informe o ano de competencia *"
    E o cursor volta para o campo do ano de competência

  Cenário: Consulta sem instituição beneficente
    Dado que informo a coordenação regional e o ano de competência, e deixo a instituição beneficente em branco
    Quando confirmo a consulta
    Então vejo os fornecedores daquele grupo e daquele ano, de todas as instituições
    E o sinal de divergência continua aparecendo em quem não fecha

  Cenário: Consulta de grupo ao qual não tenho acesso
    Dado que o meu perfil tem uma coordenação regional atribuída
    Quando informo a coordenação regional de outro grupo
    Então vejo a mensagem "* Usuario sem acesso a outro grupo *"
    E o cursor volta para o campo da coordenação regional

  Cenário: Instituição beneficente não cadastrada
    Dado que informo um código de instituição beneficente que não existe
    Quando confirmo a consulta
    Então vejo a mensagem "* Instituicao beneficente nao cadastrada *"
    E o cursor volta para o campo do código INEP

  Cenário: Fornecedor da lista que não existe no cadastro
    Dado que a lista traz um CNPJ de fornecedor que não está no cadastro de fornecedores
    Quando a lista é montada
    Então vejo a mensagem "* Fornecedor nao cadastrado *"
    E a lista não é apresentada

  Cenário: Linha apontada sem CNPJ
    Dado que confirmo uma linha marcada como preenchida e sem o CNPJ do fornecedor
    Quando a tela processa a linha
    Então vejo a mensagem "* Linha nao preenchida *"
    E o cursor vai para o campo do CNPJ daquela linha

  Cenário: De um fornecedor da lista para as notas fiscais dele
    Dado que vejo a lista de fornecedores de um grupo
    Quando confirmo a linha de um fornecedor que tem CNPJ preenchido
    Então o sistema abre a tela de notas fiscais por fornecedor já filtrada por aquele CNPJ
    E leva junto a coordenação regional, o ano de competência e a instituição beneficente
    E essa tela abre em consulta

  Cenário: Operação diferente de consulta é recusada
    Dado que a tela recebe uma operação diferente de consulta
    Quando a tela processa a primeira linha
    Então vejo a mensagem "* Opcao nao disponivel. Use CON *"
    E o cursor vai para o campo da operação

  Cenário: A consulta não grava nada
    Dado que consultei os fornecedores de um grupo
    Quando a tela termina de apresentar a lista
    Então nenhum fornecedor, instituição ou total foi incluído, alterado ou excluído
    E nenhum registro de auditoria foi gerado
```
