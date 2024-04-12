 # Stock Screener API
This is a FastAPI-based API for stock screening, fetching data from Financial Modeling Prep API and storing/retrieving in a PostgreSQL database. It allows users to add stocks to the database and retrieve them based on filters.

 ## Installation
 ### Clone the repository:

bash
git clone 'https://github.com/yourusername/stock-screener-api.git
cd stock-screener-api
Create a virtual environment (recommended):

bash
'''python3 -m venv venv
venv\Scripts\activate      # For Windows

 ### Install the dependencies:
bash
'pip install -r requirements.txt

Set up PostgreSQL:

Create a PostgreSQL database named StockScreener.
Update the connection parameters in main.py if needed (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, PORT).
Usage

Run the FastAPI server:

bash
'''uvicorn main:app --reload
Access the API at http://localhost:55280/.

Endpoints
'''POST /add-stocks/

Fetches stock data from Financial Modeling Prep API and adds them to the database.
POST /get-stocks/

Retrieves stocks from the database, with optional filtering parameters.
Example Usage
Adding Stocks
bash
Copy code
curl -X POST "http://localhost:55280/add-stocks/"
Getting Stocks
bash
Copy code
curl -X POST "http://localhost:55280/get-stocks/"
Data Model
Stock Schema
json
Copy code
{
  "symbol": "AAPL",
  "company_name": "Apple Inc.",
  "price": 1500.00,
  "market_cap": 2000000000.00,
  "dividend": 4.25,
  "volume": 1000000
}
Technologies Used
Python
FastAPI
PostgreSQL
Requests
Contributing
Fork the repository.
 ### Create a new branch (git checkout -b feature/new-feature).
Make your changes.
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature/new-feature).
Create a new Pull Request.

 ### License
This project is licensed under the MIT License - see the LICENSE file for details.
