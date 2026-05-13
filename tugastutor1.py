import pytest
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture()
def driver():
    options = webdriver.ChromeOptions()
    # MANDATORY FOR LINUX/CLOUD WORKSPACES:
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-pipe")
    options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    yield driver
    driver.quit()

def test_positive_register(driver):
    driver.get("https://parabank.parasoft.com/parabank/register.htm")
    wait = WebDriverWait(driver, 20)

    unique_user = f"user_{random.randint(1000, 999999)}"

    wait.until(EC.presence_of_element_located((By.ID, "customer.firstName"))).send_keys("Yusuf")
    driver.find_element(By.ID, "customer.lastName").send_keys("Tester")
    driver.find_element(By.ID, "customer.address.street").send_keys("Jl. Kelompok")
    driver.find_element(By.ID, "customer.address.city").send_keys("Tangerang")
    driver.find_element(By.ID, "customer.address.state").send_keys("Banten")
    driver.find_element(By.ID, "customer.address.zipCode").send_keys("15000")
    driver.find_element(By.ID, "customer.phoneNumber").send_keys("0812345678")
    driver.find_element(By.ID, "customer.ssn").send_keys("123-456")
    
    driver.find_element(By.ID, "customer.username").send_keys(unique_user)
    driver.find_element(By.ID, "customer.password").send_keys("Pass123!")
    driver.find_element(By.ID, "repeatedPassword").send_keys("Pass123!")
    driver.find_element(By.XPATH, "//input[@value='Register']").click()

    wait.until(EC.presence_of_element_located((By.ID, "rightPanel")))
    driver.save_screenshot("success_register.png")
    
    success_text = driver.find_element(By.ID, "rightPanel").text
    assert "Your account was created successfully" in success_text

def test_negative_empty_username(driver):
    driver.get("https://parabank.parasoft.com/parabank/register.htm")
    wait = WebDriverWait(driver, 15)

    wait.until(EC.presence_of_element_located((By.ID, "customer.firstName"))).send_keys("Yusuf")
    driver.find_element(By.XPATH, "//input[@value='Register']").click()

    wait.until(EC.presence_of_element_located((By.ID, "customer.username.errors")))
    driver.save_screenshot("error_empty_username.png")

    error_message = driver.find_element(By.ID, "customer.username.errors").text
    assert "Username is required." in error_message

def test_negative_password_mismatch(driver):
    driver.get("https://parabank.parasoft.com/parabank/register.htm")
    wait = WebDriverWait(driver, 15)

    wait.until(EC.presence_of_element_located((By.ID, "customer.username"))).send_keys("tester_kelompok")
    driver.find_element(By.ID, "customer.password").send_keys("Pass123!")
    driver.find_element(By.ID, "repeatedPassword").send_keys("BedaBanget123")
    driver.find_element(By.XPATH, "//input[@value='Register']").click()

    wait.until(EC.presence_of_element_located((By.ID, "repeatedPassword.errors")))
    driver.save_screenshot("error_password_mismatch.png")

    error_message = driver.find_element(By.ID, "repeatedPassword.errors").text
    assert "Passwords did not match." in error_message

