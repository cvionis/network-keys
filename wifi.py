import os
import sys
import re
import shlex
import subprocess

def main():
    subprocess.run(["clear"])

    # Redirect output of "netsh wlan show profile" to text file inside project directory
    subprocess.run(["netsh", "wlan", "show" ,"profile", ">", "ssid_profiles.txt"], shell=True)

    # Save each line of the file containing profile info to a list
    with open(f"ssid_profiles.txt", "r+") as f:
        file_split = list((f.read()).split("\n"))

    # Delete text file containing profile information
    subprocess.run(["rm", "-f", f"ssid_profiles.txt"])

    # Get listed user profiles from 'file_split' list and save them to a new list
    profiles = ([(i.split(':'))[1].replace(" ", "") for i in file_split if 'All User Profile' in i])

    # Add profiles to a dictionary, giving each an incremented key ('c') starting from 1
    p_dict = {}
    c = 1

    for i in range(len(profiles)):
        p_dict.update({c:profiles[i]})
        c+=1
        i+=1

    # Print all profiles, use a loop to check selection input, and save input to 'profile_input'
    print("\nChoose a network:\n")
    [print(f"{i}) {p_dict.get(i)}") for i in (p_dict)]

    while True:
        try:
            profile_input = int(input("\n> "))
        except ValueError:
            print("\nError: Enter an integer value")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\n\nExiting script...")
            sys.exit(1)
     
        if (profile_input in p_dict):
            break
        else:
            print("\nInvalid choice: try again")

    profile_value = p_dict.get(profile_input)

    # Export file containing profile's password to current working directory, hide processing info

    subprocess.run(["netsh", "wlan", "export", "profile", f"name={profile_value}", "folder=.", "key=clear", "|", "@echo", "off"], shell=True)

    pw_file = (f"Wi-Fi-{profile_value}.xml")

    # Get <keyMaterial> tag inside exported file, save its contents to variable
    with open(pw_file, "r") as f:
        wifi_pw_element = "".join([i for i in list(f.read().split("\n")) if "keyMaterial" in i])

    wifi_pw = ''.join(re.findall(r'[0-9]', wifi_pw_element))
     
    print(f"\n{profile_value}'s password:\n------------\n| {wifi_pw} |\n------------")

    # Delete file containing info about selected profile
    subprocess.run(["rm", "-f", f"{pw_file}"])

if __name__ == "__main__":
    main()
