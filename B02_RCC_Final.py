import re
import pandas
import os
from tabulate import tabulate
from datetime import date

# Functions


def make_statement(statement, decoration):
    """Emphasises headings by adding decoration
    at the start and end"""

    return f"{decoration * 3} {statement} {decoration * 3}\n"


def yes_no_check(question):
    """Checks that users enter yes / no / y / n"""

    while True:

        response = input(question).lower()

        if response == "y" or response == "yes":
            return "yes"
        elif response == "n" or response == "no":
            return "no"

        print(f"Please answer yes / no (y / n)")


def instructions():
    """Displays instructions"""

    print(make_statement("Instructions", "ℹ️")) # Instruction heading for aesthetics.

    print('''This program will ask you for...
    - The name of the recipe
    - The amount of servings you are going to prepare
    - The names of the ingredients
    - The amounts used for each ingredient
    - The amounts bought for each ingredient
    - The price of the amount bought

⚠️ You are also supposed to enter the Amount with the Unit! (no units are also possible.)
Note that all the units are metric units and are in measured in nz standards!

The Available Units are 
Mass Units - grams, kilograms
Volume Units - milliliters, liters, teaspoons(5ml), cups(250ml), tablespoons(15ml)

The program will output an list with all the things that the
user entered along with the cost to make for each ingredient.
The program will also calculate the total cost to make and the 
total cost to make per serving.

The program will then ask if you want to write the information to file
which basically means that it will print the output to note document.

At the end, the program will ask if you want to return to the start of the program.


''')


def not_blank(question):
    """Checks user response is not blank"""

    while True:
        response = input(question).strip()

        if response != "":
            return response
        else:
            print("❌ Sorry, this can't be blank.")


def num_check(question, num_type="float", question_type="price"):
    """Checks if the input is an integer or not"""

    # Changes error message depending on the number type.
    if num_type == "float":
        error = "❌ Please enter a number more than 0."
    else:
        error = "❌ Please enter an integer more than 0."

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

        # Checks for simple integer with no Unit (e.g. 4 (eggs) or 10 (grapes))
        if response.isdigit():

            # Checks if the integer is equal to 0
            if int(response) == 0:
                print("❌ Please enter an integer greater than 0.")
                continue

            # return the Integer and the unit as None to the program.
            return int(response), None

        # Checks for Quantity with unit (e.g. 100g, 25.5 millilitres or 3 tablespoons)
        # Uses Regex to separate the number and the unit.
        match = re.fullmatch(r"([0-9]*\.?[0-9]+)\s*([a-zA-Z]+)", response)

        # Checks if the input matches the pattern
        if not match:
            print("❌ Please enter a valid input! (e.g. 100kg, 20 millilitres or just 4.)")
            continue

        number = float(match.group(1))  # Convert the quantity to float

        unit = match.group(2).lower()  # Convert the unit to lowercase

        # Checks if the quantity is positive.
        if number <= 0:
            print("❌ Please enter a number higher than 0.")
            continue

        # Checks if the unit is in the Units dictionary (means that if it is a valid unit).
        if unit not in units_dict:
            print("❌ Invalid unit! Valid units include"
                  " weight classes(kg, g) and volume classes(l, ml, tsp, tbsp, cups)")
            continue

        # return the number and the unit.
        return number, unit
    # Return None statement to avoid a light warning due to some IDE issues
    return None


def are_units_compatible(u1, u2):
    """Checks if units are compatible"""

    # Checks if both the units have the same base unit
    # returns boolean value True if they do.
    return units_dict[u1][0] == units_dict[u2][0]


def convert_amount(quantity, u1, u2):
    """Converts amount between compatible units"""

    # Takes the factor of both the units.
    factor_1 = units_dict[u1][1]
    factor_2 = units_dict[u2][1]

    # Convert bought amount into the same unit as used amount
    # It calculates this by multiplying the bought quantity
    # with factor 1 to see how much that quantity is in base units
    # then it is divided by the factor 2 to get the converted amount
    converted_quantity = quantity * factor_1 / factor_2

    # Returns the converted amount
    return converted_quantity


def currency(x):
    """Formats numbers as currency ($#.##)"""
    return "${:.2f}".format(x)


def valid_filename(filename):
    """Checks if filename has illegal characters and is not too long"""

    # Replaces the spaces in the filename to underscores
    filename = filename.replace(" ", "_") + "_RRC"

    # Checks if the filename is too long
    if len(filename) >= 35:
        # If filename is too long filename will be defaulted to standard format.
        filename = f"Recipe_Cost_Calculator_{day}_{month}_{year}"

    # Iterates over the filename for individual characters
    for letter in filename:
        # Checks if the filename contains any illegal characters.
        if letter.isalnum() is False and letter != "_":
            # If filename contains special characters defaults to standard format.
            filename = f"Recipe_Cost_Calculator_{day}_{month}_{year}"
        else:
            return filename

    # returns the original filename if it is valid.
    return filename


# Main Routine

# Initializing the Units

units_dict = {
    # No unit
    None: ("none", 1),

    # Mass
    "g": ("g", 1), "gram": ("g", 1), "grams": ("g", 1),
    "kg": ("g", 1000), "kilogram": ("g", 1000), "kilograms": ("g", 1000),

    # Volume
    "ml": ("ml", 1), "millilitre": ("ml", 1), "millilitres": ("ml", 1),
    "l": ("ml", 1000), "litre": ("ml", 1000), "litres": ("ml", 1000),
    "tsp": ("ml", 5), "teaspoon": ("ml", 5), "teaspoons": ("ml", 5),
    "tbsp": ("ml", 15), "tablespoon": ("ml", 15), "tablespoons": ("ml", 15),
    "cup": ("ml", 250), "cups": ("ml", 250),
}


# Program heading
print(make_statement("Recipe Cost Calculator", "🥝"))

print()
if yes_no_check("Do you want to see the instructions? ") == "yes":
    instructions()
print()

# loop to allow to the user to use the program multiple times in one run.
while True:

    # Recipe Details heading
    print(make_statement("Recipe Details", "==="))

    # Get Recipe Details
    recipe_name = not_blank("Recipe Name: ")
    servings = num_check("Servings: ", "integer")
    print()

    # List for Pandas
    all_names = []
    all_amounts = []
    all_amounts_bought = []
    all_prices = []
    all_costs = []
    all_costs_raw = []

    # Recipe Dictionary for pandas.
    recipe_dict = {
        'Ingredient Name': all_names,
        'Amount Used': all_amounts,
        'Amount Bought': all_amounts_bought,
        'Price Paid': all_prices,
        'Cost to Make': all_costs
    }

    # Ingredient Details Heading
    print(make_statement("Ingredient Details", "---"))

    # Loop to get Ingredient Details.
    while True:
        # Get name and check it is not blank.
        name = not_blank("Ingredient Name (or 'xxx' to finish): ")

        # check if the user enters at least one ingredient
        if name.lower() == "xxx" and len(all_names) == 0:
            print("❌ You must enter at least one ingredient!")
            continue

        # checks if the user wants to end the loop
        elif name.lower() == "xxx":
            break

        # store the names.
        all_names.append(name)

        # asks for the Amount used
        amount_used, unit_used = get_amount_and_unit("Amount Used: ")

        # asks for the Amount bought
        converted_amt = None # defining converted amount outside the loop.

        while True:
            amount_bought, unit_bought = get_amount_and_unit("Amount Bought: ")

            # Checks if the units
            # of both amounts are compatible with each other
            if not are_units_compatible(unit_used, unit_bought):
                print(f"❌ The Units are not compatible"
                      f", please use units with the base unit [ {units_dict[unit_used][0]} ]")
                continue

            # converts the amount bought according to the unit of the amount used.
            # so that the cost to make can be calculated correctly.
            converted_amt = convert_amount(amount_bought, unit_bought, unit_used)

            # checks if the bought amount is less than the amount used
            if converted_amt < amount_used:
                print("❌ The Amount bought can not be less than the Amount Used!")
                continue
            break

        # Asks for the price
        price = num_check("Price Paid: ")
        print()

        # Calculate cost to make
        cost_to_make = price * (amount_used / converted_amt)

        # Store data
        all_amounts.append(f"{amount_used}{unit_used or ''}") # if the Unit is None, it will be stored as blank
        all_amounts_bought.append(f"{amount_bought}{unit_bought or ''}")
        all_prices.append(currency(price))
        all_costs.append(currency(cost_to_make))
        all_costs_raw.append(cost_to_make)

    # Convert recipe data into a DataFrame for neat table formatting
    recipe_frame = pandas.DataFrame(recipe_dict)

    # Display table and recipe details
    print()
    print(make_statement("Recipe Cost Table", "📜"))
    print(f"Recipe Name: {recipe_name}")
    print(f"Servings: {servings} \n")
    print(tabulate(recipe_frame, headers='keys', tablefmt='fancy_grid', showindex=False))


    # Calculate and output total cost to make and the cost per serve.
    total_cost = sum(all_costs_raw)
    total_cost_per_serving = total_cost / servings
    print()
    print(f"💰 Total Cost to Make: {currency(total_cost)}")
    print(f"💰 Per Serve: {currency(total_cost_per_serving)} \n")
    print()

    # Asks if the user wants to record this information to file.
    want_file = yes_no_check("Do you want to record this information in a file (y/n)?: ")
    if want_file == "yes":

        # strings / output area

        # Get current date for file name and heading
        today = date.today()

        # Get day, month and year as individual strings
        day = today.strftime("%d")
        month = today.strftime("%m")
        year = today.strftime("%Y")

        # Headings / Strings
        main_heading_string = make_statement(f"Recipe Cost Calculator"
                                             f"({recipe_name}, {day}/{month}/{year})", "=")

        name_string = f"Recipe Name: {recipe_name}"

        servings_string = f"Amount of Servings: {servings}"

        ingredient_heading_string = make_statement(f"Ingredient Details", "-")

        # Use 'psql' format for file output since 'fancy_grid' uses emojis that break in plain text
        recipe_table_string = tabulate(recipe_frame, headers='keys', tablefmt='psql', showindex=False)

        total_cost_string = f"Total Cost to Make: {currency(total_cost)}"

        per_serve_string = f"Cost Per Serve: {currency(total_cost_per_serving)}"

        ending_string = "!Thank You for Trying out the Recipe Cost Calculator!"


        # List of strings to be outputted / written to file
        to_write = [
            main_heading_string, name_string,
            servings_string, "\n", ingredient_heading_string,
             recipe_table_string, "\n", total_cost_string,
            per_serve_string, "\n", ending_string, "\n",
        ]

        # checks if the recipe name has no illegal characters or is not too long
        # if the recipe name is valid, it will be chosen as the filename.
        safe_filename = valid_filename(recipe_name)

        # Writes to file
        write_to = "{}.txt".format(safe_filename)
        text_file = open(write_to, "w+", encoding = "utf-8" )

        # write the item to file
        for item in to_write:
            text_file.write(item)
            text_file.write("\n")
            text_file.flush() # Allow multiple files to be written in one run.
            os.fsync(text_file.fileno()) # Makes sure the file is saved to disk.

        # Confirmation of file save along with the chosen filename.
        print(f"The Filename is {safe_filename} and has been saved.")


    # Thank you note :)
    print("\n !Thank you for trying out the Recipe Cost Calculator! \n")

    # Asks the user if they want to restart.
    return_to_start = not_blank("Enter R to return to the start of the program "
                            "(enter any other letter to close): ").strip()

    # checks if the user enters r, if they do , restarts.
    if return_to_start.lower() == "r":
        print()
        # return to the start of the program.
        # allows multiple recipes to be calculated in one run.
        continue

    else:
        break   #  Ends the Program.
