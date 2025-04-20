import requests
import os


class Waha:

    def __init__(self):
        self.__api_url = "http://waha:3000"

    def send_message(self, chat_id: str, message: str) -> dict:
        """ Envia uma mensagem para um chat via API."""
        url = f"{self.__api_url}/api/sendText"
        headers = {
            'Content-Type': "application/json",
        }
        payload = {
            'session': 'default',
            'chatId': chat_id,
            'text': message,
        }
        try:
           response = requests.post(
                            url=url,
                            json=payload,
                            headers=headers
                        )
           response.raise_for_status()
           
           return response.json()
        except requests.exceptions.RequestException as ex:
            return {"error": str(ex)}


    def start_typing(self, chat_id: str) -> dict:
        """Envia um estado de 'digitando' ao Chat"""
        url = f"{self.__api_url}/api/startTyping"
        
        headers = {
            'Content-Type': 'application/json',
        }
        payload = {
            'session': 'default',
            'chatId': chat_id,
        } 

        try:
            response = requests.post(
                url=url,
                json=payload,
                headers=headers,
            )
            
            response.raise_for_status()

            return response.json()
        
        except requests.RequestException as ex:
            return {"error": str(ex)}

    def stop_typing(self, chat_id: str) -> dict:
        """Para de atualizar o estado 'digitando' ao chat"""
        url = f"{self.__api_url}/api/stopTyping"
        headers = {
            'Content-Type': 'application/json',
        }
        payload = {
            'session': 'default',
            'chatId': chat_id,
        }

        try:
            response = requests.post(
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()

            return response.json()
        except requests.RequestException as ex:
            return {"error": str(ex)}