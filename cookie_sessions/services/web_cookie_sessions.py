from automate_login.services.auto_login_service import WebDriverInitiator
from django.conf import settings
import os
import pickle

class CookieSession : 

    def start_session (browser, channel, credential_name):
        url = ''
        if channel == 'agoda' :
            url = 'https://ycs.agoda.com/mldc/en-us/public/login'
        elif channel == 'airbnb' :
            url = 'https://www.airbnb.com/login'
        elif channel == 'rakuten' :
            url = 'https://manage.travel.rakuten.co.jp/portal/inn/mp_kanri.main?f_lang=J&f_t_flg=heya&f_flg=RTN'
        
        CookieSession.get_session(browser=browser, channel=channel, url=url, credential_name=credential_name)

    def get_session (browser, channel, credential_name, url):
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
            print(f"{channel} {credential_name} session file does not exist!")
    
    def get_session_file (channel, credential_name):
        return os.path.join(settings.WEB_COOKIES_PATH, f'{channel}_{credential_name}_cookies.pkl')