# tests/test_app_flow.py

import unittest
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import shutil
import sys
# Shared server & driver for all tests in this module
server = None
driver = None
wait = None

def setUpModule():
    """Start HTTP server and browser once for all tests."""
    global server, driver, wait
    server = subprocess.Popen(
        ["python3", "-m", "http.server", "3000"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment if you want headless testing
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    chromedriver_path = shutil.which("chromedriver")
    if not chromedriver_path:
        sys.exit("❌ ChromeDriver not found in PATH. Make sure it is installed and available.")

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 5)


def tearDownModule():
    """Stop browser and HTTP server."""
    global server, driver
    driver.quit()
    server.terminate()

class IndexPageTests(unittest.TestCase):
    base_url = "http://localhost:3000/index.html"

    def setUp(self):
        self.driver = driver
        self.wait = wait
        self.driver.get(self.base_url)
        # Ensure login form is present before each test
        self.wait.until(EC.presence_of_element_located((By.ID, "loginForm")))

    def test_valid_login_with_email_shows_survey(self):
        """Logging in with valid email & password hides login and shows survey."""
        self.driver.find_element(By.ID, "emailInput").send_keys("testuser@example.com")
        self.driver.find_element(By.ID, "passwordInput").send_keys("Test1234")
        self.driver.find_element(By.CLASS_NAME, "btn-login").click()

        survey = self.wait.until(EC.visibility_of_element_located((By.ID, "surveyContainer")))
        self.assertTrue(survey.is_displayed())
        self.assertFalse(self.driver.find_element(By.ID, "loginContainer").is_displayed())

    def test_valid_login_with_phone_shows_survey(self):
        """Logging in with valid phone & password shows the survey form."""
        self.driver.find_element(By.ID, "emailInput").send_keys("5551234567")
        self.driver.find_element(By.ID, "passwordInput").send_keys("phonePass")
        self.driver.find_element(By.CLASS_NAME, "btn-login").click()

        survey = self.wait.until(EC.visibility_of_element_located((By.ID, "surveyContainer")))
        self.assertTrue(survey.is_displayed())

    def test_invalid_login_shows_error(self):
        """Incorrect credentials display an error and keep login visible."""
        self.driver.find_element(By.ID, "emailInput").send_keys("wrong@example.com")
        self.driver.find_element(By.ID, "passwordInput").send_keys("badpass")
        self.driver.find_element(By.CLASS_NAME, "btn-login").click()

        msg = self.wait.until(EC.visibility_of_element_located((By.ID, "message")))
        self.assertEqual(msg.text, "Invalid Credentials. Try again!")
        self.assertFalse(self.driver.find_element(By.ID, "surveyContainer").is_displayed())

    def test_missing_email_shows_fill_all_message(self):
        """Submitting without email shows the 'fill out all fields' message."""
        self.driver.find_element(By.ID, "passwordInput").send_keys("Test1234")
        self.driver.find_element(By.CLASS_NAME, "btn-login").click()

        msg = self.wait.until(EC.visibility_of_element_located((By.ID, "message")))
        self.assertEqual(msg.text, "Please fill out all fields.")

    def test_missing_password_shows_fill_all_message(self):
        """Submitting without password shows the 'fill out all fields' message."""
        self.driver.find_element(By.ID, "emailInput").send_keys("testuser@example.com")
        self.driver.find_element(By.CLASS_NAME, "btn-login").click()

        msg = self.wait.until(EC.visibility_of_element_located((By.ID, "message")))
        self.assertEqual(msg.text, "Please fill out all fields.")

    def test_google_button_shows_survey(self):
        """Clicking the Google button immediately shows the survey."""
        self.driver.find_element(By.ID, "googleBtn").click()
        survey = self.wait.until(EC.visibility_of_element_located((By.ID, "surveyContainer")))
        self.assertTrue(survey.is_displayed())

    def test_facebook_button_shows_survey(self):
        """Clicking the Facebook button immediately shows the survey."""
        self.driver.find_element(By.ID, "facebookBtn").click()
        survey = self.wait.until(EC.visibility_of_element_located((By.ID, "surveyContainer")))
        self.assertTrue(survey.is_displayed())

    def test_survey_form_fields_present_after_login(self):
        """After a successful login, all expected survey fields are present."""
        # perform a valid login
        self.driver.find_element(By.ID, "emailInput").send_keys("testuser@example.com")
        self.driver.find_element(By.ID, "passwordInput").send_keys("Test1234")
        self.driver.find_element(By.CLASS_NAME, "btn-login").click()
        self.wait.until(EC.visibility_of_element_located((By.ID, "surveyForm")))

        # verify key inputs/buttons
        for field_id in ["fullName", "birthDate", "educationLevel", "city", "useCases", "surveySubmit"]:
            el = self.driver.find_element(By.ID, field_id)
            # 'surveySubmit' is a button, others should be enabled inputs
            self.assertTrue(el.is_enabled() or el.tag_name == "button")

class SurveyBuilderTests(unittest.TestCase):
    base_url = "http://localhost:3000/survey-builder.html"

    def setUp(self):
        self.driver = driver
        self.wait = wait
        self.driver.get(self.base_url)
        # Ensure builder is ready
        self.wait.until(EC.presence_of_element_located((By.ID, "newQuestionBtn")))

    def test_new_question_button_resets_form(self):
        """Clicking “New Question” clears inputs and keeps Save disabled."""
        # pre-fill
        self.driver.find_element(By.ID, "qText").send_keys("foo")
        Select(self.driver.find_element(By.ID, "qType")).select_by_value("text")
        # reset
        self.driver.find_element(By.ID, "newQuestionBtn").click()

        self.assertEqual(self.driver.find_element(By.ID, "formTitle").text, "Add Question")
        self.assertEqual(self.driver.find_element(By.ID, "qText").get_attribute("value"), "")
        self.assertEqual(
            Select(self.driver.find_element(By.ID, "qType")).first_selected_option.get_attribute("value"),
            ""
        )
        self.assertFalse(self.driver.find_element(By.ID, "saveQuestionBtn").is_enabled())

    def test_saving_multiple_choice_question_updates_list_and_preview(self):
        """Saving an MCQ adds it to the list and renders radio inputs in preview."""
        # fill MCQ
        self.driver.find_element(By.ID, "qText").send_keys("Favorite color?")
        Select(self.driver.find_element(By.ID, "qType")).select_by_value("multiple-choice")
        self.wait.until(EC.visibility_of_element_located((By.ID, "optionsGroup")))
        self.driver.find_element(By.ID, "qOptions").send_keys("Red\nGreen\nBlue")

        save = self.driver.find_element(By.ID, "saveQuestionBtn")
        self.assertTrue(save.is_enabled())
        save.click()

        # list updated
        items = self.driver.find_elements(By.CLASS_NAME, "q-item")
        self.assertEqual(len(items), 1)
        self.assertIn("Favorite color? (multiple-choice)", items[0].text)

        # preview correctness
        preview_label = self.driver.find_element(By.CSS_SELECTOR, "#previewForm label")
        self.assertEqual(preview_label.text, "Favorite color?")
        radios = self.driver.find_elements(By.CSS_SELECTOR, "#previewForm input[type=radio]")
        self.assertEqual(len(radios), 3)

    def test_conditional_logic_hides_and_shows_dependent_question(self):
        """A dependent question stays hidden until its trigger answer is selected."""
        # Q1: MCQ
        self.driver.find_element(By.ID, "qText").send_keys("Pick one")
        Select(self.driver.find_element(By.ID, "qType")).select_by_value("multiple-choice")
        self.wait.until(EC.visibility_of_element_located((By.ID, "optionsGroup")))
        self.driver.find_element(By.ID, "qOptions").send_keys("A\nB")
        self.driver.find_element(By.ID, "saveQuestionBtn").click()

        # Q2: conditional text
        self.driver.find_element(By.ID, "qText").send_keys("Why A?")
        Select(self.driver.find_element(By.ID, "qType")).select_by_value("text")
        self.driver.find_element(By.ID, "enableCond").click()
        Select(self.driver.find_element(By.ID, "condQuestion")).select_by_value("0")
        self.wait.until(EC.element_to_be_clickable((By.ID, "condValue")))
        Select(self.driver.find_element(By.ID, "condValue")).select_by_visible_text("A")
        self.driver.find_element(By.ID, "saveQuestionBtn").click()

        wrappers = self.driver.find_elements(By.CSS_SELECTOR, "#previewForm > div")
        self.assertEqual(len(wrappers), 2)
        self.assertFalse(wrappers[1].is_displayed())

        # trigger show
        first_radio = self.driver.find_element(
            By.XPATH, "//label[contains(., 'A')]/input[@type='radio']"
        )
        first_radio.click()
        self.wait.until(lambda d: wrappers[1].is_displayed())
        self.assertTrue(wrappers[1].is_displayed())

    def test_export_and_import_survey_code_preserves_questions(self):
        """Exporting to Base64 and re-importing restores the exact question set."""
        # add a text question
        self.driver.find_element(By.ID, "qText").send_keys("Q?")
        Select(self.driver.find_element(By.ID, "qType")).select_by_value("text")
        self.driver.find_element(By.ID, "saveQuestionBtn").click()

        # export
        self.wait.until(lambda d: d.find_element(By.ID, "createSurveyBtn").is_enabled())
        self.driver.find_element(By.ID, "createSurveyBtn").click()

        code_area = self.driver.find_element(By.ID, "surveyCode")
        self.assertTrue(code_area.is_displayed())
        code = code_area.get_attribute("value")
        self.assertGreater(len(code), 0)

        # reload & import
        self.driver.get(self.base_url)
        self.wait.until(EC.presence_of_element_located((By.ID, "loadSurveyCode")))
        self.driver.find_element(By.ID, "loadSurveyCode").send_keys(code)
        self.driver.find_element(By.ID, "loadSurveyBtn").click()

        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "q-item")))
        self.assertEqual(len(items), 1)
        self.assertIn("Q? (text)", items[0].text)
        preview_label = self.driver.find_element(By.CSS_SELECTOR, "#previewForm label")
        self.assertEqual(preview_label.text, "Q?")

    def test_import_invalid_survey_code_shows_alert(self):
        """Loading a malformed Base64 code shows an alert and leaves the question list empty."""
        # make sure builder is loaded
        self.wait.until(EC.presence_of_element_located((By.ID, "loadSurveyCode")))
        self.driver.find_element(By.ID, "loadSurveyCode").send_keys("not-base64!!!")
        # hijack window.alert to capture message
        self.driver.execute_script("window.alert = msg => window._lastAlert = msg;")
        self.driver.find_element(By.ID, "loadSurveyBtn").click()
        alert_text = self.driver.execute_script("return window._lastAlert;")
        self.assertIn("Invalid survey code", alert_text)
        # no questions should be added
        items = self.driver.find_elements(By.CLASS_NAME, "q-item")
        self.assertEqual(len(items), 0)

    def test_rapid_new_and_save_does_not_crash(self):
        """Repeated New→Save clicks don’t break the builder, and you can still add a real question."""
        self.wait.until(EC.element_to_be_clickable((By.ID, "newQuestionBtn")))
        for _ in range(10):
            self.driver.find_element(By.ID, "newQuestionBtn").click()
            self.driver.find_element(By.ID, "saveQuestionBtn").click()
        # now actually add one valid question
        self.driver.find_element(By.ID, "qText").send_keys("Stable?")
        Select(self.driver.find_element(By.ID, "qType")).select_by_value("text")
        self.driver.find_element(By.ID, "saveQuestionBtn").click()
        items = self.driver.find_elements(By.CLASS_NAME, "q-item")
        self.assertTrue(any("Stable? (text)" in itm.text for itm in items))

class SurveyPageErrorTests(unittest.TestCase):
    def setUp(self):
        self.driver = driver
        self.wait = wait

    def test_survey_page_no_code_shows_error(self):
        """Visiting survey.html without "?code=" displays the error message."""
        self.driver.get("http://localhost:3000/survey.html")
        err = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body p")))
        self.assertEqual(err.text, "No survey code provided.")


class BuilderFeatureTests(unittest.TestCase):
    base_url = "http://localhost:3000/survey-builder.html"

    def setUp(self):
        self.driver = driver
        self.wait = wait
        self.driver.get(self.base_url)
        self.wait.until(EC.element_to_be_clickable((By.ID, "newQuestionBtn")))

    def test_options_group_appears_for_multiple_choice_and_disappears_for_text(self):
        # Select MCQ → options textarea appears
        Select(self.driver.find_element(By.ID, "qType")).select_by_value("multiple-choice")
        self.assertTrue(self.driver.find_element(By.ID, "optionsGroup").is_displayed())

        # Switch to text → options hidden
        Select(self.driver.find_element(By.ID, "qType")).select_by_value("text")
        self.assertFalse(self.driver.find_element(By.ID, "optionsGroup").is_displayed())

    
if __name__ == "__main__":
    unittest.main()
