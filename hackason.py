import discord
from discord import channel
import TOKEN

import random
import subprocess
import os

TOKEN = TOKEN.TOKEN

# 接続に必要なオブジェクトを生成
client = discord.Client()


#imageList = subprocess.check_output("ls ~/hackason/images/",shell=True).decode().replace("/", " ").split()
#numOfImages = len(imageList)-1

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    channel = message.channel

    if message.content.startswith("animal"):
        
        messageList = message.content.split()
        if len(messageList) == 1:
            messageList.append("")
        imageList = subprocess.check_output("ls ~/hackason/images/"+messageList[1],shell=True).decode().replace("/", " ").split()

        numOfImages = len(imageList)-1
        radomInt = random.randint(0,numOfImages)


        try:
            await channel.send(file = discord.File("images/"+messageList[1]+"/"+imageList[radomInt]))
        except FileNotFoundError as e:
            await channel.send("指定したフォルダは存在しません")

    if message.content.startswith("/upload"):
        messageList = message.content.split()
        try:
            attachment = message.attachments[0]
            await attachment.save(attachment.filename)
            if len(messageList) != 1:
                messageList.append("")
            if not os.path.isdir(messageList[1]):
                subprocess.run("mkdir images/"+messageList[1],shell=True)
            subprocess.run("mv "+attachment.filename+" images/"+messageList[1], shell=True)
            await channel.send(attachment.filename+"を保存しました")

        except IndexError as identifier:
            await channel.send("画像をアップロードしてください")

    #if message.content.startswith("/move"):
    #    messageList = message.content.split()
    #    if len(messageList) <= 2:
    #        await channel.send("/move 移動させたいファイルのファイル名 移動先")

        # 移動先がない場合
    #    if not os.path.isdir(messageList[2]):
    #        subprocess.run("mkdir images/"+messageList[2],shell=True)

        # 移動させたいファイルがない場合
    #    if not os.path.isfile(messageList[1]):
    #        await channel.send("指定したファイルは存在しません")

    #elif [client in message.mentions]:
    #    subprocess.run("wget "+message.jump_url, shell= True)
    #    subprocess.run("cp *.png *.jpeg images/", shell=True)

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('Connected to Discord')
    print(discord.__version__)
    guilds = client.guilds

    #for guild in guilds:
    #    await guild.system_channel.send("画像を見るときは\'animal (カテゴリ名)\'()内は省略可能")
    #    await guild.system_channel.send("画像をアップロードするときは\'/upload (カテゴリ名)\'()内は省略可能")

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)