import urllib.request
import zipfile

from pathlib import Path
Path("data/raw").mkdir(parents=True, exist_ok=True)
Path("data/preprocessed").mkdir(parents=True, exist_ok=True)


# Select only entries that have some corrections, and are only from corpuses that offer good sentences

url = "https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1185/vejica13.zip"

def download_corpus():
    print("Downloading corpus Vejica 1.3...")
    filehandle, _ = urllib.request.urlretrieve(url)
    zip_file_object = zipfile.ZipFile(filehandle, 'r')
    first_file = zip_file_object.namelist()[0]
    file = zip_file_object.open(first_file)
    content = file.read()
    f = open("data/raw/vejica13.txt", "wb")
    f.write(content)
    f.close()
    print("Downloaded")


# todo replace ,÷ with ÷

download_corpus()

