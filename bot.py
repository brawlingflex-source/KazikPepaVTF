import asyncio
import re
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

BOT_TOKEN = "8881114696:AAFUBfpjzcwyfsUISpRlqpRaoz0Lp1p-q7M"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 777 как отдельное число, не часть другого
JACKPOT_PATTERN = re.compile(r'(?<!\d)777(?!\d)')

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("🎰 Бот активен. Жду 777.")

@dp.message(F.text)
async def handle_text(message: Message):
    print(f"\n📩 [TEXT] Получено: '{message.text}' от {message.from_user.full_name}")
    if JACKPOT_PATTERN.search(message.text):
        print("✅ Найдено 777! Пытаюсь удалить...")
        try:
            await message.delete()
            print("✅ Сообщение успешно удалено!")
        except TelegramForbiddenError:
            print("❌ ОШИБКА: бот не администратор или нет прав на удаление!")
            await message.answer("❌ Не могу удалить — дайте права администратора с удалением сообщений.")
        except TelegramBadRequest as e:
            print(f"❌ ОШИБКА API: {e}")
        except Exception as e:
            print(f"❌ Неизвестная ошибка: {e}")
    else:
        print("➖ 777 не найдено в этом сообщении.")

@dp.message(F.caption)
async def handle_caption(message: Message):
    print(f"\n📩 [CAPTION] Получено: '{message.caption}' от {message.from_user.full_name}")
    if JACKPOT_PATTERN.search(message.caption):
        print("✅ Найдено 777 в подписи! Пытаюсь удалить...")
        try:
            await message.delete()
            print("✅ Сообщение успешно удалено!")
        except Exception as e:
            print(f"❌ Ошибка удаления: {e}")
    else:
        print("➖ 777 не найдено в подписи.")

@dp.message(F.dice)
async def handle_dice(message: Message):
    # Слот-машина 🎰: value = 64 соответствует комбинации 777 (джекпот)
    if message.dice.emoji == "🎰" and message.dice.value == 64:
        print("🎰 Джекпот! Выпало 777 в слотах! Пытаюсь удалить эмодзи...")
        try:
            await message.delete()
            print("✅ Эмодзи с кубиками успешно удалено!")
        except TelegramForbiddenError:
            print("❌ Ошибка: У бота нет прав на удаление! Сделайте бота админом.")
        except Exception as e:
            print(f"❌ Ошибка при удалении: {e}")

@dp.message()
async def any_other(message: Message):
    print(f"\n📩 [OTHER] Тип: {message.content_type}, от: {message.from_user.full_name}")

async def main():
    print("=== БОТ ЗАПУЩЕН ===")
    print("Ожидаю сообщения...")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
