import random
def game_instruction():
    print("""Welcome to our Wordle! 👋
You have to guess a five letter hidden word! (๑•́o•̀๑)
You have six attempts to guess the word
✔️ - Indicates that the letter at that position was guessed correctly 
❔- Indicates that the letter at that position is in the hidden word, but in a different position
❌  - Indicates that the letter at that position is wrong, and isn't in the hidden word   """)


game_instruction()

def load_dict(file_name):
    file=open(file_name)
    words=file.readlines()
    file.close()
    return [word[:5].lower() for word in words]

def check_word():
    dict_ans = load_dict('ans.txt')
    answer = random.choice(dict_ans)
    attempt = 6
    while attempt > 0:
        guess = str(input("Guess the word: "))
        if guess == answer:
            print("You guessed the words correctly! CONGRATS 🏆🎉👏 ")
            break
        else:
            attempt = attempt - 1
            print(f"you have {attempt} attempt(s) ,, \n ")
            for character, word in zip(answer, guess):
                if word in answer and word in character:
                    print(word + " ✔️ ")
                elif word in answer:
                    print(word + " ❔ ")
                else:
                    print(word + " ❌ ")
        if attempt == 0:
            print(" Game over !!! 😥, The word was", answer)

check_word()
