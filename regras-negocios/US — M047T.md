# US — M047T — Completar o mapa do mês de uma unidade com a justificativa de cada dia

## Estória

Como **servidor de CRE**, quero **lançar de uma vez, no mapa do mês de referência de uma unidade da minha coordenadoria, a justificativa de cada dia do período**, para que **os dias úteis, os sábados, os domingos, os feriados e os recessos daquela unidade fiquem registrados no mapa sem eu ter de lançar dia a dia**.

O mapa guarda, dia por dia, o que vale na unidade: a semana do cardápio e a justificativa daquele dia; e, quando a unidade tem grupo de atendimento, o mesmo dia para cada grupo. Quem lê o mapa espera o mês inteiro preenchido, e é por isso que esta tela existe: ela **completa** o mês, acrescentando só os dias que ainda não têm registro, e por isso pode ser executada de novo no mesmo mês sem estragar o que já foi lançado. Sem ela, o mês teria de ser digitado dia a dia, e o mapa da unidade ficaria incompleto até o último dia ser lançado.

## Contexto

Jornada S000M → M000M → M047T.

Ator: servidor de CRE — lança no mapa do mês de uma unidade da sua coordenadoria as justificativas dos dias do período e, quando a unidade tem grupo de atendimento, também os dias desse grupo.

A entrada — o `LOGON` e o menu principal `S000M` — está em `Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra de negócio.

A tela é aberta pelo encadeamento do menu `M000M`, que passa a ela a sessão já montada pela entrada: a secretaria (o tipo de órgão), a coordenadoria, a unidade e a matrícula do servidor. Não vem de quem a chama nenhum modo de operação — ela abre sempre na inclusão, e o que muda de uma abertura para outra é só a unidade que a sessão já traz. Terminado o lançamento, ela **reabre a própria tela** e não encadeia para nenhuma outra.

As regras abaixo são só as da tela desta jornada; elas não repetem as da entrada. O que se revelou pertencer ao arquivo da entrada está no anexo de evidências.

## Regras de negócio

### RN-01 — A tela completa o mapa do mês com os dias que faltam

A operação da tela é gerar, para a unidade e o mês de referência informados, o registro no mapa de cada dia do período que ainda não tenha nenhum. Cada registro gerado leva a secretaria, a unidade, a coordenadoria, o dia, o mês e o ano do mapa, o mês e o ano de referência, a semana do cardápio correspondente ao dia, a resposta sobre creche da unidade e a justificativa daquele dia:

- nos dias úteis, a justificativa dos dias úteis;
- quando o dia cai em sábado, a de sábado; quando cai em domingo, a de domingo;
- quando o dia está no calendário de feriados da secretaria, a de feriado — e, se o que está registrado ali for recesso ou recesso escolar, a de recesso, que prevalece sobre a de feriado.

Cada registro gerado é acompanhado do registro da operação na auditoria, com a unidade, a matrícula e a estação de quem lançou, a data e a hora e a própria operação de inclusão.

[?] A escolha entre a justificativa dos dias úteis, a de sábado e a de domingo sai do nome do dia da semana que a rotina de data do ambiente deixa na última conversão de data. Essa rotina não tem corpo no material lido, e não se conclui dele se o nome corresponde ao dia que está sendo gerado ou ao dia anterior. Pergunta ao site.

[?] O registro do dia é gerado mesmo quando o dia não tem período semanal cadastrado para a coordenadoria: a semana vai para o registro vinda de uma busca que não achou o período daquele dia, e o acervo não diz o que esse campo leva nesse caso. Pergunta ao site.

### RN-02 — O grupo de atendimento acrescenta os seus dias ao mapa

Quando a unidade tem grupo de atendimento e o servidor informa a justificativa desse grupo (RN-12), a tela gera também o registro de cada dia para o grupo: o dia, o mês e o ano do mapa, a secretaria, a unidade, a coordenadoria, o segmento do grupo, o grupo de atendimento e a justificativa do grupo. Esse registro só é gerado para o dia que **já tem** registro no mapa — os dias que a própria tela acabou de gerar contam —, nunca em sábado, em domingo, em feriado ou em recesso, e nunca quando o registro do grupo já existe para aquele dia.

### RN-03 — A tela só acrescenta: o que já está no mapa não é tocado

A tela não altera e não apaga nada no mapa. O dia que já tem registro é deixado exatamente como está, e o que já foi lançado para um grupo também. Por isso a operação pode ser repetida no mesmo mês: cada execução só acrescenta os dias que faltavam, e o resultado é o mesmo quantas vezes for executada.

### RN-04 — A tela só inclui, e não é uma tela de consulta

A operação da tela é a inclusão, e é com ela que a tela abre. Se a mensagem chegar com outra opção, o sistema recusa com **\* Opcao nao disponivel. Use INC \***, devolve o cursor ao campo da opção e não lê nem grava nada.

Não há caminho de consulta. Abrir a tela mostra a unidade, o período do mês e as justificativas já cadastradas para o tipo de órgão, mas não mostra o que já foi lançado no mapa e não grava nada; ser recusado, ou responder "não" à pergunta de confirmação (RN-14), também não grava.

[?] A recusa manda usar **INC**, mas a tela compara o campo com o código interno da operação de inclusão, que vem da tabela de mensagens do ambiente e não tem valor no material lido. Se a opção chegar escrita como "INC", a inclusão seria recusada. Pergunta ao site.

### RN-05 — A unidade é a do meu vínculo, e a coordenadoria é a da unidade

Quando o meu vínculo com a secretaria já define a unidade, ela vem preenchida e é a única em que eu posso lançar: informar outra é recusado com **\* Usuario sem acesso a outro orgao \***, com o código da minha unidade na mensagem. Quando o vínculo define a coordenadoria mas não a unidade, a unidade é obrigatória: **\* Informe o orgao \***. Quando não define nenhuma das duas, também é preciso informar a unidade.

A coordenadoria digitada só serve para o campo não ficar em branco: aceita a unidade, a tela repõe ali a coordenadoria da própria unidade, e é ela que vale dali em diante — inclusive para achar o perfil do mês (RN-09).

### RN-06 — A unidade tem de estar cadastrada, ativa e com o cadastro completo

A unidade informada é procurada no cadastro de órgãos. Não existindo, a recusa é **\* Orgao nao cadastrado \***. Existindo e estando marcada como inativa, **\* Orgao cadastrado como inativo \***. E se faltar no cadastro qualquer um destes seis dados — o bairro, o órgão pai, o nome, o endereço, o número de matrículas e o número de pessoas —, **\* Orgao cadastrado com dados incompletos \***. Em todas elas o cursor volta ao campo da unidade e nada é gravado.

### RN-07 — A unidade tem de ser da minha secretaria e da minha coordenadoria

Aceita a unidade, o sistema confere se ela é da secretaria da sessão: não sendo, a recusa é **\* Orgao nao pertence a esta secretaria \***. E, quando o vínculo define uma coordenadoria, confere se a unidade é daquela coordenadoria: não sendo, **\* Usuario sem acesso ao grupo deste orgao \***, com o código da coordenadoria da unidade na mensagem. Passando as duas conferências, o nome da unidade e a coordenadoria dela passam a preencher a tela, e a resposta sobre creche fica guardada para os registros do mapa.

### RN-08 — O mês e o ano de referência são obrigatórios e não podem ser anteriores a agosto de 2008

A competência do lançamento é o mês e o ano de referência. Faltando um dos dois, a recusa é **\* Informe Mes/Ano de referencia \***; se a competência formada com eles for anterior a agosto de 2008, **\* Mes/Ano de referencia invalido \***. O cursor volta ao mês e nada é gravado.

### RN-09 — A unidade precisa ter o perfil do mês de referência, e o período do mês é mostrado

Para lançar, a unidade precisa ter o perfil do mês de referência cadastrado — o registro que amarra a unidade e a coordenadoria ao mês. Sem ele a recusa é **\* Perfil nao cadastrado \***, com o cursor no mês, e nada é gravado.

A tela mostra também o período do mapa daquele mês: as datas de início e de limite cadastradas para o mês de referência, com dia, mês e ano.

### RN-10 — O período é informado só pelos dias, presos ao mês de referência

O período do lançamento vai do dia inicial ao dia final, os dois presos ao mês e ao ano da referência. Cada uma das duas datas precisa existir no calendário — o dia, o mês e o ano têm de formar uma data real, com o ano entre 1994 e 2099. Falhando a inicial, a recusa é **\* Periodo inicial invalido \***, com o cursor no dia inicial; falhando a final, **\* Periodo final invalido \***, com o cursor no dia final.

Nenhuma das duas pode estar no futuro: a inicial recusada assim é **\* Data inicial maior que data atual \***; a final, **\* Data final maior que data atual \***. E a final não pode ser anterior à inicial: **\* Data final menor que data inicial \***, com o cursor no dia final. Nenhuma dessas recusas grava.

### RN-11 — As justificativas dos tipos de dia têm de estar cadastradas para o tipo de órgão

Ao abrir, a tela procura no cadastro de justificativas do tipo de órgão as justificativas de descrição **SÁBADO**, **DOMINGO**, **FERIADO** e **RECESSO** (ou **RECESSO ESCOLAR**) e já mostra os códigos delas, com as descrições ao lado; a dos dias úteis vem em branco, para o servidor informar.

Na conferência, as cinco justificativas — a dos dias úteis, a de sábado, a de domingo, a de feriado e a de recesso — são procuradas uma a uma nesse cadastro. A que não existir — e a que vier em branco, que é o mesmo que procurar a justificativa de código zero — é recusada com **\* Justificativa nao cadastrada \***, com o cursor no campo daquela justificativa, e nada é gravado. A justificativa dos dias úteis é dispensada quando a do grupo de atendimento foi informada; sem as duas, a recusa é **\* Inf.justificativa do dia ou do grupo atend \***, com o cursor na justificativa dos dias úteis.

[?] Com a justificativa dos dias úteis em branco e a do grupo informada, os dias úteis do período são gravados no mapa com a justificativa em branco (zero), porque é essa que a geração usa nesses dias. O acervo não diz se é isso que o site espera. Pergunta ao site.

### RN-12 — O grupo de atendimento e a sua justificativa andam juntos

O grupo de atendimento só entra na conferência quando a justificativa do grupo é informada. Faltando o código do grupo, a recusa é **\* Informe o grupo de atendimento \***; grupo que não existe no cadastro, **\* Grupo de atendimento nao cadastrado \***; grupo que existe mas não é daquela unidade, **\* Orgao sem este grupo de atendimento \***; e justificativa do grupo que não existe no cadastro do tipo de órgão, **\* Justificativa nao cadastrada \***, com o cursor no campo do grupo. Só o código do grupo, sem a justificativa dele, não é conferido nem aproveitado: a tela o ignora em silêncio e nada é gerado para o grupo.

### RN-13 — A justificativa "UCG NOVA" só é aceita quando a unidade não tem perfil nos meses anteriores

Quando a justificativa conferida por último é a de descrição **UCG NOVA**, o sistema procura o perfil da unidade nos dois meses anteriores ao de referência. Existindo o perfil em qualquer um deles, a recusa é **\* Use outra justificativa. Perfil cad. meses ant \***, com o cursor na justificativa dos dias úteis, e nada é gravado.

[?] A conferência só olha a descrição da última justificativa lida na conferência das cinco — a de recesso —, embora a recusa devolva o cursor ao campo da justificativa dos dias úteis. Se a regra deveria valer para qualquer uma das cinco, as outras quatro não passam por ela. Pergunta ao site.

[?] Na volta de um mês sobre o outro, o ano informado é reposto a cada passo: em janeiro, o segundo mês conferido vira novembro do próprio ano, e não novembro do ano anterior. Ou a intenção era outra, ou a virada de ano ficou pela metade. Pergunta ao site.

### RN-14 — A tela pergunta antes de gravar, e só grava com a resposta afirmativa

Passando por todas as conferências, o sistema não grava: mostra na própria tela a pergunta **\* Confirma justificativas no periodo <S/N> ? \***, com o cursor no campo da resposta, e espera. Só quando a resposta é **S** — e os treze campos informados (a opção, a unidade, o mês, o ano, o dia inicial, o dia final, as cinco justificativas dos dias e os dois códigos do grupo) estão iguais aos que foram conferidos — o lançamento é executado.

Resposta diferente de **S**, ou qualquer campo alterado depois da pergunta, faz o sistema conferir tudo de novo e perguntar outra vez: responder **N** não grava e não cancela, devolve a mesma pergunta. Terminado o lançamento, a tela volta com o aviso **\* Justificativas cadastradas \*** e o cursor no mês.

### RN-15 — A requisição com um código de tela no campo do prefixo vai para aquela tela

A requisição com que a tela é retomada pode trazer, no campo do prefixo de tela, o código de uma tela. Quando ele vem preenchido, esta tela não confere nem grava nada: a transação é desviada para a tela indicada nesse campo, antes de qualquer leitura.

[?] Nenhuma das telas da jornada atribui valor a esse campo, e o acervo não mostra quem o preenche. Pergunta ao site.

## Cenários BDD

```gherkin
Funcionalidade: Completar o mapa do mês de uma unidade com a justificativa de cada dia

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela M047T

  Cenário: O mês da unidade é completado de uma vez
    Dado que a unidade não tem nenhum dia lançado no mês de referência
    Quando informo a unidade, o mês, o ano, o período e as justificativas e confirmo
    Então o sistema cria o registro de cada dia do período no mapa
    E vejo o aviso "* Justificativas cadastradas *"

  Cenário: Cada tipo de dia recebe a justificativa própria
    Dado que o período tem dias úteis, sábados, domingos e feriados
    Quando informo as justificativas e confirmo
    Então cada dia útil entra no mapa com a justificativa dos dias úteis
    E cada sábado entra com a justificativa de sábado
    E cada domingo entra com a justificativa de domingo
    E cada feriado entra com a justificativa de feriado

  Cenário: O recesso prevalece sobre o feriado
    Dado que um dia do período está no calendário de feriados como recesso escolar
    Quando informo as justificativas e confirmo
    Então esse dia entra no mapa com a justificativa de recesso

  Cenário: Cada registro gerado leva a unidade, o mês, o dia, a semana e a justificativa
    Dado que o período foi lançado
    Então cada registro do dia leva a secretaria, a unidade e a coordenadoria
    E leva o dia, o mês e o ano do mapa e o mês e o ano de referência
    E leva a semana do cardápio daquele dia e a resposta sobre creche da unidade

  Cenário: Cada registro gerado fica na auditoria
    Dado que os dias do período foram lançados
    Então cada registro gerado tem o seu registro na auditoria
    E a auditoria leva a unidade, a matrícula, a estação, a data, a hora e a operação de inclusão

  Cenário: O grupo de atendimento acrescenta os seus dias
    Dado que a unidade tem grupo de atendimento
    Quando informo o grupo, a justificativa do grupo e o período e confirmo
    Então cada dia com registro no mapa também recebe o registro do grupo
    E o registro do grupo leva o segmento, o grupo de atendimento e a justificativa do grupo

  Cenário: O dia do grupo que já existe é deixado como está
    Dado que um dia do período já tem o registro do grupo
    Quando informo o grupo e confirmo
    Então esse dia não é tocado
    E os outros dias do período recebem o registro do grupo

  Cenário: O grupo não entra em sábado, domingo, feriado nem recesso
    Dado que o período tem sábados, domingos, feriados e recessos
    Quando informo o grupo e confirmo
    Então nenhum desses dias recebe o registro do grupo

  Cenário: O dia que já tem registro no mapa é deixado como está
    Dado que um dia do período já tem registro no mapa
    Quando lanço o mesmo período e confirmo
    Então esse dia não é alterado nem apagado
    E os dias que faltavam são lançados

  Cenário: Executar de novo no mesmo mês só completa o que falta
    Dado que executei o lançamento do período uma vez
    Quando executo o mesmo lançamento outra vez e confirmo
    Então nada é alterado e nada é apagado
    E o mapa fica com os mesmos registros da primeira execução

  Cenário: Opção diferente da inclusão é recusada
    Dado que estou na tela
    Quando informo outra opção que não a inclusão
    Então vejo a mensagem "* Opcao nao disponivel. Use INC *"
    E o cursor volta ao campo da opção
    E nada é lido nem gravado

  Cenário: Abrir a tela não grava nada
    Dado que abro a tela
    Então vejo a unidade, o período do mês e as justificativas cadastradas para o tipo de órgão
    E nenhum registro do mapa é gravado ou alterado

  Cenário: Sem a unidade informada
    Dado que o meu vínculo não define a unidade
    Quando deixo o campo da unidade em branco e confirmo
    Então vejo a mensagem "* Informe o orgao *"
    E o cursor volta ao campo da unidade

  Cenário: Unidade diferente daquela do meu vínculo
    Dado que o meu vínculo define uma unidade
    Quando informo outra unidade e confirmo
    Então vejo a mensagem "* Usuario sem acesso a outro orgao *"
    E o lançamento não é feito

  Cenário: A coordenadoria que fica na tela é a da unidade
    Dado que informo a unidade e uma coordenadoria diferente da dela
    Quando confirmo a unidade
    Então a tela passa a mostrar a coordenadoria da própria unidade
    E é essa coordenadoria que vale para achar o perfil do mês

  Cenário: Unidade não cadastrada
    Quando informo uma unidade que não existe no cadastro
    Então vejo a mensagem "* Orgao nao cadastrado *"
    E o cursor volta ao campo da unidade

  Cenário: Unidade cadastrada como inativa
    Quando informo uma unidade marcada como inativa
    Então vejo a mensagem "* Orgao cadastrado como inativo *"
    E o cursor volta ao campo da unidade

  Cenário: Unidade com o cadastro incompleto
    Quando informo uma unidade sem bairro, sem órgão pai, sem nome, sem endereço, sem matrículas ou sem pessoas
    Então vejo a mensagem "* Orgao cadastrado com dados incompletos *"
    E o cursor volta ao campo da unidade

  Cenário: Unidade de outra secretaria
    Quando informo uma unidade de outra secretaria
    Então vejo a mensagem "* Orgao nao pertence a esta secretaria *"
    E o lançamento não é feito

  Cenário: Unidade de outra coordenadoria
    Dado que o meu vínculo define uma coordenadoria
    Quando informo uma unidade de outra coordenadoria
    Então vejo a mensagem "* Usuario sem acesso ao grupo deste orgao *"
    E o lançamento não é feito

  Cenário: Sem o mês e o ano de referência
    Quando deixo o mês ou o ano de referência em branco e confirmo
    Então vejo a mensagem "* Informe Mes/Ano de referencia *"
    E o cursor volta ao campo do mês

  Cenário: Mês e ano de referência anteriores a agosto de 2008
    Quando informo um mês de referência anterior a agosto de 2008
    Então vejo a mensagem "* Mes/Ano de referencia invalido *"
    E o cursor volta ao campo do mês

  Cenário: Unidade sem o perfil do mês de referência
    Dado que a unidade não tem perfil cadastrado para o mês e o ano informados
    Quando confirmo
    Então vejo a mensagem "* Perfil nao cadastrado *"
    E o cursor volta ao campo do mês
    E nada é gravado

  Cenário: O período do mapa do mês é mostrado
    Dado que abro a tela com a unidade e o mês de referência
    Então vejo as datas de início e de limite cadastradas para aquele mês
    E o período que eu informar fica preso ao mês e ao ano da referência

  Cenário: Dia inicial que não existe no mês
    Quando informo um dia inicial que não existe naquele mês
    Então vejo a mensagem "* Periodo inicial invalido *"
    E o cursor volta ao dia inicial

  Cenário: Dia final que não existe no mês
    Quando informo um dia final que não existe naquele mês
    Então vejo a mensagem "* Periodo final invalido *"
    E o cursor volta ao dia final

  Cenário: Dia inicial no futuro
    Quando informo um dia inicial posterior à data de hoje
    Então vejo a mensagem "* Data inicial maior que data atual *"
    E o cursor volta ao dia inicial

  Cenário: Dia final no futuro
    Quando informo um dia final posterior à data de hoje
    Então vejo a mensagem "* Data final maior que data atual *"
    E o cursor volta ao dia final

  Cenário: Dia final anterior ao inicial
    Quando informo um dia final anterior ao dia inicial
    Então vejo a mensagem "* Data final menor que data inicial *"
    E o cursor volta ao dia final

  Cenário: Justificativa de um tipo de dia não cadastrada
    Quando informo uma justificativa que não existe no cadastro do tipo de órgão
    Então vejo a mensagem "* Justificativa nao cadastrada *"
    E o cursor volta ao campo daquela justificativa
    E nada é gravado

  Cenário: Sem a justificativa dos dias úteis e sem a do grupo
    Dado que deixo a justificativa dos dias úteis em branco
    E não informo a justificativa do grupo
    Quando confirmo
    Então vejo a mensagem "* Inf.justificativa do dia ou do grupo atend *"
    E o cursor volta à justificativa dos dias úteis

  Cenário: Sem o código do grupo de atendimento
    Dado que informo a justificativa do grupo
    Quando deixo o código do grupo em branco e confirmo
    Então vejo a mensagem "* Informe o grupo de atendimento *"
    E o cursor volta ao campo do grupo

  Cenário: Grupo de atendimento não cadastrado
    Quando informo um grupo de atendimento que não existe no cadastro
    Então vejo a mensagem "* Grupo de atendimento nao cadastrado *"
    E o cursor volta ao campo do grupo

  Cenário: Unidade sem esse grupo de atendimento
    Quando informo um grupo que não é daquela unidade
    Então vejo a mensagem "* Orgao sem este grupo de atendimento *"
    E o cursor volta ao campo do grupo

  Cenário: Justificativa do grupo não cadastrada
    Quando informo uma justificativa de grupo que não existe no cadastro
    Então vejo a mensagem "* Justificativa nao cadastrada *"
    E o cursor volta ao campo do grupo

  Cenário: Só o código do grupo, sem a justificativa dele
    Dado que informo o código do grupo e deixo a justificativa do grupo em branco
    Quando confirmo
    Então a tela ignora o grupo em silêncio
    E nada é gerado para o grupo
    E os dias do período são lançados normalmente

  Cenário: Justificativa "UCG NOVA" com perfil nos meses anteriores
    Dado que a unidade tem perfil cadastrado no mês anterior
    Quando informo a justificativa de descrição UCG NOVA e confirmo
    Então vejo a mensagem "* Use outra justificativa. Perfil cad. meses ant *"
    E o cursor volta à justificativa dos dias úteis
    E nada é gravado

  Cenário: A tela pergunta antes de gravar
    Dado que todas as conferências passaram
    Quando confirmo os dados
    Então vejo a pergunta "* Confirma justificativas no periodo <S/N> ? *"
    E o cursor vai para o campo da resposta

  Cenário: Nada é lançado antes da resposta
    Dado que a tela está esperando a resposta da pergunta
    Então nenhum registro do mapa foi gravado
    E nenhum registro do grupo foi gravado

  Cenário: Responder não à pergunta não grava, e a tela pergunta de novo
    Dado que a tela está esperando a resposta da pergunta
    Quando respondo algo diferente de S
    Então nada é gravado
    E o sistema confere tudo de novo
    E vejo a mesma pergunta outra vez

  Cenário: A resposta S com os dados alterados não grava
    Dado que a tela está esperando a resposta da pergunta
    Quando altero qualquer campo informado e respondo S
    Então nada é gravado
    E o sistema confere tudo de novo e pergunta outra vez

  Cenário: Requisição com um código de tela no campo do prefixo
    Dado que a requisição chega com um código de tela no campo do prefixo
    Então a transação é desviada para aquela tela
    E esta tela não confere nem grava nada
```
