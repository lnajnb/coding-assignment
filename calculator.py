print('Welcome to the calculator program!!')
while True:
    ex = input('Please enter an expression or type cancel to exit the calculator: ')
    if ex.lower() == 'cancel':
        print('Turning off..')
        print('Calculator off')
        break
    try:
        res = eval(ex)
        print("Result:", res)
    except:
        print('Invalid input. Please try again.')

    restart = input('Do you want to perform another calculation? (yes/no): ')
    if restart.lower() != 'yes':
        break
print('Thank you for using the Calculator program!')

