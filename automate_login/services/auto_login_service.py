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
import time
import pickle
import os
from django.conf import settings

class WebDriverInitiator :

    # '--headless', 

    HEADERS = ['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage', '--disable-extensions', '--enable-cookies', '--enable-features=SameSiteByDefaultCookies', '--disable-blink-features=AutomationControlled']

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

    def agoda_login (browser, credential) : 
        file_path = os.path.join(settings.WEB_COOKIES_PATH, f'agoda_{credential.username}_cookies.pkl')

        print(f"Opening {browser} browser ...")
        driver_obj = WebDriverInitiator(browser=browser, url='https://ycs.agoda.com/mldc/en-us/public/login', headless=True)
        driver = driver_obj.get_driver_instand()
        driver.refresh()
        wait = WebDriverWait(driver, 10)

        if os.path.exists(file_path) :
            with open(file_path, 'rb') as file:
                load_cookies = pickle.load(file)

            for cookie in load_cookies:
                print("Cookie: ", cookie)
                driver.add_cookie(cookie)

            print(f"Agoda {credential.username} session already exist!")

        else:
            time.sleep(3)

            print(f"Agoda {credential.username} login in progress ...")

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

            # Save cookies to a file after successful login
            cookies = driver.get_cookies()

            # Save cookies to a file (e.g., cookies.pkl)
            with open(file_path, 'wb') as file:
                pickle.dump(cookies, file)

        # Refresh the page to apply the cookies (you should now be logged in)
        # driver.refresh()

        # print("Sending message ...")
        # driver.get(f"https://ycs.agoda.com/mldc/en-us/app/hermes/inbox/ycs/{credential.channel_id}?bid={credential.reservation_id}")

        # time.sleep(1)

        # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[data-element-name='inbox-conversation-send-message-text-area']")))
        # text_area = driver.find_element(By.CSS_SELECTOR, "textarea[data-element-name='inbox-conversation-send-message-text-area']")
        # text_area.send_keys("Have a nice day!")
        #send_message_btn = driver.find_element(By.CSS_SELECTOR, "[data-element-name='inbox-conversation-send-message-button']")
        #send_message_btn.click()
        
        print("Agoda message has been sent!")
        #driver.quit()
    
    def airbnb_login (browser, credential) : 
        file_path = os.path.join(settings.WEB_COOKIES_PATH, f'airbnb_{credential.username}_cookies.pkl')
        print("Opening browser ...")
        driver_object = WebDriverInitiator(browser=browser, url='https://www.airbnb.com/login', headless=True)
        driver = driver_object.get_driver_instand()
        wait = WebDriverWait(driver, 10)

        if os.path.exists(f'airbnb_{credential.username}_cookies.pkl') :
            with open(f'airbnb_{credential.username}_cookies.pkl', 'rb') as file:
                load_cookies = pickle.load(file)

            for cookie in load_cookies:
                print("Airbnb Cookie: ", cookie)
                driver.add_cookie(cookie)

            print(f"Airbnb {credential.username} session already exist!")

        else:
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

            time.sleep(3)
            print(f"Airbnb {credential.username} login successfunlly ...")

            cookies = driver.get_cookies()

            with open(file_path, 'wb') as file:
                pickle.dump(cookies, file)

        driver.refresh()

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[href='/hosting']")))

        # for i in ['lak;sdjf;as', '29348232094'] :
        # time.sleep(3)
        # driver.get('https://www.airbnb.com/hosting/messages/' + credential.channel_id + '?query=' + i)
        # wait.until(EC.presence_of_element_located(By.ID, "message_input"))
        # text_area = driver.find_element(By.ID, "message_input")
        # text_area.send_keys("")

        # send_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='messaging_compose_bar_send_button']")
        # send_button.click()

        # driver.quit() 
    
    def rakuten_login (browser, credential) :
        
        driver_object = WebDriverInitiator(browser=browser, url='https://manage.travel.rakuten.co.jp/portal/inn/mp_kanri.main?f_lang=J&f_t_flg=heya&f_flg=RTN', headless=True)
        driver = driver_object.get_driver_instand()
        wait = WebDriverWait(driver, 10)

        if os.path.exists(f'rakuten_{credential.username}_cookies.pkl') :
            with open(f'rakuten_{credential.username}_cookies.pkl', 'rb') as file:
                load_cookies = pickle.load(file)

            for cookie in load_cookies:
                print('Rakuten Cookie: ', cookie)
                driver.add_cookie(cookie)

            print(f"Rakuten {credential.username} session already exist!")

        else:
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

            cookies = driver.get_cookies()

            with open(f'rakuten_{credential.username}_cookies.pkl', 'wb') as file:
                pickle.dump(cookies, file)

        driver.refresh()

        time.sleep(3)

        login_btn = driver.find_element(By.CSS_SELECTOR, "[value='【新】予約者の確認・キャンセル・変更処理']")
        login_btn.click()

        time.sleep(3)

        input_field = driver.find_element(By.CSS_SELECTOR, "[data-testid='searchBox-search-bar']")
        input_field.click()

        time.sleep(3)

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[name='tags.0.searchText']")))
        real_input = driver.find_element(By.CSS_SELECTOR, "[name='tags.0.searchText']")
        real_input.send_keys(credential.reservation_id)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-testid='search-condition-field-taglist']")))
        elements = driver.find_elements(By.CSS_SELECTOR, "ul[data-testid='search-condition-field-taglist'] > li")
        elements[0].click()

        search_btn = driver.find_element(By.CSS_SELECTOR, "[data-testid='searchHeader-submit-button']")
        search_btn.click()

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='bookingList-reservationId']")))
        booking_item = driver.find_element(By.CSS_SELECTOR, "[data-testid='bookingList-reservationId-v1-link']")
        booking_item.click()

        first_window_handle = driver.current_window_handle

        time.sleep(3)

        driver.switch_to.window((driver.window_handles)[1])
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='javascript:onClick=document.act1.submit();']")))
        chat_btn = driver.find_element(By.CSS_SELECTOR, "a[href='javascript:onClick=document.act1.submit();']")
        chat_btn.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[name='send']")))
        btn_send = driver.find_element(By.CSS_SELECTOR, "[name='send']")
        btn_send.click()

        driver.switch_to.window(driver.window_handles[2])

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='f_msg']")))
        text_area = driver.find_element(By.CSS_SELECTOR, "textarea[name='f_msg']")
        text_area.send_keys("Have a nice day!")

        btn_send_message = driver.find_element(By.CSS_SELECTOR, "input[name='send']")
        #btn_send_message.click()


        all_window_handles = driver.window_handles
        for handle in all_window_handles:
            if handle != first_window_handle:
                driver.switch_to.window(handle)
                driver.close()

        driver.switch_to.window(first_window_handle)

        #driver.quit()
