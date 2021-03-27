"""La CNN che usavo per leggere la dashboard https://www.governo.it/it/cscovid19/report-vaccini/"""

#
##
### SCREENSHOTTO
##
#

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image

def screenshot():

	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--start-maximized')
	driver = webdriver.Chrome(options=chrome_options)
	driver.get('https://www.governo.it/it/cscovid19/report-vaccini/')
	time.sleep(2)

	driver.set_window_size(1500, 2600)
	time.sleep(2)
	driver.save_screenshot("screenshot.png")
	driver.quit()

	im = Image.open('screenshot.png')
	im = im.crop( (300, 1400, 1900, 4000 ) )	#unità di misura diverse da set_window_size(), credo
	im.save("screenshot.png")

#
##
### CHIEDO A GINO DI LEGGERE
##
#

import matplotlib.pyplot as plt
import keras_ocr

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def gino_leggi():
	# keras-ocr will automatically download pretrained weights for the detector and recognizer.
	Gino = keras_ocr.pipeline.Pipeline()

	# Get a batch of example images
	images = [ keras_ocr.tools.read('screenshot.png') ]

	# Each prediction in predictions_lists is a list of (word, box) tuples.
	predictions_lists = Gino.recognize(images)
	words_list = [ pair[0] for pair in predictions_lists[0] ]
	scope = words_list.index('lombardia')

	return words_list[ scope-3 : scope+5 ]