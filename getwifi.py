import os
import re

os.system("clear")
cwd = os.getcwd()

# Direct output of command to text file inside project directory
os.system(f"netsh wlan show profile > {cwd}/profile_info/ssid_profiles.txt")

with open(f"{cwd}/profile_info/ssid_profiles.txt", "r") as f:
    file_split = list((f.read()).split("\n"))

profiles = ([(i.split(':'))[1].replace(" ", "") for i in file_split if 'All User Profile' in i])
p_dict = {}

c = 1

for i in range(len(profiles)):
    p_dict.update({c:profiles[i]})
    c+=1
    i+=1

print("\nChoose a network:\n")
[print(f"{e}) {p_dict.get(e)}") for e in (p_dict)]

while True:
    profile_input = int(input("\n> "))
 
    if (profile_input in p_dict):
        break
    else:
        print("Invalid choice -- try again")

profile_value = p_dict.get(profile_input)

os.system(f"netsh wlan export profile name={profile_value} folder={cwd}\profile_info key=clear")

pw_file_name = (f"Wi-Fi-{profile_value}")

with open(f"{cwd}\\profile_info\\{pw_file_name}.xml", "r") as f:
    wifi_pw_element = "".join([i for i in list(f.read().split("\n")) if "keyMaterial" in i])

wifi_pw = ''.join(re.findall(r'[0-9]', wifi_pw_element))
 
print(f"{profile_value}'s password: {wifi_pw}")

os.system(f"rm {cwd}/profile_info/*")