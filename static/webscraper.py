import requests
from bs4 import BeautifulSoup


def Find_Link():
    # Making a GET request
    r = requests.get('https://www.w3schools.com/references/index.php')

    # Parsing the HTML
    HtmlContent = BeautifulSoup(r.content, 'html.parser')

    Raw_Data = HtmlContent.find_all("a",class_ = "ga-nav")
    output=  []
    for input in Raw_Data:
        input = input["href"]
        if input != "javascript:void(0);":
            output.append("https://www.w3schools.com"+input)
    return output

