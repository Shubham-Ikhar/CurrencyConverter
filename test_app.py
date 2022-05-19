from unittest.mock import patch, MagicMock
from app import CurrencyConverter
import unittest


class TestCurrencyConverter(unittest.TestCase):

    def test_success_get_exchange_rate(self):
        source = "GBP"
        target = "EUR"
        mgc = CurrencyConverter().get_exchange_rate(source, target)
        assert '1999-01' in mgc.to_string()

    @patch("requests.get", MagicMock(side_effect=Exception('error')))
    def test_success_get_exchange_rate_exception(self):
        mgc = CurrencyConverter().get_exchange_rate(1,1)
        assert mgc == ('Get Exchange Rate responded with an error: error', 412)

    def test_success_get_raw_data(self):
        identifier = 'M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N'
        mgc = CurrencyConverter().get_raw_data(identifier)
        assert '1999-01' in mgc.to_string()

    @patch("requests.get", MagicMock(side_effect=Exception('error')))
    def test_success_get_raw_data_exception(self):
        mgc = CurrencyConverter().get_raw_data(1)
        assert mgc == ('Get Raw Data responded with an error: error', 412)

    def test_success_get_data_if_condition(self):
        identifier = 'M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N'
        mgc = CurrencyConverter().get_data(identifier)
        assert '1999-01' in mgc.to_string()

    def test_success_get_data_else_condition(self):
        identifier = 'M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N'
        target = 'EUR'
        mgc = CurrencyConverter().get_data(identifier, target)
        assert 'TIME_PERIOD' in mgc.to_string()


if __name__ == '__main__':
    unittest.main()
