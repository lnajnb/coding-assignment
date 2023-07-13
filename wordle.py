def game_instruction():
    print("""Welcome to our Wordle! 👋
You have to guess a five letter hidden word! (๑•́o•̀๑)
You have six attempts to guess the word
✔️ - Indicates that the letter at that position was guessed correctly 
❔- Indicates that the letter at that position is in the hidden word, but in a different position
❌  - Indicates that the letter at that position is wrong, and isn't in the hidden word   """)


game_instruction()

def check_word():
  hidden_word = "jake"
  attempt = 6
  while attempt > 0:
    guess = str(input("Guess the word: "))
    if guess == hidden_word:
      print("You guessed the words correctly! CONGRATS 🏆🎉👏 ")
      break
    else:
      attempt = attempt - 1
      print(f"you have {attempt} attempt(s) ,, \n ")
      for char, word in zip(hidden_word, guess):
            if word in hidden_word and word in char:
                print(word + " ✔️ ")

            elif word in hidden_word:
                print(word + " ❔ ")
            else:
                print(word + " ❌ ")
      if attempt == 0:
        print(" Game over !!! 😥 ")

check_word() 
