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
        if units not in Units:
            print("❌ Invalid unit! Valid units include"
                  " weight classes(kg, g) and volume classes(l, ml)")
            continue

        return number, units
    # Return None statement to avoid a light warning due to some IDE issues
    return None

# Initializing the Units

Units = {
    "grams":"g", "gram":"g", "g":"g",
    "kilograms":"kg", "kilogram":"kg", "kg":"kg",
    "millilitres":"ml", "millilitre":"ml", "ml":"ml",
    "litres":"l", "litre":"l", "l":"l"
}

# Main Routine
while True:

    amounts = get_amount_and_units("Please Enter the Amount(with the unit): ")