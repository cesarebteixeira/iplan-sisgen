# US — C272T — Percentual do atendimento por órgão filho, segmento e tipo de refeição

## Estória

Como **servidor de CRE**, quero **definir, para cada órgão filho da minha coordenação e cada tipo
de refeição de cada segmento de atendimento, o percentual que a apuração do atendimento deve
aplicar**, para que **o atendimento daquele órgão seja apurado na proporção que lhe cabe, sem
ninguém refazer a conta órgão por órgão**.

O percentual é o que converte o atendimento apurado no quantitativo que cabe ao órgão filho, e o
desta tela é o mais específico de todos: não existindo para um par de segmento e tipo de refeição,
a apuração desce para o percentual do segmento, depois para o da refeição e, por último, para o
geral; sem nenhum deles, toma a refeição por inteiro. E a tela não guarda só o percentual: a cada
mudança ela reavalia o atendimento já registrado do órgão para aquele par de segmento e refeição,
sinalizando o que ficou acima do que o percentual permite e limpando o que está vazio — é o que
mantém o atendimento do órgão coerente com o percentual sem esperar o processamento do mês.

## Contexto

Jornada S000M → C000M → C028M → C272T.

Ator: servidor de CRE — informa o órgão filho e o segmento de atendimento, mantém o percentual de
cada tipo de refeição do segmento e vê a reavaliação do atendimento do órgão.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio.

A tela trabalha sobre um órgão filho por vez. A coordenação regional escolar e o indicador de
creche que ela mostra vêm do cadastro do órgão, não do que o servidor digita; a lista que ela
oferece é a das refeições que aquele segmento já tem, e o que o servidor informa é o percentual de
cada uma. O que ela usa da sessão — o tipo de órgão (a secretaria), a matrícula, o acesso, a
coordenação, o órgão filho do usuário e o terminal — é o que a entrada e as telas anteriores
deixaram.

A tela **grava**: mantém o percentual de cada par de órgão filho, segmento e tipo de refeição,
registra a auditoria de cada mudança e, a cada mudança, reavalia e limpa os atendimentos do órgão.
Ela **não** cria nem apaga órgão, segmento, refeição ou vínculo: esses cadastros são apenas lidos.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela mantém o percentual do órgão filho, do segmento e do tipo de refeição

A tela mantém, para cada órgão filho, cada segmento de atendimento e cada tipo de refeição, um
percentual inteiro de zero a cem, junto com a matrícula de quem o registrou e a data do registro. O
órgão filho, o segmento e a refeição identificam o registro, e o órgão filho é sempre da secretaria
da sessão: a tela não pergunta de qual secretaria se trata e não há como manter o percentual de
outra. A coordenação regional escolar é guardada com o registro, mas não faz parte da identificação
dele — e a coordenação gravada é a do cadastro do órgão, não a que o servidor digitar.

[?] O cadastro do percentual admite mais de um registro para o mesmo órgão filho, segmento e
refeição, e a tela lê e grava como se houvesse um só: se houver dois, ela não sabe qual deles está
mostrando nem qual está trocando. Ou a repetição é intencional e a tela devia escolher, ou a base
devia barrá-la. Pergunta ao site.

[?] A coordenação regional escolar fica fora da chave do registro, mas é gravada nele. Se um mesmo
órgão filho puder mudar de coordenação, o percentual antigo continua identificando o par e passa a
carregar a coordenação nova. Ou a coordenação é redundante com o órgão, ou a chave não protege o
que a tela grava. Pergunta ao site.

[?] O dicionário da base declara, nesse cadastro, um segundo campo numérico — um campo de perfil —
que nenhum programa do acervo escreve, e que o registro montado por esta tela nem carrega. Ou o
campo é de outro dono, ou o percentual desta tela deveria preenchê-lo. Pergunta ao site.

### RN-02 — O percentual do órgão filho é o mais específico da escala

Ao reavaliar um atendimento, a tela procura o percentual do órgão filho para aquele segmento e
aquela refeição; não o achando, ou achando-o zerado, procura o do segmento e da refeição; depois o
da refeição; depois o geral; e, não achando nenhum, toma a refeição por inteiro. É a mesma
escala que a apuração do atendimento usa, e é por isso que o percentual desta tela, quando existe,
é o que vale para o órgão filho.

### RN-03 — A tela lista as refeições que o segmento tem, com o percentual de cada uma

A tela lista as refeições que o segmento já tem, uma por linha, com o código, a descrição e o
percentual de cada uma — em branco quando não há percentual registrado para aquele órgão filho. A
lista comporta **onze** linhas. A tela mostra ainda o nome do órgão filho, a descrição do tipo de
órgão, a descrição do segmento, o indicador de creche do órgão (traduzido em **Sim** ou **Nao**) e a
data do sistema.

No fim da lista vem a linha de referência, com o código e a descrição de uma refeição. A refeição
informada ali posiciona a listagem: a lista recomeça pela primeira refeição que o segmento tem a
partir daquela informada. Se a refeição informada não estiver no cadastro de refeições, a lista
recomeça pela primeira refeição do segmento. Quando a página se completa com as onze linhas, a
própria tela reescreve ali o código e a descrição da refeição da última linha, de modo que o
servidor sempre vê na referência a última refeição que estava na tela.

### RN-04 — Segmento sem refeição: a tela avisa e encerra a listagem

Quando o segmento não tem nenhuma refeição, a tela avisa **\* Segmento sem percentuais cadastrados
\*** e encerra a listagem.

[?] O aviso fala de percentuais, mas a condição que o dispara é o segmento não ter refeição nenhuma:
um segmento com refeições e sem nenhum percentual registrado não dá aviso — aparece com a coluna do
percentual em branco. Ou o aviso está no caso errado, ou o silêncio é intencional. Pergunta ao site.

### RN-05 — A tela só aceita alteração e consulta

A opção informada só pode ser **alteração** ou **consulta**. Qualquer outra é recusada com
**\* Opcao nao disponivel. Use ALT ou CON \***, o cursor volta ao campo da opção e nada é lido nem
gravado.

[?] A mensagem nomeia as opções como **ALT** e **CON**, mas a tela confere o que foi digitado contra
os códigos internos de alteração e de consulta do sistema. Nenhum fonte do acervo mostra quem
traduz o que o servidor digita no código conferido; se não houver essa tradução, a guarda recusa
toda opção — inclusive as duas que a própria mensagem pede. A mesma dúvida já está registrada nas
telas irmãs desta família. Pergunta ao site.

### RN-06 — Consultar exige um órgão filho informado, cadastrado e ativo

Na consulta o órgão filho é obrigatório: em branco, a recusa é **\* Informe o orgao \***. Informado,
ele tem de estar no cadastro do órgão; estando cadastrado como inativo, a recusa é **\* Orgao
cadastrado como inativo \***; e, sendo de outra secretaria, a recusa é **\* Orgao nao pertence a
esta secretaria \***. Em todos os casos o cursor volta ao campo do órgão e nada é lido nem gravado.

### RN-07 — O acesso ao órgão depende da coordenação e do órgão filho do usuário

O órgão informado também tem de estar numa coordenação regional escolar a que o servidor tenha
acesso: quando o órgão é de outra coordenação, a recusa é **\* Usuario sem acesso ao grupo deste
orgao \***. E quando a sessão já traz um órgão filho para o usuário, ele só consulta aquele:
informar outro dá **\* Usuario sem acesso a outro orgao \***. Nos dois casos o cursor volta ao campo
do órgão e nada é lido nem gravado.

[?] O órgão filho que a sessão guarda para o usuário não é escrito por nenhum programa do acervo —
só lido por esta tela e pelas telas irmãs, e zerado na preparação da sessão. Ou o perfil do usuário
o preenche por fora do acervo, ou a recusa **\* Usuario sem acesso a outro orgao \*** é inalcançável
e a restrição não existe na prática. Pergunta ao site.

### RN-08 — Consultar exige o segmento cadastrado e ligado ao órgão

O segmento informado tem de existir no cadastro de segmentos: não existindo, a recusa é
**\* Segmento nao cadastrado \***. E tem de estar ligado àquele órgão filho: não estando, a recusa é
**\* Orgao nao cadastrado neste segmento \***. Nos dois casos o cursor volta ao campo do segmento.
Passando, a tela adota o órgão, o segmento e as descrições deles, e reinicia a leitura da lista
desde a primeira refeição do segmento. Quando o órgão e o segmento são os mesmos da consulta
anterior, a tela não refaz nada disso: a listagem continua de onde estava, com a refeição de
referência que já estava na tela.

### RN-09 — Trocar de órgão leva ao primeiro segmento dele

Quando o órgão informado não é o que a sessão já tinha, o segmento informado é descartado e a tela
passa ao primeiro segmento cadastrado para aquele órgão. Quando o órgão é o mesmo e só o segmento
muda, o segmento informado é o que a tela adota — desde que passe pelas conferências de RN-08.

### RN-10 — Alterar exige ter consultado o mesmo órgão e segmento

Para alterar, o órgão filho e o segmento informados têm de ser os mesmos que a última consulta
deixou na sessão. Se forem outros, a recusa é **\* Consulte antes de atualizar \***, com o cursor de
volta ao campo do órgão, e nada é lido nem gravado. É essa amarração que garante que a alteração
recai sobre um órgão e um segmento que a tela já leu e validou no cadastro.

### RN-11 — O percentual vai de zero a cem

O percentual informado é um número de três posições: o que não for número é recusado pela edição
numérica, com o cursor de volta ao campo, e o campo deixado em branco conta como **zero**. Acima de
cem a recusa é **\* Percentual maximo invalido \***, com o cursor de volta ao campo do percentual. O
zero é aceito e tem significado: a refeição fica **sem percentual registrado**, e é ele que apaga o
que estava lá (RN-12). Nada é gravado quando a recusa acontece.

[?] O texto que o servidor lê nessa coluna não é demonstrável: o nome interno do campo fala em
quantidade de pessoas, a mensagem de recusa o chama de percentual e a própria tela o divide por cem
para calcular. O rótulo da coluna não está no corpus. Pergunta ao site.

[?] A recusa do percentual devolve o cursor a uma posição calculada com um passo de duas linhas por
refeição, e as demais recusas da mesma lista usam três. Ou o passo certo é um dos dois e o outro
deixa o cursor na linha errada — a máscara da tela não está no corpus para decidir qual. Pergunta ao
site.

### RN-12 — Na alteração, cada refeição é incluída, trocada, apagada ou deixada como está

Com a opção de alteração, o sistema cuida do percentual de **cada** refeição listada, e o que ele
faz depende do que já estava registrado para aquele órgão filho:

- não havia percentual e o informado não é zero: o percentual é **incluído**;
- havia um percentual diferente do informado e o informado não é zero: o percentual é **trocado**;
- havia um percentual registrado e o informado é zero: o registro é **apagado**;
- o informado é igual ao que já estava registrado: **nada é feito**;
- não havia percentual e o informado é zero: **nada é feito**.

Na inclusão, a matrícula de quem operou e a data do dia ficam no registro.

[?] Na troca, o registro mantém a matrícula e a data de quem o registrou pela primeira vez: o
sistema reescreve apenas o percentual. O dado é apresentado como data de atualização, mas numa troca
ela não avança — pela tela, a data do registro é sempre a da inclusão. Ou a intenção é guardar quem
cadastrou, ou a data da última mudança está se perdendo. Pergunta ao site.

### RN-13 — A consulta não grava nada

Com a consulta escolhida, o processamento termina antes de qualquer decisão de gravação: nenhum
percentual é incluído, trocado ou apagado, nenhum atendimento é reavaliado ou limpo e nenhum
registro de auditoria é escrito. A consulta só lê.

### RN-14 — A passagem para o novo segmento não grava nada

A tela aceita um indicador de passagem para o **novo segmento**: ele leva ao segmento seguinte ao
informado e, quando esse não existe, volta ao primeiro segmento cadastrado para o órgão. Quando o
indicador vem preenchido, nenhum percentual é gravado, nenhum atendimento é reavaliado e nenhuma
auditoria é escrita — a passagem só troca o segmento em foco, tanto na consulta quanto na alteração.

[?] Quem preenche esse indicador não está no programa: ele é lido e limpo, nunca escrito. Ou o
terminal o preenche — uma tecla de função —, ou o recurso é inalcançável. Pergunta ao site.

[?] Na alteração o indicador é aceito em silêncio e a gravação é pulada; na tela irmã do percentual
por segmento a mesma passagem é recusada, com aviso ao servidor. Ou o silêncio aqui é intencional,
ou a tela perde a alteração sem avisar quem operou. Pergunta ao site.

[?] Ao adotar um segmento informado, a tela mostra a descrição de trinta posições; na passagem para
o novo segmento, ela mostra a descrição de quinze posições do mesmo cadastro. Ou as duas são a mesma
coisa, ou a passagem troca o texto que o servidor lê. Pergunta ao site.

### RN-15 — Toda mudança do percentual deixa rastro na auditoria

Cada inclusão, troca ou exclusão grava um registro de auditoria com o cadastro auditado (o próprio
percentual por órgão filho, segmento e refeição), a operação, os valores anterior e posterior e o
contexto da sessão: matrícula, coordenação regional escolar, terminal, data e hora. O número do
processo no rastro é o **código do órgão filho**. A reavaliação do atendimento (RN-16) também deixa
o seu rastro quando marca o atendimento como inativo.

[?] Na troca, o valor anterior e o posterior que vão para a auditoria são o mesmo registro antigo: o
percentual informado não chega ao rastro, e as telas irmãs do mesmo sistema gravam o valor novo no
posterior. Ou a auditoria da troca guarda o cadastro como estava, ou o valor novo se perde no
rastro. Pergunta ao site.

[?] Na inclusão, o valor anterior que vai para a auditoria é o registro recém-criado e o posterior
fica em branco — o mesmo formato da exclusão, e o inverso do que faz a tela de percentual por gênero
deste mesmo sistema. Ou o campo é o "valor gravado" e não o "anterior" neste gerador, ou a auditoria
da inclusão conta a história da exclusão. Pergunta ao site.

### RN-16 — A gravação reavalia o atendimento do par de segmento e refeição

Ao gravar o percentual de uma refeição, a tela reavalia o atendimento daquele órgão filho para
aquele par de segmento e refeição. Ela toma o percentual em vigor (na escala de RN-02) multiplicado
pelo total apurado no mês de referência cadastrado para o órgão — esse produto é o que o percentual
permite. Se a quantidade de pessoas já registrada no atendimento **não superar** o produto, o
atendimento é marcado como **ativo**; se **superar**, ele é marcado como **inativo**, e nesse caso a
matrícula e a data de quem operou ficam no registro e a mudança deixa rastro na auditoria. Sem mês
de referência cadastrado para o órgão, ou sem nenhum total apurado, nada é reavaliado.

Para um órgão marcado como **creche**, o total apurado não é o do segmento em foco: a tela soma os
segmentos em dois grupos — o par formado pelos segmentos 10 e 20 e todo o restante — e compara o
atendimento de um segmento do par com o total do restante, e o de um segmento de fora do par com o
total do par.

[?] Quando o atendimento do par de segmento e refeição não existe, a decisão de marcar o atendimento
é tomada sobre o que restou da última leitura feita para o órgão, e o registro que a tela grava
nesse caso depende do comportamento do acesso a dados. O corpus não permite dizer o que acontece
aí. Pergunta ao site.

### RN-17 — A gravação apaga os atendimentos vazios do órgão

No mesmo movimento de reavaliação, a tela percorre os atendimentos do órgão filho e apaga os que
estão sem segmento, sem refeição ou sem quantidade de pessoas — inclusive o do par que ela acabou de
reavaliar, quando a quantidade registrada nele é zero. É uma limpeza: o atendimento que não
representa ninguém deixa de existir.

### RN-18 — Nada acontece sem a segurança do perfil, da rota e da operação

Antes de exibir, a tela leva a sessão à segurança do perfil (o cadastro de telas); a passagem de
conferência leva o contexto da sessão à segurança da rota e à da operação (a **alteração**, que é a
operação desta tela). Se qualquer uma não devolver OK, o processamento é abandonado: nada é
exibido, nada é conferido, nada é gravado e nada é auditado. A liberação da alteração é conferida
uma vez, na passagem de conferência, e não se repete na de gravação.

[?] A permissão é conferida na passagem de conferência e não se repete na que grava: se ela mudasse
entre as duas, a gravação não a reconferiria. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Percentual do atendimento por órgão filho, segmento e tipo de refeição

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C272T

  Cenário: O percentual é mantido para o órgão filho, o segmento e a refeição
    Dado que consultei um segmento de um órgão filho da minha secretaria
    Quando registro um percentual para uma refeição desse segmento
    Então o percentual fica registrado para aquele órgão filho, aquele segmento e aquela refeição
    E ficam com ele a minha matrícula e a data do dia
    E a coordenação regional escolar gravada é a do cadastro do órgão
    E não há campo para escolher outra secretaria

  Cenário: A tela lista as refeições do segmento com o percentual de cada uma
    Dado que a minha secretaria tem um órgão filho com um segmento que tem refeições
    Quando consulto esse segmento
    Então vejo as refeições do segmento, uma por linha, com o código, a descrição e o percentual de cada uma
    E vejo o nome do órgão filho, a descrição do tipo de órgão, a descrição do segmento e o indicador de creche
    E vejo a data do sistema
    E a lista mostra até onze refeições

  Cenário: A linha da refeição de referência posiciona a lista
    Dado que consultei um segmento com várias refeições
    Quando informo na linha de referência uma refeição que o segmento tem
    Então a lista recomeça por essa refeição
    E, quando a página se completa, a linha de referência passa a mostrar a refeição da última linha

  Cenário: Refeição de referência fora do cadastro de refeições
    Dado que consultei um segmento com várias refeições
    Quando informo na linha de referência uma refeição que não está no cadastro de refeições
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

  Cenário: Consulta sem o órgão informado
    Dado que estou na tela com a opção de consulta
    Quando deixo o órgão filho em branco e confirmo
    Então vejo a mensagem "* Informe o orgao *"
    E o cursor volta ao campo do órgão
    E nada é lido nem gravado

  Cenário: Consulta de um órgão inativo
    Dado que estou na tela com a opção de consulta
    Quando informo um órgão filho cadastrado como inativo
    Então vejo a mensagem "* Orgao cadastrado como inativo *"
    E o cursor volta ao campo do órgão
    E nada é lido nem gravado

  Cenário: Consulta de um órgão de outra secretaria
    Dado que estou na tela com a opção de consulta
    Quando informo um órgão filho de outra secretaria
    Então vejo a mensagem "* Orgao nao pertence a esta secretaria *"
    E o cursor volta ao campo do órgão
    E nada é lido nem gravado

  Cenário: Consulta de um órgão de outra coordenação
    Dado que estou na tela com a opção de consulta
    Quando informo um órgão filho de uma coordenação a que não tenho acesso
    Então vejo a mensagem "* Usuario sem acesso ao grupo deste orgao *"
    E o cursor volta ao campo do órgão
    E nada é lido nem gravado

  Cenário: Consulta de outro órgão filho por quem está preso ao seu
    Dado que a minha sessão já traz um órgão filho
    Quando informo outro órgão filho
    Então vejo a mensagem "* Usuario sem acesso a outro orgao *"
    E o cursor volta ao campo do órgão
    E nada é lido nem gravado

  Cenário: Consulta de um segmento não cadastrado
    Dado que estou na tela com a opção de consulta
    Quando informo um segmento que não existe no cadastro de segmentos
    Então vejo a mensagem "* Segmento nao cadastrado *"
    E o cursor volta ao campo do segmento
    E nada é lido nem gravado

  Cenário: Consulta de um segmento que não é do órgão
    Dado que estou na tela com a opção de consulta
    Quando informo um segmento que não está ligado àquele órgão filho
    Então vejo a mensagem "* Orgao nao cadastrado neste segmento *"
    E o cursor volta ao campo do segmento
    E nada é lido nem gravado

  Cenário: Trocar de órgão passa ao primeiro segmento dele
    Dado que consultei um órgão filho com um segmento
    Quando informo outro órgão filho e um segmento qualquer
    Então a tela adota o primeiro segmento cadastrado para o novo órgão
    E o segmento que eu havia informado é descartado

  Cenário: Alteração de um órgão ou segmento que não foram consultados
    Dado que estou na tela com a opção de alteração
    E informo um órgão filho ou um segmento diferente do que consultei
    Quando confirmo
    Então vejo a mensagem "* Consulte antes de atualizar *"
    E o cursor volta ao campo do órgão
    E nada é gravado

  Cenário: Percentual acima de cem
    Quando informo um percentual maior que cem
    Então vejo a mensagem "* Percentual maximo invalido *"
    E o cursor volta ao campo do percentual
    E nada é gravado

  Cenário: Percentual em branco conta como zero
    Dado que uma das refeições listadas já tem percentual registrado
    Quando deixo o percentual dessa linha em branco, com a opção de alteração, e confirmo
    Então o percentual registrado deixa de existir
    E a operação deixa rastro na auditoria
    E o atendimento daquele par de segmento e refeição é reavaliado

  Cenário: Alteração inclui o percentual de uma refeição que não tinha
    Dado que uma das refeições listadas não tem percentual registrado para o órgão
    Quando informo um percentual de um a cem e confirmo
    Então o percentual dessa refeição fica registrado
    E a data do dia e a minha matrícula ficam no registro
    E a operação deixa rastro na auditoria

  Cenário: Alteração troca o percentual de uma refeição
    Dado que uma das refeições listadas já tem um percentual registrado
    Quando informo outro percentual e confirmo
    Então o percentual dessa refeição passa a ser o informado
    E a matrícula e a data do primeiro registro continuam no cadastro
    E a operação deixa rastro na auditoria

  Cenário: Alteração com o mesmo percentual não muda nada
    Dado que uma das refeições listadas já tem um percentual registrado
    Quando informo o mesmo percentual e confirmo
    Então nada é gravado
    E nenhum atendimento é reavaliado por causa dessa refeição

  Cenário: A consulta não grava nada
    Dado que estou na tela com a opção de consulta e um segmento consultado
    Quando percorro a lista e confirmo
    Então nenhum percentual é incluído, trocado ou apagado
    E nenhum atendimento é reavaliado ou apagado
    E nenhum registro de auditoria é escrito

  Cenário: Passagem para o novo segmento
    Dado que estou consultando um segmento
    Quando aciono a passagem para o novo segmento
    Então a tela passa ao segmento seguinte cadastrado
    E, se não houver seguinte, volta ao primeiro segmento cadastrado
    E nada é gravado nem reavaliado nessa passagem

  Cenário: Passagem para o novo segmento na alteração
    Dado que estou na tela com a opção de alteração e um segmento consultado
    Quando aciono a passagem para o novo segmento e confirmo
    Então a tela passa ao segmento seguinte
    E nada é gravado

  Cenário: O atendimento acima do que o percentual permite fica inativo
    Dado que o órgão tem mês de referência e um total apurado para o segmento
    E o atendimento do par de segmento e refeição tem quantidade maior que o total permitido pelo percentual
    Quando gravo esse percentual
    Então o atendimento daquele par é marcado como inativo
    E ficam nele a minha matrícula e a data do dia
    E a mudança deixa rastro na auditoria

  Cenário: O atendimento dentro do que o percentual permite fica ativo
    Dado que o órgão tem mês de referência e um total apurado para o segmento
    E o atendimento do par de segmento e refeição tem quantidade menor ou igual ao total permitido
    Quando gravo esse percentual
    Então o atendimento daquele par é marcado como ativo
    E a marcação em si não deixa registro de auditoria

  Cenário: Órgão creche toma o total pelo grupo de segmentos
    Dado que o órgão é creche e tem mês de referência com total apurado
    Quando gravo o percentual de uma refeição de um segmento
    Então a comparação do atendimento daquele par usa o total do grupo de segmentos a que o segmento pertence
    E não somente o total apurado daquele segmento

  Cenário: Sem mês de referência não há reavaliação
    Dado que o órgão não tem mês de referência cadastrado
    Quando gravo um percentual
    Então o percentual fica registrado
    E nenhum atendimento é reavaliado
    E nenhum atendimento é apagado

  Cenário: Os atendimentos vazios do órgão são apagados
    Dado que o órgão tem mês de referência cadastrado
    E tem atendimentos sem segmento, sem refeição ou sem quantidade de pessoas
    Quando gravo um percentual de uma refeição do órgão
    Então esses atendimentos deixam de existir

  Cenário: Toda mudança do percentual deixa rastro na auditoria
    Dado que incluí, troquei ou apaguei o percentual de uma refeição
    Quando a gravação termina
    Então existe um registro de auditoria com o cadastro auditado, a operação e os valores anterior e posterior
    E com a matrícula, a coordenação regional escolar, o terminal, a data e a hora
    E o número do processo no rastro é o código do órgão filho

  Cenário: Operação sem autorização
    Dado que a minha sessão não passa na segurança do perfil, da rota ou da alteração
    Quando tento manter os percentuais
    Então a tela volta sem conferir os dados
    E nada é gravado nem reavaliado
```
