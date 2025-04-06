from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

from .weather_service import get_weather

load_dotenv()

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.secret_key = os.environ.get("SECRET_KEY")

limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])


@app.route("/weather/<city>", methods=["GET"])
@limiter.limit("10/minute")
def weather_endpoint(city):

    try:
        result = get_weather(city)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 500
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 502


if __name__ == "__main__":
    app.run(debug=True, port=5000)
