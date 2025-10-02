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
    print(make_statement("Instructions", "ℹ️"))

    print('''This program will ask you for...
    - The name of the recipe
    - The amount of servings you are going to prepare
    - The names of the ingredients
    - The amounts(with the unit) used for each ingredient
    - The amounts(with the unit) bought for each ingredient
    - The price of the amount bought

⚠️Note that all the units are metric units and are in measured in nz standards!

The program will output an list with all the things that the
user entered along with the cost to make for each ingredient.
The program will also calculate the total cost to make and the 
total cost to make per serving.

The program will then ask if you want to write the information to file
which basically means that it will print the output to a word document.

At the end, the program will ask if you want to return to the start of the program.


''')


# Main routine

Instructions = yes_no_check("Do you want to see the instructions(y/n): ")
if Instructions == "yes":
    instructions()
else:
    print("Program continues...")