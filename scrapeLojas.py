import requests
import random
from bs4 import BeautifulSoup
from mecanismosBusca import buscaGoodReads









user_agents = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0'
]

user_agent = random.choice(user_agents)


HEADING = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'}
heading_teste = {'user-agent': user_agent}

urlAmazon = 'https://www.amazon.com.br' #deu errado/ 503
urlCultura = 'https://www.livrariacultura.com.br' # funcionou/ retornou 200
urlSaraiva = 'https://www.saraiva.com.br' # funcionou/ retornou 200
urlSubmarino = 'https://www.submarino.com.br/busca/' # terminada + ou -
urlEstante = 'https://www.estantevirtual.com.br' # funcionou / retornou 200

listaLivros = []


def limpaTexto(texto):
    texto = texto.replace('.', '')
    return texto

#função que vai ser usada em todas as outras funções, tem prioridade
#Só estão sendo imprimidos os autores que tem esse símbolo '|'
#se forem 2 autores?


def mudaLayout(string):
    if type(string) == str:
        resposta = string.split(',')
        resposta[0],resposta[1] = resposta[1], resposta[0]
        return " ".join(resposta)[1:]
    else:
        for i in range(len(string)):
            resposta = string[i].replace(' ', '').split(',')
            resposta[0],resposta[1] = resposta[1], resposta[0]
            string[i] = " ".join(resposta)
        return string


def comparaAutor(autor):
    resposta = ''
    try:
        if autor[autor.index('|') + 1].lower() == 'a':
            if autor[1].lower() == 'a':
                pass
                print(mudaLayout(autor.replace('\n', '').replace('Autor:', '').split('|')))
            else:
                autorPedaco = slice(10, autor.index('|'))
                print(mudaLayout(autor[autorPedaco]))
        else:
            autorPedaco = slice(7, autor.index('|'))
            print(mudaLayout(autor[autorPedaco]))
    except Exception as e:
        autorPedaco = slice(7, len(autor)+1)





#Fazer uma função diferente para cada site, mas depois de concluído, criar uma função com as partes que se repetem em todos
#Usar o nome do autor junto do nome do livro para conseguir resultados mais corretos
#Usar o filtro de menor preço, além de pegar os mais baratos ainda ajuda a filtrar os kits de livros
#Agora eu preciso entrar no link provided dentro da tag 'a' para entrar na página do livro e procurar o nome do autor
#Outra maneira de filtrar é colocar apenas livros com avaliação
#Colocar o código para fazer uma pesquisa no google usando o nome do livro e usar o nome do autor como referência para fazer a filtragem
#pegar a imagem também

#VOU TER QUE MELHORAR A FUNÇÃO DE COMPARAÇÃO DOS NOMES, CRIAR UMA FUNÇÃO PRÓPRIA PARA ISSO




#tá funcionando, não vai precisar do selenium
def cultura():
    responsePesquisa = requests.get('https://www.livrariacultura.com.br/livros/o%20homem%20mais%20rico%20da%20babil%C3%B4nia?PS=24&O=OrderByPriceASC', headers=heading_teste)
    soupPesquisa = BeautifulSoup(responsePesquisa.text, 'html.parser')
    livros = soupPesquisa.find_all('li', class_='livros')
    for livro in livros:
        imagem = livro.find('img')
        autor = livro.find('ul')
        comparaAutor(autor.text)







   




#nome do livro, autor, preco, loja, link
def submarino(busca):
    #essa variável retira os espaços do query e coloca um '-' no lugar, para funcionar no link para pegar o preço mais baixo
    resultadoAutor = buscaGoodReads(busca)
    busca = busca.replace(' ', '-')
    link = f'https://www.submarino.com.br/busca/{busca}?content={busca.replace("-", "%20")}&filter=%7B%22id%22%3A%22rating%22%2C%22value%22%3A%223%2C5+-+4%2C5%22%2C%22fixed%22%3Afalse%7D&sortBy=lowerPrice'
    responseBusca = requests.get(link, headers=HEADING)
    soupBusca = BeautifulSoup(responseBusca.text, 'html.parser')
    #essa variável está procurando todas as tags 'a' com essa classe, que contém todas as informações dos livros
    container = soupBusca.find_all('a', class_='inStockCard__Link-sc-1ngt5zo-1 JOEpk')
    for i in container:
        #entrar nesse link e procurar o nome do autor, criar um response, um soup e um find usando a tag específica do nome do autor como argumento
        responseLivro = requests.get(f'https://www.submarino.com.br{i["href"]}', headers=HEADING)
        soupLivro = BeautifulSoup(responseLivro.text, 'html.parser')
        titulo = soupLivro.find('h1', class_='src__Title-sc-1xq3hsd-0 eEEsym').text
        autor = soupLivro.find('p', class_='src__AuthorUI-sc-1gt98wm-10 kOvTUY').text
        preco = soupLivro.find('div', class_='src__BestPrice-sc-1jnodg3-5 ykHPU priceSales').text.replace('R$', '').replace(',', '.').replace(' ', '')
        if limpaTexto(autor) == limpaTexto(resultadoAutor):
            listaLivros.append([titulo, autor, preco, link, 'Submarino'])

        
    

try:
    cultura()
















except Exception as e:
    print(e)
