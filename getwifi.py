import os

cwd = os.getcwd()

# Direct output of command to text file inside project directory
os.system(f"netsh wlan show profile > {cwd}/ssid_profiles.txt")

with open(f"{cwd}/ssid_profiles.txt", "r") as f:
    file_split = list((f.read()).split("\n"))

profiles = [(i.split(':'))[1] for i in file_split if 'All User Profile' in i]

p_dict = {}

c = 1

for i in range(len(profiles)):
    p_dict.update({c: profiles[i]})
    c+=1
    i+=1

print("\nChoose a network:\n")
[print(f"{e} {p_dict.get(e)}") for e in (p_dict)]


while True:
    profile_input = int(input())
    
    if (profile_input in p_dict):
        break
    else:
        print("Try again")
# Save project path to variable; Run 'netsh wlan show profile' and direct output to new file in project path; 
# get the list of ssid's from the file,
# print them out and let the user choose which one's password should be displayed.

# Once user chooses from the list of ssid's, run 'netsh wlan export profile key=clear'. 
# Open the xml file that the info was saved to using 'with open()'; 
# get the key (pw) inside <keyMaterial> and print it

