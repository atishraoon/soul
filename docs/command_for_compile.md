# soul  

--

**command to compile**

```sh
pyinstaller --onefile --windowed --add-data "core;core" --add-data "env/Lib/site-packages/pygame_gui/data;pygame_gui/data" main.py

```

**project tree**

```
project/
├── core/
│   ├── ui_components/
│   │   ├── popupwindow.py
│   │   ├── alertpopup.py
│   │   ├── .... (other files)
│   ├── level.json
│   ├── level.py
│   ├── settings.py
│   ├── .... (other files)
├── main.py

```



**success 100%**
```sh
 pyi-makespec --onefile --add-data "core/level.json;core" --add-data "core;core" --add-data "env/Lib/site-packages/pygame_gui/data;pygame_gui/data" main.py
 ```
```sh
pyinstaller main.spec

```


 

**replicate command success 100%**

```sh
pyinstaller --onefile --windowed --icon=env/icon.ico --add-data "core/level.json;core" --add-data "core;core" --add-data "env/Lib/site-packages/pygame_gui/data;pygame_gui/data" main.py

```



**other**
```sh
 --add-data "core/ui_components/*.py;core/ui_components
```
