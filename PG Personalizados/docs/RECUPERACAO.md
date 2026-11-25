# Política de recuperação — Pavane Greyce

## O que precisa ser protegido?

| Pergunta | O código | Os dados |
|---|---|---|
| **O quê?** | O repositório do projeto Pavane Greyce | O banco de dados `pavane_greyce` |
| **Como?** | `git push` para o GitHub | Backup do PostgreSQL com `pg_dump`, no formato Custom |
| **Quando?** | A cada commit importante que vale guardar | Toda sexta-feira e antes de qualquer alteração importante no banco |
| **Onde?** | No GitHub | Em uma pasta de backup no computador ou em um serviço de armazenamento privado |
| **Quem?** | Quem realizou o commit | A pessoa responsável pelo projeto |
| **Como sei que funciona?** | Clonar o repositório em uma pasta nova e executar os testes | Restaurar o backup em um banco vazio de teste e verificar os dados |

## Como recuperar o código

1. Acessar o repositório do projeto no GitHub.
2. Clonar o projeto em uma nova pasta:

   ```powershell
   git clone URL_DO_REPOSITORIO
   ```

3. Criar e ativar o ambiente virtual.
4. Instalar as bibliotecas:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Configurar o arquivo `.env` com os dados de conexão.
6. Executar os testes:

   ```powershell
   python -m pytest -v
   ```

## Como recuperar os dados

1. Localizar o arquivo de backup do PostgreSQL.
2. Abrir o pgAdmin.
3. Criar um banco vazio para restauração.
4. Utilizar a opção **Restore** do pgAdmin.
5. Selecionar o arquivo de backup no formato Custom.
6. Restaurar os dados e verificar se as tabelas e os registros estão disponíveis.

## Cuidados importantes

- O banco principal é `pavane_greyce`.
- O banco de testes é `pavane_greyce_teste`.
- Nunca utilizar o banco principal para executar testes destrutivos.
- O arquivo `.env` não deve ser enviado ao GitHub.
- Os backups do banco contêm informações que podem ser privadas e devem ficar em local protegido, com acesso restrito.
- O backup só é considerado confiável depois de uma restauração de teste bem-sucedida.

## Objetivo da política

Garantir que o projeto Pavane Greyce possa ser recuperado caso ocorra perda dos arquivos, falha no computador ou problema no banco de dados.