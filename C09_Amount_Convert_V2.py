import re
# Functions

def unit_compatibility(u1, u2):
    """Checks if units are compatible"""

    # Returns true if both the units have the same base unit.
    return units_dict[u1][0] == units_dict[u2][0]


def convert_amount(quantity, u1, u2):
    """Convert amount between compatible units"""
    # Checks if there are no units or both the amounts have the same unit
    if u1 is None or u2 is None or u1 == u2:
        return quantity

    # Takes the factor of both the units.
    factor_1 = units_dict[u1][1]
    factor_2 = units_dict[u2][1]

    # Calculates the converted quantity.
    converted_quantity = quantity * factor_1 / factor_2

    return converted_quantity


def get_amount_and_unit(question):
    """Gets the Amount and the Unit at once and returns them to the program."""

    while True:
        response = input(question).strip() # Removes any leading and trailing whitespaces.

        # Case 1 :  Simple integer with no Unit (e.g. 4 (eggs) or 10 (grapes))
        if response.isdigit():
            # Checks if the integer is equal to 0
            if int(response) == 0:
                print("❌ Please enter an integer greater than 0.")
                continue
            return int(response), None

        # Case 2 : Quantity with unit (e.g. 100g, 2 millilitres or 3 tablespoons)
        match = re.fullmatch(r"([0-9]*\.?[0-9]+)\s*([a-zA-Z]+)", response)
        # Checks if the input matches the pattern
        if not match:
            print("❌ Invalid input. Example: 100kg, 200ml, or just 4")
            continue

        number = float(match.group(1)) # Convert the quantity to float

        unit = match.group(2).lower() # Convert the unit to lowercase

        # Checks if the quantity is positive.
        if number <= 0:
            print("Please enter a number higher than 0.")
            continue

        # Checks if the unit is in the Units dictionary.
        if unit not in units_dict:
            print("❌ Invalid unit! Valid units include"
                  " weight classes(kg, g) and volume classes(l, ml)")
            continue

        return number, unit
    # Return None statement to avoid a light warning due to some IDE issues
    return None

units_dict = {
    # No unit
    None:("none",1),

    # Mass
    "g": ("g", 1), "gram": ("g", 1), "grams": ("g", 1),
    "kg": ("g", 1000), "kilogram": ("g", 1000), "kilograms": ("g", 1000),

    # Volume
    "ml": ("ml", 1), "milliliter": ("ml", 1), "milliliters": ("ml", 1),
    "l": ("ml", 1000), "liter": ("ml", 1000), "liters": ("ml", 1000),
    "tsp": ("ml", 5), "teaspoon": ("ml", 5), "teaspoons": ("ml", 5),
    "tbsp": ("ml", 15), "tablespoon": ("ml", 15), "tablespoons": ("ml", 15),
    "cup": ("ml", 250), "cups": ("ml", 250),

}

# Main Routine
while True:
    # Get the Amount Used
    amount_used, unit_used = get_amount_and_unit("Enter the Amount Used(with the Unit): ")
    # Loop to secure the Amount Bought and the converted Amount.
    while True:
        amount_bought, unit_bought = get_amount_and_unit("Enter the Amount Bought(with the Unit): ")
        if not unit_compatibility(unit_used, unit_bought):
            print("The Units are not compatible.")
            continue
        converted_amount = convert_amount(amount_bought, unit_bought, unit_used)

        print(f"The amount used is {amount_used} {unit_used}"
              f" and the amount bought is {converted_amount} {unit_used}. ")

        break


