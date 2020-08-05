# выгрузка статей из https://vk.com/@yvkurse в .csv файл
API vk.com на момент получения задания не дает возможности рабоатать со статьсями. Полный список статей в группе может получить только зарегистрированный пользователь, поэтому пришлось использовать браузер в headless режиме. Для установки chrome на ubuntu server см. https://gist.github.com/ipepe/94389528e2263486e53645fa0e65578b

## Установка
```
git clone https://github.com/scherbininvladimir/yvkurse
cd yvkurse
pip3 install -r requirements.txt
```

## Настройка
Нужно создать файл .env с таким содержанием
```
LOGIN="<Ваш логин vk.com>"
PASSWORD="<Ваш пароль vk.com>"
```

## Запуск
```
python3 get_csv.py
```
