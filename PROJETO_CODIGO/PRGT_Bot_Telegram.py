import requests
import time
import json
import os

class TelegramBot:
    def __init__(self):
        #token = '1870414063:AAFDHH64kyx9BP2GQSS4Q7TlrdC4GoxHfwE' 
        token = '1855933212:AAFnb53pSH-hGEXiYj4e_WKKK2OWDb7bDLU'
        self.url_base = f'https://api.telegram.org/bot{token}/'


    def Iniciar(self, resposta):
        chat_id = 862677162
        self.responder(resposta,chat_id)


    def responder(self,resposta,chat_id):
        link_de_envio = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_de_envio)


#bot = TelegramBot()
#bot.Iniciar()
