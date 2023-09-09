import config
import together
from utils import mapHistoryToPrompt, updateHistory
from time import sleep
from notify import notify

__all__ = ['handle_prompt']


def handle_prompt(history, user_input, new_token_callback, end_callback):
    response = ''
    is_first_run = True
    i = 0
    retries = 0
    errors = []
    last_error = None
    while config.END_OF_ANSWER not in response:
        if retries > 10:
            response += '\nSomething went wrong, I apologize.</bot>'
            new_token_callback(updateHistory(
                history, user_input, response), response)
            notify({'last_error': last_error, 'errors': errors})
            break
        try:
            prompt = mapHistoryToPrompt(history, user_input, response)

            tokens = together.Complete.create_streaming(
                prompt, config.MODEL_NAME, stop="<human>:", max_tokens=512)

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
        except Exception as e:
            print('{:=^50}'.format(f'Exception'))
            print(e)
            print('{:=^50}'.format(f'End of exception'))
            errors.append(e)
            last_error = e
            sleep(1)
        finally:
            retries += 1
    print()
    print('{:=^50}'.format(f'Tokens used {i}'))

    end_callback(updateHistory(history, user_input, response))
