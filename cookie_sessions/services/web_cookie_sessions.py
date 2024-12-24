from automate_login.services.auto_login_service import WebDriverInitiator
from selenium.webdriver.common.by import By
from django.conf import settings
import os
import pickle
import time

class CookieSession : 

    def start_session (browser, channel, credential_name, password):
        url = ''
        if channel == 'agoda' :
            url = 'https://ycs.agoda.com/mldc/en-us/public/login'
        elif channel == 'airbnb' :
            url = 'https://www.airbnb.com/login'
        elif channel == 'rakuten' :
            url = 'https://manage.travel.rakuten.co.jp/portal/inn/mp_kanri.main?f_lang=J&f_t_flg=heya&f_flg=RTN'
        
        CookieSession.get_session(browser=browser, channel=channel, url=url, credential_name=credential_name, password=password)

    def get_session (browser, channel, credential_name, url, password):
        driver_object = WebDriverInitiator(browser, url, headless=False)
        driver = driver_object.get_driver_instand()

        file_path = CookieSession.get_session_file(channel=channel, credential_name=credential_name)
        print("Cookies: ", file_path)

        if os.path.exists(file_path) :
            with open(file_path, 'rb') as file:
                load_cookies = pickle.load(file)

            for cookie in load_cookies:
                print("Cookie:", cookie)
                driver.add_cookie(cookie)

            driver.refresh()
            print(f"{channel} {credential_name} session reload successfuly!")
        else:
            CookieSession.login(driver, channel, credential_name, password)
    
    def login (driver, channel, credential_name, password) :
            if channel == 'agoda' :
                print(f"{channel} {credential_name} login in progress ...")
                iframe = driver.find_element(By.CSS_SELECTOR, "iframe[data-cy='ul-app-frame']")
                driver.switch_to.frame(iframe)
                email_input = driver.find_element(By.ID, "email")
                password_input = driver.find_element(By.ID, "password")
                email_input.send_keys(password)
                password_input.send_keys(credential_name)

                login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                login_button.click()
                time.sleep(2)
                print(f"{channel} {credential_name} login successfunlly ...")
                return CookieSession.save_session(driver, channel=channel, credential_name=credential_name)
            
            elif channel == 'airbnb' :
                print(f"Airbnb {credential_name} login in progress ...")
                time.sleep(3)

                email_btn = driver.find_element(By.CSS_SELECTOR, "[data-testid='social-auth-button-email']")
                email_btn.click()
                email_field = driver.find_element(By.ID, "email-login-email")
                form_submit = driver.find_element(By.CSS_SELECTOR, "[data-testid='auth-form']")
                email_field.send_keys(credential_name)
                form_submit.submit()

                time.sleep(3)
        
                password_field = driver.find_element(By.CSS_SELECTOR, "[name='user[password]']")
                password_field.send_keys(password)
                form_submit2 = driver.find_element(By.CSS_SELECTOR, "[data-testid='auth-form']")
                form_submit2.submit()

                print(f"Airbnb {credential_name} login successfunlly ...")
                time.sleep(3)

                return CookieSession.save_session(driver, channel=channel, credential_name=credential_name)

            elif channel == 'rakuten' :
                print(f"Rakuten {credential_name} login in progress ...")
                time.sleep(3)

                username_field = driver.find_element(By.CSS_SELECTOR, "[name='f_id']")
                password_input = driver.find_element(By.CSS_SELECTOR, "[name='f_pass']")
                username_field.send_keys(credential_name)
                password_input.send_keys(password)
                login_button = driver.find_element(By.XPATH, "//input[@type='submit']")
                login_button.click()

                time.sleep(1)
                print(f"Rakuten {credential_name} login successfunlly ...")

                return CookieSession.save_session(driver, channel=channel, credential_name=credential_name)
            
    def save_session (driver, channel, credential_name) :
        file_path = CookieSession.get_session_file(channel=channel, credential_name=credential_name)
        cookies = driver.get_cookies()
        with open(file_path, 'wb') as file:
            pickle.dump(cookies, file)

        return driver

    def get_session_file (channel, credential_name):
        return os.path.join(settings.WEB_COOKIES_PATH, f'{channel}_{credential_name}_cookies.pkl')

                        