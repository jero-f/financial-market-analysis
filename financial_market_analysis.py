"""
Financial Market Analysis - Análisis de Mercados Financieros
Descarga datos públicos de Yahoo Finance y realiza análisis interesante
VERSIÓN CORREGIDA
"""

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════

# Activos a analizar (acciones, criptos, índices)
ASSETS = {
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'AAPL': 'Apple',
    'MSFT': 'Microsoft',
    'TSLA': 'Tesla',
    'GOOGL': 'Google',
    'SPY': 'S&P 500 ETF',
}

# Período de análisis
PERIOD = '1y'  # 1 año de datos
START_DATE = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
END_DATE = datetime.now().strftime('%Y-%m-%d')

# ═══════════════════════════════════════════════════════════════════
# DESCARGA DE DATOS
# ═══════════════════════════════════════════════════════════════════

def download_data(assets, start, end):
    """Descarga datos de Yahoo Finance"""
    print(f"📊 Descargando datos de {start} a {end}...")
    
    data = {}
    for ticker, name in assets.items():
        try:
            print(f"  ⏳ {name} ({ticker})...", end=' ')
            df = yf.download(ticker, start=start, end=end, progress=False)
            data[ticker] = df
            print("✅")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return data

# ═══════════════════════════════════════════════════════════════════
# ANÁLISIS DE RETORNOS
# ═══════════════════════════════════════════════════════════════════

def analyze_returns(data):
    """Calcula retornos y volatilidad"""
    print("\n📈 ANÁLISIS DE RETORNOS\n")
    
    results = []
    
    for ticker, df in data.items():
        # Retorno total
        price_start = df['Close'].iloc[0]
        price_end = df['Close'].iloc[-1]
        total_return = ((price_end - price_start) / price_start) * 100
        
        # Retorno anualizado
        daily_returns = df['Close'].pct_change()
        annual_return = (daily_returns.mean() * 252) * 100
        
        # Volatilidad anualizada
        volatility = (daily_returns.std() * np.sqrt(252)) * 100
        
        # Máximo drawdown
        cumulative = (1 + daily_returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min() * 100
        
        # Ratio de Sharpe (asumiendo 2% como tasa libre de riesgo)
        risk_free_rate = 0.02
        
        # CORRECCIÓN IMPORTANTE: Convertir a float para evitar error de pandas
        volatility_float = float(volatility)
        annual_return_float = float(annual_return)
        
        if volatility_float > 0:
            sharpe = (annual_return_float/100 - risk_free_rate) / (volatility_float/100)
        else:
            sharpe = 0
        
        results.append({
            'Ticker': ticker,
            'Retorno Total (%)': round(total_return, 2),
            'Retorno Anual (%)': round(annual_return_float, 2),
            'Volatilidad (%)': round(volatility_float, 2),
            'Max Drawdown (%)': round(float(max_drawdown), 2),
            'Sharpe Ratio': round(sharpe, 2),
            'Precio Actual': round(float(price_end), 2),
        })
    
    df_results = pd.DataFrame(results)
    print(df_results.to_string(index=False))
    
    return df_results

# ═══════════════════════════════════════════════════════════════════
# ANÁLISIS DE CORRELACIÓN
# ═══════════════════════════════════════════════════════════════════

def analyze_correlation(data):
    """Calcula correlación entre activos"""
    print("\n\n🔗 MATRIZ DE CORRELACIÓN\n")
    
    # Obtener retornos diarios
    returns = pd.DataFrame()
    for ticker, df in data.items():
        returns[ticker] = df['Close'].pct_change()
    
    # Correlación
    correlation = returns.corr()
    print(correlation.round(3).to_string())
    
    return correlation, returns

# ═══════════════════════════════════════════════════════════════════
# VISUALIZACIONES
# ═══════════════════════════════════════════════════════════════════

def plot_price_trends(data):
    """Grafica tendencia de precios normalizados"""
    plt.figure(figsize=(14, 8))
    
    for ticker, df in data.items():
        # Normalizar precios (100 = primer día)
        normalized = (df['Close'] / df['Close'].iloc[0]) * 100
        plt.plot(normalized.index, normalized.values, label=ticker, linewidth=2)
    
    plt.title('Tendencia de Precios Normalizados (últimos 12 meses)', fontsize=14, fontweight='bold')
    plt.xlabel('Fecha', fontsize=12)
    plt.ylabel('Precio Normalizado (100 = inicio)', fontsize=12)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('price_trends.png', dpi=150)
    print("\n💾 Gráfico guardado: price_trends.png")
    plt.show()

def plot_volatility_vs_return(results):
    """Grafica Riesgo vs Retorno (Sharpe frontier)"""
    plt.figure(figsize=(12, 8))
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
    
    for i, row in results.iterrows():
        plt.scatter(row['Volatilidad (%)'], 
                   row['Retorno Anual (%)'],
                   s=300, alpha=0.7, color=colors[i % len(colors)],
                   edgecolors='black', linewidth=2)
        plt.text(row['Volatilidad (%)'] + 1, 
                row['Retorno Anual (%)'],
                row['Ticker'], 
                fontsize=10, fontweight='bold')
    
    plt.title('Riesgo vs Retorno (Frontera Eficiente)', fontsize=14, fontweight='bold')
    plt.xlabel('Volatilidad Anualizada (%)', fontsize=12)
    plt.ylabel('Retorno Anual (%)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='r', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig('risk_return.png', dpi=150)
    print("💾 Gráfico guardado: risk_return.png")
    plt.show()

def plot_correlation_heatmap(correlation):
    """Heatmap de correlación"""
    plt.figure(figsize=(10, 8))
    
    # Crear heatmap manual
    im = plt.imshow(correlation.values, cmap='RdYlGn', aspect='auto', vmin=-1, vmax=1)
    
    # Labels
    plt.xticks(range(len(correlation)), correlation.columns, rotation=45)
    plt.yticks(range(len(correlation)), correlation.columns)
    
    # Valores en celdas
    for i in range(len(correlation)):
        for j in range(len(correlation)):
            text = plt.text(j, i, f'{correlation.values[i, j]:.2f}',
                          ha="center", va="center", color="black", fontsize=9, fontweight='bold')
    
    plt.title('Matriz de Correlación de Retornos', fontsize=14, fontweight='bold')
    plt.colorbar(im)
    plt.tight_layout()
    plt.savefig('correlation_heatmap.png', dpi=150)
    print("💾 Gráfico guardado: correlation_heatmap.png")
    plt.show()

# ═══════════════════════════════════════════════════════════════════
# INSIGHT INTERESANTE: MEJOR PORTAFOLIO
# ═══════════════════════════════════════════════════════════════════

def suggest_portfolio(results):
    """Sugiere portafolio óptimo basado en Sharpe Ratio"""
    print("\n\n🎯 SUGERENCIA DE PORTAFOLIO ÓPTIMO\n")
    
    best_sharpe = results.loc[results['Sharpe Ratio'].idxmax()]
    print(f"✅ Mejor relación riesgo-retorno: {best_sharpe['Ticker']}")
    print(f"   Sharpe Ratio: {best_sharpe['Sharpe Ratio']}")
    print(f"   Retorno: {best_sharpe['Retorno Anual (%)']}% | Volatilidad: {best_sharpe['Volatilidad (%)']}\n")
    
    # Diversificación simple
    best_3 = results.nlargest(3, 'Sharpe Ratio')
    weights = [0.4, 0.35, 0.25]
    
    print("📊 Portafolio diversificado sugerido (40-35-25):")
    weighted_return = 0
    weighted_volatility = 0
    
    for idx, (i, row) in enumerate(best_3.iterrows()):
        print(f"   {idx+1}. {row['Ticker']}: {weights[idx]*100:.0f}%")
        weighted_return += row['Retorno Anual (%)'] * weights[idx]
        weighted_volatility += row['Volatilidad (%)'] * weights[idx]
    
    print(f"\n   Retorno esperado: {weighted_return:.2f}%")
    print(f"   Volatilidad esperada: {weighted_volatility:.2f}%")

# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("="*70)
    print("ANÁLISIS DE MERCADOS FINANCIEROS 📊")
    print("="*70)
    
    # Descargar datos
    data = download_data(ASSETS, START_DATE, END_DATE)
    
    if not data:
        print("❌ Error: No se pudieron descargar los datos")
        exit()
    
    # Análisis
    results = analyze_returns(data)
    correlation, returns = analyze_correlation(data)
    
    # Visualizaciones
    plot_price_trends(data)
    plot_volatility_vs_return(results)
    plot_correlation_heatmap(correlation)
    
    # Insights
    suggest_portfolio(results)
    
    print("\n" + "="*70)
    print("✅ Análisis completado")
    print("="*70)