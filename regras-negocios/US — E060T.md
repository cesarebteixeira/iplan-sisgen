# US — E060T — Prazo, dia da semana e arredondamento por tipo de órgão

## Estória

Como **servidor de CRE**, quero **manter, para o tipo de órgão da minha sessão, o
prazo em dias, o dia da semana de referência e o percentual de arredondamento**,
para que **as telas que calculam data-base, data-limite e quantidade fechada
cheguem sempre ao mesmo resultado, sem depender de quem opera**.

Esses três números não são de um documento nem de uma requisição: são do tipo de
órgão, e valem para tudo o que sai dele. O prazo é o que separa a data-base da
data-limite; o dia da semana é a condição que a data-base precisa atender; e o
percentual de arredondamento é o que fecha a quantidade pedida no múltiplo da
fração do item. Sem eles cadastrados, cada operador calcula do seu jeito e a mesma
requisição sai com datas e quantidades diferentes.

A tela inclui, altera, exclui e consulta **um** conjunto por tipo de órgão. Ela
não pergunta qual é o tipo de órgão — usa o da sessão — e não deixa dois conjuntos
para o mesmo tipo de órgão.

## Contexto

Jornada S000M → E000M → E060M → E060T.

Ator: servidor de CRE — mantém, para o tipo de órgão da sua sessão, o prazo em
dias, o dia da semana de referência e o percentual de arredondamento que as telas
do módulo usam.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual
opção de qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é
**dado de navegação**, não regra de negócio.

O menu `E060M` que abre esta tela só encaminha: não deixa registro nem operação
para ela. Ao abrir, a tela se coloca sozinha em consulta e toma o tipo de órgão que
a entrada deixou na sessão; o comportamento é o mesmo qualquer que seja a tela que
a chamou. Esta tela também não entrega registro nem operação a nenhuma outra:
depois de uma consulta ela reescreve a si mesma, e depois de uma manutenção fica
nela com o aviso.

---

## Regras de negócio

### RN-01 — Os parâmetros são de um tipo de órgão, e o tipo de órgão é o da sessão

Cada tipo de órgão tem **um** conjunto de parâmetros, e não mais de um: o prazo em
dias (até 99), o dia da semana de referência (um nome, de segunda a domingo) e o
percentual de arredondamento (até 99).

O tipo de órgão não é escolhido na tela: é o da sessão. O campo aceita digitação e
passa pela edição numérica, mas o valor digitado é descartado — o que a tela lê,
mostra e grava é sempre o tipo de órgão que a entrada deixou na sessão. As recusas
da tela falam em "secretaria", que é o nome que o sistema dá a esse mesmo cadastro.

[?] Se a intenção era deixar o operador escolher o tipo de órgão por esse campo, o
caminho não o faz: o valor digitado é substituído pelo da sessão antes de qualquer
leitura. Pergunta ao site.

[?] A chave do cadastro é só o tipo de órgão: não há CRE nem órgão filho. Se os
parâmetros deveriam variar por CRE, não há onde guardá-los. Pergunta ao site.

[?] O cadastro de parâmetros declara **onze** campos e esta tela só mostra e grava
**cinco**. O que os outros seis guardam, e quem os mantém, não está nesta jornada.
Pergunta ao site.

### RN-02 — A tela abre em consulta, com os parâmetros do tipo de órgão da sessão

Ao ser aberta, a tela assume a consulta sozinha e mostra o que estiver guardado
para o tipo de órgão da sessão: o prazo, o dia da semana e o percentual. Fora dos
parâmetros, mostra a descrição do tipo de órgão e a data do sistema.

[?] Quando o tipo de órgão ainda não tem parâmetros, a tela não preenche nem limpa
os três campos; o que o operador vê neles não pôde ser determinado pelo acervo.
Pergunta ao site.

### RN-03 — A consulta não grava nada

Na consulta a tela só lê: repõe nos campos o que está guardado, reescreve a si
mesma e devolve o controle ao operador. Nenhum parâmetro é incluído, alterado ou
excluído, e nenhum registro de auditoria é gerado.

### RN-04 — Os três números passam por edição numérica antes das conferências

O tipo de órgão, o prazo e o percentual são tratados como número: campo em branco
vira zero e o que não for número é recusado. O dia da semana não passa por essa
edição — ele é conferido contra a lista de nomes.

[?] O que o operador vê quando a digitação é recusada — se há mensagem, e qual —
não está no acervo lido: a rotina que faz a edição não faz parte do que foi lido. E
não há posição de cursor definida para o campo do tipo de órgão: se a digitação
dele falhar, o cursor não é levado a ele. Pergunta ao site.

### RN-05 — Fora das quatro operações, o sistema recusa com \* Operacao nao disponivel \*

A tela só admite quatro operações: consulta, inclusão, alteração e exclusão. Com
qualquer outra opção, antes de ler ou de gravar qualquer coisa, a recusa é
**\* Operacao nao disponivel \***. Inclusão, alteração e exclusão ainda exigem que
a tela permita manutenção; a consulta não exige.

[?] A recusa é emitida pela lógica comum de rota, que não marca a interrupção que
barraria o trecho que grava: depois dessa recusa a execução segue pelo caminho da
gravação, e a rotina comum de mensagem não está no acervo. Não dá para afirmar,
pelo fonte, se a recusa impede a operação. O mesmo vale para as recusas que a
própria tela emite, adiante. Pergunta ao site.

### RN-06 — A inclusão é recusada quando o tipo de órgão já tem parâmetros

Para incluir, o sistema procura os parâmetros do tipo de órgão da sessão.
Existindo, recusa com **\* Parametros ja cadastrados para esta secretaria \*** e
devolve o cursor ao campo da opção.

### RN-07 — A inclusão exige os dados, o dia da semana da lista e o percentual até 99

Na inclusão, os três dados são conferidos nesta ordem: sem nenhum dos três
preenchido, a recusa é **\* Informe dados para cadastramento \***, com o cursor no
campo do prazo; com o percentual acima de **99**, a recusa é
**\* % de arredondamento invalido \***, com o cursor no campo do percentual; e com
o dia da semana fora de SEGUNDA, TERCA, QUARTA, QUINTA, SEXTA, SABADO e DOMINGO, a
recusa é **\* Dia de semana = SEGUNDA, TERCA, ..., DOMINGO \***, com o cursor no
campo do dia da semana.

O dia da semana é, na prática, sempre obrigatório: o primeiro aviso só sai quando
os três estão vazios, mas a conferência seguinte não deixa passar nenhum valor que
não seja um dos sete nomes.

### RN-08 — A alteração e a exclusão exigem parâmetros já cadastrados

Para alterar ou excluir, o tipo de órgão precisa ter parâmetros guardados. Não
tendo, a recusa é **\* Parametros nao cadastr. para esta secretaria \***, com o
cursor no campo da opção.

### RN-09 — A alteração exige os dados, o dia da semana da lista e o percentual até 99

Na alteração valem as mesmas conferências da inclusão, com o primeiro aviso
trocado: sem nenhum dos três preenchido, a recusa é
**\* Informe dados para atualizacao \***; o percentual acima de 99 e o dia da
semana fora da lista são recusados com as mesmas mensagens e os mesmos cursores da
inclusão.

### RN-10 — A inclusão grava os parâmetros do tipo de órgão

Passando nas conferências, a inclusão grava um conjunto novo de parâmetros para o
tipo de órgão da sessão, com o prazo, o dia da semana e o percentual informados.

[?] A inclusão não tem aviso de sucesso no programa — a alteração e a exclusão têm.
Se o aviso vem do ambiente, não está no acervo. Pergunta ao site.

[?] A criação do registro e a gravação dele são dois passos separados na inclusão,
e o segundo acontece mesmo quando o primeiro falha — por exemplo, se o registro
aparecer entre a conferência e a gravação. O que o operador vê nesse caso não está
no acervo. Pergunta ao site.

### RN-11 — A alteração grava e avisa; a exclusão apaga e avisa

Na alteração, o registro é travado e regravado com os três valores informados, e o
aviso é **\* Alteracao realizada \***. Na exclusão, o registro é travado e apagado,
e o aviso é **\* Exclusao realizada \***.

### RN-12 — Sem autorização para a tela ou para a operação, nada acontece

A tela só abre para o código de acesso que a tem autorizada no cadastro de telas
por código de acesso; não tendo, a recusa é
**\* Acesso negado para esta matricula \***.

E, antes de qualquer leitura de cadastro, a operação informada passa pela
segurança: inclusão, alteração e exclusão exigem, cada uma, o seu flag liberado
para aquele código de acesso naquela tela; não estando, a recusa é
**\* Acesso negado para esta operacao \***, a operação é abandonada e o servidor
volta ao menu principal. A consulta passa sem exigir flag nenhum.

[?] A conferência não olha o flag da consulta, e uma opção que não seja nenhuma das
quatro também passa por ela sem conferência de flag. Se a intenção era exigir o
flag de consulta por tela, o caminho não o exige. Pergunta ao site.

### RN-13 — O tipo de órgão da sessão precisa estar cadastrado e ativo

Antes de gravar, o tipo de órgão da sessão é procurado no cadastro de secretarias.
Não estando cadastrado, o sistema acusa o campo; estando marcado como excluído ou
purgado, a recusa sai pelo canal de checagem de campo — o mesmo que o sistema usa
quando o valor informado não existe.

[?] O texto dessa recusa não está no acervo lido. E a conferência não interrompe o
trecho que grava: ela acontece depois do processamento e imediatamente antes da
gravação, na mesma execução. Não dá para afirmar, pelo fonte, se a recusa impede a
operação. Pergunta ao site.

### RN-14 — Toda operação fica registrada na auditoria

Inclusão, alteração e exclusão gravam, além dos parâmetros, um registro de
auditoria com a tela de origem, a operação, os valores **antes** e **depois**, a
matrícula, a estação, a CRE, o tipo de órgão, o número do processo e a data e a
hora da sessão. Na inclusão o "antes" vai em branco; na exclusão o "depois" vai em
branco. A consulta não gera registro de auditoria.

[?] O cadastro de parâmetros tem um marcador de uma posição que a inclusão grava em
branco, a alteração grava como **A** e a exclusão grava como **D** — e esse **D** é
escrito antes de o registro ser apagado, sem ir para a auditoria. O que o marcador
significa, e o que acontece com a inclusão, que o deixa em branco embora o
dicionário o declare obrigatório, é pergunta ao site.

---

## Cenários BDD

```gherkin
Funcionalidade: Prazo, dia da semana e arredondamento por tipo de órgão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E tenho acesso à tela E060T

  Cenário: Consulta dos parâmetros do tipo de órgão da sessão
    Dado que o tipo de órgão da minha sessão já tem parâmetros cadastrados
    Quando abro a tela
    Então ela abre em consulta
    E vejo o prazo em dias, o dia da semana e o percentual de arredondamento guardados
    E vejo a descrição do tipo de órgão e a data do sistema

  Cenário: A consulta não grava nada
    Dado que o tipo de órgão da minha sessão já tem parâmetros cadastrados
    Quando consulto os parâmetros
    Então nenhum parâmetro é incluído, alterado ou excluído
    E nenhum registro de auditoria é gerado

  Cenário: Inclusão de um conjunto novo de parâmetros
    Dado que o tipo de órgão da minha sessão ainda não tem parâmetros
    Quando informo a inclusão com um prazo em dias, um dia da semana da lista e um percentual até 99
    Então o sistema grava os parâmetros do tipo de órgão da minha sessão
    E registra a operação na auditoria

  Cenário: Inclusão recusada porque o tipo de órgão já tem parâmetros
    Dado que o tipo de órgão da minha sessão já tem parâmetros cadastrados
    Quando tento incluir
    Então vejo a mensagem "* Parametros ja cadastrados para esta secretaria *"
    E o cursor volta ao campo da opção

  Cenário: Inclusão sem nenhum dado
    Dado que o tipo de órgão da minha sessão ainda não tem parâmetros
    Quando peço a inclusão sem preencher o prazo, o dia da semana e o percentual
    Então vejo a mensagem "* Informe dados para cadastramento *"
    E o cursor volta ao campo do prazo

  Cenário: Percentual de arredondamento acima de 99
    Quando peço a inclusão ou a alteração com um percentual maior que 99
    Então vejo a mensagem "* % de arredondamento invalido *"
    E o cursor volta ao campo do percentual

  Cenário: Dia da semana fora da lista
    Quando peço a inclusão ou a alteração com um dia da semana que não é um dos sete nomes
    Então vejo a mensagem "* Dia de semana = SEGUNDA, TERCA, ..., DOMINGO *"
    E o cursor volta ao campo do dia da semana

  Cenário: Alteração dos parâmetros
    Dado que o tipo de órgão da minha sessão já tem parâmetros cadastrados
    Quando informo a alteração com novos valores
    Então o sistema grava os parâmetros com os valores informados
    E vejo a mensagem "* Alteracao realizada *"
    E registra a operação na auditoria

  Cenário: Alteração ou exclusão de tipo de órgão sem parâmetros
    Dado que o tipo de órgão da minha sessão não tem parâmetros cadastrados
    Quando tento alterar ou excluir
    Então vejo a mensagem "* Parametros nao cadastr. para esta secretaria *"
    E o cursor volta ao campo da opção

  Cenário: Alteração sem nenhum dado
    Dado que o tipo de órgão da minha sessão já tem parâmetros cadastrados
    Quando peço a alteração sem preencher o prazo, o dia da semana e o percentual
    Então vejo a mensagem "* Informe dados para atualizacao *"
    E o cursor volta ao campo do prazo

  Cenário: Exclusão dos parâmetros
    Dado que o tipo de órgão da minha sessão já tem parâmetros cadastrados
    Quando informo a exclusão
    Então o sistema apaga os parâmetros
    E vejo a mensagem "* Exclusao realizada *"
    E registra a operação na auditoria

  Cenário: Opção de manutenção fora das quatro
    Quando informo uma opção que não é consulta, inclusão, alteração nem exclusão
    Então vejo a mensagem "* Operacao nao disponivel *"

  Cenário: Operação não autorizada para o meu código de acesso
    Dado que o meu código de acesso não tem o flag da operação pretendida nessa tela
    Quando tento incluir, alterar ou excluir
    Então vejo a mensagem "* Acesso negado para esta operacao *"
    E nada é gravado

  Cenário: Tela não autorizada para o meu código de acesso
    Dado que o meu código de acesso não tem a tela E060T autorizada
    Quando tento abrir a tela
    Então vejo a mensagem "* Acesso negado para esta matricula *"
    E não consigo operar

  Cenário: Tipo de órgão excluído no cadastro de secretarias
    Dado que o tipo de órgão da minha sessão está marcado como excluído ou purgado
    Quando tento incluir, alterar ou excluir os parâmetros
    Então o sistema acusa o campo do tipo de órgão
    E a gravação não é confirmada

  Cenário: Toda operação deixa rastro de auditoria
    Dado que a operação passou em todas as conferências
    Quando incluo, altero ou excluo os parâmetros
    Então um registro de auditoria é gravado com a operação, os valores antes e depois,
      a matrícula, a estação, a CRE, o tipo de órgão e a data e a hora da sessão
    E na inclusão o "antes" fica em branco
    E na exclusão o "depois" fica em branco

  Cenário: Prazo ou percentual que não é número
    Quando digito um prazo ou um percentual que não é número
    Então o cursor volta ao campo recusado
```
