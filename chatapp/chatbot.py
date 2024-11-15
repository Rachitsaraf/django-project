# chatbot.py
def get_bot_response(user_input):
    # Define some basic responses
    responses = {
        "hi": "Hello! jay shri Ram how can i help you",
        "hello": "Hi there! What can I assist you with?",
        "how are you": "faltu baat mat kare kaam ki baat bata, but I'm doing great!",
        "bye": "Goodbye! Have a great day!"
    }

    # Convert user input to lowercase to standardize it
    user_input = user_input.lower()

    # Check if the input matches any predefined response
    for keyword in responses:
        if keyword in user_input:
            return responses[keyword]

    # Default response if no match found
    return "I'm sorry, I don't understand that."
