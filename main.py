import wikipedia
import pandas as pd
from bs4 import BeautifulSoup

data = pd.read_excel("google_lang.xlsx")

langs = data["Languages"]
print(langs)

results = list()
for i, lang in enumerate(langs):
    print(i, lang)

    try:
        wiki_page = wikipedia.page("%s language" % lang.split(" (")[0])

        page_html = BeautifulSoup(wiki_page.html(), features='html.parser')

        for f in page_html.find_all("tr"):
            ths = f.find_all("th")
            if len(ths) > 0 and ths[0].text == "Language family":
                family_parts = [a.text for a in f.find_all("td")[0].find_all('a') if "[" not in a.text and "]" not in a.text]
                results.append({
                    "Language": lang,
                    "Family": ",".join(family_parts)
                })
                break
    except wikipedia.exceptions.PageError:
        print("Page Error")

pd.DataFrame(results).to_excel("google_language_family.xlsx")
