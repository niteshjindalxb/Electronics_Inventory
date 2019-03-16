from bs4 import BeautifulSoup
import requests

def scrap_rollno():
    url = 'http://192.168.43.94:8000/input.txt'

    try:
        page = requests.get(url)
        data = BeautifulSoup(page.text, "html.parser")
        data = str(data)
        return data
    except requests.exceptions.ConnectionError:
        return "160101084"


if __name__ == "__main__":
    rollno = scrap_rollno()
    print(rollno)