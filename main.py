import zipfile
import hashlib
import requests
import re
import os
import csv
import pandas as pd


# Задание №1
directory_to_extract_to = r"C:\Users\Георгий\PycharmProjects\Lub_1\место_под_архив"
arch_file = "C:\\Users\\Георгий\\Downloads\\tiff-4.2.0_lab1.zip"
'''
os.mkdir(directory_to_extract_to)

test_zip = zipfile.ZipFile(arch_file)

test_zip.extractall(directory_to_extract_to)

test_zip.close()
'''
os.chdir(directory_to_extract_to)

# Задание №2.1
file = open("txt_files.txt", "w")

for r, d, f in os.walk(os.getcwd()):
    for i in f:
        if i.endswith('.txt'):
            text = os.path.abspath(i) + '\n'
            file.write(text)

file.close()

# Задание №2.2
fl = open("txt_files.txt", "rb")

for f in fl:
    result = hashlib.md5(f).hexdigest()
    print(result)
fl.close()

directory_to_extract_to = directory_to_extract_to + "\\"

# Задание №3
target_hash = '4636f9ae9fef12ebd56cd39586d33cfb'
target_file = ''  # полный путь к искомому файлу
target_file_data = ''  # содержимое искомого файла

for r, d, f in os.walk(directory_to_extract_to):
    for i in f:
        if i.endswith('.sh'):
            file_tmp = open(r + '\\' + i, 'rb').read()
            result = hashlib.md5(file_tmp).hexdigest()
            if target_hash == result:
                target_file = r + '\\' + i
                target_file_data = open(target_file, 'r').read()
                break

print(target_file + '\n')
print(target_file_data)

# Задание №4
r = requests.get(target_file_data)
result_dct = {}

lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)

headers = re.sub("<.*?>", " ", lines[0])
headers = re.sub("\  +", " ", headers)
del lines[0]
size = len(lines) - 1
counter = 0
head = headers.split(" ")
del head[0]
result_dct.update({"Заголовки": (head[0], head[1], head[2], head[3] + "-" + head[4])})
for line in lines:
    temp = re.sub("<.*?>", ';', line)
    temp = re.sub(r'\(.+?\)', '', temp)
    temp = re.sub(r'/\xF0\x9F\x93\x9D/u', '', temp)
    temp = re.sub("\;+", ';', temp)
    tmp_split = temp.split(";")

    if counter != size:
        del tmp_split[0]
        country_name = tmp_split[0]
        country_name = country_name[country_name.find(" ") + 2:]
    else:
        del tmp_split[0]
        del tmp_split[0]
        country_name = tmp_split[0]

    if tmp_split[3] == '0*':
        tmp_split[3] = 0
    if tmp_split[3] != '0' and tmp_split[3] != 0:
        tmp_split[3] = re.sub('\xa0', "", tmp_split[3])
    if tmp_split[4] == '_':
        tmp_split[4] = -1
    if tmp_split[4] != -1:
        tmp_split[4] = re.sub('\xa0', "", tmp_split[4])
    col1_val = re.sub('\xa0', "", tmp_split[1])
    col2_val = re.sub('\xa0', "", tmp_split[2])
    col3_val = tmp_split[3]
    col4_val = re.sub(r'\s', '', str(tmp_split[4]))
    result_dct.update({country_name: (col1_val, col2_val, col3_val, col4_val)})
    counter += 1
    #for key, value in result_dct.items():
        #print(key, ':', value)

# Задание №5
# Запись данных из полученного словаря в файл
'''
output = open('data.csv', 'w')
for key, value in result_dct.items():
    output.write(key + " ")
    output.write(str(value) + "\n")
output.close()
'''
output = open('data.csv', 'w')
writer = csv.writer(output, delimiter=",")
for key, val in result_dct.items():
    writer.writerow([key, val[0], val[1], val[2], val[3]])
output.close()
'''
# Задание №6
target_country = input("Введите название страны: ")
print(result_dct.get("Заголовки"))
print(result_dct.get(target_country))
'''

def sum(array: list, start: int, end: int) -> int:
    sum = 0
    for i in range(end - start):
        sum = sum + array[start + i]
    return sum

df = pd.read_csv('data.csv', encoding='cp1251')
arr = df['Заболели']
size = len(arr) - 1
rez = sum(arr, 0, size)
print(rez)
