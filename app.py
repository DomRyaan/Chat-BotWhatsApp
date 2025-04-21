from flask import Flask, request, jsonify

import time
from datetime import datetime
from pytz import timezone


from bot.ai_bot import AIBot
from services.waha import Waha
from controls import BusinessRules

app = Flask(__name__)

@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    data = request.json
    
    waha = Waha()
    ai_bot = AIBot()
    rules = BusinessRules()

    chat_id = data['payload']['from']
    received_message = data['payload']['body']

    fuso_horario = timezone('America/Sao_Paulo')
    horario = datetime.now(fuso_horario).hour

    """Verificando se a mensagem que recebemos não vem de um grupo"""
    if chat_id.endswith("@c.us"):
        
        if rules.is_open(horario):
            waha.start_typing(chat_id=chat_id)

            time.sleep(3)
            
            response = ai_bot.invoke(question=received_message)
            waha.send_message(
                chat_id=chat_id,
                message=response,
                )

            waha.stop_typing(chat_id=chat_id)
        else:
             waha.send_message(
                chat_id=chat_id,
                message="Desculpe, mas no momento estamos fechados. Nosso horário de funcionamento é das 6h às 11h e das 14h às 18h.",
            )

    return jsonify({'status': 'sucess'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)