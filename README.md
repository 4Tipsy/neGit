# neGit v6.0
Скрипт, который позволяет делать бекапы чего угодно
 -> тут даже можно игнорировать файлы/папки, которые не надо копировать,
 отметив их в [ignored], тем не менее игнорирование доступно только на "верхнем" уровне


Процесс создания бекапа можно сильно ускорить и делать в пару кликов,
благодаря использованию [пресетов]
 -> когда скрипт выполнится без использование пресета, он предложит вам
 сохранить использованные [хранилище], [копир. файлы] и т.д. как пресет


-------------------------------------------------------------------------------------------------------------------------

*[!] Не допускайте того, чтобы [хранилище] находилось в [копир. файлах], т.к. авто-игнор реализован только на "верхнем" уровне[!]*
 *-> На тот случай, если [хранилище] находится в той же папке, что и [копир. файлы], [хранилище] всегда включено  в [ignored]. Это сделано, чтобы избежать его бесконечного самокопирования!*




# updates:
--6.0:

	1) корректно работает на линуксе! (был устранен недочет с созданием путей из-за которого скрипт
		некорректно работал на линуксе)
	2) мелкие фиксы
--5.x:

	1) добавлены [флаги] для настройки скрипта
	2) в windows теперь используется более быстрое XCOPY (можно отключить во флагах)
	3) второе "дефолтное" хранилище - [4test] (хранилище для теста скрипта и т.д.)
	4) nullifyPresets теперь находится в основном скрипте, а не в отдельном
--4.x:

	1) мелкие(и не очень) улучшения
	2) исправление багов
	3) улучшена читабельность [пресетов]
--3.x:

	1) возможность смотреть информацию о пресетах("?[назв.пресета]" при выборе пресетов)
	2) обновленный readme
--3.0:

	1) [хранилище] всегда включено  в [ignored] для избежания бесконечного самокопирования
	2) фиксы
--2.0:

	добавлена возможность игнорировать файлы и папки при копировании
--1.x:

	мелкие фиксы
	