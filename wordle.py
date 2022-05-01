import random
import typing


GAMEWORD_LIST_FNAME = "sgb-words.txt"
GUESSWORD_LIST_FNAME = "sgb-words.txt"


def filter_word(word: str, length: int) -> str:
   
    if len(word.strip()) == length:
       
        return word.strip().upper()
    return None


def create_wordlist(fname: str, length: int) -> typing.List[str]:
    
    with open(fname, "r") as f:
        lines = f.readlines()
    return list(map(lambda word: filter_word(word, length), lines))


def validate(guess: str, wordlen: int,
             wordlist: typing.Set[str]) -> typing.Tuple[str, str]:
    
   
    guess_upper = guess.upper()
  
    if len(guess_upper) != wordlen:
        return f"Guess must be of length {wordlen}", guess_upper

  
    if guess_upper not in wordlist:
        return "Guess must be a valid word", guess_upper
    return None, guess_upper


def get_user_guess(wordlen: int, wordlist: typing.Set[str]) -> str:
    """Get a user guess input, validate, and return the guess."""
    
    while True:
        guess = input("Guess: ")
       
        error, guess = validate(guess=guess, wordlen=wordlen,
                                wordlist=wordlist)
        if error is None:
            break

        print(error)
    return guess


def find_all_char_positions(word: str, char: str) -> typing.List[int]:
    """Given a word and a character, find all the indices of that character."""
    positions = []
    pos = word.find(char)
    while pos != -1:
        positions.append(pos)
        pos = word.find(char, pos + 1)
    return positions 
def compare(expected: str, guess: str) -> typing.List[str]:
    """Compare the guess with the expected word and return the output parse."""
   
    output = ["_"] * len(expected)
    counted_pos = set()
    for index, (expected_char, guess_char) in enumerate(zip(expected, guess)):
        if expected_char == guess_char:
            # a correct character in the correct position
            output[index] = "*"
            counted_pos.add(index)

   
    for index, guess_char in enumerate(guess):
      
        if guess_char in expected and \
                output[index] != "*":
            positions = find_all_char_positions(word=expected, char=guess_char)
            for pos in positions:
                if pos not in counted_pos:
                    output[index] = "-"
                    counted_pos.add(pos)
                    break
    return output



if __name__ == '__main__':
   
    WORDLEN = 5
    GAMEWORD_WORDLIST = create_wordlist(
        GAMEWORD_LIST_FNAME, length=WORDLEN)
    GUESSWORD_WORDLIST = set(create_wordlist(
        GUESSWORD_LIST_FNAME, length=WORDLEN))
    WORD = random.choice(GAMEWORD_WORDLIST)
    GAME_WORD_LENGTH = len(WORD)
    NUM_GUESSES = 0
    print("""
Guess words one at a time to guess the game word.

A * character means a letter was guessed correctly
in the correct position.
A - character means a letter was guessed correctly,
but in the incorrect position.

To quit, press CTRL-C.
""")

    print("_ " * GAME_WORD_LENGTH)

   
    try:
        while True:
            
            GUESS = get_user_guess(
                wordlen=GAME_WORD_LENGTH, wordlist=GUESSWORD_WORDLIST)
            NUM_GUESSES += 1
            result = compare(expected=WORD, guess=GUESS)
            print(" ".join(result))

            if WORD == GUESS:
                print(f"You won! It took you {NUM_GUESSES} guesses.")
                break
    except KeyboardInterrupt:
        print(f"""
You quit - the correct answer was {WORD.upper()}
and you took {NUM_GUESSES} guesses
""")