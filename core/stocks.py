import yfinance as yf


class StocksAnalyze:

    def __init__(self) -> None:
        pass

    def get_stock(self, symbol: str) -> list:
        ticker = yf.download(symbol, progress=False,
                             interval='1d', period='1mo')
        ticker.index = ticker.index.strftime('%Y-%m-%d')
        ticker = ticker.reset_index()
        return [{column.lower().rstrip(): value for column, value in zip(
            ticker.columns, row)} for row in ticker.values]


if __name__ == '__main__':
    stock = StocksAnalyze()
    print(stock.get_stock('ITSA4.SA'))
