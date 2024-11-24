## Установка и настройка MongoDB SERVER на Ubuntu 22.04

**1. Установка MongoDB** 

1.  Обновите пакеты:
```
sudo apt update && sudo apt upgrade -y
```
    
2.  Импортируйте ключ репозитория MongoDB: 
``` bash
curl -fsSL [https://pgp.mongodb.com/server-6.0.asc](https://pgp.mongodb.com/server-6.0.asc) | sudo gpg --dearmor -o /usr/share/keyrings/mongodb-server-6.0.gpg
```
    
3.  Добавьте репозиторий MongoDB: 
```
echo "deb [signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
```
    
4.  Установите MongoDB:
```
sudo apt update 
sudo apt install -y mongodb-org
```
    
5.  Запустите MongoDB и настройте автозапуск: 
```
sudo systemctl start mongod 
sudo systemctl enable mongod
```
    
6.  Проверьте статус службы: 
```
sudo systemctl status mongod
```
    
 **2. Настройка для удалённого подключения**

7.  Откройте конфигурационный файл MongoDB: 
```
sudo nano /etc/mongod.conf
```

8.  Измените настройку bindIp для разрешения подключений со всех IP: 
```
net: 
	bindIp: 0.0.0.0 
	port: 27017
```
9.  Перезапустите MongoDB для применения изменений:
``` 
sudo systemctl restart mongod
 ```
    
**3. Настройка файервола**

10. Установите UFW
```
sudo apt update
sudo apt install ufw -y
 ```
 11. После установки выполните команды для открытия порта MongoDB + **SSH**:
```
sudo ufw status
sudo ufw allow 27017/tcp
sudo ufw allow 22/tcp
sudo ufw enable
sudo ufw status
```
**4.  Безопасность** 

11. SSH-ключ (желательно несколько)
12. SSH-тунель или VPN
13. Ограничение по IP 
```
sudo iptables -A INPUT -p tcp -s YOUR_HOME_IP --dport 27017 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 27017 -j DROP
```
14. Авторизация

**В файле `/etc/mongod.conf` найти секцию `security` и добавить:**
```
security:
  authorization: enabled
```
**Создайте пользователя для администрирования**:
Подключиться к `mongosh` и создать пользователя:
```
use admin
db.createUser({
  user: "admin",
  pwd: "securepassword",
  roles: [{ role: "root", db: "admin" }]
})
```

Подключение - `"mongodb://admin:securepassword@SERVER_IP:27017/admin"`
