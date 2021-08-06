import datetime as dt

DATE_FORMAT = '%d.%m.%Y'


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def get_today_date(self):
        return dt.date.today()

    def get_week_date(self):
        return self.get_today_date() - dt.timedelta(days=7)

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        t_amount = 0
        for record in self.records:
            if record.date == self.get_today_date():
                t_amount += record.amount
        return t_amount

    def get_week_stats(self):
        total_week_amount = 0
        for record in self.records:
            if self.get_today_date() >= record.date > self.get_week_date():
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
        currencies = {'rub': ('руб', 1),
                      'usd': ('USD', CashCalculator.USD_RATE),
                      'eur': ('Euro', CashCalculator.EURO_RATE)}

        c_type, c_rate = currencies[currency]

        if self.currency not in currencies:
            return 'Указана неверная валюта. Повторите ввод.'
        if t_amount == 0:
            return 'Денег нет, держись'
        if t_amount > 0:
            return (f'На сегодня осталось '
                    f'{abs(round((t_amount / c_rate), 2))} {c_type}')
        else:
            return (f'Денег нет, держись: твой долг - '
                    f'{abs(round((t_amount / c_rate), 2))} {c_type}')


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def get_calories_remained(self):
        positive_message = ('Сегодня можно съесть что-нибудь ещё, '
                            'но с общей калорийностью не более')

        t_amount = self.get_today_limit()

        if t_amount > 0:
            return (f'{positive_message} {t_amount} кКал')
        return ('Хватит есть!')
