"""Testes do programa – implementação em pytest TODO."""

from src.main import validar_entrada, calcular_missao


def testar():
    assert validar_entrada(80, 10, 3) is True
    assert validar_entrada(101, 10, 3) is False
    assert validar_entrada(50, 0, 3) is False

    possivel, valor = calcular_missao(80, 10, 3)
    assert possivel is True and valor == 50.0

    possivel, valor = calcular_missao(30, 10, 3)
    assert possivel is True and valor == 0.0

    possivel, valor = calcular_missao(20, 10, 3)
    assert possivel is False and valor == 10.0

    print("Testes básicos concluídos.")

if __name__ == "__main__":
    testar()
