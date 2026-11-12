
from datetime import date
from unittest.mock import Mock

from UC3.cobranca import Emprestimo, CobradorDeAtrasos


def test_emprestimo_atrasado_recebe_aviso():

    # Arrange: preparar os objetos dublês
    repositorio = Mock()
    avisador = Mock()
    relogio = Mock()

    hoje = date(2026, 11, 12)

    emprestimo = Emprestimo(
        1,
        "Maria",
        "51999999999",
        date(2026, 11, 10)
    )

    repositorio.abertos.return_value = [emprestimo]
    relogio.hoje.return_value = hoje

    cobrador = CobradorDeAtrasos(
        repositorio,
        avisador,
        relogio
    )

    # Act: executar a cobrança
    cobrador.cobrar()

    # Assert: verificar o resultado
    avisador.avisa.assert_called_once_with(emprestimo)
    assert cobrador.total_avisados == 1

def test_emprestimo_no_prazo_nao_recebe_aviso():

    # Arrange: preparar os objetos dublês
    repositorio = Mock()
    avisador = Mock()
    relogio = Mock()

    hoje = date(2026, 11, 12)

    emprestimo = Emprestimo(
        2,
        "João",
        "51988888888",
        date(2026, 11, 15)
    )

    repositorio.abertos.return_value = [emprestimo]
    relogio.hoje.return_value = hoje

    cobrador = CobradorDeAtrasos(
        repositorio,
        avisador,
        relogio
    )

    # Act: executar a cobrança
    cobrador.cobrar()

    # Assert: verificar que não houve aviso
    avisador.avisa.assert_not_called()
    assert cobrador.total_avisados == 0


def test_dia_exato_do_prazo_nao_recebe_aviso():

    # Arrange
    repositorio = Mock()
    avisador = Mock()
    relogio = Mock()

    hoje = date(2026, 11, 12)

    emprestimo = Emprestimo(
        3,
        "Ana",
        "51977777777",
        date(2026, 11, 12)
    )

    repositorio.abertos.return_value = [emprestimo]
    relogio.hoje.return_value = hoje

    cobrador = CobradorDeAtrasos(
        repositorio,
        avisador,
        relogio
    )

    # Act
    cobrador.cobrar()

    # Assert
    avisador.avisa.assert_not_called()
    assert cobrador.total_avisados == 0


def test_fim_de_semana_nao_recebe_aviso():

    # Arrange
    repositorio = Mock()
    avisador = Mock()
    relogio = Mock()

    hoje = date(2026, 11, 14)  # Sábado

    emprestimo = Emprestimo(
        4,
        "Carlos",
        "51966666666",
        date(2026, 11, 10)
    )

    repositorio.abertos.return_value = [emprestimo]
    relogio.hoje.return_value = hoje

    cobrador = CobradorDeAtrasos(
        repositorio,
        avisador,
        relogio
    )

    # Act
    cobrador.cobrar()

    # Assert
    avisador.avisa.assert_not_called()
    assert cobrador.total_avisados == 0


def test_whatsapp_fora_do_ar_nao_interrompe_cobranca():

    # Arrange
    repositorio = Mock()
    avisador = Mock()
    relogio = Mock()

    hoje = date(2026, 11, 12)

    emprestimo = Emprestimo(
        5,
        "Pedro",
        "51955555555",
        date(2026, 11, 10)
    )

    repositorio.abertos.return_value = [emprestimo]
    relogio.hoje.return_value = hoje

    # Simula o WhatsApp fora do ar
    avisador.avisa.side_effect = ConnectionError(
        "WhatsApp indisponível"
    )

    cobrador = CobradorDeAtrasos(
        repositorio,
        avisador,
        relogio
    )

    # Act
    cobrador.cobrar()

    # Assert
    assert cobrador.total_avisados == 0
    repositorio.atualiza.assert_not_called()

def cobrar(self) -> None:
    hoje = self.relogio.hoje()

    if hoje.weekday() >= 5:
        return

    for emprestimo in self.repositorio.abertos():
        if emprestimo.atrasado_em(hoje):

            try:
                self.avisador.avisa(emprestimo)

            except ConnectionError:
                continue

            emprestimo.registrar_aviso(hoje)
            self.repositorio.atualiza(emprestimo)
            self.total_avisados += 1

