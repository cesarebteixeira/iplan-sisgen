# US — F120C — Consultar instituições beneficentes da coordenadoria

## Estória

Como **servidor de CRE**, quero **consultar as instituições beneficentes da minha coordenadoria e
abrir a ficha da que eu marcar**, para que **eu confira como cada uma está identificada no sistema e
chegue à manutenção dela sem decorar o código INEP**.

A identificação da instituição beneficente — o nome do órgão, o código INEP e o CNPJ — é o que a
mantém ligada aos registros que dependem dela. Esta relação existe para que essa identificação seja
conferida de uma vez, instituição por instituição da coordenadoria, e para que a ficha da instituição
escolhida seja alcançada sem que se decore o código. Sem ela, a conferência seria uma consulta por
código, uma a uma — e quem não decora os códigos não chega à ficha.

## Contexto

Jornada S000M → F000M → F100M → F120C (4 passos).
Ator: servidor de CRE — consulta a relação das instituições beneficentes da sua coordenadoria e
escolhe uma delas para abrir a ficha.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de qual
menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não
regra de negócio, e este documento não o descreve.

As duas telas anteriores ao destino, `F000M` e `F100M`, são **menus de 12 opções** e nada gravam: só
encaminham. A `F100M` abre a `F120C` passando o registro adiante, mas não deixa dado de negócio
nenhum. O contexto que a `F120C` usa é o que a **entrada** deixou na sessão: a **coordenadoria**, o
**tipo de órgão** e, para o cabeçalho, a descrição desse tipo de órgão e a data do sistema.

A `F120C` é uma tela de **consulta**, não um menu: ela mostra uma página de **doze instituições** por
vez, da coordenadoria em uso, e não grava nada. Ela encadeia com a `F120T`, a tela que mantém o
cadastro das instituições beneficentes: marcada uma instituição da relação, esta tela entrega a
sessão à `F120T` com a instituição escolhida e registra-se como **origem** da passagem (RN-08). É por
causa dessa origem que a `F120T` abre sobre a instituição escolhida — e é por isso que a jornada
termina aqui: quem mantém a ficha é a tela seguinte, e esta tela é o índice dela.

As regras abaixo são só as da tela desta jornada. As regras que se revelaram da entrada estão
apontadas no anexo de evidências, na seção das regras da entrada.

---

## Regras de negócio

### RN-01 — A tela é de consulta e não grava nada

Esta é uma tela de **consulta**. Ao abrir, ela repõe sozinha a operação de consulta, seja qual for a
tela que a chamou — inclusive quando vem do menu. Nenhum cadastro é incluído, alterado, cancelado ou
travado, e nenhum registro de auditoria é criado: das operações de gravação que o programa gerado
declara para os cadastros que enxerga — inclusão, exclusão e travamento de registro —, **nenhuma é
executada** por caminho nenhum.

A tela lê o **cadastro de instituições beneficentes** e o **cadastro de coordenadorias**; pelas
rotinas comuns de segurança, lê também o **cadastro de telas**, o **cadastro de autorizações por
código de acesso** e o **cadastro da sessão do servidor**. O cadastro de auditoria não está entre os
cadastros que ela enxerga.

### RN-02 — A relação traz doze instituições por página, com o INEP, o CNPJ e a marca da linha

A página comporta **doze instituições**. Cada uma ocupa **uma linha da tela** (80 posições) e traz
quatro informações: o **nome do órgão** (40 posições), o **código INEP** (8 dígitos), o **CNPJ**
(14 posições) e a **marca da linha** (uma posição), que é como se escolhe a instituição (RN-08). No
alto ficam a **coordenadoria em uso** (2 dígitos), a **operação**, a **descrição do tipo de órgão da
sessão** e a **data do sistema**.

O CNPJ exibido é o **CNPJ do órgão**; quando o cadastro não o traz, a tela mostra o **CNPJ da
mantenedora** no lugar — a linha não fica sem CNPJ por falta do CNPJ do órgão.

[?] O cadastro guarda o CNPJ do órgão como texto, e a troca pelo da mantenedora é decidida
comparando esse texto com zero. O que o cadastro grava quando a instituição não tem CNPJ próprio —
em branco, com zeros, ou com zeros à esquerda — não está no material lido, e é disso que depende a
troca acontecer. Pergunta ao site.

[?] A descrição do tipo de órgão e a data do sistema que o cabeçalho mostra são preenchidas pelo
ambiente, e não pela tela: no acervo lido elas só aparecem sendo inicializadas em branco. A descrição
tem origem na entrada, que a lê do cadastro de tipos de órgão, mas o trecho do ambiente que a
transporta não está no acervo lido. Pergunta ao site.

### RN-03 — A relação sai do cadastro de instituições beneficentes da coordenadoria e anda de doze em doze

A relação é montada a partir do **cadastro de instituições beneficentes**, restrita à **coordenadoria
em uso**: cada linha é uma instituição daquela coordenadoria, na **ordem do cadastro** — pela
coordenadoria, pelo nome do órgão e pelo código INEP. Um registro de outra coordenadoria encerra a
relação. Não há busca por nome, por código INEP nem por CNPJ: a tela apenas percorre o cadastro, e
não oferece página anterior.

Ao montar a página, a tela guarda na sessão o **nome da última instituição mostrada**, e é dessa
posição que a montagem parte na abertura seguinte — cada abertura continua de onde a anterior parou.
Quando a relação termina antes da décima segunda linha, a posição é **limpa** e a abertura seguinte
recomeça da primeira instituição.

A montagem acontece na **abertura** da tela. A passagem em que o servidor informa outra coordenadoria
confere a coordenadoria e passa a considerá-la em uso, mas não remonta a relação (RN-05 e RN-07).

[?] A leitura que parte da posição guardada usa o recurso de posicionamento do dicionário de dados,
cujo efeito exato não está no acervo nem no manual: se ele exige a chave exata, a primeira linha da
abertura seguinte **repete** a última instituição mostrada; se posiciona na primeira chave igual ou
posterior, a abertura seguinte **avança**. Os dois comportamentos são compatíveis com o que o fonte
mostra. Pergunta ao site.

[?] Se a relação da coordenadoria recém-informada só aparece na abertura seguinte da tela, ou se há
um caminho que a remonta na mesma resposta, o material lido não determina: a passagem que trata a
mensagem do servidor não relê o cadastro das instituições. Pergunta ao site.

### RN-04 — Não havendo instituição beneficente na coordenadoria, a tela avisa

Não achando nenhuma instituição beneficente para a coordenadoria em uso, a tela avisa
**\* Nao existem inst. beneficentes cadastradas \*** e não monta nenhuma linha. O aviso é decidido na
montagem da **primeira linha** e não se repete: uma relação que se esgote depois da primeira linha
fica em branco, sem aviso.

O mesmo aviso sai quando a **sessão não traz coordenadoria nenhuma**: sem coordenadoria em uso a tela
não lê instituição alguma e avisa como se não houvesse nenhuma cadastrada (RN-05).

### RN-05 — A tela abre com a coordenadoria da sessão, e é ela que limita a consulta

A tela abre com a **coordenadoria da sessão** já no campo, e é essa coordenadoria que a relação
mostra. Quando a sessão **não traz coordenadoria** — o caso do servidor de secretaria —, o campo abre
em zero, nenhuma instituição é lida e a tela avisa que não existem instituições cadastradas (RN-04);
nesse caso, qualquer coordenadoria cadastrada passa a ser aceita (RN-07).

A conferência do cadastro da coordenadoria **não se repete** para a mesma coordenadoria: informada de
novo a que já está em uso, a tela segue sem reconsultá-la. É por isso que a coordenadoria com que a
tela **abre** não é conferida no cadastro — a conferência do cadastro só acontece quando o servidor
informa **outra** coordenadoria.

[?] A coordenadoria da sessão que esta tela lê está numa área de trabalho que o acervo lido só
inicializa em branco: nenhum programa do acervo atribui valor de negócio a ela — a entrada guarda a
coordenadoria do funcionário em outra área. O mesmo vale para o tipo de órgão, a matrícula, o
privilégio e o código de acesso que a tela repassa às rotinas de segurança. Se esses valores não
forem transportados, todo servidor cai no ramo de "sem coordenadoria": a relação abre vazia com o
aviso de que não existem instituições cadastradas, e a conferência do cadastro de coordenadorias é
feita com o tipo de órgão zerado — e então nenhuma coordenadoria é achada. Pergunta ao site.

[?] A tela não confere no cadastro a coordenadoria com que abre; se essa coordenadoria puder estar
excluída sem que a tela perceba, o fonte não diz: a marca de exclusão só é conferida quando o
servidor informa outra coordenadoria. Pergunta ao site.

### RN-06 — A coordenadoria e o código INEP passam pela edição numérica

Os dois códigos da tela — a **coordenadoria** e o **código INEP** da instituição — são tratados como
número: o que estiver **em branco vira zero**, os zeros à esquerda são descartados, e o número
tratado volta para o campo. Quando a edição acusa erro, o cursor volta ao **campo da coordenadoria**
e a passagem é encerrada. A edição é feita uma vez, antes de as linhas serem percorridas.

[?] A edição numérica é um serviço do ambiente, sem fonte no acervo: o que exatamente ela recusa
(letra, sinal, excesso de dígitos) e o que ela deixa no campo não estão no material lido. Pergunta ao
site.

### RN-07 — A coordenadoria informada tem de estar preenchida, ser a da sessão e estar cadastrada

Informada uma coordenadoria, a tela a confere nesta ordem, e a primeira recusa encerra a passagem,
com o cursor de volta ao campo da coordenadoria e sem relacionar nada:

| o que se informou | o que a tela faz |
| --- | --- |
| a **mesma** que já está em uso | deixa passar sem reconsultar o cadastro |
| **em branco** (que vira zero), havendo outra em uso | recusa com **\* Informe o grupo \*** |
| **outra** que não a da sessão, quando a sessão tem uma | recusa com **\* Usuario sem acesso a este grupo \*** |
| **uma qualquer**, quando a sessão não tem coordenadoria | confere o cadastro e deixa passar |

Passando por essas conferências, a coordenadoria é procurada no **cadastro de coordenadorias**, pelo
**tipo de órgão da sessão** e pelo código informado. Não estando cadastrada — ou estando marcada como
**excluída** —, a recusa é **\* Grupo nao cadastrado \***, com o cursor de volta ao campo. A marca de
exclusão é conferida depois de o registro ser achado: coordenadoria excluída é tratada como não
cadastrada.

Sendo aceita, a coordenadoria informada passa a ser a que está em uso, e a posição guardada da
relação é limpa.

[?] A procura no cadastro de coordenadorias usa o **tipo de órgão da sessão**, e o acervo lido não
atribui valor a esse dado: ele só aparece sendo zerado. Se ele não chegar à tela, a procura é feita
com zero e nenhuma coordenadoria é achada — e então a tela recusa toda coordenadoria informada. A
tela irmã que lê o mesmo cadastro usa, para a mesma chave, o tipo de órgão da área de segurança.
Pergunta ao site.

### RN-08 — Marcada a linha de uma instituição, a ficha dela se abre na tela seguinte

A escolha é a **marca da linha**: marcada uma linha que tenha **instituição**, a tela **não** segue
com operação própria — ela entrega a sessão à `F120T`, a tela que mantém o cadastro das instituições
beneficentes, com a **instituição escolhida** (o código INEP e o CNPJ do órgão que a linha mostra) e
registra a **própria tela como origem** dessa passagem. É por causa dessa origem que a `F120T` abre
lendo a instituição escolhida pelo código INEP; aberta pelo menu, a `F120T` não faz essa leitura.

Sem a marca na linha — ou marcando uma linha **sem instituição** —, a tela apenas segue mostrando a
relação: não abre ficha nenhuma e não avisa nada. Nada é gravado por esta tela nessa passagem.

[?] O valor que dispara a passagem é a letra **X**, e é o único que o fonte compara; o rótulo que a
máscara mostra para essa coluna, e o formato da coluna, não estão no lote. Pergunta ao site.

[?] O modo com que a `F120T` abre por causa da passagem não fica determinado no material lido: a
`F120C` deixa a operação de consulta na área da sessão, mas não informa operação própria da passagem
— esse campo vai em branco —, e a `F120T` decide o modo pelo campo do próprio registro. Se o modo
chega pela passagem ou se a `F120T` o repõe sozinha, pergunta ao site.

### RN-09 — Nada acontece sem a conferência de tela, de rota e de permissão

Antes de conferir a coordenadoria e antes de qualquer passagem, a transação passa pelas rotinas
comuns de **segurança de perfil**, de **rota** e de **permissão por operação**, com o contexto da
sessão. A tela precisa estar no **cadastro de telas** — não estando, a recusa é
**\* Tela nao disponivel \***; depois, a matrícula precisa ter a tela autorizada no seu **código de
acesso** — não tendo, a recusa é **\* Acesso negado para esta matricula \***. Se qualquer conferência
não devolver "OK", a transação é abandonada: nenhuma instituição é relacionada.

A permissão por operação examina **inclusão, alteração e exclusão**; a **consulta não tem marca
própria exigida** — o cadastro de autorizações guarda a marca de consulta, mas a rotina não a exige.
Como a tela repõe a consulta na abertura, a conferência da operação passa; se o cabeçalho levar uma
operação que o código de acesso não libera, a recusa é **\* Acesso negado para esta operacao \***.

[?] A tela repassa à conferência de permissão a operação que estiver no cabeçalho e não limita o modo
informado. Se a máscara oferecer o campo do modo, uma operação diferente da consulta chega à
conferência sem mudar mais nada no comportamento da tela. Pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Consultar as instituições beneficentes da coordenadoria regional escolar

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F120C

  Cenário: A tela abre em consulta e mostra as instituições da coordenadoria
    Dado que a minha sessão está vinculada a uma coordenadoria
    Quando abro a tela F120C
    Então vejo até doze instituições beneficentes daquela coordenadoria
    E cada linha traz o nome do órgão, o código INEP, o CNPJ e a marca da linha
    E vejo a coordenadoria em uso, a descrição do tipo de órgão da minha sessão e a data do sistema
    E nenhum cadastro é gravado

  Cenário: O CNPJ mostrado é o do órgão e, sem ele, o da mantenedora
    Dado que uma instituição da relação não tem CNPJ próprio no cadastro
    Quando a relação é montada
    Então a linha daquela instituição mostra o CNPJ da mantenedora

  Cenário: A relação anda de doze em doze
    Dado que a coordenadoria tem mais de doze instituições beneficentes
    Quando abro a tela F120C
    Então vejo as doze primeiras
    E a abertura seguinte continua a partir da última que apareceu

  Cenário: A relação termina antes da décima segunda linha
    Dado que a coordenadoria tem menos de doze instituições beneficentes
    Quando abro a tela F120C
    Então as linhas restantes ficam em branco
    E a abertura seguinte recomeça da primeira instituição

  Cenário: Coordenadoria sem instituição beneficente cadastrada
    Dado que a coordenadoria em uso não tem instituição beneficente cadastrada
    Quando abro a tela F120C
    Então vejo a mensagem "* Nao existem inst. beneficentes cadastradas *"
    E nenhuma linha é montada

  Cenário: Sessão sem coordenadoria abre sem relação e avisa
    Dado que a minha sessão não está vinculada a nenhuma coordenadoria
    Quando abro a tela F120C
    Então nenhuma instituição é lida
    E vejo a mensagem "* Nao existem inst. beneficentes cadastradas *"

  Cenário: A tela aberta pelo menu abre em consulta
    Dado que vim do menu F100M, que me encaminhou para a tela F120C
    Quando a tela F120C abre
    Então a operação em uso é a consulta
    E nenhum cadastro é gravado

  Cenário: Código não numérico no campo da coordenadoria
    Quando informo uma coordenadoria que não é número
    Então a tela recusa o campo antes de consultar o cadastro
    E o cursor volta para o campo

  Cenário: Coordenadoria em branco
    Dado que a minha sessão está vinculada a uma coordenadoria
    Quando apago o conteúdo do campo da coordenadoria
    E peço a operação
    Então vejo a mensagem "* Informe o grupo *"
    E o cursor volta ao campo da coordenadoria
    E nenhuma instituição é relacionada

  Cenário: Coordenadoria fora da minha sessão
    Dado que a minha sessão está vinculada a uma coordenadoria
    Quando informo outra coordenadoria
    Então vejo a mensagem "* Usuario sem acesso a este grupo *"
    E o cursor volta ao campo da coordenadoria
    E nenhuma instituição é relacionada

  Cenário: Coordenadoria não cadastrada ou excluída
    Dado que informo uma coordenadoria que não está cadastrada para o tipo de órgão da sessão, ou que está marcada como excluída
    Quando peço a operação
    Então vejo a mensagem "* Grupo nao cadastrado *"
    E o cursor volta ao campo da coordenadoria
    E nenhuma instituição é relacionada

  Cenário: Coordenadoria cadastrada passa a ser a que está em uso
    Dado que a minha sessão não está vinculada a nenhuma coordenadoria
    Quando informo uma coordenadoria cadastrada
    Então ela passa a ser a coordenadoria em uso
    E nada é gravado

  Cenário: Marcar a linha abre a ficha da instituição na tela seguinte
    Dado que a relação mostra uma instituição beneficente
    Quando marco a linha dela e peço a operação
    Então a tela F120T abre sobre aquela instituição, lida pelo código INEP
    E a tela F120C fica registrada como origem da passagem
    E nada é gravado por esta tela

  Cenário: Linha marcada sem instituição não faz nada
    Dado que marco uma linha em que não há instituição
    Quando peço a operação
    Então nenhuma ficha é aberta
    E nenhuma mensagem é mostrada por causa disso

  Cenário: Linha com instituição e sem marca não faz nada
    Dado que a relação mostra uma instituição beneficente
    Quando deixo a marca da linha dela em branco
    E peço a operação
    Então nenhuma ficha é aberta
    E nada é gravado

  Cenário: A tela não está cadastrada
    Dado que a tela F120C não está no cadastro de telas
    Quando tento abrir a tela
    Então vejo a mensagem "* Tela nao disponivel *"
    E nenhuma instituição é relacionada

  Cenário: Sem autorização para a tela
    Dado que a minha matrícula não tem a tela F120C autorizada no meu código de acesso
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E nenhuma instituição é relacionada

  Cenário: Sem permissão para a operação informada
    Dado que o cabeçalho da tela leva uma operação que o meu código de acesso não libera
    Quando peço a operação
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nenhuma instituição é relacionada
```
