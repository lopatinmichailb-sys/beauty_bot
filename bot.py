import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiohttp import web
from aiogram.webhook.aiohttp_handler import SimpleRequestHandler, setup_application

# Берем токен из файла настроек
from config import TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="💅 Записаться на процедуру"))
    builder.add(types.KeyboardButton(text="📜 Услуги и цены"))
    builder.add(types.KeyboardButton(text="📞 Контакты студии"))
    builder.adjust(1)
    
    await message.answer(
        f"Приветствуем вас в студии красоты Beauty Vibe, {message.from_user.first_name}! 👋\n"
        "Я ваш личный виртуальный ассистент. Чем я могу помочь вам сегодня?",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

@dp.message(F.text == "📜 Услуги и цены")
async def show_services(message: types.Message):
    text = (
        "✨ **Прайс-лист нашей студии:** ✨\n\n"
        "💅 **Ногтевой сервис (Мастер Нина):**\n"
        "• Маникюр с покрытием гель-лак — 2 000 руб.\n"
        "• Педикюр комплексный — 2 500 руб.\n\n"
        "👁️ **Взгляд (Мастер Надежда):**\n"
        "• Наращивание ресниц (Классика) — 2 200 руб.\n"
        "• Наращивание ресниц (2D / 3D) — 2 600 руб.\n\n"
        "Для записи нажмите кнопку «Записаться на процедуру» ниже 👇"
    )
    await message.answer(text, parse_mode="Markdown")

@dp.message(F.text == "📞 Контакты студии")
async def show_contacts(message: types.Message):
    text = (
        "📍 **Наш адрес:**\n"
        "г. Хабаровск, ул. Серышева, д. 80 (2 этаж)\n\n"
        "📞 **Телефон для связи:**\n"
        "+7 (914) 161-50-15\n\n"
        "⏰ **Режим работы:**\n"
        "Ежедневно с 10:00 до 20:00\n\n"
        "📱 Наш Инстаграм: @beauty.vibe.khv"
    )
    await message.answer(text, parse_mode="Markdown")

async def on_startup(bot: Bot):
    # Очищаем старые зависшие обновления
    await bot.delete_webhook(drop_pending_updates=True)

def main():
    # Создаем полноценное веб-приложение, которое займет порт для Render
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot)
    setup_application(app, dp, bot=bot)
    app.on_startup.append(on_startup)
    
    # Читаем порт, который требует сервер Render (по умолчанию 8080)
    port = int(os.getenv("PORT", 8080))
    
    # Запускаем фоновый опрос параллельно с пустым веб-сервером для удержания порта
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling(bot))
    
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
