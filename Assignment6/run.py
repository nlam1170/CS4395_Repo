from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from bs4 import BeautifulSoup 
import requests
import string
import os
import pickle


class URLGenerator:
    def __init__(self):
        self.starter_url = "https://www.google.com/search?q=christopher+nolan&sxsrf=ALiCzsZK4ngEVVIj0FsSwUsQS9CdYJr0jg%3A1665355511187&ei=905DY571Ctm3qtsPk625uAs&ved=0ahUKEwjezKzdnNT6AhXZm2oFHZNWDrcQ4dUDCA4&uact=5&oq=christopher+nolan&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECcyDQguEIAEEIcCELEDEBQyDQgAEIAEEIcCELEDEBQyCAguEIAEELEDMggILhCABBCxAzIICAAQgAQQsQMyBQgAEIAEMgUIABCABDIICAAQsQMQgwEyBQgAEIAEOgoIABBHENYEELADOgcIIxDqAhAnOgUILhCRAjoLCC4QgAQQsQMQgwE6BAguEEM6CwgAEIAEELEDEIMBOhEILhCABBCxAxCDARDHARDRAzoECC4QJzoICC4Q1AIQkQI6BwguENQCEEM6DgguEIAEELEDEMcBENEDOggILhCxAxCDAToFCAAQkQI6CwguELEDEIMBEJECOgoILhCxAxCDARBDOgoILhCABBCHAhAUOg4ILhCABBCxAxCDARDUAjoLCC4QgAQQxwEQ0QM6CAguELEDEJECOgsILhCABBCxAxDUAjoFCC4QgARKBAhBGABKBAhGGABQuA9Y7zFg6zNoAnABeACAAVCIAd0HkgECMTeYAQCgAQGwAQrIAQjAAQE&sclient=gws-wiz"
        self.urls = self.populate_urls()

    def populate_urls(self):
        req = requests.get(self.starter_url)
        data = req.text
        soup = BeautifulSoup(data, features="lxml")
        urls = []

        for link in soup.find_all("a"):
            link_str = str(link.get("href"))
            if "facebook" in link_str or "twitter" in link_str or "instagram" in link_str:
                continue
            if "Nolan" in link_str or "nolan" in link_str:
                if link_str.startswith('/url?q='):
                    link_str = link_str[7:]
                if '&' in link_str:
                    i = link_str.find('&')
                    link_str = link_str[:i]
                if link_str.startswith('http') and 'google' not in link_str:
                    urls.append(link_str)
        return urls
    
    def grab_text(self, url):
        try:
            html = requests.get(url)
            soup = BeautifulSoup(html.text, features="lxml")
            return soup.get_text()

        except:
            return ""
    
    def clean_text(self,text):
        text = text.replace("\n", "")
        text = text.replace("\t", "")
        return text

    def write_to_file(self):
        if not os.path.exists("url_output"):
            os.mkdir("url_output")

        i = 1
        for u in self.urls:
            content = self.grab_text(u)
            if content == "":
                continue
            else:
                content = self.clean_text(content)
                with open(f"url_output/url_{i}.txt", "w+") as fs:
                    fs.write(content)
                i += 1
    
    def write_sent_to_file(self):
        if not os.path.exists("sent_output"):
            os.mkdir("sent_output")
        
        url_text_files = os.listdir("url_output")
        
        i = 1
        for file_name in url_text_files:
            file_name = f"url_output/{file_name}"
            with open(file_name, "r") as f:
                with open(f"sent_output/sent_{i}.txt", "w+") as out:
                    sent_tokens = sent_tokenize(f.read())
                    for token in sent_tokens:
                        out.write(token + "/n")
            i += 1

    def build_word_list(self):
        sent_files = os.listdir("sent_output")
        stop = set(stopwords.words("english"))
        months = set(["january", "febuary", "march", "april", "may", "june", "july" "august", "september", "october", "november", "december"])
        all_words = []

        for file_name in sent_files:
            with open("sent_output/"+file_name, "r") as f:
                content = f.read()
                content = content.lower()
                content = content.translate(str.maketrans('', '', string.punctuation))
                tokens = word_tokenize(content)
                filtered_tokens = [w for w in tokens if w not in stop and w.isalnum() and w not in months and not w.isnumeric()]
                all_words.extend(filtered_tokens)

        return all_words

    def print_top_words(self):
        tokens = self.build_word_list()

        dist = FreqDist(t for t in tokens)
        print("Top 40 terms:\n")
        print(dist.most_common(40))

    def build_knowledge_base(self):
        base = {}
        base["job"] = ["director", "film", "original", "hollywood", "awards", "films", "academy"]
        base["movies"] = ["inception", "batman", "tenet", "knight"]
        base["other"] = ["screenplay", "foreign", "coen", "critics"]
        return base



if __name__ == "__main__":
    x = URLGenerator()
    x.write_to_file()
    x.write_sent_to_file()
    x.print_top_words()
    knowldge_base = x.build_knowledge_base()
    pickle.dump(knowldge_base, open("base.p", "wb"))