import pytest, os
from selenium import webdriver
import config


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
    # chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option(name="detach", value=True)
    return chrome_options


@pytest.fixture(scope="session")
def chr_driver(request, chr_options):
    driver = webdriver.Chrome(
            executable_path="D:\Repositories\TimeClockAutomation\src\exe\chromedriver.exe",
            options=chr_options, desired_capabilities={"loggingPrefs": {'browser': 'ALL'}})
    yield driver
    #driver.quit()