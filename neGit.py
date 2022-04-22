# coding:utf8
import os, string, json, datetime, time, shutil, codecs, sys


# --- флаги(опции) скрипта -- #
FLAG__useWin_XCopy = True                  # использует более быстрый xcopy для windows
FLAG__remove_ignoredTxt_after_copy = True  # удаляет ignored.txt (нужен, чтобы записать в него IGNORED для xcopy)


# --------------------------- #
# -       лого и readme     - #
# --------------------------- #
windowLen = 121 #длина окна скрипта
if sys.platform == "win32":
    os.system(f"mode con:cols={windowLen} lines=29") #устанавливаем длину окна скрипта
    
logo = "@4Tipsy - neGit v5.0"

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
            if "*" in line:
                print(line.strip())

    print(windowLen * "-")
    print("\n")
except:
    print("\n","-не удалось открыть/найти readme-","\n")

# --------------------------- #
# - использование пресетов  - #
# --------------------------- #

presetUsed = False # по дефолту

with open("presets.json", "r", encoding='utf-8') as read_file:
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
                    print(f"{presetName}: {preset4info['storage']} <-- {preset4info['files']}, ignored:{preset4info['ignored']}, prename:{preset4info['prename']}")
                    print(f"{presetName}: alwaysUseShutil == {preset4info['alwaysUseShutil']}")
                    print("\n")
                    
                    

                elif presetName == "0":
                    break
                else:
                    chosenPreset = presets[presetName]

                    alwaysUseShutil = chosenPreset["alwaysUseShutil"]
                    STORAGE = chosenPreset["storage"]
                    FILES = chosenPreset["files"]
                    IGNORED = chosenPreset["ignored"]
                    PRENAME = chosenPreset["prename"]
                
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
    useDefaultStorage = input("(1-[defaultStorage] // 4-[4test] // [any]-choose)")

    if useDefaultStorage == "1":
        print(f"Хранилище - {os.path.abspath('storage')}")
        STORAGE = os.path.abspath('storage')
        print(f"Хранилище содержит: {os.listdir(STORAGE)}")

    elif useDefaultStorage == "4":
        print(f"Хранилище - {os.path.abspath('4test')}")
        STORAGE = os.path.abspath('4test')
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
                print("-такой папки не существует-")


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
                print(f"{os.path.basename(STORAGE)}-(выбранное хранилище) уже указано по умолчанию, во избежание бесконечного копирования")
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
                        print("-такой папки не существует-")
                
                FILES = os.path.abspath(thisDir)
                break
            
        else:
            print("-такой папки не существует-")


    print("\nИспользовать ВСЕГДА(если это пойдет в пресет) ИМЕННО py_shutil при копировании?")
    if input("(1-yes // [any]-no)") == 1:
        alwaysUseShutil = 1
    else:
        alwaysUseShutil = 0




# --------------------------- #
# -   копирование файлов    - #
# --------------------------- #
def mycopy(src, dst, follow_symlinks=True):
    print(os.path.basename(STORAGE), "<- ", src, " "*(windowLen-len(src)), end='\r')
    return shutil.copy2(src, dst, follow_symlinks=follow_symlinks)
def myignore(path, filenames):
    toReturn = []
    for filename in filenames:
        if filename in IGNORED:
            toReturn.append(filename)
    return toReturn


# для названия сейва
name_ = input("\nНазвание(причина) бекапа > ") 
if not presetUsed:
    PRENAME = input("preName > ")


# для info файла
reasonTexted = input("Назовите причину бекапа > ")
print("\n")

# так мы назовем сейв
saveName = PRENAME + "("+ name_ +")" + datetime.datetime.today().strftime("(%Y-%m-%d)(%H-%M-%S)")


# ----- само копирование ---- #
copyStartTime = time.time()
# для windows
if (sys.platform == "win32") and (FLAG__useWin_XCopy) and (alwaysUseShutil == 0):
    methodUsed = "win_xcopy"

    # создаем файл игнорирования
    with open("ignored.txt", "w", encoding="utf-8") as write_file:
        for i in IGNORED:
            write_file.write(f"\\{i}\\\n")

    # копируем файлы
    path_ = STORAGE+'\\'+saveName
    os.system(f"mkdir {path_}")
    os.system(f'xcopy "{FILES}" "{path_}" /E /H /exclude:ignored.txt')
    print("если тут не все файлы, скорее всего их просто не назвало(и такое бывает...)")

    # удаляем файл игнорирования
    if FLAG__remove_ignoredTxt_after_copy:
        os.remove(os.path.abspath('ignored.txt'))


# в остальных случаях
else:
    methodUsed = "py_shutil"
    shutil.copytree(FILES, (STORAGE + "\\" + saveName),ignore=myignore , copy_function=mycopy)


# создание info файла
with open((STORAGE + "\\" + saveName + "\\" + "info.txt"), "w", encoding='utf-8') as file:
    file.write(f"Copied from {FILES} by {methodUsed}{'(принуд)' if alwaysUseShutil == 1 else ''}\nIgnored: {IGNORED}\n\nWhy backuped: {reasonTexted}\n{logo}")
 

print("\n")
print(f"метод: {methodUsed}{'(принуд)' if alwaysUseShutil == 1 else ''} | {time.time() - copyStartTime} sec")
print("Сохранено как: " + os.path.basename(STORAGE + "\\" + saveName))


# --------------------------- #
# -    создание пресета     - #
# --------------------------- #

if not presetUsed:
    print("Вы не использовали пресет!")
    print(windowLen * "-")
    print("Сохранить [данные] как пресет?")
    print(f"[!] alwaysUseShutil == {alwaysUseShutil}")
    print(f"-->{STORAGE} -хранилище")
    print(f"-->{FILES} -то, что вы сохраняли")
    print(f"-->{IGNORED} -проигнорированно")
    print(f"-->{PRENAME} -префикс пред именем сейва")
          
    if input("(1-yes // [any]-no)") == "1":
        while True:
            newPresetName = input("Название пресета > ")
            print(f"presets[{newPresetName}] = {STORAGE} <- {FILES}, ignored:{IGNORED}, prename:{PRENAME}")
            if input("Подтвердить имя?(1-yes // [any]-no)") == "1":
                break

        presets[newPresetName] = {}
        presets[newPresetName]["alwaysUseShutil"] = alwaysUseShutil
        presets[newPresetName]["storage"] = STORAGE
        presets[newPresetName]["files"] = FILES
        presets[newPresetName]["ignored"] = IGNORED
        presets[newPresetName]["prename"] = PRENAME
         
        with open("presets.json", "w", encoding="utf-8") as write_file:
            json.dump(presets, write_file, indent=4)
        print("-пресет создан-")


# ---- завершение работы ---- #
print("\n")
print("-работа скрипта завершена-")



# если ты это читаешь, я оч признателенXD