import random
import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ChatAction
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from gtts import gTTS

import config

REACTIONS = ["❤️", "🔥", "😂", "😍", "👍", "😎"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👑 Owner", url=f"tg://user?id={config.OWNER_ID}")],
        [InlineKeyboardButton("💬 Support", url=config.SUPPORT_CHANNEL)],
        [InlineKeyboardButton("👥 Group", url=config.GROUP_LINK)]
    ]

    await update.message.reply_text(
        f"👋 Hello {update.effective_user.first_name}\n\n"
        f"🤖 Main *King User Bot* hoon\n"
        f"⚡ Free Plan Compatible\n"
        f"👑 Owner: {config.OWNER_NAME}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    reply_text = f"🤖 Tumne bola:\n`{text}`\n\n✨ Main sun raha hoon 😉"
    await update.message.reply_text(reply_text, parse_mode="Markdown")

    # random reaction
    reaction = random.choice(REACTIONS)
    await update.message.reply_text(reaction)

    # voice reply
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.RECORD_VOICE)

    tts = gTTS(text="Main tumhari baat samajh gaya hoon", lang="hi")
    file_name = "voice.mp3"
    tts.save(file_name)

    await update.message.reply_voice(voice=open(file_name, "rb"))
    os.remove(file_name)

def main():
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    print("🤖 Bot Started Successfully")
    app.run_polling()

if __name__ == "__main__":
    main()
