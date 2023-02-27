# -*- coding: utf-8 -*-
import os
import sqlite3
import time
import requests
import vk_api


# Выбор авторизации, настройка, редактура и инфо
class Menu:
    def intro(self):
        print(' +-+-+-+-+-+-+-+-+ +-+-+-+-+-+\n |M|e|s|s|a|g|e|s| |B|o|o|s|t|\n +-+-+-+-+-+-+-+-+ +-+-+-+-+-+')
        print(' Легальная накрутка сообщений\n')
        self.mode_selection()

    def mode_selection(self):
        while True:
            try:
                self.selection = int(input('Выберите пункт:\n[1] Начать работу скрипта\n[2] Создать конфиг\n[3] Редакти'
                                           'ровать конфиг\n[4] Инфо\n\n'))
                if self.selection == 1:
                    self.authorization()
                    break
                elif self.selection == 2:
                    self.add_config()
                    break
                elif self.selection == 3:
                    self.edit_config()
                    break
                elif self.selection == 4:
                    self.info()
                    break
                else:
                    print('\nВведите число от 1 до 4!\n')
            except ValueError:
                print('\nВведите число!\n')
            except Exception as e:
                print(f'\nПроизошла ошибка: {e}\n')

    def authorization(self):
        while True:
            try:
                self.authorization_choice = int(input('\nКак авторизуемся?\n[1] Через конфиг\n[2] Через токен\n[3] Чере'
                                                      'з пароль и логин\n'))
                if self.authorization_choice == 1:
                    conn = sqlite3.connect('config.db')
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM info")
                    data = cur.fetchall()[0]
                    conn.commit()
                    conn.close()
                    print('Запускаю накрутку...')
                    Work().boost(data[0], data[1], data[3], data[2])
                    break
                elif self.authorization_choice == 2:
                    self.authorization_token()
                    break
                elif self.authorization_choice == 3:
                    self.authorization_logpass()
                    break
                else:
                    print('\nВведите число от 1 до 3!\n')
            except ValueError:
                print('\nВведите число!\n')
            except Exception as e:
                print(f'\nПроизошла ошибка: {e}\n')

    # создаем базу
    def add_config(self):
        conn = sqlite3.connect('config.db')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE info(
                        token_vk TEXT,
                        id TEXT,
                        title TEXT,
                        count INTEGER
        )""")
        conn.commit()
        conn.close()
        # заполняем значениями базу
        while True:
            try:
                print('\nВыберите способ авторизации:\n[1] Через пароль и логин\n[2] Через токен')
                self.method_autorization_db = int(input('Введите число: '))
                if self.method_autorization_db == 1:
                    self.authorization_logpass()
                    break
                elif self.method_autorization_db == 2:
                    self.authorization_token()
                    break
                else:
                    print("\nВведите 1 или 2!\n")
            except ValueError:
                print('\nВведите число!\n')
            except Exception as e:
                print(f'\nПроизошла ошибка: {e}\n')

    def edit_config(self):
        while True:
            try:
                print('\nЧто будем редактировать?\n[1] Токен приглашающего\n[2] Айди приглашаемых\n[3] Название беседы'
                      '\n[4] Количество сообщений\n[5] Удалить конфиг\n[6] Выйти\n')
                self.num_edit = int(input('Введите число: '))
                if self.num_edit == 1:
                    print('\nВыберите способ авторизации:\n[1] Через пароль и логин\n[2] Через токен')
                    self.method_autorization_db = int(input('Введите число: '))
                    if self.method_autorization_db == 1:
                        self.authorization_logpass()
                        break
                    elif self.method_autorization_db == 2:
                        self.authorization_token()
                        break
                    else:
                        print('...')
                elif self.num_edit == 2:
                    self.userid_invite()
                    break
                elif self.num_edit == 3:
                    self.title()
                    break
                elif self.num_edit == 4:
                    self.count_messages()
                    break
                elif self.num_edit == 5:
                    os.remove('config.db')
                    print('\nКонфиг был успешно удален!\nВозвращаю вас назад\n')
                    self.mode_selection()
                    break
                elif self.num_edit == 6:
                    self.mode_selection()
                    break
                else:
                    print('\n\nВведите число от 1 до 6!\n')
            except ValueError:
                print('\nВведите число!\n')
            except Exception as e:
                print(f'\nПроизошла ошибка: {e}\n')

    def info(self):
        print('Скрипт для накрутки сообщений в вк.\n\nСОВЕТЫ ПО ИСПОЛЬЗОВАНИЮ\n[1] Для пользования скриптом нужен как м'
              'инимум один аккаунт который будет вас добавлять.\n[2] В среднем после 25 сообщений происходит флуд контр'
              'ол который длится долго.\n[3] Накрутка происходит со скоростью 2 сообщения в минуту\n[4] Люди которых вл'
              'аделец токена будет приглашать в беседу должны быть у него в друзьях c разрешенными приглашениями в бесе'
              'ду.\n[5] Айди стоит писать вот так: 544, 1231, 424\n[6] Вы можете приглашать от 1 человека\n[7] Советую '
              'создать конфиг, чтобы не мучиться с постоянным вводом данных\n[8] Токен можно получить на сайте https://'
              'vkhost.github.io/\n[9] Бан за крутилку сообщений не дают!\n')
        input('Введите что-угодно чтобы вернуться обратно\n')
        self.mode_selection()

    def authorization_token(self):
        while True:
            try:
                self.token = input('\nВведите токен:\n')
                if len(self.token) == 85 or len(self.token) == 198:
                    vk = vk_api.VkApi(token=self.token)  # авторизовываемся в вк для проверки работоспособности токена
                    if self.selection == 3:  # если пользователь выбрал редактировать конфиг, шлем его сюда
                        conn = sqlite3.connect('config.db')
                        cur = conn.cursor()
                        cur.execute('UPDATE info SET token_vk="%s"' % (self.token))
                        conn.commit()
                        conn.close()
                        print('Токен успешно сменён!')
                        self.edit_config()
                        break
                    else:
                        self.userid_invite()
                        break
                else:
                    print(f'Ваш токен содержит {len(self.token)} символов, а должен 85 или 198. Повторите попытку.')
            except Exception as e:
                print(f'\nПроизошла ошибка:\n{e}')

    def authorization_logpass(self):
        while True:
            try:
                number = input('\nВведите номер: ')
                password = input('Введите пароль: ')
                url = f"https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB" \
                      f"1inYsH&username={number}&password={password}"
                ke = requests.get(url).json()
                vk = self.token = ke['access_token']  # получаем токен
                vk_api.VkApi(token=self.token)  # авторизовываемся в вк для проверки работоспособности токена
                if self.selection == 3:  # если пользователь выбрал редактировать конфиг, шлем его сюда
                    conn = sqlite3.connect('config.db')
                    cur = conn.cursor()
                    cur.execute('UPDATE info SET token_vk="%s"' % (self.token))
                    conn.commit()
                    conn.close()
                    print('Токен успешно сменён!')
                    self.edit_config()
                    break
                else:
                    self.userid_invite()
                    break
            except Exception as e:
                print(f'\nПроизшла ошибка:\n{e}')

    def userid_invite(self):
        while True:
            try:
                self.user_id = input('\nВведите айди пользователей которых будем добавлять в беседу(если пользователей '
                                     'больше одного, вводите значения через запятую вот так: 1, 2, 3)\n')
                if self.selection == 3:  # если пользователь выбрал редактировать конфиг, шлем его сюда
                    conn = sqlite3.connect('config.db')
                    cur = conn.cursor()
                    cur.execute('UPDATE info SET id="%s"' % (self.user_id))
                    conn.commit()
                    conn.close()
                    print('Айди успешно сменены!')
                    self.edit_config()
                    break
                else:
                    self.title()
                    break
            except Exception as e:
                print(f'\nПроизошла ошибка:\n{e}')

    def title(self):
        while True:
            try:
                self.chat_title = input('\nВведите название беседы, которое будем ставить\n')
                if self.selection == 3:  # если пользователь выбрал редактировать конфиг, шлем его сюда
                    conn = sqlite3.connect('config.db')
                    cur = conn.cursor()
                    cur.execute('UPDATE info SET title="%s"' % (self.chat_title))
                    conn.commit()
                    conn.close()
                    print('Название успешно сменено!')
                    self.edit_config()
                    break
                else:
                    self.count_messages()
                    break
            except Exception as e:
                print(f'\nПроизошла ошибка:\n{e}')

    def count_messages(self):
        while True:
            try:
                self.count = input('Введите количество сообщений, которое нужно накрутить: ')
                if self.selection == 2:
                    conn = sqlite3.connect('config.db')
                    cur = conn.cursor()
                    cur.execute('INSERT INTO info VALUES("%s", "%s", "%s", "%s")'
                                % (self.token, self.user_id, self.chat_title, self.count))
                    conn.commit()
                    conn.close()
                    print('Настройка конфига завершена. Возвращаю вас в меню.')
                    self.mode_selection()
                    break
                elif self.selection == 3:  # если пользователь выбрал редактировать конфиг, шлем его сюда
                    conn = sqlite3.connect('config.db')
                    cur = conn.cursor()
                    cur.execute('UPDATE info SET count="%s"' % (self.count))
                    conn.commit()
                    conn.close()
                    print('Количество успешно изменено!')
                    self.edit_config()
                    break
                else:
                    print('\nНастройка успешно завершена!\nИдет запуск скрипта.\n')
                    Work().boost(self.token, self.user_id, self.count, self.chat_title)
                    break
            except Exception as e:
                print(f'\nПроизошла ошибка:\n{e}')


class Work:
    def enter_arms(self, captcha):
        key = input(f"Введите капчу {captcha.get_url()}:\n").strip()
        return captcha.try_again(key)

    def boost(self, token, user_id, count, title):
        vk = vk_api.VkApi(token=token, captcha_handler=self.enter_arms)
        for num in range(count):
            try:
                chat_id = vk.method('messages.createChat', {'user_ids': user_id, 'title': title})
                if num + 1 == count:
                    print(f'Беседа №{num + 1} создана!\nЕе айди: {chat_id}')
                    print('\nЗаданное количество сообщений было успешно накручено!\nВозвращаю вас в меню\n')
                    Menu().mode_selection()
                else:
                    print(f'Беседа №{num + 1} создана!\nЕе айди: {chat_id}\n')
                    for second in range(30):
                        print(f'Прошло секунд {second + 1}... Осталось {30 - second - 1}с ', end='\r')
                        time.sleep(1)
                    print('\n')
            except Exception as e:
                print(f'Ошибка: {e}\nБеру перерыв 600 секунд\n')
                time.sleep(600)


if __name__ == '__main__':
    Menu().intro()
