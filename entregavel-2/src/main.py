"""Visualizador das anotações do material complementar com OpenCV."""

import sys
from pathlib import Path

import cv2
import numpy as np

from arquivos import ErroDeLeitura, agrupar_por_imagem, ler_anotacoes, ler_imagem
from modelos import CORES_POR_CLASSE, ImagemAnotada

RAIZ = Path(__file__).resolve().parent.parent
ARQUIVO_CSV = RAIZ / "dados" / "anotacoes.csv"
PASTA_IMAGENS = RAIZ / "imagens"
PASTA_RESULTADOS = RAIZ / "resultados"

NOME_JANELA = "Visualizador de anotacoes"
LARGURA_MAX_TELA = 1280
ALTURA_MAX_TELA = 720
TECLA_AVANCAR = ord(" ")
TECLA_SAIR = ord("q")


def reduzir_para_tela(imagem: np.ndarray) -> np.ndarray:
    """Reduz a cópia exibida caso a imagem não caiba na tela."""
    altura, largura = imagem.shape[:2]
    escala = min(1.0, LARGURA_MAX_TELA / largura, ALTURA_MAX_TELA / altura)
    if escala == 1.0:
        return imagem.copy()
    tamanho = (round(largura * escala), round(altura * escala))
    return cv2.resize(imagem, tamanho, interpolation=cv2.INTER_AREA)


def desenhar_legenda(imagem: np.ndarray, titulo: str) -> None:
    """Escreve o nome da imagem e a cor de cada classe no canto superior."""
    fonte = cv2.FONT_HERSHEY_SIMPLEX
    linhas = [(titulo, (255, 255, 255))]
    linhas += [(f"classe {cid}", cor) for cid, cor in CORES_POR_CLASSE.items()]

    # fundo escuro para o texto ficar legível em cenas claras
    altura_fundo = 12 + 24 * len(linhas)
    largura_fundo = 20 + max(
        cv2.getTextSize(texto, fonte, 0.6, 2)[0][0] for texto, _ in linhas
    )
    cv2.rectangle(imagem, (0, 0), (largura_fundo, altura_fundo), (0, 0, 0), -1)

    for i, (texto, cor) in enumerate(linhas):
        cv2.putText(imagem, texto, (10, 28 + 24 * i), fonte, 0.6, cor, 2, cv2.LINE_AA)


def esperar_tecla() -> bool:
    """Espera Espaço (True, avança) ou q (False, encerra); ignora o resto."""
    while True:
        tecla = cv2.waitKey(0) & 0xFF
        if tecla == TECLA_AVANCAR:
            return True
        if tecla == TECLA_SAIR:
            return False


def processar_imagem(anotada: ImagemAnotada, titulo: str) -> np.ndarray:
    """Desenha as caixas, salva o resultado e devolve a cópia para exibição."""
    imagem = ler_imagem(anotada)
    resultado = anotada.desenhar_caixas(imagem)

    destino = PASTA_RESULTADOS / anotada.nome
    if not cv2.imwrite(str(destino), resultado):
        raise ErroDeLeitura(f"não foi possível salvar {destino}")

    exibicao = reduzir_para_tela(resultado)
    desenhar_legenda(exibicao, titulo)
    return exibicao


def main() -> None:
    """Lê as anotações e mostra uma imagem por vez."""
    try:
        imagens = agrupar_por_imagem(ler_anotacoes(ARQUIVO_CSV), PASTA_IMAGENS)
    except ErroDeLeitura as erro:
        print(f"Erro: {erro}")
        sys.exit(1)

    if not imagens:
        print(f"Erro: nenhuma anotação encontrada em {ARQUIVO_CSV.name}")
        sys.exit(1)

    PASTA_RESULTADOS.mkdir(exist_ok=True)
    nomes = sorted(imagens)
    total = len(nomes)

    for posicao, nome in enumerate(nomes, start=1):
        anotada = imagens[nome]
        titulo = f"{nome} ({posicao}/{total})"

        try:
            exibicao = processar_imagem(anotada, titulo)
        except ErroDeLeitura as erro:
            print(f"Erro: {erro}")
            cv2.destroyAllWindows()
            sys.exit(1)

        print(f"[{posicao}/{total}] {nome}: {len(anotada.deteccoes)} caixas desenhadas")
        cv2.imshow(NOME_JANELA, exibicao)

        if not esperar_tecla():
            print("Encerrado pelo usuário.")
            break

    cv2.destroyAllWindows()
    # no macOS a janela só fecha de fato depois de mais um ciclo de eventos
    cv2.waitKey(1)


if __name__ == "__main__":
    main()
