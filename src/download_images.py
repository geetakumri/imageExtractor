import requests
import os
from bs4 import BeautifulSoup
from crontab import CronTab
import re


def download_images(folder_name, images):
    img_count = len(images)
    if img_count > 0:
        download = 0
        for i, image in enumerate(images):
            try:
                image_link = image['src']
                try:
                    r = requests.get(image_link).content
                    try:
                        r = str(r, 'utf-8')

                    except UnicodeDecodeError:
                        with open(f"{folder_name}/images{i + 1}.jpg", "wb+") as f:
                            f.write(r)
                            download += 1
                except:
                    pass
            except:
                print('No image source')

        print("Total downloaded images = ", download)


def folder_create(search_image, images):
    folder_name = r"D:\git_projects\junk\\" + search_image
    try:
        os.mkdir(folder_name)
    except:
        print("Folder exists")
    finally:
        download_images(folder_name, images)


def main(search_image):
    url = f'https://www.google.com/search?q={search_image}&hl=en&tbm=isch'

    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }
    resp = requests.get(url, header)

    soup = BeautifulSoup(resp.content, 'html.parser')
    images = soup.find_all('img')
    folder_create(search_image, images)


def scheduler(timing, search_image):
    cron = CronTab(user='root')
    job = cron.new(command=main(search_image))
    """
    *       *       *       *       *
    (0-59)  (0-23)  (1-31)  (1-12)  (0-6)
    """
    job.setall(timing)
    cron.write()


def send_email(email_id, file_loc):
    pass


def verify_timing(timing):
    regex = re.compile('^(\d{4})-((0[1-9])|(1[0-2]))-((0[1-9])|(1[0-9])|(2[0-9])|(3[0-1])) ([0-1][0-9]|[2][0-3]):([0-5][0-9])$')
    return re.match(regex, timing)


def get_user_input():
    search_image = ''
    while len(search_image) == 0:
        search_image = input('Enter image to search: ')

    timing = ''
    while verify_timing(timing):
        timing = input('Enter timing to run the search in YYYY-MM-DD hh:mm format: ')

    email_id = ''
    while len(email_id) == 0:
        email_id = input('Enter your email_id: ')

    scheduler(timing, search_image)


if __name__ == '__main__':
    get_user_input()
