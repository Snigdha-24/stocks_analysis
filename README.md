# Stock Analytics Dashboard

A full-stack web application for analyzing stock correlations and visualizing market data.

## Project Structure
```
stock_analysis/
├── backend/               # Flask backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   ├── models/
│   │   └── utils/
│   ├── config.py
│   └── requirements.txt
└── frontend/             # React frontend
    ├── public/
    ├── src/
    └── package.json
```

## Setup Instructions

### Backend Setup
1. Create a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up MongoDB:
- Install MongoDB locally or use MongoDB Atlas
- Update connection string in config.py

4. Run the Flask server:
```bash
python run.py
```

### Frontend Setup
1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## Features
- User authentication with JWT
- Real-time stock data visualization
- Correlation analysis with benchmark
- Interactive charts using Chart.js
- Data caching with MongoDB

## Tech Stack
- Frontend: React, Chart.js, Axios
- Backend: Flask, JWT, yfinance
- Database: MongoDB
