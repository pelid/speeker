from datetime import date, timedelta
import string
import logging

DOW_NOT_FOUND_TMPL = 'Не знаю что нужно брать с собой в {dow_name}. Спроси у мамы!'
SUBJECT_ITEMS_SCRIPT_PLUG = 'Спроси у мамы!'

INTRO_TMPL = "Собираем рюкзак на {dow_name}."
SUBJECT_INTRO = "Предметы в этот день."
EXTRA_ITEMS_TMPL = "В {dow_name} не забудь {extra_items_str}."

logger = logging.getLogger('school_bag')

DOW_NAMES = {
    0: 'понедельник',
    1: 'вторник',
    2: 'среда',
    3: 'четверг',
    4: 'пятница',
    5: 'суббота',
    6: 'воскресенье',
}


SUBJECTS_TO_ITEMS_SCRIPT = {
    'обучение грамоте': 'Взять азбуку и тетрадь',
    'письмо': 'Положи прописи и тетрадь',
    'математика': 'Нужны учебник, рабочая тетрадь, тетрадь в клетку',
    'физкультура по понедельникам': 'Возьми футболку, шорты, носки и кроссовки',
    'физкультура по пятницам': 'Возьми футболку, шорты, носки и чешки',
    'футбол': 'Проверь что взял футболку, шорты, носки и кроссовки',
    'музыка': 'Положи рабочую тетрадь',
    'английский язык': 'Положи рабочую тетрадь',
    'окружающий мир': 'Взять учебник и рабочую тетрадь',
    'ИЗО': 'Взять рабочую тетрадь и цветные карандаши',
    'логика': 'Возьми рабочую тетрадь',
}


COMMON_ITEMS = [
    'Пенал',
    'Подставка для книг',
    'Блокнот',
]

DOW_ITEMS = {
    'понедельник': {
        'subjects': [
            'обучение грамоте',
            'письмо',
            'математика',
            'физкультура по понедельникам',
            'футбол',
        ],
        'items': [
            'сменка',
        ],
    },
    'вторник': {
        'subjects': [
            'музыка',
            'обучение грамоте',
            'письмо',
            'математика',
        ],
    },
    'среда': {
        'subjects': [
            'обучение грамоте',
            'английский язык',
            'письмо',
            'окружающий мир',
            'ИЗО',
            'логика',
            'футбол',
        ],
    },
    'четверг': {
        'subjects': [
            'обучение грамоте',
            'письмо',
            'математика',
            'технология',
        ],
    },
    'пятница': {
        'subjects': [
            'окружающий мир',
            'физкультура по пятницам',
            'письмо',
            'математика',
        ],
    },
}

def get_subject_script(subject_name, with_trailing_dot=True):
    if subject_name in SUBJECTS_TO_ITEMS_SCRIPT:
        items_script = SUBJECTS_TO_ITEMS_SCRIPT[subject_name].strip()
    else:
        items_script = SUBJECT_ITEMS_SCRIPT_PLUG


    script = '{}. {}'.format(subject_name.title(), items_script)

    if with_trailing_dot and script and not script[-1] in string.punctuation:
        script += '.'

    return script

def get_script(_date=None):
    if _date is None:
        _date = date.today() + timedelta(days=1)

    dow = _date.weekday()
    if dow > 4:
        dow = 0
    dow_name = DOW_NAMES[dow]

    if not dow_name in DOW_ITEMS:
        yield DOW_NOT_FOUND_TMPL.format(dow_name=_date.day)
        return

    yield INTRO_TMPL.format(dow_name=dow_name)

    cfg = DOW_ITEMS[dow_name]
    extra_items = cfg.get('items', [])
    logger.debug('extra_items: %s', extra_items)
    subjects = cfg.get('subjects', [])
    logger.debug('subjects: %s', subjects)

    if subjects:
        yield SUBJECT_INTRO
        for subject in subjects:
            yield get_subject_script(subject)

    if extra_items:
        extra_items_str = ', '.join(extra_items)
        yield EXTRA_ITEMS_TMPL.format(dow_name=dow_name, extra_items_str=extra_items_str)
