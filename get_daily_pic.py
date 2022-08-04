import requests
import platform
import pwd
import os
import time
import darkdetect
import subprocess
from secrets import Secrets


url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
currentTime = time.strftime("%Y-%m-%d-%H-%M-%S")
FILENAME = f'nasa_pic_{currentTime}.png'

# make sure we're in this file's directory no matter from which directory we run this file
os.chdir(os.path.dirname(__file__))
# print(os.getcwd())

def get_filename():
    username = pwd.getpwuid(os.getuid()).pw_name
    if platform.system()=="Linux":
        directory = os.getcwd() + '/nasa_daily_pic_collection/'
    elif platform.system()=="Darwin":
        directory = "/Users/" + username + "/Documents/Github/nasa_daily_pic_collection/archive/"
    return os.path.join(directory, FILENAME)

def download_pic_of_day():
    r = requests.get(url)

    if r.status_code != 200:
        print('error')
        return

    picture_url = r.json()['url']
    if "jpg" not in picture_url:
        print("No image for today, must be a video")
    else:
        pic = requests.get(picture_url , allow_redirects=True)
        filename = get_filename()

        open(filename, 'wb').write(pic.content)

        print(f"saved picture of the day to {filename}!")

def main():
    lastDate = ''
    if not os.path.isfile(f'{os.getcwd()}/time_stamp.txt'):
        print('creating file')
        with open(f'{os.getcwd()}/time_stamp.txt', 'w') as f:
            f.write('')
    with open(f'{os.getcwd()}/time_stamp.txt', 'r') as f:
        lastDate = f.read()
        if lastDate == time.strftime("%Y-%m-%d"):
            print(f'{__file__}: already ran this')
            return
    with open(f'{os.getcwd()}/time_stamp.txt', 'w') as f:
        f.write(time.strftime("%Y-%m-%d"))
    download_pic_of_day()

    filename = get_filename()
    print(filename)

    # set background
    if platform.system()=="Linux":
        # append -dark if the os theme is dark
        darkText = '-dark' if darkdetect.isDark() else ''
        cmd = f"gsettings set org.gnome.desktop.background picture-uri{darkText} file://" + filename
        os.system(cmd)
        # get the latest picture from our nasa pic collections
        # subprocess.run(f'{Secrets.SHELL_SCRIPT_PATH}./latest.sh')
    elif platform.system()=="Darwin":
        cmd = "osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"" + filename +"\"'"
        # use absolute path to the image, and not a path that begins with a user path (~/Downloads/image.jpg)!

        os.system(cmd)

if __name__ == '__main__':
    main()
#    subprocess.run(f'{Secrets.SHELL_SCRIPT_PATH}./latest.sh')



