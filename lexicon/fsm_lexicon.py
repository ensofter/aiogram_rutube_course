LEXICON_RU: dict[str, str] = {
    '/start': 'Этот бот демонстрирует работу FSM\n\n'
              'Чтобы перейти к заполнению анкеты - '
              'отправьте команду /fillform',
    '/cancel': 'Отменять нечего. Вы вне машины состояний\n\n'
               'Чтобы перейти к заполнению анкеты - '
               'отправьте команду /fillform',
    '/cancel_in_state': 'Вы нажали кнопку!',
    '/fillform': 'Пожалуйста, введите ваше имя',
    'give_age': 'Спасибо!\n\nА теперь введите ваш возраст',
    'warning_not_name': 'То, что вы отправили не похоже на имя\n\n'
                        'Пожалуйста, введите ваше имя\n\n'
                        'Если вы хотите прервать заполнение анкеты - '
                        'отправьте команду /cancel',
    'gender': 'Спасибо!\n\nУкажите ваш пол',
    'male': 'Мужской',
    'female': 'Женский',
    'undefined_gender': 'Пока не ясно',
    'warning_not_age': 'Возраст должен быть целым числом от 4 до 120\n\n'
                       'Попробуйте еще раз\n\nЕсли вы хотите прервать '
                       'заполнение анкеты - отправьте команду /cancel',
    'photo': 'Спасибо! А теперь загрузите, пожалуйста, ваше фото',
    'secondary': 'Среднее',
    'higher': 'Высшее',
    'no_edu': 'Нету',
    'education': 'Спасибо!\n\nУкажите ваше образование',
    'warning_no_photo': 'Пожалуйста, на этом шаге отправьте '
                        'ваше фото\n\nЕсли вы хотите прервать '
                        'заполнение анкеты - отправьте команду /cancel',
    'yes_news': 'Да',
    'no_news': 'Нет, спасибо',
    'get_news': 'Спасибо!\n\nОстался последний шаг.\n'
                'Хотели бы вы получать новости?',
    'warning_no_education': 'Пожалуйста, пользуйтесь кнопками при выборе образования\n\n'
                            'Если вы хотите прервать заполнение анкеты - отправьте '
                            'команду /cancel',
    'questionare_end': 'Спасибо! Ваши данные сохранены!\n\n'
                       'Вы вышли из машины состояний',
    'get_my_data': 'Чтобы посмотреть данные вашей '
                   'анкеты - отправьте команду /showdata',
    'warning_not_news': 'Пожалуйста, воспользуйтесь кнопками!\n\n'
                        'Если вы хотите прервать заполнение анкеты - '
                        'отправьте команду /cancel',
    'no_profile': 'Вы еще не заполняли анкету. Чтобы приступить - '
                  'отправьте команду /fillform'
}
