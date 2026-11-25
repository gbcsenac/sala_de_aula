# Locadora — balcão

O sistema do balcão da locadora: jogos, clientes, aluguel e devolução, os
atrasados com a multa, um resumo para o dono e as configurações da loja. É o
exemplo da UC4 (Projeto Integrador) de como fica um projeto **organizado**: a
interface da UC1, o banco da UC2 e os testes da UC3, num repositório só.

O mesmo sistema abre de três jeitos — numa janela, no terminal, e no terminal
com a biblioteca rich —, e os três usam as mesmas regras e o mesmo banco.

O plano inteiro, issue por issue (o que fechou, o que saiu e por quê), está em
[`docs/PLANO.md`](docs/PLANO.md).

## O problema

| Pergunta | Na locadora |
|---|---|
| **qual** é o problema? | o dono não sabe quem está com jogo atrasado |
| **quem** sofre com ele? | o dono e a atendente, no balcão |
| **como é hoje?** | um caderno, folheado toda sexta |
| **como saber que resolveu?** | a atendente vê na tela os atrasados e a multa de cada um, em segundos |

## As histórias

- **H1** — Como atendente, quero cadastrar, achar, alterar e apagar jogos, para
  a lista estar certa no dia em que o jogo chega.
- **H2** — Como atendente, quero cadastrar o cliente no balcão, para alugar para
  quem chega pela primeira vez.
- **H3** — Como atendente, quero registrar o aluguel e a devolução, para saber
  que jogo está com quem.
- **H4** — Como atendente, quero ver os empréstimos atrasados e a multa de cada
  um, para cobrar no balcão sem abrir o caderno.
- **H5** — Como dono, quero ver o que mais sai e quanto há a cobrar, para
  decidir o que comprar.
- **H6** — Como dono, quero mudar a multa sem chamar o programador, para a regra
  acompanhar a loja.

Os critérios de aceitação de cada uma estão no `docs/PLANO.md`, e cada
critério virou um teste em `tests/`.

## Como está organizado

```
main.py                  a janela (Tkinter)
terminal.py              o terminal, só com print e input
terminal_rich.py         o terminal, com a biblioteca rich
locadora/
    janela.py            interface: a janela, com o cabeçalho e as abas
    aba_*.py             interface: uma aba por arquivo
    menu.py              interface: os menus do terminal, para os dois jeitos
    tela_texto.py        interface: como o terminal mostra, com print e input
    tela_rich.py         interface: como o terminal mostra, com rich
    estilo.py            as cores e as letras da janela
    formato.py           o R$ e a data, iguais nas três interfaces
    regras.py            regras do negócio — o que pode e o que não pode
    dados.py             acesso ao banco — o SQL, e só ele
    dados_peewee.py      o mesmo acesso ao banco, com o Peewee (para comparar)
    conexao.py           abre a conexão a partir do .env
tests/
    test_regras.py       as regras, sem banco e sem janela
    test_dados.py        o acesso ao banco, no banco de teste (nas duas versões)
    conftest.py          a conexão com o banco de teste, limpa a cada teste
banco/
    criar_tabelas.sql    as tabelas
    dados_de_exemplo.sql jogos, clientes e aluguéis para a janela ter o que mostrar
docs/RECUPERACAO.md      como recuperar o sistema se a máquina sumir
docs/PLANO.md            o quadro de issues, escrito
```

Cada camada só conversa com a de baixo: a janela e o menu chamam `regras` e
`dados`, e nunca escrevem SQL. É por isso que a mesma regra serve às três
interfaces.

## Como rodar

1. Instale o Python 3 e o PostgreSQL (com o pgAdmin).
2. No pgAdmin, crie os bancos `locadora` e `locadora_teste`, e rode o
   `banco/criar_tabelas.sql` nos dois. No `locadora`, rode também o
   `banco/dados_de_exemplo.sql`.
3. Copie o `.env.exemplo`, renomeie a cópia para `.env` e ponha a senha do
   seu PostgreSQL. O `.env` nunca vai para o repositório.
4. Instale as bibliotecas: num notebook aberto nesta pasta, uma célula com
   `%pip install -r requirements.txt`.
5. Abra um dos três no VS Code e clique no ▶:
   - `main.py` — a janela;
   - `terminal.py` — o terminal, sem biblioteca nenhuma além do banco;
   - `terminal_rich.py` — o terminal com tabela, cor e barra.

## Como rodar os testes

No VS Code, painel **Testing** (o frasco) → ▶. São 58: os de dados rodam duas
vezes, uma com o `dados.py` e outra com o `dados_peewee.py`. Os testes de dados
usam o banco `locadora_teste`, que é apagado antes de cada teste — nunca aponte
para o `locadora`.

## O que aprendemos

- **Planejado e feito:** seis histórias na Aula 01; as seis saíram. Três
  issues menores foram para **Depois**, com o motivo escrito em cada uma.
- **Uma decisão que mudou:** a janela ia ter só o botão Cadastrar. No teste
  cruzado, a pessoa de outro grupo apertou Enter e esperou; agora o Enter
  cadastra.
- **O que travou:** o `tests/` não achava o pacote `locadora`
  (`ModuleNotFoundError`). Resolveu o `pythonpath` no `pyproject.toml`.

## O que vem depois

| Issue | O quê | Versão |
|---|---|---|
| #20 | aceitar "R$ 6,50" na diária | v2.1.0 |
| #22 | paginação das tabelas | v2.1.0 |
| #21 | o erro desconhecido do banco, em português de balcão | v2.0.1, é conserto |
