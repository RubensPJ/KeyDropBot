## Fix >1 screens ##
from PIL import ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

## Text from image reader ##
import pytesseract

## Basic imports  ##
import pyautogui as auto
import pyperclip as clip
from time import sleep
import re

## POP UP 
import popUp as pop

## selenium ##
from loadbar import loadbar

auto.PAUSE = 1
w = pop.WindowsBalloonTip()

'''
1. open site
2. click first giveaway
3. click second giveaway (daily)t
4. click freecase (in case its possible to retrieve)

'''

## Links ##
keydrop_site = "https://key-drop.com/"
first_give_btn = "./imgs/6h_sorteio_btn.PNG"
second_give_btn = "./imgs/day_sorteio_btn.PNG"
free_case_btn = "./imgs/daily_case_btn.PNG"
join_now_btn = "./imgs/join_now_btn.PNG"
open_case_btn = "./imgs/open_case_btn.PNG"
robot_capt_btn = "./imgs/robot_capt_btn.PNG"
erro_case_opend_check = "./imgs/erro_case_opend_check.PNG"
exit_modal = "./imgs/exit_modal_window.PNG"
sorteio_box_6h = "./imgs/sorteio_6h.PNG"


def data_collector():
    ''' 
        Colect the data from keydrop.com and send it via whatsapp
        Funds = saldo_punkty --> <span class="text-sm font-semibold leading-none uppercase text-gold saldo_punkty" data-value="0.78"> $0.78 </span>
        Golden Coins = mt-px saldo_gold --> <span class="mt-px saldo_gold">445</span>

    '''
    pass

def capture_text(img):
    '''
        Reads an image and captures its content into a text.

        img >>> str 
    '''
    pytesseract.pytesseract.tesseract_cmd = "./Tesseract/tesseract"
    
    text = pytesseract.image_to_string(img, config='--psm 1')
    print(f"Texto capturado:\n{text}\n")
    pattern = re.compile(r'\d{2}|\d')

    mat = pattern.finditer(text.replace("Ih", "1"))
    
    # mat_len = sum(1 for _ in mat)
    numbers = []
    
    for i in mat:
            numbers.append(int(i.group()))
            
    print(numbers)

    
    print(f"Texto filtrado:\n{numbers}\n")
    return numbers


def search_and_click(img, waiting_time=10):
    '''
        Receive an image string or a list off of it and
        tries to localize them in the screen a sort amount of times determined 
        by waiting_time, if it is mentioned.

        img_path >>> str(x, y)
    '''

    if isinstance(img, (str)):
        position = auto.locateCenterOnScreen(img)
        
        i = 0
        if position == None:
            print("Imagem não encontrada...")
            while position == None and i < waiting_time:
                
                i += 1
        auto.click(position)
        return position
        
    elif isinstance(img, (list)):
        ## Loading bar ##
        l = len(img)
        # loadbar(0, l, prefix=f'Searching image again: {img}', suffix='Complete', length=l)

        for i, item in enumerate(img):
            print(f"Tentando localizar {item} ", end=" | \r")
            position = auto.locateCenterOnScreen(item, confidence=0.9)
            
            loadbar(i + 1, l, prefix=f'Checking img: {item}', suffix='Complete', length=100)

            i = 0
            if position != None:
                print(f"Imagem encontrada {item} ", end=" | ")
                auto.click(position)
                sleep(2)

            # loadbar(i + 1, l, prefix=f'Checking img: {item}', suffix='Complete', length=l)
            

def check_msg(img):
    pass
    # position = auto.loca

def abrir_site(link, new_tab=False):
    '''
        Receives a http link as a string value to be browsed
        and sends it to the browser

        img >>> str 
    '''
    if new_tab:
        auto.hotkey("ctrl","t")
        
    # abrir aba nova e clicando no campo correto
    clip.copy(link)
    auto.hotkey("ctrl","v")
    auto.press("enter")
    sleep(0.5)
    
def exec_soft(software: str):
    '''
        Reads an image and captures its text content,
        converting it and returning it as a string value 

        str( software ) >>> new_program 
    '''
    
    # Abrindo navegador
    auto.hotkey("winleft","r")

    auto.write(software)
    auto.press("enter")

def page_changer(link: str):
    '''
        Receives a link as a string value and Load a new site, 
        sending it to the browser

        str( link ) >>> new_page/new_site 
    '''
    clip.copy(link)
    auto.hotkey("ctrl","l")
    auto.hotkey("ctrl","v")
    auto.press("enter")

def scheduler():
    '''
        Takes a printscreen of the rectangle of the next 6h giveaway 
        and calls the sleep() method to stops the script execution waiting for the next loop 

        printed_image >>> time_data_captured >> sleep( time_data_captured )
    '''
    import datetime

    
    
    tried_getting_data = False

    page_changer(keydrop_site)
    sleep(2)
    
    # Getting image from 6h giveaway
    img = auto.screenshot( region=( 495, 378, ( 676-481 ), ( 447-378 ) ) )
    img.save( sorteio_box_6h )
    time_in_str = capture_text( sorteio_box_6h )
    
    try:
        if len(time_in_str) > 2:
            horas = time_in_str[0] * 3600
            minutos = time_in_str[1] * 60
            segundos = time_in_str[2]
            next_exec = horas + minutos + segundos
        elif len(time_in_str) == 2:
            minutos = time_in_str[0] * 60
            seconds = time_in_str[1]
            next_exec = minutos + seconds
        else:
            next_exec = time_in_str[0] if len( time_in_str ) >= 1 else 1

    except IndexError as ie:
        if not tried_getting_data:
            instance_notification = w.ShowWindow("KEYDROP BOT -- Ops! {tried_getting_data}", "Erro tentando ler a data do sorteio! Vou ler novamente")
            sleep(2)
            ''' 
                ** ADD Later Log:
                    Find an image from the home page to see if it is loaded
                    alt+tab if it finds and if not, opens a new window. 
                
            '''
            tried_getting_data = True
            scheduler()
        else:
            main()


    timestamp = str(datetime.timedelta(seconds=next_exec))
    print(f"Sleeping for {timestamp}  ...")
    # log_time = 
    w.ShowWindow("Timing Out", f"Log time: {datetime.date.today()}\nDormindo por {timestamp}")
    # alert(text=f"Sleeping for {timestamp} ! \n{datetime.date.today()}", title='Timing Out', button='OK')
    
    timeline_lenght = int(next_exec / 100) if next_exec >= 100 else int(next_exec / 10)

    # loadbar(0,
    # next_exec,
    # prefix=f'Countdown for the next exec: { str( datetime.timedelta( seconds=next_exec ) ) }  ', 
    # suffix='Complete', length=next_exec)

    for seg in range(next_exec, 0, -1):
        sleep(1)
        loadbar( seg - 1,
         next_exec,
          prefix=f'Countdown for the next exec: { str( datetime.timedelta( seconds=next_exec-1 ) ) }',
           suffix='Complete',
            length=100)

    # sleep( next_exec )
    main()

def main():
    '''
        Main execution, sequentionally calling the steps 
        needed to fufill the script execution
    '''
    exec_soft( "chrome" )
    abrir_site( keydrop_site )
    sleep( 2 )

    ## Relative prositions:
    ## x=349, y=336
    ## x=676, y=335
    ## x=350, y=447
    ## x=680, y=444


    search_and_click(
        [
            first_give_btn, 
            join_now_btn, 
            exit_modal,
            second_give_btn,
            join_now_btn,
            exit_modal,
            free_case_btn,
            open_case_btn,
            robot_capt_btn
        ]
    )
    
    erro_box = search_and_click(erro_case_opend_check)
    sleep(2)
    print(erro_box)
    if erro_box != None:
        erro = auto.screenshot(region=(1405, 720, 500, 300))
        print("Caixa já aberta", erro)
    
    scheduler() 


if __name__ == '__main__':
    main()