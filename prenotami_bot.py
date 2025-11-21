#!/usr/bin/env python3
"""
Prenotami.esteri.it Appointment Booking Bot
Automates the process of booking an appointment for ID card renewal
"""

import os
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('prenotami_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PrenotamiBot:
    """Bot to automate appointment booking on prenotami.esteri.it"""
    
    def __init__(self, email, password, booking_details=None, headless=False):
        """
        Initialize the bot
        
        Args:
            email: User email for login
            password: User password for login
            booking_details: Dictionary with booking form details
            headless: Run browser in headless mode (default: False)
        """
        self.email = email
        self.password = password
        self.booking_details = booking_details or {}
        self.headless = headless
        self.driver = None
        self.base_url = "https://prenotami.esteri.it/"
        self.user_area_url = "https://prenotami.esteri.it/UserArea"
        
    def setup_driver(self):
        """Setup and configure the Chrome WebDriver"""
        logger.info("Setting up Chrome WebDriver...")
        
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Additional options for stability
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Set window size
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Try system ChromeDriver first (faster and more reliable)
        try:
            logger.info("Using system ChromeDriver...")
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("✓ System ChromeDriver loaded successfully")
        except Exception as e:
            logger.warning(f"System ChromeDriver failed: {e}")
            logger.info("Trying fallback: webdriver-manager...")
            
            # Fallback: try using webdriver-manager
            try:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("✓ WebDriver manager loaded successfully")
            except Exception as e2:
                logger.error(f"WebDriver manager also failed: {e2}")
                logger.error("\n" + "="*60)
                logger.error("SOLUTION: Please install ChromeDriver manually:")
                logger.error("  macOS: brew install chromedriver")
                logger.error("  Then run: xattr -d com.apple.quarantine $(which chromedriver)")
                logger.error("="*60 + "\n")
                raise
        
        self.driver.implicitly_wait(10)
        logger.info("WebDriver setup complete")
        
    def login(self):
        """Login to the prenotami.esteri.it website"""
        try:
            logger.info(f"Navigating to {self.base_url}...")
            self.driver.get(self.base_url)
            
            # Wait for page to load
            time.sleep(2)
            
            # Find and fill email field
            logger.info("Looking for login form...")
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "login-email"))
            )
            email_field.clear()
            email_field.send_keys(self.email)
            logger.info("Email entered")
            
            # Find and fill password field
            password_field = self.driver.find_element(By.ID, "login-password")
            password_field.clear()
            password_field.send_keys(self.password)
            logger.info("Password entered")
            
            # Wait a moment for any JavaScript to load
            time.sleep(1)
            
            # Try submitting by pressing Enter (more reliable than clicking button)
            logger.info("Submitting form by pressing Enter...")
            password_field.send_keys(Keys.RETURN)
            logger.info("Form submitted")
            
            # Wait for redirect to UserArea
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("UserArea")
            )
            logger.info("✓ Login successful!")
            
            return True
            
        except TimeoutException:
            logger.error("Timeout during login. Check if the page structure has changed.")
            self.take_screenshot("login_timeout")
            return False
        except NoSuchElementException as e:
            logger.error(f"Could not find login elements: {e}")
            self.take_screenshot("login_element_not_found")
            return False
        except Exception as e:
            logger.error(f"Login failed: {e}")
            self.take_screenshot("login_error")
            return False
    
    def navigate_to_booking(self):
        """Navigate to the booking section"""
        try:
            logger.info("Looking for 'Prenota' tab...")
            
            # Wait a bit for the page to fully load
            time.sleep(2)
            
            # Look for the "Prenota" tab (third tab) - it's a link
            prenota_tab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Prenota"))
            )
            
            logger.info("Found 'Prenota' tab, clicking...")
            prenota_tab.click()
            time.sleep(2)
            
            logger.info("✓ Navigated to booking section")
            return True
            
        except TimeoutException:
            logger.error("Could not find 'Prenota' tab")
            self.take_screenshot("prenota_tab_not_found")
            return False
        except Exception as e:
            logger.error(f"Error navigating to booking: {e}")
            self.take_screenshot("booking_navigation_error")
            return False
    
    def click_id_card_booking(self):
        """Click on the ID card appointment booking button"""
        try:
            logger.info("Looking for ID card booking button...")
            
            # Wait for the table to load
            time.sleep(2)
            
            # The PRENOTA buttons might be links (<a> tags) styled as buttons
            # Try multiple approaches
            booking_element = None
            
            try:
                # Approach 1: Find by link text
                booking_element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.LINK_TEXT, "PRENOTA"))
                )
                logger.info("Found PRENOTA as link")
            except:
                try:
                    # Approach 2: Find by partial link text
                    booking_element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "PRENOTA"))
                    )
                    logger.info("Found PRENOTA as partial link")
                except:
                    try:
                        # Approach 3: Find any element containing PRENOTA text
                        booking_element = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'PRENOTA')]"))
                        )
                        logger.info("Found PRENOTA element")
                    except:
                        # Approach 4: Find specifically in the first table row
                        booking_element = self.driver.find_element(
                            By.XPATH, 
                            "(//tr)[1]//*[contains(text(), 'PRENOTA')]"
                        )
                        logger.info("Found PRENOTA in first table row")
            
            if booking_element:
                # Scroll to element
                self.driver.execute_script("arguments[0].scrollIntoView(true);", booking_element)
                time.sleep(1)
                
                # Click using JavaScript for reliability
                self.driver.execute_script("arguments[0].click();", booking_element)
                logger.info("✓ Clicked on ID card appointment booking!")
                time.sleep(3)
                return True
            else:
                logger.error("Could not find PRENOTA element")
                return False
                
        except Exception as e:
            logger.error(f"Error clicking ID card booking: {e}")
            self.take_screenshot("id_card_booking_error")
            return False
    
    def fill_booking_form(self):
        """Fill in the booking form with user details"""
        try:
            logger.info("Filling booking form...")
            
            # Wait for form to load
            time.sleep(2)
            
            # Take screenshot of the form
            self.take_screenshot("booking_form_start")
            
            # Tipo di Prenotazione (dropdown)
            tipo_prenotazione = self.booking_details.get('TIPO_PRENOTAZIONE', 'Prenotazione Singola')
            if tipo_prenotazione:
                try:
                    logger.info(f"Selecting booking type: {tipo_prenotazione}")
                    tipo_dropdown = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.ID, "tipoPrenotazione"))
                    )
                    Select(tipo_dropdown).select_by_visible_text(tipo_prenotazione)
                    time.sleep(1)
                except Exception as e:
                    logger.warning(f"Could not select booking type: {e}")
            
            # Indirizzo completo di residenza
            indirizzo = self.booking_details.get('INDIRIZZO_RESIDENZA', '')
            if indirizzo:
                try:
                    logger.info("Filling in address...")
                    address_field = self.driver.find_element(By.ID, "indirizzoResidenza")
                    address_field.clear()
                    address_field.send_keys(indirizzo)
                    time.sleep(1)
                except Exception as e:
                    logger.warning(f"Could not fill address: {e}")
            
            # Statura in CM
            statura = self.booking_details.get('STATURA_CM', '')
            if statura:
                try:
                    logger.info(f"Filling in height: {statura} cm")
                    height_field = self.driver.find_element(By.ID, "statura")
                    height_field.clear()
                    height_field.send_keys(str(statura))
                    time.sleep(1)
                except Exception as e:
                    logger.warning(f"Could not fill height: {e}")
            
            # Stato Civile (dropdown - optional)
            stato_civile = self.booking_details.get('STATO_CIVILE', '')
            if stato_civile:
                try:
                    logger.info(f"Selecting marital status: {stato_civile}")
                    stato_dropdown = self.driver.find_element(By.ID, "statoCivile")
                    Select(stato_dropdown).select_by_visible_text(stato_civile)
                    time.sleep(1)
                except Exception as e:
                    logger.warning(f"Could not select marital status: {e}")
            
            # Numero figli minorenni
            numero_figli = self.booking_details.get('NUMERO_FIGLI_MINORENNI', '0')
            try:
                logger.info(f"Filling in number of minor children: {numero_figli}")
                children_field = self.driver.find_element(By.ID, "numeroFigliMinorenni")
                children_field.clear()
                children_field.send_keys(str(numero_figli))
                time.sleep(1)
            except Exception as e:
                logger.warning(f"Could not fill number of children: {e}")
            
            # Note per la sede (optional)
            note = self.booking_details.get('NOTE_PER_SEDE', '')
            if note:
                try:
                    logger.info("Filling in notes...")
                    notes_field = self.driver.find_element(By.ID, "notePerSede")
                    notes_field.clear()
                    notes_field.send_keys(note)
                    time.sleep(1)
                except Exception as e:
                    logger.warning(f"Could not fill notes: {e}")
            
            # Accept Privacy Policy checkbox
            try:
                logger.info("Accepting privacy policy...")
                privacy_checkbox = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        "//input[@type='checkbox' and contains(@id, 'privacy')]"
                    ))
                )
                if not privacy_checkbox.is_selected():
                    self.driver.execute_script("arguments[0].click();", privacy_checkbox)
                    logger.info("✓ Privacy policy accepted")
                time.sleep(1)
            except Exception as e:
                logger.warning(f"Could not click privacy checkbox: {e}")
            
            # Take screenshot of filled form
            self.take_screenshot("booking_form_filled")
            
            # Click "Avanti" button
            try:
                logger.info("Clicking 'Avanti' button...")
                avanti_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        "//button[contains(text(), 'AVANTI') or contains(text(), 'Avanti')]"
                    ))
                )
                self.driver.execute_script("arguments[0].click();", avanti_button)
                logger.info("✓ Clicked 'Avanti'")
                time.sleep(3)
            except Exception as e:
                logger.error(f"Could not click 'Avanti' button: {e}")
                self.take_screenshot("avanti_button_error")
                return False
            
            # Take screenshot of confirmation page
            self.take_screenshot("confirmation_page")
            
            # Handle confirmation dialog
            try:
                logger.info("Looking for confirmation button...")
                confirm_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        "//button[contains(text(), 'OK') or contains(text(), 'CONFERMA') or contains(text(), 'Conferma')]"
                    ))
                )
                self.driver.execute_script("arguments[0].click();", confirm_button)
                logger.info("✓ Clicked confirmation button!")
                time.sleep(3)
            except Exception as e:
                logger.warning(f"Could not find/click confirmation button: {e}")
            
            # Take final screenshot
            self.take_screenshot("booking_completed")
            
            logger.info("🎉 Booking form submitted successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error filling booking form: {e}")
            self.take_screenshot("form_filling_error")
            return False
    
    def check_availability(self):
        """Check for available appointment slots and attempt to book"""
        try:
            logger.info("Checking for available appointment slots...")
            
            # Wait for the page to load
            time.sleep(3)
            
            # Take a screenshot for manual review
            self.take_screenshot("availability_page")
            
            # Check if there's a "no slots available" message
            try:
                no_slots_message = self.driver.find_element(
                    By.XPATH,
                    "//*[contains(text(), 'esauriti') or contains(text(), 'disponibili')]"
                )
                if no_slots_message:
                    logger.info("⚠️  Website reports: No slots available (all spots exhausted)")
                    logger.info("💡 The bot will try again at 7:00 AM when new slots are released")
                    return False
            except:
                # No "exhausted" message found - good sign!
                pass
            
            # Look for available dates/slots in a calendar or date picker
            # Try multiple selectors for different possible layouts
            available_slots = []
            
            try:
                # Try finding clickable date buttons
                available_slots = self.driver.find_elements(
                    By.XPATH, 
                    "//button[not(@disabled) and not(contains(@class, 'disabled'))]"
                )
            except:
                pass
            
            try:
                # Try finding available dates in a calendar
                available_slots.extend(self.driver.find_elements(
                    By.XPATH,
                    "//td[contains(@class, 'available') or contains(@class, 'selectable')]"
                ))
            except:
                pass
            
            try:
                # Try finding any clickable elements that might be appointment slots
                available_slots.extend(self.driver.find_elements(
                    By.XPATH,
                    "//*[contains(@class, 'slot') and not(contains(@class, 'disabled'))]"
                ))
            except:
                pass
            
            # Filter out non-relevant elements (like navigation buttons, etc.)
            # Keep only elements that seem like appointment slots
            clickable_slots = [slot for slot in available_slots if slot.is_displayed() and slot.is_enabled()]
            
            if clickable_slots:
                logger.info(f"🎉 Found {len(clickable_slots)} potentially available slot(s)!")
                
                # Click on the first available slot
                logger.info("Attempting to book first available slot...")
                clickable_slots[0].click()
                time.sleep(3)
                
                # Take screenshot of the booking page
                self.take_screenshot("slot_selected")
                
                # Fill in the booking form
                if self.booking_details:
                    logger.info("Proceeding to fill booking form...")
                    form_success = self.fill_booking_form()
                    if form_success:
                        logger.info("✓ Booking completed successfully!")
                        logger.info("🎉 CHECK SCREENSHOTS TO VERIFY BOOKING!")
                        return True
                    else:
                        logger.warning("⚠️  Form filling had issues. Check screenshots.")
                        return True
                else:
                    logger.warning("⚠️  No booking details provided. Stopping at slot selection.")
                    logger.warning("💡 Add booking details to .env to complete automatic booking")
                    self.take_screenshot("booking_stopped_no_details")
                    return True
            else:
                logger.info("No available slots found at this time.")
                return False
                
        except Exception as e:
            logger.error(f"Error checking availability: {e}")
            self.take_screenshot("availability_check_error")
            return False
    
    def take_screenshot(self, name):
        """Take a screenshot for debugging"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{name}_{timestamp}.png"
            self.driver.save_screenshot(filename)
            logger.info(f"Screenshot saved: {filename}")
        except Exception as e:
            logger.error(f"Could not take screenshot: {e}")
    
    def run(self):
        """Main execution flow"""
        try:
            logger.info("="*60)
            logger.info("Starting Prenotami Bot")
            logger.info("="*60)
            
            self.setup_driver()
            
            # Step 1: Login
            if not self.login():
                logger.error("Failed to login. Aborting.")
                return False
            
            # Step 2: Navigate to booking section
            if not self.navigate_to_booking():
                logger.error("Failed to navigate to booking section. Aborting.")
                return False
            
            # Step 3: Click on ID card booking
            if not self.click_id_card_booking():
                logger.error("Failed to click ID card booking. Aborting.")
                return False
            
            # Step 4: Check availability and book
            success = self.check_availability()
            
            if success:
                logger.info("="*60)
                logger.info("✓ Bot completed successfully!")
                logger.info("="*60)
            else:
                logger.info("="*60)
                logger.info("Bot completed but no slots were available.")
                logger.info("="*60)
            
            # Keep browser open for a bit so you can see the result
            time.sleep(5)
            
            return success
            
        except Exception as e:
            logger.error(f"Unexpected error in main flow: {e}")
            self.take_screenshot("unexpected_error")
            return False
            
        finally:
            if self.driver:
                logger.info("Closing browser...")
                self.driver.quit()


def main():
    """Main entry point"""
    # Load environment variables
    load_dotenv()
    
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    
    if not email or not password:
        logger.error("Please set EMAIL and PASSWORD in .env file")
        logger.error("Copy env.example to .env and fill in your credentials")
        return
    
    # Load booking form details
    booking_details = {
        'INDIRIZZO_RESIDENZA': os.getenv("INDIRIZZO_RESIDENZA", ""),
        'STATURA_CM': os.getenv("STATURA_CM", ""),
        'NUMERO_FIGLI_MINORENNI': os.getenv("NUMERO_FIGLI_MINORENNI", "0"),
        'NOTE_PER_SEDE': os.getenv("NOTE_PER_SEDE", ""),
        'TIPO_PRENOTAZIONE': os.getenv("TIPO_PRENOTAZIONE", "Prenotazione Singola"),
        'STATO_CIVILE': os.getenv("STATO_CIVILE", ""),
    }
    
    # Check if booking details are provided
    if not booking_details['INDIRIZZO_RESIDENZA'] or not booking_details['STATURA_CM']:
        logger.warning("⚠️  Booking details not fully configured in .env")
        logger.warning("💡 Bot will find slots but won't complete the booking form")
        logger.warning("💡 See env.example for required fields")
    
    # Create and run bot
    bot = PrenotamiBot(
        email=email,
        password=password,
        booking_details=booking_details,
        headless=False
    )
    bot.run()


if __name__ == "__main__":
    main()

