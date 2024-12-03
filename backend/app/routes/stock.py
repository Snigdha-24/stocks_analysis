from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

stock_bp = Blueprint('stock', __name__)

def fetch_stock_data(ticker, start_date, end_date):
    # Check cache first
    cached_data = current_app.db.stocks.find_one({
        'ticker': ticker,
        'start_date': start_date,
        'end_date': end_date
    })
    
    if cached_data:
        return pd.DataFrame(cached_data['data'])
    
    # Fetch from Yahoo Finance if not cached
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date, interval='1mo')
    
    # Cache the data
    current_app.db.stocks.insert_one({
        'ticker': ticker,
        'start_date': start_date,
        'end_date': end_date,
        'data': data.to_dict('records'),
        'timestamp': datetime.utcnow()
    })
    
    return data

def calculate_sharpe_ratio(returns, risk_free_rate=0.03):
    """Calculate the Sharpe ratio for a given series of returns."""
    excess_returns = returns - risk_free_rate
    return {
        'annualizedReturn': returns.mean() * 12,  # Monthly to annual
        'riskFreeRate': risk_free_rate,
        'annualizedStdDev': returns.std() * np.sqrt(12),  # Monthly to annual
        'sharpeRatio': (excess_returns.mean() * 12) / (returns.std() * np.sqrt(12))
    }

@stock_bp.route('/fetch-stock', methods=['GET'])
@jwt_required()
def fetch_stock():
    ticker = request.args.get('ticker')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not all([ticker, start_date, end_date]):
        return jsonify({'error': 'Missing parameters'}), 400
    
    if ticker not in current_app.config['ALLOWED_TICKERS'] + [current_app.config['BENCHMARK_TICKER']]:
        return jsonify({'error': 'Invalid ticker'}), 400
    
    try:
        data = fetch_stock_data(ticker, start_date, end_date)
        return jsonify({'data': data['Close'].to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stock_bp.route('/correlation', methods=['GET'])
@jwt_required()
def get_correlation():
    ticker = request.args.get('ticker')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not all([ticker, start_date, end_date]):
        return jsonify({'error': 'Missing parameters'}), 400
    
    try:
        # Fetch stock and benchmark data
        stock_data = fetch_stock_data(ticker, start_date, end_date)['Close']
        benchmark_data = fetch_stock_data(current_app.config['BENCHMARK_TICKER'], 
                                        start_date, end_date)['Close']
        
        # Calculate correlation
        correlation = stock_data.corr(benchmark_data)
        
        # Prepare scatter plot data
        scatter_data = {
            'x': benchmark_data.tolist(),
            'y': stock_data.tolist(),
            'correlation': correlation
        }
        
        # Calculate correlation matrix for heatmap
        all_tickers = current_app.config['ALLOWED_TICKERS'] + [current_app.config['BENCHMARK_TICKER']]
        corr_matrix = pd.DataFrame()
        
        for t in all_tickers:
            data = fetch_stock_data(t, start_date, end_date)['Close']
            corr_matrix[t] = data
        
        heatmap_data = corr_matrix.corr().to_dict()
        
        return jsonify({
            'scatter_data': scatter_data,
            'heatmap_data': heatmap_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stock_bp.route('/sharpe-ratio', methods=['GET'])
@jwt_required()
def get_sharpe_ratio():
    ticker = request.args.get('ticker')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not all([ticker, start_date, end_date]):
        return jsonify({'error': 'Missing parameters'}), 400
        
    try:
        # Fetch monthly stock data
        stock_data = fetch_stock_data(ticker, start_date, end_date)
        
        # Calculate monthly returns
        monthly_returns = stock_data['Close'].pct_change().dropna()
        
        # Calculate Sharpe ratio
        sharpe_data = calculate_sharpe_ratio(monthly_returns)
        
        return jsonify(sharpe_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
