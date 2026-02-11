# Those who never attempt to achieve their goals shall fall towards the deepest pits of despair. 
import sys 
import os
import datetime
import hashlib

# Defines the boot function for the OS
def os_boot():
    # Gets the current date and time
    crt_datetime = datetime.datetime.now()
    print(f"System booting at: {crt_datetime}")
    print("Initializing boot drive")
    # Checks for a sysroot directory and switches into it:
    if os.path.exists("sysroot") == True:
        os.chdir("sysroot")
        # Checks if the config exists if not invokes the os_config function
        if os.path.exists("config.cnfg") == True:
          with open("config.cnfg", "r") as config:
           contents = config.readlines()
           sys_dir = contents[0].strip()
           usr_name = contents[1].strip()
           mchn_name = contents[4].strip()
           cfg_status = contents[5].strip()
           log_dir = contents[6].strip()
           # Checks all the data by invoking
           print("Begining system integrity check")
           os_int_check(sys_dir,usr_name,mchn_name,cfg_status,log_dir)
        else:
            print("The OS configuration file does not exist, you will be prompted to configure the OS once again")
            os_config()
    else:
        print("The main system path is missing, you will be prompted to configure the system")
        os_config()
        # Finalizes boot and passes to logon
        logon()
# TO DO: ADD THE BOOT LOG FUNCTION


# Defines the function to check for errors within the system config
def os_int_check(sys_dir, usr_name, mchn_name, cfg_status,log_dir):

   with open("hashes.chk", "r") as hashes:
    checklist = hashes.readlines()
    if cfg_status == "True":
        with open("checklog.log",'w') as checklog:
            if hashlib.sha256(sys_dir.encode()).hexdigest() == checklist[0].strip():
                print("sys_dir has passed the integrity check, moving on...")
                checklog.writelines(f"sys_dir has passed the integrity check at: {datetime.datetime.now()}\n")
            else:
                print("sys_dir has failed the integrity check, please reconfigure the OS if you encounter any issues")
                checklog.writelines(f"sys_dir has failed the integrity check at: {datetime.datetime.now()}, please verify line 1 in the configuration file located in the sysroot dir.\n")
            if hashlib.sha256(usr_name.encode()).hexdigest() == checklist[1].strip():
                print("usr_name has passed the integrity check, moving on...")
                checklog.writelines(f"usr_name has passed the integrity check at: {datetime.datetime.now()}\n")
            else:
                print("usr_name has failed the integrity check, this might cause log-on issue, please reconfigure the OS if you encounter any issues")
                checklog.writelines(f"usr_name has failed the integrity check at: {datetime.datetime.now()}, please verify the configuration file located in the sysroot dir.\n")
            if hashlib.sha256(mchn_name.encode()).hexdigest() == checklist[2].strip():
                print("mchn_name has passed the integrity check, the OS will boot shortly...")
                checklog.writelines(f"mchn_name has passed the integrity check at: {datetime.datetime.now()}\n")
            else:
                print("mchn_name has failed the integrity check, this might cause issues, if you encounter any of them, please reconfigure the OS")
                checklog.writelines(f"mchn_name has failed the integrity check at: {datetime.datetime.now()}, please verify line 5 in the configuration file located in the sysroot dir.\n")
            if hashlib.sha256(log_dir.encode()).hexdigest() == checklist[3].strip():
                print("log_dir has passed the integrity check, moving on")
                checklog.writelines(f"log_dir has passed the integrity check at {datetime.datetime.now()}")
            else:
                print(f"log_dir has failed the system integrity check at {datetime.datetime.now()} issues with logs might arise, please verify line 6 in the configuration file")
                checklog.writelines(f"log_dir has failed the system integrity check at {datetime.datetime.now()} issues with logs might arise, please verify line 6 in the configuration file\n")
                
            
    pass # Work in progress


# Defines the config function for the OS
def os_config():
    inpt = input("Would you like to begin the configuration, any configuration created before will be deleted Y/N: ")
    if inpt.lower() == "y":
        print("Welcome to the configuration wizard")
        # Creates the sysroot directory of the system and changes into it for the config
        os.mkdir("sysroot", exist_ok = True)
        os.chdir("sysroot")
        sys_dir = "sysroot"
        # Creates the log directory 
        os.mkdir("syslog", exist_ok = True)
        log_dir = "syslog"

        # Gets the username
        usr_name = input("Please input a username: ")
        
        # Asks the user if they want a password
        usr_psswd_status = input("Would you like a password for your login? (Y/N): ")
        hashed_psswd = ""
        if usr_psswd_status.lower() == "y":
            usr_psswd = input("Please input a password: ")
            hashed_psswd = hashlib.sha256(usr_psswd.encode()).hexdigest()
        elif usr_psswd_status.lower() == "n":
            pass
        
        # Gets the machine name
        mchn_name = input("Please input a name for your machine: ")
        
        # Finishes the config by writing the data to a file
        cfg_status = "True"
        
        # Creates a file for the config
        with open("config.cnfg", "w") as config:
            config.writelines([f"{sys_dir}\n", f"{usr_name}\n", f"{usr_psswd_status}\n", f"{hashed_psswd}\n", f"{mchn_name}\n", f"{cfg_status}\n", f"{log_dir}\n"])
        # Creates a file for hashed data from the config file used in integrity checks
        with open("hashes.chk", "w") as hashes:
            hashes.writelines([f"{hashlib.sha256(sys_dir.encode()).hexdigest()}\n", f"{hashlib.sha256(usr_name.encode()).hexdigest()}\n", f"{hashlib.sha256(mchn_name.encode()).hexdigest()}\n", f"{hashlib.sha256(log_dir.encode()).hexdigest()}\n"])
        
# Defines the function responsible for logon
def logon():
    # Gets the username and password
    username = input("Username: ")
    password = input("Password (if none leave empty): ")

    # Checks username against config and hash and checks password against hash
    with open("config.cnfg", "r") as config:
        confcon = config.readlines()
        with open("hashes.chk","r") as hashes:
            hashcon = hashes.readlines()
            if (username == confcon[1].strip() and hashlib.sha256(username.encode()).hexdigest() == hashcon[1].strip()) and (hashlib.sha256(password.encode()).hexdigest() == confcon[3].strip()):
                 print(f"Logon successful, welcome to ArchieOS {username}")
    # Passes to TUI renderer 
def tui_renderer():
    # TO DO: ADD TUI
    pass
