import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/stock_analysis')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Stock tickers configuration
    ALLOWED_TICKERS = ['AAPL', 'NVDA', 'MSFT', 'AMZN', 'META']
    BENCHMARK_TICKER = '^NDX'
