import os

# Use 'netsh wlan show profile' and get all listed user profiles; print them out and let the user choose which one's
# password should be displayed

# Once user chooses from the list of ssid's, run 'netsh wlan export profile key=clear'. 
# Open the xml file the info was saved to using with open(); get the key (pw) inside <keyMaterial> and print it