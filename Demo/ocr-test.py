import tesserocr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36' }
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('w3c',False)

from PIL import Image

image = Image.open(r'/Users/james/Downloads/picture.jpeg')


image = image.convert('L')

threshold = 150

table = []
for i in range(256):
    if i< threshold:
        table.append(0)
    else:
        table.append(1)

image= image.point(table,'1')


image.show()



result = tesserocr.image_to_text(image)

print(result)

