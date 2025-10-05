import re

# Functions
def get_amount_and_units(question):
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

        units = match.group(2).lower() # Convert the unit to lowercase

        # Checks if the quantity is positive.
        if number <= 0:
            print("Please enter a number higher than 0.")
            continue

        # Checks if the unit is in the Units dictionary.
        if units not in units_dict:
            print("❌ Invalid unit! Valid units include"
                  " weight classes(kg, g) and volume classes(l, ml)")
            continue

        return number, units
    # Return None statement to avoid a light warning due to some IDE issues
    return None

def are_units_compatible(u1, u2):
    for group in unit_groups:
        if u1 in group and u2 in group:
            return True
    return False

def convert_amount(amount, from_unit, to_unit):
    if from_unit is None and to_unit is None:
        return amount
    if from_unit is None or to_unit is None:
        return None
    if from_unit == to_unit:
        return amount
    if (from_unit, to_unit) in conversions:
        return amount * conversions[(from_unit, to_unit)]

    print(f"❌ Cannot convert from {from_unit} to {to_unit}.")
    return None

# Initializing the Units
units_dict = {
    "grams":"g", "gram":"g", "g":"g",
    "kilograms":"kg", "kilogram":"kg", "kg":"kg",
    "millilitres":"ml", "millilitre":"ml", "ml":"ml",
    "litres":"l", "litre":"l", "l":"l"
}

conversions = {
    ("kg", "g"): 1000,
    ("g", "kg"): 1 / 1000,
    ("l", "ml"): 1000,
    ("ml", "l"): 1 / 1000
}

unit_groups = [
    {"g", "kg"},
    {"ml", "l"},
    {None, None}
]

# Main Routine
while True:
    amount_used, unit_used = get_amount_and_units("Enter the Amount Used(with the Unit): ")
    while True:
        amount_bought, unit_bought = get_amount_and_units("Enter the Amount Bought(with the Unit): ")
        if not are_units_compatible(unit_used, unit_bought):
            print("The Units are not compatible.")
            continue

        while True:
            converted_amount = convert_amount(amount_bought, unit_bought, unit_used)

            print(f"The amount used is {amount_used} {units_dict[unit_used]} and the amount bought is {converted_amount} {units_dict[unit_used]}. ")
            break
