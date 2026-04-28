# Apollo vs Clay - Analisis comparativo

Generador de un PDF descargable con el analisis comparativo entre Apollo.io y Clay.com,
pensado para llevar a una conversacion de decision con la gerencia de una agencia de marketing.

## Como generar el PDF

Requisitos: Python 3 y `reportlab`.

```bash
pip install reportlab
python3 generate_pdf.py
```

Salida: `Apollo_vs_Clay_Analisis.pdf` (6 paginas).

## Que contiene el PDF

1. **Caratula con veredicto en una linea**
2. **Contexto y problema actual**
3. **Tabla comparativa Apollo vs Clay** (15 criterios: precio, base de datos, deep research,
   personalizacion, envio de emails, match rate, curva de aprendizaje, costo por lead,
   riesgo de overage, etc.)
4. **Pros y contras** de cada herramienta lado a lado
5. **Costo real proyectado** con escenarios para 1, 2 y 3 SDRs
6. **Matriz de decision**: cuando elegir cual segun prioridad
7. **Recomendacion final** con plan de accion sugerido

## Veredicto

Para una agencia con presupuesto acotado que necesita combinar campanias masivas y
campanias top-200 con personalizacion, **Apollo Professional ($79/usuario/mes anual)**
es la eleccion recomendada. Clay sigue siendo mejor para deep research puro, pero su modelo
de creditos + ausencia de envio nativo eleva el costo total al doble o mas.
