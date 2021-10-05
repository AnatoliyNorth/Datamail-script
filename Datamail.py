import psycopg2 # Подключение к DB
import smtplib  # Работа с gmail
from email.mime.text import MIMEText # для кодировки
import csv
from email.message import EmailMessage #формирование тела письма


# функция заборы инфы с базы

with psycopg2.connect(dbname='DBname', user='User', # Имя базы и учетка
                        password='password', host='10.10.10.10') as conn: # закрыть соединение
     with  conn.cursor() as cursor: # закрыть файл
        cursor.execute("select get_orpon_users()") # SQL запрос


        results = cursor.fetchall()   # присваиваем  результ запроса  переменной в список

        contacts = [] #Делаем  список
        contacts.append(["МРФ","ФИО"," Почта"]) # Добавлем шапку в список
        for i in results:
            i=i[0] # переводим в строку через обращение по индексу
            chars = ['(', ')', "'", '"'] # определеяем лишнее
            i = "".join(c for c in i if c not in chars) # убираем лишнее
            i=i.split(',') # переводим строку в список
            contacts.append(i) # добавляем в список списки

        results=contacts

# Функция создания и записи инфы в файл

def csv_writer (results,path):
    with open(path, "w", newline='') as csv_file:  #Открываем файл указывая путь
        writer = csv.writer(csv_file, delimiter=';') #создаем  лист
        for i in results:

            writer.writerow(i)

if __name__ == "__main__":
    path = "C:/..../contacts.csv"
    csv_writer(results, path)

# Функция отправки файла по gmail

def mail ():

    sender = "yourmail@gmail.com"  # отправитель
    password = 'password'  # пароль
    reciver = ["reciver@gmail.ru"]   # Получатель

    filename = "C:/..../contacts.csv" # вложение

    msg = EmailMessage()
    msg["From"] = sender
    msg["Subject"] = "Контакты"
    msg["To"] = reciver
    msg.set_content("Контакты")

    with open(filename, 'rb') as f: #Открываем  файл
        file_data = f.read() # передеам файл переменной
    msg.add_attachment(file_data, maintype="application", subtype="csv", filename="contacts.csv")

    server = smtplib.SMTP('smtp.gmail.com', 587)  # сервер почты gmail
    server.starttls() #проброс ttls
    server.login(sender, password) # Авторизуемся
    server.send_message(msg) # Отправка

    #text = MIMEText(text, 'plain', 'utf-8')   # переводим в другую кодировку, чтобы понимать кириллицу


if __name__ == '__main__':
    mail()