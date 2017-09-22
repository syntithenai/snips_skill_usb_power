from unittest import TestCase

from usbpowerskill.usbpowerskill import UsbPowerSkill


class BaseTest(TestCase):

    def setUp(self):
        self.skill = UsbPowerSkill()
        self.sampleDevices="""
   Port 1: 0503 highspeed power enable connect [0424:ec00]
   Port 2: 0100 power
   Port 3: 0000 off
   Port 4: 0503 highspeed power enable connect [1415:2000 OmniVision Technologies, Inc. USB Camera-B4.09.24.1]
   Port 5: 0103 power enable connect [046d:c52b Logitech USB Receiver]
"""
        self.sampleListOutput="""Device ID 0424:ec00 on usb port 1
Nothing plugged into usb port 2
Usb port 3 is switched off
OmniVision Technologies, Inc. USB Camera-B4.09.24.1 on usb port 4
Logitech USB Receiver on usb port 5"""


class UsbPowerSkillTest(BaseTest):
    def test_get_devices(self):
        text = self.skill.usb_get_devices()
        self.assertTrue(len(text.splitlines()) > 1 ) # at least two usb ports listed
        
    def test_sample(self):
        results =  self.skill.usb_load_devices(self.sampleDevices)
        self.assertEqual(results[0]['deviceId'],"0424:ec00")
        self.assertEqual(results[0]['power'],True)
        self.assertEqual(results[2]['power'],False)
        self.assertEqual(results[0]['id'],'1')
        self.assertEqual(results[3]['device'],'OmniVision Technologies, Inc. USB Camera-B4.09.24.1')

    def test_list_devices(self):
        pass
        #self.assertEqual(self.skill.usb_list_devices(self.skill.usb_load_devices(self.sampleDevices)),self.sampleListOutput)

    def test_find_device(self):
        result = self.skill.usb_find_device("Camera",self.skill.usb_load_devices(self.sampleDevices));
        print(result);
        self.assertTrue(result is not None and 'id' in result.keys() and result['id'] == '4')
        result2 = self.skill.usb_find_device("046d:c52b",self.skill.usb_load_devices(self.sampleDevices));
        print(result2);
        self.assertTrue(result is not None and 'id' in result.keys() and result['id'] == '5')
        
            
