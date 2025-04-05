import unittest
from src import conversions


class TestConversions(unittest.TestCase):
    def test_convert_length(self):
        self.assertAlmostEqual(
            conversions.convert_length(1, "meter", "centimeter"), 100.0, places=4
        )
        self.assertAlmostEqual(
            conversions.convert_length(1, "foot", "inch"), 12.0, places=4
        )
        self.assertAlmostEqual(
            conversions.convert_length(1, "mile", "meter"), 1609.344, places=3
        )

    def test_convert_weight(self):
        self.assertAlmostEqual(
            conversions.convert_weight(1, "kilogram", "gram"), 1000.0, places=4
        )
        self.assertAlmostEqual(
            conversions.convert_weight(1, "pound", "ounce"), 16.0, places=2
        )
        self.assertAlmostEqual(
            conversions.convert_weight(1000, "milligram", "gram"), 1.0, places=4
        )

    def test_convert_temperature(self):
        self.assertAlmostEqual(
            conversions.convert_temperature(0, "Celsius", "Fahrenheit"), 32.0, places=4
        )
        self.assertAlmostEqual(
            conversions.convert_temperature(273.15, "Kelvin", "Celsius"), 0.0, places=4
        )
        self.assertAlmostEqual(
            conversions.convert_temperature(100, "Celsius", "Fahrenheit"),
            212.0,
            places=4,
        )

    def test_invalid_length_unit(self):
        with self.assertRaises(ValueError):
            conversions.convert_length(1, "invalid_unit", "meter")

    def test_invalid_weight_unit(self):
        with self.assertRaises(ValueError):
            conversions.convert_weight(1, "kilogram", "invalid_unit")

    def test_invalid_temperature_unit(self):
        with self.assertRaises(ValueError):
            conversions.convert_temperature(100, "invalid", "Celsius")


if __name__ == "__main__":
    unittest.main()
