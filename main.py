import os
import logging
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from flask import Flask
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "SEU_TOKEN_AQUI"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot está online!"

async def gerar_imagem(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        nome_produto = soup.find("h1", class_="nome-produto").text
        preco_produto = soup.find("span", class_="preco-produto").text
        imagem_produto = soup.find("img", class_="imagem-produto")["src"]
        img = Image.open(requests.get(imagem_produto, stream=True).raw)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 24)
        draw.text((10, 10), nome_produto, font=font)
        draw.text((10, 40), preco_produto, font=font)
        img.save("produto.png")
        return "produto.png"
    except Exception as e:
        print(f"Erro ao gerar imagem: {e}")

async def gerar_legenda(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        nome_produto = soup.find("h1", class_="nome-produto").text
        preco_produto = soup.find("span", class_="preco-produto").text
        legenda = f"🚨 PROMOÇÃO! 🚨\n{nome_produto}\nPreço: {preco_produto}"
        return legenda
    except Exception as e:
        print(f"Erro ao gerar legenda: {e}")
        return "Erro ao gerar legenda"

async def produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = context.args[0]
        imagem = await gerar_imagem(url)
        legenda = await gerar_legenda(url)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(imagem, 'rb'), caption=legenda)
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Erro: {e}")

def start_bot():
    app_telegram = ApplicationBuilder().token(TOKEN).build()
    app_telegram.add_handler(CommandHandler("produto", produto))
    app_telegram.run_polling()

if __name__ == '__main__':
    threading.Thread(target=start_bot).start()
    app.run(host='0.0.0.0', port=8080)
