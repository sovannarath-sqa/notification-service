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
