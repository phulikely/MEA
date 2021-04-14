# System basic lib
import time
# The 3rd party
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
	# def test_TC_INDEX_001(self, set_up):
	# 	expected = 'Welcome to VMO'
	# 	self.driver.get(settings.MAIN_URL)
	# 	assert self.driver.title == expected

	# def test_TC_INDEX_002(self, set_up):
	# 	expected = 'Login'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	assert self.driver.title == expected


	# Login Screen
	# def test_TC_LOGIN_001(self, set_up):
	# 	expected = 'Project Index'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	self.driver.find_element_by_name('email').clear()
	# 	self.driver.find_element_by_name('email').send_keys('phulikely@gmail.com')
	# 	self.driver.find_element_by_name('password').clear()
	# 	self.driver.find_element_by_name('password').send_keys('123')
	# 	self.driver.find_element_by_id('login').click()
	# 	assert self.driver.title == expected

	def test_TC_LOGIN_002(self, set_up):
		expected = 'Invalid email or password!'
		path = self.get_file_name_by_time(settings.LOGIN_PATH)
		self.driver.get(settings.MAIN_URL)
		start_btn = self.driver.find_element_by_id('start')
		time.sleep(2)
		self.draw_rectangle(start_btn).save(path)
		time.sleep(2)
		start_btn.click()
		self.driver.find_element_by_name('email').clear()
		email = self.driver.find_element_by_name('email')
		email.send_keys('phulikely@gmail.com')
		path = self.get_file_name_by_time(settings.LOGIN_PATH)
		self.draw_rectangle(email).save(path)
		time.sleep(2)
		self.driver.find_element_by_name('password').clear()
		password = self.driver.find_element_by_name('password')
		password.send_keys('12345')
		path = self.get_file_name_by_time(settings.LOGIN_PATH)
		self.draw_rectangle(password).save(path)
		time.sleep(2)
		login_btn = self.driver.find_element_by_id('login')
		path = self.get_file_name_by_time(settings.LOGIN_PATH)
		self.draw_rectangle(login_btn).save(path)
		time.sleep(2)
		login_btn.click()
		err_msg = self.driver.find_element_by_xpath('//label')
		path = self.get_file_name_by_time(settings.LOGIN_PATH)
		self.draw_rectangle(err_msg).save(path)
		time.sleep(2)
		assert err_msg.text == expected 

	# def test_TC_LOGIN_003(self, set_up):
	# 	expected = 'Invalid email or password!'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	self.driver.find_element_by_name('email').clear()
	# 	self.driver.find_element_by_name('email').send_keys('phulikely123@gmail.com')
	# 	self.driver.find_element_by_name('password').clear()
	# 	self.driver.find_element_by_name('password').send_keys('123')
	# 	self.driver.find_element_by_id('login').click()
	# 	err_msg = self.driver.find_element_by_xpath('//label')
	# 	assert err_msg.text == expected

	# def test_TC_LOGIN_004(self, set_up):
	# 	expected = 'Invalid email or password!'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	self.driver.find_element_by_name('email').clear()
	# 	self.driver.find_element_by_name('email').send_keys('phulikely123@gmail.com')
	# 	self.driver.find_element_by_name('password').clear()
	# 	self.driver.find_element_by_name('password').send_keys('12345')
	# 	self.driver.find_element_by_id('login').click()
	# 	err_msg = self.driver.find_element_by_xpath('//label')
	# 	assert err_msg.text == expected

	# def test_TC_LOGIN_005(self, set_up):
	# 	expected = 'Registration'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	self.driver.find_element_by_xpath('//div[3]/a').click()
	# 	assert self.driver.title == expected


	# Registration Screen
	# def test_TC_REGISTER_001(self, set_up):
	# 	expected = 'Login'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	time.sleep(2)
	# 	self.driver.find_element_by_xpath('//div[3]/a').click()
	# 	time.sleep(2)
	# 	self.driver.find_element_by_name('fname').send_keys('Quoc Viet')
	# 	self.driver.find_element_by_name('lname').send_keys('Hoang')
	# 	self.driver.find_element_by_name('email').send_keys('email1@gmail.com')
	# 	self.driver.find_element_by_name('pwd').send_keys('12345')
	# 	self.driver.find_element_by_name('repwd').send_keys('12345')
	# 	self.driver.find_element_by_xpath('//input[7]').click()
	# 	assert self.driver.title == expected

	# def test_TC_REGISTER_002(self, set_up):
	# 	expected = 'Passwords do not match!'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	#time.sleep(2)
	# 	#self.driver.find_element_by_xpath('//div[3]/a').click()
	# 	WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[3]/a"))).click()
	# 	#time.sleep(2)
	# 	#self.driver.find_element_by_name('fname').send_keys('Quoc Viet')
	# 	WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "fname"))).send_keys('Quoc Viet')
	# 	#self.driver.find_element_by_name('lname').send_keys('Hoang')
	# 	WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "lname"))).send_keys('Hoang')
	# 	#self.driver.find_element_by_name('email').send_keys('email2@gmail.com')
	# 	WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys('email2@gmail.com')
	# 	#self.driver.find_element_by_name('pwd').send_keys('12345')
	# 	WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "pwd"))).send_keys('12345')
	# 	#self.driver.find_element_by_name('repwd').send_keys('123456789')
	# 	WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "repwd"))).send_keys('12345678')
	# 	#self.driver.find_element_by_xpath('//input[7]').click()
	# 	WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[7]"))).click()
	# 	assert self.driver.find_element_by_xpath('//label').text == expected

	def test_TC_REGISTER_003(self, set_up):
		expected = 'Email already existed!'
		path = self.get_file_name_by_time(settings.REGISTER_PATH)
		self.driver.get(settings.MAIN_URL)
		time.sleep(2)
		start_btn = self.driver.find_element_by_id('start')
		self.draw_rectangle(start_btn).save(path)
		time.sleep(2)
		start_btn.click()
		register_btn = self.driver.find_element_by_xpath('//div[3]/a')
		path = self.get_file_name_by_time(settings.REGISTER_PATH)
		self.draw_rectangle(register_btn).save(path)
		time.sleep(2)
		register_btn.click()
		time.sleep(2)
		fname = self.driver.find_element_by_name('fname')
		fname.send_keys('Quoc Viet')
		path = self.get_file_name_by_time(settings.REGISTER_PATH)
		self.draw_rectangle(fname).save(path)
		time.sleep(2)
		lname = self.driver.find_element_by_name('lname')
		lname.send_keys('Hoang')
		path = self.get_file_name_by_time(settings.REGISTER_PATH)
		self.draw_rectangle(lname).save(path)
		time.sleep(2)
		email = self.driver.find_element_by_name('email')
		email.send_keys('phulikely@gmail.com')
		path = self.get_file_name_by_time(settings.REGISTER_PATH)
		self.draw_rectangle(email).save(path)
		time.sleep(2)	
		pwd = self.driver.find_element_by_name('pwd')
		pwd.send_keys('12345')
		path = self.get_file_name_by_time(settings.REGISTER_PATH)
		self.draw_rectangle(pwd).save(path)
		time.sleep(2)
		repwd = self.driver.find_element_by_name('repwd')
		repwd.send_keys('12345')
		path = self.get_file_name_by_time(settings.REGISTER_PATH)
		self.draw_rectangle(repwd).save(path)
		time.sleep(2)		
		reg_btn = self.driver.find_element_by_xpath('//input[7]')
		path = self.get_file_name_by_time(settings.REGISTER_PATH)
		self.draw_rectangle(reg_btn).save(path)
		time.sleep(2)
		reg_btn.click()
		time.sleep(2)
		err = self.driver.find_element_by_xpath('//label')
		path = self.get_file_name_by_time(settings.REGISTER_PATH)
		self.draw_rectangle(err).save(path)
		time.sleep(2)		
		assert err.text == expected

	# def test_TC_REGISTER_004(self, set_up):
	# 	expected = 'Login'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	time.sleep(2)
	# 	self.driver.find_element_by_xpath('//div[3]/a').click()
	# 	time.sleep(2)
	# 	self.driver.find_element_by_name('fname').send_keys('😂')
	# 	self.driver.find_element_by_name('lname').send_keys('😂')
	# 	self.driver.find_element_by_name('email').send_keys('email1@gmail.com')
	# 	self.driver.find_element_by_name('pwd').send_keys('123')
	# 	self.driver.find_element_by_name('repwd').send_keys('123')
	# 	self.driver.find_element_by_xpath('//input[7]').click()
	# 	assert self.driver.title == expected

	def test_TC_REGISTER_005(self, set_up):
		expected = 'Login'
		self.driver.get(settings.MAIN_URL)
		self.driver.find_element_by_id('start').click()
		time.sleep(2)
		self.driver.find_element_by_xpath('//div[3]/a').click()
		time.sleep(2)
		self.driver.find_element_by_name('fname').send_keys('Quoc Viet')
		self.driver.find_element_by_name('lname').send_keys('Hoang')
		self.driver.find_element_by_name('email').send_keys('email1@gmail.com')
		self.driver.find_element_by_name('pwd').send_keys('😂')
		self.driver.find_element_by_name('repwd').send_keys('😂')
		self.driver.find_element_by_xpath('//input[7]').click()
		assert self.driver.title == expected

	# def test_TC_REGISTER_006(self, set_up):
	# 	expected = 'Login'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	time.sleep(2)
	# 	self.driver.find_element_by_xpath('//div[3]/a').click()
	# 	time.sleep(2)
	# 	self.driver.find_element_by_name('fname').send_keys('Quoc Viet')
	# 	self.driver.find_element_by_name('lname').send_keys('Hoang')
	# 	self.driver.find_element_by_name('email').send_keys('email😂1@gmail.com')
	# 	self.driver.find_element_by_name('pwd').send_keys('123')
	# 	self.driver.find_element_by_name('repwd').send_keys('123')
	# 	self.driver.find_element_by_xpath('//input[7]').click()
	# 	assert self.driver.title == expected

	# def test_TC_REGISTER_007(self, set_up):
	# 	expected = 'Registration'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	time.sleep(2)
	# 	self.driver.find_element_by_xpath('//div[3]/a').click()
	# 	time.sleep(2)
	# 	self.driver.find_element_by_name('fname').clear()
	# 	self.driver.find_element_by_name('lname').send_keys('Hoang')
	# 	self.driver.find_element_by_name('email').send_keys('email1@gmail.com')
	# 	self.driver.find_element_by_name('pwd').send_keys('123')
	# 	self.driver.find_element_by_name('repwd').send_keys('123')
	# 	self.driver.find_element_by_xpath('//input[7]').click()
	# 	assert self.driver.title == expected

	# def test_TC_REGISTER_008(self, set_up):
	# 	expected = 'Registration'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	time.sleep(2)
	# 	self.driver.find_element_by_xpath('//div[3]/a').click()
	# 	time.sleep(2)
	# 	self.driver.find_element_by_name('fname').send_keys('Quoc Viet')
	# 	self.driver.find_element_by_name('lname').clear()
	# 	self.driver.find_element_by_name('email').send_keys('email1@gmail.com')
	# 	self.driver.find_element_by_name('pwd').send_keys('123')
	# 	self.driver.find_element_by_name('repwd').send_keys('123')
	# 	self.driver.find_element_by_xpath('//input[7]').click()
	# 	assert self.driver.title == expected

	# def test_TC_REGISTER_009(self, set_up):
	# 	expected = 'Registration'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	time.sleep(2)
	# 	self.driver.find_element_by_xpath('//div[3]/a').click()
	# 	time.sleep(2)
	# 	self.driver.find_element_by_name('fname').send_keys('Quoc Viet')
	# 	self.driver.find_element_by_name('lname').send_keys('Hoang')
	# 	self.driver.find_element_by_name('email').clear()
	# 	self.driver.find_element_by_name('pwd').send_keys('123')
	# 	self.driver.find_element_by_name('repwd').send_keys('123')
	# 	self.driver.find_element_by_xpath('//input[7]').click()
	# 	assert self.driver.title == expected

	# def test_TC_REGISTER_010(self, set_up):
	# 	expected = 'Registration'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	time.sleep(2)
	# 	self.driver.find_element_by_xpath('//div[3]/a').click()
	# 	time.sleep(2)
	# 	self.driver.find_element_by_name('fname').send_keys('Quoc Viet')
	# 	self.driver.find_element_by_name('lname').send_keys('Hoang')
	# 	self.driver.find_element_by_name('email').send_keys('email1@gmail.com')
	# 	self.driver.find_element_by_name('pwd').clear()
	# 	self.driver.find_element_by_name('repwd').send_keys('123')
	# 	self.driver.find_element_by_xpath('//input[7]').click()
	# 	assert self.driver.title == expected

	# def test_TC_REGISTER_011(self, set_up):
	# 	expected = 'Registration'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	time.sleep(2)
	# 	self.driver.find_element_by_xpath('//div[3]/a').click()
	# 	time.sleep(2)
	# 	self.driver.find_element_by_name('fname').send_keys('Quoc Viet')
	# 	self.driver.find_element_by_name('lname').send_keys('Hoang')
	# 	self.driver.find_element_by_name('email').send_keys('email1@gmail.com')
	# 	self.driver.find_element_by_name('pwd').send_keys('123')
	# 	self.driver.find_element_by_name('repwd').clear()
	# 	self.driver.find_element_by_xpath('//input[7]').click()
	# 	assert self.driver.title == expected

	# def test_TC_REGISTER_012(self, set_up):
	# 	expected = 'Login'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	time.sleep(2)
	# 	self.driver.find_element_by_xpath('//div[3]/a').click()
	# 	time.sleep(2)
	# 	self.driver.find_element_by_xpath('//a').click()
	# 	assert self.driver.title == expected

	# def test_TC_ProIndex_001(self, set_up):
	# 	expected = 'Project Index'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	self.driver.find_element_by_name('email').clear()
	# 	self.driver.find_element_by_name('email').send_keys('phulikely@gmail.com')
	# 	self.driver.find_element_by_name('password').clear()
	# 	self.driver.find_element_by_name('password').send_keys('123')
	# 	self.driver.find_element_by_id('login').click()
	# 	assert self.driver.title == expected
	# 	assert 'Project 2' in self.driver.page_source

	# def test_TC_ProIndex_002(self, set_up):
	# 	expected = 'Project Index'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	self.driver.find_element_by_name('email').clear()
	# 	self.driver.find_element_by_name('email').send_keys('phulikely@gmail.com')
	# 	self.driver.find_element_by_name('password').clear()
	# 	self.driver.find_element_by_name('password').send_keys('123')
	# 	self.driver.find_element_by_id('login').click()
	# 	assert self.driver.title == expected
	# 	assert 'Project 2' in self.driver.page_source

	def test_TC_AddPro_001(self, set_up):
		expected = 'Project Index'
		self.driver.get(settings.MAIN_URL)
		path = self.get_file_name_by_time(settings.CREATE_NEW_PRO_PATH)
		start_btn = self.driver.find_element_by_id('start')
		time.sleep(2)
		self.draw_rectangle(start_btn).save(path)
		time.sleep(2)
		start_btn.click()
		self.driver.find_element_by_name('email').clear()
		email = self.driver.find_element_by_name('email')	
		email.send_keys('phulikely@gmail.com')
		path = self.get_file_name_by_time(settings.CREATE_NEW_PRO_PATH)		
		time.sleep(2)
		self.draw_rectangle(email).save(path)
		time.sleep(2)
		self.driver.find_element_by_name('password').clear()
		password = self.driver.find_element_by_name('password')
		password.send_keys('123')
		path = self.get_file_name_by_time(settings.CREATE_NEW_PRO_PATH)
		time.sleep(2)
		self.draw_rectangle(password).save(path)
		time.sleep(2)
		login_btn = self.driver.find_element_by_id('login')
		time.sleep(2)
		path = self.get_file_name_by_time(settings.CREATE_NEW_PRO_PATH)
		self.draw_rectangle(login_btn).save(path)
		time.sleep(2)
		login_btn.click()
		time.sleep(2)		
		add_pro_btn = self.driver.find_element_by_link_text('Add Project')
		path = self.get_file_name_by_time(settings.CREATE_NEW_PRO_PATH)
		self.draw_rectangle(add_pro_btn).save(path)
		time.sleep(2)
		add_pro_btn.click()
		title = self.driver.find_element_by_id('project_title')
		title.send_keys('Project 3')
		time.sleep(2)
		path = self.get_file_name_by_time(settings.CREATE_NEW_PRO_PATH)
		self.draw_rectangle(title).save(path)
		time.sleep(2)
		desc = self.driver.find_element_by_id('project_description')
		desc.send_keys('This is Project 3')
		time.sleep(2)
		path = self.get_file_name_by_time(settings.CREATE_NEW_PRO_PATH)
		self.draw_rectangle(desc).save(path)
		time.sleep(2)
		tech = self.driver.find_element_by_id('project_technology')
		tech.send_keys('Django')
		time.sleep(2)
		path = self.get_file_name_by_time(settings.CREATE_NEW_PRO_PATH)
		self.draw_rectangle(tech).save(path)
		time.sleep(2)
		mem = self.driver.find_element_by_id('project_member')
		mem.send_keys('Quoc Viet')
		time.sleep(2)
		path = self.get_file_name_by_time(settings.CREATE_NEW_PRO_PATH)
		self.draw_rectangle(mem).save(path)
		time.sleep(2)
		btn_img = self.driver.find_element_by_id('btn_img')
		btn_img.send_keys('C:\\Users\\VMO-PHUCH\\Downloads\\3.png')
		time.sleep(2)
		path = self.get_file_name_by_time(settings.CREATE_NEW_PRO_PATH)
		self.draw_rectangle(btn_img).save(path)
		time.sleep(2)
		btn_single = self.driver.find_element_by_id('singlebutton')
		time.sleep(2)
		path = self.get_file_name_by_time(settings.CREATE_NEW_PRO_PATH)
		self.draw_rectangle(btn_single).save(path)
		time.sleep(2)
		btn_single.click()
		time.sleep(2)
		#self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		pro_new = self.driver.find_element_by_xpath('//div[3]/div/div/a')
		#self.driver.execute_script("arguments[0].scrollIntoView();", pro_new)
		time.sleep(2)
		path = self.get_file_name_by_time(settings.CREATE_NEW_PRO_PATH)
		self.draw_rectangle(pro_new).save(path)
		time.sleep(2)
		assert self.driver.title == expected
		assert 'Project 3' in self.driver.page_source

	# def test_TC_AddPro_002(self, set_up):
	# 	expected = 'Add New Project'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	self.driver.find_element_by_name('email').clear()
	# 	self.driver.find_element_by_name('email').send_keys('phulikely@gmail.com')
	# 	path = self.get_file_name_by_time(settings.CREATE_NEW_PRO_PATH)
	# 	self.driver.find_element_by_name('password').clear()
	# 	self.driver.find_element_by_name('password').send_keys('123')
	# 	self.driver.find_element_by_id('login').click()
	# 	self.driver.find_element_by_link_text('Add Project').click()
	# 	time.sleep(2)
	# 	#self.driver.find_element_by_id('project_title').clear()
	# 	WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "project_description"))).click()
	# 	#self.driver.find_element_by_id('project_description').send_keys('This is Project 4')
	# 	self.driver.find_element_by_id('project_technology').send_keys('Django')
	# 	self.driver.find_element_by_id('project_member').send_keys('Quoc Viet')
	# 	self.driver.find_element_by_id('btn_img').send_keys('C:\\Users\\VMO-PHUCH\\Downloads\\moon1.jpg')
	# 	self.driver.find_element_by_id('singlebutton').click()
	# 	assert self.driver.title == expected			
		
	# def test_TC_AddPro_003(self, set_up):
	# 	expected = 'Add New Project'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	self.driver.find_element_by_name('email').clear()
	# 	self.driver.find_element_by_name('email').send_keys('phulikely@gmail.com')
	# 	path = self.get_file_name_by_time(settings.CREATE_NEW_PRO_PATH)				
	# 	self.driver.find_element_by_name('password').clear()
	# 	self.driver.find_element_by_name('password').send_keys('123')
	# 	self.driver.find_element_by_id('login').click()
	# 	self.driver.find_element_by_link_text('Add Project').click()
	# 	self.driver.find_element_by_id('project_title').send_keys('Project 4')
	# 	self.driver.find_element_by_id('project_description').clear()
	# 	self.driver.find_element_by_id('project_technology').send_keys('Django')
	# 	self.driver.find_element_by_id('project_member').send_keys('Quoc Viet')
	# 	self.driver.find_element_by_id('btn_img').send_keys('C:\\Users\\VMO-PHUCH\\Downloads\\moon1.jpg')
	# 	self.driver.find_element_by_id('singlebutton').click()
	# 	assert self.driver.title == expected

	# def test_TC_AddPro_004(self, set_up):
	# 	expected = 'Add New Project'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	self.driver.find_element_by_name('email').clear()
	# 	self.driver.find_element_by_name('email').send_keys('phulikely@gmail.com')
	# 	path = self.get_file_name_by_time(settings.CREATE_NEW_PRO_PATH)				
	# 	#self.driver.find_element_by_name('password').clear()
	# 	self.driver.find_element_by_name('password').send_keys('123')
	# 	self.driver.find_element_by_id('login').click()
	# 	self.driver.find_element_by_link_text('Add Project').click()
	# 	self.driver.find_element_by_id('project_title').send_keys('Project 4')
	# 	self.driver.find_element_by_id('project_description').send_keys('This is Project 4')
	# 	self.driver.find_element_by_id('project_technology').clear()
	# 	self.driver.find_element_by_id('project_member').send_keys('Quoc Viet')
	# 	self.driver.find_element_by_id('btn_img').send_keys('C:\\Users\\VMO-PHUCH\\Downloads\\moon1.jpg')
	# 	self.driver.find_element_by_id('singlebutton').click()
	# 	assert self.driver.title == expected

	# def test_TC_AddPro_005(self, set_up):
	# 	expected = 'Add New Project'
	# 	self.driver.get(settings.MAIN_URL)
	# 	self.driver.find_element_by_id('start').click()
	# 	self.driver.find_element_by_name('email').clear()
	# 	self.driver.find_element_by_name('email').send_keys('phulikely@gmail.com')
	# 	path = self.get_file_name_by_time(settings.CREATE_NEW_PRO_PATH)				
	# 	self.driver.find_element_by_name('password').clear()
	# 	self.driver.find_element_by_name('password').send_keys('123')
	# 	self.driver.find_element_by_id('login').click()
	# 	self.driver.find_element_by_link_text('Add Project').click()
	# 	self.driver.find_element_by_id('project_title').send_keys('Project 5')
	# 	self.driver.find_element_by_id('project_description').send_keys('This is Project 5')
	# 	self.driver.find_element_by_id('project_technology').send_keys('Flask')
	# 	self.driver.find_element_by_id('project_member').clear()
	# 	self.driver.find_element_by_id('btn_img').send_keys('C:\\Users\\VMO-PHUCH\\Downloads\\moon1.jpg')
	# 	self.driver.find_element_by_id('singlebutton').click()
	# 	assert self.driver.title == expected

	def test_TC_AddPro_006(self, set_up):
		expected = 'Add New Project'
		self.driver.get(settings.MAIN_URL)
		# self.driver.find_element_by_id('start').click()
		# self.driver.find_element_by_name('email').clear()
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "start"))).click()
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).clear()
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys('phulikely@gmail.com')
		#self.driver.find_element_by_name('email').send_keys('phulikely@gmail.com')
		path = self.get_file_name_by_time(settings.CREATE_NEW_PRO_PATH)				
		#self.driver.find_element_by_name('password').clear()
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).clear()
		#self.driver.find_element_by_name('password').send_keys('123')
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys('123')
		#self.driver.find_element_by_id('login').click()
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "login"))).click()
		#self.driver.find_element_by_link_text('Add Project').click()
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Add Project"))).click()
		#self.driver.find_element_by_id('project_title').send_keys('Project 4')
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "project_title"))).send_keys('Project 4')
		#self.driver.find_element_by_id('project_description').send_keys('This is Project 4')
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "project_description"))).send_keys('This is Project 4')
		#self.driver.find_element_by_id('project_technology').send_keys('Django')
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "project_technology"))).send_keys('Django')
		#self.driver.find_element_by_id('project_member').send_keys('Quoc Viet')
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "project_member"))).send_keys('Quoc Viet')
		self.driver.find_element_by_id('btn_img').send_keys('C:\\Users\\VMO-PHUCH\\Downloads\\test.txt')
		#WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "btn_img"))).send_keys('C:\\Users\\VMO-PHUCH\\Downloads\\test.txt')
		#self.driver.find_element_by_id('singlebutton').click()
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "singlebutton"))).click()
		assert self.driver.title == expected

	# def test_TC_AddPro_007(self, set_up):
	# 	expected = 'Add New Project'
	# 	self.driver.get(settings.MAIN_URL)
	# 	WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "start"))).click()
	# 	WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).clear()
	# 	WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys('phulikely@gmail.com')
	# 	path = self.get_file_name_by_time(settings.CREATE_NEW_PRO_PATH)				
	# 	WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).clear()
	# 	WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys('123')
	# 	WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "login"))).click()
	# 	WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Add Project"))).click()
	# 	#self.driver.find_element_by_id('project_title').clear()
	# 	#self.driver.find_element_by_id('project_description').clear()
	# 	#self.driver.find_element_by_id('project_technology').clear()
	# 	#self.driver.find_element_by_id('project_member').clear()
	# 	self.driver.find_element_by_id('btn_img').send_keys('C:\\Users\\VMO-PHUCH\\Downloads\\moon1.jpg')
	# 	self.driver.find_element_by_id('singlebutton').click()
	# 	assert self.driver.title == expected

	def test_TC_ProDetail_001(self, set_up):
		expected = 'Mr. B'
		self.driver.get(settings.MAIN_URL)
		path = self.get_file_name_by_time(settings.PRO_DETAIL_PATH)
		start_btn = self.driver.find_element_by_id('start')
		time.sleep(2)
		self.draw_rectangle(start_btn).save(path)
		time.sleep(2)
		start_btn.click()
		self.driver.find_element_by_name('email').clear()
		email = self.driver.find_element_by_name('email')	
		email.send_keys('phulikely@gmail.com')
		path = self.get_file_name_by_time(settings.PRO_DETAIL_PATH)		
		time.sleep(2)
		self.draw_rectangle(email).save(path)
		time.sleep(2)		
		self.driver.find_element_by_name('password').clear()
		password = self.driver.find_element_by_name('password')
		password.send_keys('123')
		path = self.get_file_name_by_time(settings.PRO_DETAIL_PATH)
		time.sleep(2)
		self.draw_rectangle(password).save(path)
		time.sleep(2)
		login_btn = self.driver.find_element_by_id('login')
		time.sleep(2)
		path = self.get_file_name_by_time(settings.PRO_DETAIL_PATH)
		self.draw_rectangle(login_btn).save(path)
		time.sleep(2)
		login_btn.click()
		project_2 = self.driver.find_element_by_xpath('//div[2]/div/div/a')
		time.sleep(2)
		path = self.get_file_name_by_time(settings.PRO_DETAIL_PATH)
		self.draw_rectangle(project_2).save(path)
		time.sleep(2)
		project_2.click()
		actual = self.driver.find_element_by_xpath('//p[3]')
		time.sleep(2)
		path = self.get_file_name_by_time(settings.PRO_DETAIL_PATH)
		self.draw_rectangle(actual).save(path)		
		assert actual.text == expected