import telegram_send as ts
import subprocess as sbp
import requests

TOKEN = ""
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

def send_it(text: str) -> None:
    """
    Main function.
    """
        

    print(f"\_ {requests.get(url).json()}")
    # Initial msg
    log = ts.send( messages=[text] )
    #ts.send( messages=[""] )
    # restarts dietpi-dashboard service
    '''
        dash_restart = sbp.Popen(["systemctl", "restart", "dietpi-dashboard"], stdout=sbp.PIPE)
        output = dash_restart.communicate()[0]
        message = "Reiniciei o dashboard do server. Tenta abrir outra vez mano"
        prompt = f"resultado do comando: {output}" 
        ts.send( messages=[message, prompt] )
    '''

