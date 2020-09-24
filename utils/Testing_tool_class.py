import os
import time
import configparser
from ftplib import FTP


class install_Testing_tool():
    def __init__(self):
        self.New_Version = "V104"
        self.download_path = "/home/nvidia/Downloads/"
        self.install_path = "/opt/aetina/"
        self.download_file_location = ''
        self.ftpip = 'fs02.aetina.corp'
        self.username = 'Jetson'
        self.password = 'Aetina111111'


    def download_TT(self,ftpip,user,password):
        ftp = FTP(ftpip)
        ftp.login(user,password)

        ftp.cwd('Testing_tool/')
        lists = ftp.nlst()
        for name in lists:
            TT_locaton = name.find(self.New_Version)
            if TT_locaton > 0 :
                Testin_tool_name = name
        
        print(Testin_tool_name)
        self.download_file_location = self.download_path + Testin_tool_name
        print(self.download_file_location)

        f = open(self.download_file_location,'wb')
        bufsize = 1024
        filename = 'RETR ' + Testin_tool_name
        ftp.retrbinary(filename,f.write,bufsize)
        #time.sleep(2)
        ftp.quit()
        os.system("tar -C " + self.download_path + " -zxvf " + self.download_file_location)



    def Check_Testing_tool_download(self):

        if os.path.isdir(self.download_path + "Testing_tool"):
            print("Find old version,start remove...")
            os.system("sudo rm -r " + self.download_path + "Testing*")
        else:
            print("Prepare download new verion...")

        self.download_TT(self.ftpip,self.username,self.password)

    def Check_Aetina_folder(self):
        if os.path.isdir(self.install_path):
            print("aetina is exist")
            if os.path.isdir(self.install_path + 'bin'):
                print("find old Version")
                if os.path.isfile(self.install_path + '/bin/config.ini'):
                    print("find config.ini")
                    times = self.load_ini(self.install_path + '/bin/config.ini')
                    if times == 0:
                        os.system("sudo rm -r " + self.install_path )
                        os.system("sudo cp -ax " + self.download_path + "aetina/ " + "/opt" )
                        self.Run_Testing_tool()
                    else:
                        self.Run_Testing_tool()
            else:
                self.Run_Testing_tool()
        else:
            print("Reinstall Testing tool")
            os.system("sudo cp -ax " + self.download_path + "aetina/ " + "/opt" )
            self.Run_Testing_tool()


    def load_ini(self,location):
        conf = configparser.ConfigParser()
        conf.read(location)
        times = conf.getint("items","times")
        print(times)
        return times

    def Run_Testing_tool(self):
        commend = "sudo " + self.install_path +'bin/Aetina -a'
        os.system(commend)