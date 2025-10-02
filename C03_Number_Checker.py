# Function

def num_check(question, num_type = "float"):
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



# Main Routine(loop for testing)
while True:
    servings = num_check("Please Enter the Number of Servings: ", "integer")
    print(f"You chose {servings} Servings.")