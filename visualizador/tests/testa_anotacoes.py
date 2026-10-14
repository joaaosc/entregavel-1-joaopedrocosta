"""Testes básicos das classes e da leitura do CSV."""

import sys
import tempfile
from pathlib import Path

import numpy as np

# os módulos de src importam uns aos outros pelo nome, então src entra no path
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))

from arquivos import ErroDeLeitura, agrupar_por_imagem, ler_anotacoes  # noqa: E402
from modelos import Deteccao, ImagemAnotada  # noqa: E402

CABECALHO = "imagem,classe_id,x_min,y_min,x_max,y_max\n"


def ler_csv_temporario(conteudo: str) -> dict[str, ImagemAnotada]:
    with tempfile.TemporaryDirectory() as pasta:
        caminho = Path(pasta) / "anotacoes.csv"
        caminho.write_text(conteudo, encoding="utf-8")
        return agrupar_por_imagem(ler_anotacoes(caminho), Path("imagens"))


def testar():
    # cantos inclusivos: x_max precisa ser menor que a largura
    assert Deteccao(0, 0, 0, 9, 9).cabe_na_imagem(10, 10) is True
    assert Deteccao(0, 0, 0, 10, 9).cabe_na_imagem(10, 10) is False
    assert Deteccao(0, 5, 0, 5, 9).cabe_na_imagem(10, 10) is False

    # a imagem original não pode ser alterada pelo desenho
    anotada = ImagemAnotada(Path("imagens/teste.jpg"))
    anotada.adicionar(Deteccao(0, 1, 1, 5, 5))
    anotada.adicionar(Deteccao(1, 2, 2, 8, 8))
    original = np.zeros((10, 10, 3), dtype=np.uint8)
    resultado = anotada.desenhar_caixas(original)
    assert original.sum() == 0 and resultado.sum() > 0

    # linhas da mesma imagem separadas no CSV
    imagens = ler_csv_temporario(
        CABECALHO + "b.jpg,0,1,1,5,5\na.jpg,1,1,1,5,5\nb.jpg,1,2,2,8,8\n"
    )
    assert sorted(imagens) == ["a.jpg", "b.jpg"]
    assert len(imagens["b.jpg"].deteccoes) == 2

    for invalido in ["a.jpg,0,1,abc,5,5\n", "a.jpg,0,1,1\n", "a.jpg,7,1,1,5,5\n"]:
        try:
            ler_csv_temporario(CABECALHO + invalido)
        except ErroDeLeitura:
            pass
        else:
            raise AssertionError(f"linha inválida aceita: {invalido!r}")

    # arquivo fornecido no material complementar
    imagens = agrupar_por_imagem(
        ler_anotacoes(RAIZ / "dados" / "anotacoes.csv"), RAIZ / "imagens"
    )
    assert len(imagens) == 10
    assert sum(len(a.deteccoes) for a in imagens.values()) == 581

    print("Testes básicos concluídos.")


if __name__ == "__main__":
    testar()
