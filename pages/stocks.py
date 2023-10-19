from nicegui import events
import nicegui
from database.data import DataBase
from pages.validations import Validate
from core.stocks import StocksAnalyze


class StocksPage(DataBase):

    def __init__(self, nicegui: nicegui) -> None:
        super().__init__()
        self.ui = nicegui.ui

    def body(self):
        with self.ui.header(elevated=True).style('background-color: #3874c8;'):  # Header
            self.ui.label('Stocks').style('font-size: 20px;')
        # Left Drawer
        with self.ui.dialog() as dialog, self.ui.card():
            def __add_stock():
                validate = Validate
                if validate.validate_stocks(name.value, symbol.value) is True:
                    if self.insert_stock(name.value, symbol.value) is True:
                        self.ui.notify(message=f'Stock {name.value} added',
                                       type='positive', position='top-right')
                        self.select_stocks.update()

                    else:
                        self.ui.notify(message='Stock already registered',
                                       type='negative', position='top-right')
                self.ui.update(self.select_stocks)
                dialog.close()
            self.ui.label('Add new stocks').style('font-size: 20px;')
            name = self.ui.input('Name').style('width: 100%;')
            symbol = self.ui.input('Symbol').style('width: 100%;')
            self.ui.button('Close', on_click=dialog.close).style(
                'width: 100%;')
            self.ui.button('Add', on_click=__add_stock).style('width: 100%;')
        with self.ui.left_drawer(fixed=False).style('background-color: #3874c8;'):
            with self.ui.row().style('padding: 10px; justify-content: center;'):
                self.ui.label('Painel').style('font-size: 20px; color: white;')
                self.select_stocks = self.ui.select(
                    options=self.list_stock(), on_change=self.__update_values).style('width: 100%;')
                self.ui.button('Add', on_click=dialog.open, icon='add').style(
                    'width: 100%; margin-top: 10px;')
        with self.ui.row().style('padding: 10px; justify-content: center; width: 100%;'):  # Body
            with self.ui.column():  # Body
                self.title_table = self.ui.label(self.select_stocks.value if self.select_stocks.value else 'Select a stock',).style(
                    'font-size: 20px; width: 100%; text-align: center;')
                self.table = self.ui.table(
                    columns=[{'name': 'date', 'label': 'Date', 'field': 'date', 'sortable': True
                              }, {'name': 'open', 'label': 'Open', 'field': 'open', 'sortable': True
                                  }, {'name': 'high', 'label': 'High', 'field': 'high', 'sortable': True
                                      }, {'name': 'low', 'label': 'Low', 'field': 'low', 'sortable': True
                                          }, {'name': 'close', 'label': 'Close', 'field': 'close', 'sortable': True
                                              }, {'name': 'adj close', 'label': 'Adj Close', 'field': 'adj close', 'sortable': True
                                                  }, {'name': 'volume', 'label': 'Volume', 'field': 'volume', 'sortable': True}],
                    rows=[],
                    row_key='date',
                )
        with self.ui.footer().style('background-color: #3874c8;'):  # Footer
            self.ui.label('Footer').style('font-size: 20px;')

    def __update_values(self):
        self.table.rows = []
        [self.table.add_rows(row) for row in self.__get_stock()]
        self.title_table.text = self.select_stocks.value

    def __get_stock(self):
        stock = StocksAnalyze()
        return stock.get_stock(self.select_stocks.value) if self.select_stocks.value else []
