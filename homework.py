import datetime as dt

now = dt.datetime.now()
date_format = '%d.%m.%Y'


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            # Указываем сегодняшнюю дату по-умолчанию
            self.date = now.date()
        else:
            # Приводим полученную дату к виду date_format
            self.date = dt.datetime.strptime(date, date_format).date()


class Calculator():
    def __init__(self, limit):
        self.limit = limit
        self.week_later = dt.date.today() - dt.timedelta(days=7)
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        t_amount = 0
        for record in self.records:
            if record.date == now.date():
                t_amount += record.amount
        return t_amount

    def get_week_stats(self):
        total_week_amount = 0
        for record in self.records:
            if now.date() >= record.date > self.week_later:
                total_week_amount += record.amount
        return total_week_amount

    def get_today_limit(self):
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    USD_RATE = 73.20
    EURO_RATE = 86.64

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def get_today_cash_remained(self, currency):
        self.currency = currency
        t_amount = self.get_today_limit()
        rub_currency = 'руб'
        usd_currency = 'USD'
        eur_currency = 'Euro'
        wrong_currency_message = 'Указана неверная валюта. Повторите ввод.'
        positive_message = 'На сегодня осталось'
        neutral_message = 'Денег нет, держись'
        negative_message = 'Денег нет, держись: твой долг -'

        if t_amount > 0:
            if self.currency == 'rub':
                return (f'{positive_message} {t_amount} {rub_currency}')
            elif self.currency == 'usd':
                t_amount = round((t_amount / CashCalculator.USD_RATE), 2)
                return (f'{positive_message} {t_amount} {usd_currency}')
            elif self.currency == 'eur':
                t_amount = round((t_amount / CashCalculator.EURO_RATE), 2)
                return (f'{positive_message} {t_amount} {eur_currency}')
            else:
                return (f'{wrong_currency_message}')
        elif t_amount == 0:
            return (f'{neutral_message}')
        else:
            if self.currency == 'rub':
                return (f'{negative_message} {abs(t_amount)} {rub_currency}')
            elif self.currency == 'usd':
                t_amount = round((t_amount / CashCalculator.USD_RATE), 2)
                return (f'{negative_message} {abs(t_amount)} {usd_currency}')
            elif self.currency == 'eur':
                t_amount = round((t_amount / CashCalculator.EURO_RATE), 2)
                return (f'{negative_message} {abs(t_amount)} {eur_currency}')
            else:
                return (f'{wrong_currency_message}')


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def get_calories_remained(self):
        positive_message = ('Сегодня можно съесть что-нибудь ещё, но с '
                            'общей калорийностью не более')
        neutral_message = 'Хватит есть!'

        t_amount = 0
        for record in self.records:
            if record.date == now.date():
                t_amount += record.amount
        t_amount = self.limit - t_amount

        if t_amount > 0:
            return (f'{positive_message} {t_amount} кКал')
        else:
            return (f'{neutral_message}')
