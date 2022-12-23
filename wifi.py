import os
import re
import subprocess

def main():
    subprocess.run(["clear"])

    # Redirect output of "netsh wlan show profile" to text file inside project directory
    subprocess.run(["netsh", "wlan", "show", "profile", ">", f"ssid_profiles.txt"])

    # Save each line of the file containing profile info to a list
    with open(f"ssid_profiles.txt", "a+") as f:
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
        profile_input = int(input("\n> "))
     
        if (profile_input in p_dict):
            break
        else:
            print("Invalid choice -- try again")

    profile_value = p_dict.get(profile_input)

    # Export file containing profile's password to current working directory, hide processing info
    cwd = os.getcwd()
    subprocess.run(["netsh", "wlan", "export", "profile", "name={profile_value}", f"folder={cwd}" "key=clear", "|", "@echo", "off"])

    pw_file = (f"Wi-Fi-{profile_value}.xml")

    # Get <keyMaterial> tag inside exported file, save its contents to variable
    with open(f"{pw_file}", "r") as f:
        wifi_pw_element = "".join([i for i in list(f.read().split("\n")) if "keyMaterial" in i])

    wifi_pw = ''.join(re.findall(r'[0-9]', wifi_pw_element))
     
    print(f"\n{profile_value}'s password:\n------------\n| {wifi_pw} |\n------------")

    # Delete file containing info about selected profile
    subprocess.run(["rm", "-f", f"pw_file"])

if __name__ == "__main__":
    main()
