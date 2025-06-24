import telebot
from telebot import types
import requests
from io import BytesIO


bot = telebot.TeleBot("*********************************")

waste_info = {
    "Пластик": {
        "description": "Пластик разлагается от 100 до 500 лет. Сдавайте его в пункты переработки!\n\n<b>Перед сдачей:</b>\n- Промойте пластиковые бутылки и контейнеры от остатков пищи и напитков.\n- Удалите крышки, если это требуется в вашем пункте приёма.\n- Сожмите бутылки, чтобы они занимали меньше места.\n- Сдавайте только маркированный пластик (обычно маркировка от 1 до 7).\n\n<b>Где сдавать:</b>\n- Экобоксы в супермаркетах и торговых центрах.\n- Муниципальные пункты приёма вторсырья.",
        "image": "https://cdn.pixabay.com/photo/2023/09/14/09/07/pollution-8252592_1280.jpg"
    },
    "Стекло": {
        "description": "Стекло практически не разлагается. Оно отлично поддается переработке!\n\n<b>Перед сдачей:</b>\n- Разделяйте стекло по цветам (белое, зелёное, коричневое), если это требуется.\n- Промойте стеклянные банки и бутылки от остатков.\n- Удалите металлические крышки или пластмассовые элементы.\n- Не сдавайте битое стекло, оконное стекло и зеркала (их принимают отдельно).\n\n<b>Где сдавать:</b>\n- Контейнеры для стекла во дворах жилых домов.\n- Пункты приёма вторсырья",
        "image": "https://cdn.pixabay.com/photo/2019/02/27/16/58/broken-glass-4024471_1280.png"
    },
    "Бумага": {
        "description": "Бумага разлагается за 2-6 месяцев. Её легко переработать!\n\n<b>Перед сдачей:</b>\n- Удалите пластиковые окна из конвертов.\n- Не сдавайте загрязнённую бумагу (жир, краска, пища).\n- Сложите и спрессуйте бумагу или картон.\n- Сдавайте отдельно газеты, журналы, картон и офисную бумагу, если требуется.\n\n<b>Где сдавать:</b>\n- Синие контейнеры для макулатуры.\n- Школы, офисы и библиотеки часто собирают бумагу на переработку.\n- Частные и государственные пункты приёма вторсырья.",
        "image": "https://cdn.pixabay.com/photo/2022/01/15/22/51/paper-6940901_1280.png"
    },
    "Металл": {
        "description": "Металл разлагается около 10 лет. Металлы важно сдавать в переработку!\n\n<b>Перед сдачей:</b>\n- Промойте консервные банки и другие металлические упаковки.\n- Удалите пластиковые и бумажные элементы, если возможно.\n- Сдавайте алюминиевые банки отдельно от других видов металла.\n- Не сдавайте крупногабаритный или ржавый металл без уточнения в пункте приёма.\n\n<b>Где сдавать:</b>\n- Специализированные пункты приёма лома и металла.\n- Контейнеры для сбора алюминиевых банок.",
        "image": "https://cdn.pixabay.com/photo/2012/04/26/20/36/can-43122_1280.png"
    }
}

@bot.message_handler(commands=['start','help'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for waste_type in waste_info:
        markup.add(types.KeyboardButton(waste_type))
    bot.send_message(
        message.chat.id,
        "Привет! Я бот, который расскажет, как правильно сортировать мусор. Выберите тип отходов:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text in waste_info)
def handle_waste_type(message):
    info = waste_info[message.text]
    try:
        response = requests.get(info['image'])
        image = BytesIO(response.content)
        bot.send_photo(
            message.chat.id,
            photo=image,
            caption=f"<b>{message.text}</b>\n{info['description']}",
            parse_mode='HTML'
        )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"Не удалось загрузить изображение /n/n <b>{message.text}</b>\n{info['description']}"
        )


@bot.message_handler(func=lambda message: True)
def fallback(message):
    bot.send_message(
        message.chat.id,
        "Пожалуйста, выберите тип отходов из предложенных кнопок."
    )

bot.polling()
