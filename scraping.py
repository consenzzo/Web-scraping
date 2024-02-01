# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import StaleElementReferenceException
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import nltk
# from nltk.corpus import stopwords
# from collections import Counter
# import re
# import pandas as pd

# # Configuração inicial do NLTK
# nltk.download('stopwords')
# stop_words = set(stopwords.words('portuguese'))

# # Configurações do Selenium
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Executa o Chrome em modo headless (sem abrir a janela)

# service = Service('caminho/para/chromedriver')  # Substitua pelo caminho do seu ChromeDriver
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# # Função para fazer o web scraping com Selenium
# def scrape_site(url):
#     driver.get(url)
#     time.sleep(5)  # Espera inicial

#     # Rolar a página para baixo para carregar mais elementos
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     while True:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(5)  # Espera para carregar a página
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height

#     return driver.page_source

# # Função para limpar e processar o texto
# def process_text(text):
#     words = re.findall(r'\b[a-z]+\b', text.lower())
#     words = [word for word in words if word not in stop_words]
#     return words

# # Função principal
# def main():
#     i = 1
#     total_pages = [1]
#     lista_de_texto = []
#     all_words = {'texto':[] , 'valor':[], 'pagina':[]}
    
#     while i <= max(total_pages):
#         url = f'https://www.workana.com/jobs?category=it-programming&language=pt&subcategory=web-development%2Cdata-science-1%2Cdesktop-apps&page={i}'
#         page_source = scrape_site(url)
#         # Use o Selenium para encontrar os elementos
#         driver.get(url)
#         # driver.execute_script("window.scrollBy(0, 500);")

#         pagination_container = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CLASS_NAME, 'pagination'))
#         )
#         pagination_items = pagination_container.find_elements(By.TAG_NAME, 'li')


#         # pagination_container = driver.find_element(By.CLASS_NAME, 'pagination')
#         # pagination_items = pagination_container.find_elements(By.TAG_NAME, 'li')
#         for item in pagination_items:
#             page_number_text = item.text.strip()
#             if page_number_text.isdigit():  # Verifica se o texto é um número
#                 total_pages.append(int(page_number_text))

#         # project_elements = driver.find_elements(By.CLASS_NAME, 'js-project') 
#         WebDriverWait(driver, 10).until(
#                 EC.presence_of_all_elements_located((By.CLASS_NAME, 'js-project'))
#             )
#         project_elements = driver.find_elements(By.CLASS_NAME, 'js-project') 

#         for element in project_elements:
#             # try:
#             body = element.find_element(By.CLASS_NAME,'project-body')
#             details =  body.find_element(By.CLASS_NAME,'project-details')
#             text = details.find_element(By.CLASS_NAME,'js-expander-passed').text.strip()
#             text = text.strip('... Ver mais detalhes')
#             # except StaleElementReferenceException:
#             #     i += 1
#             #     break
#                 # text_element = element.find_element(By.CLASS_NAME, 'js-expander-passed')
#                 # text = text_element.text.strip().strip('... Ver mais detalhes')

#             # try:
#             valor = element.find_elements(By.CLASS_NAME,'values').text.strip()
#             # except StaleElementReferenceException:
#             #     valor = 0
#                 # valor = element.find_element(By.CLASS_NAME, 'values').text.strip()
#             # text = element.text.strip()
#             # words = process_text(text)
#             # all_words.extend(words)
#             all_words['texto'].append(text)
#             all_words['valor'].append(valor)
#             all_words['pagina'].append(i)


#         # Contar a frequência das palavras
#         # word_counts = Counter(all_words)
#         # print("Palavras mais comuns nos títulos dos projetos:")
#         # for word, count in word_counts.most_common(10):
#         #     print(f'{word}: {count}')
#         # for palavra in all_words:
#         #     print(f'texto >> {palavra}\n')

        

#         if i == max(total_pages):
#             break

#     driver.quit()

#     df = pd.DataFrame(all_words)
#     df.to_csv('vagas.csv', encoding='utf-8', sep=';')   

# if __name__ == '__main__':
#     main()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import math
import re

# Configuração inicial
url = 'https://www.workana.com/pt/jobs'
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

driver.get(url)

time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')

dic_text = {'text': [], 'value': [], 'page': [],}
i = 1
total_pages = [1]

while i <= max(total_pages):

    # for i in range( 1, max(total_pages)):
    url_pag = f'https://www.workana.com/jobs?category=it-programming&language=pt&subcategory=web-development%2Cdata-science-1%2Cdesktop-apps&page={i}'
    driver.get(url_pag)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    pages = soup.find_all('ul', class_=re.compile('pagination'))
    try:
        li_tags = pages[0].find_all('li')

        # Loop para obter o texto de cada tag <li>
        for li_tag in li_tags:
            li_text = li_tag.text
            if li_text.isdigit():  # Verifica se o texto é um número
                if li_text not in total_pages:
                    total_pages.append(int(li_text))
                    print(max(total_pages))
    except:
        pass


#         # pagination_container = driver.find_element(By.CLASS_NAME, 'pagination')
#         # pagination_items = pagination_container.find_elements(By.TAG_NAME, 'li')
#         for item in pagination_items:
#             page_number_text = item.text.strip()
#             if page_number_text.isdigit():  # Verifica se o texto é um número
#                 total_pages.append(int(page_number_text))

    texts = soup.find_all('div', class_=re.compile('js-project'))

    for text in texts:
        texto = text.find('div', class_=re.compile('js-expander-passed')).get_text().strip()
        value = text.find('span', class_=re.compile('values')).get_text().strip()

        # print(marca, preco)

        dic_text['text'].append(texto)
        dic_text['value'].append(value)
        dic_text['page'].append(i)

    print(url_pag)
    i += 1
    
    if i == max(total_pages):
        break

driver.quit()

df = pd.DataFrame(dic_text)
df.to_csv('vagas.csv', sep=';')
# for item , text in enumerate(dic_text['text']):
#     print(f'TEXTO = {text}\n')
