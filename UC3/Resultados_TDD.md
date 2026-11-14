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