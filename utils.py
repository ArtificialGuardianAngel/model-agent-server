import copy
from config import END_OF_ANSWER
from typing import List


def is_response_has_one_of_end_tag(endTags: List[str], response: str):
    for tag in endTags:
        if tag in response:
            return True
    return False


def get_end_tag_from_response(endTags: List[str], response: str):
    for tag in endTags:
        if tag in response:
            return tag
    return None


def get_index_of_one_of_end_tag(endTags: List[str], response: str):
    for tag in endTags:
        if tag in response:
            return response.index(tag)
    return -1


def clearResponseFromEndTags(response: str):
    if is_response_has_one_of_end_tag(END_OF_ANSWER, response):
        firstIndexOfEndTag = get_index_of_one_of_end_tag(
            END_OF_ANSWER, response)
        responseLastIndex = firstIndexOfEndTag + \
            len(get_end_tag_from_response(END_OF_ANSWER, response))
        return response[0:responseLastIndex]
    return response


def mapHistoryToPrompt(history, prompt, response=""):
    mapped_history = "<human>: Hello</human>\n<bot>: Hi, how can I assist today?</bot>\n"
    for conv in history['visible']:
        formatted_response = clearResponseFromEndTags(conv[1])
        mapped_history += f'<human>:{conv[0]}</human>\n<bot>:{formatted_response.strip()}\n'

    # {'</bot>' in response if '' else '</bot>'}
    return mapped_history + f"<human>:{prompt}</human>\n<bot>:{response.strip()}"


def updateHistory(oldHistory, prompt, answer):
    newHistory = copy.deepcopy(oldHistory)
    newHistory['internal'].append([prompt, answer])
    newHistory['visible'].append([prompt, answer])
    return newHistory
