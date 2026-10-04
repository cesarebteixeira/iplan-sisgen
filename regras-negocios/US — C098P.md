# US — C098P — Pedir a emissão do relatório de permissões de contrato

## Estória

Como **servidor de CRE**, quero **pedir a emissão do relatório de permissões de
contrato informando a permissão de origem e a de destino**, para que **eu receba o
relatório das duas permissões sem ter de levantar esses dados por fora do sistema**.

O relatório sai de um recorte e vai para outro: quem pede aponta a permissão de origem
e a de destino, cada uma com a sua coordenação regional escolar, o seu tipo de
contrato, o seu grupamento e a sua data limite. O sistema só registra o pedido depois
de conferir que as duas permissões existem no cadastro exatamente como foram
informadas. Sem essa conferência a emissão correria com um parâmetro que não
corresponde a nenhuma permissão cadastrada, e o relatório sairia vazio ou apontando
para a permissão errada. Pelo mesmo motivo não podem coexistir dois pedidos do mesmo
relatório para o mesmo grupo: enquanto um estiver pendente, o segundo é recusado.

## Contexto

Jornada S000M → C000M → C050M → C030M → C031M → C098P.

Ator: servidor de CRE — informa a permissão de origem e a de destino e pede a emissão
do relatório.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. O `C000M`, o `C050M` e o `C030M` são menus
e não gravam nada; o `C031M` é o menu de relatórios, e é ele que diz ao sistema qual
relatório está sendo pedido. A `C098P` não abre por opção de menu: o `C031M`
**encadeia** nela, passando o relatório escolhido na sessão. O que a `C098P` usa da
sessão — matrícula, tipo de órgão, coordenação regional escolar, impressora e estação —
é o que a entrada deixou.

As regras abaixo são só as da tela desta jornada.

---

## Regras de negócio

### RN-01 — A tela só atende o relatório a que foi amarrada

A `C098P` é a tela de parâmetros de um relatório: ela recebe da sessão o código do
relatório escolhido no menu e só segue adiante quando esse código é o do relatório
dela. Com qualquer outro código, a tela abre igual, mas nada é conferido nem
registrado, e o operador não vê aviso nenhum — a tela volta sem fazer nada.

O mesmo menu de relatórios (`C031M`) tem duas opções que abrem esta tela: uma leva o
código do relatório desta tela e a outra leva o código de **outro** relatório, este
atendido por outra tela de parâmetros do sistema. Por essa segunda, nada do que o
operador informar será processado.

[?] Ou aquela opção do menu deveria abrir a tela de parâmetros daquele outro
relatório, ou esta tela deveria atender os dois. Do jeito que está, o pedido por
aquela opção é inalcançável: a tela aparece e não faz nada, sem mensagem. O acervo
desta jornada não diz qual dos dois era o pretendido. Pergunta ao site.

### RN-02 — O pedido tem dois blocos: a permissão de origem e a de destino

Cada bloco identifica uma permissão de contrato pelos mesmos quatro dados: a
coordenação regional escolar (o grupo), o tipo de contrato, o grupamento e a data
limite — dia, mês e ano. O bloco de destino tem ainda a secretaria. O grupamento é um
só para os dois blocos: não há na tela um grupamento próprio do destino.

Os campos da origem aparecem descritos por nomes de negócio — coordenação regional
escolar, grupamento, dia limite, mês limite e ano limite —, e os do destino, pelos
próprios nomes internos dos campos. Fora dos blocos, a tela mostra a data do sistema e
a descrição do tipo de órgão de quem opera.

[?] O texto dos rótulos do bloco de destino não está no programa — o que o operador lê
ali vem da máscara da tela, que não faz parte do acervo lido. Pergunta ao site.

### RN-03 — O grupo da origem é limitado ao grupo de quem opera

Se o cadastro de quem opera traz uma coordenação regional escolar, o grupo informado
na origem tem de ser essa mesma; informar outro é recusa, com
**\* Usuario sem acesso a outro grupo \***. Se quem opera não tem coordenação no
cadastro, essa conferência não recusa nada e qualquer grupo passa. O grupo do destino
não sofre essa limitação.

### RN-04 — O grupo da origem é obrigatório

Sem o grupo da origem o pedido não anda: a recusa é **\* Informe o grupo - DE \***,
com o cursor de volta ao campo.

### RN-05 — Um pedido de cada vez por órgão, grupo e relatório

Antes de conferir os parâmetros do pedido, o sistema procura um pedido já registrado
para o mesmo tipo de órgão, o mesmo grupo e o mesmo relatório. Achando, recusa com
**\* Relatorio ja esta em processamento. Aguarde. \*** e não confere mais nada. A
procura é por qualquer pedido, sem olhar a situação dele nem a marca de exclusão.

[?] Como o sistema não olha a situação do pedido, um pedido antigo que continue na
base bloqueia todos os pedidos seguintes daquele grupo e daquele relatório, e a tela
não mostra como tirá-lo dali. Quem remove esses pedidos está fora desta jornada.
Pergunta ao site.

### RN-06 — Na origem, o tipo de contrato, o grupamento e o dia limite são obrigatórios

São três recusas distintas, nesta ordem: **\* Informe o Tipo Contrato - DE \***,
**\* Informe o grupamento \*** e
**\* Informe a data limite da permissao - DE \***, cada uma com o cursor de volta ao
campo.

[?] Só o dia é exigido: o mês e o ano limite podem ficar em branco e o pedido segue
para a conferência da permissão, onde uma data incompleta não encontra nada. Se a data
limite é para ser uma data inteira, a conferência não a exige. Pergunta ao site.

### RN-07 — A permissão de origem tem de estar cadastrada, exatamente como informada

O sistema procura no cadastro das permissões de contrato (`C061T`) a permissão do tipo
de órgão de quem opera, com o grupo, a data limite (dia, mês e ano), o tipo de
contrato e o grupamento informados; a classe, a subclasse e o gênero da permissão
entram zerados, porque a tela não os informa. Permissão marcada como excluída não é
encontrada. Não achando, a recusa é **\* Permissao nao cadastrada - DE \***, com o
cursor de volta ao campo do dia limite.

### RN-08 — No destino, a secretaria, o grupo, o tipo de contrato e o dia limite são obrigatórios

São quatro recusas, nesta ordem: **\* Informe a Secretaria - PARA \***,
**\* Informe o grupo - PARA \***, **\* Informe o Tipo Contrato - PARA \*** e
**\* Informe a data limite da permissao - PARA \***, cada uma com o cursor de volta ao
campo.

### RN-09 — A permissão de destino tem de estar cadastrada, com o mesmo grupamento da origem

A procura é no mesmo cadastro, agora pela secretaria, pelo grupo, pela data limite e
pelo tipo de contrato informados e pelo grupamento da origem — o destino não tem
grupamento próprio. Não achando, a recusa é **\* Permissao nao cadastrada - PARA\***
(a mensagem sai assim mesmo, sem o espaço antes do asterisco), com o cursor de volta
ao campo do dia limite do destino.

[?] Como o grupamento do destino é o da origem, um destino cadastrado com outro
grupamento é recusado como se não existisse. Se a intenção era comparar grupamentos
diferentes, falta um campo na tela. Pergunta ao site.

### RN-10 — Passando nas conferências, o pedido é numerado, registrado e entregue à emissão

O sistema toma o próximo número de pedido (o seguinte ao último já registrado),
registra o pedido com o relatório, o tipo de órgão, o grupo, a data do pedido, a
matrícula, a estação e a impressora da sessão, e deixa a situação do pedido em branco;
o e-mail do cadastro de quem opera vai junto nos parâmetros, assim como o código da
tela que responde pela impressão do relatório. Em seguida monta o pedido de execução
do relatório e o entrega ao serviço que dispara a emissão.

[?] O número do pedido é o último registrado mais um, lido sem travamento: dois
pedidos simultâneos podem receber o mesmo número, e o acervo não diz o que acontece
nesse caso. Pergunta ao site.

[?] Há um caminho em que o pedido fica registrado e a execução não é entregue —
reservado a um ambiente diferente do de origem, que o próprio acervo fixa no valor
normal. Se esse caminho ainda tem uso, o acervo não diz. Pergunta ao site.

[?] A tela não mostra mensagem de confirmação depois de registrar o pedido; o que o
operador vê ao voltar não está no programa. Pergunta ao site.

[?] A tela entrega a execução do relatório e não acompanha o resultado: o que o serviço
de relatórios faz com o pedido — se imprime, se guarda, se devolve erro — não está no
acervo lido. Pergunta ao site.

### RN-11 — A tela só escreve o pedido; o cadastro das permissões é apenas lido

Nenhuma permissão de contrato é alterada ou apagada por esta tela: o cadastro das
permissões é só lido. O único registro que ela cria é o do pedido de relatório
(`S040T`), o mesmo cadastro usado pelas outras telas de parâmetros de relatório do
sistema. Esse pedido não deixa rastro no cadastro de auditoria (`A010T`), que esta tela
nem enxerga.

[?] Se a ausência de rastro é intencional: quem pediu, quando e com que parâmetros não
fica registrado para auditoria. Pergunta ao site.

### RN-12 — Falha de banco interrompe o pedido

Toda leitura e a gravação testam o erro do banco; havendo erro, a transação é
interrompida com a mensagem de erro do sistema e o pedido não é considerado
registrado.

---

## Cenários BDD

```gherkin
Funcionalidade: Pedir a emissão do relatório de permissões de contrato

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela C098P

  Cenário: RN-01 e RN-02 — abrir a tela pelo relatório dela
    Dado que escolhi no menu de relatórios a opção que traz o relatório desta tela
    Quando a tela abre
    Então vejo os dois blocos de parâmetros — a permissão de origem e a de destino
    E vejo a data do sistema e a descrição do tipo de órgão da minha sessão
    E nada é registrado

  Cenário: RN-01 — abrir a tela pela opção que traz o código de outro relatório
    Dado que escolhi a outra opção do menu de relatórios, que abre esta mesma tela com o código de outro relatório
    Quando confirmo os parâmetros
    Então nada é conferido e nada é registrado
    E não vejo mensagem nenhuma

  Cenário: RN-03 — grupo de origem fora do meu grupo
    Dado que o meu cadastro tem coordenação regional escolar
    Quando informo outra coordenação na origem
    Então vejo "* Usuario sem acesso a outro grupo *"

  Cenário: RN-03 — sem coordenação no meu cadastro, o grupo da origem é livre
    Dado que o meu cadastro não tem coordenação regional escolar
    Quando informo qualquer grupo na origem
    Então essa conferência não me recusa

  Cenário: RN-04 — grupo de origem em branco
    Quando confirmo sem informar o grupo da origem
    Então vejo "* Informe o grupo - DE *"
    E o cursor volta para o campo

  Cenário: RN-05 — já existe pedido para o órgão, o grupo e o relatório
    Dado que já existe um pedido registrado para o meu tipo de órgão, o grupo informado e este relatório
    Quando confirmo
    Então vejo "* Relatorio ja esta em processamento. Aguarde. *"
    E nada é registrado

  Cenário: RN-06 — tipo de contrato da origem em branco
    Quando confirmo sem informar o tipo de contrato da origem
    Então vejo "* Informe o Tipo Contrato - DE *"

  Cenário: RN-06 — grupamento em branco
    Quando confirmo sem informar o grupamento
    Então vejo "* Informe o grupamento *"

  Cenário: RN-06 — dia limite da origem em branco
    Quando confirmo sem informar o dia limite da origem
    Então vejo "* Informe a data limite da permissao - DE *"

  Cenário: RN-06 e RN-07 — dia limite informado sem mês e sem ano
    Dado que informo o dia limite da origem e deixo o mês e o ano em branco
    Quando confirmo
    Então vejo "* Permissao nao cadastrada - DE *"

  Cenário: RN-07 — permissão de origem não cadastrada
    Quando informo um grupo, uma data limite, um tipo de contrato e um grupamento que não estão cadastrados juntos
    Então vejo "* Permissao nao cadastrada - DE *"
    E nada é registrado

  Cenário: RN-07 — permissão de origem marcada como excluída
    Quando informo uma permissão que está marcada como excluída no cadastro
    Então vejo "* Permissao nao cadastrada - DE *"

  Cenário: RN-08 — secretaria do destino em branco
    Quando confirmo sem informar a secretaria do destino
    Então vejo "* Informe a Secretaria - PARA *"

  Cenário: RN-08 — grupo do destino em branco
    Quando confirmo sem informar o grupo do destino
    Então vejo "* Informe o grupo - PARA *"

  Cenário: RN-08 — tipo de contrato do destino em branco
    Quando confirmo sem informar o tipo de contrato do destino
    Então vejo "* Informe o Tipo Contrato - PARA *"

  Cenário: RN-08 — dia limite do destino em branco
    Quando confirmo sem informar o dia limite do destino
    Então vejo "* Informe a data limite da permissao - PARA *"

  Cenário: RN-09 — permissão de destino não cadastrada
    Quando informo, para o destino, uma combinação de secretaria, grupo, data limite e tipo de contrato que não está cadastrada
    Então vejo "* Permissao nao cadastrada - PARA*"
    E nada é registrado

  Cenário: RN-09 — permissão de destino com outro grupamento
    Dado que o destino está cadastrado com um grupamento diferente do da origem
    Quando confirmo o pedido
    Então vejo "* Permissao nao cadastrada - PARA*"

  Cenário: RN-10 e RN-11 — pedir a emissão com as duas permissões cadastradas
    Dado que a permissão de origem e a de destino existem, exatamente como informadas
    E não há pedido em andamento para o órgão, o grupo e o relatório
    Quando confirmo
    Então o pedido é registrado com um número, a minha matrícula, a estação e a impressora da sessão
    E a situação do pedido fica em branco
    E a execução da emissão é entregue ao serviço de relatórios
    E nenhuma permissão de contrato é alterada

  Cenário: RN-11 — recusa não registra nada
    Dado que confirmo um pedido com um parâmetro em falta ou com uma permissão não cadastrada
    Quando a tela recusa
    Então nenhum pedido é registrado
    E nenhuma permissão de contrato é alterada

  Cenário: RN-12 — falha de banco durante o registro do pedido
    Dado que a leitura ou a gravação falha no banco
    Quando confirmo o pedido
    Então a transação é interrompida com a mensagem de erro do sistema
    E o pedido não é considerado registrado
```
