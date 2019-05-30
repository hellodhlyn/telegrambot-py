from telegrambot import Bot

bot = Bot('your_bot_token')


@bot.command("/ping")
def ping(ctx):
    return 'pong'


if __name__ == '__main__':
    bot.start()
