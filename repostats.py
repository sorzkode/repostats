import requests
import json
import matplotlib.pyplot as plt

with open('vars.json') as f:
    secret_vars = json.load(f)

USERNAME = secret_vars['GH_USERNAME']
TOKEN = secret_vars['GH_API_KEY']

def get_repo_languages():
    try:
        url = f"https://api.github.com/users/{USERNAME}/repos"
        headers = {"Authorization": f"token {TOKEN}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        repos = response.json()

        languages = {}
        for repo in repos:
            repo_languages_url = repo["languages_url"]
            response = requests.get(repo_languages_url, headers=headers)
            response.raise_for_status()  # Raise an exception if the request was unsuccessful
            repo_languages = response.json()
            for language, bytes_count in repo_languages.items():
                languages[language] = languages.get(language, 0) + bytes_count

        return languages
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def save_languages_to_json(languages):
    try:
        with open("languages.json", "w") as file:
            json.dump(languages, file, indent=4)
    except IOError as e:
        print(f"An error occurred while saving the languages to JSON: {e}")

def create_language_chart():
    try:
        with open("languages.json", "r") as file:
            languages = json.load(file)

        labels = list(languages.keys())
        values = list(languages.values())

        plt.bar(labels, values)
        plt.xlabel("Languages")
        plt.ylabel("Bytes Count")
        plt.title("Language Distribution")

        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

        plt.tight_layout()  # Adjust layout to prevent overlap

        plt.savefig("langchart.png")
        plt.show()
    except IOError as e:
        print(f"An error occurred while creating the language chart: {e}")

if __name__ == "__main__":
    languages = get_repo_languages()
    if languages is not None:
        save_languages_to_json(languages)
        create_language_chart()
