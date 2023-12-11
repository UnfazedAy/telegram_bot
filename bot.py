#!/usr/bin/env python3

from scraping import get_product_info
from config import settings
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, CallbackContext
)
from telegram import Update
import logging.config
import pathlib

configfile = pathlib.Path.cwd() / "logging.conf"
logging.config.fileConfig(configfile, disable_existing_loggers=False)

logger = logging.getLogger(__name__)


class MyBot:
    """
    A simple bot that recieves a product link and
    returns a ready made post with an affiliate link
    """
    def __init__(self, token: str):
        logger.info('Initializing bot...')
        self.app = Application.builder().token(token).build()
        self.affiliate_link = None

        # Add handlers
        self.app.add_handler(CommandHandler('start', self.start))
        self.app.add_handler(CommandHandler('set_affiliate_link', self.set_affiliate_link))
        self.app.add_handler(MessageHandler(filters.TEXT, self.generate_post))
        self.app.add_handler(CommandHandler('help', self.help))
        self.app.add_error_handler(self.error)

    async def start(self, update: Update, context: CallbackContext):
        """
        Send a message when the command /start is issued.
        """
        message = 'Welcome! Send me a product link to get an affiliate post.'
        await update.message.reply_text(message)
    
    async def set_affiliate_link(self, update: Update, context: CallbackContext):
        """
        Set the affiliate link for the user
        """
        new_affiliate_link = context.args[0]
        self.affiliate_link = new_affiliate_link
        message = f'Affiliate link set to: {self.affiliate_link}'
        await update.message.reply_text(message)

    async def generate_post(self, update: Update, context: CallbackContext):
        """
        Generate a post with the affiliate link
        """
        if not self.affiliate_link:
            message = 'Affiliate link not set. Use /set_affiliate_link to set it.'
            await update.message.reply_text(message)
            return

        product_link = update.message.text
        product_name, product_price = get_product_info(product_link)

        if product_name and product_price:
            message = f'{product_name}\n{product_price}\n{self.affiliate_link}'
            await update.message.reply_text(message)
        else:
            message = 'Error getting product info.'
            await update.message.reply_text(message)

    async def help(self, update: Update, context: CallbackContext):
        message = f"Available commands:\n' \start - Start the bot\n' \
            '\set_affiliate_link - Set the affiliate link\n' \
            '\help - Show this help message"
        await update.message.reply_text(message)

    async def error(self, update: Update, context: CallbackContext):
        logger.error(context.error)

    def run(self):
        logger.info('Bot started')
        logger.info('Bot polling...')
        self.app.run_polling(poll_interval=3)
        logger.info('Press Ctrl-C to stop')

logger.info('Starting bot...')
bot = MyBot(settings.TOKEN)
bot.run()
