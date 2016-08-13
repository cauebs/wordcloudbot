import os, logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from wordcloud import WordCloud
from PIL import Image

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

TOKEN = os.environ.get('TOKEN')
APPNAME = os.environ.get('APPNAME')
PORT = int(os.environ.get('PORT', '5000'))
updater = Updater(TOKEN)
updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
updater.bot.setWebhook("https://"+APPNAME+".herokuapp.com/"+TOKEN)

words = {}

def handle_message(bot, update):
	cid = update.message.chat.id
	txt = update.message.text
	
	if cid in words:
		words[cid] = ''

	words[cid] += txt + ' '

def wordcloud(bot, update):
	cid = update.message.chat.id
	wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(words[cid])
	image = wordcloud.to_image()
	image.save("/tmp/"+str(cid)+".png", "PNG")
	with open("/tmp/"+str(cid)+".png", 'rb') as photo:
		bot.sendPhoto(chat_id=cid, photo=photo)

updater.dispatcher.add_handler(CommandHandler('wordcloud', wordcloud))
updater.dispatcher.add_handler(MessageHandler([Filters.text], handle_message))
updater.idle()