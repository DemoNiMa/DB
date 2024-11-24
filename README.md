## Установка и настройка MongoDB на Ubuntu 22.04

Шаг 1. Установка MongoDB

1.  Обновите пакеты:
```sudo apt update && sudo apt upgrade -y```
    
2.  Импортируйте ключ репозитория MongoDB: 
``` bash
curl -fsSL [https://pgp.mongodb.com/server-6.0.asc](https://pgp.mongodb.com/server-6.0.asc) | sudo gpg --dearmor -o /usr/share/keyrings/mongodb-server-6.0.gpg
```
    
3.  Добавьте репозиторий MongoDB: 
```
echo "deb [signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
```
    
4.  Установите MongoDB: sudo apt update sudo apt install -y mongodb-org
    
5.  Запустите MongoDB и настройте автозапуск: sudo systemctl start mongod sudo systemctl enable mongod
    
6.  Проверьте статус службы: sudo systemctl status mongod
    

Шаг 2. Настройка для удалённого подключения

1.  Откройте конфигурационный файл MongoDB: sudo nano /etc/mongod.conf
    
2.  Измените настройку bindIp для разрешения подключений со всех IP: net: bindIp: 0.0.0.0 port: 27017
    
3.  Убедитесь, что авторизация отключена (секция security должна быть закомментирована или отсутствовать): #security:
    

# authorization: enabled

4.  Перезапустите MongoDB для применения изменений: sudo systemctl restart mongod

Шаг 3. Настройка файервола

1.  Убедитесь, что порт 27017 открыт для внешних подключений:

Если используется UFW: sudo ufw allow 27017/tcp sudo ufw enable

Если используется iptables: sudo iptables -A INPUT -p tcp --dport 27017 -j ACCEPT

2.  (Опционально) Ограничьте доступ только для определённого IP: sudo iptables -A INPUT -p tcp -s YOUR_HOME_IP --dport 27017 -j ACCEPT sudo iptables -A INPUT -p tcp --dport 27017 -j DROP

Шаг 4. Подключение с другого устройства

1.  Убедитесь, что клиент MongoDB установлен на вашем ПК: sudo apt install mongodb-clients
    
2.  Подключитесь к серверу с вашего домашнего ПК: mongosh "mongodb://195.133.13.249:27017"
