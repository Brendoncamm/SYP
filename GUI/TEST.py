import callscript
import time
def ask_to_call():
    quest = str(input("Would you like to use the calculator? " ))
    if quest == 'yes':
        num1 = int(input("What number: "))
        num2 = int(input("what number: "))
        print('Thank you, answer will be displayed for 1 minute')
        callscript.addition(num1,num2)
        time.sleep(60) 
    else:
        print("well you're garb")

if __name__ == '__main__':
    ask_to_call()

