# System basic lib
import time
# The 3rd party
from selenium import webdriver
import chromedriver_binary
import pytest
from io import BytesIO
from PIL import Image, ImageDraw
# My import
import settings


# Execution
class TestMySite():

	@pytest.fixture()
	def set_up(self):
		self.driver = webdriver.Chrome()
		self.driver.implicitly_wait(10)
		self.driver.maximize_window()
		self.driver.delete_all_cookies()
		yield
		self.driver.close()
		self.driver.quit()		

	def screenshot(self):
		return self.driver.get_screenshot_as_png()

	def get_file_name_by_time(self, path):
		self.timestr = time.strftime("%Y%m%d%H%M%S")
		return path + 'screenshot_' + self.timestr + '.png'

	def draw_rectangle(self, element):
		location = element.location
		size = element.size
		png = self.screenshot()
		img = Image.open(BytesIO(png))
		left = location['x']
		top = location['y']
		right = location['x'] + size['width']
		bottom = location['y'] + size['height']
		red_frame = ImageDraw.Draw(img)
		red_frame = red_frame.rectangle((left - settings.OFFSET_ELEMENT, 
											top - settings.OFFSET_ELEMENT, 
											right + settings.OFFSET_ELEMENT, 
											bottom + settings.OFFSET_ELEMENT), 
											outline ="red", width=4)
		# img.save(file_name)
		return img


	# Testing
	# Index Screen
	def test_TC_INDEX_001(self, set_up):
		expected = 'Welcome to VMO'
		self.driver.get(settings.MAIN_URL)
		assert self.driver.title == expected

	def test_TC_INDEX_002(self, set_up):
		expected = 'Login'
		self.driver.get(settings.MAIN_URL)
		self.driver.find_element_by_id('start').click()
		assert self.driver.title == expected


	# Login Screen
	def test_TC_LOGIN_001(self, set_up):
		expected = 'Project Index'
		self.driver.get(settings.MAIN_URL)
		self.driver.find_element_by_id('start').click()
		self.driver.find_element_by_name('email').clear()
		self.driver.find_element_by_name('email').send_keys('phulikely@gmail.com')
		self.driver.find_element_by_name('password').clear()
		self.driver.find_element_by_name('password').send_keys('123')
		self.driver.find_element_by_id('login').click()
		assert self.driver.title == expected

	def test_TC_LOGIN_002(self, set_up):
		expected = 'Invalid email or password!'
		path = self.get_file_name_by_time(settings.LOGIN_PATH)
		self.driver.get(settings.MAIN_URL)
		start_btn = self.driver.find_element_by_id('start')
		time.sleep(1)
		self.draw_rectangle(start_btn).save(path)
		time.sleep(2)
		start_btn.click()
		self.driver.find_element_by_name('email').clear()
		email = self.driver.find_element_by_name('email')
		email.send_keys('phulikely@gmail.com')
		path = self.get_file_name_by_time(settings.LOGIN_PATH)
		self.draw_rectangle(email).save(path)
		time.sleep(1)
		self.driver.find_element_by_name('password').clear()
		password = self.driver.find_element_by_name('password')
		password.send_keys('12345')
		path = self.get_file_name_by_time(settings.LOGIN_PATH)
		self.draw_rectangle(password).save(path)
		time.sleep(1)
		login_btn = self.driver.find_element_by_id('login')
		path = self.get_file_name_by_time(settings.LOGIN_PATH)
		self.draw_rectangle(login_btn).save(path)
		time.sleep(1)
		login_btn.click()
		err_msg = self.driver.find_element_by_xpath('//label')
		path = self.get_file_name_by_time(settings.LOGIN_PATH)
		self.draw_rectangle(err_msg).save(path)
		time.sleep(1)
		assert err_msg.text == expected 

	def test_TC_LOGIN_003(self, set_up):
		expected = 'Invalid email or password!'
		self.driver.get(settings.MAIN_URL)
		self.driver.find_element_by_id('start').click()
		self.driver.find_element_by_name('email').clear()
		self.driver.find_element_by_name('email').send_keys('phulikely123@gmail.com')
		self.driver.find_element_by_name('password').clear()
		self.driver.find_element_by_name('password').send_keys('123')
		self.driver.find_element_by_id('login').click()
		err_msg = self.driver.find_element_by_xpath('//label')
		assert err_msg.text == expected

	def test_TC_LOGIN_004(self, set_up):
		expected = 'Invalid email or password!'
		self.driver.get(settings.MAIN_URL)
		self.driver.find_element_by_id('start').click()
		self.driver.find_element_by_name('email').clear()
		self.driver.find_element_by_name('email').send_keys('phulikely123@gmail.com')
		self.driver.find_element_by_name('password').clear()
		self.driver.find_element_by_name('password').send_keys('12345')
		self.driver.find_element_by_id('login').click()
		err_msg = self.driver.find_element_by_xpath('//label')
		assert err_msg.text == expected

	def test_TC_LOGIN_005(self, set_up):
		expected = 'Registration'
		self.driver.get(settings.MAIN_URL)
		self.driver.find_element_by_id('start').click()
		self.driver.find_element_by_xpath('//div[3]/a').click()
		assert self.driver.title == expected


	# Registration Screen
	def test_TC_REGISTER_001(self, set_up):
		expected = 'Login'
		self.driver.get(settings.MAIN_URL)
		self.driver.find_element_by_id('start').click()
		time.sleep(1)
		self.driver.find_element_by_xpath('//div[3]/a').click()
		time.sleep(1)
		self.driver.find_element_by_name('fname').send_keys('Quoc Viet')
		self.driver.find_element_by_name('lname').send_keys('Hoang')
		self.driver.find_element_by_name('email').send_keys('email1@gmail.com')
		self.driver.find_element_by_name('pwd').send_keys('12345')
		self.driver.find_element_by_name('repwd').send_keys('12345')
		self.driver.find_element_by_xpath('//input[7]').click()
		assert self.driver.title == expected

	def test_TC_REGISTER_002(self, set_up):
		expected = 'Passwords do not match!'
		self.driver.get(settings.MAIN_URL)
		self.driver.find_element_by_id('start').click()
		time.sleep(1)
		self.driver.find_element_by_xpath('//div[3]/a').click()
		time.sleep(1)
		self.driver.find_element_by_name('fname').send_keys('Quoc Viet')
		self.driver.find_element_by_name('lname').send_keys('Hoang')
		self.driver.find_element_by_name('email').send_keys('email2@gmail.com')
		self.driver.find_element_by_name('pwd').send_keys('12345')
		self.driver.find_element_by_name('repwd').send_keys('123456789')
		self.driver.find_element_by_xpath('//input[7]').click()
		assert self.driver.find_element_by_xpath('//label').text == expected

	def test_TC_REGISTER_003(self, set_up):
		expected = 'Email already existed!'
		path = self.get_file_name_by_time(settings.LOGIN_PATH)
		self.driver.get(settings.MAIN_URL)
		time.sleep(2)
		start_btn = self.driver.find_element_by_id('start')
		self.draw_rectangle(start_btn).save(path)
		time.sleep(2)
		start_btn.click()
		register_btn = self.driver.find_element_by_xpath('//div[3]/a')
		path = self.get_file_name_by_time(settings.LOGIN_PATH)
		self.draw_rectangle(register_btn).save(path)
		time.sleep(1)
		register_btn.click()
		time.sleep(1)
		fname = self.driver.find_element_by_name('fname')
		fname.send_keys('Quoc Viet')
		path = self.get_file_name_by_time(settings.LOGIN_PATH)
		self.draw_rectangle(fname).save(path)
		time.sleep(1)
		lname = self.driver.find_element_by_name('lname')
		lname.send_keys('Hoang')
		path = self.get_file_name_by_time(settings.LOGIN_PATH)
		self.draw_rectangle(lname).save(path)
		time.sleep(1)
		email = self.driver.find_element_by_name('email')
		email.send_keys('email1@gmail.com')
		path = self.get_file_name_by_time(settings.LOGIN_PATH)
		self.draw_rectangle(email).save(path)
		time.sleep(1)	
		pwd = self.driver.find_element_by_name('pwd')
		pwd.send_keys('12345')
		path = self.get_file_name_by_time(settings.LOGIN_PATH)
		self.draw_rectangle(pwd).save(path)
		time.sleep(1)
		repwd = self.driver.find_element_by_name('repwd')
		repwd.send_keys('12345')
		path = self.get_file_name_by_time(settings.LOGIN_PATH)
		self.draw_rectangle(repwd).save(path)
		time.sleep(1)		
		reg_btn = self.driver.find_element_by_xpath('//input[7]')
		path = self.get_file_name_by_time(settings.LOGIN_PATH)
		self.draw_rectangle(reg_btn).save(path)
		time.sleep(1)
		reg_btn.click()
		time.sleep(1)
		err = self.driver.find_element_by_xpath('//label')
		path = self.get_file_name_by_time(settings.LOGIN_PATH)
		self.draw_rectangle(err).save(path)
		time.sleep(1)		
		assert err.text == expected

	def test_TC_REGISTER_004(self, set_up):
		expected = 'Login'
		self.driver.get(settings.MAIN_URL)
		self.driver.find_element_by_id('start').click()
		time.sleep(1)
		self.driver.find_element_by_xpath('//div[3]/a').click()
		time.sleep(1)
		self.driver.find_element_by_name('fname').send_keys('😂')
		self.driver.find_element_by_name('lname').send_keys('😂')
		self.driver.find_element_by_name('email').send_keys('email1@gmail.com')
		self.driver.find_element_by_name('pwd').send_keys('123')
		self.driver.find_element_by_name('repwd').send_keys('123')
		self.driver.find_element_by_xpath('//input[7]').click()
		assert self.driver.title == expected

	def test_TC_REGISTER_005(self, set_up):
		expected = 'Login'
		self.driver.get(settings.MAIN_URL)
		self.driver.find_element_by_id('start').click()
		time.sleep(1)
		self.driver.find_element_by_xpath('//div[3]/a').click()
		time.sleep(1)
		self.driver.find_element_by_name('fname').send_keys('Quoc Viet')
		self.driver.find_element_by_name('lname').send_keys('Hoang')
		self.driver.find_element_by_name('email').send_keys('email1@gmail.com')
		self.driver.find_element_by_name('pwd').send_keys('😂')
		self.driver.find_element_by_name('repwd').send_keys('😂')
		self.driver.find_element_by_xpath('//input[7]').click()
		assert self.driver.title == expected

	def test_TC_REGISTER_006(self, set_up):
		expected = 'Login'
		self.driver.get(settings.MAIN_URL)
		self.driver.find_element_by_id('start').click()
		time.sleep(1)
		self.driver.find_element_by_xpath('//div[3]/a').click()
		time.sleep(1)
		self.driver.find_element_by_name('fname').send_keys('Quoc Viet')
		self.driver.find_element_by_name('lname').send_keys('Hoang')
		self.driver.find_element_by_name('email').send_keys('email😂1@gmail.com')
		self.driver.find_element_by_name('pwd').send_keys('123')
		self.driver.find_element_by_name('repwd').send_keys('123')
		self.driver.find_element_by_xpath('//input[7]').click()
		assert self.driver.title == expected

	def test_TC_REGISTER_007(self, set_up):
		expected = 'Registration'
		self.driver.get(settings.MAIN_URL)
		self.driver.find_element_by_id('start').click()
		time.sleep(1)
		self.driver.find_element_by_xpath('//div[3]/a').click()
		time.sleep(1)
		self.driver.find_element_by_name('fname').clear()
		self.driver.find_element_by_name('lname').send_keys('Hoang')
		self.driver.find_element_by_name('email').send_keys('email1@gmail.com')
		self.driver.find_element_by_name('pwd').send_keys('123')
		self.driver.find_element_by_name('repwd').send_keys('123')
		self.driver.find_element_by_xpath('//input[7]').click()
		assert self.driver.title == expected

	def test_TC_REGISTER_008(self, set_up):
		expected = 'Registration'
		self.driver.get(settings.MAIN_URL)
		self.driver.find_element_by_id('start').click()
		time.sleep(1)
		self.driver.find_element_by_xpath('//div[3]/a').click()
		time.sleep(1)
		self.driver.find_element_by_name('fname').send_keys('Quoc Viet')
		self.driver.find_element_by_name('lname').clear()
		self.driver.find_element_by_name('email').send_keys('email1@gmail.com')
		self.driver.find_element_by_name('pwd').send_keys('123')
		self.driver.find_element_by_name('repwd').send_keys('123')
		self.driver.find_element_by_xpath('//input[7]').click()
		assert self.driver.title == expected

	def test_TC_REGISTER_009(self, set_up):
		expected = 'Registration'
		self.driver.get(settings.MAIN_URL)
		self.driver.find_element_by_id('start').click()
		time.sleep(1)
		self.driver.find_element_by_xpath('//div[3]/a').click()
		time.sleep(1)
		self.driver.find_element_by_name('fname').send_keys('Quoc Viet')
		self.driver.find_element_by_name('lname').send_keys('Hoang')
		self.driver.find_element_by_name('email').clear()
		self.driver.find_element_by_name('pwd').send_keys('123')
		self.driver.find_element_by_name('repwd').send_keys('123')
		self.driver.find_element_by_xpath('//input[7]').click()
		assert self.driver.title == expected

	def test_TC_REGISTER_010(self, set_up):
		expected = 'Registration'
		self.driver.get(settings.MAIN_URL)
		self.driver.find_element_by_id('start').click()
		time.sleep(1)
		self.driver.find_element_by_xpath('//div[3]/a').click()
		time.sleep(1)
		self.driver.find_element_by_name('fname').send_keys('Quoc Viet')
		self.driver.find_element_by_name('lname').send_keys('Hoang')
		self.driver.find_element_by_name('email').send_keys('email1@gmail.com')
		self.driver.find_element_by_name('pwd').clear()
		self.driver.find_element_by_name('repwd').send_keys('123')
		self.driver.find_element_by_xpath('//input[7]').click()
		assert self.driver.title == expected

	def test_TC_REGISTER_011(self, set_up):
		expected = 'Registration'
		self.driver.get(settings.MAIN_URL)
		self.driver.find_element_by_id('start').click()
		time.sleep(1)
		self.driver.find_element_by_xpath('//div[3]/a').click()
		time.sleep(1)
		self.driver.find_element_by_name('fname').send_keys('Quoc Viet')
		self.driver.find_element_by_name('lname').send_keys('Hoang')
		self.driver.find_element_by_name('email').send_keys('email1@gmail.com')
		self.driver.find_element_by_name('pwd').send_keys('123')
		self.driver.find_element_by_name('repwd').clear()
		self.driver.find_element_by_xpath('//input[7]').click()
		assert self.driver.title == expected

	def test_TC_REGISTER_012(self, set_up):
		expected = 'Login'
		self.driver.get(settings.MAIN_URL)
		self.driver.find_element_by_id('start').click()
		time.sleep(1)
		self.driver.find_element_by_xpath('//div[3]/a').click()
		time.sleep(1)
		self.driver.find_element_by_xpath('//a').click()
		assert self.driver.title == expected

	# def test_get_tech_member(self, set_up):
	# 	# go to site
	# 	self.driver.get('http://127.0.0.1:8000/')
	# 	# enter the locator of start button and click
	# 	self.driver.find_element_by_id('start').click()
	# 	# enter the locator of email and clear the input field before entering any value
	# 	self.driver.find_element_by_name('email').clear()
	# 	# enter the email
	# 	self.driver.find_element_by_name('email').send_keys('phulikely@gmail.com')
	# 	# enter the locator of password and clear the input field
	# 	self.driver.find_element_by_name('password').clear()
	# 	# enter the password
	# 	self.driver.find_element_by_name('password').send_keys('123')
	# 	# enter the locator of login button and click
	# 	self.driver.find_element_by_id('login').click()
	# 	# enter the locator of project 2 and click
	# 	self.driver.find_element_by_xpath('//div[2]/div/div/a').click()
	# 	time.sleep(1)
	# 	# assert
	# 	expected = 'Mr. T&T'
	# 	actual = self.driver.find_element_by_xpath('//p[3]').text
	# 	self.assertTrue (expected == actual)