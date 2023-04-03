import socket
import sqlite3
import threading

conn = sqlite3.connect('agenda.db')

cursor = conn.cursor()

conn.execute('''
CREATE TABLE IF NOT EXISTS contatos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    email TEXT NOT NULL,
    cliente_id INTEGER NOT NULL
)
''')


conn.commit()
registro_atual = None
letra_atual = 'a'
def adicionar_contato(nome, telefone, email, cliente_id):
    with sqlite3.connect("agenda.db") as conn:
        cursor = conn.cursor()
         
        cursor.execute('INSERT INTO contatos (nome, telefone, email, cliente_id) VALUES (?, ?, ?,?)', (nome, telefone, email,cliente_id))
        conn.commit()
        return 'Contato adicionado com sucesso.'

def apagar_contato(nome, cliente_id):
    with sqlite3.connect("agenda.db") as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM contatos WHERE nome = ? AND cliente_id = ?', (nome, cliente_id))
        conn.commit()
        if cursor.rowcount == 1:
            return 'Contato removido com sucesso.'
        else:
            return 'Contato não encontrado.'
    
def pesquisar_letra(letra, cliente_id):
    resultados = []
    # pesquisando contatos no banco de dados
    conn = sqlite3.connect('agenda.db')
    c = conn.cursor()
    c.execute('SELECT * FROM contatos WHERE LOWER(nome) LIKE ? || "%" AND cliente_id = ?', (str(letra.lower()), cliente_id))
    rows = c.fetchall()
    conn.close()

    # transformando os resultados em uma lista de dicionários
    for row in rows:
        contato = {'nome': row[1], 'telefone': row[2], 'email': row[3]}
        resultados.append(contato)

    return resultados

def proximo_registro(cliente_id):
    global registro_atual
    # Check if cliente_id is a list and extract the first element
    if isinstance(cliente_id, list):
        cliente_id = cliente_id[0]
    # Convert cliente_id to integer
    cliente_id = int(cliente_id)

    # se o registro atual ainda não foi definido, buscar o primeiro registro
    if registro_atual is None:
        conn = sqlite3.connect('agenda.db')
        c = conn.cursor()
        c.execute('SELECT * FROM contatos WHERE cliente_id = ? ORDER BY nome ASC', (cliente_id,))
        rows = c.fetchall()
        conn.close()

        if rows:
            registro_atual = rows[0]
            return registro_atual
        else:
            return None

    # buscar todos os registros para o cliente
    conn = sqlite3.connect('agenda.db')
    c = conn.cursor()
    c.execute('SELECT * FROM contatos WHERE cliente_id = ? ORDER BY nome ASC', (cliente_id,))
    rows = c.fetchall()
    conn.close()

    # procurar pelo registro atual e retornar o próximo
    for i in range(len(rows)):
        if rows[i] == registro_atual:
            if i < len(rows) - 1:
                registro_atual = rows[i + 1]
                return registro_atual
            else:
                return None
    
    # se o registro atual não for encontrado, retornar o primeiro registro
    registro_atual = rows[0]
    return registro_atual

def pesquisar_nome(nome, cliente_id):
    resultados = []
    # pesquisando contatos no banco de dados
    conn = sqlite3.connect('agenda.db')
    c = conn.cursor()
    c.execute('SELECT * FROM contatos WHERE LOWER(nome) = ? AND cliente_id = ?', (nome.lower(), cliente_id))
    row = c.fetchone()
    conn.close()

    if row is not None:
        # transformando o resultado em uma lista de dicionários
        contato = {'nome': row[1], 'telefone': row[2], 'email': row[3]}
        resultados.append(contato)

    return resultados
    
def pular_letra():
    # avançando para a próxima letra
    global letra_atual
    if letra_atual == '':
        letra_atual = 'A'
    else:
        letra_atual = chr(ord(letra_atual) + 1)
        if letra_atual > 'Z':
            letra_atual = 'A'
    return letra_atual

def alterar_contato(nome, novo_telefone, novo_email, cliente_id):
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE contatos SET telefone = ?, email = ? WHERE nome = ? AND cliente_id = ?', (novo_telefone, novo_email, nome, cliente_id))
    conn.commit()
    conn.close()
    return "Contato atualizado com sucesso."


def handle_client(client_socket, client_address):
    print('Conectado por', client_address)
    while True:
        mensagem  = client_socket.recv(1024)  # Recebe dados do cliente
        if not mensagem:
            break  # Se não há mensagem, sai do loop interno

        # processar a mensagem recebida
        mensagem = mensagem.decode()
        if mensagem.startswith('ADD'):
            nome, telefone, email, cliente_id = mensagem[3:].split(',')
            resultado = adicionar_contato(nome, telefone, email,cliente_id)
        elif mensagem.startswith('LETRA'):
            letra,cliente_id = mensagem[5:].upper().split(',')
            resultados = pesquisar_letra(letra,cliente_id)
            resultado = str(resultados)
        elif mensagem.startswith('NOME'):
            nome,cliente_id= mensagem[4:].lower().split(',')
            resultados = pesquisar_nome(nome,cliente_id)
            resultado = str(resultados)
        elif mensagem.startswith('PROXIMO'):
            cliente_id = mensagem[7:].lower().split(',')
            resultados = proximo_registro(cliente_id)
            resultado = str(resultados)
        elif mensagem.startswith('PULAR'):
            cliente_id = mensagem[5:].lower()
            letra_atual = pular_letra()
            resultados = pesquisar_letra(letra_atual,cliente_id)
            resultado = str(resultados)
        elif mensagem.startswith('APAGAR'):
            nome, cliente_id = mensagem[6:].lower().split(',')
            resultado = apagar_contato(nome,cliente_id)
        elif mensagem.startswith('ALTERAR'):
            dados = mensagem[7:].split(',')
            nome = dados[0].lower()
            novo_telefone = dados[1]
            novo_email = dados[2]
            cliente_id = int(dados[3])
            resultado = alterar_contato(nome, novo_telefone, novo_email, cliente_id)
        else:
            resultado = 'Comando inválido'

        # enviar a resposta de volta para o cliente
        client_socket.sendall(resultado.encode())

    client_socket.close()

print('Aguardando conexão...')

# loop principal do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 500))
server_socket.listen(5)  # permitir até 5 conexões simultâneas

while True:
    client_socket, client_address = server_socket.accept()  # Aceita uma conexão

    # criar uma nova thread para lidar com o cliente
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()