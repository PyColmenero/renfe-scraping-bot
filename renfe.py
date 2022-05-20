from selenium import webdriver
import os
import io
import time
import json
import datetime

import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def acceptCookies():

	ccookies = WebDriverWait(driver,20).until(lambda d: driver.find_element_by_id('onetrust-banner-sdk'))
	driver.execute_script('document.getElementById("onetrust-banner-sdk").remove();')
	# accept_cookies = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")) )
	# accept_cookies.click()

def enterDirs(origin,destination):

	

	origin_input = WebDriverWait(driver, 20).until( EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/rf-header/rf-header-top/div[2]/rf-search/div/div[1]/rf-awesomplete[1]/div/div[1]/input")) ) #
	origin_input.send_keys(origin)
	listItem = WebDriverWait(driver, 20).until( EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/rf-header/rf-header-top/div[2]/rf-search/div/div[1]/rf-awesomplete[1]/div/div[1]/ul/li[1]")))
	listItem.click()

	time.sleep(2)
	origin_input = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/rf-header/rf-header-top/div[2]/rf-search/div/div[1]/rf-awesomplete[2]/div/div[1]/input")) ) #
	origin_input.send_keys(destination)
	listItem = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/rf-header/rf-header-top/div[2]/rf-search/div/div[1]/rf-awesomplete[2]/div/div[1]/ul/li[1]")))
	listItem.click()

def setSoloIda():

	WebDriverWait(driver,20).until( EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/rf-header/rf-header-top/div[2]/rf-search/div/div[2]/div[1]/div[1]/rf-select/div/button')) ).click()
	soloIda = WebDriverWait(driver,20).until( EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/rf-header/rf-header-top/div[2]/rf-search/div/div[2]/div[1]/div[1]/rf-select/div/div/ul/li[1]/button')) )
	soloIda.click()
	time.sleep(1)
	try:
		soloIda.click()
	except Exception as e:
		print( e )
	

def setDate():

	time.sleep(1)
	dateInput = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/rf-header/rf-header-top/div[2]/rf-search/div/div[2]/div[1]/div[2]/div/rf-date-search/div/rf-date-picker/div/div/input')
	dateInput.click()

	time.sleep(1)
	dateDay = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/rf-header/rf-header-top/div[2]/rf-search/div/div[2]/div[1]/div[2]/div/rf-date-search/div/rf-date-picker/section/div[1]/div[2]/section[1]/div[3]/div[9]')
	dateDay.click()

	time.sleep(1)
	dateAccept = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/rf-header/rf-header-top/div[2]/rf-search/div/div[2]/div[1]/div[2]/div/rf-date-search/div/rf-date-picker/section/div[2]/button[2]')
	dateAccept.click()

def searchTicket():

	driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/rf-header/rf-header-top/div[2]/rf-search/div/div[2]/div[2]/div[2]/form/rf-button/div/button/div[2]").click()


def getData():

	# print()
	# print(origin + " -> " + destination + ": " + str(dayTripDate) + "/" + str(monthTripDate) + "/2021")

	current_date = str(dayTripDate) + "_" + str(monthTripDate) + "_"+ str(yearTripDate)

	try:
		trayectos = WebDriverWait(driver,10).until(lambda d: driver.find_elements_by_class_name('trayectoRow'))

		time.sleep(1)
		for trayecto in trayectos:

			
			current_trip = {}
			datas = trayecto.find_elements_by_class_name("displace-text")

			for index, data in enumerate(datas):

				if index == 0: 
					current_trip["duration"] = data.text.strip().replace("\n","")
				elif index == 2: 
					current_trip["type"] = data.text.strip().replace("\n","")

			datas = trayecto.find_elements_by_class_name("booking-list-element-big-font") #displace-text
			

			for index, data in enumerate(datas):

				if index == 0: 
					current_trip["horaSalida"] = data.text.strip().replace("\n","")
				elif index == 2: 
					current_trip["horaLlegada"] = data.text.strip().replace("\n","")
				elif index > 2: 

					print(current_date + ": " + data.text.strip().replace("\n",""))
					current_trip["fecha"] = current_date
					price = data.text.strip().replace("\n","")[0:-2]
					if price in prices_json:
						prices_json[price].append(current_trip)
					else:
						prices_json[price] = [current_trip]
					break
			

		with io.open(filename,'w',encoding='utf8') as f:
			    f.write(json.dumps(prices_json));
		trayectos = None
	except Exception as e:
		print(e)


prices_json = {}

filename = ""

origin = "A Coruña"
destination = "Sevilla"

dayTripDate = 25
monthTripDate = 9
yearTripDate = 2021


if __name__ == "__main__":

	if True:

		driver = webdriver.Chrome(ChromeDriverManager().install())
		driver.get("https://www.renfe.com/es/es")

		today = datetime.datetime.today().strftime('%d_%m_%Y')

		filename = today + "_" + origin + "-" + destination + ".json"

		try:
			file = open(filename,"r+")
			prices_json = json.loads(file.read())
		except Exception as e:
			prices_json = {}
		


		acceptCookies()
		enterDirs(origin,destination)
		setSoloIda()
		searchTicket()
		acceptCookies()
		getData()


		for y in range(90):

			if dayTripDate==30:
				dayTripDate=1;
				if monthTripDate == 12: 
					monthTripDate = 1
					yearTripDate = 2022
				else: monthTripDate+=1;

			else: dayTripDate+=1;

			day =  "0"+str(dayTripDate) if (len(str(dayTripDate))==1) else str(dayTripDate)
			month =  "0"+str(monthTripDate) if (len(str(monthTripDate))==1) else str(monthTripDate)
			# month = (len(monthTripDate+"")==1) ? "0"+monthTripDate : monthTripDate
			date = str(day)+'/'+str(month)+'/'+str(yearTripDate)
			print(date)


			driver.execute_script('$("#fechaSeleccionada0").val("'+date+'");var e = jQuery.Event("keypress");e.which = 13;e.keyCode = 13;$("#fechaSeleccionada0").trigger(e);');
			print(WebDriverWait(driver,20).until( EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/section[2]/div/section/div[3]/div[2]'))).get_attribute("class"))

			while True:

				isActive = WebDriverWait(driver,20).until( EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/section[2]/div/section/div[3]/div[2]'))).get_attribute("class")
				if isActive == "tab-pane active":
					# print("wait...")
					time.sleep(0.1)

				else:
					break

			
			getData()
