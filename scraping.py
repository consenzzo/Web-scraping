import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from collections import Counter
import re

# Configuração inicial do NLTK
nltk.download('stopwords')
stop_words = set(stopwords.words('portuguese'))

# Função para fazer o web scraping
def scrape_site(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

# Função para limpar e processar o texto
def process_text(text):
    # Removendo caracteres não-alfabéticos e convertendo para minúsculas
    words = re.findall(r'\b[a-z]+\b', text.lower())
    # Removendo stopwords
    words = [word for word in words if word not in stop_words]
    return words

# Função principal
def main():
    # print(stop_words)
    url = 'https://www.workana.com/jobs?category=it-programming&language=pt&subcategory=web-development%2Cdata-science-1%2Cdesktop-apps&page=1'
    soup = scrape_site(url)

    # Encontrar todos os títulos dos projetos
    project_titles = soup.find_all('div', class_='js-project')  # Adapte conforme necessário
    all_words = []

    for title in project_titles:
        words = title.find('div', class_='js-expander-passed').get_text().strip()
        # words = process_text(title.get_text())
        all_words.extend(words)

    # Contar a frequência das palavras
    word_counts = Counter(all_words)
    print("Palavras mais comuns nos títulos dos projetos:")
    for word, count in word_counts.most_common(10):
        print(f'{word}: {count}')

if __name__ == '__main__':
    main()
