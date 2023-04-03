# Importa a classe Flask do módulo flask, que é usada para criar um objeto que representa a aplicação web.
from flask import Flask, jsonify, request

# Importa o módulo sqlite3, que é uma biblioteca que fornece uma API para trabalhar com o banco de dados SQLite.
import sqlite3

# Cria uma conexão com o banco de dados
conn = sqlite3.connect('agenda.db')

# Cria a tabela de contatos
conn.execute('''
CREATE TABLE IF NOT EXISTS contatos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    email TEXT NOT NULL,
    cliente_id INTEGER NOT NULL
)
''')

# Fecha a conexão
conn.close()

# Cria uma instância da classe Flask e atribui a variável app. __name__ é uma variável especial que define o nome do módulo. 
# Quando este módulo é executado, __name__ será definido como __main__. 
# Isso é necessário para que o Flask saiba onde encontrar os arquivos da aplicação, como modelos e arquivos estáticos.
app = Flask(__name__)


# Define uma rota da API para a listagem de contatos.
@app.route('/contatos')
def listar_contatos():

    cliente_id = request.args.get('cliente_id')
    letra = request.args.get('letra')
    nome = request.args.get('nome')

    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    
    if letra:
        cursor.execute('SELECT * FROM contatos WHERE nome LIKE ? AND cliente_id = ?', (letra + '%', cliente_id))
    elif nome:
        cursor.execute('SELECT * FROM contatos WHERE nome = ? AND cliente_id = ?', (nome, cliente_id))
    else:
        cursor.execute('SELECT * FROM contatos WHERE cliente_id = ?', (cliente_id,))
    contatos = []
    for linha in cursor.fetchall():
        contato = {
            'id': linha[0],
            'nome': linha[1],
            'telefone': linha[2],
            'email': linha[3]
        }
        contatos.append(contato)
    conn.close()
    return jsonify(contatos)

#define uma rota na aplicação, /contatos, que pode ser acessada via método HTTP POST.
@app.route('/contatos', methods=['POST'])
def criar_contato():

    #extrai o objeto JSON enviado com a requisição HTTP e armazena em uma variável chamada dados
    dados = request.json
    
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO contatos (nome, telefone, email, cliente_id) VALUES (?, ?, ?, ?)',
                   (dados['nome'], dados['telefone'], dados['email'], dados['cliente_id']))
    conn.commit()
    #recupera o ID do contato recém-criado usando a propriedade lastrowid do objeto cursor.
    novo_id = cursor.lastrowid
    #fecha a conexão com o banco de dados.
    conn.close()
    #retorna o ID do novo contato em formato JSON para o cliente que fez a requisição HTTP.
    return jsonify({'id': novo_id})

# Define a rota para a exclusão de um contato
@app.route('/contatos/<int:id>', methods=['DELETE'])
def excluir_contato(id):
    # Obtém o cliente_id do corpo da requisição HTTP em formato JSON
    dados = request.json
    cliente_id = dados.get('cliente_id')
    
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()

    # Verifica se o id e o cliente_id pertencem ao mesmo registro
    cursor.execute('SELECT id FROM contatos WHERE id = ? AND cliente_id = ?', (id, cliente_id))
    registro = cursor.fetchone()
    if registro is None:
        conn.close()
        # Retorna uma mensagem de erro em formato JSON como resposta HTTP
        return jsonify({'erro': 'Contato não encontrado ou não pertence ao cliente especificado'}), 404

    cursor.execute('DELETE FROM contatos WHERE id = ?', (id,))
    conn.commit()
    
    conn.close()
    # Retorna uma mensagem de sucesso em formato JSON como resposta HTTP
    return jsonify({'mensagem': 'Contato excluído com sucesso'})

@app.route('/contatos/<int:id>', methods=['PUT'])
def atualizar_contato(id):

    # Obtém os dados do contato a ser atualizado do corpo da requisição HTTP em formato JSON
    dados = request.json
    
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()

    # Verifica se o contato a ser atualizado pertence ao cliente que está realizando a requisição
    cursor.execute('SELECT cliente_id FROM contatos WHERE id = ?', (id,))
    result = cursor.fetchone()

    if result is None:
        conn.close()
        # Retorna uma mensagem de erro em formato JSON como resposta HTTP
        return jsonify({'mensagem': 'Contato não encontrado'}), 404

    cursor.execute('UPDATE contatos SET nome = ?, telefone = ?, email = ? WHERE id = ?',
                   (dados['nome'], dados['telefone'], dados['email'], id))
    conn.commit()
    
    conn.close()
    
    #Retorna uma mensagem de sucesso em formato JSON como resposta HTTP
    return jsonify({'mensagem': 'Contato atualizado com sucesso'})

if __name__ == '__main__':
    app.run(debug=False)