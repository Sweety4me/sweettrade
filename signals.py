import yfinance as yf
import matplotlib.pyplot as plt

def generate_trade_signal(ticker):
    df = yf.download(ticker, period='5d', interval='15m')
    df['EMA'] = df['Close'].ewm(span=9, adjust=False).mean()

    latest_close = df['Close'].iloc[-1]
    latest_ema = df['EMA'].iloc[-1]

    signal = "No Signal"
    if latest_close > latest_ema:
        signal = "🔥 BUY Signal"
    elif latest_close < latest_ema:
        signal = "🔻 SELL Signal"

    # Plot chart
    fig, ax = plt.subplots()
    df[['Close', 'EMA']].plot(ax=ax)
    ax.set_title(f"{ticker} - Price & EMA")
    return signal, fig
