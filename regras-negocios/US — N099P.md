# US — N099P — Solicitar o processamento dos relatórios fiscais

## Estória

Como **servidor de CRE que responde pelos relatórios fiscais**, quero **completar
os parâmetros do relatório que escolhi e pedir que ele seja processado**, para que
**o relatório saia na impressora certa, com o meu grupo e o período de que eu
preciso, sem eu ter de repetir o que já informei no menu anterior**.

O relatório não é montado enquanto o servidor digita: ele roda no processamento,
depois. Esta é a tela em que a solicitação é montada — ela recebe do menu de
relatórios **qual** relatório foi escolhido e **em que impressora**, pergunta
apenas os parâmetros daquele relatório e registra a solicitação, que o
processamento vai buscar. Sem esse registro o relatório não é produzido; e pedir
duas vezes o mesmo relatório para o mesmo grupo só ocuparia a fila, por isso o
pedido repetido é recusado enquanto o primeiro não sai dela.

## Contexto

Jornada S000M → N000M → N010M → N099P.
Ator: servidor de CRE — escolhe o relatório e a impressora no menu de relatórios e,
na N099P, completa os parâmetros daquele relatório e confirma o pedido.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O que a jornada deixa pronto para esta tela: a entrada define o servidor (a
matrícula, o tipo de órgão, o grupo do vínculo e o órgão); o `N000M` é o menu do
módulo de notas fiscais e leva ao menu de relatórios; e o menu de relatórios
entrega o **relatório escolhido** e a **impressora**, que ele já guardou como
preferência do servidor. A mesma N099P atende a **33 relatórios** diferentes — o
menu desta jornada sozinho oferece **9** deles —, e é isso que explica a forma
desta tela: ela é uma só tela, com todas as posições de parâmetro possíveis, e o
relatório escolhido decide quais delas valem.

As regras abaixo são só as da tela desta jornada.

## Regras de negócio

### RN-01 — O relatório e a impressora já vêm escolhidos

Esta tela não pergunta qual relatório emitir nem em que impressora: as duas
decisões vêm do menu de relatórios. Sem impressora informada naquele menu o pedido
nem chega aqui — o menu avisa que a impressora é obrigatória. A impressora
informada ali fica guardada no cadastro do servidor, para ser sugerida nas próximas
vezes, e é ela que segue na solicitação, ao lado da estação de onde o pedido saiu e
da matrícula de quem pediu. Quando o relatório não pede a quantidade de vias, sai
uma.

### RN-02 — A tela só pede os parâmetros do relatório escolhido

A mesma tela serve a 33 relatórios. Ao abrir, ela deixa em uso apenas as posições
de que o relatório escolhido precisa, assinala cada uma com um asterisco e deixa o
cursor na primeira delas; as demais ficam fora de uso e em branco.

Nos **nove** relatórios a que esta jornada chega, o que se pede varia entre: o
**número do processo** (a secretaria, o grupo, o lote e os dígitos finais) com o
**grupo**; o **fornecedor**, o **período** (data inicial e data limite) e a **forma
de impressão**; o **fornecedor**, o **período**, o **grupo**, o **tipo de
contrato** e a **subclasse com o gênero**; o **período** com o **grupo**, a
**subclasse e o gênero**; o **período** com o **grupo** e o **órgão**; o
**período** com o **grupo**, o **órgão** e o **tipo de nota**; o **período** com o
**grupo**, o **fornecedor**, o **tipo de contrato**, a **subclasse e o gênero** e o
**tipo de nota**; e o **período** com a **subclasse**, o **gênero**, a
**quantidade de vias** e o **tipo de nota**. Há ainda relatórios, fora desta
jornada, que exigem o **nome do destinatário** e o **local de entrega do
relatório**.

[?] O que o asterisco faz na tela — se apenas aponta a posição, se a exige ou se a
impede de ser digitada — não está no acervo. Pergunta ao site.

[?] Os relatórios não têm nome de negócio no acervo: o que existe é o código de
cada um no menu, sem título (o título mora no desenho da tela, que não veio no
lote). E o mapa de opções do menu de relatórios desta jornada não foi extraído, de
modo que **não se decide pelo acervo qual dos nove relatórios esta jornada pede**.
Por isso esta estória fala dos relatórios pelos parâmetros que eles pedem. Pergunta
ao site.

### RN-03 — Abrir a tela não grava nada

A primeira passagem da tela serve só para apresentá-la: ela lê o cadastro de telas,
passa pelas conferências de segurança, lê o cadastro do tipo de órgão, liga as
posições do relatório escolhido, preenche o que a sessão já sabe e termina — sem
conferir parâmetro nenhum e sem gravar. Só a confirmação do servidor percorre o
caminho que registra a solicitação.

### RN-04 — Não se pede duas vezes o mesmo relatório para o mesmo grupo

Antes de registrar, a tela procura na fila de solicitações uma solicitação **do
mesmo relatório, para o mesmo tipo de órgão e para o mesmo grupo**. Havendo, recusa
com **\* Relatorio em processamento. Aguarde. \***, devolve o cursor ao campo do
grupo e abandona: nenhuma solicitação nova é registrada e nenhum processamento é
disparado. Nos relatórios que não perguntam o grupo, a procura é feita com o grupo
que o próprio relatório fixa — zerado em dois deles, e 01 no relatório por período
—, de modo que uma única solicitação daquele relatório já barra as demais.

A solicitação que a própria tela acabou de registrar é a que satisfaz essa procura:
é assim que o mesmo relatório fica bloqueado para o mesmo grupo enquanto não sai da
fila. A fila tem capacidade declarada de **90 mil solicitações** — é o máximo
esperado, parâmetro de dimensionamento, e não o volume de solicitações existentes,
que o acervo não informa.

[?] A procura não olha a situação da solicitação, e a recusa fala de "em
processamento". Ou quem processa apaga a solicitação quando termina — e a recusa
vale só enquanto há pedido pendente —, ou a segunda emissão do mesmo relatório para
o mesmo grupo nunca passa. A entrada limpa as solicitações vencidas ao abrir a
sessão, mas o prazo dessa limpeza é regra da entrada, não desta tela. Pergunta ao
site; não concluo qual dos dois.

### RN-05 — O grupo é o limite de alcance do servidor

O grupo do vínculo do servidor limita o que ele pode pedir:

- o **grupo é obrigatório**; em branco, a recusa é **\* Informe o grupo \*** (nos
  relatórios cujo grupo admite o valor que significa "todos", a recusa indica esse
  valor: **\* Informe o grupo.  Todos = 99 \***);
- o grupo informado tem de ser o do servidor; sendo outro, a recusa é
  **\* Usuario sem acesso a este grupo \*** (em alguns relatórios, **\* Usuario sem
  acesso a outro grupo \***);
- quem **tem** grupo na sessão **não** pode pedir o valor que significa "todos": a
  recusa é **\* Usuario sem acesso a 99 \***. O "todos" fica reservado a quem não
  tem grupo no vínculo.

[?] Quem **não** tem grupo na sessão nunca é recusado por grupo: a conferência do
acesso é simplesmente pulada, e qualquer grupo informado passa. Ou esses servidores
são de fora da estrutura de grupos — e o alcance deles é decidido em outro lugar —,
ou a conferência está incompleta. Pergunta ao site.

### RN-06 — Os parâmetros de cadastro têm de existir

Cada relatório confere, no cadastro, os parâmetros que pede. Não estando lá, a tela
recusa, devolve o cursor ao campo e nada é registrado. As recusas desta família
são: **\* Fornecedor nao cadastrado \***, **\* Tipo de contrato nao cadastrado \***,
**\* Genero nao cadastrado \***, **\* Orgao nao cadastrado \***,
**\* Permissao nao cadastrada \***, **\* Grupo nao cadastrado \***,
**\* Operador logistico nao cadastrado \***, **\* Grupamento nao cadastrado \*** e
**\* Secretaria nao cadastrada \***. O gênero, a permissão e as notas fiscais são
conferidos sobre conjuntos que já deixam os registros excluídos de fora; os demais
cadastros são aceitos existindo, sem conferência de exclusão.

Há ainda os parâmetros que também dependem de um dado que existe no banco e não é
digitado: o **processo** tem de ter pelo menos uma nota fiscal não excluída
(**\* Processo nao cadastrado \***) e essa nota tem de ser do grupo informado
(**\* Processo cadastrado em outro grupo \***); e alguns relatórios só passam se
houver registro a listar para os parâmetros informados (**\* Nao existem reg. para
os parametros inf. \*** e **\* Nao existem registros para estes parametros \***).

[?] O fornecedor é o único cadastro conferido num conjunto que **traz** os
excluídos, e o código procura o registro informado; achando um marcado como
excluído, ele volta a procurar, mas **não reconfere se o registro que voltou é o
fornecedor informado** — ao contrário do que faz com o processo, o gênero e as
notas fiscais, que reconferem a chave depois de ler. Ou essa releitura pula o
excluído e segue para outro fornecedor, e o pedido passa a valer para um
fornecedor que não foi o informado, ou ela devolve o mesmo registro e a procura
não termina. Pergunta ao site; não escolho um dos dois.

### RN-07 — As datas têm de ser reais e o período tem de fechar

Nos relatórios que pedem período, a **data inicial** e a **data limite** são
conferidas como datas: cada uma tem de ser um dia, mês e ano que existam, com o
**ano entre 1994 e 2099**. Não sendo, a recusa é **\* Data inicial invalida \*** ou
**\* Data final invalida \***, com o cursor de volta ao campo. A data limite não
pode ser anterior à inicial: **\* Data final < data inicial \***. E alguns
relatórios limitam o tamanho do período, com recusa própria: menos de seis meses,
num dos relatórios desta jornada — e dois anos, em outros, fora dela.

### RN-08 — O que o relatório exige tem de vir informado e dentro do domínio

Além dos parâmetros de cadastro, cada relatório tem os seus parâmetros
obrigatórios. Em branco, a tela recusa com a mensagem daquele parâmetro — por
exemplo **\* Informe o fornecedor \***, **\* Informe o tipo de contrato \***,
**\* Informe o genero \***, **\* Informe o Orgao. Todos = 99999999 \***,
**\* Informe a quantidade de vias. Maximo = 3 \*** — sempre devolvendo o cursor ao
campo. Quando o parâmetro admite um valor que significa "todos", a própria
mensagem o indica: **\* Informe o fornecedor. Todos = 9999 \***,
**\* Informe o tipo de contrato. Todos = 999 \***.

Há parâmetros de domínio fechado, que aceitam apenas as letras anunciadas na
própria recusa: **\* Informe O=por processo ou C=consolidado \***,
**\* Informe O=Orgao, F=Fornecedor ou T=TC \***, **\* Informe P=em proc, S=sem nr
proc ou T=todas \***. E a quantidade de vias vai de 1 a 3:
**\* Maxima quantidade de vias = 3 \***.

### RN-09 — A digitação é editada antes de qualquer conferência

As **22 posições de entrada** da tela passam pela conferência numérica **antes** de
qualquer consulta a cadastro: o que não for número não chega ao banco. Campo em
branco é tratado como zero, e o que sobra é interpretado pelo tamanho que a tela
espera — a secretaria com dois dígitos, o lote com seis, o fornecedor com quatro, o
dia e o mês com dois, o ano com quatro, o órgão com oito, o tipo de contrato com
três, a subclasse com dois, o gênero com cinco, a quantidade de vias com um, o mês
e o ano do pagamento com dois e quatro, e as partes do número do processo com dois,
dois, seis e quatro. Quando uma posição é recusada, o cursor volta para ela.

[?] O que o servidor vê quando a digitação é recusada — se há mensagem, e qual —
não está no acervo: a conferência numérica é feita por um recurso do ambiente do
sistema, que não veio no lote de fontes. Só se sabe que o cursor volta ao campo.

### RN-10 — Passando, a tela registra a solicitação e dispara o processamento

Passando por todas as conferências, a tela **registra uma solicitação nova na
fila** — com o relatório, o tipo de órgão, o grupo (ou o grupo que o relatório fixa,
nos relatórios que não perguntam o grupo), a matrícula de quem pediu, a impressora
da sessão, a estação, a data do sistema e os parâmetros daquele relatório — e, em
seguida, **entrega o relatório ao processamento**. São dois processamentos
possíveis, e qual deles recebe a solicitação depende do relatório: um recebe a
estação de onde o pedido saiu junto com os parâmetros; o outro recebe o número do
processo e uma lista de fornecedores no lugar dela.

O número da solicitação não é digitado: a tela procura a última solicitação
registrada na fila e toma a seguinte.

Esta é a última tela da jornada: ela **não abre outra tela** e não passa registro
nenhum adiante. O que ela entrega é a solicitação — ao processamento, que a busca
depois —, e o servidor volta ao menu de relatórios, de onde pode pedir outro
relatório.

### RN-11 — A tela não altera, não exclui e não deixa auditoria

A tela lê o cadastro de telas, o cadastro de tipos de órgão, o cadastro do
servidor, os cadastros de fornecedor, grupo, tipo de contrato, órgão, gênero,
permissão, grupamento, operador logístico, as notas fiscais, os registros de
processo e a própria fila de solicitações. Ela **escreve só na fila, e só
incluindo**. Nenhum registro existente é alterado ou excluído, e nenhum registro de
trilha de auditoria é gerado — o cadastro de auditoria nem sequer está entre os que
a tela enxerga. Para todos esses cadastros existe o que seria preciso para gravar e
para excluir, mas nada disso é executado em nenhum caminho: **estar preparado não é
executar**.

### RN-12 — Falha de acesso ao banco interrompe o pedido

Toda leitura e a gravação testam o retorno do banco. Havendo erro, a transação é
interrompida com o aviso do sistema e o resto do caminho não é percorrido: a
solicitação não é considerada registrada, e nenhum processamento é disparado.

---

## Cenários BDD

```gherkin
Funcionalidade: Solicitar o processamento dos relatórios fiscais

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela N099P
    E escolhi o relatório e a impressora no menu de relatórios

  Cenário: O relatório e a impressora não são perguntados
    Dado que cheguei à tela pelo menu de relatórios
    Quando abro a tela
    Então não me é pedido qual relatório emitir
    E a impressora que escolhi no menu é a que segue com o pedido
    E a solicitação sai com a minha matrícula e com a estação de onde pedi

  Cenário: A tela só pede os parâmetros do relatório escolhido
    Dado que escolhi um dos relatórios que esta tela atende
    Quando abro a tela
    Então só ficam em uso as posições de que aquele relatório precisa
    E essas posições aparecem assinaladas com um asterisco
    E o cursor fica na primeira delas
    E as demais posições ficam em branco

  Cenário: Abrir a tela não grava nada
    Dado que abro a tela e ainda não confirmei
    Então nenhuma solicitação é registrada
    E nenhum processamento é disparado

  Cenário: Pedido do relatório que se resolve pelo processo
    Dado que escolhi um relatório que pede o número do processo e o grupo
    E informei a secretaria, o lote e o grupo
    E o processo existe e é do meu grupo
    E não há solicitação desse relatório na fila para o meu grupo
    Quando confirmo a tela
    Então uma solicitação nova é registrada na fila
    E o relatório é entregue ao processamento

  Cenário: Pedido do relatório que se resolve pelo fornecedor e pelo período
    Dado que escolhi um relatório que pede o fornecedor e o período
    E informei um fornecedor cadastrado
    E informei a data inicial e a data limite
    E não há solicitação desse relatório na fila para o meu grupo
    Quando confirmo a tela
    Então uma solicitação nova é registrada na fila
    E o relatório é entregue ao processamento

  Cenário: Pedido do relatório que se resolve pelo órgão e pelo período
    Dado que escolhi um relatório que pede o período, o grupo e o órgão
    E informei a data inicial e a data limite
    E informei o grupo e o órgão
    E não há solicitação desse relatório na fila para o meu grupo
    Quando confirmo a tela
    Então uma solicitação nova é registrada na fila
    E o relatório é entregue ao processamento

  Cenário: Pedido repetido enquanto o anterior está na fila
    Dado que já existe uma solicitação do mesmo relatório para o meu grupo
    Quando confirmo a tela
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E o cursor volta ao campo do grupo
    E nenhuma solicitação nova é registrada
    E nenhum processamento é disparado

  Cenário: Grupo não informado
    Dado que deixei o grupo em branco
    Quando confirmo a tela
    Então vejo a mensagem "* Informe o grupo *"
    E o cursor volta ao campo do grupo
    E nada é registrado

  Cenário: Grupo de outro servidor
    Dado que tenho grupo na minha sessão
    E informei um grupo diferente do meu
    Quando confirmo a tela
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"
    E o cursor volta ao campo do grupo
    E nada é registrado

  Cenário: O "todos" pedido por quem tem grupo
    Dado que escolhi um relatório cujo grupo admite o valor que significa "todos"
    E tenho grupo na minha sessão
    E pedi o valor que significa "todos"
    Quando confirmo a tela
    Então vejo a mensagem "* Usuario sem acesso a 99 *"
    E o cursor volta ao campo do grupo
    E nada é registrado

  Cenário: Fornecedor não cadastrado
    Dado que escolhi um relatório que pede o fornecedor
    E informei um fornecedor que não está cadastrado
    Quando confirmo a tela
    Então vejo a mensagem "* Fornecedor nao cadastrado *"
    E o cursor volta ao campo do fornecedor
    E nada é registrado

  Cenário: Tipo de contrato não cadastrado
    Dado que escolhi um relatório que pede o tipo de contrato
    E informei um tipo de contrato que não está cadastrado
    Quando confirmo a tela
    Então vejo a mensagem "* Tipo de contrato nao cadastrado *"
    E o cursor volta ao campo do tipo de contrato
    E nada é registrado

  Cenário: Processo que não existe ou é de outro grupo
    Dado que escolhi um relatório que se resolve pelo processo
    Quando confirmo a tela com um processo sem nota fiscal, ou de outro grupo
    Então vejo a mensagem "* Processo nao cadastrado *" ou "* Processo cadastrado em outro grupo *"
    E o cursor volta ao campo do processo
    E nada é registrado

  Cenário: Sem registro para os parâmetros informados
    Dado que escolhi um relatório que confere se há registro a listar
    E informei parâmetros para os quais não há registro
    Quando confirmo a tela
    Então vejo a mensagem de que não existem registros para os parâmetros informados
    E o cursor volta ao campo do período
    E nada é registrado

  Cenário: Data inicial que não existe
    Dado que escolhi um relatório que pede período
    E informei uma data inicial que não é uma data real
    Quando confirmo a tela
    Então vejo a mensagem "* Data inicial invalida *"
    E o cursor volta ao campo da data inicial
    E nada é registrado

  Cenário: Data limite anterior à inicial
    Dado que escolhi um relatório que pede período
    E informei uma data limite anterior à data inicial
    Quando confirmo a tela
    Então vejo a mensagem "* Data final < data inicial *"
    E o cursor volta ao campo da data limite
    E nada é registrado

  Cenário: Período maior do que o relatório aceita
    Dado que escolhi um relatório que limita o tamanho do período
    E informei um período maior do que o limite
    Quando confirmo a tela
    Então vejo a mensagem de período máximo daquele relatório
    E o cursor volta ao campo da data
    E nada é registrado

  Cenário: Parâmetro obrigatório em branco
    Dado que escolhi um relatório que exige um parâmetro
    E deixei esse parâmetro em branco
    Quando confirmo a tela
    Então vejo a mensagem que pede aquele parâmetro
    E o cursor volta ao campo
    E nada é registrado

  Cenário: Letra fora do domínio daquele parâmetro
    Dado que escolhi um relatório cujo parâmetro só aceita as letras anunciadas
    E informei uma letra que não está entre elas
    Quando confirmo a tela
    Então vejo a mensagem que anuncia as letras aceitas
    E o cursor volta ao campo
    E nada é registrado

  Cenário: Quantidade de vias acima do máximo
    Dado que escolhi um relatório que pede a quantidade de vias
    E informei mais de três vias
    Quando confirmo a tela
    Então vejo a mensagem "* Maxima quantidade de vias = 3 *"
    E o cursor volta ao campo das vias
    E nada é registrado

  Cenário: Digitação não numérica
    Dado que digitei em uma das posições numéricas algo que não é número
    Quando confirmo a tela
    Então o sistema recusa a digitação antes de conferir qualquer cadastro
    E o cursor volta à posição recusada
    E nada é registrado

  Cenário: A tela não altera, não exclui e não deixa auditoria
    Dado que registro uma solicitação
    Então nenhum registro existente é alterado ou excluído
    E nenhum registro de trilha de auditoria é gerado
    E o único registro escrito é o da solicitação, na fila

  Cenário: Falha de acesso ao banco
    Dado que o banco falha em uma das leituras ou na gravação
    Quando confirmo a tela
    Então a transação é interrompida com o aviso do sistema
    E a solicitação não é considerada registrada
    E nenhum processamento é disparado
```
