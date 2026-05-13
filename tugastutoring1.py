import pytest
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

"""
=============================================================================
TUGAS TUTORIAL - KELOMPOK [NAMA KELOMPOK] - [NIM]
=============================================================================

GHERKIN SYNTAX:

Feature: Registrasi Akun Baru di ParaBank

  Scenario: Registrasi Berhasil (Positive Case)
    Given User membuka halaman registrasi ParaBank
    When User mengisi semua data valid dan username unik
    And User menekan tombol 'Register'
    Then User harus melihat pesan 'Your account was created successfully'

  Scenario: Registrasi Gagal karena Username Kosong (Negative Case 1)
    Given User membuka halaman registrasi ParaBank
    When User mengisi data kecuali kolom Username
    And User menekan tombol 'Register'
    Then User harus melihat pesan error 'Username is required.'

  Scenario: Registrasi Gagal karena Password Tidak Cocok (Negative Case 2)
    Given User membuka halaman registrasi ParaBank
    When User mengisi password 'Pass123' dan konfirmasi password 'Pass456'
    And User menekan tombol 'Register'
    Then User harus melihat pesan error 'Passwords did not match.'
=============================================================================
"""

@pytest.fixture()
def driver():
    options = Options()
    # Pengaturan wajib untuk Linux/Cloud Workspace agar tidak error
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # Menggunakan Chromium karena lebih stabil di lingkungan Linux
    service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    driver = webdriver.Chrome(service=service, options=options)
    
    yield driver
    driver.quit()

def test_positive_register(driver):
    wait = WebDriverWait(driver, 20)
    driver.get("https://parabank.parasoft.com/parabank/register.htm")
    
    # Username harus unik setiap kali test dijalankan
    unique_user = f"mhs_{random.randint(1000, 999999)}"

    driver.find_element(By.ID, "customer.firstName").send_keys("Nama")
    driver.find_element(By.ID, "customer.lastName").send_keys("Mahasiswa")
    driver.find_element(By.ID, "customer.address.street").send_keys("Jl. Kampus")
    driver.find_element(By.ID, "customer.address.city").send_keys("Jakarta")
    driver.find_element(By.ID, "customer.address.state").send_keys("DKI")
    driver.find_element(By.ID, "customer.address.zipCode").send_keys("12345")
    driver.find_element(By.ID, "customer.phoneNumber").send_keys("081234567")
    driver.find_element(By.ID, "customer.ssn").send_keys("123-456")
    
    driver.find_element(By.ID, "customer.username").send_keys(unique_user)
    driver.find_element(By.ID, "customer.password").send_keys("Password123!")
    driver.find_element(By.ID, "repeatedPassword").send_keys("Password123!")
    
    driver.find_element(By.XPATH, "//input[@value='Register']").click()

    success_msg = wait.until(EC.presence_of_element_located((By.ID, "rightPanel"))).text
    assert "Your account was created successfully" in success_msg

def test_negative_username_required(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://parabank.parasoft.com/parabank/register.htm")
    
    # Langsung klik register tanpa isi data
    driver.find_element(By.XPATH, "//input[@value='Register']").click()
    
    error_msg = wait.until(EC.presence_of_element_located((By.ID, "customer.username.errors"))).text
    assert "Username is required." in error_msg

def test_negative_password_mismatch(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://parabank.parasoft.com/parabank/register.htm")
    
    driver.find_element(By.ID, "customer.password").send_keys("Password123")
    driver.find_element(By.ID, "repeatedPassword").send_keys("PasswordBeda")
    
    driver.find_element(By.XPATH, "//input[@value='Register']").click()
    
    error_msg = wait.until(EC.presence_of_element_located((By.ID, "repeatedPassword.errors"))).text
    assert "Passwords did not match." in error_msg
  
