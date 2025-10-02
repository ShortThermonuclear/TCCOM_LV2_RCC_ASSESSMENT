# Function

def make_statement(statement, decoration):
    """Emphasises headings by adding decoration
    at the start and end"""

    return f"{decoration * 3} {statement} {decoration * 3}\n"

# Main Routine

heading = make_statement("Recipe Cost Calculator", "🥝")
print(heading)