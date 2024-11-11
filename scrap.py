import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class AdrenalineScraper:
    def __init__(self):
        self.url = "https://www.adrenaline.com.br/games/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
        }

    def get_news_data(self):
        try:
            print("Fazendo requisição para a página do Adrenaline...".encode("utf-8"))
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()

            print(f"Status Code: {response.status_code}")
            soup = BeautifulSoup(response.content, 'html.parser')

            news_list = []
            articles = soup.find_all('article', {'class': 'feed'})

            print(f"Encontrados {len(articles)} artigos")

            for article in articles[:10]:  # Pega até 10 notícias
                try:
                    title_elem = article.find('h2')
                    link_elem = article.find('a', href=True)
                    date_elem = article.find('time')

                    if title_elem and link_elem:
                        title = title_elem.text.strip()
                        link = link_elem['href']
                        date = date_elem.text.strip() if date_elem else "Data não disponível"

                        news_data = {
                            'título': title,
                            'link': link,
                            'data': date
                        }
                        news_list.append(news_data)
                        print(f"Notícia encontrada: {title}".encode("utf-8"))
                except Exception as e:
                    print(f"Erro ao processar artigo: {e}".encode("utf-8"))
                    continue

            return news_list
        except Exception as e:
            print(f"Erro ao fazer scraping: {e}".encode("utf-8"))
            return []

class EmailSender:
    def __init__(self):
        self.email_from = os.getenv('EMAIL_FROM')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.email_to = os.getenv('EMAIL_TO')

    def create_html_table(self, data):
        html = """
        <table border="1" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #f2f2f2;">
                <th style="padding: 8px; text-align: left;">Título</th>
                <th style="padding: 8px; text-align: left;">Data</th>
                <th style="padding: 8px; text-align: left;">Link</th>
            </tr>
        """
        
        for news in data:
            html += f"""
            <tr>
                <td style="padding: 8px;">{news['título']}</td>
                <td style="padding: 8px;">{news['data']}</td>
                <td style="padding: 8px;"><a href="{news['link']}">Ler mais</a></td>
            </tr>
            """
        
        html += "</table>"
        return html

    def send_email(self, news_data):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_from
            msg['To'] = self.email_to
            msg['Subject'] = f'Últimas Notícias de Games - Adrenaline - {datetime.now().strftime("%d/%m/%Y")}'

            html_table = self.create_html_table(news_data)
            html_content = f"""
            <html>
                <head>
                    <style>
                        table {{
                            border-collapse: collapse;
                            width: 100%;
                        }}
                        th, td {{
                            border: 1px solid black;
                            padding: 8px;
                            text-align: left;
                        }}
                        th {{
                            background-color: #f2f2f2;
                        }}
                        a {{
                            color: #0066cc;
                            text-decoration: none;
                        }}
                        a:hover {{
                            text-decoration: underline;
                        }}
                    </style>
                </head>
                <body>
                    <h2>Últimas Notícias de Games - Adrenaline</h2>
                    {html_table}
                    <p>Data da extração: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
                </body>
            </html>
            """

            msg.attach(MIMEText(html_content, 'html'))

            print("Conectando ao servidor SMTP...".encode("utf-8"))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            
            print("Fazendo login no email...".encode("utf-8"))
            server.login(self.email_from, self.email_password)
            
            print("Enviando email...".encode("utf-8"))
            server.send_message(msg)
            server.quit()
            
            print("Email enviado com sucesso!".encode("utf-8"))
        except Exception as e:
            print(f"Erro ao enviar email: {e}".encode("utf-8"))

def main():
    print("Verificando configurações...".encode("utf-8"))
    
    if not os.path.isfile('.env'):
        print("Erro: Arquivo .env não encontrado!".encode("utf-8"))
        return
    
    email_from = os.getenv('EMAIL_FROM')
    email_password = os.getenv('EMAIL_PASSWORD')
    email_to = os.getenv('EMAIL_TO')
    
    if not all([email_from, email_password, email_to]):
        print("Erro: Configurações de email incompletas no arquivo .env!".encode("utf-8"))
        print(f"EMAIL_FROM: {'Configurado' if email_from else 'Não configurado'}".encode("utf-8"))
        print(f"EMAIL_PASSWORD: {'Configurado' if email_password else 'Não configurado'}".encode("utf-8"))
        print(f"EMAIL_TO: {'Configurado' if email_to else 'Não configurado'}".encode("utf-8"))
        return

    print("Iniciando scraping do Adrenaline...".encode("utf-8"))
    scraper = AdrenalineScraper()
    news_data = scraper.get_news_data()

    if news_data:
        print(f"Encontradas {len(news_data)} notícias. Preparando para enviar email...".encode("utf-8"))
        email_sender = EmailSender()
        email_sender.send_email(news_data)
    else:
        print("Nenhuma notícia foi coletada para enviar.".encode("utf-8"))

if __name__ == "__main__":
    main()
