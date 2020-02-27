import pandas as pd
import re

data = pd.read_excel("google_language_family.xlsx", index_col=0)

# Split familty string.
data["Family"] = data["Family"].apply(lambda x: x.split(',')[0])


def extract_number_from_text(N):
    """
    Extract float number from string value with some regex.
    :param N: string with value.
    :return: float of value.
    """
    if not pd.isna(N):
        N = N.replace(u'\xa0', u' ')
        N = re.subn(r'\[\d\]', "", N)[0]
        N = re.findall(r'(?i)(((\d*\.\d*)|(\d*)) [m,b]illion|(\d{1,3},){1,3}\d{1,3})', N)[0][0]
        if "million" in N.lower():
            return float(N.split(" ")[0])*1e6
        elif "billion" in N:
            return float(N.split(" ")[0])*1e9
        else:
            return float(N.replace(",", ""))
    else:
        return 0


# Parse number of native speakers into numbers.
data["Native speakers"] = data["Native speakers"].apply(lambda x: extract_number_from_text(x))

# Find back languages.s
id_select = data.groupby(["Family"], sort=False)['Native speakers'].transform(max) == data["Native speakers"]

print(data[id_select].sort_values("Native speakers", ascending=False))
