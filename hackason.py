import discord
import TOKEN

import random
import subprocess

TOKEN = TOKEN.TOKEN

# 接続に必要なオブジェクトを生成
client = discord.Client()


imageList = subprocess.check_output("ls ~/hackason/images/",shell=True).decode().replace("/", " ").split()
numOfImages = len(imageList)-1

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    elif message.content == "animal":
        radomInt = random.randint(0,numOfImages)
        await message.channel.send(file = discord.File("images/"+imageList[radomInt]))
    #elif [client in message.mentions]:
    #    subprocess.run("wget "+message.jump_url, shell= True)
    #    subprocess.run("cp *.png *.jpeg images/", shell=True)

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('Connected to Discord')
    print(discord.__version__)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)