import discord
import os
import mysql.connector

client = discord.Client()  # 接続に使用するオブジェクト

db = mysql.connector.connect(host='localhost', user='root',
                             passwd=os.environ['MYSQL_PASSWORD'],
                             database='19fuckyou_schedule')
cur = db.cursor()

add_flag = 0
search_flag = 0
year = ""
month = ""
day = ""
date = ""
event = ""
place = ""


@client.event
async def on_ready():
    """起動時に通知してくれる処理"""
    print('ログインしました')
    print(client.user.name)  # ボットの名前
    print(client.user.id)  # ボットのID
    print(discord.__version__)  # discord.pyのバージョン
    print('------')


@client.event
async def on_message(message):
    global add_flag
    global cur
    global year
    global month
    global day
    global date
    global event
    global place

    """メッセージを処理"""
    if message.author.bot:  # ボットのメッセージをハネる
        return

    if message.content == "!add":
        # チャンネルへメッセージを送信
        # f文字列（フォーマット済み文字列リテラル）
        add_flag = 1
        await message.channel.send("何時に予定？ 例: 2021:08:01")

    elif add_flag == 1:
        date = message.content.split(':')
        if(date[0].isdigit()):
            year = date[0]
        else:
            add_flag = 0
            await message.channel.send("日付を打て! !addからやり直し")
        if(date[1].isdigit()):
            month = date[1]
        else:
            add_flag = 0
            await message.channel.send("日付を打て! !addからやり直し")
        if(date[2].isdigit()):
            day = date[2]
        else:
            add_flag = 0
            await message.channel.send("日付を打て! !addからやり直し")
        date = year + '-' + month + '-' + day
        await message.channel.send(year + "年" + month + "月" + day + "日で登録します")
        await message.channel.send("なんの予定？ 例: 線形代数のテスト")
        add_flag = 2

    elif add_flag == 2:
        event = message.content
        await message.channel.send(message.content + "で登録します")
        await message.channel.send("どこで？ 例: 大学")
        add_flag = 3

    elif add_flag == 3:
        place = message.content
        cur.execute("INSERT INTO event VALUES (%s, %s, %s, %s)",
                    (str(message.author.id), date, event, place))
        db.commit()
        await message.channel.send(year + "年" + month + "月" + day + "日" + "に" + event + "が" + place + "で行われます!")
        await message.channel.send("登録完了!")
        add_flag = 0

    elif message.content == "!event":
        # ダイレクトメッセージ送信
        cur.execute("SELECT * FROM event WHERE user=%s ORDER BY date",
                    (str(message.author.id),))
        rows = cur.fetchall()
        for row in rows:
            year = str(row[1].year)
            month = str(row[1].month)
            day = str(row[1].day)
            await message.channel.send(month + "月" + day + "日" + " " + row[2] + " " + row[3])

# botの接続と起動
# （botアカウントのアクセストークンを入れてください）
client.run(os.environ['DISCORD_TOKEN'])
