LENGTH_FACTORS = {
    "millimeter": 0.001,
    "centimeter": 0.01,
    "meter": 1.0,
    "kilometer": 1000.0,
    "inch": 0.0254,
    "foot": 0.3048,
    "yard": 0.9144,
    "mile": 1609.344,
}


def convert_length(value, from_unit, to_unit):

    if from_unit not in LENGTH_FACTORS or to_unit not in LENGTH_FACTORS:
        raise ValueError("Invalid length unit.")

    base_value = value * LENGTH_FACTORS[from_unit]
    converted_value = base_value / LENGTH_FACTORS[to_unit]
    return converted_value


WEIGHT_FACTORS = {
    "milligram": 1e-6,
    "gram": 1e-3,
    "kilogram": 1.0,
    "ounce": 0.0283495,
    "pound": 0.453592,
}


def convert_weight(value, from_unit, to_unit):

    if from_unit not in WEIGHT_FACTORS or to_unit not in WEIGHT_FACTORS:
        raise ValueError("Invalid weight unit.")

    base_value = value * WEIGHT_FACTORS[from_unit]
    converted_value = base_value / WEIGHT_FACTORS[to_unit]
    return converted_value


def convert_temperature(value, from_unit, to_unit):
    valid_units = ["Celsius", "Fahrenheit", "Kelvin"]
    if from_unit not in valid_units or to_unit not in valid_units:
        raise ValueError("Invalid temperature unit.")

    if from_unit == "Celsius":
        celsius = value
    elif from_unit == "Fahrenheit":
        celsius = (value - 32) * 5.0 / 9.0
    else:
        celsius = value - 273.15

    if to_unit == "Celsius":
        return celsius
    elif to_unit == "Fahrenheit":
        return celsius * 9.0 / 5.0 + 32
    else:
        return celsius + 273.15
