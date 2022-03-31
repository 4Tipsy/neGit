# coding:utf8
import os, string, json, datetime, shutil, codecs


# --------------------------- #
# -   собственно логотип    - #
# --------------------------- #
windowLen = 121 #длина окна скрипта
os.system(f"mode con:cols={windowLen} lines=29") #устанавливаем длину окна скрипта
logo = "@4Tipsy - neGit v1.1"

print(windowLen * "#")
print("###" + (windowLen - 6)*" " + "###")
t = int(((windowLen - 6) - len(logo)) / 2)
print("###" + " "*t + logo + " "*t + " ###")
print("###" + (windowLen - 6)*" " + "###")
print(windowLen * "#")
print("*хранилище не должно находиться в копируемой папке,/n иначе будет вечное самокопирование")


# readme
print("Показать [readme]?")
showReadme = input("(1-yes // [any]-no)")
if showReadme == "1":
    print(windowLen * "-")
    with codecs.open("README.md", encoding="utf-8") as readme:
        lines = readme.readlines()
        for line in lines:
            print(line.strip())
    print(windowLen * "-")

# --------------------------- #
# - использование пресетов  - #
# --------------------------- #

presetUsed = False
with open("presets.json", "r") as read_file:
    presets = json.load(read_file)
if len(presets) > 0:
    print("Использовать пресет?")
    if input("(1-yes // [any]-no)") == "1":
        print(presets.keys())
        while True:
            try:
                temp = input("Название пресета(0-выход) > ")
                if temp == "0":
                    break
                chosenPreset = presets[temp]

                STORAGE = chosenPreset[0]
                FILES = chosenPreset[1]
                presetUsed = True #для пропуска выбора файлов
                break
            except:
                print("-неправильное название-")
else:
    print("У вас нет пресетов")



# --------------------------- #
# -      выбор файлов       - #
# --------------------------- #

if not presetUsed:
    # выбираем хранилище
    print("Выберите хранилище")
    useDefaultStorage = input("(1-[defaultStorage] // [any]-choose)")
    if useDefaultStorage == "1":
        print(f"Хранилище - {os.path.abspath('storage')}")
        STORAGE = os.path.abspath('storage')
        print(f"Хранилище содержит: {os.listdir(STORAGE)}")
        
    else:
        print(f"Доступные диски: {['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]}")   

        while True:
            thisDir = input("Выберите папку > ")
            if os.path.exists(thisDir):
                print(f"Путь - {os.path.abspath(thisDir)}")
                print(f"Папка содержит: {os.listdir(thisDir)}")

                print("Выбрать эту папку?")
                if input("(1-yes // [any]-no)") == "1":
                    print(f"Хранилище - {os.path.abspath(thisDir)}")
                    print(f"Хранилище содержит: {os.listdir(thisDir)}")
                    STORAGE = os.path.abspath(thisDir)
                    break
                
            else:
                print("-такой папки не сущетсвует-")


    # выбираем файлы
    print("Выберите файлы для копирования")
    print(f"Доступные диски: {['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]}")
    print("-не выбирайте файлы noGit'а, иначе [storage] будет копироваться до бесконечности!-")
    while True:
            thisDir = input("Выберите папку > ")
            if os.path.exists(thisDir):
                if os.getcwd() == os.path.abspath(thisDir):
                    print("-выбрана папка скрипта! нельзя так делать!-")
                    print("-закрытие программы...-")
                    os.abort()
                print(f"Путь - {os.path.abspath(thisDir)}")
                print(f"Папка содержит: {os.listdir(thisDir)}")

                print("Выбрать эту папку?")
                if input("(1-yes // [any]-no)") == "1":
                    print(f"Файлы - {os.path.abspath(thisDir)}")
                    FILES = os.path.abspath(thisDir)
                    break
                
            else:
                print("-такой папки не сущетсвует-")


# --------------------------- #
# -   копирование файлов    - #
# --------------------------- #
def mycopy(src, dst, follow_symlinks=True):
    print(src,"→",dst, end='\r')
    return shutil.copy2(src, dst, follow_symlinks=follow_symlinks)

# так мы назовем сейв
saveName = "sv" + datetime.datetime.today().strftime("(%Y-%m-%d)(%H-%M-%S)") + os.path.basename(FILES)

shutil.copytree(FILES, (STORAGE + "\\" + saveName), copy_function=mycopy)
with open((STORAGE + "\\" + saveName + "\\" + "info.txt"), "w") as file:
    file.write(f"Copied from {FILES}\n{logo}")
    
print("-завершено-")
print("-результат: " + str(os.path.exists(STORAGE + "\\" + saveName)) + "-")
print("Сохранено как: " + os.path.basename(STORAGE + "\\" + saveName))



# --------------------------- #
# -    создание пресета     - #
# --------------------------- #

if not presetUsed:
    print("Вы не использывали пресет!")
    print(windowLen * "-")
    print("Сохранить [данные] как пресет?")
    print(f"-->{STORAGE} -хранилище")
    print(f"-->{FILES} -то, что вы сохраняли")
          
    if input("(1-yes // [any]-no)") == "1":
        presetName = input("Название пресета(use only eng plz) > ")
        presets[presetName] = [STORAGE, FILES]
        print(f"presets[{presetName}] = [{STORAGE}, {FILES}]")
          
        if input("Подтвердить?(1-yes // [any]-no)") == "1": 
            with open("presets.json", "w") as write_file:
                json.dump(presets, write_file)


input("-работа скрипта завершена-")



























    
