import os
import sys
import re
import subprocess

def main():
    # Store network profiles inside a local text file
    subprocess.run(["netsh", "wlan", "show" ,"profile", ">", 
        "ssid_profiles.txt"], shell=True)

    with open(f"ssid_profiles.txt", "r") as f:
        lines = f.readlines()

    profiles = ([(i.split(':'))[1].replace(" ", "") for line in lines 
        if 'All User Profile' in line])
    subprocess.run(["rm", "-f", f"ssid_profiles.txt"])

    profile_dict = {}
    for i in range(len(profiles)):
        profile_dict.update({i+1:profiles[i]})
        i+=1

    print("\nChoose a network:\n")
    [print(f"{i}) {profile_dict.get(i)}") for i in (profile_dict)]

    while True:
        try:
            profile_input = int(input("\n> "))
        except ValueError:
            print("\nError: Enter an integer value")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\n\nExiting script...")
            sys.exit(1)

        if (profile_input in profile_dict):
            break
        else:
            print("\nInvalid choice: Choose a number from the list")

    profile = profile_dict.get(profile_input)

    # Export file containing profile's password to current working directory
    subprocess.run(["netsh", "wlan", "export", "profile", f"name={profile}", 
        "folder=.", "key=clear", "|", "@echo", "off"], shell=True)

    pw_file = (f"Wi-Fi-{profile}.xml")

    with open(pw_file, "r") as f:
        lines = f.readlines()

    pw_element = "".join([line for line in lines if "keyMaterial" in line])
    wifi_pw = ''.join(re.findall(r'[0-9]', pw_element))
     
    print(f"\n{profile}'s password:\n\n{wifi_pw}")

    subprocess.run(["rm", "-f", f"{pw_file}"])

if __name__ == "__main__":
    main()
