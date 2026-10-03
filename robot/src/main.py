"""Programa para verificação de bateria do robô."""

import sys


def validar_entrada(bateria: float, duracao: float, consumo: float) -> bool:
    """Valida os parâmetros conforme as regras do problema."""
    return (0 <= bateria <= 100) and (duracao > 0) and (consumo > 0)


def calcular_missao(
    bateria: float, duracao: float, consumo: float
) -> tuple[bool, float]:
    """Calcula se a missão é viável e retorna resultado + valor residual."""
    consumo_total = duracao * consumo
    if consumo_total <= bateria:
        return True, bateria - consumo_total
    return False, consumo_total - bateria


def main() -> None:
    """Ponto de entrada do programa."""
    try:
        bateria = float(input("Bateria atual (0-100): "))
        duracao = float(input("Duração da missão (minutos): "))
        consumo = float(input("Consumo por minuto (%): "))
    except ValueError:
        print("Valor inválido")
        sys.exit(1)

    if not validar_entrada(bateria, duracao, consumo):
        print("Valor inválido")
        sys.exit(1)

    possivel, valor = calcular_missao(bateria, duracao, consumo)

    if possivel:
        print(f"Missão pode ser concluída. Bateria restante: {valor:.1f}%")
    else:
        print(f"Missão não pode ser concluída. Faltam {valor:.1f} pontos percentuais.")


if __name__ == "__main__":
    main()
