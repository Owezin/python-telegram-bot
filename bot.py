import logging
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram import Update
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

# Configurações do bot
TOKEN = "8098294615:AAERsoEDOpj7WC-EdLZ9CMMoSzw9BusPFgk"

# Função para gerar imagem do produto
def gerar_imagem(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        nome_produto = soup.find("h1", class_="nome-produto").text.strip()
        preco_produto = soup.find("span", class_="preco-produto").text.strip()
        imagem_produto = soup.find("img", class_="imagem-produto")["src"]
        
        img = Image.open(requests.get(imagem_produto, stream=True).raw)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 24)
        draw.text((10, 10), nome_produto, font=font)
        draw.text((10, 40), preco_produto, font=font)
        img.save("produto.png")
    except Exception as e:
        print(f"Erro ao gerar imagem: {e}")

# Função para gerar legenda do produto
def gerar_legenda(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        nome_produto = soup.find("h1", class_="nome-produto").text.strip()
        preco_produto = soup.find("span", class_="preco-produto").text.strip()
        legenda = f"🚨 PROMOÇÃO! 🚨\n{nome_produto}\nPreço: {preco_produto}\nCompre agora e economize!"
        return legenda
    except Exception as e:
        print(f"Erro ao gerar legenda: {e}")
        return "Erro ao gerar legenda"

# Função para lidar com o comando
def produto(update, context):
    try:
        url = context.args[0]
        gerar_imagem(url)
        legenda = gerar_legenda(url)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("produto.png", "rb"), caption=legenda)
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Erro: {e}")

# Crie o bot
def main():
    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(CommandHandler("produto", produto))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
