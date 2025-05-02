import requests
import pandas as pd
import utils
import defs

class OandoAPI():

    def __init__(self):
        self.session = requests.Session()


    def fetch_instruments(self):
        url = f"{defs.OANDO_URL}/accounts/{defs.ACCOUNT_ID}/instruments"
        response = self.session.get(url, headers=defs.SECURE_HEADER, params=None)
        return response.status_code, response.json()

    def get_instruments_df(self):
        code, data = self.fetch_instruments()
        if code == 200:
            df = pd.DataFrame.from_dict(data['instruments'])
            return df[['name', 'type', 'displayName', 'pipLocation', 'marginRate']]
        else:
            return None
        
    def save_instruments(self):
        df = self.get_instruments_df()
        if df is not None:
            df.to_pickle(utils.get_instruments_data_filename())
           


    def fetch_candles(self, pair_name, count, granularity):
        url = f"{defs.OANDO_URL}/instruments/{pair_name}/candles"

        params = dict(
            count = count,
            granularity = granularity,
            price = 'MBA'
        )

        response = self.session.get(url, headers=defs.SECURE_HEADER, params=params)

        return response.status_code, response.json()
    


if __name__ == "__main__":
    api = OandoAPI()
    api.save_instruments()
    
