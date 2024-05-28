import cmd
import os
import AtikSDK
import time
from datetime import datetime
import LabJackPython as LJUD

class pyAtik(cmd.Cmd):
    prompt = '>> '
    intro = 'Welcome to pyAtik. Type "help" for available commands.'
    # u3Handle = LJUD.openLabJack(LJUD.LJ_dtU3, LJUD.LJ_ctUSB, "1", 1)
    # LJUD.ePut(u3Handle.handle, LJUD.LJ_ioPUT_CONFIG, LJUD.LJ_chLOCALID, 0, 0)

    def do_InitialiseAtik(self, line):
        """Initialising Atik Settings"""
        try:
            print("Connecting to Atik... ")
            cam = AtikSDK.AtikSDKCamera()
            while(cam.is_device_present(0) == False):
                time.sleep(1)
                print("Atik camera is not detected!")
            cam.connect()
            # camera serial code
            serial = cam.get_serial()
            print("Camera serial: ", serial)
            temp_count = cam.get_temperature_sensor_count()
            print("Temperature sensors count:", temp_count)
            if temp_count > 0:
                temp = cam.get_temperature()
                print("Temperature °C:", temp)
            else:
                print("No temperature sensor on camera")
            target_temp = input("Set camera temperature ('C):")
            cam.set_cooling(100*target_temp)
            target_exp = input("Set exposure time (s):")
        except ImportError as e:
            print("Could not import AtikSDK:", str(e))
    def do_SnapshotMode(self, line):
        """ Snapshot Mode - manually trigger Atik"""
        try:
            ValueDIPort = 1 # LJ triggers on logical LOW by grounding FI04 to GND
            while(ValueDIPort != 0):
                os.system('cls')
                # ValueDIPort = LJUD.eDI(u3Handle.handle, 4)
                temp = cam.get_temperature()
                print('waiting for trigger. Temperature °C:',temp/100)
            print('Start exposure...')
            arr = cam.take_image(target_exp)
            now = datetime.now() # current date and time
            while(ArtemisImageReady(cam) == 0.0):
                time.sleep(10)  # we need to wait for the camera to be ready, else we'll get nothing when we download the image
            print("Image size:", arr.shape)
            # Save TIFF
            try:
                import tifffile
                year = now.strftime("%Y")
                month = now.strftime("%m")
                day = now.strftime("%d")
                time = now.strftime("%H:%M:%S")
                file_name = 's' + month + day + '_' + year + '_' + time + '_c' + serial
                tifffile.imwrite(file_name + ".tiff", arr)
            except ImportError as e:
                print("Could not import tifffile to save TIFF image:", str(e))
        except NameError:
            print('Initialise Atik camera first!') 
    def do_quit(self, line):
        """Exit pyAtik"""
        return True

if __name__ == '__main__':
    pyAtik().cmdloop()