# terminal-AI

Проект для интеграции  искусственного интеллекта посредством API в консоли пользователя. На данный момент реализовано:

- Основаная логика программы (обработка токенов AI, запросов API);
- Обработка возможных ошибок время запуска программы (наличие токенов в окружении, получение ответа от сервиса, проверка документации и т.д.);
- Логирование программы с выводом ошибок;
- Ввод пользовательского запроса;
- Вывод ответа Искусственного интеллекта;
- Контекст чата обрабатывается и обновляется во время работы программы.
- Обработка текста markdown, текст AI отличается от текста User;
- Удобная настройка через конфниги;
- Loader во время обработки запроса.

В планах:
- [ ] Написать README по кастомизации текста;
- [ ] Запуск программы по ключевым словам;
- [ ] Интеграция PostgreSQL в программу.

Известные баги:
- Периодически не обрабатывает Markdown;
- Рекурсия при наличии в запросе пропуска строки.