# Financial Market Analysis 📊

Análisis cuantitativo de mercados financieros usando datos públicos. Descarga información de acciones, criptos e índices, y realiza análisis estadístico interesante.

## 🎯 Características

- ✅ **Descarga automática** de datos históricos (Yahoo Finance - GRATIS)
- ✅ **Análisis de retornos**: total, anualizado, volatilidad
- ✅ **Métricas de riesgo**: Maximum Drawdown, Sharpe Ratio
- ✅ **Matriz de correlación** entre activos
- ✅ **Visualizaciones profesionales**: tendencias, riesgo vs retorno, heatmap
- ✅ **Recomendaciones de portafolio** basadas en Sharpe Ratio
- ✅ **Fácil de ejecutar** y customizar

## 🚀 Inicio Rápido

### Requisitos
```bash
pip install pandas numpy yfinance matplotlib
```

### Ejecutar análisis
```bash
python financial_market_analysis.py
```

### Output
El script genera:
- Tabla con análisis de retornos y volatilidad
- Matriz de correlación
- 3 gráficos (PNG):
  - `price_trends.png` - Evolución de precios normalizados
  - `risk_return.png` - Gráfico riesgo vs retorno
  - `correlation_heatmap.png` - Matriz de correlación

## 📊 Ejemplo de Output

```
ANÁLISIS DE RETORNOS

 Ticker  Retorno Total (%)  Retorno Anual (%)  Volatilidad (%)  ...  Sharpe Ratio
    BTC                45.23             28.15            95.32             0.29
   AAPL                32.10             22.50             25.18             0.82
   MSFT                28.95             20.33             22.10             0.86
   TSLA               -12.34             -8.20             60.15            -0.27

MATRIZ DE CORRELACIÓN
           BTC       ETH      AAPL     MSFT     TSLA    GOOGL       SPY
BTC      1.000     0.82     0.35     0.25     0.42     0.28      0.31
ETH      0.82      1.000    0.28     0.20     0.38     0.22      0.27
AAPL     0.35      0.28     1.000    0.72     0.55     0.68      0.78
...

SUGERENCIA DE PORTAFOLIO ÓPTIMO
✅ Mejor relación riesgo-retorno: MSFT
   Sharpe Ratio: 0.86

📊 Portafolio diversificado sugerido (40-35-25):
   1. MSFT: 40%
   2. AAPL: 35%
   3. SPY: 25%

   Retorno esperado: 20.85%
   Volatilidad esperada: 22.33%
```

## 🔧 Customización

Edita `ASSETS` para analizar diferentes títulos:

```python
ASSETS = {
    'BTC': 'Bitcoin',        # Cripto
    'AAPL': 'Apple',         # Acción USA
    'SQQQ.BA': 'Nasdaq ETF', # Argentina
    'GOLD': 'Oro',           # Commodities
}
```

O cambia el período:
```python
PERIOD = '3y'  # 3 años de datos
```

## 📈 Conceptos Explicados

### Sharpe Ratio
Mide retorno ajustado por riesgo. Mayor = mejor.
- Formula: `(Retorno - Tasa Libre Riesgo) / Volatilidad`
- Sharpe > 1: Bueno
- Sharpe > 2: Excelente

### Maximum Drawdown
Peor pérdida desde pico a valle.
- -50% = perdió la mitad desde su máximo

### Volatilidad Anualizada
Desviación estándar de retornos diarios, escalada a un año.
- Volatilidad alta = más riesgo

### Correlación
Cómo se mueven dos activos juntos.
- 1.0 = perfectamente correlacionados
- 0.0 = independientes
- -1.0 = inversamente correlacionados

## 🎓 Casos de Uso

1. **Análisis de portafolio**: ¿Cuál es mi mejor opción?
2. **Diversificación**: ¿Cuáles activos no se correlacionan?
3. **Evaluación de riesgo**: ¿Cuál es el downside máximo?
4. **Backtesting básico**: ¿Hubiera funcionado mi estrategia?

## 📝 Limitaciones

- No es financial advice (solo análisis educativo)
- Datos históricos ≠ resultados futuros
- Sharpe Ratio asume distribución normal (real no lo es)
- No incluye costos de transacción ni impuestos

## 🔗 Fuentes de Datos

- **Yahoo Finance** (vía yfinance): Acciones, ETFs, Criptos
- Gratuito, sin límite de llamadas, actualizado diariamente

## 📄 Licencia

Libre para usar, modificar y distribuir.



