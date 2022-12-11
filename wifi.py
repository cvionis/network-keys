import os
import re
import subprocess

subprocess.run(["clear"])
cwd = os.getcwd()

# Direct output of command to text file inside project directory
subprocess.run(["netsh", "wlan", "show", "profile", ">", f"{cwd}/profile_info/ssid_profiles.txt"])

# Save each line of file containing profile info to a list
with open(f"{cwd}/profile_info/ssid_profiles.txt", "r") as f:
    file_split = list((f.read()).split("\n"))

# Delete all files inside profile_info 
subprocess.run(["rm", "-f", f"{cwd}/profile_info/*")

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

# Export file containing profile's password to 'profile_info' directory, hide processing info
subprocess.run(["netsh", "wlan", "export", "profile", "name={profile_value}", f"folder={cwd}profile_info", "key=clear", "|", "@echo", "off"])

pw_file_name = (f"Wi-Fi-{profile_value}")

# Get <keyMaterial> tag inside exported file, save its contents to variable
with open(f"{cwd}\\profile_info\\{pw_file_name}.xml", "r") as f:
    wifi_pw_element = "".join([i for i in list(f.read().split("\n")) if "keyMaterial" in i])

wifi_pw = ''.join(re.findall(r'[0-9]', wifi_pw_element))
 
print(f"\n{profile_value}'s password:\n------------\n| {wifi_pw} |\n------------")

# Delete all files inside 'profile_info' directory
subprocess.run(["rm", f"{cwd}/profile_info/*"])
