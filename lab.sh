#!/bin/bash

dir_name=$1 # путь до папки для которой зап скрипт
max_percentage=$2 # максимальный допустимый процент заполнения папки
batch_size=$3 # по сколько файлов надо архивировать (если заполнено больше допустимого процента)

percentage=$(df -h | grep ${dir_name} | awk '{ printf("%d", $5); }') #проц исп диска 

i=1
while [ ${percentage} > ${max_percentage} ]; do
    percentage=$(df -h | grep ${dir_name} | awk '{ printf("%d", $5); }')
    echo ${percentage} / ${max_percentage} #наш процент относительно максимального
    if [ -z "$(ls -A "${dir_name}")" ]; then # Проверка на наличие файлов в директории
        break
    fi

    while [ -f "/tmp/backup_${i}.tar.gz" ]; do #что бы архивировать в разные архивы, а не перезаписывать один
        ((i++))
    done
    
    find ${dir_name} -maxdepth 1 -type f -printf '%T@ %p\n' | sort -n | awk -v batch_size=$batch_size 'NR<=batch_size { print $2 }' | tee /tmp/file_list.txt | xargs tar --remove-files -czvf /tmp/backup_${i}.tar.gz #проц исп диска 
    #все файлы отсорт по времени (сначала стар) | выводим только имена файлов (столб 9) без первой строки (NR>1) && первые сколько-то файлов (кол-во меньше или равно batch_size) - печатает 9 столб (назв этих файлов)
    #архивирует эти файлы в /tmp/backup.tar.gz
    #NR - номер обр строки, врем пер в awk
    
done
 