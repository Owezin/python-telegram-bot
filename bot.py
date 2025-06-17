import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

# Configurações do bot
TOKEN = "8098294615:AAERsoEDOpj7WC-EdLZ9CMMoSzw9BusPFgk"

# Função para gerar imagem do produto
async def gerar_imagem(url):
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
        return "produto.png"
    except Exception as e:
        print(f"Erro ao gerar imagem: {e}")

# Função para gerar legenda do produto
async def gerar_legenda(url):
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
async def produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = context.args[0]
        imagem = await gerar_imagem(url)
        legenda = await gerar_legenda(url)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(imagem, "rb"), caption=legenda)
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Erro: {e}")

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("produto", produto))
    application.run_polling()

if __name__ == "__main__":
    main()
