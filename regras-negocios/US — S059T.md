# US — S059T — Manter os níveis de acesso e copiar as permissões de outro nível

## Estória

Como **servidor de CRE**, quero **manter os níveis de acesso do sistema e copiar
as permissões de um nível para outro**, para que **as autorizações de tela e de
operação dos servidores da secretaria sejam definidas em blocos reutilizáveis, em
vez de tela por tela**.

O nível de acesso é o bloco que diz o que um servidor pode fazer: para cada tela —
e também para cada relatório —, se ele consulta, inclui, altera ou exclui. É esta
tela que cria, renomeia e exclui esses blocos, e é por aqui que as permissões de
um bloco nascem — em geral copiadas de um nível que já funciona. Sem ela não há
como abrir um nível novo com as permissões certas; e excluir um nível não é só
descartar um nome, porque a exclusão derruba o acesso de todo servidor que o
tinha.

## Contexto

Jornada S000M → S001M → S004M → S059T (4 passos).
Ator: servidor de CRE — mantém os níveis de acesso do sistema e copia as
permissões de um nível para outro.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela —
qual opção de qual menu a abre — está em
`Documents/jornadas/00 Navegação e menus.md`: é **dado de navegação**, não regra
de negócio.

As duas telas do meio do caminho são menus: elas não passam registro nem operação
para a tela de destino, e o modo de trabalho da `S059T` — alterar ou consultar —
é decidido dentro dela mesma, pelo campo de opção (RN-04). As conferências de
acesso (a tela estar cadastrada, o código de acesso tê-la liberada e a operação
estar liberada no perfil) são as da entrada e não se repetem aqui. A `S059T`
termina em si mesma: não encaminha a tela seguinte e não passa registro nem
operação adiante.

---

## Regras de negócio

### RN-01 — O que é um nível de acesso e o que cada linha da tela pede

O nível de acesso é um bloco de autorizações identificado por um **código de dois
dígitos** e por uma **descrição de até 40 caracteres**. O código é digitado pelo
servidor — o sistema não o atribui —, e é o que for informado que fica no
cadastro. A descrição é de preenchimento obrigatório para incluir e para alterar
(RN-08). Cada linha da tela tem quatro campos: o **código do nível**, a
**descrição**, o **código de um nível de onde copiar as permissões** e a
**situação**, que diz o que fazer com aquela linha. A tela mostra **15 linhas**
por vez.

### RN-02 — Os dois códigos da linha são numéricos

Antes de qualquer conferência, o código do nível e o código do nível de origem da
cópia passam por edição numérica: o que estiver em branco vira zero e o que não
for número é recusado, com o cursor devolvido ao campo. O que não passa por essa
edição não chega às conferências seguintes.

### RN-03 — Ao entrar, a tela mostra a data e o órgão da sessão e lista os níveis já cadastrados

Ao abrir, a tela mostra a **data do sistema** e a **descrição do tipo de órgão da
sessão** e preenche as linhas com os níveis já cadastrados, do primeiro em diante.
Não havendo nenhum, a tela avisa **\* Nao existem niveis cadastrados \*** e deixa
o cursor no campo do código do nível.

[?] A tela mostra 15 níveis por vez e guarda, na área da sessão, o código do
último nível lido — quando o cadastro acaba, essa posição é zerada. Se existe uma
forma de o servidor pedir os níveis seguintes, e a partir de qual mensagem, não
está neste programa. Pergunta ao site.

### RN-04 — A tela só altera e consulta; incluir e excluir são situações de linha

O servidor escolhe a operação no campo de opção: **ALT** altera e **CON**
consulta. Em branco, a tela assume **consulta**. Qualquer outra opção é recusada
com **\* Opcao nao disponivel. Use ALT ou CON \*** e o cursor volta ao campo da
opção. Não há modo de inclusão nem de exclusão: incluir e excluir são situações de
linha, dentro do modo de alteração (RN-05). A opção é lida uma vez, da primeira
linha.

[?] A mensagem manda usar ALT ou CON, mas a tela compara a opção com os códigos
internos de operação do sistema, e nenhum texto "ALT" ou "CON" existe no acervo
lido — a mesma mensagem (nas duas redações, com "Opcao" e com "Operacao") aparece
em 105 dos 506 programas extraídos. Ou a máscara traduz o que o servidor digita,
ou quem seguir a mensagem é recusado. O texto da máscara não está no lote. Pergunta
ao site.

### RN-05 — A situação de cada linha decide a operação

Em cada linha, a **situação** decide o que fazer: **I** inclui, **A** altera e
**E** exclui. Linha sem código de nível, ou com situação diferente de I, A e E, é
**ignorada** e não gera operação nenhuma. A situação é traduzida para a operação
correspondente antes de a operação passar pelas conferências de autorização e de
nível (RN-06).

[?] Uma linha marcada para excluir em modo de consulta não produz nada — e não por
causa da situação: em consulta o processamento das linhas nem começa. Se a máscara
deixa marcar E em consulta, o que o servidor espera ver é pergunta ao site.

### RN-06 — O nível do próprio servidor limita o que ele pode manter

Antes de cada operação, o sistema apura o **maior código de nível vinculado à
matrícula do servidor** e o compara com o código do nível da linha. Para quem tem
o **privilégio**, a operação passa enquanto o código da linha **não for maior** que
o do servidor; para quem não tem, ela só passa se o código da linha for
**estritamente menor**. Fora disso, a linha é recusada com
**\* Seu nivel de acesso nao permite esta operacao \***, o cursor volta à coluna da
situação e nada é gravado. Servidor sem nenhum vínculo de nível não passa em
nenhuma das duas conferências.

[?] O que o código do nível significa em ordem — se o número maior é o nível mais
poderoso ou o menos — não está no corpus nem no dicionário. A regra acima descreve
a comparação, não a hierarquia; sem isso não se sabe se a conferência protege ou
expõe. Pergunta ao site.

### RN-07 — Incluir nível já cadastrado, alterar ou excluir nível inexistente: recusados

Para incluir, o sistema procura o código informado no cadastro de níveis:
existindo, a inclusão é recusada com **\* Nivel ja cadastrado \***. Para alterar
ou excluir, o código precisa existir no cadastro: não existindo, a recusa é
**\* Nivel nao cadastrado \***. Nas duas recusas o cursor volta à coluna da
situação.

### RN-08 — Incluir e alterar exigem a descrição do nível

Em linha de inclusão ou de alteração sem descrição, a operação é recusada com
**\* Informe descricao do nivel de acesso \*** e o cursor volta ao campo da
descrição.

### RN-09 — As permissões de um nível podem ser copiadas de outro nível

Informando o código de um segundo nível na linha, o sistema copia para o nível da
linha o **quadro de permissões** do nível informado: para cada tela — e também
para cada relatório —, se a consulta, a inclusão, a alteração e a exclusão estão
liberadas. A cópia é recusada em dois casos: quando o nível de **destino já tem**
permissões cadastradas — **\* Nao copie. Ja existem acessos cadastrados \*** — e
quando o nível de **origem não tem** permissão nenhuma —
**\* Nivel de acesso para copia nao cadastrado \***. A cópia leva as permissões, e
não as pessoas: o vínculo dos servidores com o nível de origem não é copiado.

[?] As duas conferências procuram as permissões de um nível informando o código do
nível e deixando em branco as outras duas partes da chave (o tipo e o código da
tela ou do relatório). Se a leitura exigir a chave inteira — e não "qualquer
permissão deste nível" —, nenhuma das duas acha registro: a recusa por o destino
já ter permissões nunca aconteceria, e a origem nunca precisaria ter nenhuma. O
que a leitura faz com a chave parcialmente preenchida é do dialeto do banco e não
está no corpus. Pergunta ao site.

[?] Quando o servidor não indica de qual nível copiar, a gravação procura mesmo
assim as permissões do **nível de código zero** e as copia, se existirem. O que o
código zero significa — e se ele pode existir como nível — não está no corpus.
Pergunta ao site.

### RN-10 — A inclusão cria o nível e grava as permissões copiadas

A inclusão cria o nível com o código e a descrição informados e, em seguida, grava
uma permissão para cada permissão do nível de origem, uma a uma. O nível nasce
marcado com a operação de inclusão.

[?] As recusas das regras RN-06 a RN-09 são mensagens emitidas numa passagem de
conferência; quem grava é uma passagem seguinte, que não reconfere nenhuma delas
nem consulta o indicador de erro que elas deixam. Se a mensagem não marcar a falha
que interrompe a transação — e quem a marca é a rotina de comunicação do ambiente,
que não tem corpo no acervo lido —, a linha recusada ainda assim seria gravada.
Não se escolhe um dos dois lados. Pergunta ao site.

### RN-11 — A alteração regrava a descrição e copia as permissões

A alteração regrava o nível com a nova descrição — o código não muda — e, quando
foi indicado um nível de origem, grava as permissões copiadas dele. A alteração
passa pelas mesmas conferências de existência, de descrição, de nível do servidor
e de cópia (RN-06 a RN-09).

### RN-12 — A exclusão apaga o nível, as permissões dele e o vínculo dos servidores

A exclusão apaga o nível e, na mesma operação, apaga **todas as permissões**
daquele nível e **todos os vínculos dos servidores com ele**. Quem tinha aquele
nível deixa de tê-lo. Não há aviso de quantos servidores serão atingidos nem
confirmação antes de apagar.

[?] Excluir um nível derruba o acesso de todos os servidores que o tinham, sem
aviso e sem conferência de uso — e esta tela não tem caminho que recrie um vínculo:
por aqui ele só se apaga. Se a intenção era só tirar o nível de circulação, ou se
a tela deveria avisar antes, é pergunta ao site.

### RN-13 — A consulta não grava nada

Na consulta, o sistema lista os níveis e para: nenhum nível é criado, alterado ou
excluído, nenhuma permissão é copiada ou apagada, nenhum vínculo é tocado e
nenhuma trilha de auditoria é gerada.

### RN-14 — Toda operação fica registrada na auditoria

Cada nível criado, alterado ou excluído, cada permissão gravada e cada permissão e
vínculo apagados deixam um registro de auditoria com a origem do registro (nível,
permissão ou vínculo), a operação praticada, o conteúdo anterior e o posterior, a
matrícula, a estação, o ano, o dia, o mês e a hora da sessão, o órgão, a CRE e o
número do processo. As permissões copiadas entram na auditoria **como inclusão**,
mesmo quando a cópia acontece numa alteração.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter os níveis de acesso e copiar as permissões de outro nível

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela S059T

  Cenário: Linha da tela
    Dado que estou na S059T
    Quando preencho uma linha
    Então informo o código do nível, a descrição, o código do nível de origem da cópia e a situação
    E a tela aceita até 15 linhas

  Cenário: Código de nível ou de origem não numérico
    Quando informo, no código do nível ou no código do nível de origem, algo que não é número
    Então o sistema recusa antes de qualquer conferência
    E o cursor volta ao campo

  Cenário: Lista dos níveis ao abrir a tela
    Dado que existem níveis de acesso cadastrados
    Quando abro a S059T
    Então vejo a data do sistema e o órgão da sessão
    E vejo os níveis cadastrados, até 15 por vez, com código e descrição
    E nada é gravado

  Cenário: Nenhum nível cadastrado
    Dado que não há nenhum nível de acesso cadastrado
    Quando abro a S059T
    Então vejo a mensagem "* Nao existem niveis cadastrados *"
    E o cursor fica no campo do código do nível

  Cenário: Opção de manutenção diferente de ALT e de CON
    Quando informo uma opção diferente de alteração e de consulta
    Então vejo a mensagem "* Opcao nao disponivel. Use ALT ou CON *"
    E o cursor volta ao campo da opção
    E nada é gravado

  Cenário: Linha sem código ou com situação desconhecida é ignorada
    Dado que preenchi uma linha sem código de nível, ou com situação diferente de I, A e E
    Quando a tela processa as linhas
    Então aquela linha não gera operação nenhuma

  Cenário: Operação sobre nível que o meu nível não alcança
    Dado que o maior nível vinculado à minha matrícula não alcança o nível da linha
    Quando envio a linha
    Então vejo a mensagem "* Seu nivel de acesso nao permite esta operacao *"
    E o cursor volta à coluna da situação
    E nada é gravado

  Cenário: Inclusão de nível que já existe
    Dado que o código informado já está cadastrado
    Quando informo a situação I
    Então vejo a mensagem "* Nivel ja cadastrado *"
    E o cursor volta à coluna da situação
    E nada é gravado

  Cenário: Alteração ou exclusão de nível não cadastrado
    Dado que o código informado não está cadastrado
    Quando informo a situação A ou E
    Então vejo a mensagem "* Nivel nao cadastrado *"
    E o cursor volta à coluna da situação
    E nada é gravado

  Cenário: Descrição do nível não informada
    Dado que informo a situação I ou A sem descrição
    Quando envio a linha
    Então vejo a mensagem "* Informe descricao do nivel de acesso *"
    E o cursor volta ao campo da descrição
    E nada é gravado

  Cenário: Cópia recusada porque o nível de destino já tem permissões
    Dado que o nível da linha já tem permissões cadastradas
    Quando indico um nível de origem para copiar
    Então vejo a mensagem "* Nao copie. Ja existem acessos cadastrados *"
    E o cursor volta à coluna da situação
    E nada é gravado

  Cenário: Cópia recusada porque o nível de origem não tem permissões
    Dado que o nível de origem não tem nenhuma permissão cadastrada
    Quando indico esse nível de origem
    Então vejo a mensagem "* Nivel de acesso para copia nao cadastrado *"
    E o cursor volta ao campo do nível de origem
    E nada é gravado

  Cenário: Inclusão de um nível com as permissões copiadas de outro
    Dado que estou na S059T em modo de alteração
    E que o nível de origem tem permissões cadastradas
    Quando informo a situação I em uma linha, com o código e a descrição do nível novo e o código do nível de origem
    Então o sistema cria o nível com o código e a descrição informados
    E grava uma permissão para cada permissão do nível de origem
    E o vínculo dos servidores com o nível de origem não é copiado

  Cenário: Alteração da descrição de um nível
    Dado que o nível existe e o meu nível permite mantê-lo
    Quando informo a situação A com a nova descrição
    Então o sistema regrava a descrição e o código do nível não muda

  Cenário: Exclusão do nível, das permissões e dos vínculos
    Dado que o nível existe e o meu nível permite mantê-lo
    Quando informo a situação E
    Então o sistema apaga o nível
    E apaga todas as permissões daquele nível
    E apaga o vínculo de todos os servidores que tinham aquele nível

  Cenário: Consulta não grava nada
    Dado que estou na S059T em modo consulta
    Quando abro a tela e percorro os níveis
    Então nenhum nível, permissão ou vínculo é criado, alterado ou apagado
    E nenhuma trilha de auditoria é gerada

  Cenário: Toda operação fica registrada na auditoria
    Dado que incluo, altero ou excluo um nível com as permissões dele
    Quando a operação é gravada
    Então cada nível, permissão e vínculo tocados deixam um registro de auditoria
    E as permissões copiadas entram na auditoria como inclusão, mesmo numa alteração
```
