# US — C270T — Percentual do atendimento por segmento e tipo de refeição

## Estória

Como **servidor de CRE**, quero **definir, para cada tipo de refeição de cada segmento de
atendimento da minha secretaria, o percentual que a atualização do cadastro de atendimento deve
aplicar**, para que **as quantidades de atendimento sejam apuradas na proporção de cada
segmento, sem ninguém refazer a conta segmento por segmento**.

O percentual é o que converte o total de atendimento apurado na quantidade que cabe àquele
segmento em cada tipo de refeição. A atualização do cadastro procura o percentual do nível mais
específico ao mais geral e aplica o primeiro que encontra; o desta tela é o do segmento, e sem
ele registrado a atualização desce para o nível mais geral e, não existindo nenhum, toma a
refeição por inteiro. E é também por esta tela que a secretaria pede que a atualização do
cadastro rode, para não depender de alguém lembrar de disparar o processamento depois.

## Contexto

Jornada S000M → C000M → C028M → C270T.

Ator: servidor de CRE — define o percentual de cada tipo de refeição de cada segmento de
atendimento da sua secretaria e decide se manda atualizar o cadastro.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**,
não regra de negócio.

A tela lista as refeições que o segmento já tem — as mesmas que a tela `C116T`, do vínculo entre
o segmento e a refeição, declara — uma linha por refeição, com o percentual de cada uma. O
segmento se informa pelo código, e a refeição também, numa linha própria, que posiciona a
listagem. No fim vem a pergunta **Atualiza Cadastro <S/N>?**, com o campo da resposta ao lado.

A tela **grava**: mantém o percentual de cada par segmento e refeição, registra a auditoria de
cada mudança e cria o pedido de atualização do cadastro quando o servidor responde S. Ela **não**
cria nem apaga segmento, refeição ou vínculo: o cadastro de segmentos, o de refeições e o de
vínculos são apenas lidos. O que ela usa da sessão — a secretaria, o tipo de órgão, a matrícula,
o acesso, a CRE e o terminal — é o que a entrada deixou.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela mantém um percentual por segmento e tipo de refeição

A tela mantém, para cada segmento de atendimento e cada tipo de refeição, um percentual inteiro
de zero a cem, junto com a matrícula de quem o registrou e a data do registro. O tipo de órgão é
sempre o da sessão: a tela não pergunta de qual secretaria se trata e não há como manter o
percentual de outra. O segmento e a refeição identificam o registro, e a refeição com que a tela
trabalha é uma das que o segmento já tem — é essa a lista que ela mostra e sobre a qual ela
grava.

[?] O cadastro do percentual admite mais de um registro para o mesmo par segmento e refeição, e a
tela lê e grava como se houvesse um só: se houver dois, ela não sabe qual deles está mostrando
nem qual está trocando. Ou a repetição é intencional e a tela devia escolher, ou a base devia
barrá-la. Pergunta ao site.

[?] O dicionário da base declara, nesse cadastro, um segundo campo numérico — um campo de perfil
— que nenhum programa do acervo escreve, e que o registro montado por esta tela nem carrega. Ou
o campo é de outro dono, ou o percentual desta tela deveria preenchê-lo. Pergunta ao site.

### RN-02 — A tela lista as refeições do segmento com o percentual de cada uma

A tela lista as refeições que o segmento já tem, uma por linha, com o código, a descrição e o
percentual de cada uma — em branco quando não há percentual registrado. A lista comporta
**onze** linhas. A tela mostra ainda a descrição do tipo de órgão, a descrição do segmento, a
data do sistema, uma linha própria com o código e a descrição de uma refeição de referência e,
no fim da lista, a pergunta **Atualiza Cadastro <S/N>?** com o campo da resposta ao lado.

A refeição informada na linha de referência posiciona a listagem: se ela for uma das que o
segmento tem, a lista recomeça por ela; se não for, a lista recomeça pela primeira refeição do
segmento. Quando a página se completa com as onze linhas, a própria tela reescreve ali o código
e a descrição da refeição da última linha, de modo que o servidor sempre vê ali a última
refeição que estava na tela.

### RN-03 — Segmento sem refeição: a tela avisa e encerra a listagem

Quando o segmento não tem nenhuma refeição, a tela avisa
**\* Segmento sem percentuais cadastrados \*** e encerra a listagem.

[?] O aviso fala de percentuais, mas a condição que o dispara é o segmento não ter refeição
nenhuma: um segmento com refeições e sem nenhum percentual registrado não dá aviso — aparece com
a coluna do percentual em branco. Ou o aviso está no caso errado, ou o silêncio é intencional.
Pergunta ao site.

### RN-04 — A tela só aceita alteração e consulta

A opção informada só pode ser **alteração** ou **consulta**. Qualquer outra é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \***, o cursor volta ao campo da opção e nada é lido
nem gravado.

[?] A mensagem nomeia as opções como **ALT** e **CON**, mas a tela confere o que foi digitado
contra os códigos internos de alteração e de consulta do sistema. Nenhum fonte do acervo mostra
quem traduz o que o servidor digita no código conferido; se não houver essa tradução, a guarda
recusa toda opção — inclusive as duas que a própria mensagem pede. A mesma dúvida já está
registrada nas telas irmãs desta família. Pergunta ao site.

### RN-05 — Consultar exige um segmento informado e cadastrado

Na consulta o segmento é obrigatório: em branco, a recusa é **\* Informe o segmento \***;
informado mas não cadastrado para o tipo de órgão, a recusa é
**\* Segmento nao cadastrado \*** — nos dois casos com o cursor de volta ao campo do segmento.
Passando, a tela adota aquele segmento e a sua descrição e reinicia a leitura das refeições desde
a primeira. O segmento que a sessão já adotou não é reconferido no cadastro.

### RN-06 — Alterar exige ter consultado o mesmo segmento

Para alterar, o segmento informado tem de ser o mesmo que a última consulta deixou na sessão. Se
for outro, a recusa é **\* Consulte antes de atualizar \***, com o cursor de volta ao campo do
segmento, e nada é lido nem gravado. É essa amarração que garante que a alteração recai sobre um
segmento que a tela já leu e validou no cadastro.

### RN-07 — A passagem para o novo segmento leva ao seguinte e não grava nada

A tela aceita um indicador de passagem para o **novo segmento**: ele leva ao segmento seguinte ao
informado e, quando esse não existe, volta ao primeiro segmento cadastrado para o tipo de órgão.
Quando o indicador vem preenchido, nenhum percentual é gravado e nenhum pedido de atualização é
criado — a passagem só troca o segmento em foco. Na alteração o indicador é recusado com
**\* Consulte antes de solicitar novo seg \***, com o cursor de volta ao campo do segmento.

[?] Quem preenche esse indicador não está no programa: ele é lido e limpo, nunca escrito. Ou o
terminal o preenche — uma tecla de função —, ou o recurso é inalcançável. Pergunta ao site.

[?] Ao adotar um segmento informado, a tela mostra a descrição de trinta posições; na passagem
para o novo segmento, ela mostra a descrição de quinze posições do mesmo cadastro. Ou as duas
são a mesma coisa, ou a passagem troca o texto que o servidor lê. Pergunta ao site.

### RN-08 — O percentual vai de zero a cem

O percentual informado é um número de três posições: o que não for número é recusado pela edição
numérica, com o cursor de volta ao campo, e o campo deixado em branco conta como **zero**. Acima
de cem a recusa é **\* Percentual maximo invalido \*** e o cursor volta ao campo do percentual. O
zero é aceito e tem significado: a refeição fica **sem percentual registrado**, e é ele que apaga
o que estava lá (RN-09). Nada é gravado na passagem em que a recusa acontece, e o percentual não
chega a ser conferido quando o servidor responde S (RN-11).

[?] O texto que o servidor lê nessa coluna não é demonstrável: o nome interno do campo fala em
quantidade de pessoas, a mensagem de recusa o chama de percentual e a atualização do cadastro o
divide por cem para obter a fração. O rótulo da coluna não está no corpus. Pergunta ao site.

### RN-09 — Na alteração, cada refeição é incluída, trocada, apagada ou deixada como está

Com a opção de alteração e a resposta do fim da lista **diferente de S** (o **N** da pergunta; em
branco também não é S e segue o mesmo caminho), o sistema cuida do percentual de **cada** refeição
listada, e o que ele faz depende do que já estava registrado:

- não havia percentual e o informado não é zero: o percentual é **incluído**;
- havia um percentual diferente do informado e o informado não é zero: o percentual é
  **trocado**;
- havia um percentual registrado e o informado é zero: o registro é **apagado**;
- o informado é igual ao que já estava registrado: **nada é feito**;
- não havia percentual e o informado é zero: **nada é feito**.

Na inclusão, a matrícula de quem operou e a data do dia ficam no registro.

[?] Na troca, o registro mantém a matrícula e a data de quem o registrou pela primeira vez: o
sistema reescreve apenas o percentual. O dado é apresentado como data de atualização, mas numa
troca ela não avança — pela tela, a data do registro é sempre a da inclusão. Ou a intenção é
guardar quem cadastrou, ou a data da última mudança está se perdendo. Pergunta ao site.

### RN-10 — A consulta não grava nada

Com a consulta escolhida, o processamento da gravação termina antes de qualquer decisão de
registro: nenhum percentual é incluído, trocado ou apagado, nenhum pedido de atualização é criado
e nenhum registro de auditoria é escrito — mesmo que o servidor preencha a resposta do fim da
lista. A consulta ainda pode mostrar a recusa de relatório em processamento (RN-12), e essa
recusa barra também a gravação da alteração na mesma passagem.

### RN-11 — A resposta S pede a atualização do cadastro, e só na alteração

Com a opção de **alteração** e a resposta **S**, o sistema cria um **pedido de atualização do
cadastro** — o relatório de atualização — com o número seguinte ao último pedido já registrado,
o tipo de órgão da sessão, a coordenação regional escolar **1**, a matrícula de quem opera, o
terminal, o dia e o mês — e, na instalação que processa em lote, manda o pedido ao processamento
com o código do relatório, uma cópia, o terminal, a matrícula, o correio eletrônico de quem opera
e os parâmetros da secretaria. A tela avisa **\*\* Cadastro sendo atualizado \*\*** e volta para
si mesma.

**Os percentuais informados nessa passagem não são gravados nem conferidos**: quem os grava é a
resposta diferente de S (RN-09), e a atualização usa o que já estava registrado para cada par.

O pedido só é criado na alteração: com a consulta escolhida, a resposta S não cria pedido nenhum
e não grava nada (RN-10).

[?] A resposta S é ignorada na consulta, mas a conferência de relatório em processamento roda nas
duas opções: quem consulta e responde S pode ser recusado por causa de um relatório que a sua
resposta não iria criar. Ou a resposta devia valer nas duas opções, ou a conferência não devia
acontecer na consulta. Pergunta ao site.

[?] Se o servidor digitar percentuais novos e responder S, a atualização roda com os percentuais
que já estavam registrados e os novos se perdem. O acervo não mostra o servidor fazendo as duas
coisas em duas passagens, nem permite dizer se a intenção era essa. Pergunta ao site.

[?] O pedido é registrado sempre para a **coordenação regional escolar 1**, e não para a
coordenação de quem opera. O acervo não diz por quê. Pergunta ao site.

[?] O envio ao processamento depende da instalação: numa instalação que não seja a que processa em
lote, pelo texto o pedido fica criado e o servidor vê o aviso de que o cadastro está sendo
atualizado, sem a atualização rodar. O que distingue as instalações não está no corpus. Pergunta
ao site.

### RN-12 — Não se pede a atualização com um relatório em processamento

Antes de aceitar a resposta **S**, o sistema confere se já existe um pedido do mesmo relatório de
atualização para o tipo de órgão da sessão e a coordenação 1. Havendo, a recusa é
**\* Relatorio em processamento. Aguarde. \***, com o cursor no campo da resposta, e nada é pedido
nem gravado. A conferência vale só para a resposta S: com a resposta diferente de S os percentuais
são registrados mesmo com o relatório em andamento — e, como ela roda também na consulta, pode
recusar uma resposta S que não criaria pedido nenhum (RN-11).

[?] A tela tem um atalho que dispensaria as conferências quando a solicitação de atualização já
estivesse marcada na sessão; nenhum ponto do acervo marca essa condição, e a própria tela só a
limpa. Ou o atalho é inalcançável, ou quem a marca está fora do que se pôde ler. Pergunta ao site.

### RN-13 — Toda mudança do percentual deixa rastro na auditoria

Cada inclusão, troca ou exclusão grava um registro de auditoria com o cadastro auditado (o próprio
percentual por segmento e refeição), a operação, os valores anterior e posterior e o contexto da
sessão: matrícula, coordenação regional escolar, terminal, data e hora. O número do processo no
rastro é o **código do segmento**. O pedido de atualização **não** gera registro de auditoria: o
próprio pedido é o documento da solicitação.

[?] Na inclusão, o valor anterior que vai para a auditoria é o registro recém-criado e o posterior
fica em branco — o mesmo formato da exclusão, e o inverso do que faz a tela de percentual por
gênero deste mesmo sistema. Ou o campo guarda o valor gravado, ou a auditoria da inclusão conta a
história trocada. Pergunta ao site.

[?] A inclusão só deixa o rastro quando a gravação não devolve uma marca própria do ambiente; o
acervo não mostra quem produz essa marca nem o que ela significa, e o mesmo trecho não existe nos
outros dois caminhos. Ou a marca nunca acontece, ou há inclusões sem rastro. Pergunta ao site.

### RN-14 — Nada acontece sem a segurança do perfil, da rota e da operação

Antes de exibir, a tela leva a sessão à segurança do perfil (o cadastro de telas); a passagem de
conferência leva o contexto da sessão à segurança da rota e à da operação (a **alteração**, que é
a operação desta tela). Se qualquer uma não devolver OK, o processamento é abandonado: nada é
exibido, nada é conferido, nada é gravado e nada é auditado. A liberação da alteração é conferida
uma vez, na passagem de conferência, e não se repete na de gravação.

[?] A permissão é conferida na passagem de validação e não se repete na passagem que grava: se ela
mudasse entre as duas, a gravação não a reconferiria. Pergunta ao site.

### RN-15 — A tela abre pelo que a sessão já trazia; sem segmento, abre em consulta

Ao abrir, a tela toma a operação e o segmento de atendimento do que a sessão já tinha. Quem chega
pela tela de consulta desta mesma família — a `C270C`, que passa o segmento adiante — entra já
posicionado nesse segmento e no modo que ela passou, sem precisar informar nada. Quem chega pelo
menu encontra o campo do segmento vazio e a operação já em **consulta**: sem segmento na sessão, a
tela não deixa a operação em alteração. É por isso que a mesma tela pode abrir pronta para
consultar um segmento já escolhido, ou abrir vazia e em consulta, conforme a origem.

[?] O acervo mostra a tela de consulta da família passando o segmento e o modo para esta, mas não
mostra o servidor acionando essa passagem — o campo que a dispara é lido pela tela de origem e
nunca escrito por ela. Ou a passagem é acionada por uma tecla de função do terminal, ou é
inalcançável. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Percentual do atendimento por segmento e tipo de refeição

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C270T

  Cenário: O percentual é mantido para o tipo de órgão da minha secretaria
    Dado que consultei um segmento da minha secretaria
    Quando registro um percentual para uma refeição desse segmento
    Então o percentual fica registrado para o tipo de órgão da minha sessão
    E ficam com ele a minha matrícula e a data do dia
    E não há campo para escolher outro tipo de órgão

  Cenário: A tela lista as refeições do segmento com o percentual de cada uma
    Dado que a minha secretaria tem um segmento com refeições
    Quando consulto esse segmento
    Então vejo as refeições do segmento, uma por linha, com o código, a descrição e o percentual de cada uma
    E vejo a descrição do tipo de órgão, a descrição do segmento e a data do sistema
    E vejo, no fim, a pergunta "Atualiza Cadastro <S/N>?" com o campo da resposta
    E a lista mostra até onze refeições

  Cenário: A linha da refeição de referência posiciona a lista
    Dado que consultei um segmento com várias refeições
    Quando informo na linha de referência uma refeição que o segmento tem
    Então a lista recomeça por essa refeição
    E, quando a página se completa, a linha de referência passa a mostrar a refeição da última linha

  Cenário: Refeição de referência que o segmento não tem
    Dado que consultei um segmento com várias refeições
    Quando informo na linha de referência uma refeição que o segmento não tem
    Então a lista recomeça pela primeira refeição do segmento

  Cenário: Segmento sem refeições
    Dado que o segmento informado não tem nenhuma refeição
    Quando o consulto
    Então vejo a mensagem "* Segmento sem percentuais cadastrados *"
    E a lista termina

  Cenário: Opção de manutenção fora de alteração e consulta
    Quando informo uma opção diferente de alteração e de consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é lido nem gravado

  Cenário: Consulta sem o segmento informado
    Dado que estou na tela com a opção de consulta
    Quando deixo o segmento em branco e confirmo
    Então vejo a mensagem "* Informe o segmento *"
    E o cursor volta ao campo do segmento

  Cenário: Consulta de um segmento não cadastrado
    Dado que estou na tela com a opção de consulta
    Quando informo um segmento que não está cadastrado para o tipo de órgão
    Então vejo a mensagem "* Segmento nao cadastrado *"
    E o cursor volta ao campo do segmento

  Cenário: Alteração de um segmento que não foi consultado
    Dado que estou na tela com a opção de alteração
    E informo um segmento diferente do que consultei
    Quando confirmo
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E nada é gravado

  Cenário: Passagem para o novo segmento
    Dado que estou consultando um segmento
    Quando aciono a passagem para o novo segmento
    Então a tela passa ao segmento seguinte cadastrado
    E, se não houver seguinte, volta ao primeiro segmento cadastrado
    E nada é gravado nem pedido nessa passagem

  Cenário: Passagem para o novo segmento na alteração
    Dado que estou na tela com a opção de alteração
    Quando aciono a passagem para o novo segmento e confirmo
    Então vejo a mensagem "* Consulte antes de solicitar novo seg *"
    E nada é gravado

  Cenário: Percentual acima de cem
    Quando informo um percentual maior que cem
    Então vejo a mensagem "* Percentual maximo invalido *"
    E o cursor volta ao campo do percentual
    E nada é gravado

  Cenário: Percentual em branco conta como zero
    Dado que uma das refeições listadas já tem percentual registrado
    Quando deixo o percentual dessa linha em branco, respondo N e confirmo
    Então o percentual registrado deixa de existir
    E a operação deixa rastro na auditoria

  Cenário: Alteração inclui o percentual de uma refeição que não tinha
    Dado que uma das refeições listadas não tem percentual registrado
    Quando informo um percentual de um a cem, respondo N e confirmo
    Então o percentual dessa refeição fica registrado
    E a data do dia e a minha matrícula ficam no registro
    E a operação deixa rastro na auditoria

  Cenário: Alteração troca o percentual de uma refeição
    Dado que uma das refeições listadas já tem um percentual registrado
    Quando informo outro percentual, respondo N e confirmo
    Então o percentual dessa refeição passa a ser o informado
    E a operação deixa rastro na auditoria

  Cenário: Alteração com o mesmo percentual não muda nada
    Dado que uma das refeições listadas já tem um percentual registrado
    Quando informo o mesmo percentual, respondo N e confirmo
    Então nada é gravado

  Cenário: A consulta não grava nada
    Dado que estou na tela com a opção de consulta e um segmento consultado
    Quando percorro a lista e confirmo
    Então nenhum percentual é incluído, trocado ou apagado
    E nenhum pedido de atualização é criado
    E nenhum registro de auditoria é escrito

  Cenário: Resposta S na alteração pede a atualização do cadastro
    Dado que estou na tela com a opção de alteração e não há atualização em processamento
    Quando respondo S e confirmo
    Então o sistema cria um pedido de atualização do cadastro para o meu tipo de órgão
    E o pedido recebe o número seguinte ao último já registrado
    E vejo a mensagem "** Cadastro sendo atualizado **"
    E, na instalação que processa em lote, o pedido é enviado ao processamento

  Cenário: Resposta S não grava os percentuais informados
    Dado que estou na tela com a opção de alteração e uma refeição já tem percentual registrado
    Quando informo um percentual diferente, respondo S e confirmo
    Então o pedido de atualização é criado
    E o percentual informado não é gravado
    E a atualização usa o percentual que já estava registrado

  Cenário: Resposta S na consulta não cria pedido
    Dado que estou na tela com a opção de consulta e um segmento consultado
    Quando respondo S e confirmo
    Então nenhum pedido de atualização é criado
    E nada é gravado

  Cenário: Relatório de atualização já em processamento
    Dado que já existe um pedido de atualização em processamento para o meu tipo de órgão
    Quando respondo S e confirmo
    Então vejo a mensagem "* Relatorio em processamento. Aguarde. *"
    E o cursor volta ao campo da resposta
    E nada é pedido nem gravado

  Cenário: Toda mudança do percentual deixa rastro na auditoria
    Dado que incluí, troquei ou apaguei o percentual de uma refeição
    Quando a gravação termina
    Então existe um registro de auditoria com o cadastro auditado, a operação e os valores anterior e posterior
    E com a matrícula, a coordenação regional escolar, o terminal, a data e a hora
    E o número do processo no rastro é o código do segmento

  Cenário: Operação sem autorização
    Dado que a minha sessão não passa na segurança do perfil, da rota ou da alteração
    Quando tento manter os percentuais
    Então a tela volta sem conferir os dados
    E nada é gravado nem pedido

  Cenário: A tela abre pelo que a sessão já trazia
    Dado que a sessão já tem um segmento de atendimento adotado
    Quando abro a tela
    Então ela abre já posicionada nesse segmento e no modo que a sessão deixou
    E não preciso informar o segmento outra vez

  Cenário: A tela sem segmento na sessão abre em consulta
    Dado que a sessão não tem segmento de atendimento adotado
    Quando abro a tela
    Então ela abre sem segmento e com a operação em consulta
    E não há como abri-la em alteração sem antes consultar um segmento
```
