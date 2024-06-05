import requests
from bs4 import BeautifulSoup
from mecanismosBusca import buscaGoodReads


HEADING = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'}


urlAmazon = 'https://www.amazon.com.br' #deu errado/ 503
urlCultura = 'https://www.livrariacultura.com.br' # funcionou/ retornou 200
urlSaraiva = 'https://www.saraiva.com.br' # funcionou/ retornou 200
urlSubmarino = 'https://www.submarino.com.br/busca/' # funcionou depois do user agent
urlEstante = 'https://www.estantevirtual.com.br' # funcionou / retornou 200


buscaGoodReads('o homem mais rico da babilônia')



#Fazer uma função diferente para cada site, mas depois de concluído, criar uma função com as partes que se repetem em todos
#Usar o nome do autor junto do nome do livro para conseguir resultados mais corretos
#Usar o filtro de menor preço, além de pegar os mais baratos ainda ajuda a filtrar os kits de livros
#Agora eu preciso entrar no link provided dentro da tag 'a' para entrar na página do livro e procurar o nome do autor
#Outra maneira de filtrar é colocar apenas livros com avaliação
#Colocar o código para fazer uma pesquisa no google usando o nome do livro e usar o nome do autor como referência para fazer a filtragem
 


def checarAutor(query):
    response = requests.get('https://www.google.com/search?q={query}', headers=HEADING)
    soup = BeautifulSoup(response.text, 'html.parser')
    autor = soup.find('a', class_='FLP8od')
    print(autor)



def submarino(busca):
    #essa variável retira os espaços do query e coloca um '-' no lugar, para funcionar no link para pegar o preço mais baixo
    busca = busca.replace(' ', '-')
    responseBusca = requests.get(f'https://www.submarino.com.br/busca/{busca}?content={busca.replace("-", "%20")}&filter=%7B%22id%22%3A%22rating%22%2C%22value%22%3A%223%2C5+-+4%2C5%22%2C%22fixed%22%3Afalse%7D&sortBy=lowerPrice', headers=HEADING)
    soupBusca = BeautifulSoup(responseBusca.text, 'html.parser')
    #essa variável está procurando todas as tags 'a' com essa classe, que contém todas as informações dos livros
    container = soupBusca.find_all('a', class_='inStockCard__Link-sc-1ngt5zo-1 JOEpk')
    for i in container:
        #entrar nesse link e procurar o nome do autor, criar um response, um soup e um find usando a tag específica do nome do autor como argumento
        responseLivro = requests.get(f'https://www.submarino.com.br{i["href"]}', headers=HEADING)
        soupLivro = BeautifulSoup(responseLivro.text, 'html.parser')
        autor = soupLivro.find('p', class_='src__AuthorUI-sc-1gt98wm-10 kOvTUY')
        print(autor.text)

        
    

try:
    pass
















except Exception as e:
    print(e)
