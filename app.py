from flask import Flask, request, jsonify
import time
from services.waha import Waha

app = Flask(__name__)

@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    data = request.json
    
    waha = Waha()

    chat_id = data['payload']['from']
    mensagem = data['payload']['body']
    checagem: bool = chat_id.endswith("@c.us")

    print(f"Mensagem: {mensagem} evianda por esse número: {chat_id}")

    """Verificando se a mensagem que recebemos não vem de um grupo"""
    if checagem:
        waha.start_typing(chat_id=chat_id)

        time.sleep(4)

        waha.send_message(
            chat_id=chat_id,
            message="""Olá! 😊 Seja bem-vindo(a) a GiSalgados. 
Se precisar de ajuda, tiver dúvidas ou quiser conhecer mais sobre nossos serviços, é só nos chamar.""",
        )

        waha.stop_typing(chat_id=chat_id)

    return jsonify({'status': 'sucess'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)