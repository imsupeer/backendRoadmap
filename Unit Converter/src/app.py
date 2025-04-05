from flask import Flask, request, render_template
from .conversions import convert_length, convert_weight, convert_temperature

unitConversorApp = Flask(
    __name__, template_folder="../templates", static_folder="../static"
)


@unitConversorApp.route("/length", methods=["GET", "POST"])
def length():
    result = None
    if request.method == "POST":
        value_str = request.form.get("value", "").strip()
        from_unit = request.form.get("from_unit", "").strip()
        to_unit = request.form.get("to_unit", "").strip()
        try:
            value = float(value_str)
            converted = convert_length(value, from_unit, to_unit)
            result = f"{value} {from_unit} = {converted:.4f} {to_unit}"
        except Exception as e:
            result = f"Erro: {str(e)}"
    return render_template("length.html", result=result)


@unitConversorApp.route("/weight", methods=["GET", "POST"])
def weight():
    result = None
    if request.method == "POST":
        value_str = request.form.get("value", "").strip()
        from_unit = request.form.get("from_unit", "").strip()
        to_unit = request.form.get("to_unit", "").strip()
        try:
            value = float(value_str)
            converted = convert_weight(value, from_unit, to_unit)
            result = f"{value} {from_unit} = {converted:.4f} {to_unit}"
        except Exception as e:
            result = f"Erro: {str(e)}"
    return render_template("weight.html", result=result)


@unitConversorApp.route("/temperature", methods=["GET", "POST"])
def temperature():
    result = None
    if request.method == "POST":
        value_str = request.form.get("value", "").strip()
        from_unit = request.form.get("from_unit", "").strip()
        to_unit = request.form.get("to_unit", "").strip()
        try:
            value = float(value_str)
            converted = convert_temperature(value, from_unit, to_unit)
            result = f"{value} {from_unit} = {converted:.2f} {to_unit}"
        except Exception as e:
            result = f"Erro: {str(e)}"
    return render_template("temperature.html", result=result)


if __name__ == "__main__":
    unitConversorApp.run(debug=True)
