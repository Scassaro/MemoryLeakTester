####################################################
#Program: Memory Leak Tester                       #
#Author: Stephen Cassaro                           #
#Description: Will test for memory leaks in MXK    #
#systems.                                          #
#Company: Dasan Zhone Solutions                    #
####################################################

import time
import telnetlib

########################################################
# Hardcoded IP and login info. All our test MXKs are   #
# the same, so there is no point in wasting time with  #
# user input.                                          #
########################################################

def telnetToMXKAndLogin():
    
    host = "10.155.2.100"
    tn = telnetlib.Telnet(host)
    tn.read_until(b"login:")
    temp = "r"
    tn.write(b"admin\r")
    tn.read_until(b"password:")
    tn.write(b"zhone\r")
    print("Login successful.")
    return tn

########################################################
# Determines type of MXK being queried.                #
# Not currently used, and may not be necessary, but    #
# could be important in later implementations on other #
# platforms.                                           #
########################################################

def determineMXKType(tn):

    tn.read_until(b'zSH>')
    tn.write(b'slots\r')
    time.sleep(1)
    MXKTypeString = tn.read_very_eager().decode('ascii')

    print(MXKTypeString)

########################################################
# Parses the text that comes out of 'card              #
# stats all'.                                          #
########################################################
    
def runMemAnalysis(tn):

    # Collect raw memory data from Telnet object
    
    tn.read_until(b"zSH>")
    tn.write(b"card stats all\r")
    time.sleep(1)
    OutString = tn.read_very_eager().decode('ascii')
    OutArray = [int(s) for s in OutString.split() if s.isdigit()]
    OutArray = [OutArray[9] , OutArray[20]]
    return OutArray

def yesNoYes(tn):
    
    time.sleep(1)
    tn.write(b"yes\r")
    time.sleep(1)
    tn.write(b"no\r")
    time.sleep(1)
    tn.write(b"yes\r")
    time.sleep(1)
    tn.read_until(b"zSH>")
    return

########################################################
# Provision 1024 ONUs and 1 bridge per ONU.            #
########################################################

def provisionAndDeleteBridges(tn):

    tn.write(b"\r")
    time.sleep(1)
    tn.read_until(b"zSH>")
    print("Provisioning in progress, please wait...")
    tn.write(b"onu set 2/[1-16]/[1-64] meprof zhone-2402\r")
    time.sleep(1)
    tn.read_until(b"zSH>")
             
    print("Provisioning ONUs complete. Now provisioning bridges...")
    tn.write(b"bridge add 1-2-[1-16]-[1-64]/gpononu downlink vlan 3503 tagged\r")
    time.sleep(1)
    tn.read_until(b"zSH>")
             
    print("Provisioning bridges complete. Deleting bridges in progress...")
    tn.write(b"bridge delete vlan 3503\r")
    time.sleep(1)
    tn.read_until(b"zSH>")

    print("Bridges deleted. Deleting ONUs in progress...")

    ############################################################

    # Unusable until SLMSC-6362 fixed by Diana. 
    
    #tn.write(b"onu delete 2\r")
    #yesNoYes(tn)

    ############################################################

    # Workaround until above ZOI is fixed.

    tn.write(b"onu delete 2/1")
    yesNoYes(tn)
    tn.write(b"onu delete 2/2")
    yesNoYes(tn)
    tn.write(b"onu delete 2/3")
    yesNoYes(tn)
    tn.write(b"onu delete 2/4")
    yesNoYes(tn)
    tn.write(b"onu delete 2/5")
    yesNoYes(tn)
    tn.write(b"onu delete 2/6")
    yesNoYes(tn)
    tn.write(b"onu delete 2/7")
    yesNoYes(tn)
    tn.write(b"onu delete 2/8")
    yesNoYes(tn)
    tn.write(b"onu delete 2/9")
    yesNoYes(tn)
    tn.write(b"onu delete 2/10")
    yesNoYes(tn)
    tn.write(b"onu delete 2/11")
    yesNoYes(tn)
    tn.write(b"onu delete 2/12")
    yesNoYes(tn)
    tn.write(b"onu delete 2/13")
    yesNoYes(tn)
    tn.write(b"onu delete 2/14")
    yesNoYes(tn)
    tn.write(b"onu delete 2/15")
    yesNoYes(tn)
    tn.write(b"onu delete 2/16")
    yesNoYes(tn)
    
    ############################################################
    
    print("All provisioning removed.")
    return

def main():

    print("Memory Leak Tester\n==================")
    
    tn = telnetToMXKAndLogin()
    #MXKType = determineMXKType(tn)
             
    FirstResult = runMemAnalysis(tn)
    print("Memory before provisioning:\nCard 1 (Control): " + str(FirstResult[0]) + " KB")
    print("Card 2 (Testing): " + str(FirstResult[1]) + " KB")
             
    provisionAndDeleteBridges(tn)
             
    EndResult = runMemAnalysis(tn)
    print("Memory after provisioning:\nCard 1 (Control): " + str(EndResult[0]) + " KB")
    print("Card 2 (Testing): " + str(EndResult[1]) + " KB")

    if(FirstResult[1] > EndResult[1]):
        print(str(FirstResult[1] - EndResult[1]) + " KB less memory available between start and finish.") 
    elif(EndResult[1] > FirstResult[1]):
        print(str(FirstResult[1] - EndResult[1]) + " KB more memory available between start and finish.")
    else:
        print("No memory difference between start and finish.") 
        
    tn.write(b"exit\r")
    tn.close()
             
main()
