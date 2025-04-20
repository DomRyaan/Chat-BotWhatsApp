from flask import Flask, request, jsonify

from services.waha import Waha

app = Flask(__name__)

@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    data = request.json
    
    waha = Waha()

    chat_id = data['payload']['from']
    
    print(f"Esse numero mandou mensagem: {chat_id}")

    if "@c" in chat_id:
        waha.send_message(
            chat_id=chat_id,
            message="Automatico",
        )

    return jsonify({'status': 'sucess'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)