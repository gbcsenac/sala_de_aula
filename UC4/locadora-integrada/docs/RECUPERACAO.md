# Política de recuperação

| Pergunta | O código | Os dados |
|---|---|---|
| o quê | este repositório | o banco `locadora` |
| como | `git push` para o GitHub | backup do pgAdmin (`pg_dump`), formato Custom |
| quando | a cada commit que vale guardar | toda sexta, e antes de cada mudança no banco |
| onde | o GitHub | o drive do grupo — nunca o GitHub, que é público |
| quem | quem fez o commit | Ana; se faltar, Bruno |
| como sei que funciona | clonar numa pasta nova e rodar os testes | restaurar num banco vazio e abrir a janela |
