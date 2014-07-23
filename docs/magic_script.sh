find $1  -type f | while read FILENAME; do
# здесь что-то с файлами делаем
echo "$FILENAME"



tr -d '\r' < "$FILENAME" > "$FILENAME+1"

rm "$FILENAME"

mv "$FILENAME+1" "$FILENAME"


done
