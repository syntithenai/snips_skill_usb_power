"""
Prerequisites:
uhubctl is on the path
"""

import subprocess

class UsbPowerSkill:

    def __init__(self,tts_service=None):
        """ Initialisation.
        :param db: the json database.
        :param tts_service: A TTS service, i.e. an object which has a
                            `speak(text)` method for speaking the result.
                                                       
Current status for hub 1-1, vendor 0424:9514, 5 ports
   Port 1: 0503 highspeed power enable connect [0424:ec00]
   Port 2: 0100 power
   Port 3: 0100 power
   Port 4: 0503 highspeed power enable connect [1415:2000 OmniVision Technologies, Inc. USB Camera-B4.09.24.1]
   Port 5: 0103 power enable connect [046d:c52b Logitech USB Receiver]
                            
        """
        self.tts_service = tts_service
        
    def usb_get_devices(self):
        output = subprocess.check_output('uhubctl',shell = True)
        return output
        
    def usb_load_devices(self,output):
        results=[]
        for result in output.splitlines():
            portId = result[8:9]
            partsA = result.split(":")
            if len(partsA) >= 2:
                text = result[16:]
                parts = result.split("[")
                port = {'id':portId}
                if parts[0].find("power") != -1 :
                    port['power'] = True
                else:
                    port['power'] = False
                    
                if parts[0].find("connect") != -1 :
                    port['connect'] = True
                else:
                    port['connect'] = False
                
                if len(parts) == 2:
                    port['deviceId'] = parts[1][0:9]
                    device = parts[1][10:]
                    port['device'] = device[:-1]
                    
                results.append(port)
        return results
        
    def usb_find_device(self,description,results):
        for result in results:
            print(result)
            if ('device' in result.keys() and result['device'].find(description)!=-1):
                print('found device matching {}'.format(description))
                print(result['device'])
                return result
            elif ('deviceId' in result and description == result['deviceId']):
                print('found deviceID matching {}'.format(description))
                print(result['deviceId'])
                return result
        return None
    
    def usb_list_devices(self,results):
        outputs=[]
        portsOff=[]
        for result in results:
            if result['power']:
                if 'device' in result.keys() and len(result['device']) > 0:
                    outputs.append("{} on usb port {} ".format(result['device'],result['id']))
                elif 'deviceId' in result.keys() and len(result['deviceId']) > 0:
                    outputs.append("Device ID {} on usb port {} ".format(result['deviceId'],result['id']))
                else:
                    outputs.append("Nothing plugged into usb port {} ".format(result['id']))
            else:
                outputs.append("Usb port {} is switched off".format(result['id']))
        return "\n".join(outputs)
        
    def usb_list_devices_say(self,results):    
        response=self.usb_list_devices(results);
        if self.tts_service:
           self.tts_service.speak(response)

        
    def usb_power_on(self,usbPortIdentifier):
        results=self.usb_load_devices(self.usb_get_devices())
        device=self.find_device(usbPortIdentifier,results)
        response=''
        if device is not None:
            if not device['power']:
                if 'device' in device.keys() or 'deviceId' in device.keys():
                    response="Turning on power to {}".format(usbPortIdentifier)
                else:
                    response="Turning on power to empty usb port {}".format(usbPortIdentifier)
            else:
                response="{} is already turned on".format(usbPortIdentifier)
        else:
            response="Could not find a usb port matching {}".format(usbPortIdentifier)
        return response;
        
    def usb_power_on_say(self,usbPortIdentifier):
        response = self.usb_power_on(self,usbPortIdentifier)
        if self.tts_service:
           self.tts_service.speak(response)

    def usb_power_off(self,usbPortIdentifier):
        results=self.usb_load_devices(self.usb_get_devices())
        device=self.find_device(usbPortIdentifier,results)
        response=''
        if device is not None:
            if device['power']:
                if 'device' in device.keys() or 'deviceId' in device.keys():
                    response="Turning off power to {}".format(usbPortIdentifier)
                else:
                    response="Turning off power to empty usb port {}".format(usbPortIdentifier)
            else:
                response="{} is already turned off".format(usbPortIdentifier)
        else:
            response="Could not find a usb port matching {}".format(usbPortIdentifier)
        return response;

    def usb_power_off_say(self,usbPortIdentifier):
        response = self.usb_power_off(self,usbPortIdentifier)
        if self.tts_service:
           self.tts_service.speak(response)
