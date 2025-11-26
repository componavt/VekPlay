#!/bin/bash
#
# Script to dump all VepKar database tables structure.
# Asks for user credentials, generates a dump file with the current date,

# Ask for user credentials
read -p "Enter MariaDB username: " user_name
echo -n "Enter MariaDB password: "
stty -echo  # Отключаем эхо-вывод (скрываем ввод пароля)
read password
stty echo   # Включаем эхо-вывод обратно
echo

sudo mysqldump -u "$user_name" -p"$password" \
    --no-data \
    --default-character-set=utf8mb4 \
    --single-transaction \
    --skip-add-drop-table \
    vepkar > vepkar_structure_$(date +"%Y%m%d").sql

echo "Database structure dump completed and compressed."
