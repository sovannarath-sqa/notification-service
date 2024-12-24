from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FireFoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.conf import settings
import time
import pickle
import os

class WebDriverInitiator :

    HEADERS = [
        '--disable-gpu', 
        '--no-sandbox', 
        '--disable-dev-shm-usage',
        '--disable-extensions', 
        '--enable-cookies', 
        '--enable-features=SameSiteByDefaultCookies', 
        '--disable-blink-features=AutomationControlled'
    ]

    def __init__(self, browser, url, headless) :
        if (browser == 'Chrome') :
            self.options = ChromeOptions()
            if headless == True :
                for header in WebDriverInitiator.HEADERS :
                    self.options.add_argument(header)
            self.driver = webdriver.Chrome(options= self.options, service=ChromeService(ChromeDriverManager().install()))
        elif (browser == 'Firefox') :
            self.options = FirefoxOptions()
            if headless == False :
                for header in WebDriverInitiator.HEADERS :
                    self.options.add_argument(header)
            self.driver = webdriver.Firefox(options=self.options, service=FireFoxService(GeckoDriverManager().install()))

        self.driver.get(url)

    def get_driver_instand (self) :
        return self.driver


class AutoLoginService :

    def Open_brower (browser, channel):
        print(f"Opening {browser} browser ...")
        
        url = ''
        if channel == 'agoda' :
            url = 'https://ycs.agoda.com/mldc/en-us/public/login'
        elif channel == 'airbnb' :
            url = 'https://www.airbnb.com/login'
        elif channel == 'rakuten' :
            url = 'https://manage.travel.rakuten.co.jp/portal/inn/mp_kanri.main?f_lang=J&f_t_flg=heya&f_flg=RTN'

        driver_object = WebDriverInitiator(browser, url, headless=True)
        driver = driver_object.get_driver_instand()
        return driver
        
    def load_session (driver, channel, credential_name):
        session_existed = False
        file_path = AutoLoginService.get_session_file(channel=channel, credential_name=credential_name)
        print("Cookies: ", file_path)

        if os.path.exists(file_path) :
            existed = True
            with open(file_path, 'rb') as file:
                load_cookies = pickle.load(file)

            for cookie in load_cookies:
                print("Cookie:", cookie)
                driver.add_cookie(cookie)

        driver.refresh()
        return session_existed
    
    def save_session (driver, channel, credential_name) :
        file_path = AutoLoginService.get_session_file(channel=channel, credential_name=credential_name)
        cookies = driver.get_cookies()
        with open(file_path, 'wb') as file:
            pickle.dump(cookies, file)

        return driver
    
    def get_session_file (channel, credential_name):
        return os.path.join(settings.WEB_COOKIES_PATH, f'{channel}_{credential_name}_cookies.pkl')

    def agoda_login (browser, credential, reservations) :
        driver = AutoLoginService.Open_brower(browser=browser, channel=credential.channel)
        wait = WebDriverWait(driver, 10)

        

        if AutoLoginService.load_session(driver=driver, channel=credential.channel, credential_name=credential.username) == False :
            time.sleep(3)

            print(f"{credential.channel} {credential.username} login in progress ...")
            iframe = driver.find_element(By.CSS_SELECTOR, "iframe[data-cy='ul-app-frame']")
            driver.switch_to.frame(iframe)
            email_input = driver.find_element(By.ID, "email")
            password_input = driver.find_element(By.ID, "password")
            email_input.send_keys(credential.username)
            password_input.send_keys(credential.password)
            login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()

            time.sleep(2)
            print(f"Agoda {credential.username} login successfunlly ...")
            
            driver = AutoLoginService.save_session(driver=driver, channel=credential.channel, credential_name=credential.username)

        # Sending batch message
        for data in reservations : 
            driver.get(f"https://ycs.agoda.com/mldc/en-us/app/hermes/inbox/ycs/{credential.channel}?bid={data.reservation_id}")

            time.sleep(2)

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[data-element-name='inbox-conversation-send-message-text-area']")))
            text_area = driver.find_element(By.CSS_SELECTOR, "textarea[data-element-name='inbox-conversation-send-message-text-area']")

            # Message content
            text_area.send_keys(data.message)

            print("Sending message ...")

            send_message_btn = driver.find_element(By.CSS_SELECTOR, "[data-element-name='inbox-conversation-send-message-button']")
            send_message_btn.click()

            time.sleep(2)
            print(f"Reservation {data.reservation_id} message has been sent!")
        
        driver.quit()
    
    def airbnb_login (browser, credential, reservations) : 
        driver = AutoLoginService.Open_brower(browser=browser, channel=credential.channel)
        wait = WebDriverWait(driver, 10)

        if AutoLoginService.load_session(driver=driver, channel=credential.channel, credential_name=credential.username) == False :
            print(f"Airbnb {credential.username} login in progress ...")
            time.sleep(3)

            email_btn = driver.find_element(By.CSS_SELECTOR, "[data-testid='social-auth-button-email']")
            email_btn.click()
            email_field = driver.find_element(By.ID, "email-login-email")
            form_submit = driver.find_element(By.CSS_SELECTOR, "[data-testid='auth-form']")
            email_field.send_keys(credential.username)
            form_submit.submit()

            time.sleep(3)
        
            password_field = driver.find_element(By.CSS_SELECTOR, "[name='user[password]']")
            password_field.send_keys(credential.password)
            form_submit2 = driver.find_element(By.CSS_SELECTOR, "[data-testid='auth-form']")
            form_submit2.submit()

            print(f"Airbnb {credential.username} login successfunlly ...")
            time.sleep(3)

            driver = AutoLoginService.save_session(driver=driver, channel=credential.channel, credential_name=credential.username)

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[href='/hosting']")))

        for data in reservations :
            time.sleep(3)
            driver.get('https://www.airbnb.com/hosting/messages/' + credential.channel_id + '?query=' + data.reservation_id)
            wait.until(EC.presence_of_element_located(By.ID, "message_input"))
            text_area = driver.find_element(By.ID, "message_input")

            # Message Content
            text_area.send_keys(data.message)

            print("Message sending ...")
            send_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='messaging_compose_bar_send_button']")
            send_button.click()

            time.sleep(2)
            print(f"Reservation {data.reservation_id} message has been sent!")

        driver.quit() 
    
    def rakuten_login (browser, credential, reservations) :
        driver = AutoLoginService.Open_brower(browser=browser, channel=credential.channel)
        wait = WebDriverWait(driver, 10)

        if AutoLoginService.load_session(driver=driver, channel=credential.channel, credential_name=credential.username) == False :
            print(f"Rakuten {credential.username} login in progress ...")
            time.sleep(3)

            username_field = driver.find_element(By.CSS_SELECTOR, "[name='f_id']")
            password_input = driver.find_element(By.CSS_SELECTOR, "[name='f_pass']")
            username_field.send_keys(credential.username)
            password_input.send_keys(credential.password)
            login_button = driver.find_element(By.XPATH, "//input[@type='submit']")
            login_button.click()

            time.sleep(1)
            print(f"Rakuten {credential.username} login successfunlly ...")

            driver = AutoLoginService.save_session(driver=driver, channel=credential.channel, credential_name=credential.username)

        login_btn = driver.find_element(By.CSS_SELECTOR, "[value='【新】予約者の確認・キャンセル・変更処理']")
        login_btn.click()
        time.sleep(3)

        # Current browser tab
        first_window_handle = driver.current_window_handle

        for data in reservations :

            input_field = driver.find_element(By.CSS_SELECTOR, "[data-testid='searchBox-search-bar']")
            input_field.click()
            time.sleep(3)

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[name='tags.0.searchText']")))
            real_input = driver.find_element(By.CSS_SELECTOR, "[name='tags.0.searchText']")
            real_input.send_keys(data.reservation_id)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-testid='search-condition-field-taglist']")))
            elements = driver.find_elements(By.CSS_SELECTOR, "ul[data-testid='search-condition-field-taglist'] > li")
            elements[0].click()

            search_btn = driver.find_element(By.CSS_SELECTOR, "[data-testid='searchHeader-submit-button']")
            search_btn.click()

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='bookingList-reservationId']")))
            booking_item = driver.find_element(By.CSS_SELECTOR, "[data-testid='bookingList-reservationId-v1-link']")
            booking_item.click()
            time.sleep(3)

            # Swithc to secnod tab
            driver.switch_to.window((driver.window_handles)[1])
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='javascript:onClick=document.act1.submit();']")))
            chat_btn = driver.find_element(By.CSS_SELECTOR, "a[href='javascript:onClick=document.act1.submit();']")
            chat_btn.click()
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[name='send']")))
            btn_send = driver.find_element(By.CSS_SELECTOR, "[name='send']")
            btn_send.click()
            
            # Switch to third tab
            driver.switch_to.window(driver.window_handles[2])

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='f_msg']")))
            text_area = driver.find_element(By.CSS_SELECTOR, "textarea[name='f_msg']")

            # Message content
            text_area.send_keys(data.message)

            btn_send_message = driver.find_element(By.CSS_SELECTOR, "input[name='send']")
            btn_send_message.click()

            all_window_handles = driver.window_handles
            for handle in all_window_handles:
                if handle != first_window_handle:
                    driver.switch_to.window(handle)
                    driver.close()

            driver.switch_to.window(first_window_handle)

        driver.quit()
