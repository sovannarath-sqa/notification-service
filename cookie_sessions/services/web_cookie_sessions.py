from automate_login.services.auto_login_service import WebDriverInitiator
from selenium.webdriver.common.by import By
from django.conf import settings
import os
import pickle
import time
import json
import requests


BASE_URL = settings.OP_CONNECT_HOST
VAULT_ID = "nubfqfqv44rnsd4w3rfuyfsu2i"
HEADERS = {
    "Authorization": f"Bearer {settings.OP_API_TOKEN}",
    "Content-Type": "application/json",
}


class CookieSession:

    def start_session(browser, channel, credential_name, password):
        url = ""
        if channel == "agoda":
            url = "https://ycs.agoda.com/mldc/en-us/public/login"
        elif channel == "airbnb":
            url = "https://www.airbnb.com/login"
        elif channel == "rakuten":
            url = "https://manage.travel.rakuten.co.jp/portal/inn/mp_kanri.main?f_lang=J&f_t_flg=heya&f_flg=RTN"

        print(f"[DEBUG] Channel: {channel}, URL: {url}")

        # Validate URL
        if not url:
            raise ValueError(f"Invalid or unsupported channel: {channel}")

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
        cookies = driver.get_cookies()

        formatted_cookies = []
        for cookie in cookies:
            formatted_cookies.append(
                {
                    "domain": cookie.get("domain"),
                    "expirationDate": (
                        cookie.get("expiry") * 1000 if "expiry" in cookie else None
                    ),
                    "hostOnly": cookie.get("hostOnly", False),
                    "httpOnly": cookie.get("httpOnly", False),
                    "name": cookie.get("name"),
                    "path": cookie.get("path", "/"),
                    "sameSite": cookie.get("sameSite", "unspecified"),
                    "secure": cookie.get("secure", False),
                    "session": cookie.get("session", False),
                    "storeId": cookie.get("storeId", "0"),
                    "value": cookie.get("value"),
                }
            )

        session_data = {
            "channel": channel,
            "credential_name": credential_name,
            "cookies": formatted_cookies,
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
            # Create output directory for cookies
            web_cookies_path = os.path.join(os.getcwd(), "web_cookies")
            os.makedirs(web_cookies_path, exist_ok=True)
            output_file_path = os.path.join(web_cookies_path, output_file)

            print(f"[DEBUG] Output file path: {output_file_path}")

            # Fetch vault items
            response = requests.get(
                f"{BASE_URL}/v1/vaults/{VAULT_ID}/items", headers=HEADERS
            )
            if response.status_code != 200:
                raise Exception(f"Failed to fetch vault items: {response.text}")

            vault_items = response.json()
            all_sessions = {}
            detailed_results = []

            for vault_item in vault_items:
                try:
                    item_id = vault_item["id"]
                    item_response = requests.get(
                        f"{BASE_URL}/v1/vaults/{VAULT_ID}/items/{item_id}",
                        headers=HEADERS,
                    )
                    if item_response.status_code != 200:
                        raise Exception(
                            f"Failed to fetch item details: {item_response.text}"
                        )

                    item_details = item_response.json()

                    # Extract credentials and website
                    username = None
                    password = None
                    title = vault_item.get("title", "Unknown Title")
                    website = None
                    channel = None

                    # Fetch username and password from fields
                    for field in item_details.get("fields", []):
                        if field.get("id") == "username":
                            username = field.get("value")
                        elif field.get("id") == "password":
                            password = field.get("value")

                    # Use additionalInformation as fallback for username
                    if not username:
                        username = vault_item.get("additionalInformation")

                    # Get the primary website URL
                    for url in item_details.get("urls", []):
                        if url.get("primary", False):
                            website = url.get("href")
                            break

                    # Validate and sanitize the website URL
                    if website:
                        if not website.startswith(("http://", "https://")):
                            website = f"https://{website.strip()}"

                    # Map URL to channel
                    if website:
                        if "airbnb.com" in website:
                            channel = "airbnb"
                        elif "agoda.com" in website:
                            channel = "agoda"
                        elif "rakuten.co.jp" in website:
                            channel = "rakuten"

                    # Skip if any required field is missing
                    if not username or not password or not website or not channel:
                        print(
                            f"[WARNING] Missing required details for item: {title}. Skipping."
                        )
                        continue

                    print(f"[INFO] Logging into {website} with username: {username}")
                    print(f"[DEBUG] Channel: {channel}, URL: {website}")

                    result = {
                        "channel": channel,
                        "title": title,
                        "username": username,
                        "status": "failed",
                        "message": "No profile generated",
                    }

                    # Start session
                    profile = CookieSession.start_session(
                        browser="Firefox",
                        channel=channel,
                        credential_name=username,
                        password=password,
                    )

                    if profile:
                        if website not in all_sessions:
                            all_sessions[website] = []
                        all_sessions[website].append(profile)

                        result["status"] = "success"
                        result["message"] = "Session generated successfully"

                    detailed_results.append(result)

                except Exception as e:
                    print(
                        f"[ERROR] Error processing item {vault_item.get('title', 'Unknown')}: {str(e)}"
                    )

            # Save all sessions to a file
            if all_sessions:
                CookieSession.save_all_sessions_to_file(all_sessions, output_file_path)
                print(f"[INFO] All sessions saved to {output_file_path}")
            else:
                print("[INFO] No sessions to save.")

            return {
                "message": "Sessions generated successfully.",
                "sessions": detailed_results,
            }

        except Exception as e:
            print(f"[ERROR] An error occurred: {e}")
            raise

    def fetch_profile_sessions(file_path="all_sessions.json"):
        try:
            full_path = os.path.join(settings.BASE_DIR, "web_cookies", file_path)
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"File not found: {full_path}")

            with open(full_path, "r") as file:
                profiles = json.load(file)

            formatted_profiles = {}

            # Enhance each profile with additional metadata
            for channel, sessions in profiles.items():
                for session in sessions:
                    credential_name = session.get("credential_name")
                    cookies = session.get("cookies", [])

                    # Default metadata based on the channel
                    favicon_url, static_url = None, None

                    if channel == "airbnb":
                        favicon_url = "https://a0.muscache.com/airbnb/static/logotype_favicon-21cc8e6c6a2cca43f061d2dcabdf6e58.ico"
                        static_url = "https://www.airbnb.com/hosting/messages"
                    elif channel == "agoda":
                        favicon_url = "https://cdn6.agoda.net/images/ycs/favicon.ico"
                        static_url = "https://ycs.agoda.com/mldc/en-us/app/reporting/booking/55052795"
                    elif channel == "rakuten":
                        favicon_url = (
                            "https://trv.r10s.com/eve/static/images/favicon.ico"
                        )
                        static_url = "https://manage.travel.rakuten.co.jp/portal/inn/mp_kanri.main?f_lang=J&f_no=182771&f_t_flg=heya&f_flg=RTN"

                    # Construct the profile data
                    profile_key = (
                        f"{credential_name} {channel}" if credential_name else channel
                    )
                    profile_data = {
                        "name": credential_name,
                        "aos_slug": credential_name.lower(),
                        "domain": (
                            "https://www.airbnb.com"
                            if channel == "airbnb"
                            else (
                                "https://manage.travel.rakuten.co.jp"
                                if channel == "rakuten"
                                else (
                                    "https://ycs.agoda.com"
                                    if channel == "agoda"
                                    else cookies[0]["domain"] if cookies else None
                                )
                            )
                        ),
                        "faviconUrl": favicon_url,
                        "localStorage": None,
                        "otaPlatform": channel,
                        "profileName": profile_key,
                        "searchableText": f"{profile_key} {cookies[0]['domain'] if cookies else ''}",
                        "staticUrl": static_url,
                        "cookies": cookies,
                    }

                    # Add to formatted profiles
                    if profile_key not in formatted_profiles:
                        formatted_profiles[profile_key] = profile_data

            print(
                f"[DEBUG] Profiles fetched and formatted successfully from {full_path}"
            )
            return {"profileData": formatted_profiles}

        except FileNotFoundError as fnfe:
            print(f"[ERROR] {str(fnfe)}")
            return {"error": str(fnfe)}
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred: {str(e)}")
            return {
                "error": "An unexpected error occurred. Please check the logs for more details."
            }

    def generate_sessions_from_json(
        output_file="all_sessions.json", props_file="props.json"
    ):
        try:
            # Define paths for web cookies and props.json
            web_cookies_path = os.path.join(settings.BASE_DIR, "web_cookies")
            props_file_path = os.path.join(settings.BASE_DIR, props_file)
            os.makedirs(web_cookies_path, exist_ok=True)
            output_file_path = os.path.join(web_cookies_path, output_file)

            print(f"[DEBUG] Output file path: {output_file_path}")

            # Load properties from props.json
            with open(props_file_path, "r") as props_file:
                props_data = json.load(props_file)

            # Hardcoded credentials for simplicity (can be replaced later)
            ota_credentials = {
                "airbnb": {
                    "username": "guest-haneda-airport@minn.asia",
                    "password": "hpy2raq4ubq6pam-MVX",
                },
                "rakuten": {
                    "username": "theatelh",
                    "password": "theatel.12",
                },
                "agoda": {
                    "username": "guest-kamata@minn.asia",
                    "password": "Squeeze0901",
                },
            }

            all_sessions = {}
            detailed_results = []

            # Iterate over properties and their OTAs
            for property_item in props_data["properties"]:
                property_name = property_item["name"]
                otas = property_item["otas"]

                for ota in otas:
                    if ota not in ota_credentials:
                        print(f"[WARNING] No credentials found for OTA: {ota}")
                        continue

                    credentials = ota_credentials[ota]
                    result = {
                        "channel": ota,
                        "property_name": property_name,
                        "credential_name": credentials["username"],
                        "status": "failed",
                        "message": None,
                    }

                    try:
                        print(f"Processing OTA: {ota} for property: {property_name}")

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
                            result["message"] = (
                                f"Session generated successfully for {ota}"
                            )
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
