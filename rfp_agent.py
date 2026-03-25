import requests
from bs4 import BeautifulSoup
from datetime import date

KEYWORDS = [
    "housing", "housing study", "planning",
    "redevelopment", "market analysis"
]

def fetch_rfps():
    url = "https://www.bidnetdirect.com/public/supplier/solicitations"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []

    for item in soup.text.split("\n"):
        line = item.strip()
        if any(k.lower() in line.lower() for k in KEYWORDS):
            if len(line) > 20:
                results.append(line)

    return list(set(results))[:20]


def run():
    rfps = fetch_rfps()

    today = date.today()
    output = f"\n--- {today} ---\n"

    if not rfps:
        output += "No relevant RFPs found.\n"
    else:
        for r in rfps:
            output += f"- {r}\n"

    with open("rfp_report.txt", "a") as f:
        f.write(output)


if __name__ == "__main__":
    run()
