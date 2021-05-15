import pytest
from src.negocio.MiembroOfercompas import MiembroOfercompas

miembro = MiembroOfercompas()
miembro.email = "jorge@gmail.com"
miembro.tipoMiembro = 1
miembro.nickname = "jorgito"
miembro.estado = 1


def test_registrar_miembro_ofercompas():
    resultado = miembro.registrar()
    assert resultado == 0


def test_actualizar_miembro_ofercompas():
    miembro.nickname = "jorgitoActualizado"
    resultado = miembro.actualizar_miembro("jorge@gmail.com")
    assert resultado == 0


def test_iniciar_sesion():
    resultado = miembro.iniciar_sesion()
    assert  resultado == 0


def test_email_registrado():
    resultado = miembro.email_registrado()
    assert  resultado

def test_nickname_registrado():
    resultado = miembro.nickname_registrado()
    assert resultado

def test_recuperar_miembro_ofercompas():
    miembro_recuperar = MiembroOfercompas()
    miembro_recuperar.email = "jorge@gmail.com"
    miembro_recuperar.recuperar_miembro()
    esIgual = False
    if miembro_recuperar.email == miembro.email and miembro_recuperar.nickname == miembro.nickname:
        esIgual = True
    assert  esIgual





