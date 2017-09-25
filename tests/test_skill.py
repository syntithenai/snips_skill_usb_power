from unittest import TestCase

from usbpowerskill.usbpowerskill import UsbPowerSkill
import time

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
        self.sampleListOutput="""Device I D 0424:ec00 on u s b port 1
Nothing plugged into u s b port 2
Usb port 3 is switched off
OmniVision Technologies, Inc. USB Camera-B4.09.24.1 on u s b port 4
Logitech USB Receiver on u s b port 5"""


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
       pass #self.assertEqual(self.skill.usb_list_devices(self.skill.usb_load_devices(self.sampleDevices)),self.sampleListOutput)

    def test_find_device(self):
        result = self.skill.usb_find_device("Camera",self.skill.usb_load_devices(self.sampleDevices));
        # by device name
        self.assertTrue(result is not None)
        self.assertTrue('id' in result.keys())
        self.assertTrue(result['id'] == '4')
        # by deviceId
        result = self.skill.usb_find_device("046d:c52b",self.skill.usb_load_devices(self.sampleDevices))
        self.assertTrue(result is not None and 'id' in result.keys() and result['id'] == '5')
        # fail
        result = self.skill.usb_find_device("046d:NOFINDMEc52b",self.skill.usb_load_devices(self.sampleDevices))
        self.assertIsNone(result)
        # by id
        result = self.skill.usb_find_device("4",self.skill.usb_load_devices(self.sampleDevices))
        self.assertTrue(result is not None and 'id' in result.keys() and result['id'] == '4')
        
    def test_power_on_off(self):
        results =  self.skill.usb_load_devices(self.sampleDevices)
        # by name off
        result,action = self.skill.usb_power_off('Camera',results)
        self.assertEqual(result,'Turning off power to Camera')
        
        # by id off already off
        result,action = self.skill.usb_power_off('3',results)
        self.assertEqual(result,'3 is already turned off')
        
        # by id off 
        result,action = self.skill.usb_power_off('2',results)
        self.assertEqual(result,'Turning off power to empty u s b port 2')
        
        # fail find
        result,action = self.skill.usb_power_on('NOFIND',results)
        self.assertIsNone(action)
        self.assertEqual(result,'Could not find a u s b port matching NOFIND')
        result,action = self.skill.usb_power_off('NOFIND',results)
        self.assertIsNone(action)
        self.assertEqual(result,'Could not find a u s b port matching NOFIND')
        
        # by id on
        result,action = self.skill.usb_power_on('3',results)
        self.assertEqual(result,'Turning on power to empty u s b port 3')
        
        # by id on already on
        result,action = self.skill.usb_power_on('2',results)
        self.assertEqual(result,'2 is already turned on')
        
        #self.assertEqual(self.skill.usb_power_on('Camera',results),'Turning on power to Camera')
        #self.assertEqual(self.skill.usb_power_on('Camera',results),'Camera is already turned on')
        #self.assertEqual(self.skill.usb_power_on('2',results),'Turning on power to empty usb port 2')
        #self.assertEqual(self.skill.usb_power_off('2',results),'Turning off power to empty usb port 2')
        #self.assertEqual(self.skill.usb_power_off('2',results),'2 is already turned off')
        
