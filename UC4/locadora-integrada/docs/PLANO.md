# O plano da locadora, issue por issue

Na Aula 05 eu abro o quadro de issues de vocês e pergunto três coisas: **o que
foi planejado, o que fechou, e o que saiu, e por quê.** Este é o quadro da
locadora, de um grupo de três (Ana, Bruno e Carla), respondendo às três.

O zip não leva o quadro do GitHub junto, então ele está escrito aqui. No
repositório de vocês, cada linha das tabelas abaixo é uma **issue**, e não um
parágrafo no README.

Antes de ler, um palpite: das 24 issues, quantas vocês acham que fecharam? E
quantas saíram da versão?

O grupo de vocês não precisa de seis histórias. A locadora tem seis porque é
o exemplo de todas as tarefas; o projeto de um grupo cabe em duas ou três.

---

## Como se lê uma issue

```
#11 Alugar e devolver, no banco
    História:   H3 — alugar e devolver
    Critério:   o jogo alugado some da lista de disponíveis, e volta na devolução
    Rótulo:     dados          Responsável: Bruno        Milestone: Aula 04
    Fechada por: "Grava o emprestimo e os itens num commit so (fixes #11)"
```

- **Rótulo** é a camada: `regra`, `dados` ou `interface`.
- **Responsável** é o *Assignee*: uma pessoa, não "todos".
- **Milestone** é o prazo: `Aula 02`, `Aula 03`, `Aula 04` e `Depois`.
- O commit com `fixes #11` fecha a issue sozinho, como na UC3.

---

## O problema e as histórias

O problema está no [`README.md`](../README.md), na seção **O problema**: o dono
não sabe quem está com jogo atrasado. As histórias:

| História | Do jeito *como… quero… para…* | Milestone |
|---|---|---|
| **H1** jogos | Como atendente, quero cadastrar, achar, alterar e apagar jogos na janela, para a lista estar certa no dia em que o jogo chega. | Aula 03 |
| **H2** clientes | Como atendente, quero cadastrar o cliente no balcão, para alugar para quem chega pela primeira vez. | Aula 03 |
| **H3** alugar e devolver | Como atendente, quero registrar o aluguel e a devolução, para saber que jogo está com quem. | Aula 04 |
| **H4** atrasados | Como atendente, quero ver os empréstimos atrasados e a multa de cada um, para cobrar no balcão sem abrir o caderno. | Aula 04 |
| **H5** resumo | Como dono, quero ver o que mais sai e quanto há a cobrar, para decidir o que comprar. | Aula 04 |
| **H6** configurações | Como dono, quero mudar a multa sem chamar o programador, para a regra acompanhar a loja. | Aula 04 |

A H4 é a que responde "como saber que resolveu". As outras existem para ela
ter dado de verdade.

---

## Milestone `Aula 02` — o projeto organizado

A suíte da UC3 tinha **5 verdes** no começo da aula (3 da multa, 2 do CRUD de
jogo). No fim tem de ter os mesmos 5.

| # | Issue | Rótulo | Quem | Critério | Estado |
|---|---|---|---|---|---|
| 1 | Tirar o CRUD de jogo do notebook para `locadora/dados.py` | dados | Bruno | nenhum `SELECT` fora do `dados.py`; nenhum `print` nem `input`; a conexão chega por parâmetro | fechada |
| 2 | Conectar pelo `.env`, com o `.env.exemplo` no repositório | dados | Carla | sem o `.env`, o sistema avisa em português o que fazer; o `.env` está no `.gitignore` | fechada |
| 3 | Levar a multa para `locadora/regras.py` e os testes para `tests/` | regra | Ana | a suíte acha o pacote `locadora` (o `pyproject.toml`) e continua com **5 verdes** | fechada |

```
Tira o CRUD de jogo do notebook para locadora/dados.py (fixes #1)
Le a senha do .env e poe o .env.exemplo no repositorio (fixes #2)
Leva multa e valor_do_aluguel para regras.py; tests/ acha o pacote (fixes #3)
```

---

## Milestone `Aula 03` — H1 e H2, com a janela

Os critérios de aceitação viraram testes **antes** da janela existir.

| # | Issue | Rótulo | Quem | Critério | Estado |
|---|---|---|---|---|---|
| 4 | Conferir o jogo digitado (`validar_jogo`, `preparar_jogo`) | regra | Ana | título em branco, ano com letra ou até 1970, preço com letra ou negativo: recusados, com aviso em português | fechada |
| 5 | Buscar e alterar jogo no banco | dados | Bruno | a busca ignora maiúscula; o título repetido é recusado pelo banco | fechada |
| 6 | A aba Jogos: formulário, busca e tabela | interface | Bruno | a aba só chama `regras` e `dados`; o erro do banco vira aviso, e não erro no terminal | fechada |
| 7 | A janela com as abas, aberta pelo `main.py` | interface | Carla | o ▶ no `main.py` abre a janela; a conexão fecha quando a janela fecha | fechada |
| 8 | Cliente: conferir e gravar | dados | Ana | e-mail sem @ é recusado; e-mail vazio vira NULL; cliente desativado sai da lista | fechada |
| 9 | A aba Clientes | interface | Carla | cliente com aluguel no histórico se desativa, não se apaga | fechada |

---

## Milestone `Aula 04` — H3 a H6, o teste cruzado e a versão

| # | Issue | Rótulo | Quem | Critério | Estado |
|---|---|---|---|---|---|
| 10 | Conferir o aluguel e calcular o total | regra | Ana | sem cliente, sem jogo ou com zero dias: recusado; o total é a diária de cada jogo pelos dias | fechada |
| 11 | Alugar e devolver, no banco | dados | Bruno | o jogo alugado some dos disponíveis e volta na devolução; a multa fica gravada | fechada |
| 12 | A aba Aluguéis | interface | Carla | vários jogos num aluguel só; o total aparece no aviso | fechada |
| 13 | Quem está atrasado, e quanto deve | regra | Ana | devolvido não aparece; 2 dias de atraso, R$ 0,00; 3 dias, R$ 15,00 | fechada |
| 14 | A aba Atrasados | interface | Bruno | sem ninguém atrasado, a tela diz "Nenhum atraso hoje", e não fica em branco | fechada |
| 15 | A aba Resumo, com a pizza e as barras | interface | Carla | cada fatia tem o nome e o número escritos: a cor sozinha não basta | fechada |
| 16 | A tabela `configuracao` e a aba Configurações | dados | Bruno | multa negativa é recusada pelo banco; a frase de exemplo acompanha o que foi digitado | fechada |
| 17 | O mesmo sistema no terminal | interface | Ana | `terminal.py` e `terminal_rich.py` fazem tudo o que a janela faz, com as mesmas `regras` e `dados` | fechada |
| 18 | Enter não cadastrava *(do teste cruzado)* | interface | Bruno | Enter em qualquer campo cadastra, sem precisar do mouse | fechada |
| 19 | A lista de jogos não rolava *(do teste cruzado)* | interface | Carla | toda tabela tem barra de rolagem | fechada |
| 20 | "R$ 6,50" na diária é recusado *(do teste cruzado)* | regra | Ana | aceitar o "R$" que a atendente digita | **Depois** |
| 21 | Erro desconhecido do banco aparece em texto técnico | interface | Carla | todo aviso que chega à atendente está em português de balcão | **Depois** — defeito conhecido |
| 22 | Paginação das tabelas | interface | Bruno | com centenas de jogos, a tabela mostra de 20 em 20 | **Depois** |
| 23 | O GitHub roda os testes de regra a cada push *(opcional)* | regra | Bruno | o ✓ verde aparece no commit | fechada |
| 24 | A camada de dados também com Peewee, para comparar *(opcional)* | dados | Ana | a mesma suíte de dados passa no `dados.py` e no `dados_peewee.py` | fechada |

A suíte na `v2.0.0`: **58 verdes** — 26 de regra e 16 de dados, que rodam duas
vezes, uma com cada versão da camada de dados.

### Por que três issues saíram

O comentário em cada uma, escrito às 20h do dia 24/11:

> **#20** — Sai da v2.0.0. O aviso já mostra o exemplo "8,50", e a pessoa do
> teste cruzado acertou na segunda tentativa. Aceitar o "R$" mexe na regra e
> nos testes dela; entra na v2.1.0.
>
> **#21** — Sai, e entra no Release como defeito conhecido. O título repetido
> e o jogo já alugado já viram aviso; o erro que sobra é raro, e consertar
> hoje seria mexer em todas as abas na véspera da demonstração.
>
> **#22** — Sai. Com o acervo de hoje, a barra de rolagem da #19 resolve.
> Paginação é `LIMIT`/`OFFSET` no SQL e dois botões em cada aba: fica para
> quando o acervo pedir.

Cortar com motivo escrito também é cumprir o plano. O que não pode é a issue
sumir.

### O que o teste cruzado mudou

A tarefa, em linguagem do balcão: *"cadastre o jogo Hollow Knight, de 2017, a
R$ 6,50 a diária"*. A pessoa de outro grupo:

1. digitou tudo e apertou **Enter**. Nada aconteceu, e ela procurou o botão
   (virou a #18);
2. procurou o jogo novo na lista e não achou: ele estava embaixo, e a lista não
   rolava (virou a #19);
3. escreveu **"R$ 6,50"** na diária e recebeu "tem de ser um número" (virou a
   #20). O aviso já mostra o exemplo "8,50", e na segunda tentativa ela
   acertou. Por isso a #20 pôde esperar, e a #18 e a #19 não.

---

## O quadro no fim da Aula 04

| | Aula 02 | Aula 03 | Aula 04 | Depois |
|---|---|---|---|---|
| planejadas na Aula 01 | 3 | 6 | 8 | |
| nasceram no caminho | 0 | 0 | 7 | |
| fechadas | 3 | 6 | 12 | |
| movidas para **Depois** | 0 | 0 | 3 | **3** abertas, com motivo |

Ana tem 8 issues, Bruno 9 e Carla 7: ninguém com tudo, ninguém sem nada.

---

## O Release da `v2.0.0`

As três linhas, no Release do GitHub:

> **Entrou:** jogos, clientes, aluguel e devolução, os atrasados com a multa,
> o resumo e as configurações — na janela e no terminal.
> **Ficou para depois:** aceitar "R$" na diária (#20); paginação (#22).
> **Defeito conhecido:** quando o banco recusa por um motivo que a janela não
> conhece, o aviso mostra o texto técnico do PostgreSQL (#21).

---

## E o de vocês?

Ponham o quadro de vocês ao lado deste e confiram:

- Cada issue tem **um** dono, um milestone e um rótulo?
- O critério diz o que a atendente vê, ou só "fazer a tela"?
- Alguma issue foi apagada, em vez de ir para **Depois** com comentário?
- Qual travada do teste cruzado virou conserto, e qual esperou? Por quê?
