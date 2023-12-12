import win32api
import win32file
import os
import json
from xml.dom import minidom
import xml.etree.ElementTree as ET
import zipfile


# 1ое задание
DRIVE_TYPES = """
0 	Unknown
1 	No Root Directory
2 	Removable Disk
3 	Local Disk
4 	Network Drive
5 	Compact Disc
6 	RAM Disk
"""


def get_drives_info():
    drive_list = win32api.GetLogicalDriveStrings()
    drive_list = drive_list.split("\x00")[0:-1]
    dict_drives = {}
    for drive in drive_list:
        drive_type = win32file.GetDriveType(drive)
        drive_size = win32file.GetDiskFreeSpace(drive)
        drive_volume = win32file.GetVolumePathName(drive)
        dict_drives[str(drive)] = {
            'type': drive_types[drive_type],
            'size': round((drive_size[0] * drive_size[1] * drive_size[3]) / (1024 * 1024 * 1024), 1),
            'free_size': round(drive_size[0] * drive_size[1] * drive_size[2] / (1024 * 1024 * 1024), 1),
            'volume_label': drive_volume if drive_volume != drive else "Don't have volume label"
        }
    return dict_drives


drive_types = dict((int(i), j) for (i, j) in (l.split("\t") for l in DRIVE_TYPES.splitlines() if l))
drives_data = get_drives_info()
for disk in drives_data.keys():
    s = f'''
    Название: {disk}
    Тип: {drives_data[disk]['type']}
    Пространство: {drives_data[disk]['size']} GiB
    Свободное пространство: {drives_data[disk]['free_size']} GiB
    Метка: {drives_data[disk]['volume_label']}
    '''
    print(s)


v = input('Выберите задание, введя цифру:\n'
          '1. Работа с файлами\n'
          '2. Работа с форматом JSON\n'
          '3. Работа с форматом XML\n'
          '4. Создание zip архива, добавление туда файла, определение размера архива\n')


match v:
    case '1':
        # 2ое задание
        def filework():
            name = input("Введите название файла: ")
            my_file = open(name, "wt")
            text = input("Введите, что записать в файл: ")
            print(text, file=my_file, sep=" ", end=" ")
            my_file.close()
            my_file = open(name, "r")
            print(my_file.read())
            my_file.close()
            os.remove(name)

        filework()
        
    case '2':
        # 3е задание
        class Person:
            def __init__(self):
                self.first_name = firstname
                self.last_name = lastname
                self.age = age
                self.gender = gender

        firstname = input('Введите имя: ')
        lastname = input('Введите фамилию: ')
        age = input('Введите возраст: ')
        gender = input('Введите пол: ')

        data = Person()

        with open("data_file.json", "w") as write_file:
            json.dump(data.__dict__, write_file)
        with open("data_file.json", "r") as read_file:
            json_data = json.load(read_file)

        print(json_data)
        os.remove('data_file.json')

    case '3':
        # 4е задание
        root = minidom.Document()

        xml = root.createElement('root')
        root.appendChild(xml)

        productChild = root.createElement('Person')
        productChild.setAttribute('Firstname', input("Введите имя: "))
        productChild.setAttribute('Lastname', input("Введите фамилию: "))
        productChild.setAttribute('Age', input("Введите возраст: "))
        productChild.setAttribute('Gender', input("Введите пол: "))

        xml.appendChild(productChild)

        xml_str = root.toprettyxml(indent="\t")

        save_path_file = "data_file.xml"

        with open(save_path_file, "w") as f:
            f.write(xml_str)
        tree = ET.parse('data_file.xml')
        root = tree.getroot()
        print(root)
        print(root[0].attrib)
        os.remove('data_file.xml')

    case '4':
        # 5е задание
        archive = zipfile.ZipFile('Data.zip', mode='w')
        zipfilename = input('Введите название файла, который попадет в архив: ')
        my_filezip = open(zipfilename, "wt")
        textzip = input("Введите, что записать в файл: ")
        print(textzip, file=my_filezip, sep=" ", end=" ")
        my_filezip.close()
        archive.write(zipfilename)
        archive.close()
        os.remove(zipfilename)
        archive = zipfile.ZipFile('Data.zip', 'r')
        print("Файлы в архиве: ")
        archive.printdir()
        print("Извлечение...")
        archive.extractall()
        archive.close()
        print("Удаление файла и архива...")
        os.remove(zipfilename)
        os.remove("Data.zip")
