### ПОИСК СВОБОДНЫХ РЕСУРСОВ НА ОРБИТАХ ПЛАНЕТ ###

### ТРЕБОВАНИЯ ###
* Python v>=3.6
* `apt-get install python3-selenium chromium-chromedriver`
* `pip3 install lxml`

### ЗАПУСК ###
* `python3 run.py --login="${LOGIN}" --password="${PASSWORD}"` - просмотр всех галактик и систем
* `python3 run.py --login="${LOGIN}" --password="${PASSWORD}" --galaxy=${GALAXY}` - просмотр указанной галактики
* `python3 run.py --login="${LOGIN}" --password="${PASSWORD}" --galaxy=${GALAXY} --system=${SYSTEM}` - просмотр указанной системы в указанной галактике
* за просмотр каждой страницы игрой взимается 10 водорода

### АВТОР ###
Шатров Алексей Сергеевич <mail@ashatrov.ru>