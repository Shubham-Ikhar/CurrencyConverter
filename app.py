from typing import Optional
import pandas as pd
from bs4 import BeautifulSoup
import requests
import logging


class CurrencyConverter:
    def __init__(self):
        self.exchange_rate_url = "https://sdw-wsrest.ecb.europa.eu/service/data/EXR/M.{}.{}.SP00.A?detail=dataonly"
        self.get_raw_data_url = "https://sdw-wsrest.ecb.europa.eu/service/data/BP6/{}?detail=dataonly"

    def process_request(self, url):
        """
        Process and GET provided url content
        """
        return requests.get(url)

    def extract_content(self, xml_object):
        """
        Extract XML object using BeatifulSoup
        """
        soup = BeautifulSoup(xml_object.content, 'lxml')
        generic_tag = soup.find_all('generic:obs')
        time_period = soup.find_all('generic:obsdimension')
        obs_value = soup.find_all('generic:obsvalue')
        return soup, generic_tag, time_period, obs_value

    def get_exchange_rate(self, source: str, target: str = "EUR") -> pd.DataFrame:
        """
        THis method is used to get the exchange rate of source and targeted currency which we passed.
        :param source:
        :param target:
        :return:  pd.DataFrame
        """
        logging.info("Get Exchange Rate initiated.")
        try:
            xml = self.process_request(self.exchange_rate_url.format(source, target))
            soup, generic_tag, time_period, obs_value = self.extract_content(xml)

            data = []
            for i in range(0, len(generic_tag)):
                rows = [time_period[i]['value'], obs_value[i]['value']]
                data.append(rows)

            df = pd.DataFrame(data, columns=['TIME_PERIOD', 'OBS_VALUE'], dtype=float)
            return df.head()
        except Exception as err:
            logging.error(f'Error when fetching data from sdw: {str(err)}')
            return f'Get Exchange Rate responded with an error: {str(err)}', 412

    # print(get_exchange_rate(source="GBP"))

    def get_raw_data(self, identifier: str) -> pd.DataFrame:
        try:
            xml = self.process_request(self.get_raw_data_url.format(identifier))
            soup, generic_tag, time_period, obs_value = self.extract_content(xml)

            data = []
            for i in range(0, len(generic_tag)):
                rows = [time_period[i]['value'], obs_value[i]['value']]
                data.append(rows)

            df = pd.DataFrame(data, columns=['TIME_PERIOD', 'OBS_VALUE'], dtype=float)
            return df.head()
        except Exception as e:
            logging.error(f'Error when fetching data from sdw: {str(e)}')
            return f'Get Raw Data responded with an error: {str(e)}', 412

    # print(get_raw_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N"))

    def get_data(self, identifier: str, target_currency: Optional[str] = None) -> pd.DataFrame:
        """
        #     This Function works on the target_currency value provided by user, If the target_currency parameter is None,
        #     then it will return the DataFrame as-is like in the get_raw_data method.
        #     Else convert the data from the source currency to the target one, defined by the target_currency parameter.
        #     :param identifier:
        #     :param target_currency:
        #     :return:  pd.DataFrame
        #     """
        if not target_currency:
            return self.get_raw_data(identifier)
        source_currency = identifier.split(".")[12]
        return self.get_exchange_rate(source_currency, target_currency)


if __name__ == "__main__":
    print("Output of Get Exchange Method:")
    print(CurrencyConverter().get_exchange_rate("GBP"))
    print("Output of Get Raw Data Method:")
    print(CurrencyConverter().get_raw_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N"))