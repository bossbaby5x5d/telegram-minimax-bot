import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = "8006638684:AAE9-VE4yh7oyjftfOYWjUAaXbBv-8Bvzgs"
MINIMAX_API_KEY = "sk-api-HIaAqcunFejbtMJNPIvl-TumSpZSlp4-usCZe-Mk6ls-fmEe8b6pJbubotbZOlhzbSppUNhXuSso36Oq-5IRGadX-XNugGxmZ5KCh4rCoww0u88ZCQIsJzA"
MINIMAX_API_URL = "https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId=your_group_id"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "မင်္ဂလာမယ်! MiniMax AI Bot မှကြိုဆိုပါတယ်! 😊\n\n"
        "မေးချင်တာမေးပါ။ AI ကဖြေပေးပါမယ်!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ဤ Bot သည် MiniMax AI နှင့်ချိတ်ဆက်ထားသည်။\n"
        "/start - Bot စတင်မည်\n"
        "/help - ဤမက်ဆိုင်ချက်"
    )

async def chat_with_minimax(user_message: str) -> str:
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "MiniMax-Text-01",
        "messages": [{"role": "user", "content": user_message}]
    }

    try:
        response = requests.post(MINIMAX_API_URL, headers=headers, json=data, timeout=30)
        result = response.json()
        logger.info(f"MiniMax API Response: {result}")

        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        elif "base_resp" in result:
            return f"API Error: {result['base_resp'].get('retmsg', 'Unknown error')}"
        else:
            return f"Response: {result}"
    except Exception as e:
        logger.error(f"Error: {e}")
        return f"Error: {str(e)}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text("🤔 စဉ်းစားနေသည်...")
    response = await chat_with_minimax(user_message)
    await update.message.reply_text(response)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
