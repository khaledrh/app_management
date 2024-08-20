from appium import webdriver
import time
import os
import unittest
from appium import webdriver
import subprocess
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

# def run_appium_test(apk_path, result_path):
#     desired_caps = {
#         'platformName': 'Android',
#         'platformVersion': '15.0',
#         'deviceName': 'emulator-5554',
#         'app': apk_path,
#         'automationName': 'UiAutomator2'
#     }

#     print("Desired Capabilities:", desired_caps)
#     driver = webdriver.Remote('http://localhost:4723/', desired_caps)

#     # # Start recording video
#     # driver.start_recording_screen()

#     # # Capture initial screen and UI hierarchy
#     # initial_screen_path = os.path.join(result_path, 'initial_screen.png')
#     # driver.save_screenshot(initial_screen_path)

#     # ui_hierarchy = driver.page_source

#     # # Simulate a click on the first button
#     # first_button = driver.find_element_by_class_name('android.widget.Button')
#     # first_button.click()
#     # time.sleep(2)  # Wait for screen transition

#     # # Capture subsequent screen and UI hierarchy
#     # subsequent_screen_path = os.path.join(result_path, 'subsequent_screen.png')
#     # driver.save_screenshot(subsequent_screen_path)

#     # # Check for screen change
#     # screen_changed = driver.page_source != ui_hierarchy

#     # # Stop recording and save the video
#     # video_path = os.path.join(result_path, 'test_video.mp4')
#     # video_data = driver.stop_recording_screen()
#     # with open(video_path, 'wb') as video_file:
#     #     video_file.write(video_data)

#     # Quit the driver
#     driver.quit()

#     return {
#         'initial_screenshot': 'path/to/initial_screenshot.png',
#         'subsequent_screenshot': 'path/to/subsequent_screenshot.png',
#         'video_recording': 'path/to/video.mp4',
#         'ui_hierarchy': '<xml></xml>',
#         'screen_changed': True
#     }

def start_emulator(emulator_name):
    # Ensure that ANDROID_HOME is set
    android_home = os.environ.get("ANDROID_HOME")
    if not android_home:
        raise EnvironmentError("ANDROID_HOME environment variable is not set.")
    
    # Path to the emulator tool
    emulator_path = os.path.join(android_home, "emulator", "emulator")
    
    # Command to start the emulator
    command = [emulator_path, "-avd", emulator_name]
    
    # Start the emulator
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Starting emulator {emulator_name}...")

def install_apk_on_emulator(apk_path, emulator_name=None):
    # Ensure that the APK file exists
    if not os.path.exists(apk_path):
        raise FileNotFoundError(f"APK file not found at {apk_path}")
    
    # If an emulator name is provided, start the emulator
    if emulator_name:
        start_emulator(emulator_name)
    
    # Install the APK on the running emulator
    command = ["adb", "install", apk_path]
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    if process.returncode == 0:
        print(f"Successfully installed {apk_path} on the emulator.")
    else:
        print(f"Failed to install {apk_path}. Error: {error.decode('utf-8')}")


def appium_test():
    capabilities = dict(
        platformName='Android',
        automationName='uiautomator2',
        deviceName='Android',
        appPackage='com.android.settings',
        appActivity='.Settings',
        language='en',
        locale='US'
    )

    appium_server_url = 'http://localhost:4723'

    class TestAppium(unittest.TestCase):
        
        def setUp(self) -> None:
            self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
            print("hello")

        def tearDown(self) -> None:
            if self.driver:
                print("hello")
                self.driver.quit()

        def test_find_battery(self) -> None:
            el = self.driver.find_element(by=AppiumBy.XPATH, value='//*[@text="Battery"]')
            print("hello")
            el.click()

    suite = unittest.TestLoader().loadTestsFromTestCase(TestAppium)
    unittest.TextTestRunner(verbosity=2).run(suite)

    if __name__ == '__main__':
        unittest.main()