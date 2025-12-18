import subprocess
from bs4 import BeautifulSoup
with open("Artistneeddown.txt",encoding="utf8") as f:
    html_code = f.read()
# Parse the HTML code with BeautifulSoup
soup = BeautifulSoup(html_code, 'html.parser')

# Find all the 'a' tags
a_tags = soup.find_all('a')

# Use a set to store unique href values
hrefs = set()

# Extract the href attribute from each 'a' tag
for a_tag in a_tags:
    href = a_tag.get('href')
    if href:  # Ensure the href attribute exists
        hrefs.add(href)

# Print the unique href values
num = 0
ff = open("Needdownload-artistbulk.txt","w")
for href in hrefs:
    link = "https://hub.vroid.com/" + href
    print(link)
    ff.write(link + "\n")
    num += 1
print("Total model number:" + str(num))
ff.close()
#input("Press any key to download all, terminate to not download. Writed to file")
#subprocess.call(['python', 'nodewraper.py'])
