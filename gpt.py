import openai
import globals
import utilities
import re

def askGPT(system, user, assistant):
    openai.api_key = "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"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system}, {"role": "user", "content" : user}, {"role": "assistant", "content" : assistant}]
    )
    print(response['choices'][0]['message']['content'])
    return response['choices'][0]['message']['content']

def move():
    start, end = None, None
    fen = utilities.getBoard()
    response = '    '
    color = 'white' if globals.TURN % 2 == 0 else 'black'
    asistant = ''
    system = 'Answer by typing 4 characters without any spaces a2a4, where first two represent starting field of a chess figure to move, and other two the field its moved to. '
    user = f'You are playing {color} and its your turn in chess. The chessboard in FEN notation looks like this {fen}. Whats your move?'
    rx = r"[a-h][1-8][a-h][1-8]"
    matches = []
    while matches==[]:
        response = askGPT(system, user, asistant).lower()
        print(response)
        matches = re.findall(rx, response)
    for i, letter in enumerate('abcdefgh'):
        if matches[0][0] == letter:
            start = (8-int(matches[0][1]), i)
        if matches[0][2] == letter:
            end = (8-int(matches[0][3]), i)
    print(fen)
    print(matches[0])
    return [start, end]