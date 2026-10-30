import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Define browser and OS combinations required by the assignment[cite: 24]
TEST_CONFIGS = [
    {"browser": "chrome", "version": "128.0", "platform": "Windows 10"},
    {"browser": "MicrosoftEdge", "version": "127.0", "platform": "macOS Ventura"},
    {"browser": "firefox", "version": "130.0", "platform": "Windows 11"},
    # Note: Internet Explorer 11 is deprecated/legacy; included here as per prompt specs if supported by grid
    {"browser": "internet explorer", "version": "11.0", "platform": "Windows 10"}
]

def pytest_generate_tests(metafunc):
    if "config" in metafunc.fixturenames:
        metafunc.parametrize("config", TEST_CONFIGS, scope="class")

@pytest.fixture(scope="function")
def driver(config):
    browser_name = config["browser"].lower()
    
    # Configure options based on browser choice
    if "chrome" in browser_name:
        options = ChromeOptions()
        options.browser_version = config["version"]
    elif "edge" in browser_name or "microsoftedge" in browser_name:
        options = EdgeOptions()
        options.browser_version = config["version"]
    elif "firefox" in browser_name:
        options = FirefoxOptions()
        options.browser_version = config["version"]
    else:
        options = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()

    # Set platform and TestMu AI specific cloud capabilities
    lt_options = {
        "platformName": config["platform"],
        "projectName": "Selenium Python 101 Assignment",
        "build": "TestMu AI Certification Build",
        "name": f"Test - {config['browser']} on {config['platform']}",
        "selenium_version": "4.18.0",
        "visual": True,
        "video": True,
        "network": True,
        "console": True,
        "w3c": True
    }
    
    if hasattr(options, "set_capability"):
        options.set_capability("LT:Options", lt_options)
    else:
        options["LT:Options"] = lt_options

    # TestMu AI Remote Grid URL (Replace with your username and access key or env variables)
    USERNAME = "YOUR_TESTMU_USERNAME"
    ACCESS_KEY = "YOUR_TESTMU_ACCESS_KEY"
    GRID_URL = f"https://{USERNAME}:{ACCESS_KEY}@hub.testmuai.com/wd/hub"

    # Initialize Remote WebDriver
    if isinstance(options, dict):
        driver = webdriver.Remote(command_executor=GRID_URL, desired_capabilities=options)
    else:
        driver = webdriver.Remote(command_executor=GRID_URL, options=options)

    # Set timeout requirements (20 seconds duration)[cite: 24]
    driver.set_script_timeout(20)
    driver.implicitly_wait(10)
    driver.maximize_window()

    yield driver

    # Teardown session safely
    driver.quit()