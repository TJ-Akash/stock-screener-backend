import traceback
import psycopg2
import uvicorn
from _decimal import Decimal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
import requests
import decimal
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Stock(BaseModel):
    symbol: str
    company_name: str
    price:Decimal | None = None
    market_cap: Decimal | None = None
    dividend: Decimal | None = None
    volume: int

# PostgreSQL connection parameters
DB_NAME = 'StockScreener'
DB_USER = 'postgres'
DB_PASSWORD = 'admin'
DB_HOST = 'localhost'
PORT = '5432'

# Connect to PostgreSQL database
conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=PORT)
cur = conn.cursor()

class StockFilter(BaseModel):
    price: float = None
    market_cap: float = None
    dividend_yield: float = None

@app.post("/add-stocks/")
async def add_stocks():
    try:
        api_key = 'njejJLMhYCtSFdhQY02N0RtuC2IYTpuZ'
        response = requests.get(f'https://financialmodelingprep.com/api/v3/stock-screener?apikey={api_key}')
        all_stocks = response.json()
        if len(all_stocks) > 0:
            for stock in all_stocks:
                market_cap = stock.get('marketCap', 'N/A')
                companyName = stock.get('companyName', 'N/A')
                symbol = stock.get('symbol', 'N/A')
                volume = stock.get('volume', 'N/A')
                lastAnnualDividend = stock.get('lastAnnualDividend', 'N/A')
                price = stock.get('price', 'N/A')
                cur.execute("INSERT INTO \"Analysis\".stocklist (symbol, company_name, price, market_cap, "
                            "dividend, volume) VALUES (%s, %s, %s, %s, %s, %s)",
                            (symbol, companyName, price, market_cap, lastAnnualDividend, volume))
                print(cur.query)
                conn.commit()
            return all_stocks
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get-stocks/")
async def get_stocks():
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT symbol, company_name,
                   price::numeric(10, 2) AS price,  -- Cast price to numeric with precision and scale (adjust as needed)
                   market_cap::numeric(15, 2) AS market_cap, -- Cast market_cap to numeric with precision and scale (adjust as needed)
                   dividend::numeric(10, 2) AS dividend, -- Cast dividend to numeric with precision and scale (adjust as needed)
                   volume
            FROM "Analysis"."stocklist"  -- Replace with your actual schema name if applicable
        """)

        rows = cur.fetchall()
        stocks = []
        for row in rows:
            symbol = row[0]
            company_name = row[1]
            price = decimal.Decimal(row[2]) if row[2] else None
            market_cap = decimal.Decimal(row[3]) if row[3] else None
            dividend = decimal.Decimal(row[4]) if row[4] else None
            volume = row[5]
            try:
                stock = Stock(
                    symbol=symbol,
                    company_name=company_name,
                    price=price,
                    market_cap=market_cap,
                    dividend=dividend,
                    volume=volume
                )
                stocks.append(stock)
            except ValidationError as e:
                print(f"Validation Error for Stock (symbol: {symbol}): {e}")
        cur.close()
        conn.close()
        return stocks

    except Exception as e:
        print(f"Error fetching data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, port=55280)