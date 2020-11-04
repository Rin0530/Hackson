from os import rename
import discord
from discord import channel
import TOKEN

import random
import subprocess
import os
import pathlib
import shutil

TOKEN = TOKEN.TOKEN

# 接続に必要なオブジェクトを生成
client = discord.Client()

# imagesのパス
images = "images"

#imageList = subprocess.check_output("ls ~/hackason/images/",shell=True).decode().replace("/", " ").split()
#numOfImages = len(imageList)-1

# 後のファイル名を決定
def decide_filename(category, extension):
    print("変数images:" + images)
    print("変数category:"+category)
    imageList = subprocess.check_output(
        "ls ./"+images+"/" + category, shell=True).decode().replace("/", " ").split()
    num = len(imageList)
    after_path = images+"/"+category+"/" + \
        category+"_"+str(num)+extension
    return after_path

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    global images

    images = "images"

    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    images += "/"+str(message.author.id)

    channel = message.channel

    if message.content.startswith("animal"):
        
        messageList = message.content.split()
        if len(messageList) == 1:
            await channel.send("カテゴリを指定してください")
            return
        imageList = subprocess.check_output("ls "+images+"/"+messageList[1],shell=True).decode().replace("/", " ").split()

        numOfImages = len(imageList)-1
        radomInt = random.randint(0,numOfImages)


        try:
            await channel.send(file = discord.File(images+"/"+messageList[1]+"/"+imageList[radomInt]))
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
                os.makedirs(images+"/"+messageList[1],exist_ok=True)
            # subprocess.run("mv "+attachment.filename+" images/"+messageList[1], shell=True)
            #拡張子を取得
            extension = os.path.splitext(attachment.filename)
            #画像をカテゴリのフォルダ下に移動
            aftername =decide_filename(messageList[1],extension[1])
            shutil.move(attachment.filename, aftername)
            await channel.send(aftername.rsplit("/",1)[1]+"を保存しました")

        except IndexError as identifier:
            await channel.send("画像をアップロードしてください")

    if message.content.startswith("/move"):
        messageList = message.content.split()
        if messageList[2].startswith(".") or messageList[2].startswith("~"):
            await channel.send("移動先にはカテゴリ名を指定してください")
            return
        if len(messageList) <= 2:
            await channel.send("/move 移動させたいファイルのファイル名 移動先")

        # 移動させたいファイル、移動先ディレクトリの各Pathオブジェクトを取得
        imagesPath = pathlib.Path(images)
        filePaths =imagesPath.glob("**/*"+messageList[1])
        filePath = None
        try:
            filePath = list(filePaths)[0]
        except IndexError as identifier:
            await channel.send("指定したファイルは存在しません")
            return
        
        dirPath = images+"/"+messageList[2]

       # 移動先がない場合
        if not os.path.isdir(dirPath):
            #subprocess.run("mkdir images/"+messageList[2],shell=True)
            os.makedirs(images+"/"+messageList[2],exist_ok=True)

       # 移動させたいファイルがない場合
        if not filePath.exists():
            await channel.send("指定したファイルは存在しません")
            return

        # 移動

        try:
            extension = os.path.splitext(messageList[1])
            aftername = str(filePath).rsplit("/") #抜けたファイル名
            shutil.move(str(filePath), decide_filename(messageList[2], extension[1]))
            files = os.listdir(images+"/"+aftername[2])
            file = None
            for f in files:
                if str(len(files)) in str(f):
                    file = f
                    break
            print(str(file))
            os.rename(images+"/"+aftername[2]+"/"+file, images+"/"+aftername[2]+"/"+aftername[3])


        except shutil.Error as identifier:
            await channel.send("移動先と現在ファイルが存在するディレクトリが同一です。")

    if message.content.startswith("list"):
        messageList = message.content.split()
        if len(messageList) != 1:
            if messageList[1].startswith(".") or messageList[1].startswith("~"):
                await channel.send("閲覧先にはカテゴリ名を指定してください")
                return
        # カテゴリ指定のない場合
        if len(messageList) == 1:
            default_imageList = subprocess.check_output(
                "ls ./"+images, shell=True).decode().replace("/", " ").split()
            for tmp in default_imageList:
                await channel.send(tmp)
            return

        #カテゴリ指定あり
        category = messageList[1]       
        if "." in category or "/" in category:
            await channel.send("カテゴリのみをにゅうりょくしてください")
            return
        if not os.path.isdir("./"+images+"/"+category):
            await channel.send("カテゴリないよ？")
            return
        imageList = subprocess.check_output(
            "ls ./"+images+"/"+category, shell=True).decode().replace("/", " ").split()
        for tmp in imageList:
            images = "images"
            images += "/"+str(message.author.id)
            await channel.send(file = discord.File(images+"/"+category+"/"+tmp))
            await channel.send("↑" + tmp)
            
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