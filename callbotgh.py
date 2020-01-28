import telebot


from PIL import Image
import random as random
import numpy as np
import cv2 as cv
import urllib
import requests
from io import BytesIO



bot = telebot.TeleBot(TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
если скинуть фотку может получиться смешная ситуация
""")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text:
        bot.send_message(message.chat.id, "у меня тут проходной двор чтоли ")
    elif message.text == "как дела":
        bot.send_message(message.from_user.id, "пока не родила))")



@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    try:
        bot.reply_to(message, "красиво ;)")
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)

        kosmolot = random.randint(0, 150)  # название файла с рекламой
        url='https://api.telegram.org/file/bot%s/%s' %(TOKEN, file_info.file_path)  #целый сайт для одного файла только задумайтесь
        print(url)
        response = requests.get(url)
        user_pic = Image.open(BytesIO(response.content)) # фото юзера

        hsv_max = np.array((187, 255, 253), np.uint8)
        hsv_min = np.array((0, 54, 5), np.uint8)

        if __name__ == '__main__':
            fn = "https://raw.githubusercontent.com/Sidel-Meril/addblock/master/%s.JPG" % kosmolot  # имя файла, который будем анализировать
            print(fn)
            response = requests.get(fn)
            add = Image.open(BytesIO(response.content))  # открытие рекламы для объединения с user_pic

            req = urllib.request.urlopen(fn)
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            img = cv.imdecode(arr, -1)  # открытие рекламы для анализа

            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)  # меняем цветовую модель с BGR на HSV
            thresh = cv.inRange(hsv, hsv_min, hsv_max)  # применяем цветовой фильтр
            contours0, hierarchy = cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            # перебираем все найденные контуры в цикле
            for cnt in contours0:
                rect = cv.minAreaRect(cnt)  # пытаемся вписать прямоугольник
                box = cv.boxPoints(rect)  # поиск четырех вершин прямоугольника
                box = np.int0(box)  # округление координат
                area = int(rect[1][0] * rect[1][1])  # вычисление площади
                if area > 30000:
                    if int(rect[1][1]) > int(rect[1][0]):
                        a = int(rect[1][1])
                        b = int(rect[1][0])
                    else:
                        a = int(rect[1][0])
                        b = int(rect[1][1])
                    newsize = (a, b)
                    user_pic = user_pic.resize(newsize)
                    add.paste(user_pic, (int(box[1][0]), int(box[2][1])))

        bio = BytesIO()#биологическое имя файла для add в PIL
        bio.name = 'image.jpeg'
        add.save(bio, 'JPEG')
        bio.seek(0)

        bot.send_photo(message.chat.id, photo=bio)




    except Exception as e:
        bot.reply_to(message, e) #"ааа я женщина аааа я женщина"

#


#
bot.polling(none_stop=True, interval=5)