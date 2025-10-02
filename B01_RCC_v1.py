import re
import pandas
from tabulate import tabulate

# Functions

def make_statement(statement, decoration):
    """Emphasises headings by adding decoration
    at the start and end"""

    return f"{decoration * 3} {statement} {decoration * 3}\n"

def not_blank(question):
    """Checks user response is not blank"""
    while True:
        response = input(question)

        if response != "":
            return response
        else:
            print("Sorry, this can't be blank.")


def num_check(question, num_type="float", question_type="price"):
    """Checks if the input is an integer or not"""
    # Changes error message depending on the number type.
    if num_type == "float":
        error = "Please enter a number more than 0."
    else:
        error = "Please enter an integer more than 0."

    # Check datatype is correct and that number
    # is more than zero
    while True:
        try:
            response = input(question)

            # checks if the response starts with a dollar sign $
            if question_type == "price":
                response = response.lstrip("$")

            if num_type == "float":
                response = float(response)
            else:
                response = int(response)

            if response > 0:
                return response
            else:
                print(error)

        except ValueError:
            print(error)
            # prints an error message if the user does not enter an integer.


def get_amount_and_unit(question):
    """Gets the Amount and the Unit at once and returns them to the program."""

    while True:
        response = input(question).strip()  # Removes any leading and trailing whitespaces.

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
            print("❌ Please enter a valid input! (e.g. 100kg, 20 millilitres or just 4.)")
            continue

        number = float(match.group(1))  # Convert the quantity to float

        units = match.group(2).lower()  # Convert the unit to lowercase

        # Checks if the quantity is positive.
        if number <= 0:
            print("Please enter a number higher than 0.")
            continue

        # Checks if the unit is in the Units dictionary.
        if units not in Units:
            print("❌ Invalid unit! Valid units include"
                  " weight classes(kg, g) and volume classes(l, ml, tsp, tbsp, cups)")
            continue

        return number, units
    # Return None statement to avoid a light warning due to some IDE issues
    return None

def are_units_compatible(u1, u2):
    """Checks if units are compatible"""

    # Returns true if both the units have the same base unit.
    return Units[u1][0] == Units[u2][0]

def convert_amount(quantity, u1, u2):
    """Convert amount between compatible units"""
    # Checks if there are no units or both the amounts have the same unit
    if u1 is None or u2 is None or u1 == u2:
        return quantity

    # Takes the factor of both the units.
    factor_1 = Units[u1][1]
    factor_2 = Units[u2][1]

    # Calculates the converted quantity.
    converted_quantity = quantity * factor_1 / factor_2

    return converted_quantity

# Initializing the Units
Units = {
    # No unit
    None: ("none", 1),

    # Mass
    "g": ("g", 1), "gram": ("g", 1), "grams": ("g", 1),
    "kg": ("g", 1000), "kilogram": ("g", 1000), "kilograms": ("g", 1000),

    # Volume
    "ml": ("ml", 1), "milliliter": ("ml", 1), "milliliters": ("ml", 1),
    "l": ("ml", 1000), "liter": ("ml", 1000), "liters": ("ml", 1000),
    "tsp": ("volume", 5), "teaspoon": ("volume", 5), "teaspoons": ("volume", 5),
    "tbsp": ("volume", 15), "tablespoon": ("volume", 15), "tablespoons": ("volume", 15),
    "cup": ("volume", 240), "cups": ("volume", 240),

}

# Main Routine
# List for Pandas
all_names = []
all_amounts = []
all_amounts_bought = []
all_prices = []
all_costs = []

# Recipe Dictionary
recipe_dict = {
    'Ingredient Name': all_names,
    'Amount Used': all_amounts,
    'Amount Bought': all_amounts_bought,
    'Price Paid': all_prices,
    'Cost to Make': all_costs
}

# Get Ingredient Details
while True:
    print()
    # Get name and check it is not blank.
    name = not_blank("Ingredient Name (or 'xxx' to finish): ")

    # check users enter at least one ingredient
    if name.lower() == "xxx" and len(all_names) == 0:
        print("You must enter at least one ingredient!")
        continue
    # if there is more than 1 ingredient and the user enters xxx, the loop will break.
    elif name.lower() == "xxx":
        break
    all_names.append(name)

    # Amount used
    amount, unit = get_amount_and_unit("Amount Used: ")

    # Amount bought
    converted_amt = None
    while True:
        bought_amt, bought_unit = get_amount_and_unit("Amount bought: ")
        if not are_units_compatible(unit, bought_unit):
            print(f"❌ The Units are not compatible"
                  f", please use units with the base unit [{Units[unit][0]}]")
            continue
        converted_amt = convert_amount(bought_amt, bought_unit, unit)
        if converted_amt < amount:
            print("The Amount bought can not be less than the Amount Used!")
            continue
        break

    # Price
    price = num_check("Price: ")

    # Calculate cost to make
    cost_to_make = price * (amount / converted_amt)

    # Store data
    all_amounts.append(f"{amount}{unit or ''}")
    all_amounts_bought.append(f"{bought_amt}{bought_unit or ''}")
    all_prices.append(price)
    all_costs.append(round(cost_to_make, 2))

# make panda
recipe_frame = pandas.DataFrame(recipe_dict)

# 🔹 Display Table 🔹
print("\n" + make_statement("Recipe Cost Table", "📜"))
print(tabulate(recipe_frame, headers='keys', tablefmt='fancy_grid', showindex=False))



