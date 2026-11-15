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