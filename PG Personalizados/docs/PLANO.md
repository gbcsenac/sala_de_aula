# PG personalizado — Sistema de Produtos Personalizados

## O problema

| Pergunta | No PG Personalizados |
|---|---|
| **Qual é o problema?** | O controle de clientes, produtos e encomendas é feito sem um sistema integrado, dificultando o acompanhamento dos pedidos. |
| **Quem sofre com ele?** | A pessoa responsável pelo atendimento e pela organização das encomendas. |
| **Como é hoje?** | As informações de clientes, produtos, preços e encomendas precisam ser consultadas e organizadas manualmente. |
| **Como saber que resolveu?** | A pessoa responsável consegue cadastrar clientes e produtos, registrar encomendas e consultar os pedidos em uma única tela, com as informações organizadas e atualizadas. |

## As histórias

- **H1** — Como atendente, quero cadastrar, consultar, alterar e excluir clientes, para manter os dados dos clientes organizados e atualizados.
- **H2** — Como atendente, quero cadastrar, consultar, alterar e excluir produtos, para manter o catálogo de camisetas e canecas personalizadas atualizado.
- **H3** — Como atendente, quero registrar e consultar encomendas, para acompanhar os pedidos realizados pelos clientes.
- **H4** — Como atendente, quero adicionar produtos e quantidades às encomendas, para registrar corretamente os itens solicitados por cada cliente.
- **H5** — Como responsável pelo negócio, quero consultar os preços e as quantidades disponíveis dos produtos, para acompanhar o estoque e os valores praticados.
- **H6** — Como responsável pelo negócio, quero acompanhar as datas de pedido, pagamento e retirada, para controlar a situação de cada encomenda.

Os critérios de aceitação de cada história serão registrados no `docs/PLANO.md`, e os critérios que puderem ser automatizados serão transformados em testes na pasta `tests/`.

## Como está organizado

```text
main.py                         inicia o sistema (Tkinter)

pavane_greyce/
    janela.py                   interface: janela principal
    aba_clientes.py              interface: cadastro e consulta de clientes
    aba_produtos.py              interface: cadastro e consulta de produtos
    aba_encomendas.py            interface: registro e consulta de encomendas
    menu.py                      organização dos menus e abas
    estilo.py                    cores, fontes e aparência da janela
    formato.py                   formatação de valores e datas
    regras.py                    regras do negócio: o que pode e o que não pode
    dados.py                     acesso ao banco: comandos SQL e operações CRUD
    dados_peewee.py               alternativa de acesso com Peewee (para comparar)
    conexao.py                   abre a conexão com PostgreSQL a partir do .env

classes/
    cliente.py                   classe Cliente
    produto.py                   classe Produto
    encomenda.py                 classe Encomenda
    item_encomenda.py            classe ItemEncomenda

tests/
    test_regras.py                testes das regras do negócio
    test_dados.py                 testes do acesso ao banco
    conftest.py                   configurações e preparação dos testes

banco/
    criar_tabelas.sql             criação das tabelas do banco
    dados_de_exemplo.sql          clientes, produtos e encomendas de exemplo
    diagrama_banco_dados.md       documentação do modelo do banco

docs/
    RECUPERACAO.md                orientações para recuperar o sistema
    PLANO.md                      planejamento, histórias e critérios de aceitação

.env                              configurações locais e senha do banco
.env.exemplo                     modelo das configurações
.gitignore                       arquivos que não devem ir para o Git
requirements.txt                 bibliotecas necessárias
pyproject.toml                   configurações do projeto e do pytest
README.md                        documentação principal do projeto
```

Cada camada tem uma responsabilidade: a janela apresenta as informações e recebe as ações; as regras definem o que pode ou não acontecer; e o acesso aos dados executa os comandos SQL no PostgreSQL.

A interface não escreve SQL diretamente, e as regras não dependem da janela. Assim, podemos testar as regras separadamente e manter o acesso ao banco organizado.

## Como rodar

1. Instale o Python 3 e o PostgreSQL (com o pgAdmin).
2. No pgAdmin, crie os bancos:
   - `pavane_greyce`
   - `pavane_greyce_teste`
3. Execute o arquivo `banco/criar_tabelas.sql` nos dois bancos.
4. No banco `pavane_greyce`, execute também `banco/dados_de_exemplo.sql`, caso queira iniciar com registros de demonstração.
5. Copie o `.env.exemplo`, renomeie a cópia para `.env` e informe os dados de conexão do PostgreSQL.
6. Instale as bibliotecas necessárias:

   ```powershell
   python -m pip install -r requirements.txt
   ```

7. No VS Code, abra a pasta do projeto e execute `main.py` pelo botão ▶.

**Importante:** o arquivo `.env` contém informações privadas e nunca deve ser enviado ao GitHub. Os testes devem utilizar exclusivamente o banco `pavane_greyce_teste`.

## Como rodar os testes

No VS Code, abra o painel **Testing** (ícone do frasco) e execute os testes pelo botão ▶.

Também é possível executar pelo terminal:

```powershell
python -m pytest -v
```

Os testes das regras devem verificar as condições do negócio sem precisar abrir a janela ou acessar o banco.

Os testes de acesso aos dados devem utilizar o banco `pavane_greyce_teste`, nunca o banco principal `pavane_greyce`.

## O que aprendemos

- **Planejamento e desenvolvimento:** organizar o projeto em etapas, aproveitando os conhecimentos de Python, orientação a objetos, CRUD, PostgreSQL e testes automatizados.
- **Separação de responsabilidades:** compreender a função de cada camada: interface, regras e acesso aos dados.
- **Banco de dados:** utilizar PostgreSQL para armazenar clientes, produtos e encomendas, mantendo os relacionamentos entre as tabelas.
- **Testes:** verificar se as regras do negócio funcionam corretamente antes de integrar tudo à interface.
- **Organização:** separar classes, banco de dados, testes e documentação para facilitar a manutenção e a evolução do sistema.

## O que vem depois

| Issue | O quê | Versão |
|---|---|---|
| #1 | Criar a janela principal com Tkinter | v1.0.0 |
| #2 | Desenvolver as abas de clientes, produtos e encomendas | v1.0.0 |
| #3 | Integrar as regras do negócio à interface | v1.0.0 |
| #4 | Integrar o acesso ao PostgreSQL | v1.0.0 |
| #5 | Implementar e validar os testes automatizados | v1.0.0 |
| #6 | Melhorar a apresentação e a usabilidade do sistema | v1.1.0 |