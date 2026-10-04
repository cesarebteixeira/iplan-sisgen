# US — F022T — Consultar o vínculo do gênero com o gênero FAE

## Estória

Como **servidor da CRE**, quero **consultar, pelos códigos de subclasse e de gênero,
a que código de gênero FAE esse gênero está vinculado e com que unidade de medida e
unidade de conversão ele é tratado**, para que **a classificação e a medida do item
saiam do cadastro, e não da memória de quem prepara o documento**.

O vínculo entre o gênero e o código de gênero FAE é o que diz em que código o item é
tratado e em que unidade ele é medido, com a unidade de conversão que o vínculo
guarda. Quem prepara o documento precisa poder conferir esse vínculo antes de
classificar o item: sem a conferência, o item sai com o código ou com a medida
errados, e o erro só aparece depois, na prestação de contas. A tela é só de leitura:
não cria, não altera e não apaga vínculo nenhum, e não deixa rastro de auditoria. Quem
mantém o vínculo é outra tela.

## Contexto

Jornada S000M → F000M → F022T.

Ator: servidor de CRE — confere, pelo código de subclasse e pelo código de gênero,
qual código de gênero FAE está vinculado ao gênero, com que unidade de medida e com
que unidade de conversão.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio. As duas telas do caminho são menus e só
encaminham: esta tela abre em consulta porque ela mesma repõe a consulta quando é
aberta (RN-02), e não porque alguém lho tenha pedido.

Esta tela não muda de comportamento conforme quem a chamou: em nenhum caminho ela
compara a tela de origem com um código de tela. O que ela entrega adiante é o próprio
resultado — concluída a consulta, ela se reabre com os campos carregados (RN-07) —, e
é a única saída dela.

O que a tela usa da sessão — a **matrícula**, o **código de acesso**, o
**privilégio**, o **tipo de órgão**, a **CRE** e a **data do sistema** — é o que a
entrada deixou. A conferência do acesso à tela pertence ao documento da entrada e
está no anexo de evidências, em **Regras que se revelaram da entrada**. A data do
sistema e o tipo de órgão aparecem como contexto da consulta e não comandam o que ela
mostra.

## Regras de negócio

### RN-01 — A tela consulta o gênero e mostra o vínculo com o código de gênero FAE

Informados o **código de subclasse** e o **código de gênero**, a tela mostra o
**gênero** e o **vínculo** que ele tem com um **código de gênero FAE**:

- a **descrição resumida do gênero**, em até 15 caracteres;
- a **unidade de medida do gênero** — o código e a descrição dela;
- o **código de gênero FAE** vinculado e a **descrição dele**, em até 56 caracteres;
- a **unidade de medida do código FAE** — o código e a descrição dela;
- a **unidade de conversão** do vínculo.

Fora do vínculo, a tela exibe a **data do sistema** e a **descrição do tipo de órgão**
da sessão. Consulta-se um gênero por vez.

A descrição do gênero FAE é exibida em **até 56 caracteres**, embora o cadastro dos
gêneros FAE guarde 76: o fim de uma descrição longa não aparece na consulta.

### RN-02 — A tela é só de consulta: qualquer outra operação é recusada

A tela tem um campo de **opção** — o que se quer fazer. Quando ela é aberta pelo
menu, sem opção informada, ela mesma assume a **consulta**. Se numa mensagem seguinte
o campo da opção trouxer outra operação — incluir, alterar, excluir ou qualquer
outra —, o sistema recusa com **\* Operacao nao disponivel. Use CON \***, devolve o
cursor ao campo da opção e não lê nem grava nada. A recusa vem depois da conferência
de digitação (RN-10) e antes de qualquer leitura de cadastro.

A recusa não deixa nenhum registro: a tela não grava em caminho nenhum (RN-11).

[?] Os valores que a tela aceita como operação não são literais no programa: eles vêm
da tabela de mensagens do ambiente, carregada em tempo de execução. É por isso que a
recusa manda usar "CON" enquanto a tela compara os códigos internos dessa tabela. Se
o que o servidor digita é exatamente "CON", o material lido não confirma.

[?] Como a abertura da tela repõe a consulta sozinha, a recusa por outra operação só
é alcançada numa mensagem seguinte do servidor — e depende de a máscara da tela
oferecer esse campo de opção. O acervo lido não traz a máscara; se o campo não
existe, a recusa é trecho sem uso. Pergunta ao site.

[?] A tela carrega um campo com o **código da próxima tela**, que ela exibe e repassa
à conferência de encaminhamento. Preenchido, esse campo desvia a transmissão antes de
qualquer leitura de cadastro, e o desvio é silencioso. Esta tela não o preenche, e
quem o preencheria — a máscara da tela ou o cadastro de telas do site — não está no
acervo lido. Pergunta ao site.

### RN-03 — Sem o código de subclasse a consulta não é feita

Com o **código de subclasse** em branco — ou zerado —, o sistema avisa
**\* Informe o genero \*** e devolve o cursor ao campo do código de subclasse. Nada é
consultado.

O **código de gênero** não tem conferência própria de obrigatoriedade: em branco, ele
segue para a leitura do cadastro e cai na recusa de gênero não cadastrado (RN-04).

[?] A mensagem pede o gênero, mas a conferência é sobre o código de subclasse, e é a
ele que o cursor volta. Se o texto é o que o site espera, ou se a mensagem saiu
trocada, é pergunta ao site.

### RN-04 — O gênero tem de estar cadastrado

O par informado — **código de subclasse** e **código de gênero** — é procurado no
cadastro de gêneros. Não existindo, a recusa é **\* Genero nao cadastrado \***, com o
cursor de volta ao campo do código de subclasse, e nada é mostrado.

[?] A procura posiciona a leitura numa **versão** do gênero — ano 9999, mês e dia
zerados — e, achando o registro, confere apenas o código de subclasse e o código de
gênero: a data da versão **não** é conferida depois. O que essa posição seleciona (a
versão vigente? a última?) e qual versão aparece quando o cadastro tem várias não
está no acervo lido. Pergunta ao site.

### RN-05 — O gênero tem de ter vínculo com um código de gênero FAE

Achado o gênero, a tela procura o **vínculo** dele com um **código de gênero FAE**.
Não havendo vínculo, a recusa é **\* Relacionamentos nao cadastrados \***, com o
cursor de volta ao campo do código de subclasse. Quem mantém esse vínculo é outra
tela, não esta.

[?] A procura do vínculo é posicionada com o **código de gênero FAE zerado** e,
achando o registro, confere apenas o código de subclasse e o código de gênero — o
código FAE do registro achado não é conferido. Se a leitura for pela chave inteira,
só um vínculo com código FAE zero seria encontrado; se for pelo começo da chave, a
tela mostra o vínculo que a leitura devolver. Quantos códigos FAE um gênero pode ter,
e qual deles a tela deve mostrar, é pergunta ao site.

### RN-06 — O vínculo cadastrado manda no resultado, e não o que o servidor digita

Os campos do **código de gênero FAE** e da **unidade de conversão** aceitam digitação
e passam pela conferência de digitação (RN-10), mas não comandam a consulta: a
procura do vínculo não usa o código FAE digitado, e, antes de exibir, a tela substitui
os dois valores pelos que estão no vínculo cadastrado. O que o servidor digitar neles
não muda o resultado.

[?] Se esses campos deveriam servir de filtro — por exemplo, consultar um vínculo
específico pelo código FAE — ou se são campos de resultado que a máscara deixa
digitar, é pergunta ao site.

### RN-07 — A consulta se reabre com o resultado, e é a única saída da tela

Concluída a consulta, a tela monta o registro com os dados achados — o código de
subclasse, o código de gênero, o código de gênero FAE, a unidade de medida do código
FAE e a unidade de conversão — e **entrega esse registro, com a operação de consulta,
a ela mesma**: a mesma tela reabre exibindo o resultado. É a única passagem que ela
faz adiante, e nenhuma outra tela é aberta por causa dela.

[?] A entrega usa o mesmo mecanismo com que os menus abrem a tela seguinte, e o
acervo lido não descreve como o sistema decide entre reabrir a mesma tela e seguir
para outra; o que se lê é que o destino posto é o código desta própria tela. Pergunta
ao site.

### RN-08 — A descrição do gênero FAE ou da unidade de medida ausente não recusa a consulta

Achado o vínculo, a tela busca a **descrição do gênero FAE** no cadastro dos gêneros
FAE e as **descrições das duas unidades de medida** no cadastro das unidades. Não
achando algum desses registros, ela não avisa e não recusa: segue e mostra o que
houver.

[?] A leitura que não acha o registro não é conferida depois, e o que a tela mostra
no lugar da descrição ausente — em branco ou o valor da consulta anterior — não está
no acervo lido. Pergunta ao site.

### RN-09 — Cada consulta começa com os campos de resultado limpos

Antes de conferir a digitação e de ler qualquer cadastro, a tela apaga as descrições
que a consulta anterior havia mostrado. Uma consulta recusada, portanto, não deixa na
tela o resultado da consulta anterior.

[?] A limpeza está amarrada a um tipo de mensagem que o acervo não explica; se existe
um caminho de entrada em que os campos não são limpos, não foi possível determinar.
Pergunta ao site.

### RN-10 — Os campos digitados passam pela conferência de digitação antes das conferências de negócio

Os quatro campos digitáveis — o **código de subclasse** (2 dígitos), o **código de
gênero** (5), a **unidade de conversão** (até 5 inteiros e 3 decimais, com vírgula, e
pode ficar em branco) e o **código de gênero FAE** (7) — passam por uma conferência
numérica **antes** das conferências de negócio desta tela. O campo em branco chega às
conferências valendo zero, e o que não for número é recusado na própria digitação,
sem que a consulta seja feita.

[?] A conferência posiciona o cursor de volta apenas nos dois primeiros campos, o
código de subclasse e o código de gênero; para a unidade de conversão e para o código
de gênero FAE, a recusa não tem posição de cursor declarada neste caminho.

[?] A rotina que faz a conferência de digitação não tem corpo no acervo lido: a
mensagem que o servidor vê na digitação recusada não pôde ser conferida. Pergunta ao
site.

### RN-11 — A consulta não grava nada e não deixa rastro de auditoria

A tela lê o cadastro de gêneros, o cadastro das unidades de medida, o cadastro dos
vínculos do gênero com o código de gênero FAE e o cadastro dos códigos de gênero FAE,
e para aí: nenhum registro é incluído, alterado ou excluído, e nenhum registro de
auditoria é gerado.

## Cenários BDD

```gherkin
Funcionalidade: Consultar o vínculo do gênero com o gênero FAE

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela F022T

  Cenário: RN-01 — consultar um gênero com vínculo cadastrado
    Dado que existe o gênero informado e ele tem vínculo com um código de gênero FAE
    Quando informo o código de subclasse e o código de gênero
    Então vejo a descrição resumida do gênero e a unidade de medida dele
    E vejo o código de gênero FAE vinculado e a descrição dele
    E vejo a unidade de medida do código FAE e a descrição dela
    E vejo a unidade de conversão do vínculo
    E vejo a data do sistema e o tipo de órgão da minha sessão

  Cenário: RN-01 — a descrição do gênero FAE é mostrada em até 56 caracteres
    Dado que o gênero FAE vinculado tem uma descrição com mais de 56 caracteres
    Quando consulto o vínculo
    Então a descrição aparece cortada em 56 caracteres
    E o que passa disso não é mostrado

  Cenário: RN-02 — a tela abre em consulta
    Dado que chego a esta tela pela opção do menu que a abre
    Então ela abre em consulta
    E não há gênero carregado

  Cenário: RN-02 — operação diferente de consulta
    Dado que estou na tela F022T
    Quando o campo da opção traz uma operação que não é a consulta
    Então vejo "* Operacao nao disponivel. Use CON *"
    E o cursor volta ao campo da opção
    E nada é consultado nem gravado

  Cenário: RN-03 — código de subclasse em branco
    Dado que deixo o código de subclasse em branco
    Quando peço a consulta
    Então vejo "* Informe o genero *"
    E o cursor volta ao campo do código de subclasse
    E nada é consultado

  Cenário: RN-03, RN-04 — código de gênero em branco
    Dado que informo o código de subclasse e deixo o código de gênero em branco
    Quando peço a consulta
    Então o par não é encontrado no cadastro de gêneros
    E vejo "* Genero nao cadastrado *"

  Cenário: RN-04 — gênero não cadastrado
    Dado que o par de subclasse e gênero informado não existe no cadastro de gêneros
    Quando peço a consulta
    Então vejo "* Genero nao cadastrado *"
    E o cursor volta ao campo do código de subclasse
    E nada é mostrado

  Cenário: RN-05 — gênero sem vínculo com código de gênero FAE
    Dado que o gênero existe, mas não tem vínculo cadastrado com um código de gênero FAE
    Quando peço a consulta
    Então vejo "* Relacionamentos nao cadastrados *"
    E o cursor volta ao campo do código de subclasse
    E nada é mostrado

  Cenário: RN-06 — o código FAE e a unidade de conversão digitados não mudam o resultado
    Dado que o gênero informado tem um vínculo cadastrado, com o código FAE e a unidade de conversão dele
    Quando digito outro código de gênero FAE e outra unidade de conversão
    Então vejo os valores que estão no vínculo cadastrado
    E não os que digitei

  Cenário: RN-07 — a tela reabre com o resultado da consulta
    Dado que existe o gênero informado e ele tem vínculo com um código de gênero FAE
    Quando a consulta se conclui
    Então a tela reabre com o código de subclasse, o código de gênero, o código FAE e a unidade de conversão carregados
    E a operação que ela entrega é a consulta

  Cenário: RN-07 — a tela não encaminha para outra tela
    Dado que concluo uma consulta
    Então nenhuma outra tela é aberta
    E continuo na tela F022T

  Cenário: RN-08 — gênero FAE sem descrição cadastrada
    Dado que o gênero FAE vinculado não tem descrição no cadastro dos gêneros FAE
    Quando consulto o vínculo
    Então a consulta é feita mesmo assim
    E nenhuma mensagem de recusa é mostrada

  Cenário: RN-08 — unidade de medida não cadastrada
    Dado que a unidade de medida do gênero ou a do código FAE não está cadastrada
    Quando consulto o vínculo
    Então a consulta é feita mesmo assim
    E nenhuma mensagem de recusa é mostrada

  Cenário: RN-09 — os campos da consulta anterior não ficam na tela
    Dado que já mostrei uma consulta anterior
    Quando peço uma nova consulta
    Então as descrições da consulta anterior são apagadas antes das conferências
    E só aparecem as descrições da consulta que passar

  Cenário: RN-10 — campo com texto que não é número
    Dado que digito texto no código de subclasse, no código de gênero, na unidade de conversão ou no código de gênero FAE
    Quando peço a consulta
    Então o campo é recusado na própria digitação
    E a consulta não é feita

  Cenário: RN-11 — a consulta não grava nada
    Dado que existe o gênero informado e ele tem vínculo com um código de gênero FAE
    Quando consulto o vínculo
    Então nenhum cadastro é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado
```
