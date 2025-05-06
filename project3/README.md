# Project README

## Project Structure

- **`.venv/`**: This folder contains the virtual environment for the project. It ensures that all necessary dependencies are isolated from your system environment.
- **`index.html`**: The HTML file where the front-end code is located. This file contains the structure of the page, including the login form.
- **`login.js`**: The JavaScript file that contains the logic for the login functionality. It interacts with the elements in the HTML and handles the user input.
- **`css/`**: A folder that contains the styles for the project. While the CSS files are not crucial to the functionality, they are included for styling the application.
- **`test.py`**: This file contains the test cases for the application. It includes automated tests that interact with the front-end logic to verify the correctness of the login functionality.

### Activate the Virtual Environment

Once the virtual environment is created, activate it and run the test.py for the tests.

The test functions inside `test.py` will run automatically, and the results will be displayed in the terminal. The tests simulate login actions and verify that the application behaves as expected.

## How the Project Works

- **HTML (`index.html`)**: Contains the structure of the page, including the login form and other necessary elements.
- **JavaScript (`login.js`)**: The login logic that validates the user's credentials and performs actions based on user input.
- **CSS (`css/`)**: Used to style the application (though not essential for functionality).

The primary logic for the test case automation resides inside the `test.py` file, where Selenium is used to simulate user interactions with the HTML elements. The tests are automatically executed upon running `python test.py`.