#IMPORTANT: Not compatible with Python 3.7, must use Python 3.6 or below!!!
#Dependencies: discord.py API, PyDictionary, youtube_dl, discord.py[voice]

#Type @help in Discord chat for list of commands

import discord
import random
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
from PyDictionary import PyDictionary as PyDict
import time
from datetime import datetime
import math

TOKEN = "NTY0NTA0NTI0MjgzNDQ1MjQ4.XKo7RQ.FfRfJOUyoCk1JuV90htORUQ_XBg"
clientBot = Bot('@')
clientBot.remove_command('help')

pydict = PyDict()
players = {}

#Bot event handlers
@clientBot.event 
async def on_ready():   #signals successful connection
    print("Logged in as")
    print(clientBot.user.name)
    print(clientBot.user.id)
    
@clientBot.event
async def on_message(message):
    content = message.content
    channel = message.channel
    author = message.author
 
    await clientBot.process_commands(message)   #Overriding default on_message method prohibits execution of other commands; this line corrects that
    
###Bot Commands###
@clientBot.command(pass_context = True)
#Help section lists commands (@Help)
async def help(context):
    author = context.message.author
    channel = context.message.channel
    
    embed = discord.Embed(color = discord.Color.orange())
    embed.set_author(name = "Help Section")
    embed.add_field(name = "Hello", value = "Command: @hello \n Signals a greeting", inline = False)
    embed.add_field(name = "Say", value = "Command: @say <words> \n Repeat after the user", inline = False)
    embed.add_field(name = "Clear", value = "Command: @clear <amount> \n Clear messages from chat log \n NOTE: Bot must be given permissions in settings for command to work", inline = False)
    embed.add_field(name = "8ball", value = "Command: @8ball \n Use bot as a magic eight ball", inline = False)
    embed.add_field(name = "Hangman", value  = "Command: @hangman \n Start a game of hangman", inline = False)
    embed.add_field(name = "Square", value = "Command: @square <value> \n Calculates the square of the value given", inline = False)
    embed.add_field(name = "Root", value = "Command: @root <value> \n Calculates the square root of the value given", inline = False)
    embed.add_field(name = "Define", value = "Command: @define <word> \n Bot gives the definition of a given word", inline = False)
    embed.add_field(name = "Remind", value = "Command: @remind <time> <message> \n Schedules a reminder to be private messaged to a user (NOTE: Time based on 24-hour clock)\n Example: @remind 13:12 Buy eggs ", inline = True)
    embed.add_field(name = "PlayVideo", value = "Command: @playVideo <ur;> \n Connects bot to open voice channel and opens youtube video url in chat \nPlease make sure voice channel is connected so the bot may join it", inline = False)
    embed.add_field(name = "Logout", value = "Command: @logout \n Tells bot to log out", inline = False)

    await clientBot.send_message(channel, embed = embed)
    
@clientBot.command(pass_context = True)
#greet user
async def hello(context):
    author = context.message.author
    await clientBot.say("Hello " + author.mention)

@clientBot.command(pass_context = True)
#repeat after user
##currently only takes first word as argument
async def say(context, msg):
    author = context.message.author
    content = str(msg)
    
    await clientBot.say(content)
    
    
@clientBot.command(pass_context = True)
#Clear amount of channel messages
##Must give bot permissions in server settings
async def clear(context, amount):
    channel = context.message.channel
    messages = []
    async for message in clientBot.logs_from(channel, limit = int(amount)):
        messages.append(message)
    await clientBot.delete_messages(messages)
    
@clientBot.command(name='8ball', aliases=['eight-ball', '8-ball'], pass_context = True)
#Responds as a magic eight ball
async def eight_ball(context):
    try:
        responses = ["Definitely not", "Not Likely", "No", "It is hard to say", "Maybe...", "I don't know. Ask me another time", "It's possible", "As far as I can tell, yes", "Absolutely, yes"]
    
        eightBallEmoji = ":8ball:"
        await clientBot.say(eightBallEmoji * 3 + "\nAsk me a yes or no question. I'll try to give a helpful answer\n" + eightBallEmoji * 3)
    
        msg = await clientBot.wait_for_message(timeout = 60)
        if msg:
            await clientBot.say(random.choice(responses))
        elif msg is None:
            await clientBot.say("You never asked your question. Maybe another time")
    except:
        await clientBot.say("Something went wrong...")
        
@clientBot.command(pass_context = True)
#Begins a simple game of hangman
##Bug in win case still persists!!
async def hangman(context):
    await clientBot.say("Alright! Let's play a round :grinning:")
    
    words = ['recursion', 'multiprocesser', 'motherboard', 'software', 'python', 'database', 'constructor', 'variable', 'module', 'library']
    word = random.choice(words)
    
    playing = True
    seenLetters = ""
    chances = len(word) + 2
    correctGuess = 0

    await clientBot.say("- " * len(word) + "\tChances: " + str(chances))
    try:
        while(chances != 0):
            await clientBot.say("Enter a letter: ")
            msg = await clientBot.wait_for_message()
            if msg:
                userLetter = str(msg.content)

                if len(userLetter) > 1:
                    await clientBot.say("You entered too many characters")
                    continue
                elif userLetter in seenLetters:
                    await clientBot.say("You have already guessed that")
                    continue
                
                if userLetter in word:
                    seenLetters += userLetter
                    correctGuess += 1
                else:
                    chances -= 1

                printStr = " "
                for ch in word:
                    if ch in seenLetters:
                        printStr += ch
                    else:
                        printStr += "-"
                await clientBot.say(printStr + "\tChances: " + str(chances))

                if seenLetters == word: ##FIX!!
                    await clientBot.say("You win!")
                    return
                
        if chances == 0:
            await clientBot.say(":disappointed: You lose! Word: {}".format(word))
            return
    except KeyboardInterrupt:
        await clientBot.say("Okay, another time")
                
@clientBot.command(pass_context = True)
#Gives square of a number
async def square(context, number):
    try:
        coercedFloatNum = float(number)
        coercedIntNum = int(coercedFloatNum)
        squaredVal = coercedIntNum * coercedIntNum
        await clientBot.say(str(number) + " squared is approx " + str(squaredVal))
    except:
        await clientBot.say("I don't think that was a number")
        
@clientBot.command(pass_context = True)
#Gives square root of a number
async def root(context, number):
    try:
        coercedFloatNum = float(number)
        coercedIntNum = int(coercedFloatNum)
        rootVal = math.sqrt(coercedIntNum)
        await clientBot.say("The square root of " + str(number) + " is approx " + str(rootVal))
    except:
        await clientBot.say("I don't think that was a number")
        
@clientBot.command(pass_context = True)
#Gives definition of user-provided word 
async def define(context, word):
    try:
        userWord = str(word)
        definition = pydict.meaning(userWord)
        await clientBot.say(definition)
    except:
        await clientBot.say("Sorry, I couldn't find what you were looking for \n :thinking:")
        
@clientBot.command(pass_context = True)
#Allows user to schedule a reminder
##Currently can only schedule 1 reminder at a time; Currently only takes first word as argument
async def remind(context, userTime, msg):
    author = context.message.author
    
    currTime = datetime.now()
    remindTime = datetime.combine(datetime.now(), datetime.strptime(userTime, "%H:%M").time())
    if remindTime <= currTime:
        diff = currTime - remindTime
    else:
        diff = remindTime - currTime
        
    try:
        await clientBot.wait_until_ready()
        while not clientBot.is_closed:
            await clientBot.say("I've got your reminder scheduled!")
            await asyncio.sleep(int(diff.seconds))
            await clientBot.send_message(author, "Here's your reminder:")
            await clientBot.send_message(author, msg)
            break
    except:
        await clientBot.say("Something went wrong with scheduling your reminder")
  
@clientBot.command(name = 'playVideo', pass_context = True)
#Opens youtube video url in chat
###PyNaCL error still persists!!
async def play_video(context, url):
    author = context.message.author
    channel = author.voice_channel
    server = context.message.server
    
    if(clientBot.is_voice_connected(server)):
        await voice.disconnect()
        await asyncio.sleep(1)
        voiceClient = await clientBot.join_voice_channel(channel)
    else:
        voiceClient = await clientBot.join_voice_channel(channel)

    player = await voiceClient.create_ytdl_player(url)
    players[server.id] = player
    player.start()
    
@clientBot.command()
#logs out bot
async def logout():
    await clientBot.say("Logging out...\nGoodbye")
    await clientBot.logout()
    
#Tells client which bot is being used; login of bot
clientBot.run(TOKEN)
