#importa o módulo "socket"
import socket

def main():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as  client_socket:
        server_address = ('localhost', 500)
        client_socket.connect(server_address)
        global cliente_id
        cliente_id = input("Digite seu id para continuar: ")
        while True:
                # loop principal do cliente
                # exibindo opções para o usuário
                print('Escolha uma opção:')
                print('1 - Adicionar contato')
                print('2 - Pesquisar por letra')
                print('3 - Pesquisar por nome')
                print('4 - Próximo registro')
                print('5 - Pular para próxima letra')
                print('6 - Apagar um registro')
                print('7 - Alterar um registro')
                print('0 - Sair')

                opcao = input('Opção: ')

                # processando a opção do usuário
                if opcao == '1':
                    nome = input('Nome:')
                    telefone = input('Telefone:')
                    email = input('E-mail:')
                    #uma mensagem é criada usando as informações inseridas pelo usuário 
                    mensagem = 'ADD{},{},{},{}'.format(nome,telefone,email,cliente_id)
                elif opcao == '2':
                    letra = input('Digite uma letra:')
                    mensagem = 'LETRA{},{}'.format(letra,cliente_id)
                elif opcao == '3':
                    nome = input('Digite um nome:')
                    mensagem = 'NOME{},{}'.format(nome,cliente_id)
                elif opcao == '4':
                    mensagem = 'PROXIMO{}'.format(cliente_id)
                elif opcao == '5':
                    mensagem = 'PULAR{}'.format(cliente_id)
                elif opcao == '6':
                    nome = input('Digite o nome do contato a ser apagado:')
                    mensagem = 'APAGAR{},{}'.format(nome,cliente_id)
                elif opcao == '7':
                    nome = input('Digite o nome do contato a ser alterado:')
                    novo_telefone = input('Novo telefone:')
                    novo_email = input('Novo e-mail:')
                    mensagem = 'ALTERAR{},{},{},{}'.format(nome, novo_telefone, novo_email,cliente_id)
                elif opcao == '0':
                    print('Encerrando...')
                    break
                else:
                    print('Opção inválida. Tente novamente.')

                # enviando mensagem para o servidor
                client_socket.sendall(mensagem.encode())

                # recebendo resposta do servidor
                resposta = client_socket.recv(1024).decode()

                # processando resposta do servidor
                if resposta == 'OK':
                    print('Operação realizada com sucesso.')
                elif resposta == 'CONTATO_NAO_ENCONTRADO':
                    print('Contato não encontrado.')
                elif resposta.startswith('CONTATO'):
                    dados_contato = resposta.split(',')
                    print('Nome:{}'.format(dados_contato[1]))
                elif resposta.startswith('REGISTROS'):
                    registros = resposta.split(':')[1].split(',')
                    for registro in registros:
                        print(registro)
                else:
                    print('res: {}'.format(resposta))
        # fechando conexão
    #client_socket.close()
if __name__ == '__main__':
    main()