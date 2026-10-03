# Entregável 1 do processo seletivo da Minerva Harpia 
## Verificar bateria do robô 
**Objetivo:** 
verificar se o robô tem bateria suficiente pararealizar uma missão. Para isso, o programa exige três entradas do usuário:
- Bateria atual, em porcentagem de 0 a 100.
- Duração prevista da missão, em minutos.
- Consumo por minuto, em pontos percentuais da bateria.

*feito por João Pedro de S. T. Costa, 02/10/2026*

---
**Requisitos:**
- Python 3.8+
- Ambiente virtual com UV *[OPCIONAL, mas recomendado]*
```
uv venv .venv
source .venv/bin/activate  # Linux/macOS
```
*Opcional:*
- ```uv pip install black flake8 pytest``` (TODO)

Observação: pensado apenas para
Linux ou macOS. Não há motivos para não funcionar em Windows também, mas não foi verificado.

**Comando de execução**
A partir da pasta principal, execute com:
```
python src/main.py
```

**Exemplo de entrada e saída:**
Obs.: você pode usar ```python -m tests.testa_misssao``` para verificar funcionamento correto do programa.

[exemplo.png](entregavel_1/exemplo.png)


