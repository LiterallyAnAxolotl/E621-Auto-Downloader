import pkg_resources
import subprocess
import sys


def install_required_libraries():
    print("Initializing...")
    required_libraries = [
        "requests",
        "datetime",
        "colorama",
        "art",
    ]

    installed_packages = {pkg.key for pkg in pkg_resources.working_set}

    for library in required_libraries:
        if library not in installed_packages:
            print(f"Installing {library}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])
        else:
            print(f"{library} is already installed.")

#install_required_libraries()

import requests
import os
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from colorama import Fore, Style
import threading
import webbrowser
import ctypes
from art import tprint

if os.name == "nt":
    os.system(f"mode con: cols=150 lines=40")

ver = '2.0'


def clear():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")


def title(title):
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        subprocess.call(['printf', '\033]0;{}\a'.format(title)], shell=True)


def tinput(message):
    r = input(
        f"[{datetime.now().strftime('%H:%M:%S')}] {Fore.LIGHTCYAN_EX}[INPUT]{Style.RESET_ALL} [{threading.current_thread().name.strip(' (<lambda>), ''').replace('-', ' ').replace('MainThread', 'Main Thread').replace('MainThre', 'Main Thread').replace('(start', '').replace('(start)', '')}] {message}{Style.RESET_ALL}{Fore.LIGHTBLACK_EX} >>> {Style.RESET_ALL}")
    return r


def error(message):
    print(
        f"[{datetime.now().strftime('%H:%M:%S')}] {Fore.RED}[ERROR]{Style.RESET_ALL} [{threading.current_thread().name.strip(' (<lambda>), ''').replace('-', ' ').replace('MainThread', 'Main Thread').replace('MainThre', 'Main Thread').replace('(start', '').replace('(start)', '').replace('ThreadPoolExecutor 0_', 'Thread ')}] {message}{Style.RESET_ALL}")


def info(message):
    print(
        f"[{datetime.now().strftime('%H:%M:%S')}] {Fore.BLUE}[INFO]{Style.RESET_ALL} [{threading.current_thread().name.replace(' (<lambda>)', '').replace('-', ' ').replace('MainThread', 'Main Thread').replace('MainThre', 'Main Thread').replace('(start', '').replace('(start)', '').replace('ThreadPoolExecutor 0_', 'Thread ')}] {message}{Style.RESET_ALL}")


class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1
        return self.value

    def getValue(self):
        return self.value


class TagManager:
    def __init__(self):
        self.tag_directory = "data/tags"
        if not os.path.exists(self.tag_directory):
            os.makedirs(self.tag_directory)

    def save_tag(self, tag_name, tags):
        with open(f"{self.tag_directory}/{tag_name}.tag", "w") as f:
            f.write(tags)

    def load_tag(self, tag_name):
        try:
            with open(f"{self.tag_directory}/{tag_name}.tag", "r") as f:
                return f.read()
        except FileNotFoundError:
            info(f"Tag '{tag_name}' not found.")
            return None
    def get_tag_count(self):
        tags_dir = self.tag_directory
        if not os.path.exists(tags_dir):
            return 0
        else:
            tag_files = [file for file in os.listdir(tags_dir) if file.endswith(".tag")]
            return len(tag_files)
    def list_tags(self):
        tag_files = [f for f in os.listdir(self.tag_directory) if f.endswith(".tag")]
        tag_names = [os.path.splitext(tag_file)[0] for tag_file in tag_files]
        return tag_names

    def display_tags(self):
        info("All available tags:")
        for tag_name in self.list_tags():
            tags = self.load_tag(tag_name)
            info(f"{tag_name}: {tags}")


nono = False
noscore = False
count = Counter()
title(f"YiffScraper v{ver} | Not Yet Started... | Made by Literally An Axolotl#0001")
time.sleep(1)
clear()
tprint(f"YiffScraper v{ver}")
time.sleep(1)
AMOUNT = tinput("How many files should we download?")
AMOUNT = int(AMOUNT)
tag_manager = TagManager()

if tag_manager.get_tag_count() > 0:
    use_saved_tags = tinput("Do you want to use saved tags? (y/n)")

    if use_saved_tags.lower() == 'y':
        tag_manager.display_tags()
        selected_tag = tinput("Enter the name of the tag you want to use:")
        tag = tag_manager.load_tag(selected_tag)

        if tag is None:
            error("Selected tag not found.")
        else:
            info(f"Using saved tags: {tag}")
            tags = tag
    else:
        y = tinput("Would you like to run the tag builder? (y/n)")
        if y == 'y':
            clear()
            tprint(f"YiffScraper v{ver}")
            info("Make sure to use underscores (_) for multiple word tags!")
            yes = tinput("What things would you like to see? E.G: Male, Gay (Required)").lower().replace(', ',
                                                                                                         '+').replace(
                ' ',
                '+').replace(
                ',', "+")
            if yes == '':
                raise Exception("Tags are required!")
            print()
            no = tinput(
                "What things would you not like to see? E.G: Female, Intersex, webm (Leave blank for none)").lower().replace(
                ', ', '+-').replace(' ', '+-').replace(',', "+-")
            no = '-' + no
            if no == '':
                nono = True
            clear()
            tprint(f"YiffScraper v{ver}")
            info("E621 posts have 3 levels: safe, questionable, and explicit.")
            info("You can also use s, q, and e.")
            rating = tinput("What rating should the posts be? E.G: explicit (Required)").lower()
            if rating == '':
                raise Exception("Rating is required!")
            elif rating not in ['e', 's', 'q', 'safe', 'explicit', 'questionable']:
                raise Exception("Invalid rating!")
            clear()
            tprint(f"YiffScraper v{ver}")
            score = tinput("What should the minimum score be? E.G: 400 (Leave blank for none)")
            if score == '':
                noscore = True
            clear()
            tprint(f"YiffScraper v{ver}")
            info("Compiling tags...")
            tags = f"{yes}"
            if not nono:
                tags += f"+{no}"
            tags += f"+rating:{rating}"
            info(f"Tags: {tags}")
            yesno = tinput("Should we save these for later use? (y/n)")
            if yesno == 'y':
                name = tinput("What should we call this tag?")
                tag_manager.save_tag(name, tags)
        else:
            clear()
            tprint(f"YiffScraper v{ver}")
            info("E621 Tags Documentation: https://e621.net/wiki_pages/9169")
            x = tinput("Should we open the docs? (y/n)")
            if x == 'y':
                webbrowser.open("https://e621.net/wiki_pages/9169")
                time.sleep(3)
            tags = tinput("What tags should we use? (Seperated by a space or a +)").replace(', ', '+').replace(' ',
                                                                                                               '+').replace(
                ',', "+")
            yesno = tinput("Should we save these for later use? (y/n)")
            if yesno == 'y':
                name = tinput("What should we call these tags?")
                tag_manager.save_tag(name, tags)
else:
    y = tinput("Would you like to run the tag builder? (y/n)")
    if y == 'y':
        clear()
        tprint(f"YiffScraper v{ver}")
        info("Make sure to use underscores (_) for multiple word tags!")
        yes = tinput("What things would you like to see? E.G: Male, Gay (Required)").lower().replace(', ', '+').replace(' ',
                                                                                                                        '+').replace(
            ',', "+")
        if yes == '':
            raise Exception("Tags are required!")
        print()
        no = tinput(
            "What things would you not like to see? E.G: Female, Intersex, webm (Leave blank for none)").lower().replace(
            ', ', '+-').replace(' ', '+-').replace(',', "+-")
        no = '-' + no
        if no == '':
            nono = True
        clear()
        tprint(f"YiffScraper v{ver}")
        info("E621 posts have 3 levels: safe, questionable, and explicit.")
        info("You can also use s, q, and e.")
        rating = tinput("What rating should the posts be? E.G: explicit (Required)").lower()
        if rating == '':
            raise Exception("Rating is required!")
        elif rating not in ['e', 's', 'q', 'safe', 'explicit', 'questionable']:
            raise Exception("Invalid rating!")
        clear()
        tprint(f"YiffScraper v{ver}")
        score = tinput("What should the minimum score be? E.G: 400 (Leave blank for none)")
        if score == '':
            noscore = True
        clear()
        tprint(f"YiffScraper v{ver}")
        info("Compiling tags...")
        tags = f"{yes}"
        if not nono:
            tags += f"+{no}"
        tags += f"+rating:{rating}"
        info(f"Tags: {tags}")
        yesno = tinput("Should we save these for later use? (y/n)")
        if yesno == 'y':
            name = tinput("What should we call this tag?")
            tag_manager.save_tag(name, tags)
    else:
        clear()
        tprint(f"YiffScraper v{ver}")
        info("E621 Tags Documentation: https://e621.net/wiki_pages/9169")
        x = tinput("Should we open the docs? (y/n)")
        if x == 'y':
            webbrowser.open("https://e621.net/wiki_pages/9169")
            time.sleep(3)
        tags = tinput("What tags should we use? (Seperated by a space or a +)").replace(', ', '+').replace(' ','+').replace(',', "+")
        yesno = tinput("Should we save these for later use? (y/n)")
        if yesno == 'y':
            name = tinput("What should we call these tags?")
            tag_manager.save_tag(name, tags)
total = 0
url = f"https://e621.net/posts.json?tags={tags}"
info(f"Created URL: {url}")
time.sleep(1)
clear()
tprint(f"YiffScraper v{ver}")
stashname = tinput("What should we name the stash? (leave blank for 'stash')")
if stashname == '':
    stashname = 'stash'
timestamp = tinput("Should we add a timestamp to the name of the folder? (y/n)")
if timestamp == 'y':
    stashname = stashname + ' ' + datetime.now().strftime('%m-%d-%Y')
clear()
tprint(f"YiffScraper v{ver}")
THREADS = tinput("How many threads should we use? (Leave blank for 400)")
if THREADS == '':
    THREADS = 400
else:
    THREADS = int(THREADS)
clear()
tprint(f"YiffScraper v{ver}")
title(f"YiffScraper v{ver} | Files downloaded: 0 | Made by Literally An Axolotl#0001")


def download_file(file_url, path, extention, name):
    if file_url is None:
        return

    try:
        response = requests.get(file_url, stream=True)

        if response.status_code == 200:
            with open(path, "wb") as f:
                for chunk in response.iter_content(chunk_size=4096):
                    f.write(chunk)

            current_count = count.increment()
            title(f"YiffScraper v{ver} | Files downloaded: {current_count} | Made by Literally An Axolotl#0001")
            info(f"File {current_count} downloaded successfully. | Type: {extention} | Name: {name}{extention}")
        else:
            error(f"No file to download. Server replied with HTTP code: {response.status_code}")

    except Exception as e:
        error(e)


def get_json_object(url):
    try:
        headers = {"User-Agent": "The Yiffinator (by Literally An Axolotl#0001)"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            error(f"Response code: {response.status_code}")
            error(f"Response content: {response.content}")
            return None

    except requests.exceptions.RequestException as e:
        error(e)


def zip_folder(src_folder, dest_zip_file):
    with zipfile.ZipFile(dest_zip_file, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(src_folder):
            for file in files:
                zf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), src_folder))


if __name__ == "__main__":
    thread_pool = ThreadPoolExecutor(max_workers=THREADS)

    items_per_page = 50
    pages_needed = AMOUNT // items_per_page + (1 if AMOUNT % items_per_page > 0 else 0)

    for page in range(1, pages_needed + 1):
        remaining = AMOUNT - total
        limit = min(items_per_page, remaining)

        json_obj = get_json_object(f"{url}&page={page}&limit={limit}")
        if str(json_obj) == "{posts:[]}":
            error("No files found")

        if json_obj is None:
            info("No posts found for the current request.")
            break

        posts = json_obj["posts"]

        output_directory = "output"
        if not os.path.exists(output_directory):
            os.mkdir(output_directory)
        stash = os.path.join(output_directory, stashname)
        if not os.path.exists(stash):
            os.mkdir(stash)

        for post in posts:
            file = post["file"]

            try:
                file_url = file["url"]
            except KeyError:
                file_url = None
                info(f"No file URL found for post ID: {post['id']}")

            if file_url is None:
                file_extension = '.png'
            else:
                file_extension = os.path.splitext(file_url)[-1]

            file_name = post['id']
            thread_pool.submit(download_file, file_url, f"{stash}/{file_name}.{file_extension}", file_extension, file_name)

            total += 1
            if total >= AMOUNT:
                break

        time.sleep(3)

        if total >= AMOUNT:
            break

    thread_pool.shutdown(wait=True)
    clear()
    tprint(f"YiffScraper v{ver}")
    info("Downloading complete.")
    b = tinput("Should we zip the folder? (y/n)")
    if b == 'y':
        zip_folder(stashname, f"{stashname}.zip")
        info("Zipped successfully, exiting...")
    else:
        info("Exiting...")
    time.sleep(3)
    if os.name == 'nt':
        os.system("exit")
    else:
        exit(1)
