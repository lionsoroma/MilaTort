# -*- coding: utf-8 -*-
# SMSC.UA API (smsc.ua) версия 1.9 (01.02.2017)

from datetime import datetime
from time import sleep
import smtplib

try:
    from urllib import urlopen, quote
except ImportError:
    from urllib.request import urlopen
    from urllib.parse import quote

# Константы для настройки библиотеки
SMSC_LOGIN = "lionso"			# логин клиента
SMSC_PASSWORD = "v2jJCZbRnXEY"	# пароль
SMSC_POST = False				# использовать метод POST
SMSC_HTTPS = False				# использовать HTTPS протокол
SMSC_CHARSET = "utf-8"			# кодировка сообщения (windows-1251 или koi8-r), по умолчанию используется utf-8
SMSC_DEBUG = True				# флаг отладки

# Константы для отправки SMS по SMTP
SMTP_FROM = "api@smsc.ua"		# e-mail адрес отправителя
SMTP_SERVER = "send.smsc.ua"	# адрес smtp сервера
SMTP_LOGIN = ""					# логин для smtp сервера
SMTP_PASSWORD = ""				# пароль для smtp сервера

# Вспомогательная функция, эмуляция тернарной операции ?:


def ifs(cond, val1, val2):
    if cond:
        return val1
    return val2


# Класс для взаимодействия с сервером smsc.ua

class SMSC(object):
    def send_sms(self, phones, message, translit=0, time="", id=0, format=0, sender=False, query=""):
        formats = ["flash=1", "push=1", "hlr=1", "bin=1", "bin=2", "ping=1", "mms=1", "mail=1", "call=1"]
        m = self._smsc_send_cmd("send", "cost=3&phones=" + quote(phones) + "&mes=" + quote(message) + \
                    "&translit=" + str(translit) + "&id=" + str(id) + ifs(format > 0, "&" + formats[format-1], "") + \
                    ifs(sender == False, "", "&sender=" + quote(str(sender))) + \
                    ifs(time, "&time=" + quote(time), "") + ifs(query, "&" + query, ""))

        if SMSC_DEBUG:
            if m[1] > "0":
                print("Сообщение отправлено успешно. ID: " + m[0] + ", всего SMS: " + m[1] + ", стоимость: " + m[2] + ", баланс: " + m[3])
            else:
                print("Ошибка №" + m[1][1:] + ifs(m[0] > "0", ", ID: " + m[0], ""))

        return m

    def send_sms_mail(self, phones, message, translit=0, time="", id=0, format=0, sender=""):
        server = smtplib.SMTP(SMTP_SERVER)

        if SMSC_DEBUG:
            server.set_debuglevel(1)

        if SMTP_LOGIN:
            server.login(SMTP_LOGIN, SMTP_PASSWORD)

        server.sendmail(SMTP_FROM, "send@send.smsc.ua", "Content-Type: text/plain; charset=" + SMSC_CHARSET + "\n\n" + \
                        SMSC_LOGIN + ":" + SMSC_PASSWORD + ":" + str(id) + ":" + time + ":" + str(translit) + "," + \
                        str(format) + "," + sender + ":" + phones + ":" + message)
        server.quit()

    def get_sms_cost(self, phones, message, translit=0, format=0, sender=False, query=""):
        formats = ["flash=1", "push=1", "hlr=1", "bin=1", "bin=2", "ping=1", "mms=1", "mail=1", "call=1"]
        m = self._smsc_send_cmd("send", "cost=1&phones=" + quote(phones) + "&mes=" + quote(message) + \
                                ifs(sender == False, "", "&sender=" + quote(str(sender))) + \
                                "&translit=" + str(translit) + ifs(format > 0, "&" + formats[format-1], "") + ifs(query, "&" + query, ""))
        # (cost, cnt) или (0, -error)
        if SMSC_DEBUG:
            if m[1] > "0":
                print("Стоимость рассылки: " + m[0] + ". Всего SMS: " + m[1])
            else:
                print("Ошибка №" + m[1][1:])
        return m

    def get_status(self, id, phone, all = 0):
        m = self._smsc_send_cmd("status", "phone=" + quote(phone) + "&id=" + str(id) + "&all=" + str(all))
        # (status, time, err, ...) или (0, -error)
        if SMSC_DEBUG:
            if m[1] >= "0":
                tm = ""
                if m[1] > "0":
                    tm = str(datetime.fromtimestamp(int(m[1])))
                print("Статус SMS = " + m[0] + ifs(m[1] > "0", ", время изменения статуса - " + tm, ""))
            else:
                print("Ошибка №" + m[1][1:])
        if all and len(m) > 9 and (len(m) < 14 or m[14] != "HLR"):
            m = (",".join(m)).split(",", 8)
        return m

    def get_balance(self):
        m = self._smsc_send_cmd("balance") # (balance) или (0, -error)
        if SMSC_DEBUG:
            if len(m) < 2:
                print("Сумма на счете: " + m[0])
            else:
                print("Ошибка №" + m[1][1:])
        return ifs(len(m) > 1, False, m[0])

    def _smsc_send_cmd(self, cmd, arg=""):
        url = ifs(SMSC_HTTPS, "https", "http") + "://smsc.ua/sys/" + cmd + ".php"
        _url = url
        arg = "login=" + quote(SMSC_LOGIN) + "&psw=" + quote(SMSC_PASSWORD) + "&fmt=1&charset=" + SMSC_CHARSET + "&" + arg
        i = 0
        ret = ""
        while ret == "" and i <= 5:
            if i > 0:
                url = _url.replace("smsc.ua/", "www" + str(i) + ".smsc.ua/")
            else:
                i += 1
            try:
                if SMSC_POST or len(arg) > 2000:
                    data = urlopen(url, arg.encode(SMSC_CHARSET))
                else:
                    data = urlopen(url + "?" + arg)
                ret = str(data.read().decode(SMSC_CHARSET))
            except:
                ret = ""
            i += 1
        if ret == "":
            if SMSC_DEBUG:
                print("Ошибка чтения адреса: " + url)
            ret = "," # фиктивный ответ
        return ret.split(",")


# Examples:
# smsc = SMSC()
# smsc.send_sms("79999999999", "test", sender="sms")
# smsc.send_sms("79999999999", "http://smsc.ua\nSMSC.UA", query="maxsms=3")
# smsc.send_sms("79999999999", "0605040B8423F0DC0601AE02056A0045C60C036D79736974652E72750001036D7973697465000101", format=5)
# smsc.send_sms("79999999999", "", format=3)
# r = smsc.get_sms_cost("79999999999", "Вы успешно зарегистрированы!")
# smsc.send_sms_mail("79999999999", "test2", format=1)
# r = smsc.get_status(12345, "79999999999")
# print(smsc.get_balance())
