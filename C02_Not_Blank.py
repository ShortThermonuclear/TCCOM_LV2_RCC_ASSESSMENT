# Function

def not_blank(question):
    """Checks user response is not blank"""
    while True:
        response = input(question)

        if response != "":
            return response
        else:
            print("Sorry, this can't be blank.")


# Main Routine (loop for testing)
while True:
    name = not_blank("Enter the Recipe Name: ")
    print(f"You are making {name}.")