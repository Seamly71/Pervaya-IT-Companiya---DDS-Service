# Pervaya-IT-Companiya---DDS-Service
Тестовое задание на вакансию Разработчик Python от Никиты Рушковского.
## Ручной деплой на персональный компьютер
* Клонируем репозиторий в текущую рабочую директорию.
```commandline
git clone git@github.com:Seamly71/Pervaya-IT-Companiya---DDS-Service.git
```
* Заполняем переменные окружения.
В репозитории есть шаблонный файл с необходимыми переменными окружения: template.env.
Значения переменных в нем необходимо записать, а затем переименовать в .env.
```commandline
mv template.env .env
```
* При отсутствии оных необходимо установить Docker.
```commandline
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
 
```
И Docker compose.
```commandline
sudo apt install docker-compose-plugin
```
* Запускаем проект.
```commandline
sudo docker compose -f docker-compose.yml up --build
```
* Применяем миграции.
```commandline
sudo docker compose -f docker-compose.yml exec backend python manage.py migrate
```
* Подгружаем фикстуру.
```commandline
sudo docker compose -f docker-compose.yml exec backend python manage.py loaddata fixture
```
* Проект доступен в сети устройства на 80м порту.
```
http://localhost:80/admin/
user: root
password: samplepwd123
```