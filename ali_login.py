from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC


class Aliexpress:
	# For easier usage of Aliexpress links, storing them in dict
	# TODO: add functionality of parsing Aliexpress level and other useful stuff.
	urls = {
		'login_page': 'https://login.aliexpress.com/?returnUrl=https%3A%2F%2Ftrade.aliexpress.com%2ForderList.htm%3Fspm%3Da2g0o.home.1000001.14.650c2c25NJb2Cx%26tracelog%3Dws_topbar%26tsp%3D1584806227838',
	}

	# All needed page elements are stored here, type of element doesn't matter(css rule, xpath etc.)
	webpage_items = {
		'login_field': 'fm-login-id',
		'password_field': 'fm-login-password',
		'login_button_xpath': '/html/body/div[3]/div/div[1]/div/div/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div/form/div[5]/button',
		'my_aliexpress': '//*[@id="headMenu_default"]'
	}

	def __init__(self, driver, login, password):
		self.driver = driver
		self.login = login
		self.password = password

	# TODO: split functionality into more SOLID look
	def getting_orders(self):
		self.driver.get(Aliexpress.urls['login_page'])
		payload = {'login': self.login, 'password': self.password}
		input_into_login_field = self.driver.find_element_by_id("fm-login-id")
		input_into_login_field.clear()
		input_into_login_field.send_keys(payload['login'])

		into_password_field = self.driver.find_element_by_id("fm-login-password")
		into_password_field.send_keys(payload['password'])

		# Multiple exceptions were made to handle 'Service is not available' issue.
		try:
			submit_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
				(By.XPATH, Aliexpress.webpage_items['login_button_xpath'])
			))
			submit_button.click()

		except NoSuchElementException and TimeoutException:
			print('Login button is not clickable, exiting')
			self.driver.close()

		if EC.presence_of_element_located((By.XPATH, Aliexpress.webpage_items['login_button_xpath'])):
			try:
				already_logged_button = self.driver.find_element_by_xpath(Aliexpress.webpage_items['login_button_xpath'])
				already_logged_button.click()
			except NoSuchElementException:
				print('Script does not require clicking another button, continuing...')
				pass

		title_wait = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((
			By.XPATH, Aliexpress.webpage_items['my_aliexpress']
		)))

		if EC.presence_of_element_located((By.XPATH, Aliexpress.webpage_items['my_aliexpress'])):
			print('Logged in successfully, starting to parse necessary info')

			'''
				In this section, we are parsing 'My orders' page. TODO: find a way to loop over same page
			elements, but different orders (and converting into text using .text attribute)
			'''

			get_orders_head = self.driver.find_elements_by_class_name('order-head')
			# get_orders_body = self.driver.find_elements_by_class_name('order-body')

			for order in get_orders_head:
				order_id = order.find_element_by_class_name('first-row').find_element_by_class_name('info-body').text
				yield order_id
				order_time = order.find_element_by_class_name('second-row').find_element_by_class_name('info-body').text
				yield order_time
				order_price = order.find_element_by_class_name('amount-num').text
				yield order_price

				# TODO: add parsing of dispute status and write to db;

				# everything_about_order = order_id, order_time, order_price
				# yield everything_about_order
			# for description in get_orders_body:
			# 	order_description = description.find_element_by_class_name(
			# 		'product-sets'
			# 	).find_element_by_class_name(
			# 		'product-title').find_element_by_class_name('baobei-name').text
			# 	yield order_description

		else:
			self.driver.close()

	def shutdown(self):
		self.driver.close()

	# TODO: add functionality to start webdriver for multiple accounts (async?)
