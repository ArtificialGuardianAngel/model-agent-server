import config
import together
from utils import mapHistoryToPrompt, updateHistory
from time import sleep

__all__ = ['handle_prompt']


def handle_prompt(history, user_input, new_token_callback, end_callback):
    response = ''
    is_first_run = True
    i = 0
    while config.END_OF_ANSWER not in response:
        try:
            prompt = mapHistoryToPrompt(history, user_input, response)

            tokens = together.Complete.create_streaming(
                prompt, config.MODEL_NAME, stop="<human>:")

            if (is_first_run):
                print(prompt, end='')
            for token in tokens:
                response += token
                if i % 2 == 0:
                    new_token_callback(updateHistory(
                        history, user_input, response), response)
                print(token, end='', flush=True)
                i += 1
            is_first_run = False
        except:
            sleep(0.1)
    print()
    print('{:=^50}'.format(f'Tokens used {i}'))

    end_callback(updateHistory(history, user_input, response))
