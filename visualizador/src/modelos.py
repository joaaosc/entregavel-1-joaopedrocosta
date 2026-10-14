"""Classes que representam as caixas anotadas de cada imagem."""

from pathlib import Path

import cv2
import numpy as np

# cores no formato BGR usado pelo OpenCV
CORES_POR_CLASSE = {
    0: (0, 200, 0),  # verde
    1: (255, 128, 0),  # azul
}
ESPESSURA_CAIXA = 2


class Deteccao:
    """Uma bounding box: ID da classe e cantos em pixels (inclusivos)."""

    def __init__(
        self, classe_id: int, x_min: int, y_min: int, x_max: int, y_max: int
    ) -> None:
        self.classe_id = classe_id
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def cabe_na_imagem(self, largura: int, altura: int) -> bool:
        """Confere 0 <= x_min < x_max < largura e o mesmo para y."""
        return (0 <= self.x_min < self.x_max < largura) and (
            0 <= self.y_min < self.y_max < altura
        )

    def desenhar(self, imagem: np.ndarray) -> None:
        """Desenha a caixa na imagem recebida, com a cor da sua classe."""
        cor = CORES_POR_CLASSE[self.classe_id]
        cv2.rectangle(
            imagem,
            (self.x_min, self.y_min),
            (self.x_max, self.y_max),
            cor,
            ESPESSURA_CAIXA,
        )


class ImagemAnotada:
    """Caminho de uma imagem e a lista de caixas associadas a ela."""

    def __init__(self, caminho: Path) -> None:
        self.caminho = Path(caminho)
        self.deteccoes: list[Deteccao] = []

    @property
    def nome(self) -> str:
        return self.caminho.name

    def adicionar(self, deteccao: Deteccao) -> None:
        self.deteccoes.append(deteccao)

    def desenhar_caixas(self, imagem: np.ndarray) -> np.ndarray:
        """Retorna uma cópia da imagem com todas as caixas desenhadas."""
        copia = imagem.copy()
        for deteccao in self.deteccoes:
            deteccao.desenhar(copia)
        return copia
