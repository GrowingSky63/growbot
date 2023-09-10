from flask import Flask, render_template, jsonify, request
from commons import MAIN_PATH

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', auth_code_url='')

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        if 'email' in data and 'password' in data:
            email = data['email']
            password = data['password']

            return jsonify({"message": "Dados recebidos com sucesso!"}), 200
        else:
            return jsonify({"error": "Campos ausentes no corpo da solicitação"}), 400
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500


if __name__ == '__main__':
    app.run(debug=True)
