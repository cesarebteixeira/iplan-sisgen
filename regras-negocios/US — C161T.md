# US — C161T — Manter os segmentos do órgão

## Estória

Como **servidor de CRE**, quero **manter os segmentos do órgão da minha sessão — incluir,
alterar e excluir cada segmento, com a sua descrição, a sua descrição resumida e o seu
indicador de creche**, para que os grupos de atendimento e os atendimentos fiquem
classificados no segmento certo e as telas que os registram encontrem a descrição do
segmento.

O segmento é uma das classificações do órgão. Grupos de atendimento e atendimentos são
cadastrados presos a um órgão e a um segmento dele, e as telas que os registram procuram o
segmento pelo código para mostrar a sua descrição resumida; quando o segmento não existe,
essas telas recusam o registro. Por isso esta tela existe: sem o segmento cadastrado, o que
depende dele fica sem classificação. E, uma vez que o segmento tenha grupo de atendimento ou
atendimento, esta tela não o apaga — ela avisa e a exclusão é recusada.

## Contexto

Jornada S000M → C000M → C028M → C029M → C161T.

Ator: servidor de CRE — mantém, para o órgão da sua sessão, o cadastro dos segmentos:
inclui, altera e exclui segmentos e marca quais deles são creche.

A entrada — o `LOGON` e o menu principal `S000M` — está em
`Documents/jornadas/US — 00 Entrada (LOGON, S000M).md`. O caminho até a tela — qual opção de
qual menu a abre — está em `Documents/jornadas/00 Navegação e menus.md`: é **dado de
navegação**, não regra de negócio.

A C161T é a última tela da jornada: ela não leva a outra tela. As telas anteriores são
menus, e cada uma só escolhe a tela seguinte; nenhuma delas entrega um registro ou um modo de
operação à C161T — a tela abre pela própria máscara, e o modo (alteração ou consulta) é o que
se informa nela mesma. O que a C161T usa — a matrícula, o acesso, o privilégio, o órgão e a
CRE — é o que a entrada deixou na sessão.

As regras abaixo são só as da tela desta jornada. O cadastro que ela mantém vale para o órgão
que a sessão do servidor carrega: a tela não deixa escolher outro.

---

## Regras de negócio

### RN-01 — A tela mantém os segmentos do órgão da sessão

O cadastro que a C161T mantém é o de **segmentos**: o **código do segmento** (2 dígitos), a
**descrição** (30 caracteres), a **descrição resumida** (15 caracteres) e o **indicador de
creche**. Cada segmento pertence a um **órgão**, e é o órgão da sessão do servidor que decide
o conjunto que a tela enxerga — o mesmo par órgão + código de segmento não se repete no
cadastro. A capacidade declarada é de **200.000** registros — **capacidade** (máximo esperado,
parâmetro de dimensionamento), não volume cadastrado.

A tela apresenta **15 linhas** por vez; cada linha tem **6 valores**: o código do segmento, a
descrição, a descrição resumida, o indicador de creche, o texto **Sim** ou **Nao** que a tela
escreve no lugar do indicador e a ação. O cabeçalho tem **7 campos** — a identificação da
tela, a origem, o número da transação, a data de entrada, o mês de referência, a opção de
manutenção e o prefixo de tela —, e a tela ainda mostra a identificação do órgão da sessão e
a data do sistema. A página é montada percorrendo o cadastro do órgão da sessão na ordem do
código do segmento, e a varredura para no primeiro registro de outro órgão.

[?] A identificação do órgão e a data do sistema que a tela mostra vêm da área da sessão, e os
programas desta jornada só as inicializam em branco: quem as preenche não está no material
lido. Pergunta ao site.

[?] Como se vê o resto da lista quando o órgão tem mais de 15 segmentos: a página monta 15
linhas e para. Há no programa um mecanismo de janela, sem significado no material lido.
Pergunta ao site.

### RN-02 — A tela só trabalha em alteração ou em consulta

A opção de manutenção da página aceita **dois valores**: alteração e consulta — os mesmos que
a mensagem de recusa nomeia como **ALT** e **CON**. Qualquer outro valor é recusado com
**\* Operacao nao disponivel. Use ALT ou CON \***, com o cursor no campo da opção, e nada é
validado nem gravado. Quando a página abre sem opção informada, a própria tela assume a
**consulta**.

[?] A mensagem manda usar **ALT** e **CON**, mas os valores que a tela confere são os códigos
de alteração e de consulta do sistema. Ou a máscara traduz o mnemônico antes de enviar, ou a
mensagem está desalinhada da guarda. A máscara não está no material lido. Pergunta ao site.

### RN-03 — A ação da linha inclui, altera ou exclui

Cada linha da página tem uma ação de uma posição: **I**, para incluir o segmento, **A**, para
alterar o segmento já cadastrado, ou **E**, para excluir o segmento. Esta tela **exclui**: a
ação **E** apaga o segmento do cadastro, depois de conferir que nada depende dele (RN-11).

### RN-04 — Linha sem código de segmento ou com ação desconhecida passa em claro

Uma linha só é processada quando tem o **código do segmento** preenchido **e** a ação **I**,
**A** ou **E**. Código zerado, ação em branco ou ação diferente dessas três passa em claro: a
linha não é validada, não grava nada e não gera aviso ao usuário.

[?] Recusada uma linha, as outras linhas da mesma página ainda são gravadas? O caminho de
gravação não reconfere o indicador de erro que a validação da linha preenche, e esse
indicador é lido por rotina global: ou a página inteira é perdida, ou as demais linhas
seguem. Pergunta ao site.

### RN-05 — Na inclusão, o segmento não pode existir

Para incluir, o segmento informado na linha é procurado no cadastro do órgão da sessão. Se já
existir, a inclusão é recusada com **\* Segmento ja cadastrado \***, com o cursor na coluna da
ação, e nada é gravado. A chave do cadastro é sem duplicidade, de modo que o mesmo código de
segmento existe uma vez só por órgão — e, se a gravação ainda assim encontrar o registro, ela
trata como falha.

### RN-06 — Na alteração e na exclusão, o segmento tem de existir

Para alterar ou excluir, o segmento informado na linha também é procurado. Não existindo, a
operação é recusada com **\* Segmento nao cadastrado \***, com o cursor na coluna da ação, e
nada é gravado nem apagado.

### RN-07 — Na inclusão e na alteração, a descrição, a descrição resumida e a creche são obrigatórias

Nas duas operações que gravam os dados do segmento, a tela exige a **descrição**
(**\* Informe a descricao \***), a **descrição resumida**
(**\* Informe a descricao resumida \***) e o **indicador de creche** informado como **S** ou
**N** (**\* Informe se creche ou nao com S ou N \***). Cada recusa deixa o cursor na coluna do
campo que falta. A exclusão não pede nenhum deles.

### RN-08 — A inclusão cria o segmento no órgão da sessão

A ação **I** cria o registro do segmento com o código e as descrições informados na linha, o
indicador de creche e o **órgão da sessão**. O órgão não é digitado na tela: é o que a entrada
deixou na sessão, e é ele que decide a que órgão o segmento novo passa a pertencer.

### RN-09 — A alteração grava a nova descrição, a resumida e a creche

A ação **A** vira alteração: o sistema lê o registro do segmento, guarda o valor anterior,
trava o registro, substitui a descrição, a descrição resumida e o indicador de creche pelos
que estão na linha e grava. O código do segmento é a identidade do registro — a alteração não
o muda, nem muda o órgão a que ele pertence.

### RN-10 — A exclusão apaga o segmento

A ação **E** vira exclusão: o sistema lê o registro do segmento, guarda o valor anterior,
trava e apaga o registro. A exclusão apaga **só** o segmento: não apaga grupos de atendimento
nem atendimentos.

### RN-11 — O segmento com grupo de atendimento ou com atendimento não é excluído

Antes de apagar, o sistema procura **grupos de atendimento** do órgão e do segmento. Achando
algum, recusa com **\* Nao exclua. Grupos atendimento neste segmento \***, com o cursor na
coluna do código do segmento, e nada é apagado. Sem grupo, procura **atendimentos** do órgão
e do segmento; achando algum, recusa com
**\* Nao exclua. Atendimentos neste segmento \***, também com o cursor na coluna do código. Só
sem nenhum dos dois o segmento é apagado.

[?] A recusa por grupo de atendimento e por atendimento fica na passagem em que a linha é
validada; a passagem que grava apaga o segmento sem reconferir os dois cadastros, e a tela não
marca o erro geral da transação ao recusar. Se a mensagem não marcar esse erro, o aviso não
impede a exclusão. Quem marca o erro geral é rotina global, fora do material lido. Pergunta
ao site.

### RN-12 — Na consulta nada é gravado

Com a opção de manutenção em consulta, o processamento das linhas é abandonado antes de
qualquer validação de ação e antes de qualquer gravação — na passagem de validação e na de
gravação. A consulta é somente leitura: percorrer a página não inclui, não altera, não exclui
e não deixa rastro de auditoria.

### RN-13 — Órgão sem segmentos cadastrados é avisado

Quando a página é montada e o órgão da sessão não tem nenhum segmento cadastrado, a tela não
mostra linha alguma e avisa **\* Nao existem segmentos cadastrados \***, com o cursor na
coluna do código do segmento. É o mesmo caminho de uma tela que abre sem nada a listar.

### RN-14 — Toda operação deixa rastro na auditoria

Cada inclusão, cada alteração e cada exclusão grava também um registro na trilha de auditoria:
o cadastro de origem, a operação (inclusão, alteração ou exclusão), o órgão da sessão, o valor
anterior e o posterior e o contexto da sessão — matrícula, secretaria, CRE, terminal, data e
hora e o número do processo. Na inclusão o valor anterior vai em branco e o posterior é o
segmento criado; na alteração o anterior é o segmento como estava e o posterior é o segmento
com os valores novos; na exclusão o valor posterior vai em branco.

[?] O rastro da inclusão só é escrito se o estado devolvido pela gravação do segmento não for
um valor específico do sistema; na alteração e na exclusão o rastro é incondicional. Esse
estado vem do ambiente e não está no material lido. Se a guarda barrar, a inclusão grava o
segmento sem rastro. Pergunta ao site.

### RN-15 — Nada é gravado sem as conferências de tela, de rota e de permissão

Antes de validar as linhas e antes de gravar, a tela publica o contexto da sessão — a
matrícula, o acesso, o privilégio, o órgão e a CRE — e chama as rotinas de rota e de segurança
de perfil e de permissão por operação; na montagem da página, passa também pela segurança de
tela. Se qualquer uma delas não aprovar, a tela sai sem validar e sem gravar, e nada é
auditado. A permissão é conferida para a operação que a linha pede: incluir, alterar ou
excluir.

[?] As rotinas de segurança e de rota só aparecem declaradas nos programas; a fonte e a regra
efetiva de permissão não estão no material lido. Pergunta ao site.

### RN-16 — Prefixo de tela preenchido abandona a manutenção

Se a transação chega com o **prefixo de tela** preenchido, a validação da manutenção é
interrompida antes de qualquer teste de ação: a linha não é validada, a transação é desviada
para a tela indicada no prefixo e nada é gravado. O prefixo é usado como contexto de rota.

[?] Não se sabe quem preenche o prefixo de tela nesta tela: nenhum programa do acervo atribui
valor a ele, e o menu que abre a C161T não o preenche. Pergunta ao site.

### RN-17 — A recusa de destino inválido não é alcançada pela tela

O ramo que produz a recusa de **destino inválido** (a distribuição automática entre destinos)
só roda se o modo de distribuição automática estiver preenchido; a C161T limpa esse campo
imediatamente antes de todos os pontos em que ele poderia disparar. Pela C161T, portanto, a
mensagem de destino inválido que a ficha da tela lista **não** é apresentada.

[?] A ficha do grafo lista essa recusa para esta tela, mas o programa não alcança o ramo:
divergência entre a ficha e o comportamento, a confirmar com quem mantém o grafo.

---

## Cenários BDD

```gherkin
Funcionalidade: Manter os segmentos do órgão

  Contexto:
    Dado que entrei pelo LOGON com matrícula, senha e secretaria válidas
    E que a minha sessão carrega o órgão
    E tenho acesso à tela C161T

  Cenário: A tela lista os segmentos do meu órgão
    Dado que estou na tela C161T
    Quando a página é apresentada
    Então vejo até 15 linhas, cada uma com o código do segmento, a descrição, a descrição resumida, o indicador de creche, o texto Sim ou Nao e a ação
    E vejo a opção de manutenção, a identificação do órgão e a data do sistema
    E só aparecem segmentos do órgão da minha sessão
    E o cadastro comporta até 200.000 segmentos

  Cenário: A tela abre em consulta e a consulta não grava nada
    Dado que estou na tela C161T sem informar a opção de manutenção
    Quando percorro e valido as linhas da página
    Então a tela assume a consulta
    E nenhum segmento é incluído, alterado ou excluído
    E nenhum registro de auditoria é criado

  Cenário: Opção de manutenção diferente de ALT e de CON é recusada
    Dado que estou na tela C161T
    Quando informo uma opção de manutenção diferente de ALT e de CON
    Então vejo "* Operacao nao disponivel. Use ALT ou CON *"
    E o cursor fica no campo da opção
    E nada é gravado

  Cenário: Inclusão de um segmento
    Dado que estou na tela C161T no modo ALT
    Quando informo o código de um segmento que não existe, a descrição, a descrição resumida, a creche com S ou N e a ação I
    Então o segmento é incluído no órgão da minha sessão
    E a inclusão fica registrada na auditoria

  Cenário: Inclusão recusa segmento já cadastrado
    Dado que estou na tela C161T no modo ALT
    Quando informo a ação I para um código de segmento que já existe
    Então vejo "* Segmento ja cadastrado *"
    E o cursor fica na coluna da ação
    E o segmento existente não é alterado

  Cenário: Alteração de um segmento
    Dado que estou na tela C161T no modo ALT
    E que o segmento está cadastrado
    Quando informo a nova descrição, a nova descrição resumida, a nova creche e a ação A
    Então os novos valores são gravados
    E o código do segmento e o órgão dele não mudam
    E a alteração fica registrada na auditoria

  Cenário: Alteração recusa segmento não cadastrado
    Dado que estou na tela C161T no modo ALT
    Quando informo a ação A para um código de segmento que não existe
    Então vejo "* Segmento nao cadastrado *"
    E o cursor fica na coluna da ação
    E nada é gravado

  Cenário: Exclusão de um segmento
    Dado que estou na tela C161T no modo ALT
    E que o segmento está cadastrado e não tem grupo de atendimento nem atendimento
    Quando informo a ação E
    Então o segmento é apagado
    E a exclusão fica registrada na auditoria

  Cenário: Exclusão recusa segmento não cadastrado
    Dado que estou na tela C161T no modo ALT
    Quando informo a ação E para um código de segmento que não existe
    Então vejo "* Segmento nao cadastrado *"
    E o cursor fica na coluna da ação
    E nada é apagado

  Cenário: Exclusão recusada quando há grupo de atendimento
    Dado que estou na tela C161T no modo ALT
    E que existe grupo de atendimento para o segmento
    Quando informo a ação E
    Então vejo "* Nao exclua. Grupos atendimento neste segmento *"
    E o cursor fica na coluna do código do segmento
    E o segmento continua cadastrado

  Cenário: Exclusão recusada quando há atendimento
    Dado que estou na tela C161T no modo ALT
    E que existe atendimento para o segmento e nenhum grupo de atendimento
    Quando informo a ação E
    Então vejo "* Nao exclua. Atendimentos neste segmento *"
    E o cursor fica na coluna do código do segmento
    E o segmento continua cadastrado

  Cenário: Inclusão e alteração exigem a descrição
    Dado que estou na tela C161T no modo ALT
    Quando tento incluir ou alterar um segmento sem a descrição
    Então vejo "* Informe a descricao *"
    E o cursor fica na coluna da descrição
    E nada é gravado

  Cenário: Inclusão e alteração exigem a descrição resumida
    Dado que estou na tela C161T no modo ALT
    Quando tento incluir ou alterar um segmento sem a descrição resumida
    Então vejo "* Informe a descricao resumida *"
    E o cursor fica na coluna da descrição resumida
    E nada é gravado

  Cenário: Inclusão e alteração exigem a creche marcada com S ou N
    Dado que estou na tela C161T no modo ALT
    Quando tento incluir ou alterar um segmento com a creche em branco ou com outra letra
    Então vejo "* Informe se creche ou nao com S ou N *"
    E o cursor fica na coluna da creche
    E nada é gravado

  Cenário: Linha sem código ou com ação desconhecida é ignorada
    Dado que estou na tela C161T no modo ALT
    Quando deixo o código do segmento em branco, ou a ação em branco, ou informo uma ação que não é I, A nem E
    Então a linha não é validada, não grava nada e não gera aviso

  Cenário: Órgão sem segmentos cadastrados é avisado
    Dado que estou na tela C161T e o meu órgão não tem segmento cadastrado
    Quando a página é apresentada
    Então vejo "* Nao existem segmentos cadastrados *"
    E o cursor fica na coluna do código do segmento

  Cenário: Toda operação deixa rastro na auditoria
    Dado que confirmei uma inclusão, uma alteração ou uma exclusão na C161T
    Quando a gravação termina
    Então existe um registro de auditoria do segmento
    E com a operação e os valores anterior e posterior
    E com a matrícula, a secretaria, a CRE, o terminal e a data e hora

  Cenário: Nada é gravado sem a conferência de tela, de rota e de permissão
    Dado que estou na tela C161T
    Quando a checagem de tela, de rota ou de permissão não retorna OK
    Então a tela volta sem validar e sem gravar nada
    E nenhum registro de auditoria é criado

  Cenário: Prefixo de tela preenchido abandona a manutenção
    Dado que a transação chega à C161T com prefixo de tela preenchido
    Quando a validação da manutenção começaria
    Então a linha não é validada
    E a transação é desviada para a tela indicada no prefixo
    E nada é gravado

  Cenário: A tela não apresenta a recusa de destino inválido
    Dado que estou na tela C161T e confirmei uma operação
    Quando a gravação é preparada
    Então a tela limpa o modo de distribuição automática
    E a recusa de destino inválido não é apresentada
```
