import requests
import random
import time
import click

def clear():
    click.clear()

def get_repos():
    return requests.get(f"https://api.github.com/gists/public?page={random.randrange(0, 100)}").json()


code_len = 35


def get_rand_repo(repos):
    if not repos:
        return None

    repo = repos[random.randrange(len(repos))]

    while "files" not in repo.keys():
        repos.remove(repo)

        if not repos:
            return None

        repo = repos[random.randrange(len(repos))]

    return repo


def get_rand_file(repo):
    if not repo:
        return None, None, None

    files = repo["files"]

    if not files:
        return None, None, None

    file_keys = list(files.keys())

    key = random.choice(file_keys)
    file = files[key]

    content = requests.get(file["raw_url"]).text.strip()

    while file["language"] == None or file["language"] == "Text" or len(content) < 100 or "\n" not in content:
        files.pop(key)
        file_keys.remove(key)

        if not files:
            return None, None, None

        key = random.choice(file_keys)
        file = files[key]
        content = requests.get(file["raw_url"]).text

    return key, file, content


while True:
    repos = get_repos()

    try:
        for i in range(0, 5):
            repo = get_rand_repo(repos)

            while not repo:
                repo = get_rand_repo(repos)

            key, file, content = get_rand_file(repo)

            while not file:
                repos.remove(repo)
                repo = get_rand_repo(repos)
                key, file, content = get_rand_file(repo)

            if not repos:
                break

            codes = content.split("\n")

            rand_section = random.randrange(len(codes) - code_len) if len(codes) > code_len else 0

            while True:
                print("_" * 150)
                chunks = codes[rand_section:rand_section + code_len]

                print("\n".join(chunks))
                print("_" * 150)

                answer = input("what language is this? ").lower().strip()

                if answer == file["language"].lower():
                    break

                if answer == "idk":
                    print("the answer is " + file["language"])
                    break
                elif answer == "quit":
                    clear()
                    exit(0)

                print("WRONG try again")

                time.sleep(1)
                clear()

            if answer != "idk":
                print("you are right congrats")

            time.sleep(2)

            clear()

            if not repos:
                print("there is no files left.....")
                break
    except Exception as e:
        print(e)