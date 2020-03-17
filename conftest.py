import pytest, os
from selenium import webdriver
import config
from src.general.general import LogBrowserData
from src.general.sql import SQLGeneral

@pytest.fixture(scope="session")
def chr_options(request):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.accept_untrusted_certs = True
    chrome_options.assume_untrusted_cert_issuer = True
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-impl-side-painting")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-seccomp-filter-sandbox")
    chrome_options.add_argument("--disable-breakpad")
    chrome_options.add_argument("--disable-client-side-phishing-detection")
    chrome_options.add_argument("--disable-cast")
    chrome_options.add_argument("--disable-cast-streaming-hw-encoding")
    chrome_options.add_argument("--disable-cloud-import")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-session-crashed-bubble")
    chrome_options.add_argument("--disable-ipv6")
    chrome_options.add_argument("--allow-http-screen-capture")
    chrome_options.add_argument("--start-maximized")
    #chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option(name="detach", value=True)
    #chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "Nexus 5"})
    return chrome_options


@pytest.fixture(scope="module")
def sql_config():
    sql = SQLGeneral()
    sql.change_user_active_status(user_name=config.user1, status=1)
    sql.change_user_active_status(user_name=config.user2, status=1)
    sql.change_store_active_status(status=1)


@pytest.fixture(scope="module")
def chr_driver(chr_options, sql_config):
    driver = webdriver.Chrome(
            executable_path="D:\Repositories\TimeClockAutomation\src\exe\chromedriver.exe",
            options=chr_options, desired_capabilities={"loggingPrefs": {'browser': 'ALL'}})
    yield driver
    #driver.quit()


@pytest.fixture(scope="module")
def log_obj(chr_driver):
    return LogBrowserData(driver=chr_driver)