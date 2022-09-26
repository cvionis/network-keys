import os
import re

cwd = os.getcwd()

# Direct output of command to text file inside project directory
os.system(f"netsh wlan show profile > {cwd}/profile_info/ssid_profiles.txt")

# Note: Save path as variable at some point in order to simply substitution
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
[print(f"{e} {p_dict.get(e)}") for e in (p_dict)]

# Note: Add counter that exits program after enough failed tries are occur
while True:
    profile_input = int(input())
    
    if (profile_input in p_dict):
        break
    else:
        print("Try again")


os.system(f"netsh wlan export profile name={p_dict.get(profile_input)} folder={cwd}\profile_info key=clear")

pw_file_name = (f"Wi-Fi-{p_dict.get(profile_input)}")

with open(f"{cwd}\\profile_info\\{pw_file_name}.xml", "r") as f:
    wifi_pw_element = "".join([i for i in list(f.read().split("\n")) if "keyMaterial" in i])
# Can probably do this more efficiently (like searching for 8 numbers and returning the first matching instance)
wifi_pw = ''.join(re.findall(r'[0-9]', wifi_pw_element))
    
print(f"{p_dict.get(profile_input)}'s password: {wifi_pw}")