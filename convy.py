from random import choice

# Categorized responses
acknowledgments = [
    "Cool, I'm on it sir.",
    "Okay sir, I'm working on it.",
    "Just a second sir.",
    "Right away sir.",
    "I'll handle that for you."
]

confirmations = [
    "All set, sir.",
    "Done, sir.",
    "Completed that task for you.",
    "Finished, anything else you need?",
    "Task accomplished, sir."
]

errors = [
    "Sorry, I couldn't understand. Can you please repeat that?",
    "I'm not sure I follow, could you clarify?",
    "I didn't catch that, could you say it again?",
    "Apologies, I'm having trouble understanding.",
    "Can you try rephrasing that for me?"
]

# Function to get a random response based on category
def get_random_response(category):
    if category == 'acknowledgment':
        return choice(acknowledgments)
    elif category == 'confirmation':
        return choice(confirmations)
    elif category == 'error':
        return choice(errors)
    else:
        return "I'm not sure how to respond to that."
