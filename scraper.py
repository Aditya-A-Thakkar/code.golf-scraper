import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, user):
        self.user = user
        self.data = dict()
        self.user_data = requests.get(f"https://code.golf/golfers/{self.user}/holes/points/overall/chars").text
        self.soup = BeautifulSoup(self.user_data, 'html.parser')

    def __scrape(self):
        number_of_holes = int(self.soup.find("p", {"class": "red"}).text.split("/")[0])
        if number_of_holes == 0:
            return {}

        holes_div = self.soup.find("div", {"id": "holes"})

        for hole in holes_div.find_all("div", {"class": "hole"}):
            score_tag = hole.next_sibling.next_sibling
            score = int(score_tag.text)
            while score_tag.next_sibling.find("svg") == None:
                score_tag = score_tag.next_sibling
                score += int(score_tag.text)
            self.data[hole.text] = score
        
        return self.data
    
    def get_total_score(self):
        self.__scrape()
        return sum(self.data.values())

if __name__ == "__main__":
    print(Scraper("Aditya-A-Thakkar").get_total_score())
