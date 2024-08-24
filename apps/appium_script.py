from appium import webdriver
import time
import os
from appium import webdriver
import subprocess
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

def run_appium_test(apk_path, result_path):

    capabilities = dict(
        platformName='Android',
        automationName='uiautomator2',
        deviceName='Android',
        app=apk_path,
        language='en',
        locale='US'
    )

    appium_server_url = 'http://localhost:4723'

    driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    try:
        # Wait for the app to load
        driver.implicitly_wait(10)

        # Ensure the result directory exists
        if not os.path.exists(result_path):
            os.makedirs(result_path)

        # Capture the initial UI hierarchy
        initial_ui_hierarchy = driver.page_source

        # Construct paths for screenshots and video
        initial_screenshot_path = os.path.join(result_path, 'initial_screenshot.png')
        subsequent_screenshot_path = os.path.join(result_path, 'subsequent_screenshot.png')
        video_path = os.path.join(result_path, 'test_video.mp4')

        # Start video recording
        start_video_recording()

        # Wait for the app to load
        driver.implicitly_wait(10)

        # Capture the initial UI hierarchy
        initial_ui_hierarchy = driver.page_source

        # Capture the initial screenshot
        driver.save_screenshot(initial_screenshot_path)

        # List of potential button identifiers to search for
        button_identifiers = [
            (AppiumBy.CLASS_NAME, 'android.widget.Button'),
            (AppiumBy.CLASS_NAME, 'android.widget.ImageButton'),
        ]

        # Variable to store the first button found
        first_button = None

        # Iterate through the list of button identifiers and find the first one
        for by, identifier in button_identifiers:
            try:
                first_button = driver.find_element(by, identifier)
                if first_button:
                    break  # Exit the loop if a button is found
            except NoSuchElementException:
                continue  # Try the next identifier if no element is found

        if first_button:
            # Simulate a click on the first button found
            first_button.click()

            # Wait for possible screen change
            time.sleep(3)

            # Capture the UI hierarchy and screenshot after the click
            subsequent_ui_hierarchy = driver.page_source
            
            driver.save_screenshot(subsequent_screenshot_path)

            # Determine if the screen has changed
            screen_changed = initial_ui_hierarchy != subsequent_ui_hierarchy
        else:
            print("No button found on the screen.")
            subsequent_ui_hierarchy = initial_ui_hierarchy
            subsequent_screenshot_path = initial_screenshot_path
            screen_changed = False

    finally:
        # Stop video recording
        stop_video_recording(video_path)

        # Quit the driver
        driver.quit()

        # Close the emulator
        close_emulator()

    return {
        'initial_screenshot': initial_screenshot_path,
        'subsequent_screenshot': subsequent_screenshot_path,
        'video_recording': video_path,
        'ui_hierarchy': initial_ui_hierarchy,
        'screen_changed': screen_changed
    }

def start_video_recording():
    command = f"adb shell screenrecord /sdcard/test_video.mp4"
    subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Started video recording...")

def stop_video_recording(video_path):
    command = "adb shell pkill -l2 screenrecord"
    subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Stopped video recording...")
    time.sleep(2)  # Give time for the video to save

    # Pull the video file from the emulator/device to the result path
    command = f"adb pull /sdcard/test_video.mp4 {video_path}"
    subprocess.run(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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

    wait_for_emulator()

def wait_for_emulator():
    print("Waiting for emulator to start...")
    
    boot_completed = False
    while not boot_completed:
        try:
            # Check the emulator boot status using adb
            result = subprocess.run(["adb", "shell", "getprop", "sys.boot_completed"],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.stdout.strip() == '1':
                boot_completed = True
            else:
                print("Emulator is still booting...")
                time.sleep(5)  
        except Exception as e:
            print(f"Error checking emulator status: {e}")
            time.sleep(5)


def install_apk_on_emulator(apk_path, emulator_name=None):
    
    # If an emulator name is provided, start the emulator
    if emulator_name:
        start_emulator(emulator_name)

    # Ensure that the APK file exists
    if not os.path.exists(apk_path):
        raise FileNotFoundError(f"APK file not found at {apk_path}")
    
    # Install the APK on the running emulator
    command = ["adb", "install", apk_path]
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error = process.communicate()

    if process.returncode == 0:
        print(f"Successfully installed {apk_path} on the emulator.")
    else:
        print(f"Failed to install {apk_path}. Error: {error.decode('utf-8')}")

def close_emulator():
    # Close the emulator using adb
    command = "adb -s emulator-5554 emu kill"
    subprocess.run(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Emulator closed.")