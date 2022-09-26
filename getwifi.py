import os

cwd = os.getcwd()

os.system(f"netsh wlan show profile > {cwd}/ssid_profiles.txt")



# Save project path to variable; Run 'netsh wlan show profile' and direct output to new file in project path; 
# get the list of ssid's from the file,
# print them out and let the user choose which one's password should be displayed.

# Once user chooses from the list of ssid's, run 'netsh wlan export profile key=clear'. 
# Open the xml file that the info was saved to using 'with open()'; 
# get the key (pw) inside <keyMaterial> and print it

