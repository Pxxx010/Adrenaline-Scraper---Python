
# Adrenaline Scraper

Este projeto é um scraper desenvolvido em Python para coletar as últimas notícias de games do site Adrenaline e enviá-las por e-mail de forma automatizada.

## Descrição

O Adrenaline Scraper acessa a seção de games do site Adrenaline e extrai as últimas 10 notícias. Os dados coletados incluem:
- Título da notícia
- Data de publicação
- Link para o artigo

Essas informações são enviadas por e-mail em formato HTML, com uma tabela para facilitar a leitura.

## Pré-requisitos

Antes de executar o projeto, você precisa:

1. Ter o Python instalado (versão 3.6 ou superior).
2. Instalar as dependências listadas no arquivo `requirements.txt`.

### Dependências

Instale as dependências do projeto usando:

```bash
pip install -r requirements.txt
```

### Variáveis de Ambiente

Crie um arquivo `.env` no diretório principal do projeto e configure as seguintes variáveis:

- `EMAIL_FROM`: Endereço de e-mail que enviará as notícias.
- `EMAIL_PASSWORD`: Senha do e-mail (sugere-se o uso de senhas de aplicativo).
- `EMAIL_TO`: Endereço de e-mail que receberá as notícias.

Exemplo do arquivo `.env`:

```plaintext
EMAIL_FROM=seuemail@gmail.com
EMAIL_PASSWORD=suasenha
EMAIL_TO=emaildestino@gmail.com
```

## Estrutura do Código

- `AdrenalineScraper`: Classe responsável por acessar o site Adrenaline e coletar os dados das notícias.
- `EmailSender`: Classe responsável por formatar as notícias em HTML e enviar o e-mail.
- `main()`: Função principal que coordena a extração dos dados e o envio do e-mail.

## Como Executar

Para executar o projeto, use o comando:

```bash
python scrap.py
```

O script:
1. Verificará as configurações do arquivo `.env`.
2. Realizará o scraping das notícias no site Adrenaline.
3. Enviará as notícias coletadas por e-mail.

## Contribuição

Sinta-se à vontade para abrir issues e pull requests para melhorar o código ou adicionar novas funcionalidades.

## Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais informações.
