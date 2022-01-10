import pandas as pd
from dashboard.creds import API_KEY as ak

class SingleState:
    def __init__(self, state):
        self.state = pd.read_csv("https://api.covidactnow.org/v2/state/{}.timeseries.csv?apiKey={}".format(state, ak))
    
    def get_latest_data(self):
        latest = self.state.iloc[-1]
        return latest.to_dict()

    def get_yesterday_data(self):
        return self.state.iloc[-2].to_dict()

    def cases_from_start(self):
        return self.state['actuals.newCases'].tolist()


    
