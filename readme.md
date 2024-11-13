# Adrenaline News Scraper

Um scraper automático para notícias do site Adrenaline.

## Instalação

1. Clone o repositório
```bash
git clone [url-do-seu-repositorio]
cd [nome-do-repositorio]
```

2. Instale as dependências
```bash
pip install -r requirements.txt
```

3. Configure o arquivo .env
```
EMAIL_FROM=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_de_app
EMAIL_TO=email_destino@exemplo.com
```

## Uso

Para iniciar o servidor:
```bash
uvicorn main:app --reload
```

### Endpoints disponíveis:

- GET `/news` - Retorna as notícias mais recentes
- POST `/update-news` - Força atualização das notícias
- POST `/send-email` - Força envio de email
- GET `/status` - Retorna status do scraper
- GET `/scheduler-status` - Retorna status do agendador

O scraper executará automaticamente todos os dias às 12:00 da manhã.