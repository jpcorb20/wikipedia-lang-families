import plotly.express as px
import pandas as pd
import json
import re
from pprint import pprint

data = pd.read_excel("google_language_family.xlsx", index_col=0)

data["Family"] = data["Family"].apply(lambda x: x.split(','))


def add_or_dig(f, parent_name, parent_level, lang=False, N=None):
    if lang and not pd.isna(N):
        N = N.replace(u'\xa0', u' ')
        N = re.subn(r'\[\d\]', "", N)[0]
        N = re.findall(r'(?i)(((\d*\.\d*)|(\d*)) [m,b]illion|(\d{1,3},){1,3}\d{1,3})', N)[0][0]
        parent_level.append(dict(name=f, parent=parent_name, n=N, children=list()))
    else:
        if len(parent_level) == 0 or f not in list(map(lambda x: x["name"], parent_level)):
            parent_level.append(dict(name=f, parent=parent_name, children=list()))

    return list(filter(lambda x: x["name"] == f, parent_level))[0]


def merge_in_tree(lang, family, N):
    global lang_family_tree

    family.append(lang)

    parent_level = lang_family_tree
    for i, f in enumerate(family):
        parent_level = add_or_dig(f, parent_level['name'], parent_level["children"], lang=(f == lang), N=N)


if __name__ == "__main__":

    lang_family_tree = dict(name="Language families", parent="null", children=list())

    for i, d in data.iterrows():
        print(d["Language"])
        merge_in_tree(d["Language"], d["Family"], d["Native speakers"])

    pprint(lang_family_tree)

    with open("language_family_tree.json", "w") as fp:
        json.dump(lang_family_tree, fp)
