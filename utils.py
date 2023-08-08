import copy


def mapHistoryToPrompt(history, prompt):
    mapped_history = ""
    for conv in history['visible']:
        mapped_history += f'<human>: {conv[0]}</human>\n<bot>: {conv[1]}</bot>\n'

    return mapped_history + f"<human>: {prompt}</human>\n<bot>:"


def updateHistory(oldHistory, prompt, answer):
    newHistory = copy.deepcopy(oldHistory)
    newHistory['internal'].append([prompt, answer])
    newHistory['visible'].append([prompt, answer])
    return newHistory
