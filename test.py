#test.py

import subprocess
import os
import shutil


def create_temp_directory(): #создаем папку на которой будем запускать скрипт
    temp_dir = os.path.join(os.getcwd(), 'test_directory') 
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir


def fill_directory_with_files(directory, percentage):
    
    total_size = get_directory_size(directory)  # размер диска
    target_size = total_size * percentage // 100 # желаемый размер
    current_size = get_directory_usage(directory) * total_size // 100 # сейчас заполнено
    file_counter = 0
    #
    #
    while current_size < target_size and target_size-current_size > 1024: # заполняем текстовыми файлами
        print(f"#Fillin' with a bunch of useless files{file_counter}#")
        print(current_size)
        print(target_size)
        print(total_size)
        filename = f'file_{file_counter}.txt'
        filepath = os.path.join(directory, filename)
        file_counter += 1
        with open(filepath, 'wb') as f:
            f.write(os.urandom(1024))  # создаем файл размером 1024 б
        current_size += 1024*8
        ###
        #print(current_size/target_size)

def run_script(script_path, *args):
    result = subprocess.run(['bash', script_path] + list(args)) #, capture_output=True, text=True  - у нас же нет текстового вывода, поэтому это нам не надо
    return result # можно же наверное ничего не возвращать

def check_backup_archives():
    archives = [f for f in os.listdir('/tmp') if f.startswith('backup_') and f.endswith('.tar.gz')] 
    return archives #вернет список архивов

def get_directory_usage(directory): #процент заполнения диска
    total, used, free = shutil.disk_usage(directory)
    return (used / total) * 100

def get_directory_size(directory): #размер диска
    total, used, free = shutil.disk_usage(directory)
    return total

def main():
    correct_working = True
    wrong_arc = False
    wrong_us = False

    actual_dir = create_temp_directory()
    temp_dir = "test_directory"

    cur_proc_usage = 20
    max_proc_usage = 10

    run_script('./prepare.sh', temp_dir, cur_proc_usage)

    #заполняем папку на 20%
    fill_directory_with_files(temp_dir, cur_proc_usage)

    will_there_be_archives = False
    if( get_directory_usage(temp_dir) > max_proc_usage):
        will_there_be_archives =True

    run_script('./lab.sh', temp_dir, max_proc_usage, '2')

        
    #проверяем насколько заполнено
    usage = get_directory_usage(temp_dir)
    if(usage > max_proc_usage):
        correct_working = False
        wrong_us = True
        #print("Ошибка, папка {temp_dir} заполнена на {usage:.2f}%")
        
    #проверяем наличие архивов
    archives = check_backup_archives()
    counter = 0
    if archives:
        counter+=1
    if will_there_be_archives and counter == 0:
        correct_working = False
        wrong_arc = True
        #print("Архивов нет")

    if correct_working:
        print("Все работает без проблем")
    else:
        print("Отработало с ошибками")
        if wrong_us:
            print("Ошибка, папка {temp_dir} заполнена на {usage:.2f}%")
        if wrong_arc:
            print("Архивов нет")

    

if __name__ == "__main__":
    main()