#é responsável por importar o módulo requests, que é utilizado para realizar requisições HTTP
import requests

# Define a URL base do servidor
url_base = 'http://localhost:5000'

# Define o ID do cliente atual

# Variável global para manter o rastreamento da última letra pesquisada
ultima_letra = 'a'

# Função para listar os contatos
def listar_contatos(letra=None, nome=None):
    global ultima_letra # torna a variável global acessível dentro da função
    #define o dicionário "parametros" com a chave "cliente_id" e valor "cliente_id"
    parametros = {'cliente_id': cliente_id}
    
    if letra:
        parametros['letra'] = letra
        ultima_letra = letra # atualiza a variável global "ultima_letra" com o valor do parâmetro "letra"
    elif nome:
        parametros['nome'] = nome # adiciona ao dicionário "parametros" a chave "nome" com o valor do parâmetro "nome"
    #faz uma requisição GET à URL "url_base/contatos" com os parâmetros definidos no dicionário "parametros"
    response = requests.get(f'{url_base}/contatos', params=parametros)
    
     # se a requisição foi bem sucedida
    if response.status_code == 200:
        # converte a resposta da requisição em JSON e atribui o resultado à variável "contatos"
        contatos = response.json()
        # conta o total de contatos retornados na resposta
        total_contatos = len(contatos)
        # se não houver contatos retornados
        if total_contatos == 0:
            print('Nenhum contato encontrado')
            return
        
        contador = 1 # o contador é utilizado para imprimir o número de cada contato na lista
        for contato in contatos: # Itera sobre a lista de contatos
             # Imprime uma mensagem para cada contato, incluindo o ID, nome, telefone e email
            print(f'{contador}. ID:{contato["id"]} - {contato["nome"]} - {contato["telefone"]} - {contato["email"]}')
            contador += 1
    else:
        print('Erro ao listar contatos')

# Função para pular para a próxima letra
def pular_proxima_letra():
    global ultima_letra # torna a variável global acessível dentro da função
    letra = chr(ord(ultima_letra) + 1) # pega a próxima letra em ordem alfabética
    listar_contatos(letra=letra)
    
def proximo_contato():
    #Cria um dicionário 
    parametros = {'cliente_id': cliente_id}
    # Realiza uma requisição GET para a url_base + "/contatos" passando os "parametros" como parâmetros da requisição
    response = requests.get(f'{url_base}/contatos', params=parametros)
    
    if response.status_code == 200:
        # Converte a resposta em JSON para uma lista de contatos
        contatos = response.json()
        # Calcula o número total de contatos na list
        total_contatos = len(contatos)
        if total_contatos == 0: #Se a lista de contatos está vazia
            print('Nenhum contato encontrado')
            return
        # Atualiza o índice para o próximo contato na lista (com looping quando chega ao fim da lista)
        proximo_contato.indice = (proximo_contato.indice + 1) % total_contatos
        # Pega o contato correspondente ao índice atual e o imprime na tela
        contato = contatos[proximo_contato.indice]
        print(f'{proximo_contato.indice+1}. {contato["nome"]} - {contato["telefone"]} - {contato["email"]}')
    else:
        print('Erro ao listar contatos')
proximo_contato.indice = -1

# Função para criar um contato
def criar_contato():
    nome = input('Nome: ') #Solicita o nome do contato
    telefone = input('Telefone: ') #Solicita o Telefone 
    email = input('E-mail: ')#Solicita email

    # Cria um dicionário com os dados do novo contato
    dados = {
        'nome': nome,
        'telefone': telefone,
        'email': email,
        'cliente_id': cliente_id
    }
    # Envia uma requisição HTTP do tipo POST para  /contatos da API, passando os dados do novo contato em formato JSON
    response = requests.post(f'{url_base}/contatos', json=dados)
    # Verifica se a requisição foi bem-sucedida (código HTTP 200)
    if response.status_code == 200: 
        # Obtém o ID do novo contato a partir da resposta JSON da API
        novo_id = response.json()['id']
        print(f'Contato criado com sucesso. ID: {novo_id}')
    else:
        print('Erro ao criar contato')

# Função para excluir um contato
def excluir_contato():
    id = input('ID do contato: ')
    
    dados = {
        'cliente_id': cliente_id
    }
    
    response = requests.delete(f'{url_base}/contatos/{id}', json=dados)
    
    if response.status_code == 200:
        print('Contato excluído com sucesso')
    else:
        print('Erro ao excluir contato')

# Função para atualizar um contato
def atualizar_contato():
    id = input('ID do contato: ')
    nome = input('Nome: ')
    telefone = input('Telefone: ')
    email = input('E-mail: ')
    
    dados = {
        'nome': nome,
        'telefone': telefone,
        'email': email,
        'cliente_id': cliente_id
    }
    
    response = requests.put(f'{url_base}/contatos/{id}', json=dados)
    
    if response.status_code == 200:
        print('Contato atualizado com sucesso')
    else:
        print('Erro ao atualizar contato')

def print_menu():
    print("1. Inserir novo contato")
    print("2. Pesquisar por letra")
    print("3. Pesquisar por nome")
    print("4. Próximo registro")
    print("5. Pular para próxima letra")
    print("6. Apagar um registro")
    print("7. Alterar um registro")
    print("0. Sair")

def main():
# Loop principal do programa
    global cliente_id
    cliente_id = input("Digite seu id para continuar: ")
    while True:
       
        print_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
             criar_contato()
        elif opcao == '2':
            letra = input('Digite a letra para filtrar: ')
            listar_contatos(letra=letra)
        elif opcao == '3':
            nome = input('Digite o nome para filtrar: ')
            listar_contatos(nome=nome)
        elif opcao == '4':
            proximo_contato()
        elif opcao == '5':
            pular_proxima_letra()
        elif opcao == '6':
            excluir_contato()
        elif opcao == '7':
            atualizar_contato()
        elif opcao == '0':
            break
        else:
            print('Opção inválida')
if __name__ == '__main__':
    main()