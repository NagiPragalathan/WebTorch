from .Tools import SetupTools
from .Stack_data import get_stack
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import Select
import pyautogui
import cv2
import os
import sys
import pytest
import numpy as np
import traceback
import threading
import pytest
run = True


def getpath(nested_dict: dict, value: any, prepath=()):
    """
    Recursively search for a value in a nested dictionary and return its path.

    Args:
        nested_dict (dict): The nested dictionary to search.
        value (any): The value to search for.
        prepath (tuple, optional): Used for recursion to keep track of the path. Defaults to ().

    Returns:
        tuple: The path to the value in the dictionary, or None if not found.
    """
    for k, v in nested_dict.items():
        path = prepath + (k,)
        if v == value:
            return path
        elif isinstance(v, dict):
            p = getpath(v, value, path)
            if p is not None:
                return p


def take_video_rec():
    """
    Capture screen recording and save it to a video file.

    This function captures the screen and writes the frames to a video file.
    The recording can be stopped by pressing 'q'.

    Returns:
        None
    """
    resolution = (1920, 1080)
    codec = cv2.VideoWriter_fourcc(*"XVID")
    filename = "Test_Video/Recording.avi"  # Video file path
    fps = 30.0
    out = cv2.VideoWriter(filename, codec, fps, resolution)
    while run:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)
        if cv2.waitKey(1) == ord('q'):
            break
    out.release()
    cv2.destroyAllWindows()


def action(element: webdriver.remote.webelement.WebElement, action: str):
    """
    Perform an action on a WebElement.

    Args:
        element (webdriver.remote.webelement.WebElement): The WebElement to perform the action on.
        action (str): The action to perform (e.g., 'click').

    Returns:
        None
    """
    if action == 'click':
        element.click()

Auto_install = True

@pytest.mark.others
def Make_test(path: str):
    """
    Create and execute tests based on a JSON configuration.

    This function reads a JSON configuration file, creates the required folders,
    and executes a series of test steps using Selenium WebDriver.

    Args:
        path (str): The path to the JSON configuration file.

    Returns:
        None
    """
    global Auto_install
    # Create required folders
    folders = ['Test_Video', 'ScreenShots']
    driver=""
    Steps_of_testing = []
    try:
        for i in folders:
            current_path = os.path.join(os.getcwd().join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-1]), i)
            os.mkdir(current_path)
    except FileExistsError:
        print('Files already exist')

    global run
    get_ids = ['id', 'name', 'class', 'xpath']
    list_data = ['ls_id_clk', 'ls_name_clk', 'ls_xpath_clk']

    orginal = get_stack(path)
    stack = get_stack(path)[1:]
    try:
        if orginal[0].get("auto_install") == "true":
            driver = SetupTools.install_selenium_tool(orginal[0].get("browser"))
            Steps_of_testing.append("Driver was automatically installed")
        else:
            driver_path = orginal[0].get('driver_path')
            driver = webdriver.Chrome(driver_path)
            driver.get(orginal[0].get('get'))
            if orginal[0].get('window') == 'maximize':
                driver.maximize_window()

    except:
        if Auto_install:
            driver = webdriver.Chrome(ChromeDriverManager(version="91.0.4472.101").install())
            Auto_install = False
        driver.get(orginal[0].get('get'))
        if orginal[0].get('window') == 'maximize':
            driver.maximize_window()

    if orginal[0].get('screen_recorder') == 'true':
        t1 = threading.Thread(target=take_video_rec)
        t1.start()

    for i in stack:
        time.sleep(1)
        for j in i.keys():
            try:
                if j in list_data:
                    if j == 'ls_id_clk':
                        # List of element IDs to click
                        for k in i.get(j):
                            Element = driver.find_element(By.ID, k)
                            action(Element, 'click')

                    elif j == 'ls_name_clk':
                        # List of element names to click
                        for k in i.get(j):
                            Element = driver.find_element(By.NAME, k)
                            action(Element, 'click')

                    elif j == 'ls_xpath_clk':
                        # List of XPath expressions to click
                        for k in i.get(j):
                            Element = driver.find_element(By.XPATH, k)
                            action(Element, 'click')

                if j in get_ids:
                    if ':' in i.get(j):
                        values = i.get(j).split(':')
                        at_splited = values[1].split('@')
                        element_id = values[0]
                        print(element_id)
                        # Find the element
                        Element = driver.find_element(getattr(By, j.upper()), element_id)

                        # Check if it's a dropdown (select) element
                        if Element.tag_name == 'select':
                            select = Select(Element)  # Create a Select object

                            for k in range(1, len(values)):
                                if at_splited[0] == 'select_by_index':
                                    if 'data' in i.keys():
                                        select.select_by_index(int(i.get('data')))
                                    else:
                                        select.select_by_index(int(at_splited[1]))
                                elif at_splited[0] == 'select_by_value':
                                    if 'data' in i.keys():
                                        select.select_by_value(i.get('data'))
                                    else:
                                        select.select_by_value(at_splited[1])
                                elif at_splited[0] == 'select_by_visible_text':
                                    if 'data' in i.keys():
                                        select.select_by_visible_text(i.get('data'))
                                    else:
                                        select.select_by_visible_text(at_splited[1])

                        # Deselect Dropdown Methods
                        elif at_splited[0] == 'deselect_all':
                            if Element.tag_name == 'select':
                                select.deselect_all()
                        elif at_splited[0] == 'deselect_by_index':
                            if Element.tag_name == 'select':
                                if 'data' in i.keys():
                                    select.deselect_by_index(int(i.get('data')))
                                else:
                                    select.deselect_by_index(int(at_splited[1]))
                        elif at_splited[0] == 'deselect_by_value':
                            if Element.tag_name == 'select':
                                if 'data' in i.keys():
                                    select.deselect_by_value(i.get('data'))
                                else:
                                    select.deselect_by_value(at_splited[1])
                        elif at_splited[0] == 'deselect_by_visible_text':
                            if Element.tag_name == 'select':
                                if 'data' in i.keys():
                                    select.deselect_by_visible_text(i.get('data'))
                                else:
                                    select.deselect_by_visible_text(at_splited[1])

                        # Input Field Methods
                        for k in range(1, len(values)):
                            # Input box types...
                            if values[k] == 'sk':
                                if 'data' in i.keys():
                                    Element.send_keys(i.get('data'))
                            elif values[k] == 'c&sk':
                                if 'data' in i.keys():
                                    Element.clear()
                                    Element.send_keys(i.get('data'))
                            elif values[k] == 'click':
                                action(Element, 'click')

                        # Window Operating Methods
                        for k in range(1, len(values)):
                            if values[k] == 'maximize' or i.get('window') == 'maximize':
                                driver.maximize_window()
                            elif values[k] == 'minimize' or i.get('window') == 'minimize':
                                driver.minimize_window()

                        if isinstance(i.get('set_window_position'), list):
                            pos = i.get('set_window_position')
                            driver.set_window_position(pos[0], pos[1])

                        # Execute Python Code or Script
                        if i.get('python_code') is not None or i.get('python_script') is not None:
                            execute = i.get('python_code')
                            exec(execute, {'driver': driver})

                        if i.get('python_code_path') is not None or i.get('python_script_path') is not None:
                            if i.get('python_code_path') is not None:
                                if '@' in i.get('python_code_path'):
                                    execute = open(i.get('python_code_path').split('@')[0], 'r').read()
                                    for j in range(1, len(i.get('python_code_path').split('@'))):
                                        execute = str(execute) + "\n" + i.get('python_code_path').split('@')[j]
                                else:
                                    execute = open(i.get('python_code_path'), 'r')
                            elif i.get('python_script_path') is not None:
                                if '@' in i.get('python_code_path'):
                                    execute = open(i.get('python_code_path').split('@')[0], 'r').read()
                                    for j in range(1, len(i.get('python_code_path').split('@'))):
                                        execute = str(execute) + "\n" + i.get('python_code_path').split('@')[j]
                                else:
                                    execute = open(i.get('python_code_path'), 'r')
                            exec(execute, {'driver': driver})

                        if i.get('take') == "screenshot":
                            driver.save_screenshot('ScreenShots/pic.png')

            except BaseException as e:
                if sys.argv[0] == 'Debug=true':
                    print("".join(traceback.format_exception_only(e)).strip())

    run = False
    if orginal[0].get('run_and_wait') == 'true':
        input("\n\n\nPress 'ctrl' + 'c' to close the server")
