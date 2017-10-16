import requests, re, os
from datetime import datetime


# The REs are created, one for the URLs and one for the picture-name
urlRegex = re.compile(r"<a href='https://rare-pepe\.com/rare-pepe-collection/(.*)/'>")
bildRegex = re.compile(r'<meta property="og:image" content="https://rare-pepe\.com/wp-content/uploads/(.*(.png|.jpg|.gif))" />')


quellcode = requests.get("https://rare-pepe.com/")

# The page source is looked through for the picture-name
oc = urlRegex.findall(quellcode.text)

print("Die Namen aller Bilder wurden geladen.")
print("Insgesamt sind es {} Bilder".format(len(oc)))
print("Wie viele dieser Bilder wollen Sie herunterladen? Wenn Sie alle wollen drücken Sie einfach Enter!")
bilderAnzahl = input()
if bilderAnzahl == "":
    bilderAnzahl = len(oc)
print("Danke, wir werden für Sie {} PEPE-Memes herunterladen".format(str(bilderAnzahl)))


#Current date is created
timenow = datetime.now()
#Now the directory for the PEPE-memes is created
directory = "\\Users\\Ansgar\\Pictures\PEPE-MEMES from {}, {}-{}-{}".format(timenow.date(), timenow.hour, timenow.minute, timenow.second)
os.mkdir(directory)
# Directory is changed
os.chdir(directory)
# Now the image-sites are opened to look for the image name to download it
zähler = 0


for link in oc:
    if zähler >= int(bilderAnzahl):
        continue
    # The variable bildURL is created
    bildURL = "https://rare-pepe.com/rare-pepe-collection/{}".format(link)

    # Now the site is opened to look for the image name
    bildSeite = requests.get(bildURL)
    if bildSeite.raise_for_status() != None:
        print("Die URL {} ist nicht verfügbar!".format(bildURL))
        exit()
    # The site is searched for the image-name
    bildNameReg = bildRegex.search(bildSeite.text)
    bildName = bildNameReg.group(1)

    # The URL of the raw image is created
    url = "https://rare-pepe.com/wp-content/uploads/{}".format(bildName)

    # We're coming to the final: The download of the image
    r = requests.get(url, stream=True)
    if r.status_code == 200:

        with open("{}".format(str(zähler)+ "--PEPEpic" + bildNameReg.group(2)), 'wb') as playFile:
            for chunk in r.iter_content(100000):
                playFile.write(chunk)


    zähler += 1

input("Drücken Sie eine Taste um zu beenden")
os.system(r'explorer "C:{}"'.format(directory))
