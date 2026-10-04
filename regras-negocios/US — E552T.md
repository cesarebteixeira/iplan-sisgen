# US — E552T — Troca de cardápios e comensais

## Estória

Como **servidor da CRE**, quero **trocar os cardápios e informar os comensais de cada
refeição de um segmento do órgão filho**, para que o cálculo de consumo do período
saia com os cardápios e as quantidades que a unidade realmente vai servir.

A tela distribui, em cada refeição do segmento, quais cardápios valem e quantos
comensais há em cada um; é dessa distribuição que o sistema deriva o consumo do
período e o entrega ao cálculo. Ela não é a primeira a mexer nisso: a tela anterior
já montou a refeição e é ela que manda, junto com o registro, qual operação esta
tela vai executar — a troca de cardápios só acontece quando a entrada veio de lá.
Quem chega por outro caminho não vê uma tela vazia: é devolvido à tela de origem do
cálculo.

## Contexto

Jornada S000M → E000M → E550M → E550T → E551T → E552T.

Ator: servidor de CRE — troca os cardápios da refeição de cada segmento do órgão
filho e informa a quantidade de comensais por cardápio.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

As regras abaixo são só as da **tela desta jornada**. Nenhuma regra da entrada se
revelou aqui; o que a E552T faz com a sessão está registrado no anexo de evidências.

**A E552T não se abre por menu.** Ela é a última tela de um encadeamento: a E550T
passa o registro e a operação para a E551T, e a E551T faz o mesmo para a E552T, sem
passar por menu nenhum. Por isso o modo de operação desta tela (incluir, alterar,
excluir ou consultar) e o registro sobre o qual ela opera vêm inteiros da tela
anterior — e o sistema confere, antes de qualquer coisa, de qual tela ela foi
chamada.

---

## Regras de negócio

### RN-01 — Para operar, a matrícula tem que estar habilitada no vínculo com a secretaria

A tela identifica o usuário pela matrícula funcional e pela secretaria que vieram da
sessão, não de digitação, e confere se a matrícula está habilitada no cadastro de
usuários daquela secretaria. Se não estiver, a operação é recusada e a sessão volta
ao menu do cálculo, sem gravar nada e sem mensagem própria.

A matrícula e a secretaria também definem o escopo: é delas, e do órgão filho e da
coordenação regional escolar que a sessão carrega, que sai o conjunto de dados que a
tela pode ver. A identificação pelo `LOGON` — matrícula, senha e secretaria — está
escrita em `Documents/jornadas/US — 00 Entrada (LOGON, S000M).md` e não se repete
aqui.

### RN-02 — A tela só opera quando a chamada veio da E550T

Chamada de qualquer outra origem, a tela não exibe nem grava nada: ela é devolvida
imediatamente ao menu do cálculo. É o que garante que a troca de cardápios só seja
feita a partir do cálculo que a originou.

[?] O fonte traz um código de identificação de tela próprio desta estória gravado
num caminho que nunca é lido, e a guarda que decide o retorno compara com o código da
E550T. Ou a guarda pressupõe uma chamada por menu que não existe na árvore
expandida, ou a gravação do código próprio ficou sem uso. Pergunta ao site.

### RN-03 — A operação aceita é a que veio da tela anterior; fora dela, nada acontece

A operação sobre a refeição — incluir, alterar, excluir ou consultar — chega
decidida pela tela anterior e não é escolhida nesta tela. Recebida uma operação
diferente dessas quatro, o sistema devolve a sessão à tela anterior do encadeamento
sem processar o registro; nenhuma mensagem é mostrada e nada é gravado.

### RN-04 — Cálculo com período ou dia em aberto não se troca por aqui

Quando o cálculo tem data de início ou de fim em branco, fim anterior ao início,
qualquer um dos sete dias da semana sem o seu código de dia, ou é de creche, a
alteração dos cardápios não se faz nesta tela: o sistema força a operação de
inclusão e devolve a sessão à tela de origem do cálculo, sem gravar.

[?] A guarda dispara com "é creche" porque o código de creche chega preenchido pela
sessão, mas o programa não diz o que esse código carrega em negócio. Pergunta ao
site.

### RN-05 — A refeição do segmento tem que existir no cadastro de refeições

A tela procura o registro da refeição pelo segmento e pela data de referência. Não
achando, e havendo refeição cadastrada no catálogo de refeições para o segmento, o
sistema recusa a operação com a mensagem de que **"* Segmento sem comensais
cadastr. para refeicao *"** e não grava nada. Não havendo também a refeição no
catálogo, o sistema segue adiante e encerra sem gravar.

É o cadastro de refeições que decide quais refeições existem: a tela lê o catálogo
e só admite operar sobre as refeições que ele oferece.

### RN-06 — Incluir ou alterar exige a refeição já cadastrada no segmento

Toda operação, menos consultar e excluir, procura o registro da refeição do segmento
na data de referência e recusa quando ele não existe: **"* Requisicao nao
cadastrada *"**. A tela troca os cardápios e informa os comensais de uma refeição
que já está no cálculo; não é ela que cria a refeição.

### RN-07 — Alterar permite trocar o cardápio, não a sobremesa

Na alteração, cada um dos sete cardápios da refeição é conferido contra o que está
gravado. Se o código da sobremesa informado for diferente do gravado, o sistema
recusa com **"<- Nao altere codigo da sobremesa *"**, aponta o campo e não grava. O
que se altera são os cardápios e as quantidades; o código da sobremesa é imutável
por esta tela.

### RN-08 — Cada cardápio informado tem que existir, estar vigente, ser sobremesa quando a vez é dela, e valer para o segmento

Para cada um dos sete cardápios da refeição, a tela faz três conferências e tem uma
mensagem para cada uma:

- o cardápio tem que existir no cadastro de cardápios, com a data de início da
  vigência não posterior à data de referência; senão, **"* Cardapio nao cadastrado
  *"**;
- quando o que se está informando é a sobremesa, o cardápio tem que estar marcado
  como sobremesa no cadastro; senão, **"* Cardapio nao cadastrado como sobremesa *"**;
- o cardápio tem que estar previsto para aquele segmento e para o mesmo período de
  vigência; senão, **"* Cardapio nao cadastrado neste segmento *"**.

Em qualquer uma delas o sistema não grava nada e aponta o campo recusado.

[?] A vigência do cardápio é conferida em duas checagens de períodos diferentes — a
do cadastro de cardápios e a da previsão por segmento — e o programa não diz qual
das duas é o limite de negócio. Pergunta ao site.

### RN-09 — A sobremesa e o cardápio andam juntos, e o par tem que estar preenchido

A sobremesa só existe acompanhada do cardápio da refeição. Informado o código do
cardápio sem a quantidade de comensais da sobremesa, o sistema recusa com **"* Informe
o codigo do cardapio da sobremesa *"**. E havendo comensais na refeição e o cardápio
de sobremesa em branco, recusa com **"* Informe primeiro comensais para a refeicao
*"** — a sobremesa é cadastrada junto com os comensais da refeição, não sozinha.

### RN-10 — A quantidade de comensais tem um teto por segmento e por data

A quantidade de comensais informada em cada cardápio não pode passar do máximo
previsto para o segmento naquela data de referência; passando, o sistema recusa com
**"<-Quant. comensais maior que o maximo permitido *"** e mostra o teto no lugar da
quantidade digitada. O teto é do cadastro do segmento, por data.

### RN-11 — Segmento que não recebe refeição em sábado e domingo recusa o dia

Quando a data de referência cai em sábado ou domingo e o segmento está marcado como
não recebendo refeição nesses dias, o sistema recusa com **"* Segmento nao recebe
refeic. sabados e domingos *"** e não grava nada.

[?] O cadastro do segmento guarda a marcação em um único campo de um caractere, e o
programa o interpreta como "não recebe" quando é diferente de "N". O que significa
cada valor possível desse campo é dialeto do cadastro; o corpus não define.
Pergunta ao site.

### RN-12 — Alterar grava só o que mudou, e recalcula o consumo da refeição

Confirmada a alteração, o sistema compara os sete cardápios e as sete quantidades de
comensais informados com o que está gravado na refeição do segmento. Se está tudo
igual, nada é gravado. Havendo diferença, ele trava a refeição e regrava os cardápios
e as quantidades de comensais.

Em seguida, para cada cardápio que permaneceu, ele lê a previsão do cardápio para o
segmento, multiplica a quantidade prevista por comensal pela quantidade de comensais
da refeição e soma o resultado ao total do período para aquela subclasse e aquele
gênero — uma soma cumulativa, refeita a cada alteração. É esse total que a tela
entrega adiante.

### RN-13 — Sobremesa que sai da refeição é apagada do cadastro de sobremesas

Não havendo diferença na refeição, o sistema ainda verifica se a sobremesa que estava
distribuída naquela refeição mudou. Mudando, ela limpa o código da sobremesa das
refeições em que ele aparece naquele mesmo período e regrava o conjunto. É a única
gravação que acontece quando os cardápios da refeição continuam iguais.

### RN-14 — Excluir a refeição do segmento só quando ela é a última e nada pende dela

A exclusão da refeição do segmento só passa por três guardas, nesta ordem:

- se a refeição anterior à excluída tem dados, ou a seguinte tem, o sistema recusa com
  **"* Exclua na tela anterior de refeicoes *"** e aponta o campo do comando — a
  exclusão é da última refeição do segmento, e as demais se excluem na tela anterior;
- se algum dos sete cardápios da refeição tem registro com quantidade de sobremesa, a
  exclusão é recusada com a mesma mensagem do item anterior — a refeição com
  sobremesa distribuída não se apaga por aqui;
- passando as duas, o sistema apaga o registro da refeição do segmento.

[?] A guarda da exclusão exige que os sete campos de código de cardápio estejam em
branco, mas esses campos são os que o usuário digita na mesma tela, e o caminho de
exclusão ainda trava e regrava a própria refeição com eles. Ou a exclusão só funciona
com a tela em branco, ou o caminho de gravação dela é inalcançável. Pergunta ao site;
não concluo qual dos dois.

### RN-15 — A consulta não grava nada

Na consulta a tela apenas lê a refeição do segmento, o cadastro de refeições e o
catálogo de sobremesas, monta a grade com o que achou e encerra; a passagem de
gravação é desviada de propósito quando a operação é consultar. Nenhum registro é
inserido, alterado ou apagado.

### RN-16 — A tela entrega o cálculo refeito à tela de consolidação, e a última refeição pede a simulação

Ao fim da alteração, a tela passa adiante a refeição do segmento com a operação de
alteração e os totais do período — este é o registro que a tela de consolidação
recebe para fechar o cálculo.

A tela seguinte é alcançada em quatro saídas: pela E550M, quando a operação não tinha
o que processar; pela E551T, ao voltar para a refeição anterior, para o próximo
segmento ou para a última refeição do segmento; e pela tela de consolidação, depois
de a alteração passar.

Só quando a refeição trabalhada é a última do segmento é que o sistema pede a
simulação de cálculo — **"Calcula Simulacao <S/N>:"** — e, respondida que sim, o
total do período ainda é refeito dividindo-o por um fator de conversão cadastrado por
subclasse e gênero, para virar o total de gênero consumido.

[?] O campo que revela a última refeição do segmento é preparado pela tela anterior e
o programa o usa para decidir se pede a simulação; nesta tela ele aparece apenas
copiado da sessão. Como o valor nasce na tela anterior, a leitura isolada desta
estória não permite dizer quem o liga. Pergunta ao site.

### RN-17 — A tela lê mais cadastros do que grava

A tela enxerga treze cadastros, mas só chega a gravar em dois: a refeição do segmento
e os totais do período. Os outros onze são apenas lidos para conferir. O gerador
declara, para cada cadastro, a rotina de gravação e a de exclusão — mas declaração não
é uso: das treze rotinas de gravação declaradas, a tela executa duas, e das treze de
exclusão, uma.

---

## Cenários BDD

```gherkin
Funcionalidade: Troca de cardápios e comensais da refeição de cada segmento do órgão filho

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E552T

  Cenário: RN-02 e RN-15 — consultar a refeição de um segmento
    Dado que a tela anterior me entregou a refeição de um segmento com a operação CON
    Quando confirmo
    Então vejo a refeição, os sete cardápios distribuídos e a quantidade de comensais de cada um
    E nada é gravado

  Cenário: RN-03 — operação que a tela não executa
    Dado que a operação recebida não é incluir, alterar, excluir nem consultar
    Quando confirmo
    Então a sessão volta à tela anterior do encadeamento
    E nenhuma mensagem é mostrada
    E nada é gravado

  Cenário: RN-04 — cálculo com data de início em branco
    Dado que o cálculo tem a data de início do período em branco
    Quando abro a tela pela cadeia do cálculo
    Então o sistema força a operação de inclusão e me devolve à tela de origem do cálculo
    E nada é gravado

  Cenário: RN-01 — matrícula sem vínculo com a secretaria
    Dado que a minha matrícula não está habilitada no cadastro de usuários desta secretaria
    Quando abro a tela pela cadeia do cálculo
    Então a sessão volta ao menu do cálculo
    E nada é gravado

  Cenário: RN-05 — segmento sem comensais cadastrados para a refeição
    Dado que não existe registro da refeição para o segmento na data de referência
    E existe refeição cadastrada no catálogo para esse segmento
    Quando confirmo
    Então vejo "* Segmento sem comensais cadastr. para refeicao *"
    E nada é gravado

  Cenário: RN-06 — incluir ou alterar refeição que não está no cálculo
    Dado que a operação é incluir ou alterar
    E a refeição do segmento não tem registro na data de referência
    Quando confirmo
    Então vejo "* Requisicao nao cadastrada *"
    E nada é gravado

  Cenário: RN-08 — alterar trocando os cardápios e os comensais
    Dado que a operação é alterar e a refeição do segmento existe
    E informo cardápios vigentes, previstos para o segmento e com a sobremesa marcada
    E informo a quantidade de comensais de cada um
    Quando confirmo
    Então os cardápios e as quantidades são gravados na refeição do segmento
    E o total do período de cada subclasse e gênero é refeito com a quantidade prevista por comensal
    E a refeição segue para a tela de consolidação com a operação de alteração

  Cenário: RN-07 — alterar o código da sobremesa
    Dado que a operação é alterar e a refeição tem uma sobremesa gravada
    Quando informo um código de sobremesa diferente do gravado
    Então vejo "<- Nao altere codigo da sobremesa *"
    E nada é gravado

  Cenário: RN-08 — cardápio que não existe
    Dado que informo um cardápio que não está cadastrado
    Quando confirmo
    Então vejo "* Cardapio nao cadastrado *"
    E nada é gravado

  Cenário: RN-08 — cardápio que não é sobremesa
    Dado que informo, na posição de sobremesa, um cardápio que não está marcado como sobremesa
    Quando confirmo
    Então vejo "* Cardapio nao cadastrado como sobremesa *"
    E nada é gravado

  Cenário: RN-08 — cardápio não previsto para o segmento
    Dado que informo um cardápio que não está previsto para o segmento
    Quando confirmo
    Então vejo "* Cardapio nao cadastrado neste segmento *"
    E nada é gravado

  Cenário: RN-09 — comensais informados sem o cardápio da sobremesa
    Dado que informo a quantidade de comensais da sobremesa e deixo o cardápio dela em branco
    Quando confirmo
    Então vejo "* Informe o codigo do cardapio da sobremesa *"
    E nada é gravado

  Cenário: RN-09 — sobremesa distribuída sem comensais na refeição
    Dado que a refeição tem sobremesa gravada e os comensais dela estão zerados
    Quando confirmo
    Então vejo "* Informe primeiro comensais para a refeicao *"
    E nada é gravado

  Cenário: RN-10 — quantidade de comensais acima do teto do segmento
    Dado que informo, em um cardápio, mais comensais do que o máximo previsto para o segmento na data
    Quando confirmo
    Então vejo "<-Quant. comensais maior que o maximo permitido *" com o teto mostrado no lugar da quantidade
    E nada é gravado

  Cenário: RN-11 — refeição pedida para sábado ou domingo em segmento que não atende
    Dado que a data de referência cai em sábado ou domingo
    E o segmento está marcado como não recebendo refeição nesses dias
    Quando confirmo
    Então vejo "* Segmento nao recebe refeic. sabados e domingos *"
    E nada é gravado

  Cenário: RN-12 e RN-13 — confirmar sem nenhuma diferença na refeição
    Dado que os cardápios e as quantidades informados são iguais aos gravados
    Quando confirmo
    Então nenhum cardápio nem quantidade é regravado
    E, se a sobremesa distribuída mudou, ela é apagada das refeições do período

  Cenário: RN-14 — excluir a última refeição do segmento
    Dado que a operação é excluir
    E a refeição é a última do segmento e não tem sobremesa distribuída
    Quando confirmo
    Então o registro da refeição do segmento é apagado

  Cenário: RN-14 — excluir refeição que não é a última
    Dado que a operação é excluir
    E a refeição anterior ou a seguinte tem dados
    Quando confirmo
    Então vejo "* Exclua na tela anterior de refeicoes *" apontando o campo do comando
    E nada é apagado

  Cenário: RN-14 — excluir refeição com sobremesa distribuída
    Dado que a operação é excluir
    E um dos cardápios da refeição tem registro com quantidade de sobremesa
    Quando confirmo
    Então vejo "* Exclua na tela anterior de refeicoes *" apontando o campo do comando
    E nada é apagado

  Cenário: RN-16 — última refeição do segmento pede a simulação e entrega o total
    Dado que a refeição trabalhada é a última do segmento
    Quando confirmo
    Então o sistema me pergunta se calculo a simulacao
    E, respondendo que sim, o total do período é dividido pelo fator de conversão de cada subclasse e gênero
    E a refeição segue para a tela de consolidação
```
