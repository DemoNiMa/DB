# **Установка и настройка Redis на Ubuntu 22.04**

## 1. Установка Redis

1.  **Обновите пакеты:**
```
sudo apt update && sudo apt upgrade -y
```
2. **Установите Redis**:
```
sudo apt install redis-server
```
## 2. Настройка Redis (Для удаленного подключения)
1. ** Файл конфигурации находится по адресу `/etc/redis/redis.conf`** 
```
sudo nano /etc/redis/redis.conf
```
- ```bind 0.0.0.0```
- ```protected-mode no```
- ```requirepass your_redis_password```
2. **Настройте брандмауэр** (Убедитесь, что порт по умолчанию для Redis (6379) открыт для удаленных подключений): 
```
sudo ufw allow 6379
```

3. **Перезагрузите Redis, чтобы изменения вступили в силу**:
```
sudo systemctl restart redis-server
```
4. **Проверьте статус Redis**:
```
sudo systemctl status redis-server
```
5. **Подключение к Redis:**
```
redis-cli -h your_redis_server_ip -p 6379 -a your_redis_password
```
