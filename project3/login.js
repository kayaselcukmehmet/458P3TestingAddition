// Mock user data (in real scenarios, you would fetch from a server or database)
const mockUserData = [
  {
    emailOrPhone: "testuser@example.com",
    password: "Test1234",
  },
  {
    emailOrPhone: "5551234567",
    password: "phonePass",
  }
];

// Grab references to form elements
const loginForm = document.getElementById("loginForm");
const emailInput = document.getElementById("emailInput");
const passwordInput = document.getElementById("passwordInput");
const messageDiv = document.getElementById("message");

// Buttons for Google & Facebook (mock)
const googleBtn = document.getElementById("googleBtn");
const facebookBtn = document.getElementById("facebookBtn");

// Handle standard email/phone + password login
loginForm.addEventListener("submit", function (event) {
  event.preventDefault(); // Prevents page refresh

  const enteredEmailOrPhone = emailInput.value.trim();
  const enteredPassword = passwordInput.value.trim();

  // Validate inputs
  if (!enteredEmailOrPhone || !enteredPassword) {
    displayMessage("Please fill out all fields.", "error");
    return;
  }

  // Check credentials against mock data
  const userFound = mockUserData.find(
    (user) =>
      user.emailOrPhone === enteredEmailOrPhone && user.password === enteredPassword
  );

  if (userFound) {
    // Success
    displayMessage("Login Successful! Welcome!", "success");
    // You could redirect to another page:
    // window.location.href = "dashboard.html";
  } else {
    // Failure
    displayMessage("Invalid Credentials. Try again!", "error");
  }
});

// Mock Google login
googleBtn.addEventListener("click", function () {
  // In a real app, you'd integrate Google OAuth2.
  // For demonstration, we just show a success message:
  displayMessage("Google sign-in successful (mock).", "success");
});

// Mock Facebook login
facebookBtn.addEventListener("click", function () {
  // Similar to above, real integration with Facebook's API would go here.
  // We just simulate success/failure:
  displayMessage("Facebook sign-in successful (mock).", "success");
});

/**
 * Utility function to display success or error messages
 * @param {string} text - The message to display
 * @param {string} type - "success" or "error"
 */
function displayMessage(text, type) {
  messageDiv.textContent = text;
  messageDiv.style.color = type === "success" ? "green" : "red";
}
