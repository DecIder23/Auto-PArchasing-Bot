import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import csv
import os

# Configuration
url = "https://www.lazada.sg/"
profile_path = "C:/Temp/FastProfile"
EMAIL = "fateh1singh1d@gmail.com"
PASSWORD = "asdfghjkl123@"
CSV_FILE = "products.csv"  # CSV file with product URLs

# Chrome options
options = uc.ChromeOptions()
options.add_argument(f"--user-data-dir={profile_path}")
options.add_argument("--disable-extensions")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_argument("--disable-web-security")
options.add_argument("--disable-features=VizDisplayCompositor")

def wait_and_find_element(driver, selectors, timeout=15, clickable=False):
    """
    Enhanced element finder with multiple selector types and better waiting
    """
    print(f"[DEBUG] Searching for element with {len(selectors)} selectors...")
    
    for i, selector in enumerate(selectors):
        try:
            print(f"[DEBUG] Trying selector {i+1}: {selector[:50]}...")
            
            # Try different selector types
            if selector.startswith('//') or selector.startswith('/'):
                by_type = By.XPATH
            elif selector.startswith('#'):
                by_type = By.ID
                selector = selector[1:]  # Remove #
            elif selector.startswith('.'):
                by_type = By.CLASS_NAME
                selector = selector[1:]  # Remove .
            else:
                by_type = By.CSS_SELECTOR
            
            if clickable:
                element = WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((by_type, selector))
                )
            else:
                element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((by_type, selector))
                )
            
            print(f"✅ Found element with selector {i+1}")
            return element
            
        except Exception as e:
            print(f"❌ Selector {i+1} failed: {str(e)[:100]}")
            continue
    
    raise Exception(f"❌ No element found with any of the {len(selectors)} selectors")

def safe_type(element, text, clear_first=True):
    """
    Enhanced typing function with multiple clearing methods
    """
    try:
        # Multiple ways to clear the field
        if clear_first:
            try:
                element.clear()
            except:
                pass
            
            try:
                element.send_keys(Keys.CONTROL + "a")
                element.send_keys(Keys.DELETE)
            except:
                pass
            
            try:
                # JavaScript clear as fallback
                driver.execute_script("arguments[0].value = '';", element)
            except:
                pass
        
        # Type character by character with human-like delays
        for char in text:
            element.send_keys(char)
            time.sleep(0.05 + (hash(char) % 10) * 0.01)  # Random delay 0.05-0.14s
        
        print(f"✅ Successfully typed text into field")
        return True
        
    except Exception as e:
        print(f"❌ Typing failed: {str(e)}")
        return False

def click_element_safely(driver, element):
    """
    Enhanced clicking with multiple methods
    """
    try:
        # Method 1: Regular click
        element.click()
        return True
    except:
        try:
            # Method 2: ActionChains click
            ActionChains(driver).move_to_element(element).click().perform()
            return True
        except:
            try:
                # Method 3: JavaScript click
                driver.execute_script("arguments[0].click();", element)
                return True
            except Exception as e:
                print(f"❌ All click methods failed: {str(e)}")
                return False

try:
    print("[INFO] Launching Chrome...")
    driver = uc.Chrome(options=options)
    driver.get(url)
    print("[INFO] Page loaded, waiting for content...")
    time.sleep(3)  # Give page time to fully load

    # Login button selectors (successful one first)
    login_button_selectors = [
        "//a[contains(@class, 'login') or contains(text(), 'Login') or contains(text(), 'login')]",  # ✅ Working selector
        "//button[contains(text(), 'Login') or contains(text(), 'login')]",
        "//span[contains(text(), 'Login') or contains(text(), 'login')]/..",
        "[data-testid*='login']",
        ".login-button",
        "#login-btn",
        "//div[contains(@class, 'login')]//a",
        "//header//a[contains(@href, 'login')]"
    ]
    
    print("[INFO] Looking for login button...")
    login_button = wait_and_find_element(driver, login_button_selectors, clickable=True)
    
    if click_element_safely(driver, login_button):
        print("✅ Login button clicked successfully")
    else:
        raise Exception("Failed to click login button")

    # Wait for login form to appear
    print("[INFO] Waiting for login form...")
    time.sleep(2)
    
    # Email field selectors (successful one first)
    email_selectors = [
        "input[placeholder*='email' i]",  # ✅ Working selector
        "input[type='email']",
        "input[name*='email']",
        "input[placeholder*='Email']",
        "#email",
        "#username",
        ".email-input",
        
        # XPath selectors (more flexible)
        "//input[@type='email']",
        "//input[contains(@name, 'email')]",
        "//input[contains(@placeholder, 'email')]",
        "//input[contains(@placeholder, 'Email')]",
        "//input[contains(@class, 'email')]",
        
        # Lazada-specific patterns
        "//div[contains(@class, 'login')]//input[1]",
        "//form//input[1]",
        "//*[@id='login-container']//input[1]",
        
        # Your original XPaths
        '//*[@id="login-container"]/div/div/div/div/div[3]/div[1]/div/input',
        '/html/body/div[8]/div/div/div/div/div/div/div/div[2]/div/div[3]/div[1]/div/input',
        '/html/body/div[5]/div/div/div/div/div/div/div/div[2]/div/div[3]/div[1]/div/input'
    ]

    # Password field selectors (successful one first)
    password_selectors = [
        "input[type='password']",  # ✅ Working selector
        "input[name*='password']",
        "input[name*='pass']",
        "input[placeholder*='password' i]",
        "input[placeholder*='Password']",
        "#password",
        ".password-input",
        
        # XPath selectors
        "//input[@type='password']",
        "//input[contains(@name, 'password')]",
        "//input[contains(@name, 'pass')]",
        "//input[contains(@placeholder, 'password')]",
        "//input[contains(@placeholder, 'Password')]",
        "//input[contains(@class, 'password')]",
        
        # Lazada-specific patterns
        "//div[contains(@class, 'login')]//input[2]",
        "//form//input[2]",
        "//*[@id='login-container']//input[2]",
        
        # Your original XPaths
        '//*[@id="login-container"]/div/div/div/div/div[3]/div[2]/div/input',
        '/html/body/div[8]/div/div/div/div/div/div/div/div[2]/div/div[3]/div[2]/div/input',
        '/html/body/div[5]/div/div/div/div/div/div/div/div[2]/div/div[3]/div[2]/div/input'
    ]

    # Submit button selectors (successful one first)
    submit_selectors = [
        "button[class*='login']",  # ✅ Working selector
        "button[type='submit']",
        "input[type='submit']",
        "button[class*='submit']",
        ".login-btn",
        ".submit-btn",
        
        # XPath selectors
        "//button[@type='submit']",
        "//input[@type='submit']",
        "//button[contains(text(), 'Login')]",
        "//button[contains(text(), 'login')]",
        "//button[contains(@class, 'login')]",
        "//button[contains(@class, 'submit')]",
        
        # Lazada-specific patterns
        "//div[contains(@class, 'login')]//button",
        "//form//button",
        "//*[@id='login-container']//button",
        
        # Your original XPaths
        '//*[@id="login-container"]/div/div/div/div/div[3]/button',
        '/html/body/div[8]/div/div/div/div/div/div/div/div[2]/div/div[3]/button',
        '/html/body/div[5]/div/div/div/div/div/div/div/div[2]/div/div[3]/button'
    ]

    # Fill email field
    print("[INFO] Looking for email field...")
    email_field = wait_and_find_element(driver, email_selectors, timeout=10)
    
    # Scroll to element and ensure it's visible
    driver.execute_script("arguments[0].scrollIntoView(true);", email_field)
    time.sleep(0.5)
    
    print("[INFO] Filling email field...")
    if not safe_type(email_field, EMAIL):
        # Fallback: try JavaScript
        driver.execute_script("arguments[0].value = arguments[1];", email_field, EMAIL)
        print("✅ Email filled using JavaScript fallback")

    # Fill password field
    print("[INFO] Looking for password field...")
    password_field = wait_and_find_element(driver, password_selectors, timeout=10)
    
    # Scroll to element and ensure it's visible
    driver.execute_script("arguments[0].scrollIntoView(true);", password_field)
    time.sleep(0.5)
    
    print("[INFO] Filling password field...")
    if not safe_type(password_field, PASSWORD):
        # Fallback: try JavaScript
        driver.execute_script("arguments[0].value = arguments[1];", password_field, PASSWORD)
        print("✅ Password filled using JavaScript fallback")

    # Submit the form
    print("[INFO] Looking for submit button...")
    submit_button = wait_and_find_element(driver, submit_selectors, timeout=10, clickable=True)
    
    print("[INFO] Submitting login form...")
    if click_element_safely(driver, submit_button):
        print("✅ Login form submitted successfully")
    else:
        # Try submitting with Enter key as fallback
        password_field.send_keys(Keys.RETURN)
        print("✅ Form submitted using Enter key")

    # Enhanced login verification
    print("[INFO] Verifying login success...")
    success_indicators = [
        lambda d: "account" in d.current_url.lower(),
        lambda d: "profile" in d.current_url.lower(),
        lambda d: "dashboard" in d.current_url.lower(),
        lambda d: d.find_elements(By.XPATH, "//*[contains(@class, 'account')]"),
        lambda d: d.find_elements(By.XPATH, "//*[contains(text(), 'Welcome')]"),
        lambda d: not d.find_elements(By.XPATH, "//input[@type='email']")  # Login form gone
    ]
    
    def process_product(url, quantity=1):
        """Process a single product URL with quantity"""
        try:
            print(f"\n[INFO] Processing product URL: {url}")
            driver.get(url)
            
            # Wait for product page to load
            print("[INFO] Waiting for product page to load...")
            WebDriverWait(driver, 20).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            time.sleep(5)  # Increased wait for dynamic content
            
            # Verify we're on a product page by checking for product elements
            product_indicators = [
                "//h1[contains(@class, 'pdp-mod-product-title')]",
                "//div[contains(@class, 'pdp-product-title')]",
                "//div[@id='module_product_title']"
            ]
            
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, product_indicators[0]))
                )
                print("✅ Product page loaded successfully")
            except:
                print("⚠️ Product page load uncertain")
            
            # Wait for and set quantity
            quantity_xpath = "//*[@id='module_quantity-input']/div/div/div/div[2]/span/input"
            print("[INFO] Looking for quantity input...")
            try:
                quantity_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, quantity_xpath))
                )
                # Clear and set quantity
                quantity_input.clear()
                quantity_input.send_keys(str(quantity))
                print(f"✅ Set quantity to {quantity}")
                time.sleep(1)
            except Exception as e:
                print(f"⚠️ Could not set quantity: {str(e)}")
            
            # Click Add to Cart button using multiple selectors
            cart_button_selectors = [
                # New exact XPath selectors
                (By.XPATH, "//*[@id='module_add_to_cart']/div/div/button[2]"),
                (By.XPATH, "/html/body/div[5]/div/div[3]/div[2]/div/div/div[16]/div[1]/div/div/div/button[2]"),
                
                # CSS Selector from JavaScript path
                (By.CSS_SELECTOR, "#module_add_to_cart > div > div > button.iweb-button.iweb-button-primary.add-to-cart-buy-now-btn"),
                
                # Class-based selectors
                (By.CSS_SELECTOR, "button.iweb-button.iweb-button-primary.add-to-cart-buy-now-btn"),
                
                # XPath using exact class combination
                (By.XPATH, "//button[@class='iweb-button iweb-button-primary add-to-cart-buy-now-btn   add-to-cart-buy-now-btn  ']"),
                
                # XPath using partial class match
                (By.XPATH, "//button[contains(@class, 'add-to-cart-buy-now-btn')]"),
                
                # Type and class combination
                (By.XPATH, "//button[@type='button' and contains(@class, 'add-to-cart-buy-now-btn')]")
            ]
            print("[INFO] Looking for Add to Cart button...")
            
            try:
                cart_button = None
                
                # Try Selenium selectors first
                for by, selector in cart_button_selectors:
                    try:
                        print(f"[DEBUG] Trying Add to Cart button selector: {selector}")
                        # First try to find the element
                        element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((by, selector))
                        )
                        # Then ensure it's clickable
                        cart_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((by, selector))
                        )
                        print(f"✅ Found Add to Cart button with selector: {selector}")
                        break
                    except Exception:
                        continue
                
                # If Selenium selectors fail, try JavaScript
                if cart_button is None:
                    print("[DEBUG] Trying JavaScript selector...")
                    try:
                        cart_button = driver.execute_script(
                            "return document.querySelector('#module_add_to_cart > div > div > button.iweb-button.iweb-button-primary.add-to-cart-buy-now-btn.add-to-cart-buy-now-btn')"
                        )
                        if cart_button:
                            print("✅ Found Add to Cart button using JavaScript")
                    except Exception as e:
                        print(f"[DEBUG] JavaScript selector failed: {str(e)}")
                        
                if cart_button is None:
                    raise Exception("Could not find Add to Cart button with any selector")
                
                # Scroll to button
                driver.execute_script("arguments[0].scrollIntoView(true);", cart_button)
                time.sleep(2)  # Wait longer after scroll
                
                # Try multiple click methods
                try:
                    # Try regular click first
                    cart_button.click()
                except Exception:
                    try:
                        # Try JavaScript click
                        driver.execute_script("arguments[0].click();", cart_button)
                    except Exception:
                        # Try Actions chain click
                        ActionChains(driver).move_to_element(cart_button).click().perform()
                print("✅ Clicked Add to Cart button")
                time.sleep(2)  # Wait for cart update
                
                # Check for popup form and close it using the specific close button
                close_button_selectors = [
                    "/html/body/div[11]/div/div[2]/a/i",  # Exact xpath provided
                    "//i[contains(@class, 'next-icon-close next-icon-small')]",  # Class-based selector
                    "//i[@class='next-icon next-icon-close next-icon-small']",  # Full class selector
                    "//div[contains(@class, 'next-dialog')]//i[contains(@class, 'next-icon-close')]",  # More general selector
                ]
                
                try:
                    print("[INFO] Looking for form close button...")
                    close_button = wait_and_find_element(driver, close_button_selectors, timeout=5, clickable=True)
                    if close_button:
                        print("[INFO] Found form close button, attempting to close...")
                        if click_element_safely(driver, close_button):
                            print("✅ Successfully closed form")
                            time.sleep(1)
                        else:
                            print("⚠️ Failed to click close button")
                except Exception as e:
                    print("[INFO] No popup form found or already closed")
                
                # Navigate to cart using the cart button with exact selectors
                print("[INFO] Looking for cart button...")
                try:
                    # Try exact XPath first
                    try:
                        cart_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//*[@id='topActionHeader']/div[1]/div[2]/div/div[3]/a/span[1]"))
                        )
                        print("✅ Found cart button with XPath")
                    except Exception:
                        print("[INFO] XPath selector failed, trying JavaScript...")
                        # Try JavaScript selector as fallback
                        cart_button = driver.execute_script(
                            'return document.querySelector("#topActionHeader > div.lzd-header-content > div.lzd-logo-bar.default > div > div.lzd-nav-cart > a > span.cart-icon")')
                        if cart_button:
                            print("✅ Found cart button with JavaScript")
                        else:
                            raise Exception("Could not find cart button with any selector")

                    # Try to click the cart button
                    print("[INFO] Attempting to click cart button...")
                    try:
                        # Try regular click first
                        cart_button.click()
                    except Exception:
                        try:
                            # Try JavaScript click
                            driver.execute_script("arguments[0].click();", cart_button)
                        except Exception:
                            # Try clicking the parent <a> tag
                            parent_a = driver.execute_script("return arguments[0].closest('a')", cart_button)
                            if parent_a:
                                driver.execute_script("arguments[0].click();", parent_a)
                            else:
                                raise Exception("Failed to click cart button")
                    
                    print("✅ Successfully clicked cart button")
                    # Wait for cart page to load
                    WebDriverWait(driver, 20).until(lambda d: "cart" in d.current_url.lower())
                    print("✅ Cart page loaded")
                    time.sleep(2)  # Wait for cart to fully load
                    
                except Exception as e:
                    print(f"⚠️ Error navigating to cart: {str(e)}")
                    return False
                
                # Wait for cart page to load
                WebDriverWait(driver, 20).until(lambda d: "cart" in d.current_url.lower())
                print("✅ Cart page loaded")
                time.sleep(2)  # Wait for cart to fully load
                
                # Find and click the product selection checkbox
                print("[INFO] Looking for product selection checkbox...")
                try:
                    # Wait a bit for the cart page to fully render
                    time.sleep(3)
                    
                    # Try exact XPath first
                    try:
                        print("[INFO] Trying XPath selector...")
                        checkbox = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, "//*[@id='listHeader_H']/div/div/div[1]/label/input"))
                        )
                        print("✅ Found checkbox with XPath")
                    except Exception:
                        # Try JavaScript selector as fallback
                        print("[INFO] XPath failed, trying JavaScript selector...")
                        checkbox = driver.execute_script(
                            'return document.querySelector("#listHeader_H > div > div > div.checkbox-wrap > label > input[type=checkbox]")')
                        if checkbox:
                            print("✅ Found checkbox with JavaScript")
                        else:
                            raise Exception("Could not find checkbox with any selector")
                    
                    # Check if already selected
                    is_selected = driver.execute_script("return arguments[0].checked", checkbox)
                    if not is_selected:
                        print("[INFO] Checkbox not selected, attempting to click...")
                        try:
                            # Try JavaScript click first (more reliable)
                            driver.execute_script("arguments[0].click(); arguments[0].checked = true;", checkbox)
                            print("✅ Clicked checkbox via JavaScript")
                        except Exception:
                            try:
                                # Try regular Selenium click as fallback
                                checkbox.click()
                                print("✅ Clicked checkbox via Selenium")
                            except Exception:
                                # Try clicking the parent label as last resort
                                parent_label = driver.execute_script("return arguments[0].parentElement", checkbox)
                                if parent_label:
                                    driver.execute_script("arguments[0].click();", parent_label)
                                    print("✅ Clicked checkbox via parent label")
                                else:
                                    raise Exception("Failed to click checkbox")
                    else:
                        print("[INFO] Checkbox already selected")
                    
                    # Verify checkbox is selected
                    is_selected = driver.execute_script("return arguments[0].checked", checkbox)
                    if not is_selected:
                        print("❌ Checkbox selection failed")
                        return False
                    
                    time.sleep(1)  # Wait for any updates after checkbox selection
                except Exception as e:
                    print(f"❌ Error during checkbox selection: {str(e)}")
                    return False
                
                # Wait for and click the proceed to checkout button
                print("[INFO] Looking for proceed to checkout button...")
                checkout_button_selectors = [
                    # XPath selectors
                    "//*[@id='rightContainer_CR']/div/div[2]/div/div[3]/button",
                    "/html/body/div[2]/div/div[2]/div/div/div[1]/div[2]/div/div[2]/div/div[3]/button",
                    
                    # CSS selectors
                    "button.next-btn.next-btn-primary.next-btn-large.checkout-order-total-button.automation-checkout-order-total-button-button",
                    
                    # More general selectors as fallback
                    "button.checkout-order-total-button",
                    "button[class*='checkout-order-total-button']",
                    "button[class*='proceed-checkout']",
                    "//button[contains(text(), 'PROCEED TO CHECKOUT')]"                
                ]
                
                try:
                    checkout_button = wait_and_find_element(driver, checkout_button_selectors, timeout=10, clickable=True)
                    if checkout_button:
                        # Try multiple click methods
                        try:
                            # Method 1: Regular click
                            checkout_button.click()
                            print("✅ Clicked checkout button")
                        except Exception as e:
                            print(f"[INFO] Regular click failed: {str(e)}")
                            try:
                                # Method 2: JavaScript click
                                driver.execute_script("arguments[0].click();", checkout_button)
                                print("✅ Clicked checkout button via JavaScript")
                            except Exception as e:
                                print(f"[INFO] JavaScript click failed: {str(e)}")
                                try:
                                    # Method 3: Try JavaScript querySelector
                                    driver.execute_script("""
                                        const btn = document.querySelector("#rightContainer_CR > div > div.summary-section-content > div > div.checkout-order-total > button");
                                        if (btn) btn.click();
                                    """)
                                    print("✅ Clicked checkout button via querySelector")
                                except Exception as e:
                                    print(f"❌ Failed to click checkout button: {str(e)}")
                                    return False
                        
                        # Wait for checkout page load
                        try:
                            WebDriverWait(driver, 10).until(lambda d: "checkout" in d.current_url.lower())
                            print("✅ Checkout page loaded")
                            return True
                        except Exception as e:
                            print(f"❌ Failed to load checkout page: {str(e)}")
                            return False
                    else:
                        print("❌ Could not find checkout button")
                        return False
                except Exception as e:
                    print(f"❌ Error during checkout process: {str(e)}")
                    return False
                
            except Exception as e:
                print(f"❌ Failed to add to cart: {str(e)}")
                return False
                
        except Exception as e:
            print(f"❌ Error processing product: {str(e)}")
            return False
    
    try:
        # Wait for login success
        WebDriverWait(driver, 20).until(
            lambda d: any(indicator(d) for indicator in success_indicators)
        )
        print("✅ Login appears successful!")
        
        # Additional wait after login success
        print("[INFO] Waiting for page to stabilize after login...")
        time.sleep(5)  # Wait for any post-login redirects/updates
        
        # Verify we're properly logged in by checking for account elements
        account_indicators = [
            "//div[contains(@class, 'account')]//span[contains(text(), 'Account')]",
            "//div[contains(@class, 'account-unsigned')]//a[contains(@href, 'member')]",
            "//div[contains(@class, 'account')]//a[contains(@href, 'user')]"
        ]
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, account_indicators[0]))
            )
            print("✅ Login verification complete")
        except:
            print("⚠️ Login state uncertain, but continuing...")
        
        # Read product URLs from CSV
        print("\n[INFO] Reading products from CSV file...")
        products = []
        try:
            with open(CSV_FILE, 'r') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)  # Skip header
                for row in csv_reader:
                    if row and row[0].strip():  # Check if row is not empty
                        url = row[0].strip()
                        # Clean up URL by removing tracking parameters
                        base_url = url.split('?')[0]
                        # Get quantity from second column if available
                        quantity = int(row[1]) if len(row) > 1 and row[1].strip().isdigit() else 1
                        products.append((base_url, quantity))
            print(f"✅ Found {len(products)} products in CSV")
        except Exception as e:
            print(f"❌ Error reading CSV: {str(e)}")
            raise Exception("Failed to read products from CSV")
            
        # Process each product
        successful_products = 0
        for i, (product_url, quantity) in enumerate(products, 1):
            print(f"\n{'='*50}")
            print(f"Processing product {i}/{len(products)}")
            print(f"{'='*50}")
            
            if process_product(product_url, quantity):
                successful_products += 1
            
            # Small delay between products
            if i < len(products):
                time.sleep(2)
        
        print(f"\n[INFO] Processing completed:")
        print(f"✅ Successfully added: {successful_products}/{len(products)} products")
        
    except Exception as e:
        print(f"❌ Error during processing: {str(e)}")
        
        # Check for error messages
        error_selectors = [
            "//*[contains(text(), 'incorrect')]",
            "//*[contains(text(), 'invalid')]",
            "//*[contains(text(), 'error')]",
            "//*[contains(text(), 'wrong')]",
            "//*[contains(@class, 'error')]",
            ".error-message",
            ".alert-danger"
        ]
        
        try:
            error_element = wait_and_find_element(driver, error_selectors, timeout=3)
            print(f"❌ Login error detected: {error_element.text}")
        except:
            print("ℹ️ No clear error message found. Login might have succeeded.")
            print(f"Current URL: {driver.current_url}")

            print("\n[INFO] Login successful! Starting product processing...")
        
        # Read product URLs from CSV
        products = []
        try:
            with open(CSV_FILE, 'r') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)  # Skip header row
                for row in csv_reader:
                    if row and row[0].strip():  # Check if row is not empty
                        url = row[0].strip()
                        # Clean up the URL by removing tracking parameters
                        url = url.split('?')[0]  # Remove everything after ?
                        products.append(url)
            print(f"✅ Loaded {len(products)} products from CSV")
        except Exception as e:
            print(f"❌ Error reading CSV: {str(e)}")
            products = []

        # Process each product
        for i, product_url in enumerate(products, 1):
            try:
                print(f"\n{'='*50}")
                print(f"Processing product {i}/{len(products)}")
                print(f"{'='*50}")
                
                # Navigate to product URL
                print(f"[INFO] Navigating to product: {product_url}")
                driver.get(product_url)
                time.sleep(3)
                
                # Wait for add to cart button
                cart_button_selectors = [
                    "//button[contains(@class, 'add-to-cart')]",
                    "//button[contains(@class, 'pdp-button_cart')]",
                    "//button[contains(text(), 'Add to Cart')]",
                    "//button[contains(text(), 'ADD TO CART')]",
                    "//button[contains(@class, 'btn--add-to-cart')]",
                    ".add-to-cart-button",
                    "#AddToCart",
                    "button.add-to-cart",
                    "//button[contains(@class, 'pdp-button')]//span[contains(text(), 'cart')]/parent::button"
                ]
                
                print("[INFO] Looking for Add to Cart button...")
                cart_button = wait_and_find_element(driver, cart_button_selectors, timeout=10, clickable=True)
                
                # Click Add to Cart
                if click_element_safely(driver, cart_button):
                    print("✅ Added to cart successfully")
                    time.sleep(2)
                else:
                    print("❌ Failed to add to cart")
                    continue
                
            except Exception as e:
                print(f"❌ Error processing product: {str(e)}")
                continue
        
        # Navigate to cart page
        try:
            print("\n[INFO] Navigating to cart...")
            cart_link_selectors = [
                "//div[contains(@class, 'cart-icon')]//a",
                "//a[contains(@href, '/cart')]",
                "//div[contains(@class, 'cart')]//a",
                ".cart-link",
                "#cart-icon",
                "//a[contains(text(), 'Cart')]",
                "//a[contains(@class, 'cart')]"
            ]
            
            cart_link = wait_and_find_element(driver, cart_link_selectors, timeout=10, clickable=True)
            if click_element_safely(driver, cart_link):
                print("✅ Navigated to cart successfully")
                time.sleep(3)
            else:
                print("❌ Failed to navigate to cart")
        except Exception as e:
            print(f"❌ Error navigating to cart: {str(e)}")
        
        print("\n[INFO] All operations completed. Check the browser window.")
        input("Press ENTER to close the browser...")

except Exception as e:
    print(f"❌ Critical error occurred: {str(e)}")
    
    # Debug information
    try:
        print(f"Current URL: {driver.current_url}")
        print("Page title:", driver.title)
        
        # Take screenshot for debugging
        driver.save_screenshot("debug_screenshot.png")
        print("Debug screenshot saved as 'debug_screenshot.png'")
        
        # Print page source snippet for debugging
        page_source = driver.page_source[:1000]
        print(f"Page source snippet: {page_source}")
        
    except:
        print("Could not gather debug information")

finally:
    try:
        input("Enter to close ") 
    except:
        pass