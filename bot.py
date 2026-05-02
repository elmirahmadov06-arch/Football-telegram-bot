import pandas as pd
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ==========================
# TELEGRAM BOT TOKEN
# ==========================
TOKEN = "8484927128:AAFTUo5c-T2OY1cSuLOycAYAziTwh5Zi2mg"

# ==========================
# EXCEL FAYLI
# ==========================
EXCEL_FILE = "matches.xlsx"

# ==========================
# /start
# ==========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salam!\n\n"
        "Axtarmaq istədiyiniz əmsalları bu formatda göndərin:\n\n"
        "MS1=1.85\n"
        "MSX=3.40\n"
        "MS2=4.50"
    )

# ==========================
# EXCEL OXUMA
# ==========================
def load_data():
    return pd.read_excel(EXCEL_FILE)

# ==========================
# AXTARIŞ
# ==========================
def find_matches(df, filters_dict):
    result = df.copy()

    for column, value in filters_dict.items():
        if column in result.columns:
            result = result[
                (result[column] >= value - 0.05) &
                (result[column] <= value + 0.05)
            ]

    return result

# ==========================
# İSTİFADƏÇİ MESAJI
# ==========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    try:
        filters_dict = {}

        for line in text.split("\n"):
            if "=" in line:
                key, value = line.split("=")
                filters_dict[key.strip()] = float(value.strip())

        if not filters_dict:
            await update.message.reply_text(
                "Düzgün format istifadə edin.\n\n"
                "Məsələn:\n"
                "MS1=1.90\n"
                "MSX=3.50"
            )
            return

        df = load_data()
        matches = find_matches(df, filters_dict)

        if matches.empty:
            await update.message.reply_text("Uyğun matç tapılmadı.")
            return

        message = f"Tapılan matç sayı: {len(matches)}\n\n"

        for _, row in matches.head(10).iterrows():
            message += (
                f"{row['Ev sahibi']} vs {row['Deplasman']}\n"
                f"Nəticə: {row['MAÇ SONUCU']}\n"
                f"Skor: {row['MS']}\n\n"
            )

        await update.message.reply_text(message)

    except Exception as e:
        await update.message.reply_text(f"Xəta baş verdi:\n{e}")

# ==========================
# MAIN
# ==========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Bot aktivdir...")
    app.run_polling()

if __name__ == "__main__":
    main()
