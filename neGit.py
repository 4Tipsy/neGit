# coding:utf8
import os, string, json, datetime, shutil, codecs


# --------------------------- #
# -       лого и readme     - #
# --------------------------- #
windowLen = 121 #длина окна скрипта
os.system(f"mode con:cols={windowLen} lines=29") #устанавливаем длину окна скрипта
logo = "@4Tipsy - neGit v3.1"

print(windowLen * "#")
print("###" + (windowLen - 6)*" " + "###")
t = int(((windowLen - 6) - len(logo)) / 2)
print("###" + " "*t + logo + " "*t + " ###")
print("###" + (windowLen - 6)*" " + "###")
print(windowLen * "#")

# readme
try:
    with codecs.open("README.md", encoding="utf-8") as readme:
        print("\n")
        print(windowLen * "-")
        lines = readme.readlines()
        for line in lines:
            print(line.strip())
    print(windowLen * "-")
    print("\n")
except:
    print("\n","-не удалость открыть/найти readme-","\n")

# --------------------------- #
# - использование пресетов  - #
# --------------------------- #

presetUsed = False
with open("presets.json", "r") as read_file:
    presets = json.load(read_file)
if len(presets) > 0:
    print("Использовать пресет?")
    if input("(1-yes // [any]-no)") == "1":
        print("пресеты:",presets.keys())
        while True:
            try:
                presetName = input("Название пресета('?[пресет]'-инфо // 0-выход) > ")
                if presetName[0] == "?":
                    # вывести инфу о пресете
                    preset4info = presets[presetName[1: len(presetName)]]

                    print("-"*windowLen)
                    print(f"{presetName[1: len(presetName)]}(префикс-{preset4info[3]}):")
                    print(f"{preset4info[0]} <-- {preset4info[1]}")
                    print(f"ignored: {preset4info[2]}")
                    print("\n")

                elif presetName == "0":
                    break
                else:
                    chosenPreset = presets[presetName]

                    STORAGE = chosenPreset[0]
                    FILES = chosenPreset[1]
                    IGNORED = chosenPreset[2]
                    PRENAME = chosenPreset[3]
                
                    presetUsed = True #для пропуска выбора файлов и т.д.
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
    print("\n")
    print("Выберите файлы для копирования")
    print(f"Доступные диски: {['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]}")
    while True:
            thisDir = input("Выберите папку > ")
            if os.path.exists(thisDir):
                print(f"Путь - {os.path.abspath(thisDir)}")
                print(f"Папка содержит: {os.listdir(thisDir)}")

                print("Выбрать эту папку?")
                if input("(1-yes // [any]-no)") == "1":

                    print("\n")
                    print(f"Выберите игнорируемые папки из\n {os.listdir(thisDir)}")
                    print(f"{os.path.basename(STORAGE)}-(выбраное хранилище) уже указано по умолчанию, во избежание бесконечного копирования")
                    # реализация игнорирования папок
                    IGNORED = [os.path.basename(STORAGE)]
                    while True:
                        ignore = input("(имя папки или файла // [enter] - подтвердить) > ")
                        if ignore != "" and os.path.exists(os.path.abspath(thisDir)+"//"+ignore):
                            IGNORED.append(ignore)
                            print("ignored:", IGNORED)

                        elif ignore == "":
                            break
                        else:
                            print("-такой папки не сущетсвует-")
                    
                    FILES = os.path.abspath(thisDir)
                    break
                
            else:
                print("-такой папки не сущетсвует-")


# --------------------------- #
# -   копирование файлов    - #
# --------------------------- #

def mycopy(src, dst, follow_symlinks=True):
    print("copying-", src, end='\r')
    return shutil.copy2(src, dst, follow_symlinks=follow_symlinks)
def myignore(path, filenames):
    toReturn = []
    for filename in filenames:
        if filename in IGNORED:
            toReturn.append(filename)
    return toReturn


if not presetUsed:
    PRENAME = input("Какой префикс сделать перед именем сейва? > ")
# так мы назовем сейв
saveName = PRENAME + datetime.datetime.today().strftime("(%Y-%m-%d)(%H-%M-%S)") + os.path.basename(FILES)

shutil.copytree(FILES, (STORAGE + "\\" + saveName),ignore=myignore , copy_function=mycopy)

with open((STORAGE + "\\" + saveName + "\\" + "info.txt"), "w") as file:
    file.write(f"Copied from {FILES}\n{logo}\nIgnored: {IGNORED}")
    
print("\n")
print("-проверка: " + str(os.path.exists(STORAGE + "\\" + saveName)) + "-")
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
    print(f"-->{IGNORED} -проигнорированно")
    print(f"-->{PRENAME} -префикс пред именем сейва")
          
    if input("(1-yes // [any]-no)") == "1":
        newPresetName = input("Название пресета > ")
        presets[newPresetName] = [STORAGE, FILES, IGNORED, PRENAME]
        print(f"presets[{newPresetName}] = [{STORAGE}, {FILES}, ignored:{IGNORED}, prename:{PRENAME}]")
          
        if input("Подтвердить?(1-yes // [any]-no)") == "1": 
            with open("presets.json", "w") as write_file:
                json.dump(presets, write_file)


# ---- завершение работы ---- #
if presetUsed:
    print(f"{STORAGE} <-- {FILES}, ignored:{IGNORED}, prename:{PRENAME}")
input("-работа скрипта завершена-")




# если ты это читаешь, я оч признателенXD