# Those who never attempt to achieve their goals shall fall towards the deepest pits of despair.  
import os
import datetime
import hashlib
import subprocess
import time 
# Defines the boot function for the OS
def os_boot():
    force_reconfig = False
    # Gets the current date and time
    crt_datetime = datetime.datetime.now()
    print(f"System booting at: {crt_datetime}")
    print("Initializing boot drive")
    # Checks for a sysroot directory and switches into it:
    if os.path.exists("sysroot") == True:
        os.chdir("sysroot")
        # Checks if the config exists if not invokes the os_config function
        if os.path.exists("sysconf/sysconfig.cnfg") == True:
          with open("sysconf/sysconfig.cnfg", "r") as config:
           contents = config.readlines()
           sys_dir = contents[0].strip()
           usr_name = contents[1].strip()
           mchn_name = contents[4].strip()
           cfg_status = contents[5].strip()
           log_dir = contents[6].strip()
           # Checks all the data by invoking
           print("Begining system integrity check")
           force_reconfig=os_int_check(sys_dir,usr_name,mchn_name,cfg_status,log_dir,force_reconfig)
           if force_reconfig == True:
                os_config()
           else:
                logon()
        else:
            print("The OS configuration file does not exist, you will be prompted to configure the OS once again")
            os_config()
    else:
        print("The main system path is missing, you will be prompted to configure the system")
        os_config()
        # Finalizes boot, clears the screen and passes to logon
    
    
# TO DO: ADD THE BOOT LOG FUNCTION


# Defines the function to check for errors within the system config
def os_int_check(sys_dir, usr_name, mchn_name, cfg_status,log_dir,force_reconfig):
   err_cntr = 0
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
                err_cntr += 1

            if hashlib.sha256(usr_name.encode()).hexdigest() == checklist[1].strip():
                print("usr_name has passed the integrity check, moving on...")
                checklog.writelines(f"usr_name has passed the integrity check at: {datetime.datetime.now()}\n")
            else:
                print("usr_name has failed the integrity check, this might cause log-on issue, please reconfigure the OS if you encounter any issues")
                checklog.writelines(f"usr_name has failed the integrity check at: {datetime.datetime.now()}, please verify the configuration file located in the sysroot dir.\n")
                err_cntr += 1

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
                err_cntr += 1

                if err_cntr >= 2:
                    print(f"The system check has failed, you will be prompted to reconfigure the OS")
                    force_reconfig = True
                else:
                    force_reconfig = False
    else:
        print(f"cfg_status is set as false, if you have configured the system, please check the file")
    return(force_reconfig)
    


# Defines the config function for the OS
def os_config():
    inpt = input("Would you like to begin the configuration, any configuration created before will be deleted Y/N: ")
    if inpt.lower() == "y":
        print("Welcome to the configuration wizard")
        # checks for sysroot and creates the sysroot directory of the system and changes into it for the config if it does not exist, if it does it just changes into it
        os.makedirs("sysroot", exist_ok= True)
        os.chdir("sysroot")
        sys_dir = "sysroot"
        # Creates the log directory 
        os.makedirs("syslog", exist_ok= True)
        log_dir = "syslog"
        # Creates the config directory
        os.makedirs("sysconf", exist_ok= True)
        conf_dir = "sysconf"
        with open("syslog/config.log", "w") as conflog:
            # Gets the username
            usr_name = input("Please input a username: ")
            conflog.writelines(f"Username written to configuration file as {usr_name} at {datetime.datetime.now()}\n")
            # Asks the user if they want a password
            usr_psswd_status = input("Would you like a password for your login? (Y/N): ")
            hashed_psswd = ""
            if usr_psswd_status.lower() == "y":
                usr_psswd = input("Please input a password: ")
                hashed_psswd = hashlib.sha256(usr_psswd.encode()).hexdigest()
                conflog.writelines(f"Password hashed and written as {hashed_psswd} at {datetime.datetime.now()}\n")
            elif usr_psswd_status.lower() == "n":
                conflog.writelines(f"No password has been configured\n")
                pass
            
            # Gets the machine name
            mchn_name = input("Please input a name for your machine: ")
            conflog.write(f"Machine name written to configuration file as {mchn_name} at {datetime.datetime.now()}\n")

            # Finishes the config by writing the data to a file
            cfg_status = "True"
            conflog.writelines(f"Configuration status has been set as {cfg_status} at {datetime.datetime.now()}")

            # Creates a file for the config
            with open("sysconf/sysconfig.cnfg", "w") as config:
                config.writelines([f"{sys_dir}\n", f"{usr_name}\n", f"{usr_psswd_status}\n", f"{hashed_psswd}\n", f"{mchn_name}\n", f"{cfg_status}\n", f"{log_dir}\n"])
            conflog.writelines(f"Configuration has been written to the main config file at {datetime.datetime.now()}")
            # Creates a file for hashed data from the config file used in integrity checks
            with open("hashes.chk", "w") as hashes:
                hashes.writelines([f"{hashlib.sha256(sys_dir.encode()).hexdigest()}\n", f"{hashlib.sha256(usr_name.encode()).hexdigest()}\n", f"{hashlib.sha256(mchn_name.encode()).hexdigest()}\n", f"{hashlib.sha256(log_dir.encode()).hexdigest()}\n"])
        
# Defines the function responsible for logon
def logon():
    # Gets the username
    username = input("Username: ")
    with open("sysconf/sysconfig.cnfg","r") as config:
        confcon = config.readlines()
        pass_true = False
        if confcon[2].strip() == "y":
            while pass_true == False:
                password = input("Password: ")
                with open("hashes.chk", "r") as hashes:
                    hashcon = hashes.readlines()
                    if (hashlib.sha256(username.encode()).hexdigest() == hashcon[1].strip()) and (hashlib.sha256(password.encode()).hexdigest() == confcon[3].strip()):
                        print(f"Welcome to ArchieOS: {username}")
                        pass_true = True
                    else:
                        print("Please try again")    
                        
        else:
            with open("hashes.chk", "r") as hashes:
                hashcon = hashes.readlines()
                if (hashlib.sha256(username.encode()).hexdigest() == hashcon[1].strip()):
                    pass
                    # Pass to main command line (WIP)

def main_cli():
    # TO DO: make the main CLI work
    pass

os_boot()