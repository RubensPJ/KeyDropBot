import keydrop_twitter_bot as kdrop
from time import sleep

HORAS = 3600

def main():
    code_not_captured = True
    
    while code_not_captured:
        code_not_captured = kdrop.get_keydrop_code()
        print(f"\_ Is it closed: {code_not_captured}")
        # sleep(8*HORAS)
        if not code_not_captured:
            sleep(3)
            code_not_captured = True
        else:
            print("\_ Waiting 60 seconds...")
            sleep(60)
            
main()