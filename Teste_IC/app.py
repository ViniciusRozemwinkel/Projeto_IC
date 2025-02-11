from flask import Flask, render_template, request, jsonify
from Solver import alocar_pecas

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("Workstation.html")

@app.route('/alocar-pecas', methods=['POST'])
def alocar_pecas():
    data = request.json

    # Verifica se os dados foram recebidos corretamente
    if not data or 'forno' not in data or 'pecas' not in data:
        return jsonify({'success': False, 'message': 'Dados inválidos ou ausentes.'}), 400

    forno = data['forno']
    pecas = data['pecas']

    # Chama a função de alocação
    resultado = alocar_pecas(forno, pecas)

    # Retorna o resultado
    if isinstance(resultado, str) and resultado.startswith("Erro"):
        return jsonify({'success': False, 'message': resultado}), 400
    else:
        return jsonify({'success': True, 'pdf_url': resultado})

if __name__ == '__main__':
    app.run(debug=True)