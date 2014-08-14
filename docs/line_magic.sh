#!/bin/sh
find $1  -type f | while read FILENAME; do
# здесь что-то с файлами делаем
echo "$FILENAME"

sed '1d'  "$FILENAME"
sed -i 1i\ '#!/usr/bin/python3.4' "$FILENAME"



done


