from automate_login.services.auto_login_service import WebDriverInitiator
from selenium.webdriver.common.by import By
from django.conf import settings
import os
import pickle
import time
import json


class CookieSession:

    def start_session(browser, channel, credential_name, password):
        url = ""
        if channel == "agoda":
            url = "https://ycs.agoda.com/mldc/en-us/public/login"
        elif channel == "airbnb":
            url = "https://www.airbnb.com/login"
        elif channel == "rakuten":
            url = "https://manage.travel.rakuten.co.jp/portal/inn/mp_kanri.main?f_lang=J&f_t_flg=heya&f_flg=RTN"

        return CookieSession.get_session(
            browser=browser,
            channel=channel,
            url=url,
            credential_name=credential_name,
            password=password,
        )

    def get_session(browser, channel, credential_name, url, password):
        driver_object = WebDriverInitiator(browser, url, headless=False)
        driver = driver_object.get_driver_instand()

        file_path = CookieSession.get_session_file(channel, credential_name)
        print("Cookies file path: ", file_path)

        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                cookies = json.load(file)

            for cookie in cookies:
                driver.add_cookie(cookie)

            driver.refresh()
            print(f"{channel} {credential_name} session reloaded successfully!")
            return {
                "channel": channel,
                "credential_name": credential_name,
                "cookies": cookies,
            }
        else:
            return CookieSession.login(driver, channel, credential_name, password)

    def login(driver, channel, credential_name, password):
        if channel == "agoda":
            print(f"{channel} {credential_name} login in progress ...")
            try:
                # Wait for and switch to the iframe
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC

                iframe = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "iframe[data-cy='ul-app-frame']")
                    )
                )
                driver.switch_to.frame(iframe)

                # Wait for email input and fill in credentials
                email_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "email"))
                )
                password_input = driver.find_element(By.ID, "password")
                email_input.send_keys(credential_name)
                password_input.send_keys(password)

                # Click the login button
                login_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
                )
                login_button.click()

                # Optional: Validate login success (e.g., check for a specific element on the dashboard)
                time.sleep(
                    2
                )  # Replace with WebDriverWait for specific dashboard element
                print(f"{channel} {credential_name} login successfully ...")

                return CookieSession.save_session(
                    driver, channel=channel, credential_name=credential_name
                )

            except Exception as e:
                print(f"[ERROR] Agoda login failed for {credential_name}: {str(e)}")
                raise

        elif channel == "airbnb":
            print(f"Airbnb {credential_name} login in progress ...")
            time.sleep(3)

            email_btn = driver.find_element(
                By.CSS_SELECTOR, "[data-testid='social-auth-button-email']"
            )
            email_btn.click()
            email_field = driver.find_element(By.ID, "email-login-email")
            form_submit = driver.find_element(
                By.CSS_SELECTOR, "[data-testid='auth-form']"
            )
            email_field.send_keys(credential_name)
            form_submit.submit()

            time.sleep(3)

            password_field = driver.find_element(
                By.CSS_SELECTOR, "[name='user[password]']"
            )
            password_field.send_keys(password)
            form_submit2 = driver.find_element(
                By.CSS_SELECTOR, "[data-testid='auth-form']"
            )
            form_submit2.submit()

            print(f"Airbnb {credential_name} login successfunlly ...")
            time.sleep(3)

            return CookieSession.save_session(
                driver, channel=channel, credential_name=credential_name
            )

        elif channel == "rakuten":
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

            return CookieSession.save_session(
                driver, channel=channel, credential_name=credential_name
            )

    def save_session(driver, channel, credential_name):
        """
        Save cookies for a specific session into a unified session data structure.
        """
        cookies = driver.get_cookies()
        session_data = {
            "channel": channel,
            "credential_name": credential_name,
            "cookies": cookies,
        }
        return session_data

    def save_all_sessions_to_file(all_sessions, file_path):
        """
        Save all sessions into a single JSON file.
        """
        with open(file_path, "w") as file:
            json.dump(all_sessions, file, indent=4)
        print(f"All sessions saved successfully to {file_path}")

    def get_session_file(channel, credential_name):
        return os.path.join(
            settings.WEB_COOKIES_PATH, f"{channel}_{credential_name}_cookies.json"
        )

    def get_cookies_as_json(channel, credential_name):
        file_path = CookieSession.get_session_file(
            channel=channel, credential_name=credential_name
        )
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                cookies = pickle.load(file)

            favicon_url = None
            static_url = None
            if channel == "airbnb":
                favicon_url = "https://a0.muscache.com/airbnb/static/logotype_favicon-21cc8e6c6a2cca43f061d2dcabdf6e58.ico"
                static_url = "https://www.airbnb.com/login"
            elif channel == "agoda":
                favicon_url = "https://cdn6.agoda.net/images/ycs/favicon.ico"
                static_url = "https://ycs.agoda.com/mldc/en-us/public/login"
            elif channel == "rakuten":
                favicon_url = "https://www.google.com/s2/favicons?domain=rakuten.com"
                static_url = "https://manage.travel.rakuten.co.jp/portal/inn/mp_kanri.main?f_lang=J&f_t_flg=heya&f_flg=RTN"

            return {
                "   ": {
                    f"{credential_name} {channel}": {
                        "name": credential_name,
                        "aos_slug": channel.lower(),
                        "domain": cookies[0]["domain"] if cookies else None,
                        "faviconUrl": favicon_url,
                        "localStorage": None,
                        "otaPlatform": channel,
                        "profileName": f"{credential_name} {channel}",
                        "searchableText": f"{credential_name} {channel} {cookies[0]['domain'] if cookies else ''}",
                        "staticUrl": static_url,
                        "cookies": cookies,
                    }
                }
            }
        else:
            raise FileNotFoundError(
                f"No cookie file found for {channel} - {credential_name}"
            )

    def get_cookies_as_json_file(channel, credential_name):
        try:
            # Retrieve cookies as JSON object
            cookie_data = CookieSession.get_cookies_as_json(
                channel=channel, credential_name=credential_name
            )
            # Log the JSON object for debugging
            print(
                f"[DEBUG] Cookie data for {channel} - {credential_name}: {cookie_data}"
            )
            # Convert JSON object to a string
            json_content = json.dumps(cookie_data, indent=4)
            return json_content
        except Exception as e:
            # Log the error if any
            print(
                f"[ERROR] Failed to generate JSON file for {channel} - {credential_name}: {e}"
            )
            raise

    def generate_sessions(output_file="all_sessions.json"):

        try:
            web_cookies_path = os.path.join(settings.BASE_DIR, "web_cookies")
            os.makedirs(web_cookies_path, exist_ok=True)
            output_file_path = os.path.join(web_cookies_path, output_file)
            print(f"[DEBUG] Output file path: {output_file_path}")

            # Hardcoded OTA credentials
            ota_credentials = {
                "airbnb": {
                    "username": "guest-haneda-airport@minn.asia",
                    "password": "hpy2raq4ubq6pam-MVX",
                },
                "rakuten": {"username": "theatelh", "password": "theatel.12"},
                "agoda": {
                    "username": "guest-kamata@minn.asia",
                    "password": "Squeeze0901",
                },
            }

            all_sessions = {}
            detailed_results = []

            for ota, credentials in ota_credentials.items():
                result = {
                    "channel": ota,
                    "credential_name": credentials["username"],
                    "status": "failed",
                    "message": None,
                }

                try:
                    print(f"Processing OTA: {ota}")

                    # Generate session using CookieSession
                    profile = CookieSession.start_session(
                        browser="Firefox",
                        channel=ota,
                        credential_name=credentials["username"],
                        password=credentials["password"],
                    )

                    if profile:
                        print(f"[DEBUG] Profile generated for {ota}: {profile}")

                        if ota not in all_sessions:
                            all_sessions[ota] = []
                        all_sessions[ota].append(profile)

                        result["status"] = "success"
                        result["message"] = f"Session generated successfully for {ota}"
                    else:
                        print(f"[DEBUG] No profile returned for {ota}")
                except Exception as e:
                    result["message"] = f"Error: {str(e)}"
                    print(f"[ERROR] {result['message']}")

                detailed_results.append(result)

            # Save sessions to file
            if all_sessions:
                CookieSession.save_all_sessions_to_file(all_sessions, output_file_path)
                print(f"[DEBUG] All sessions saved to {output_file_path}")
            else:
                print("[DEBUG] No sessions to save.")

            return {
                "message": "Sessions generated successfully.",
                "sessions": detailed_results,
            }

        except Exception as e:
            print(f"[ERROR] An error occurred: {e}")
            raise
