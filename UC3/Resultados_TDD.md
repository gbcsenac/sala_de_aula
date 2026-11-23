(.venv) PS C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\UC3> python -m pytest test_multa.py -v
========================================================== test session starts ===========================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\UC3
plugins: platformdirs-4.14.2
collected 8 items                                                                                                                         

test_multa.py::test_antes_da_fronteira PASSED                                                                                       [ 12%]
test_multa.py::test_na_fronteira_dos_dois_dias PASSED                                                                               [ 25%]
test_multa.py::test_depois_da_fronteira_dos_tres_dias PASSED                                                                        [ 37%]
test_multa.py::test_depois_da_fronteira_dos_quatro_dias PASSED                                                                      [ 50%]
test_multa.py::test_aluguel_por_um_dia PASSED                                                                                       [ 62%]
test_multa.py::test_aluguel_por_dois_dias PASSED                                                                                    [ 75%]
test_multa.py::test_nao_aceita_aluguel_com_zero_dias PASSED                                                                         [ 87%]
test_multa.py::test_nao_aceita_aluguel_com_dias_negativos PASSED                                                                    [100%]

=========================================================== 8 passed in 2.54s ============================================================

(.venv) PS C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\UC3> python -m pytest test_cobranca.py -v
========================================================== test session starts ===========================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\UC3
plugins: platformdirs-4.14.2
collected 5 items                                                                                                                         

test_cobranca.py::test_emprestimo_atrasado_recebe_aviso PASSED                                                                      [ 20%]
test_cobranca.py::test_emprestimo_no_prazo_nao_recebe_aviso PASSED                                                                  [ 40%]
test_cobranca.py::test_dia_exato_do_prazo_nao_recebe_aviso PASSED                                                                   [ 60%]
test_cobranca.py::test_fim_de_semana_nao_recebe_aviso PASSED                                                                        [ 80%]
test_cobranca.py::test_whatsapp_fora_do_ar_nao_interrompe_cobranca PASSED                                                           [100%]

=========================================================== 5 passed in 0.36s ============================================================

(.venv) PS C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\UC3> python -m pytest test_emprestimo.py -v
========================================================== test session starts ===========================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\UC3
plugins: platformdirs-4.14.2
collected 6 items                                                                                                                         

test_emprestimo.py::test_cliente_com_10_ainda_leva_3 PASSED                                                                         [ 16%]
test_emprestimo.py::test_cliente_com_11_leva_4 PASSED                                                                               [ 33%]
test_emprestimo.py::test_cliente_com_10_ainda_leva_3_no_emprestimo PASSED                                                           [ 50%]
test_emprestimo.py::test_cliente_fiel_pode_levar_4_jogos PASSED                                                                     [ 66%]
test_emprestimo.py::test_cliente_fiel_nao_pode_levar_5_jogos PASSED                                                                 [ 83%]
test_emprestimo.py::test_nao_aceita_titulo_vazio PASSED                                                                             [100%]

=========================================================== 6 passed in 1.47s ============================================================

========================================================== test session starts ===========================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula
plugins: platformdirs-4.14.2
collected 6 items                                                                                                                         

UC3/test_cobranca.py::test_emprestimo_atrasado_recebe_aviso PASSED                                                                  [ 16%]
UC3/test_cobranca.py::test_emprestimo_no_prazo_nao_recebe_aviso PASSED                                                              [ 33%]
UC3/test_cobranca.py::test_dia_exato_do_prazo_nao_recebe_aviso PASSED                                                               [ 50%]
UC3/test_cobranca.py::test_fim_de_semana_nao_recebe_aviso PASSED                                                                    [ 66%]
UC3/test_cobranca.py::test_whatsapp_fora_do_ar_nao_interrompe_cobranca PASSED                                                       [ 83%]
UC3/test_cobranca.py::test_registra_aviso_depois_do_envio PASSED                                                                    [100%]

=========================================================== 6 passed in 0.55s ============================================================
# AULA 04 — MOCK OBJECTS
# PARTE A — COBRANÇA DE ATRASOS
#
# Resultado final: 6 testes PASSARAM.
# FAIL: 0
# ERROR: 0
#
# O que foi aprendido:
# - Utilizar Mock para simular dependências.
# - Utilizar spec para respeitar os métodos das classes.
# - Utilizar return_value para simular retornos.
# - Utilizar side_effect para simular falhas.
# - Verificar chamadas com assert_called_once_with.
# - Verificar ausência de chamadas com assert_not_called.
#
# Conclusão:
# A cobrança envia avisos para empréstimos atrasados,
# respeita finais de semana e não registra o aviso
# quando o WhatsApp apresenta erro.
#
# Status: PARTE A CONCLUÍDA.

====================================================================== test session starts =======================================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula
plugins: platformdirs-4.14.2
collected 6 items                                                                                                                                                 

UC3/test_cobranca.py::test_emprestimo_atrasado_recebe_aviso PASSED                                                                                          [ 16%]
UC3/test_cobranca.py::test_emprestimo_no_prazo_nao_recebe_aviso PASSED                                                                                      [ 33%]
UC3/test_cobranca.py::test_dia_exato_do_prazo_nao_recebe_aviso PASSED                                                                                       [ 50%]
UC3/test_cobranca.py::test_fim_de_semana_nao_recebe_aviso PASSED                                                                                            [ 66%]
UC3/test_cobranca.py::test_whatsapp_fora_do_ar_nao_interrompe_cobranca PASSED                                                                               [ 83%]
UC3/test_cobranca.py::test_registra_aviso_depois_do_envio PASSED                                                                                            [100%]

======================================================================= 6 passed in 1.85s ========================================================================

# RESULTADO DOS TESTES — UC3
#
# PASS = 4 testes aprovados
# FAIL = 0 testes com falha
# ERROR = 0 erros de execução
#
# Regras validadas:
# - Cliente cadastrado permite encomenda.
# - Cliente não cadastrado impede encomenda.
# - Estoque suficiente permite encomenda.
# - Estoque insuficiente impede encomenda.
#
# Conclusão:
# Todas as regras de encomenda foram aprovadas.

========================================================== test session starts ===========================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula
plugins: platformdirs-4.14.2
collected 4 items                                                                                                                         

UC3/test_regras_encomenda.py::test_cliente_cadastrado_permite_encomenda PASSED                                                      [ 25%]
UC3/test_regras_encomenda.py::test_cliente_nao_cadastrado_impede_encomenda PASSED                                                   [ 50%]
UC3/test_regras_encomenda.py::test_estoque_suficiente_permite_encomenda PASSED                                                      [ 75%]
UC3/test_regras_encomenda.py::test_estoque_insuficiente_impede_encomenda PASSED                                                     [100%]

=========================================================== 4 passed in 0.57s ============================================================

========================================================== test session starts ===========================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula
plugins: platformdirs-4.14.2
collected 4 items                                                                                                                         

UC3/test_regras_encomenda.py::test_cliente_cadastrado_permite_encomenda PASSED                                                      [ 25%]
UC3/test_regras_encomenda.py::test_cliente_nao_cadastrado_impede_encomenda PASSED                                                   [ 50%]
UC3/test_regras_encomenda.py::test_estoque_suficiente_permite_encomenda PASSED                                                      [ 75%]
UC3/test_regras_encomenda.py::test_estoque_insuficiente_impede_encomenda PASSED                                                     [100%]

=========================================================== 4 passed in 0.30s ============================================================

===================================================== test session starts ======================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula
plugins: platformdirs-4.14.2
collected 1 item                                                                                                                

UC3/locadora_demo/test_crud_jogo.py::test_cria_e_busca_pelo_id PASSED                                                     [100%]

====================================================== 1 passed in 0.54s =======================================================

# TESTE DE BUSCA PELO TÍTULO — LOCADORA

# 1º teste: PASS ✅ — busca pelo ID.
# 2º teste: FAIL ❌ — busca pelo título.

# Defeito encontrado no CRUD:
# A coluna foi escrita como "titlo",
# mas o nome correto no PostgreSQL é "titulo".

# O PostgreSQL identificou o erro de SQL.
# Correção necessária: alterar "titlo" para "titulo".

# Aprendizado:
# O teste de integração identificou um defeito
# que não seria percebido apenas olhando a lógica Python.

===================================================== test session starts ======================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula
plugins: platformdirs-4.14.2
collected 2 items                                                                                                               

UC3/locadora_demo/test_crud_jogo.py::test_cria_e_busca_pelo_id PASSED                                                     [ 50%]
UC3/locadora_demo/test_crud_jogo.py::test_busca_jogo_pelo_titulo FAILED                                                   [100%]

=========================================================== FAILURES ===========================================================
_________________________________________________ test_busca_jogo_pelo_titulo __________________________________________________

conexao = <connection object at 0x0000026DC6AB9F10; dsn: 'user=postgres password=xxx dbname=locadora_teste host=localhost port=5432', closed: 0>

    def test_busca_jogo_pelo_titulo(conexao):
        criar_jogo(conexao, "Mario", "Aventura", 2020, "10.00")
    
        achado = buscar_por_titulo(conexao, "Mario")
    
>       assert achado.titulo == "Mario"
               ^^^^^^^^^^^^^
E       AttributeError: 'NoneType' object has no attribute 'titulo'

UC3\locadora_demo\test_crud_jogo.py:17: AttributeError
----------------------------------------------------- Captured stdout call -----------------------------------------------------
ERRO:  coluna "titlo" não existe
LINE 1: ...ero, ano_lancamento, preco_diaria FROM jogo WHERE titlo = 'M...
                                                             ^
HINT:  Talvez você queira fazer referência à coluna "jogo.titulo".

=================================================== short test summary info ====================================================
FAILED UC3/locadora_demo/test_crud_jogo.py::test_busca_jogo_pelo_titulo - AttributeError: 'NoneType' object has no attribute 'titulo'
================================================= 1 failed, 1 passed in 2.05s ==================================================

===================================================== test session starts ======================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula
plugins: platformdirs-4.14.2
collected 2 items                                                                                                               

UC3/locadora_demo/test_crud_jogo.py::test_cria_e_busca_pelo_id PASSED                                                     [ 50%]
UC3/locadora_demo/test_crud_jogo.py::test_busca_jogo_pelo_titulo PASSED                                                   [100%]

====================================================== 2 passed in 1.60s =======================================================

===================================================== test session starts ======================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula
plugins: platformdirs-4.14.2
collected 3 items                                                                                                               

UC3/locadora_demo/test_crud_jogo.py::test_cria_e_busca_pelo_id PASSED                                                     [ 33%]
UC3/locadora_demo/test_crud_jogo.py::test_busca_jogo_pelo_titulo PASSED                                                   [ 66%]
UC3/locadora_demo/test_crud_jogo.py::test_apaga_jogo PASSED                                                               [100%]

====================================================== 3 passed in 1.73s =======================================================

(.venv) PS C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula> python -m pytest UC3/locadora_demo/test_crud_jogo.py -v
===================================================== test session starts ======================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula
plugins: platformdirs-4.14.2
collected 4 items                                                                                                               

UC3/locadora_demo/test_crud_jogo.py::test_cria_e_busca_pelo_id PASSED                                                     [ 25%]
UC3/locadora_demo/test_crud_jogo.py::test_busca_jogo_pelo_titulo PASSED                                                   [ 50%]
UC3/locadora_demo/test_crud_jogo.py::test_apaga_jogo PASSED                                                               [ 75%]
UC3/locadora_demo/test_crud_jogo.py::test_deleta_jogo_com_plataforma FAILED                                               [100%]

=========================================================== FAILURES ===========================================================
_______________________________________________ test_deleta_jogo_com_plataforma ________________________________________________

conexao = <connection object at 0x000001C900ABE350; dsn: 'user=postgres password=xxx dbname=locadora_teste host=localhost port=5432', closed: 0>

    def test_deleta_jogo_com_plataforma(conexao):
        criado = criar_jogo(conexao, "Zelda", "Aventura", 2017, "8.00")
    
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO plataforma (nome) VALUES ('Switch') RETURNING id_plataforma"
        )
        id_plataforma = cursor.fetchone()[0]
    
        cursor.execute(
            "INSERT INTO jogos_plataforma (id_jogo, id_plataforma) VALUES (%s, %s)",
            (criado.id_jogo, id_plataforma)
        )
        conexao.commit()
    
>       assert deletar_jogo(conexao, criado.id_jogo) is True
E       AssertionError: assert False is True
E        +  where False = deletar_jogo(<connection object at 0x000001C900ABE350; dsn: 'user=postgres password=xxx dbname=locadora_teste host=localhost port=5432', closed: 0>, 1)
E        +    where 1 = Jogo( 1 - Zelda ).id_jogo

UC3\locadora_demo\test_crud_jogo.py:42: AssertionError
----------------------------------------------------- Captured stdout call -----------------------------------------------------
ERRO:  atualização ou exclusão em tabela "jogo" viola restrição de chave estrangeira "jogos_plataforma_id_jogo_fkey" em "jogos_plataforma"
DETAIL:  Chave (id_jogo)=(1) ainda é referenciada pela tabela "jogos_plataforma".

=================================================== short test summary info ====================================================
FAILED UC3/locadora_demo/test_crud_jogo.py::test_deleta_jogo_com_plataforma - AssertionError: assert False is True
================================================= 1 failed, 3 passed in 4.03s ==================================================

===================================================== test session starts ======================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula
plugins: platformdirs-4.14.2
collected 6 items                                                                                                               

UC3/locadora_demo/test_crud_jogo.py::test_cria_e_busca_pelo_id PASSED                                                     [ 16%]
UC3/locadora_demo/test_crud_jogo.py::test_busca_jogo_pelo_titulo PASSED                                                   [ 33%]
UC3/locadora_demo/test_crud_jogo.py::test_apaga_jogo PASSED                                                               [ 50%]
UC3/locadora_demo/test_crud_jogo.py::test_deleta_jogo_com_plataforma FAILED                                               [ 66%]
UC3/locadora_demo/test_crud_jogo.py::test_banco_recusa_preco_negativo PASSED                                              [ 83%]
UC3/locadora_demo/test_crud_jogo.py::test_banco_recusa_titulo_repetido PASSED                                             [100%]

=========================================================== FAILURES ===========================================================
_______________________________________________ test_deleta_jogo_com_plataforma ________________________________________________

conexao = <connection object at 0x000002542937E460; dsn: 'user=postgres password=xxx dbname=locadora_teste host=localhost port=5432', closed: 0>

    def test_deleta_jogo_com_plataforma(conexao):
        criado = criar_jogo(conexao, "Zelda", "Aventura", 2017, "8.00")
    
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO plataforma (nome) VALUES ('Switch') RETURNING id_plataforma"
        )
        id_plataforma = cursor.fetchone()[0]
    
        cursor.execute(
            "INSERT INTO jogos_plataforma (id_jogo, id_plataforma) VALUES (%s, %s)",
            (criado.id_jogo, id_plataforma)
        )
        conexao.commit()
    
>       assert deletar_jogo(conexao, criado.id_jogo) is True
E       AssertionError: assert False is True
E        +  where False = deletar_jogo(<connection object at 0x000002542937E460; dsn: 'user=postgres password=xxx dbname=locadora_teste host=localhost port=5432', closed: 0>, 1)
E        +    where 1 = Jogo( 1 - Zelda ).id_jogo

UC3\locadora_demo\test_crud_jogo.py:42: AssertionError
----------------------------------------------------- Captured stdout call -----------------------------------------------------
ERRO:  atualização ou exclusão em tabela "jogo" viola restrição de chave estrangeira "jogos_plataforma_id_jogo_fkey" em "jogos_plataforma"
DETAIL:  Chave (id_jogo)=(1) ainda é referenciada pela tabela "jogos_plataforma".

=================================================== short test summary info ====================================================
FAILED UC3/locadora_demo/test_crud_jogo.py::test_deleta_jogo_com_plataforma - AssertionError: assert False is True
================================================= 1 failed, 5 passed in 8.70s ==================================================

===================================================== test session starts ======================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula
plugins: platformdirs-4.14.2
collected 4 items                                                                                                               

UC3/pavane_greyce/test_produto.py::test_inserir_produto PASSED                                                            [ 25%]
UC3/pavane_greyce/test_produto.py::test_listar_produtos PASSED                                                            [ 50%]
UC3/pavane_greyce/test_produto.py::test_atualizar_produto PASSED                                                          [ 75%]
UC3/pavane_greyce/test_produto.py::test_excluir_produto PASSED                                                            [100%]

====================================================== 4 passed in 2.51s =======================================================

# PASS = 4 testes aprovados.
# Inserir, listar, atualizar e excluir produtos funcionando.
# Os métodos CRUD foram testados com PostgreSQL.
# Próximo passo: testar se o banco rejeita dados inválidos.

===================================================== test session starts ======================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula
plugins: platformdirs-4.14.2
collected 
5 items

UC3/pavane_greyce/test_produto.py::test_inserir_produto PASSED                                                            [ 20%]
UC3/pavane_greyce/test_produto.py::test_listar_produtos PASSED                                                            [ 40%]
UC3/pavane_greyce/test_produto.py::test_atualizar_produto PASSED                                                          [ 60%]
UC3/pavane_greyce/test_produto.py::test_excluir_produto PASSED                                                            [ 80%]
UC3/pavane_greyce/test_produto.py::test_banco_recusa_preco_zero PASSED                                                    [100%]

====================================================== 5 passed in 3.20s =======================================================

# PASS = 5 testes aprovados.
# CRUD de Produto funcionando.
# PostgreSQL rejeita preço igual a zero.
# Restrição CHECK validada.
# Banco utilizado: pavane_greyce_teste.

===================================================== test session starts ======================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula
plugins: anyio-4.16.0, platformdirs-4.14.2
collected 7 items 

UC3/test_emprestimo.py::test_cliente_com_10_ainda_leva_3 PASSED                                                           [ 14%]
UC3/test_emprestimo.py::test_cliente_com_11_leva_4 PASSED                                                                 [ 28%]
UC3/test_emprestimo.py::test_cliente_com_10_ainda_leva_3_no_emprestimo PASSED                                             [ 42%]
UC3/test_emprestimo.py::test_cliente_fiel_pode_levar_4_jogos PASSED                                                       [ 57%]
UC3/test_emprestimo.py::test_cliente_fiel_nao_pode_levar_5_jogos PASSED                                                   [ 71%]
UC3/test_emprestimo.py::test_nao_aceita_titulo_vazio PASSED                                                               [ 85%]
UC3/test_emprestimo.py::test_nao_aceita_o_mesmo_jogo_duas_vezes FAILED                                                    [100%]

=========================================================== FAILURES ===========================================================
___________________________________________ test_nao_aceita_o_mesmo_jogo_duas_vezes ____________________________________________

    def test_nao_aceita_o_mesmo_jogo_duas_vezes():
        emprestimo = Emprestimo(Cliente("Ana", 0))
    
        emprestimo.adicionar("Zelda")
    
>       with pytest.raises(ValueError):
             ^^^^^^^^^^^^^^^^^^^^^^^^^
E       Failed: DID NOT RAISE ValueError

UC3\test_emprestimo.py:81: Failed
=================================================== short test summary info ====================================================
FAILED UC3/test_emprestimo.py::test_nao_aceita_o_mesmo_jogo_duas_vezes - Failed: DID NOT RAISE ValueError
================================================= 1 failed, 6 passed in 3.84s ==================================================

================================================= test session starts =================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula
plugins: anyio-4.16.0, platformdirs-4.14.2
collected 7 items

UC3/test_emprestimo.py::test_cliente_com_10_ainda_leva_3 PASSED                                                  [ 14%]
UC3/test_emprestimo.py::test_cliente_com_11_leva_4 PASSED                                                        [ 28%]
UC3/test_emprestimo.py::test_cliente_com_10_ainda_leva_3_no_emprestimo PASSED                                    [ 42%]
UC3/test_emprestimo.py::test_cliente_fiel_pode_levar_4_jogos PASSED                                              [ 57%]
UC3/test_emprestimo.py::test_cliente_fiel_nao_pode_levar_5_jogos PASSED                                          [ 71%]
UC3/test_emprestimo.py::test_nao_aceita_titulo_vazio PASSED                                                      [ 85%]
UC3/test_emprestimo.py::test_nao_aceita_o_mesmo_jogo_duas_vezes PASSED                                           [100%]

================================================== 7 passed in 1.10s ==================================================

===================================================== test session starts ======================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula
plugins: anyio-4.16.0, platformdirs-4.14.2
collected 7 items

UC3/test_cobranca.py::test_emprestimo_atrasado_recebe_aviso PASSED                                                        [ 14%]
UC3/test_cobranca.py::test_emprestimo_no_prazo_nao_recebe_aviso PASSED                                                    [ 28%]
UC3/test_cobranca.py::test_dia_exato_do_prazo_nao_recebe_aviso PASSED                                                     [ 42%]
UC3/test_cobranca.py::test_fim_de_semana_nao_recebe_aviso PASSED                                                          [ 57%]
UC3/test_cobranca.py::test_whatsapp_fora_do_ar_nao_interrompe_cobranca PASSED                                             [ 71%]
UC3/test_cobranca.py::test_registra_aviso_depois_do_envio PASSED                                                          [ 85%]
UC3/test_cobranca.py::test_falha_no_whatsapp_nao_impede_cobrar_proximo_cliente PASSED                                     [100%]

====================================================== 7 passed in 1.14s =======================================================
===================================================== test session starts ======================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Greyce Barcelos\OneDrive\Documents\sala_de_aula\PG Personalizados
configfile: pyproject.toml
plugins: anyio-4.16.0, platformdirs-4.14.2
collected 5 items

PG Personalizados\tests\test_regras_encomenda.py::test_cliente_cadastrado_permite_encomenda PASSED                        [ 20%]
PG Personalizados\tests\test_regras_encomenda.py::test_cliente_nao_cadastrado_impede_encomenda PASSED                     [ 40%]
PG Personalizados\tests\test_regras_encomenda.py::test_estoque_suficiente_permite_encomenda PASSED                        [ 60%]
PG Personalizados\tests\test_regras_encomenda.py::test_estoque_insuficiente_impede_encomenda PASSED                       [ 80%]
PG Personalizados\tests\test_regras_encomenda.py::test_produto_nao_encontrado_impede_encomenda PASSED                     [100%]

====================================================== 5 passed in 0.86s =======================================================