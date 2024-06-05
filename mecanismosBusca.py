from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from bs4 import BeautifulSoup
import requests
import time
HEADING = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'}

def buscaGoogle(query):
    # Caminho para o ChromeDriver
    PATH = '/bin/chromedriver'
    # Configura as opções do Chrome
    chrome_options = Options()
    # Impede a página de ser aberta
    chrome_options.add_argument('--headless')
    # Inicializa o serviço do ChromeDriver
    service = Service(PATH)
    # Inicializa o WebDriver do Chrome com o serviço e as opções configuradas
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # Acessa o site especificado
    driver.get('https://www.google.com')
    input_element = driver.find_element(By.ID, 'APjFqb')
    #escrever a pesquisa no youtube
    input_element.send_keys('Quem é o autor de  ', query)
    #esperar a página carregar para apertar o enter  
    time.sleep(2)
    #apertar o enter depois da página estar carregada
    input_element.send_keys(Keys.ENTER)
    time.sleep(2)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    #tentar esses 2 e se não funcionar procurar na wikipedia
    titulo = soup.find('div', class_='kp-header')
    autor = titulo.find('a').text
    print(autor)

 


#busca no website goodreads, é a maneira mais rápida
def buscaGoodReads(query):
    responsePesquisa = requests.get(f'https://www.goodreads.com/search?utf8=%E2%9C%93&query={query}', headers=HEADING)
    soupPesquisa = BeautifulSoup(responsePesquisa.text, 'html.parser')
    primeiroResultado = soupPesquisa.find('tr', attrs={'itemtype':'http://schema.org/Book'})
    autor = primeiroResultado.find('a', class_='authorName').text
    print('o goodreads foi usado')
