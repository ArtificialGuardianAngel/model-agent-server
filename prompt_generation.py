import utils
from prompt import handle_prompt

def handle_new_token(new_history, response):
    # print(response)
    pass

def handle_end(history):
    print("{:=^50}END")
    print(history)

if __name__ == "__main__":
    old_history = {
        "internal": [
            ["Hello", "Hello! How can I assist you today?</bot>\n"],
        ],
        "visible": [
            ["Hello", " Hello! How can I assist you today?</bot>\n"],
        ]
    }
    user_input = "what is builder pattern in development?"

    prompt = utils.mapHistoryToPrompt(old_history, user_input)
    handle_prompt(old_history, user_input, handle_new_token, handle_end)