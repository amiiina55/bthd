import os
os.environ['TZ'] = 'Asia/Almaty'

import logging
from datetime import datetime, timedelta, time
from pytz import timezone
from telegram import Update, Bot, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Устанавливаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


people = [
    {'fio': 'Юн Владимир Брониславович','position': 'Заместитель директора Департамена','department': 'Департ. бухучета и отчетности','birthday': '2024-07-01'},    
    {'fio': 'Имашева Баян Паруховна','position': 'Заместитель Председателя Правления','department': '-','birthday': '2024-07-01'},
    {'fio': 'Аманбаев Саят Жалгасович', 'position': 'Заместитель директора Департамента', 'department': 'Департамент перевода денег', 'birthday': '2024-07-02'},    
    {'fio': 'Кокханат Айдос', 'position': 'Начальник управления', 'department': 'Управление обеспечения качества', 'birthday': '2024-07-02'},
    {'fio': 'Туманов Василий Иванович', 'position': 'Директор Департамента', 'department': 'Юридический департамент', 'birthday': '2024-07-03'},    
    {'fio': 'Кубинский Денис Владимирович', 'position': 'Директор Департамента', 'department': 'Департ. ресурсов', 'birthday': '2024-07-03'},
    {'fio': 'Интемирова Жанель Кенжебековна', 'position': 'Начальник управления', 'department': 'Управление цифровизации', 'birthday': '2024-07-04'},   
    {'fio': 'Кабулов Ислям Гомарович', 'position': 'Начальник управления', 'department': 'Рег. управление банковского сервиса', 'birthday': '2024-07-05'},
    {'fio': 'Кожабекова Шынар Бауржановна', 'position': 'Начальник управления', 'department': 'Управление мобильной коммерции', 'birthday': '2024-07-05'},   
    {'fio': 'Шиварев Вячеслав Викторович', 'position': 'Начальник управления', 'department': 'Упр. №3', 'birthday': '2024-07-06'},
    {'fio': 'Выходцев Александр Александрович', 'position': 'Начальник управления', 'department': 'Упр. взаимодействия с внешними системами', 'birthday': '2024-07-06'},   
    {'fio': 'Исаханова Гульнар Зулкарнаиновна', 'position': 'Главный бухгалтер', 'department': '-', 'birthday': '2024-07-07'},
    {'fio': 'Фалеев Бейбит Хамитович', 'position': 'Председатель Правления', 'department': '-', 'birthday': '2024-07-08'},   
    {'fio': 'Кубейсинов Айбек Абильбекович', 'position': 'Начальник управления', 'department': 'Управ. кредит. рисков цифровых прод. РБ', 'birthday': '2024-07-09'},
    {'fio': 'Нурахметов Руслан Есполганович', 'position': 'Заместитель директора филиала', 'department': 'Администрация', 'birthday': '2024-07-09'},    
    {'fio': 'Нуркенев Амир Дауренбекович', 'position': 'Директор Департамента', 'department': 'Департ. цифровых госуд-х сервисов', 'birthday': '2024-07-10'},
    {'fio': 'Оспанов Айбек Бакытулы', 'position': 'Зам.дир департамента-нач. управления', 'department': 'упр. разработки внеш.интег. и фронт канал', 'birthday': '2024-07-10'},    
    {'fio': 'Маликова Наргиза Алимжановна', 'position': 'Начальник управления', 'department': 'Упр. администрирования персонала', 'birthday': '2024-07-11'},
    {'fio': 'Турсунова Русалина Сидикбяговна', 'position': 'Начальник управления', 'department': 'Упр. учета деб./кред. задол. и капитала', 'birthday': '2024-07-12'},    
    {'fio': 'Абисатов Махамбет Хайржанович', 'position': 'Генеральный директор', 'department': 'Упр. разработки внеш.интег. и фронт канал', 'birthday': '2024-07-12'}, 
    {'fio': 'Муратбеков Рустем Мусаканович', 'position': 'Глава офиса данных', 'department': 'Глава офиса данных', 'birthday': '2024-07-13'},    {'fio': 'Джемалудинов Камиль Абдулович', 'position': 'Заместитель директора по МСБ', 'department': 'Администрация', 'birthday': '2024-07-13'},
    {'fio': 'Жанкина Динара Кабдылкалыковна', 'position': 'Начальник управления', 'department': 'Управление операционного дня', 'birthday': '2024-07-14'},    {'fio': 'Медеуов Азат Игенбаевич', 'position': 'Зам.дир департамента-нач. управления', 'department': 'Управление учета депозитных операций', 'birthday': '2024-07-14'},
    {'fio': 'Бийсебаева Салтанат Сюентаевна', 'position': 'Начальник управления', 'department': 'Упр. анализа и оптим-и бизнес-процессов', 'birthday': '2024-07-15'},    
    {'fio': 'Тян Ольга Леонидовна', 'position': 'Начальник управления', 'department': 'Упр. бюджета', 'birthday': '2024-07-15'},
    {'fio': 'Закен Сандугаш Алимолдакызы', 'position': 'Начальник управления', 'department': 'Упр. по работе с ВИП и Премиум клиентами', 'birthday': '2024-07-16'},    
    {'fio': 'Ngai Ka Ching', 'position': 'Член Совета директоров-независимый директор', 'department': 'Глава офиса данных', 'birthday': '2024-07-16'},
    {'fio': 'Сапарбек Бейимбет Серикулы', 'position': 'Заместитель директора филиала', 'department': 'Администрация', 'birthday': '2024-07-18'},    
    {'fio': 'Марат Ерген Маратулы', 'position': 'Заместитель директора филиала', 'department': 'Администрация', 'birthday': '2024-07-19'},
    {'fio': 'Дияров Оскар Юрьевич', 'position': 'Глава внутреннего аудита', 'department': 'Глава внутреннего аудита', 'birthday': '2024-07-20'},    
    {'fio': 'Душатова Гульсум Сериковна', 'position': 'Управляющий директор', 'department': 'Управляющий директор ТБ', 'birthday': '2024-07-20'},
    {'fio': 'Хибибуллаева Эльмира Ашимовна', 'position': 'Начальник управления', 'department': 'Управление учета заработной платы', 'birthday': '2024-07-21'},   
    {'fio': 'Жаксылык Искендер Маратович', 'position': 'Директор департамента', 'department': 'Департ. автоматизации бизнес-процессов', 'birthday': '2024-07-21'},
    {'fio': 'Ли Вадим Юрьевич', 'position': 'Заместитель директора департамента', 'department': 'Департамент Onlinebank', 'birthday': '2024-07-21'},    
    {'fio': 'Чкоидзе Шота Мурманович', 'position': 'Зам. Генерального директора', 'department': '-', 'birthday': '2024-07-21'},
    {'fio': 'Пак Елена Эдуардовна', 'position': 'Начальник управления', 'department': 'Упр. методологии и анализа', 'birthday': '2024-07-22'},    
    {'fio': 'Жамалиева Аида Кахармановна', 'position': 'Начальник управления', 'department': 'Упр. проектами развития и поддержки', 'birthday': '2024-07-22'},
    {'fio': 'Секенова Дана Елдоскызы', 'position': 'Начальник управления', 'department': 'Управление качества клиентского сервиса', 'birthday': '2024-07-23'},    {'fio': 'Князев Олег Александрович', 'position': 'Директор департамента', 'department': 'Департамент Homebank', 'birthday': '2024-07-23'},
    {'fio': 'Спанкулов Азамат Манарбекович', 'position': 'Начальник управления', 'department': 'Упр. №2', 'birthday': '2024-07-24'},    
    {'fio': 'Курочкин Владимир Викторович ', 'position': 'Начальник управления', 'department': 'Управление технической защиты', 'birthday': '2024-07-25'},
    {'fio': 'Досумова Карлыгаш Думанбеккызы', 'position': 'Начальник управления', 'department': 'Управ. кредит. рисков цифровых прод.МБ', 'birthday': '2024-07-25'},    
    {'fio': 'Юпов Манас Бауыржанович', 'position': 'Зам. дир департамента-нач. управления', 'department': 'Управление цифровых продуктов МБ', 'birthday': '2024-07-26'},
    {'fio': 'Сейдахмет Нурлыбек Ержигитулы', 'position': 'Директор филиала', 'department': 'Администрация', 'birthday': '2024-07-27'},    
    {'fio': 'Яхьяров Нурлан Ризаевич', 'position': 'Глава Представительства', 'department': 'Представительство АО НБК КНР', 'birthday': '2024-07-28'},
    {'fio': 'Кусаинова Жамбы Токеновна ', 'position': 'Начальник управления', 'department': 'Управление развития систем отчетности', 'birthday': '2024-07-29'},    {'fio': 'Миркамилов Мирзариф Мырхамудович', 'position': 'Начальник управления', 'department': 'Управ. ИТ аудита', 'birthday': '2024-07-29'},
    {'fio': 'Захарченко Ирина Сергеевна', 'position': 'Начальник управления', 'department': 'Упр. развития персонала', 'birthday': '2024-07-31'},    
    {'fio': 'Канапьянов Чингиз Сержанович', 'position': 'член Совета директоров- независимый директор', 'department': '-', 'birthday': '2024-07-31'},

     
]

# Функция для поиска дней рождения сегодня
def get_today_birthdays(people):
    today = datetime.today().date()
    today_birthdays = [person for person in people if datetime.strptime(person['birthday'], '%Y-%m-%d').date() == today]
    return today_birthdays

# Функция для поиска ближайших дней рождения
def get_upcoming_birthdays(people, days=10):
    today = datetime.today().date()
    end_date = today + timedelta(days=days)
    upcoming_birthdays = []
    for person in people:
        birthday = datetime.strptime(person['birthday'], '%Y-%m-%d').date()
        if today <= birthday <= end_date:
            upcoming_birthdays.append(person)
    return upcoming_birthdays

# Функция для поиска информации о человеке по ФИО
def find_person_by_fio(people, fio):
    for person in people:
        if person['fio'].lower() == fio.lower():
            return person
    return None

# Функция запуска бота
async def start(update: Update, context):
    reply_keyboard = [['Просмотреть ближайшие ДР']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
    
    today_birthdays = get_today_birthdays(people)
    if today_birthdays:
        message = "Сегодня день рождения у:\n"
        for person in today_birthdays:
            message += f"{person['fio']} - {person['position']} ({person['department']}) - {person['birthday']}\n"
    else:
        message = "Сегодня нет дней рождений."
    
    await update.message.reply_text(
        f'Привет! Ваш бот запустился.\n'
        f'{message}\n'
        'Выберите опцию ниже:',
        reply_markup=markup
    )

# Обработчик сообщений с текстом
async def handle_message(update: Update, context):
    text_received = update.message.text
    if text_received == 'Просмотреть ближайшие ДР':
        upcoming_birthdays = get_upcoming_birthdays(people, days=10)
        if upcoming_birthdays:
            message = "Ближайшие дни рождения:\n"
            for person in upcoming_birthdays:
                message += f"{person['fio']} - {person['position']} ({person['department']}) - {person['birthday']}\n\n"
        else:
            message = "В ближайшие 10 дней нет дней рождений."
        await update.message.reply_text(message)
    else:
        person = find_person_by_fio(people, text_received)
        if person:
            message = f"{person['fio']} - {person['position']} ({person['department']}) - {person['birthday']}"
            await update.message.reply_text(message)

# Функция для отправки уведомления
async def send_notification(token, message):
    bot = Bot(token=token)
    CHAT_ID = '722521727'  # Укажите ваш ID чата или канала для отправки уведомлений
    await bot.send_message(chat_id=CHAT_ID, text=message)

def main():
    # Вставьте ваш токен сюда
    token = '7313228037:AAHMJ_ZPVlzVJOkDcVkr58Dxuamz5oPqBUU'
    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Создаём планировщик
    scheduler = AsyncIOScheduler()
    
    # Часовой пояс для Алматы
    tz = timezone('Asia/Almaty')
    
    # Текущая дата и время
    now = datetime.now(tz)
    
    # Задача для отправки уведомления за день до ДР в 6 вечера
    for person in people:
        birthday = datetime.strptime(person['birthday'], '%Y-%m-%d').date()
        
        notify_day_before = datetime.combine(birthday - timedelta(days=1), time(18, 0, 0))
        notify_day_before = tz.localize(notify_day_before)
        
        if notify_day_before >= now:
            scheduler.add_job(
                send_notification,
                'date',
                run_date=notify_day_before,
                args=[token, f"Завтра день рождения у {person['fio']} ({person['department']})"]
            )
        
        # Задача для отправки уведомления в день ДР в 9 утра по алматинскому времени
        notify_birthday = datetime.combine(birthday, time(15, 59, 0))
        notify_birthday = tz.localize(notify_birthday)
        
        if notify_birthday >= now:
            scheduler.add_job(
                send_notification,
                'date',
                run_date=notify_birthday,
                args=[token, f"Сегодня день рождения у {person['fio']} ({person['department']})"]
            )
    logging.info(f'Scheduled notification for {person["fio"]} at {notify_birthday}')
    scheduler.start()
    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
