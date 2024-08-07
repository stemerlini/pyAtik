import cmd
import os
import AtikSDK
import time
from datetime import datetime
import LabJackPython as LJUD

class pyAtik(cmd.Cmd):
    prompt = '>> '
    intro = 'Welcome to pyAtik. Type "help" for available commands.'
    def do_connect(self, line):
        print("Connecting to Atik... ")
        self.cam = AtikSDK.AtikSDKCamera()
        while(self.cam.is_device_present(0) == False):
            os.system('cls')
            time.sleep(1)
            print("Atik camera is not detected!")
        self.cam.connect()
        print("Atik connected :)")
    def do_InitialiseAtik(self, line):
        """Initialising Atik Settings"""
        try:
            # camera serial code
            self.serial = self.cam.get_serial()
            print("Camera serial: ", self.serial)
            temp = self.cam.get_temperature()
            print("Temperature °C:", temp)
            target_temp = input("Set camera temperature ('C):")
            self.cam.set_cooling(float(target_temp))
            while(temp > float(target_temp)):
                os.system('cls')
                print("Cooling down...")
                temp = self.cam.get_temperature()
                print("Temperature °C:", temp)
                time.sleep(1)
            self.target_exp = input("Set exposure time (s):")
        except ImportError as e:
            print("Could not import AtikSDK:", str(e))
    def do_SnapshotMode(self, line):
        """ Snapshot Mode - manually trigger Atik"""
        try:
            ValueDIPort = 1 # LJ triggers on logical LOW by grounding FI04 to GND
            while(ValueDIPort != 0):
                os.system('cls')
                ValueDIPort = LJUD.eDI(u3Handle.handle, 4)
                temp = self.cam.get_temperature()
                print('waiting for trigger. Temperature °C:',temp)
            print('Start exposure...')
            arr = self.cam.take_image(float(self.target_exp))
            now = datetime.now() # current date and time
            # while(AtikSDK.ArtemisImageReady(self.cam) == 0.0):
            #     time.sleep(10)  # we need to wait for the camera to be ready, else we'll get nothing when we download the image
            print("Image size:", arr.shape)
            # Save TIFF
            try:
                import tifffile
                year = now.strftime("%Y")
                month = now.strftime("%m")
                day = now.strftime("%d")
                time = now.strftime("%H%M%S")
                file_name = './s' + month + day + '_' + year + '_' + time + '_c' + str(self.serial)
                tifffile.imwrite(file_name + ".tiff", arr)
                print("Image saved :)")
            except ImportError as e:
                print("Could not import tifffile to save TIFF image:", str(e))
        except NameError:
            print('Initialise Atik camera first!') 
    def do_quit(self, line):
        """Exit pyAtik"""
        self.cam.disconnect()
        AtikSDK.ArtemisShutdown()
        return True

if __name__ == '__main__':
    u3Handle = LJUD.openLabJack(LJUD.LJ_dtU3, LJUD.LJ_ctUSB, "1", 1)
    LJUD.ePut(u3Handle.handle, LJUD.LJ_ioPUT_CONFIG, LJUD.LJ_chLOCALID, 0, 0)
    pyAtik().cmdloop()