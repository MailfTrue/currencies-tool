from fastapi import FastAPI, Body, HTTPException, status, responses
from cbrf import CBRFClient, CBRFApiException
import helpers

app = FastAPI()
cbrf = CBRFClient()


@app.get("/api/currencies")
async def get_currencies():
    try:
        return (await cbrf.get_daily()).currencies
    except CBRFApiException:
        raise HTTPException(detail="Sorry, quote service unavailable, try later",
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@app.post("/api/quotes")
async def get_quotes(necessary_currencies: list[str] = Body(..., min_items=1), export_to: str | None = None):
    try:
        quotes = await cbrf.get_daily()
    except CBRFApiException:
        raise HTTPException(detail="Sorry, quote service unavailable, try later",
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    # Filter only requested currencies with uppercase
    quotes.currencies = [currency
                         for currency in quotes.currencies
                         if currency.char_code in [k.upper() for k in necessary_currencies]]
    if export_to is None:
        return quotes
    elif export_to in ("csv", "xlsx"):
        header = ("Код валюты", "Название валюты", "Номинал", "Цена", "Дата котировки")
        rows = [(currency.char_code, currency.name, currency.denomination, currency.value,
                 quotes.date.strftime("%d.%m.%Y %H:%M"))
                for currency in quotes.currencies]
        if export_to == "csv":
            return responses.StreamingResponse(helpers.render_csv(header, rows), media_type="text/csv")
        else:
            return responses.StreamingResponse(
                helpers.render_xlsx(header, rows),
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    elif export_to in ("html", "pdf"):
        html = helpers.render_jinja("currencies.html", {"quotes": quotes})
        if export_to == "html":
            return responses.HTMLResponse(html)
        else:
            return responses.StreamingResponse(helpers.render_pdf(html), media_type="application/pdf")
