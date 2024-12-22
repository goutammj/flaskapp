from flask import Flask, jsonify, request
import yfinance as yf

app = Flask(__name__)

@app.route('/api-stocks', methods=['GET'])
def get_nse_stock():
    # Get the ticker from the query parameter
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({"error": "Please provide a ticker symbol"}), 400

    # Append '.NS' to the ticker to fetch NSE data
    ticker = f"{ticker.upper()}.NS"

    try:
        # Fetch stock data
        stock = yf.Ticker(ticker)
        info = stock.info

        # Extract relevant data
        stock_data = {
            "ticker": ticker,
            "market_cap": info.get("marketCap", "N/A"),
            "current_price": info.get("currentPrice", "N/A"),
            "high_52_week": info.get("fiftyTwoWeekHigh", "N/A"),
            "low_52_week": info.get("fiftyTwoWeekLow", "N/A"),
            "stock_pe": info.get("trailingPE", "N/A"),
            "book_value": info.get("bookValue", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "roce": info.get("returnOnEquity", "N/A"),  # ROCE is not directly available, using ROE instead
            "roe": info.get("returnOnEquity", "N/A"),
            "face_value": info.get("faceValue", "N/A"),
        }

        return jsonify({"status": "success", "data": stock_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
