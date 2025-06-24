import telebot
from telebot import types
import datetime

bot = telebot.TeleBot("*********************************")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Что такое энергоэффективные приборы?", "Как использовать такие приборы правильно?")
    markup.row("Где покупать энергоэффективную технику?", "Оставить отзыв")

    bot.send_message(
        message.chat.id,
        "Привет! Я бот, который расскажет тебе про энергоэффективные приборы и как сэкономить на электроэнергии.\n\n"
        "Выбери одну из опций:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "Оставить отзыв")
def ask_feedback(message):
    msg = bot.send_message(message.chat.id, "Пожалуйста, напиши свой отзыв о боте или предложи улучшения:")
    bot.register_next_step_handler(msg, save_feedback)


def save_feedback(message):
    user = message.from_user
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    username = f"@{user.username}" if user.username else "(нет username)"
    feedback_text = f"[{timestamp}] {user.first_name} {user.last_name or ''} (ID: {user.id}, {username}): {message.text}\n"

    with open("feedback.txt", "a", encoding="utf-8") as f:
        f.write(feedback_text)

    bot.send_message(message.chat.id, "Спасибо за отзыв! Мы учтём ваше мнение.")


@bot.message_handler(func=lambda message: True)
def answer_question(message):
    if "что такое" in message.text.lower():
        bot.send_photo(
            message.chat.id,
            photo='https://cdn.pixabay.com/photo/2017/04/14/11/45/letter-to-2229968_640.png',
            caption="Энергоэффективные приборы — это техника, которая потребляет меньше электроэнергии при сохранении высокой производительности.\n\n"
                    "Обычно они имеют маркировку A+, A++, A+++ и выше.",
            parse_mode='Markdown')

    elif "как использовать" in message.text.lower():
        bot.send_photo(
            message.chat.id,
            photo='https://cdn.pixabay.com/photo/2022/08/12/18/34/save-energy-7382275_640.png',
            caption="Советы по использованию:\n\n1. Не оставляйте приборы в режиме ожидания.\n2. Используйте технику при полной загрузке.\n3. Правильно настраивайте температуру холодильников.\n4. Чистите фильтры.\n5. Используйте LED-лампы.",
            parse_mode='Markdown')

    elif "где покупать" in message.text.lower():
        bot.send_photo(
            message.chat.id,
            photo='https://cdn.pixabay.com/photo/2017/01/19/13/22/ecommerce-1992280_640.png',
            caption="Покупать лучше в проверенных магазинах:\n\n- [Яндекс.Маркет](https://market.yandex.ru)\n- [Ozon](https://ozon.ru)\n- [М.Видео](https://www.mvideo.ru)\n- [DNS](https://www.dns-shop.ru)\n- [Эльдорадо](https://www.eldorado.ru)",
            parse_mode='Markdown')

    else:
        bot.send_message(message.chat.id, "Пожалуйста, выбери один из вариантов, отправив его как текстовое сообщение.")

# Запуск бота
bot.infinity_polling()
