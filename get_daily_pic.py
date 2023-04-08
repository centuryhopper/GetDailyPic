import platform

if platform.system() == "Linux":
    import linux_tools as tools
elif platform.system() == "Windows":
    import windows_tools as tools

import requests
import os
import time
import darkdetect
import subprocess
# from secrets import Secrets
import sys

# make sure we're in this file's directory no matter from which directory we run this file
os.chdir(os.path.dirname(__file__))

sys.path.append(tools.AUTOMATE_EMAIL_PATH)
from EmailingTool import EmailTool

url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
currentTime = time.strftime("%Y-%m-%d-%H-%M-%S")
FILENAME = f'nasa_pic_{currentTime}.png'


def get_filename():
    directory = os.getcwd() + '/nasa_daily_pic_collection/'
    return os.path.join(directory, FILENAME)

def download_pic_of_day():
    r = requests.get(url)

    if r.status_code != 200:
        print('error')
        return

    picture_url = r.json()['url']
    if "jpg" not in picture_url:
        print("No image for today, must be a video")
        feedback = f'no image for the date: {time.strftime("%Y-%m-%d")}'
        EmailTool.sendEmail('','', ['leozhang12345678@gmail.com'], 'NASA_Daily_Pic', feedback)
        with open(f'{os.getcwd()}/no_image_notice.txt', 'w') as f:
            f.write(feedback)
    else:
        pic = requests.get(picture_url , allow_redirects=True)
        filename = get_filename()

        if filename.startswith('ERROR'):
            print('ERROR, you are not running on Linux')
            return

        open(filename, 'wb').write(pic.content)

        feedback = f"saved picture of the day to {filename}!"
        EmailTool.sendEmail('','', ['leozhang12345678@gmail.com'], 'NASA_Daily_Pic', feedback)

def main():
    lastDate = ''
    if not os.path.isfile(f'{os.getcwd()}/time_stamp.txt'):
        print('creating file')
        with open(f'{os.getcwd()}/time_stamp.txt', 'w') as f:
            f.write('')
    with open(f'{os.getcwd()}/time_stamp.txt', 'r') as f:
        lastDate = f.read()
        if lastDate == time.strftime("%Y-%m-%d") and tools.IS_CONNECTED_TO_NETWORK:
            print(f'{__file__}: already ran this')
            return
    with open(f'{os.getcwd()}/time_stamp.txt', 'w') as f:
        f.write(time.strftime("%Y-%m-%d"))
    download_pic_of_day()

    # set background
    if platform.system()=="Linux":
        # append -dark if the os theme is dark
        # darkText = '-dark' if darkdetect.isDark() else ''
        # cmd = f"gsettings set org.gnome.desktop.background picture-uri{darkText} file://" + filename
        # os.system(cmd)
        # get the latest picture from our nasa pic collections
        # subprocess.run(f'{Secrets.SHELL_SCRIPT_PATH}./latest.sh')
        pass

if __name__ == '__main__':
    main()
#    subprocess.run(f'{Secrets.SHELL_SCRIPT_PATH}./latest.sh')
    pass



