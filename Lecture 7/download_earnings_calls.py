#%% Start
import requests
import os
from bs4 import BeautifulSoup
html_sitemap = requests.get("https://www.fool.com/sitemap/")
# Interpret html_sitemap as a XML file
soup = BeautifulSoup(html_sitemap.content, "html.parser")
pages = soup.find_all("loc")
links = [page.text for page in pages]

# %%
import time
transcripts_links = []

for link in links:
    html_sitemap = requests.get(link)
    # Check if the request was successful
    if html_sitemap.status_code != 200:
        print(f"Failed to fetch {link}")
        continue
    soup = BeautifulSoup(html_sitemap.content, "html.parser")
    # Find all the link nodes whose text contains "call-transcripts":
    pages = soup.find_all("loc", text=lambda text: "call-transcripts" in text)
    transcripts_links.extend([page.text for page in pages])
    print(f"Found {len(pages)} transcripts links in {link}")
    time.sleep(5)

# %%
# Save transcripts_links to a file:
with open("transcripts_links.txt", "w") as f:
    for link in transcripts_links:
        f.write(link + "\n")

# %%
import random
for t_link in transcripts_links:
    wait_time = random.uniform(5, 15)
    time.sleep(wait_time)
    site_content = requests.get(t_link, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(site_content.content, "html.parser")
    # Find node with class "article-body" and extract its text:
    transcript = soup.find("div", class_="article-body").text
    # File name is the last part of the URL
    # If the last character is a "/", remove it
    if t_link[-1] == "/":
        t_link = t_link[:-1]
    file_name = t_link.split("/")[-1] + ".txt"
    # Save transcript to a file inside folder "transcripts":
    os.makedirs("transcripts", exist_ok=True)
    with open(os.path.join("transcripts", file_name), "w") as f:
        f.write(transcript)
    print(f"Saved transcript to {file_name}")

# %%
