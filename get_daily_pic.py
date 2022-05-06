import requests
import platform
import pwd
import os
import time
from secrets import Secrets

url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
currentTime = time.strftime("%Y-%m-%d-%H-%M-%S")
FILENAME = f'nasa_pic_{currentTime}.png'


def get_filename():
    username = pwd.getpwuid(os.getuid()).pw_name
    if platform.system()=="Linux":
        directory = "/home/" + username + "/Documents/nasa_daily_pic_archive/"
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
    if not os.path.isfile(f'{Secrets.TIMESTAMP_FILEPATH}time_stamp.txt'):
        print('creating file')
        with open(f'{Secrets.TIMESTAMP_FILEPATH}time_stamp.txt', 'w') as f:
            f.write('')
    with open(f'{Secrets.TIMESTAMP_FILEPATH}time_stamp.txt', 'r') as f:
        lastDate = f.read()
        if lastDate == time.strftime("%Y-%m-%d"):
            print('already ran this')
            return
    with open(f'{Secrets.TIMESTAMP_FILEPATH}time_stamp.txt', 'w') as f:
        f.write(time.strftime("%Y-%m-%d"))
    download_pic_of_day()

    filename = get_filename()

    # set background
    if platform.system()=="Linux":
        cmd = "gsettings set org.gnome.desktop.background picture-uri file:" + filename
    elif platform.system()=="Darwin":
        cmd = "osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"" + filename +"\"'"
        # use absolute path to the image, and not a path that begins with a user path (~/Downloads/image.jpg)!

    os.system(cmd)

if __name__ == '__main__':
    main()


