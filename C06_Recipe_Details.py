# Function

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
        error = "Please enter a number which is also more than 0."
    else:
        error = "Please enter an integer more than 0."

    # Check datatype is correct and that number
    # is more than zero
    while True:
        try:
            response = input(question)

            # checks if the response starts with a $
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

# Main routine

while True:
    Recipe_Name = not_blank("Recipe Name: ")
    Servings = num_check("Servings: ")

    print(f"You are making {Recipe_Name} with {Servings} servings.")