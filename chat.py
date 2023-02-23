import telebot
import openai
import os

# read the api key and bot token from key.txt
with open("key.txt", "r") as f:
    api_key = f.readline().strip()
    bot_token = f.readline().strip()
    bot_name = f.readline().strip()

# initialize OpenAI API client
openai.api_key = api_key

# Setup telegram bot auth
bot = telebot.TeleBot(bot_token)

@bot.message_handler(func=lambda message: message.text.startswith("@" + bot_name))
def generate_gpt(message):
    try:
        if message.chat.type != "private":
        # message was sent in a group, respond to the group
            chat_id = message.chat.id
        else:
        # message was sent in private chat, respond to the sender
            chat_id = message.from_user.id
        prompt_array = message.text.split()[1:]
        if len(prompt_array) < 1:
            bot.send_message(chat_id=chat_id, reply_to_message_id=message.message_id, text="Please provide a prompt after mentioning the bot")
            return
        prompt = prompt_array # get the text after mentioning the bot
        prompt = ' '.join(prompt)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=2048
        )
        response_text = response["choices"][0]["text"]
        if len(response_text) > 3900:
            raise Exception("Message is too big, Telegram doesn't support messages with more than 3900 characters.")
        bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id, text=response_text)
        print(f'\n\n=======================================================================================\n{message.from_user.username} : {prompt} \n\nChatGPT : {response["choices"][0]["text"]}')
    except Exception as e:
        try:
            bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id, text=str(e))
        except Exception as e:
            print(e)

bot.polling()
