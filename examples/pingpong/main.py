from telegrambot import Bot

bot = Bot('your_bot_token')


@bot.command('/ping {name}')
def ping(ctx, name):
    return "Hello, {}!".format(name)


@bot.error_handler()
def handle_error(err):
    print(err)


if __name__ == '__main__':
    bot.start()
