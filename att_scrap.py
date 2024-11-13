from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
import requests
import os
import schedule
import time
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Carregar variáveis de ambiente
load_dotenv()

app = FastAPI()

class AdrenalineScraper:
    def __init__(self):
        self.url = "https://www.adrenaline.com.br/games/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        self.news_data = []
        self.last_update = None

    def get_news_data(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('article', {'class': 'feed'})

            self.news_data = []
            for article in articles[:10]:  # Pega até 10 notícias
                title_elem = article.find('h2')
                link_elem = article.find('a', href=True)
                if title_elem and link_elem:
                    title = title_elem.text.strip()
                    link = link_elem['href']
                    date = datetime.now().strftime("%d/%m/%Y")

                    news_data = {
                        'título': title,
                        'link': link,
                        'data': date
                    }
                    self.news_data.append(news_data)
            self.last_update = datetime.now()
            print("Scraping concluído com sucesso.")
            return True
        except Exception as e:
            print(f"Erro ao fazer scraping: {e}")
            return False

    def get_latest_news(self):
        return self.news_data

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
                <body>
                    <h2>Últimas Notícias de Games - Adrenaline</h2>
                    {html_table}
                    <p>Data da extração: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
                </body>
            </html>
            """
            msg.attach(MIMEText(html_content, 'html'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_from, self.email_password)
            server.send_message(msg)
            server.quit()
            print("Email enviado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return False

# Instância do scraper e email sender
scraper = AdrenalineScraper()
email_sender = EmailSender()

# Função para realizar scraping diário e enviar o email
def daily_scraping():
    print("Executando scraping diário...")
    if scraper.get_news_data():
        news_data = scraper.get_latest_news()
        if news_data:
            email_sender.send_email(news_data)

# Agendar a função de scraping diário
schedule.every().day.at("12:00:00").do(daily_scraping)

# Função para rodar o schedule em background
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Endpoint para obter as notícias mais recentes
@app.get("/news", response_model=list)
def get_news():
    news = scraper.get_latest_news()
    if not news:
        raise HTTPException(status_code=404, detail="Nenhuma notícia encontrada.")
    return news

# Novo endpoint para forçar a atualização das notícias
@app.post("/update-news")
def update_news():
    if scraper.get_news_data():
        return {
            "status": "success",
            "message": "Notícias atualizadas com sucesso",
            "timestamp": scraper.last_update.strftime("%d/%m/%Y %H:%M:%S"),
            "total_news": len(scraper.news_data)
        }
    else:
        raise HTTPException(
            status_code=500,
            detail="Erro ao atualizar as notícias"
        )

# Novo endpoint para forçar o envio de email
@app.post("/send-email")
def force_send_email():
    news_data = scraper.get_latest_news()
    if not news_data:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma notícia disponível para enviar por email"
        )
    
    if email_sender.send_email(news_data):
        return {
            "status": "success",
            "message": "Email enviado com sucesso",
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
    else:
        raise HTTPException(
            status_code=500,
            detail="Erro ao enviar o email"
        )

# Novo endpoint para obter status do último scraping
@app.get("/status")
def get_status():
    return {
        "last_update": scraper.last_update.strftime("%d/%m/%Y %H:%M:%S") if scraper.last_update else None,
        "total_news": len(scraper.news_data),
        "has_news": len(scraper.news_data) > 0
    }

# Inicializar o thread do agendador
thread = threading.Thread(target=run_scheduler)
thread.daemon = True
thread.start()