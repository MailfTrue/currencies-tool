import httpx
from datetime import datetime
from models import Quotes, Currency


class CBRFApiException(httpx.HTTPError):
    """Raised when request to API failed"""


class CBRFClient:
    """
    Client for unofficial API Central Bank of Russian Federation
    """
    def __init__(self):
        self.client = httpx.AsyncClient(base_url="https://www.cbr-xml-daily.ru")

    async def get_daily(self):
        try:
            response = await self.client.get("/daily_json.js")
        except httpx.HTTPError as e:
            raise CBRFApiException from e

        json_resp = response.json()
        quotes = Quotes(
            date=datetime.fromisoformat(json_resp['Date']),
            previous_date=datetime.fromisoformat(json_resp['PreviousDate']),
            currencies=[Currency(
                id=currency['ID'],
                num_code=currency['NumCode'],
                char_code=currency['CharCode'],
                denomination=currency['Nominal'],
                name=currency['Name'],
                value=currency['Value'],
                previous=currency['Previous'],
            ) for currency in json_resp['Valute'].values()]
        )
        return quotes
