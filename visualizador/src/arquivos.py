"""Leitura do CSV de anotações e das imagens."""

import csv
from pathlib import Path

import cv2
import numpy as np

from modelos import CORES_POR_CLASSE, Deteccao, ImagemAnotada

CABECALHO = ["imagem", "classe_id", "x_min", "y_min", "x_max", "y_max"]


class ErroDeLeitura(Exception):
    """CSV ou imagem que não pôde ser lido, ou linha com dados inválidos."""


def ler_anotacoes(caminho_csv: Path) -> list[dict[str, str]]:
    """Lê o CSV e devolve as linhas como dicionários (valores ainda em texto)."""
    try:
        with open(caminho_csv, newline="", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)
            if leitor.fieldnames != CABECALHO:
                raise ErroDeLeitura(
                    f"cabeçalho inesperado em {caminho_csv.name}: {leitor.fieldnames}"
                )
            return list(leitor)
    except OSError as erro:
        raise ErroDeLeitura(f"não foi possível ler {caminho_csv}: {erro.strerror}")
    except (csv.Error, UnicodeDecodeError) as erro:
        raise ErroDeLeitura(f"{caminho_csv.name} não é um CSV válido: {erro}")


def criar_deteccao(linha: dict[str, str], numero_linha: int) -> Deteccao:
    """Converte os campos numéricos de uma linha para int e cria a Deteccao."""
    try:
        classe_id, x_min, y_min, x_max, y_max = (
            int(linha[campo]) for campo in CABECALHO[1:]
        )
    except (TypeError, ValueError):
        raise ErroDeLeitura(f"linha {numero_linha}: campos numéricos inválidos")

    if classe_id not in CORES_POR_CLASSE:
        raise ErroDeLeitura(f"linha {numero_linha}: classe_id {classe_id} desconhecido")

    return Deteccao(classe_id, x_min, y_min, x_max, y_max)


def agrupar_por_imagem(
    linhas: list[dict[str, str]], pasta_imagens: Path
) -> dict[str, ImagemAnotada]:
    """Agrupa as caixas pelo nome da imagem, mesmo com linhas fora de ordem."""
    imagens: dict[str, ImagemAnotada] = {}

    # a linha 1 do arquivo é o cabeçalho
    for numero_linha, linha in enumerate(linhas, start=2):
        nome = (linha["imagem"] or "").strip()
        if not nome:
            raise ErroDeLeitura(f"linha {numero_linha}: nome da imagem vazio")

        if nome not in imagens:
            imagens[nome] = ImagemAnotada(pasta_imagens / nome)
        imagens[nome].adicionar(criar_deteccao(linha, numero_linha))

    return imagens


def ler_imagem(anotada: ImagemAnotada) -> np.ndarray:
    """Abre a imagem e confere se todas as caixas cabem dentro dela."""
    imagem = cv2.imread(str(anotada.caminho))
    if imagem is None:
        raise ErroDeLeitura(f"não foi possível abrir a imagem {anotada.caminho}")

    altura, largura = imagem.shape[:2]
    for deteccao in anotada.deteccoes:
        if not deteccao.cabe_na_imagem(largura, altura):
            raise ErroDeLeitura(
                f"{anotada.nome}: caixa ({deteccao.x_min}, {deteccao.y_min}, "
                f"{deteccao.x_max}, {deteccao.y_max}) fora dos limites "
                f"de {largura}x{altura}"
            )

    return imagem
