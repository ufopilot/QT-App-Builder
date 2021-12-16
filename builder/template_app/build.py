import json, os
import subprocess
import locale
import shutil


locale.setlocale(locale.LC_ALL,'en-US')

#copy settings folder to dist
#shutil.copytree('gui/settings', 'dist/', dirs_exist_ok=True)
if not os.path.exists("dist/settings"):
    os.makedirs("dist/settings")
    
for __file in ("ui_settings.json", "theme_settings.json"):
    print(f"copy {__file}")
    shutil.copy(f"gui/settings\\{__file}", f"dist/settings/{__file}")

with open("gui/settings/ui_settings.json", "r", encoding='utf-8') as reader:
    settings = json.loads(reader.read())

app_name = settings['window']['app_name']
icon = settings['window']['icon']     

command = ('pyinstaller.exe',
            '--onefile',
            '--windowed',
            '--icon',  icon,
            '--name', app_name,
            '--hidden-import', 'requests',
            '--hidden-import', 'bs4',
            '--hidden-import', 'pyperclip', 
            '--hidden-import', 'cloudscraper',
            '--hidden-import', 'webbrowser',
            '--hidden-import', 'webcolors',
            '--add-data', 'resources_rc.py;.',
            '--add-data', 'qt_core.py;.',
            '--add-data', 'gui;gui/',
            'main.py')
            
process = subprocess.Popen(command, 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

while True:
    output = process.stdout.readline()
    print(output.strip())
    # Do something else
    return_code = process.poll()
    if return_code is not None:
        print('RETURN CODE', return_code)
        # Process has finished, read rest of the output 
        for output in process.stdout.readlines():
            print(output.strip())
        break

# test app
print("starting App ....")

os.chdir('dist')
os.system(f"{app_name}.exe")