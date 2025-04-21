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

    is_group = "@g.us" in chat_id
    is_status = "status@broadcast" in chat_id

   # Ignora mensagens de grupos ou atualizações de status
    if is_group or is_status:
        return jsonify({"status": "sucess", "mensagem": "Mensagem ignorada: grupo ou status"}), 200


    fuso_horario = timezone('America/Sao_Paulo')
    horario = datetime.now(fuso_horario).hour

    # Verifica se o estabelecimento está fechado
    if not (rules.is_open(horario)):

        waha.send_message(
        chat_id=chat_id,
        message="Desculpe, mas no momento estamos fechados. "
                "Nosso horário de funcionamento é das 6h às 11h (manhã) "
                "e das 14h às 18h (tarde).",
        )
        return jsonify({"status": "success", "message": "Estabelecimento fechado"}), 200
    
    waha.start_typing(chat_id=chat_id)

    time.sleep(3)
    
    response = ai_bot.invoke(question=received_message)
    waha.send_message(
        chat_id=chat_id,
        message=response,
        )

    waha.stop_typing(chat_id=chat_id)

    return jsonify({'status': 'sucess'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)