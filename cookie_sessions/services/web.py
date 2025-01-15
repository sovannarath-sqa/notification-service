def generate_sessions(output_file="all_sessions.json", props_file="props.json"):
    try:
        # Define paths for web cookies and props.json
        web_cookies_path = os.path.join(settings.BASE_DIR, "web_cookies")

        os.makedirs(web_cookies_path, exist_ok=True)
        output_file_path = os.path.join(web_cookies_path, output_file)

        print(f"[DEBUG] Output file path: {output_file_path}")

        # TODO: Call vault API to get account lists
        vault = fetchVaule()

        # Loop through the vault list

        # TODO: for each list, fetch detail
        # TODO: for each detail title, find usernamme, password and website
        # TODO: get ota name by matching the website
        # TODO: login to selenium based on OTA and username/pw
        # TODO: sva profile to profile data
        # TODO: Output

        all_sessions = {}
        detailed_results = []

        # Iterate over properties and their OTAs
        for vault_item in vault:

            item = fetchDetailItem(vault_item)
            username = ""
            password = ""
            title = vault_item["title"]

            for field in item["fields"]:
                if field["id"] == "username":
                    username = field["value"]

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
