import lseg.data as ld
import datetime as dt
import numpy as np
import pandas as pd

class DataFromSource():    
    def __init__(self, RIC):
        self.RIC = RIC

    def __str__(self):
        return f"{self.RIC}"

    def get_session(self):
        try:
            ld.open_session()
        except Exception as e:
            print(f"Error opening session: {e}")
        return ld
    
    def get_timeframe(self):
        today = dt.date.today()
        initial_day = today - dt.timedelta(days=365)
        return today, initial_day
    
    def get_prices(self):
        ld = self.get_session()
        today, initial_day = self.get_timeframe()
        try:
            data = ld.get_history(universe=[self.RIC], fields=['TR.PriceClose'], interval="1D",
               start = initial_day, end = today)
            return data
        except Exception as e:
            print(f"Error retrieving data for {self.RIC}: {e}")
            return None 
        
    def get_daily_returns(self):
        prices = self.get_prices()
        if prices is not None:
            try:
                prices['Close'] = prices['Price Close'].astype(float)
                prices[self.RIC] = np.log(prices['Close'].div(prices['Close'].shift(1)))
                daily_returns = prices.drop(['Price Close', 'Close'], axis=1)
                return daily_returns
            except Exception as e:
                print(f"Error calculating daily returns for {self.RIC}: {e}")
                return None
        else:
            return None