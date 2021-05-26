from http import HTTPStatus

import pytest

from src.negocio import Motivo
from src.negocio.Denuncia import Denuncia

denuncia = Denuncia()
denuncia.id_denunciante = 7
denuncia.id_publicacion = 29
denuncia.motivo = Motivo.ALCHOL_TABACO
denuncia.comentario = "La verdad si se pasó"


def test_registrar():
    resultado = denuncia.registrar()
    assert resultado != HTTPStatus.INTERNAL_SERVER_ERROR


def test_existe_denuncia():
    assert denuncia.existe_denuncia()
