# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import matplotlib.pyplot as plt
import discord
import os
import asyncio
import random
import time
from flask import Flask
from threading import Thread
import ast


app = Flask('')

@app.route('/')
def home():
    return "I'm alive"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.default()
intents.members = True
  
client = discord.Client(intents=intents)

class Player:
    def __init__(self, id, name, team, liq, red, reh, blue, blh, green, grh,
                 yellow, yeh, histbal):
        self.id = id
        self.name = name
        self.team = team
        self.liq = liq #cash on hand
        self.red = red
        self.reh = reh #red history
        self.blue = blue
        self.blh = blh
        self.green = green
        self.grh = grh
        self.yellow = yellow
        self.yeh = yeh
        self.histbal = histbal


o = open("info.txt")
r = o.readlines()

if r == []:
    print("Empty")
    re = 100
    bl = 100
    gr = 100
    ye = 100
    rey = [100]
    bly = [100]
    gry = [100]
    yey = [100]
    xval = 0
    xvals = [0]
    players = []
    oakville = []
    milton = []
    china = []
else:
    lines = []
    for line in r:
        line = line.strip()
        lines.append(line)
    re = float(lines[0])
    bl = float(lines[1])
    gr = float(lines[2])
    ye = float(lines[3])
    rey = ast.literal_eval(lines[4])
    bly = ast.literal_eval(lines[5])
    gry = ast.literal_eval(lines[6])
    yey = ast.literal_eval(lines[7])
    xval = int(lines[8])
    xvals = ast.literal_eval(lines[9])
    oakville = ast.literal_eval(lines[10])
    milton = ast.literal_eval(lines[11])
    china = ast.literal_eval(lines[12])
    players = []
    playerss = ast.literal_eval(lines[13])
    for i in playerss:
        players.append(
            Player(str(i[0]), str(i[1]), str(i[2]), float(i[3]), int(i[4]),
                   float(i[5]), int(i[6]), float(i[7]), int(i[8]), float(i[9]),
                   int(i[10]), float(i[11]), i[12].split(";")))
print(players)

l = {"🔴": re, "🔵": bl, "🟢": gr, "🟡": ye}

admins = [795820947378405436]
times = [0, 1, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

timer = 60
timeron = False
started = False

def autosave():
    o = open("info.txt", "w")
    write = str(l["🔴"]) + "\n" + str(l["🔵"]) + "\n" + str(l["🟢"]) + "\n" + str(
        l["🟡"]) + "\n" + str(rey) + "\n" + str(bly) + "\n" + str(
            gry) + "\n" + str(yey) + "\n" + str(xval) + "\n" + str(
                xvals) + "\n" + str(oakville) + "\n" + str(
                    milton) + "\n" + str(china) + "\n"
    allplayers = []
    for i in players:
        plist = []
        for n in (i.id, i.name, i.team, i.liq, i.red, i.reh, i.blue, i.blh,
                  i.green, i.grh, i.yellow, i.yeh, ";".join(str(num) for num in i.histbal)):
            plist.append(n)
        allplayers.append(plist)
    write = write + str(allplayers)
    o.write(write)
    o.close()
  
def getnw(i):
  r = i.liq + i.red * l["🔴"] + i.blue * l["🔵"] + i.green * l["🟢"] + i.yellow * l["🟡"]
  return(round(r, 2))

def update():
    for i in l:
      l[i] *= 1 + random.uniform(0, 5.912621)/100 - 0.02912621
    global xval
    global xvals
    xval = xval + 1
    xvals.append(xval)
    rey.append(l["🔴"])
    bly.append(l["🔵"])
    gry.append(l["🟢"])
    yey.append(l["🟡"])
    mtotal = 0
    ototal = 0
    ctotal = 0
    for i in players:
        i.histbal.append(str(getnw(i)))
        if i.team == "milton":
            mtotal = mtotal + i.liq + i.red * l["🔴"] + i.blue * l[
                "🔵"] + i.green * l["🟢"] + i.yellow * l["🟡"]
        elif i.team == "oakville":
            ototal = ototal + i.liq + i.red * l["🔴"] + i.blue * l[
                "🔵"] + i.green * l["🟢"] + i.yellow * l["🟡"]
        elif i.team == "china":
            ctotal = ctotal + i.liq + i.red * l["🔴"] + i.blue * l[
                "🔵"] + i.green * l["🟢"] + i.yellow * l["🟡"]
    china.append(ctotal)
    milton.append(mtotal)
    oakville.append(ototal)


def graph(num):
    global plt
    reys = []
    blys = []
    grys = []
    yeys = []
    xvalss = []
    for i in range(-num, 0):
        reys.append(rey[i])
        blys.append(bly[i])
        grys.append(gry[i])
        yeys.append(yey[i])
        xvalss.append(xvals[i])
    plt.plot(xvalss, reys, label="red", color="red")
    plt.plot(xvalss, blys, label="blue", color="blue")
    plt.plot(xvalss, grys, label="green", color="green")
    plt.plot(xvalss, yeys, label="yellow", color="#FFD800")


def teamgraph(num):
    miltons = []
    oakvilles = []
    chinas = []
    xvalss = []
    for i in range(-num, 0):
        miltons.append(milton[i])
        oakvilles.append(oakville[i])
        chinas.append(china[i])
        xvalss.append(xvals[i])
    plt.plot(xvalss, oakvilles, label="Oakville", color="#26A4FF")
    plt.plot(xvalss, miltons, label="Milton", color="#A2E200")
    plt.plot(xvalss, chinas, label="China", color="#DF2407")


def leaderboard():
    lb = {}
    for i in players:
        nw = i.liq + i.red * l["🔴"] + i.blue * l["🔵"] + i.green * l[
            "🟢"] + i.yellow * l["🟡"]
        nw = round(nw, 2)
        lb[i.name] = nw
    lb = sorted(lb.items(), key=lambda x: x[1], reverse=True)
    lb = dict(lb)
    return (lb)

def graphnw(num, player):
  z = [float(zz) for zz in player.histbal[-num:]]
  x = xvals[-num:]
  plt.plot(x, z, label=player.name, color="#727272")
  plt.savefig("graphie.png")
  plt.close()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('0prices'):
        global timer
        global timeron
        if timeron:
            k = str(timer) + " seconds until next update\n"
        else:
            k = ""
        for j in l:
            k = k + j + " " + str(round(l[j], 2)) + "\n"
        await message.channel.send(k)

    if message.content.startswith('0start'):
        global started
        global richest
        if !started:
            print(time.localtime().tm_hour)
            if time.localtime().tm_hour in times:
                await message.channel.send("Starting Market!")
                while time.localtime().tm_hour in times:
                    started = True
                    update()
                    autosave()
                    k = ""
                    for j in l:
                        k = k + j + " " + str(l[j]) + "\n"
                    print(xval)
                    print(k)
                    timeron = True
                    timer = 60
                    while timer > 0:
                        await asyncio.sleep(1)
                        timer = timer - 1
                await message.channel.send("Market has closed")
                started = False
                timeron = False

            else:
                await message.channel.send(
                    "Market not open! Market times are from 8 am to 10 pm!")

        else:
            await message.channel.send(
                "Market already started!")

    if message.content.startswith('0save'):
        autosave()

    if message.content.startswith('0help'):
        await message.channel.send(
            "__Command List__:\n*replace everything in and including the <> when doing commands, anything with (optional) is not needed*\n\n0buy <emoji representing stock> <amount or max>\n0sell <emoji representing stock> <amount of max>\n0bal <user (optional)>\n0graph <number (optional)>\n0prices\n0top\n0teams <number(optional)>\n0start `only works between 8 am and 10 pm (market times)`"
        )

    if message.content.startswith('0plot'):
        global rey, bly, gry, yey
        hehe = message.content.split(" ")
        if hehe[-1].isdigit() == False:
            hehe.append(xval)
        else:
            hehe[-1] = int(hehe[-1])
        z = ""
        for i in range(len(hehe) - 2):
            i = i + 1
            z = z + hehe[i]
        xvalss = []
        for i in range(-hehe[-1], 0):
            xvalss.append(xvals[i])
        if '🔴' in z:
            reys = []
            for i in range(-hehe[-1], 0):
                reys.append(rey[i])
            plt.plot(xvalss, reys, label="red", color="red")
        if '🔵' in z:
            blys = []
            for i in range(-hehe[-1], 0):
                blys.append(bly[i])
            plt.plot(xvalss, blys, label="blue", color="blue")
        if '🟢' in z:
            grys = []
            for i in range(-hehe[-1], 0):
                grys.append(gry[i])
            plt.plot(xvalss, grys, label="green", color="green")
        if '🟡' in z:
            yeys = []
            for i in range(-hehe[-1], 0):
                yeys.append(yey[i])
            plt.plot(xvalss, yeys, label="yellow", color="#FFD800")
        plt.savefig("graphie.png")
        plt.close()
        await message.channel.send("Graphing " + z,
                                   file=discord.File("graphie.png"))

    if message.content.startswith('0monitor'):
        if message.author.id in admins:
            await message.channel.send("Monitoring!")
            c = 0
            while True:
                if timer == 60:
                    c += 1
                    k = ""
                    for j in l:
                        k = k + j + " " + str(round(l[j], 2)) + "\n"
                    await message.channel.send(k)
                if c == 5:
                  graph(xval)
                  plt.savefig("graph.png")
                  plt.close()
                  await message.channel.send("Graph image as of " + str(xval), file=discord.File("graph.png"))
                  c = 0

    if message.content.startswith('0graph'):
        proceed = False
        list1 = message.content.split(" ")
        if len(list1) == 1:
            graph(xval)
            proceed = True
        elif int(list1[-1]) > xval:
            await message.channel.send(
                "That many values don't exist")
            proceed = False
        elif int(list1[-1]) <= 0:
            await message.channel.send(
                "How do you even go about thinking this is possible")
            proceed = False
        elif int(list1[-1]) == 1:
            await message.channel.send("Enter in a value greater than 1!")
            proceed = False
        else:
            graph(int(list1[-1]))
            proceed = True
        if proceed == True:
            plt.savefig("graph.png")
            plt.close()  # Close the matplotlib figure to free up memory
            await message.channel.send("Graph image as of " + str(xval),
                                       file=discord.File("graph.png"))

    if message.content.startswith('0teams'):
        proceed = False
        list1 = message.content.split(" ")
        if len(list1) == 1:
            teamgraph(xval)
            proceed = True
        elif int(list1[1]) > xval:
            await message.channel.send(
                "That many values don't exist!")
            proceed = False
        elif int(list1[1]) <= 0:
            await message.channel.send(
                "How do you even go about thinking this is possible")
            proceed = False
        elif int(list1[1]) == 1:
            await message.channel.send("Enter in a value greater than 1!")
            proceed = False
        else:
            teamgraph(int(list1[1]))
            proceed = True
        if proceed == True:
            plt.savefig("teamgraph.png")
            plt.close()  # Close the matplotlib figure to free up memory

            try:
                await message.channel.send(
                    "Oakville: $" + str(round(oakville[-1], 2)) +
                    "\nMilton: $" + str(round(milton[-1], 2)) + "\nChina: $" +
                    str(round(china[-1], 2)),
                    file=discord.File("teamgraph.png"))
            except Exception as e:
                print(f"Error sending graph image: {e}")

    if message.content.startswith('0track'):
        for i in players:
            if i.name == message.author.name:
                content = message.content.split(" ")
                if len(content) == 1:
                  graphnw(len(i.histbal), i)
                  t = [round(float(j), 2) for j in i.histbal]
                  await message.channel.send("Your peak networth: **${}**\nYour lowest networth: **${}**\nYour current networth: **${}**\n\n**Below is your networth graphed over time**".format(max(t), min(t), getnw(i)), file=discord.File("graphie.png"))
                else:
                  try:
                    graphnw(int(content[-1]), i)
                    t = [round(float(j), 2) for j in i.histbal[-int(content[-1]):]]
                    await message.channel.send("Your peak networth: **${}**\nYour lowest networth: **${}**\nYour current networth: **${}**\n*Values are for the time period you requested*\n\n**Below is your networth graphed over time**".format(max(t), min(t), getnw(i)), file=discord.File("graphie.png"))
                  except:
                    await message.channel.send("that's not an integer buddy")
      
    if message.content.startswith('0register '):
        proceed = True
        if message.author.id in admins:
            list1 = message.content.split(" ")
            list1[1] = list1[1].strip("<@>")
            for i in players:
                if i.id == list1[1]:
                    await message.channel.send("This user already exists!")
                    proceed = False
            if proceed:
                username = str(client.get_user(int(list1[1])))
                username = username.split("#")[0]
                if len(list1) == 3:
                    players.append(
                        Player(list1[1], username, str(list1[2]), 10000, 0, 0,
                               0, 0, 0, 0, 0, 0, [10000]))
                elif len(list1) == 2:
                    players.append(
                        Player(list1[1], username, " ", 10000, 0, 0, 0, 0, 0,
                               0, 0, 0, [10000]))
                await message.channel.send('yes master')
                autosave()
        else:
            await message.channel.send('suck it')

    if message.content.startswith('0remove '):
        proceed = False
        if message.author.id in admins:
            list1 = message.content.split(" ")
            list1[1] = list1[1].strip("<@>")
            for i in players:
                if i.id == list1[1]:
                    players.remove(i)
                    await message.channel.send("removed the goofy goober")
                    autosave()
                    proceed = True
            if !proceed:
                await message.channel.send("This user doesn't exist!")
        else:
            await message.channel.send('suck it')

    if message.content.startswith('0buy'):
        list1 = message.content.split(" ")
        if len(list1) != 3:
            await message.channel.send(
                "Expected 2 arguments in the form of `0buy <emoji representing stock> <number>`\nRemember to have only one space between the emoji and the number"
            )
        for i in players:
            if int(i.id) == int(message.author.id):
                if list1[2] == "max":
                    list1[2] = int(i.liq / l[list1[1]])
                else:
                    list1[2] = int(list1[2])
                if list1[2] > 0:
                    if list1[1] in l:
                        if l[list1[1]] * list1[2] > i.liq:
                            await message.channel.send("You don't have enough money to complete this purchase")
                        else:
                            i.liq = i.liq - l[list1[1]] * list1[2]
                            i.liq = float(round(i.liq, 2))
                            if list1[1] == "🔴":
                                purchase = i.red + list1[2]
                                i.red = purchase
                                i.reh = i.reh + l[list1[1]] * list1[2]
                            elif list1[1] == "🔵":
                                purchase = i.blue + list1[2]
                                i.blue = purchase
                                i.blh = i.blh + l[list1[1]] * list1[2]
                            elif list1[1] == "🟢":
                                purchase = i.green + list1[2]
                                i.green = purchase
                                i.grh = i.grh + l[list1[1]] * list1[2]
                            elif list1[1] == "🟡":
                                purchase = i.yellow + list1[2]
                                i.yellow = purchase
                                i.yeh = i.yeh + l[list1[1]] * list1[2]
                            autosave()
                            msg = ""
                            aaaaa = [
                                "You have bought ",
                                str(list1[2]), " ",
                                str(list1[1]), " for ",
                                str(round(l[list1[1]], 2)),
                                " each. You now have $",
                                str(i.liq), " and ",
                                str(purchase), " ",
                                str(list1[1])
                            ]
                            for aaa in aaaaa:
                                msg = msg + (aaa) #This is inefficient but back then I didn't know about .format() and .join() methods
                            await message.channel.send(msg)

                    else:
                        await message.channel.send("That stock doesn't exist!")
                elif list1[2] < 0:
                    await message.channel.send("You can't buy negative stocks!")
                elif list1[2] == 0:
                    await message.channel.send("Why are you buying 0 shares...")

    if message.content.startswith('0sell'):
        progress = 0
        list1 = message.content.split(" ")
        if len(list1) != 3:
            await message.channel.send(
                "Expected 2 arguments in the form of `0sell <emoji representing stock> <number>`"
            )
        for i in players:
            if int(i.id) == int(message.author.id):
                if list1[2] in ["all", "max"]:
                    if list1[1] == "🔴":
                        list1[2] = i.red
                    elif list1[1] == "🔵":
                        list1[2] = i.blue
                    elif list1[1] == "🟢":
                        list1[2] = i.green
                    elif list1[1] == "🟡":
                        list1[2] = i.yellow
                else:
                    list1[2] = int(list1[2])
                if list1[2] > 0:
                    if list1[1] in l:
                        if list1[1] == "🔴":
                            if i.red < list1[2]:
                                await message.channel.send(
                                    "Nice try, but you don't own that much stock"
                                )
                            else:
                                purchase = i.red - list1[2]
                                i.red = purchase
                                progress = 1
                                if i.red != 0:
                                    i.reh = i.reh - l[list1[1]] * list1[2]
                                else:
                                    i.reh = 0
                        elif list1[1] == "🔵":
                            if i.blue < list1[2]:
                                await message.channel.send(
                                    "Nice try, but you don't own that much stock"
                                )
                            else:
                                purchase = i.blue - list1[2]
                                i.blue = purchase
                                progress = 1
                                if i.blue != 0:
                                    i.blh = i.blh - l[list1[1]] * list1[2]
                                else:
                                    i.blh = 0
                        elif list1[1] == "🟢":
                            if i.green < list1[2]:
                                await message.channel.send(
                                    "Nice try, but you don't own that much stock"
                                )
                            else:
                                purchase = i.green - list1[2]
                                i.green = purchase
                                progress = 1
                                if i.green != 0:
                                    i.grh = i.grh - l[list1[1]] * list1[2]
                                else:
                                    i.grh = 0
                        elif list1[1] == "🟡":
                            if i.yellow < list1[2]:
                                await message.channel.send(
                                    "Nice try, but you don't own that much stock"
                                )
                            else:
                                purchase = i.yellow - list1[2]
                                i.yellow = purchase
                                progress = 1
                                if i.yellow != 0:
                                    i.yeh = i.yeh - l[list1[1]] * list1[2]
                                else:
                                    i.yeh = 0
                        else:
                            await message.channel.send("Not a valid emoji.")
                        if progress == 1:
                            print(i.liq)
                            i.liq = i.liq + l[list1[1]] * list1[2]
                            i.liq = float(round(i.liq, 2))
                            print(i.liq)
                            autosave()
                            msg = ""
                            aaaaa = [
                                "You have sold ",
                                str(list1[2]), " ",
                                str(list1[1]), " for ",
                                str(round(l[list1[1]], 2)),
                                " each. You now have $",
                                str(i.liq), " and ",
                                str(purchase), " ",
                                str(list1[1])
                            ]
                            for aaa in aaaaa:
                                msg = msg + (aaa) #Again, I didn't know about .format() and .join() methods
                            await message.channel.send(msg)
                    else:
                        await message.channel.send("That stock doesn't exist!")
                else:
                    await message.channel.send("You can't buy negative stock!")

    if message.content.startswith('0bal'):
        list1 = message.content.split(" ")
        if len(list1) == 1:
            id = message.author.id
        else:
            id = list1[1].strip("<@>")
        for i in players:
            if str(i.id) == str(id):
                networth = getnw(i)
                networth = round(networth, 2)
                msg = "**Balance of: **" + i.name + "\n\nNet worth: $" + str(
                    networth) + "\nLiquidated Cash: $" + str(i.liq)
                if i.red != 0:
                    msg = msg + "\n🔴 " + str(i.red) + " (Value: $" + str(
                        round(i.red * l["🔴"], 2)) + ") **(Bought for: $" + str(
                            round(i.reh, 2)) + ")**"
                if i.blue != 0:
                    msg = msg + "\n🔵 " + str(i.blue) + " (Value: $" + str(
                        round(
                            i.blue * l["🔵"], 2)) + ") **(Bought for: $" + str(
                                round(i.blh, 2)) + ")**"
                if i.green != 0:
                    msg = msg + "\n🟢 " + str(i.green) + " (Value: $" + str(
                        round(
                            i.green * l["🟢"], 2)) + ") **(Bought for: $" + str(
                                round(i.grh, 2)) + ")**"
                if i.yellow != 0:
                    msg = msg + "\n🟡 " + str(i.yellow) + " (Value: $" + str(
                        round(i.yellow * l["🟡"],
                              2)) + ") **(Bought for: $" + str(round(
                                  i.yeh, 2)) + ")**"
                await message.channel.send(msg)
            elif str(i.name) == str(id):
                networth = i.liq + i.red * l["🔴"] + i.blue * l[
                    "🔵"] + i.green * l["🟢"] + i.yellow * l["🟡"]
                networth = round(networth, 2)
                msg = "**Balance of: **" + i.name + "\n\nNet worth: $" + str(
                    networth) + "\nLiquidated Cash: $" + str(i.liq)
                if i.red != 0:
                    msg = msg + "\n🔴 " + str(i.red) + " (Value: $" + str(
                        round(i.red * l["🔴"], 2)) + ") **(Bought for: $" + str(
                            round(i.reh, 2)) + ")**"
                if i.blue != 0:
                    msg = msg + "\n🔵 " + str(i.blue) + " (Value: $" + str(
                        round(
                            i.blue * l["🔵"], 2)) + ") **(Bought for: $" + str(
                                round(i.blh, 2)) + ")**"
                if i.green != 0:
                    msg = msg + "\n🟢 " + str(i.green) + " (Value: $" + str(
                        round(
                            i.green * l["🟢"], 2)) + ") **(Bought for: $" + str(
                                round(i.grh, 2)) + ")**"
                if i.yellow != 0:
                    msg = msg + "\n🟡 " + str(i.yellow) + " (Value: $" + str(
                        round(i.yellow * l["🟡"],
                              2)) + ") **(Bought for: $" + str(round(
                                  i.yeh, 2)) + ")**"
                await message.channel.send(msg)

    if message.content.startswith('0top'):
        msg = ""
        lb = leaderboard()
        print(lb)
        for j in lb:
            for i in players:
                if j == i.name:
                    if i.team == "oakville":
                        msg = msg + "Ⓞ "
                    elif i.team == "milton":
                        msg = msg + "Ⓜ "
                    elif i.team == "china":
                        msg = msg + "🇨🇳 "
            msg = msg + str(j) + " • $" + str(lb[j]) + "\n"
        await message.channel.send(msg)

    if message.content.startswith('0investors '):
        list1 = message.content.split(" ")
        investors = {}
        if list1[1] == "🔴":
            for i in players:
                if i.red != 0:
                    investors[i.name] = i.red
        elif list1[1] == "🔵":
            for i in players:
                if i.blue != 0:
                    investors[i.name] = i.blue
        elif list1[1] == "🟢":
            for i in players:
                if i.green != 0:
                    investors[i.name] = i.green
        elif list1[1] == "🟡":
            for i in players:
                if i.yellow != 0:
                    investors[i.name] = i.yellow
        investors = sorted(investors.items(), key=lambda x: x[1], reverse=True)
        investors = dict(investors)
        msg = "__People who've invested in " + list1[1] + " :__\n\n"
        for i in investors:
            msg = msg + i + " • " + str(investors[i]) + " " + list1[1] + "\n"
        await message.channel.send(msg)

    if message.content.startswith('0reset') or message.content.startswith(
            '0restart'):
        if message.author.id in admins:
            l["🔴"] = 100
            l["🔵"] = 100
            l["🟢"] = 100
            l["🟡"] = 100
            rey = [100]
            bly = [100]
            gry = [100]
            yey = [100]
            for i in players:
                i.liq = 10000
                i.red = 0
                i.reh = 0
                i.blue = 0
                i.blh = 0
                i.green = 0
                i.grh = 0
                i.yellow = 0
                i.yeh = 0
                i.histbal = [10000]
            autosave()
            o = open("info.txt")
            r = o.readlines()
            r[8] = '1\n'
            r[9] = '[]\n'
            r[10] = '[]\n'
            r[11] = '[]\n'
            r[12] = '[]\n'
            o = open("info.txt", "w")
            o.writelines(r)
            o.close()
            await message.channel.send("Restarted game!")
        else:
            await message.channel.send("You don't have permission to restart the game!")

    if message.content.startswith('0diefenbaker'):
        o = open("diefenbaker.txt")
        r = o.readlines()
        dief = 0
        for i in r:
            dief = dief + 1
        diefen = random.randint(0, dief)
        quote = r[diefen].strip()
        quote = "\"" + quote + "\"\n -John G. Diefenbaker"
        await message.channel.send(quote)
    if message.content.startswith('0txt'):
        await message.channel.send("zamn", file=discord.File("info.txt"))


try:
    client.run(os.getenv("TOKEN"))
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e

keep_alive()
