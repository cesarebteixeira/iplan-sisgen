# US — C664T — Prorrogar a data limite das permissões de contrato das coordenações regionais

## Estória

Como **servidor de CRE**, quero **informar o contrato, o grupamento de licitação, o período atual da permissão e a nova data limite, apontando as coordenações regionais que devem ser alcançadas, e confirmar a prorrogação**, para que **as permissões daqueles grupamentos passem a valer até a nova data, sem que ninguém tenha de corrigi-las uma a uma**.

A permissão de contrato é o registro que autoriza a compra de um grupamento de licitação, por um período, a uma coordenação regional escolar; é a data limite dela que faz o pedido da escola parar de ser aceito. Quando o prazo do contrato é estendido, essa data tem de ser estendida em todas as permissões dos grupamentos atingidos — sem isso, o fornecimento é interrompido na data antiga, mesmo com o contrato ainda vigente. Esta tela recebe a nova data uma vez, confere o que já está cadastrado para os grupamentos e as coordenações regionais que o servidor indicar e entrega a atualização de todas essas permissões ao processamento, que é quem de fato grava. Não é uma tela de cadastro.

## Contexto

Jornada S000M → C000M → C050M → C664M → C664T.
Ator: servidor de CRE — informa o contrato, o grupamento, o período atual da permissão, a nova data limite e as coordenações regionais atingidas, e confirma a prorrogação.

A entrada — o `LOGON` e o menu principal `S000M` — está em `Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de negócio. Nem o C000M, nem o C050M, nem o C664M gravam nada do que esta tela faz, e o C664M apenas abre esta tela pelo nome, sem lhe passar registro nem operação; por isso o modo desta tela não vem de quem a chamou. Esta tela não encadeia em outra: a única saída dela é ela mesma, reposta para um novo pedido.

O cadastro das permissões de contrato e o dos períodos das permissões são mantidos em outras telas do sistema. Esta não é nenhuma delas: ela lê os dois cadastros para conferir o que foi informado, e o que grava é a requisição do processamento.

---

## Regras de negócio

### RN-01 — A tela não altera o cadastro: registra o pedido de atualização e entrega o processamento

A tela enxerga **seis cadastros** — os títulos das telas, a descrição do tipo de órgão, os períodos das permissões do contrato, as permissões de contrato, os funcionários e as requisições de processamento — e, para cada um deles, o sistema traz prontas uma operação de gravar e uma de apagar. Nesta tela, a **única gravação executada é a da requisição do processamento**: as permissões de contrato e os períodos das permissões não são gravados aqui, e nenhuma exclusão é executada. Quem estende a data limite é o processamento que a tela entrega no fim, com os parâmetros que ela monta.

[?] O processamento entregue não tem fonte nos arquivos desta jornada: o programa da relação que a tela dispara não faz parte do lote lido. O que ele altera em cada permissão — se a data limite, a data limite inicial ou os períodos — e o que ele faz com o aviso de que a prorrogação passa de cinco anos não podem ser afirmados daqui. Pergunta ao site.

### RN-02 — A tela abre sempre na alteração

Aberta, a tela repõe a operação de alteração antes de qualquer leitura: quem a chamou não escolhe a operação. Se a operação que chegar não for a alteração, o sistema recusa com **\* Operacao nao disponivel. Use ALT \***, devolve o cursor ao campo da operação e encerra sem ler nem registrar nada.

[?] A mensagem manda usar "ALT", mas a conferência compara a operação informada com o código interno da alteração — o mesmo valor que a própria tela escreve nesse campo. Nenhum valor "ALT" existe no acervo lido. Ou o formulário traduz o mnemônico antes de enviar, ou a mensagem está desalinhada da conferência. Pergunta ao site; não concluo qual dos dois.

[?] Como a tela repõe a alteração sozinha, a recusa só é alcançável por quem chegue com outra operação já gravada no contexto — caminho que nenhuma tela desta jornada usa. Se a recusa é trecho sem uso, o acervo não diz. Pergunta ao site.

### RN-03 — O acesso à tela e o perfil da alteração

Ao montar a tela, o sistema confere a matrícula e a tela no cadastro de acesso. Na conferência do que foi informado, confere a operação no perfil de acesso daquela tela e exige o flag próprio da alteração. Sem acesso, a recusa é **\* Acesso negado para esta matricula \***; sem a tela cadastrada, **\* Tela nao disponivel \***; sem o flag da alteração, **\* Acesso negado para esta operacao \***. Em qualquer dos casos nada é registrado.

### RN-04 — O que a tela pede, e o que ela repõe

O servidor informa o **tipo de contrato**, o **grupamento de licitação** — ou o código **9999**, que vale por todos —, o **período atual da permissão** (o dia, o mês e o ano do início e o dia, o mês e o ano da data limite), a **nova data do prazo** (dia, mês e ano) e até **doze coordenações regionais**. O tipo de órgão não se digita: é o da secretaria do vínculo, vem da sessão e entra na identificação de tudo o que a tela lê. O início do intervalo da prorrogação também não se digita — a tela o repõe a partir da data limite informada, e o que o servidor tiver digitado ali é descartado; a única data que ele de fato escolhe é a nova. Cada coordenação regional informada é um grupamento a prorrogar; coordenação deixada em branco é pulada.

[?] O rótulo que a tela mostra para as doze coordenações regionais e para as partes do intervalo da prorrogação não está no material: só **oito** rótulos desta tela estão mapeados, e os demais campos aparecem pelo nome interno. Pergunta ao site, para não dar nome errado a esses campos.

### RN-05 — Cada campo obrigatório que falta tem a sua recusa própria

Antes de ler qualquer permissão, a tela exige, nesta ordem, o tipo de contrato, o grupamento, o **dia** do início do período, o **dia** da data limite e o **dia** da nova data, e ao menos uma coordenação regional. Cada falta tem a sua mensagem: **\* Informe o tipo de contrato \***, **\* Informe grupamento ou 9999 para todos \***, **\* Informe data inicial da permissao \***, **\* Informe data limite da permissao \***, **\* Informe nova data para prorrogacao \*** e **\* Informe grupos para prorrogacao \***. A nova data **igual** à data limite informada recebe a mesma mensagem de "informe nova data". Em todas, o cursor volta ao campo que falta — no caso dos grupos, à primeira coordenação regional — e nada é lido nem registrado. Só o dia é exigido nas três datas: o mês e o ano não têm exigência própria.

### RN-06 — Nenhum campo é texto livre

Os **vinte e seis** campos com rótulo do formulário — o tipo de contrato, o grupamento, as três partes do início do período, as três partes da data limite, as três partes do início do intervalo da prorrogação, as três partes da nova data e as doze coordenações regionais — passam pela edição numérica antes de qualquer consulta ao cadastro: o que não for número é recusado no próprio campo. **Vinte e três** deles devolvem o cursor ao campo recusado; as três partes do início do intervalo da prorrogação são as exceções.

[?] O que o servidor vê quando a edição numérica recusa não está no material: a rotina chamada é uma entrada de biblioteca e o corpo dela não faz parte dos fontes desta jornada. Também não é possível afirmar o efeito de as três partes do início do intervalo não terem posição de retorno de cursor. Pergunta ao site.

### RN-07 — A nova data não pode ser anterior ao início da permissão

Achada a permissão de contrato do grupamento e da coordenação regional, a tela compara a nova data com a **data inicial daquela permissão**: sendo anterior, recusa com **\* Data menor que data inicial da permissao \***, com o cursor de volta à primeira coordenação regional, e nada é registrado.

### RN-08 — O prazo da prorrogação é comparado com o período original da permissão

A tela mede a prorrogação — da data limite informada até a nova data — e mede o período original da permissão — da data inicial até a data limite inicial registrada nela — e recusa com **\* Periodo prorrogacao > periodo inicial permiss \*** quando o prazo pretendido não cabe no período original.

[?] A conta escrita e a mensagem não fecham. As duas medidas são montadas como "a data mais antiga menos a data mais recente, mais um", e a recusa é disparada quando a medida da prorrogação é **maior** que a do período original — o que, com as duas medidas montadas da mesma forma, corresponde à prorrogação **menor**, o inverso do que a mensagem diz. Ou a rotina de conversão de data, que é uma entrada de biblioteca e não faz parte dos fontes desta jornada, devolve os dias em outra ordem, ou a comparação está trocada. Pergunta ao site; não escolho um dos dois.

### RN-09 — A nova data não pode cruzar outro período já cadastrado

Quando a nova data ultrapassa a data limite atual, a tela percorre os períodos cadastrados para aquele contrato e aquela coordenação regional e confere se o intervalo resultante — do início da permissão até a nova data — cruza algum período que não seja o da própria permissão. Cruzando, recusa com **\* Ja existe permissao neste intervalo \***, com o cursor de volta à coordenação regional, e nada é registrado.

[?] A leitura dos períodos leva a **data inicial informada** na posição em que a identificação do período guarda a **data limite**, e o grupamento vai zerado. O que essa posição significa no cadastro não está no material; se ela não for a data limite, o efeito desta conferência muda. Pergunta ao site.

### RN-10 — Não se encurta o prazo quando já existem pedidos

Quando a nova data é **anterior** à data limite atual, a tela percorre as permissões daquele grupamento e daquela coordenação regional e verifica se alguma tem **pedidos pendentes** em quantidade maior que zero. Havendo, recusa com **\* Nao diminua periodo. Ja existem pedidos \***, com o cursor de volta à coordenação regional, e nada é registrado.

### RN-11 — O grupamento tem de existir no contrato, e a permissão também

Para cada coordenação regional informada, a tela procura os períodos cadastrados naquele contrato. Não havendo nenhum período cujo início seja o início de período informado, recusa com **\* Grupo nao cadastrado nesta permissao \***, com o cursor naquela coordenação regional, e nada é registrado. Havendo períodos, a tela procura a permissão de cada grupamento encontrado: não existindo, aquele grupamento é **pulado em silêncio**, sem mensagem e sem prorrogação.

[?] A mensagem fala em "grupo não cadastrado nesta permissão", mas o que a dispara é **não haver período** para aquela coordenação regional no contrato; e a permissão ausente, essa sim, não gera mensagem nenhuma. O que o site chama de "grupo" — a coordenação regional, o par coordenação e grupamento, ou o próprio período — não está no material. Pergunta ao site.

### RN-12 — Um pedido por vez

Depois da confirmação e antes de registrar, a tela procura uma requisição de processamento **da mesma relação**. Existindo, recusa com **\* Relatorio em processamento. Aguarde. \***, posiciona o cursor no campo da resposta e nada é registrado.

[?] A procura não examina a situação da requisição encontrada: basta haver uma requisição daquela relação para a recusa. Se requisições já processadas continuam bloqueando novos pedidos, ou se a leitura com o número da requisição zerado só alcança as pendentes, depende do posicionamento do dicionário de dados, cujo efeito exato não está no material. Pergunta ao site.

### RN-13 — A confirmação é pedida em duas perguntas, e a segunda só quando a prorrogação passa de cinco anos

Passadas as conferências, a tela repete o formulário com a pergunta **Atualiza cadastro da permissao <S/N>?** e espera a resposta em campo próprio. Se a nova data ultrapassar **cinco anos** contados do início da permissão, acrescenta a segunda pergunta — **Confirma prorrog excede prazo de 5 anos de vigencia do contrato <S/N>:** — e as duas respostas têm de ser **S**; não sendo as duas, nada é registrado. Quando a prorrogação **não** passa dos cinco anos, a segunda pergunta não é feita e a resposta dela é assumida como afirmativa pela própria tela. Os cinco anos são medidos em **1.825 dias** somados à data inicial da permissão.

[?] Responder **N** não cancela: a tela limpa as respostas, refaz as conferências e **volta a pedir a mesma confirmação**. Não há, no caminho lido, um desfecho que encerre a operação com a resposta negativa. Pergunta ao site.

### RN-14 — Mudar qualquer dado entre a pergunta e a resposta refaz a conferência

Com as respostas em S, a tela compara os **vinte e seis** dados informados — o tipo de contrato, o grupamento, as três partes do início do período, as três da data limite, as três do início do intervalo da prorrogação, as três da nova data e as doze coordenações regionais — com o que guardou quando a pergunta foi feita. Mudando qualquer um deles, a confirmação é descartada, as conferências são refeitas e a pergunta é repetida, sem registrar nada.

### RN-15 — O pedido fica registrado com o número, o servidor, a estação e os parâmetros da prorrogação

Confirmado o pedido, a tela lê o **e-mail do servidor** no cadastro de funcionários, toma o **número seguinte** ao da última requisição registrada e grava a requisição com o tipo de órgão da sessão, a matrícula, a estação, o dia, o mês e o ano. Em seguida entrega ao processamento os parâmetros da prorrogação — o tipo de órgão, o tipo de contrato, o grupamento, o início do período, a data limite, as três partes do início do intervalo, as três da nova data, as doze coordenações regionais, a matrícula e o aviso de que a prorrogação passa de cinco anos — e o servidor vê **\* Cadastro sendo atualizado \***, com a tela reposta para um novo pedido.

[?] O material não permite afirmar como o número da requisição é obtido: a leitura que o antecede usa um número sentinela deixado na sessão e uma marca de posicionamento cujo significado não está no corpus, e o número sai do que estiver no registro de trabalho mais um. Se dois pedidos saírem na mesma sessão, não posso afirmar que o número não repita. Pergunta ao site.

[?] O e-mail do servidor é lido e **descartado**: ele não entra na requisição nem nos parâmetros entregues ao processamento. Se o e-mail devia acompanhar o pedido, o caminho o perde. Pergunta ao site.

[?] Não é possível afirmar que a entrega do processamento dependa do resultado da gravação da requisição: a conferência que a antecede testa uma situação que a própria rotina de gravação deixa em branco imediatamente antes de gravar, e o material não diz o que essa situação significa nem quem a repõe. Se a intenção era não entregar o processamento quando a requisição não fosse aceita — por exemplo, por número repetido —, o caminho lido não garante isso. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Prorrogar a data limite das permissões de contrato das coordenações regionais

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E a minha sessão carrega o tipo de órgão, a coordenação regional, a matrícula, a estação e a data do sistema
    E tenho acesso à tela C664T

  Cenário: Abrir a tela
    Quando abro a tela C664T
    Então ela se apresenta na operação de alteração
    E vejo a descrição do tipo de órgão da sessão e a data do sistema
    E nada foi registrado

  Cenário: Prorrogar o prazo dentro dos cinco anos
    Dado que existe permissão de contrato para o tipo de contrato, o grupamento e o período que informei, nas coordenações regionais que indiquei
    E a nova data não é anterior ao início da permissão, cabe no período original dela e não cruza outro período cadastrado
    Quando informo os dados e respondo S à pergunta de atualização do cadastro
    Então a requisição do processamento é registrada com o número seguinte
    E o processamento recebe os parâmetros da prorrogação
    E vejo "* Cadastro sendo atualizado *"

  Cenário: A tela não altera o cadastro das permissões
    Dado que confirmei a prorrogação
    Então nenhuma permissão de contrato é incluída, alterada ou excluída
    E nenhum período de permissão é incluído, alterado ou excluído
    E o que fica registrado é a requisição do processamento

  Cenário: Operação diferente da alteração
    Quando a transação chega com uma operação que não é a de alteração
    Então vejo "* Operacao nao disponivel. Use ALT *"
    E o cursor volta ao campo da operação
    E nada é registrado

  Cenário: Sem acesso à tela ou sem o perfil da alteração
    Dado que o meu perfil não tem o acesso à tela ou o flag da alteração
    Quando envio a tela
    Então vejo "* Acesso negado para esta matricula *", "* Tela nao disponivel *" ou "* Acesso negado para esta operacao *"
    E nada é registrado

  Cenário: Campo obrigatório que falta
    Quando deixo de informar o tipo de contrato, o grupamento, o dia do início do período, o dia da data limite ou o dia da nova data, ou não informo nenhuma coordenação regional
    Então vejo a mensagem daquele campo: "* Informe o tipo de contrato *", "* Informe grupamento ou 9999 para todos *", "* Informe data inicial da permissao *", "* Informe data limite da permissao *", "* Informe nova data para prorrogacao *" ou "* Informe grupos para prorrogacao *"
    E o cursor volta ao campo que falta
    E nada é registrado

  Cenário: Nova data igual à data limite informada
    Quando informo como nova data a mesma data limite da permissão
    Então vejo "* Informe nova data para prorrogacao *"
    E nada é registrado

  Cenário: Digitação não numérica
    Quando preencho com letra qualquer um dos campos com rótulo
    Então a tela recusa a digitação antes de qualquer consulta ao cadastro
    E o cursor volta ao campo recusado, quando o campo tem posição de cursor
    E nada é registrado

  Cenário: Nova data anterior ao início da permissão
    Dado que a permissão daquela coordenação regional começa depois da nova data que informei
    Quando envio a tela
    Então vejo "* Data menor que data inicial da permissao *"
    E o cursor volta à coordenação regional
    E nada é registrado

  Cenário: Prazo pretendido que não cabe no período original da permissão
    Dado que o prazo entre a data limite e a nova data não cabe no período original da permissão
    Quando envio a tela
    Então vejo "* Periodo prorrogacao > periodo inicial permiss *"
    E nada é registrado

  Cenário: Nova data que cruza outro período cadastrado
    Dado que a nova data ultrapassa a data limite atual
    E o intervalo resultante cruza um período já cadastrado para aquele contrato e aquela coordenação regional
    Quando envio a tela
    Então vejo "* Ja existe permissao neste intervalo *"
    E o cursor volta à coordenação regional
    E nada é registrado

  Cenário: Encurtar o prazo com pedidos pendentes
    Dado que a nova data é anterior à data limite atual
    E a permissão tem pedidos pendentes
    Quando envio a tela
    Então vejo "* Nao diminua periodo. Ja existem pedidos *"
    E o cursor volta à coordenação regional
    E nada é registrado

  Cenário: Coordenação regional sem período no contrato
    Dado que informei uma coordenação regional que não tem período cadastrado naquele contrato com o início de período que informei
    Quando envio a tela
    Então vejo "* Grupo nao cadastrado nesta permissao *"
    E o cursor volta àquela coordenação regional
    E nada é registrado

  Cenário: Grupamento encontrado sem permissão é pulado
    Dado que um dos grupamentos encontrados naquela coordenação regional não tem permissão de contrato
    Quando envio a tela
    Então aquele grupamento é pulado sem mensagem e sem prorrogação

  Cenário: Já existe requisição da mesma relação
    Dado que há uma requisição de processamento da mesma relação
    Quando respondo S à pergunta de atualização do cadastro
    Então vejo "* Relatorio em processamento. Aguarde. *"
    E o cursor volta ao campo da resposta
    E nada é registrado

  Cenário: A confirmação é pedida antes de qualquer registro
    Dado que todas as conferências passaram
    Quando envio o pedido
    Então vejo a pergunta "Atualiza cadastro da permissao <S/N>?"
    E nenhuma requisição foi registrada ainda

  Cenário: Prorrogação que passa de cinco anos
    Dado que a nova data ultrapassa cinco anos contados do início da permissão
    Quando envio o pedido
    Então vejo também "Confirma prorrog excede prazo de 5 anos de vigencia do contrato <S/N>:"
    E só com as duas respostas em S o pedido é registrado

  Cenário: A resposta negativa não cancela e não registra nada
    Dado que a tela pediu a confirmação
    Quando respondo N
    Então a tela refaz as conferências e pede a confirmação outra vez
    E nenhuma requisição é registrada

  Cenário: Mudar um dado entre a pergunta e a resposta refaz a conferência
    Dado que a tela pediu a confirmação
    Quando altero o grupamento, uma das datas ou uma das coordenações regionais e respondo S
    Então a confirmação é descartada, as conferências são refeitas e a pergunta volta
    E nada é registrado

  Cenário: O que o pedido leva
    Dado que confirmei a prorrogação
    Então a requisição fica registrada com o tipo de órgão, a matrícula, a estação e a data do pedido
    E o processamento recebe os parâmetros da prorrogação, incluindo o aviso de que ela passa de cinco anos
```
