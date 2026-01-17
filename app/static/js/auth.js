// Toggle between login and signup forms using tab selectors
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const loginTab = document.getElementById('loginTab');
    const signupTab = document.getElementById('signupTab');

    // Switch to signup tab
    signupTab.addEventListener('click', function(e) {
        e.preventDefault();
        switchTab('signup');
    });

    // Switch to login tab
    loginTab.addEventListener('click', function(e) {
        e.preventDefault();
        switchTab('login');
    });

    // Get image elements
    const loginImage = document.getElementById('loginImage');
    const signupImage = document.getElementById('signupImage');

    // Tab switching function with animation
    function switchTab(tab) {
        // Don't switch if already on this tab
        if (tab === 'login' && loginTab.classList.contains('active')) {
            return;
        }
        if (tab === 'signup' && signupTab.classList.contains('active')) {
            return;
        }

        // Update tab selectors
        if (tab === 'login') {
            loginTab.classList.add('active');
            signupTab.classList.remove('active');
            
            // Animate images - fade out current, then fade in new
            signupImage.classList.remove('active');
            setTimeout(() => {
                loginImage.classList.add('active');
            }, 100);
            
            // Animate forms - fade out current, then fade in new
            signupForm.classList.remove('active');
            setTimeout(() => {
                loginForm.classList.add('active');
            }, 100);
        } else {
            signupTab.classList.add('active');
            loginTab.classList.remove('active');
            
            // Animate images - fade out current, then fade in new
            loginImage.classList.remove('active');
            setTimeout(() => {
                signupImage.classList.add('active');
            }, 100);
            
            // Animate forms - fade out current, then fade in new
            loginForm.classList.remove('active');
            setTimeout(() => {
                signupForm.classList.add('active');
            }, 100);
        }
    }

    // Login form validation and submission
    const loginFormElement = document.getElementById('loginForm');
    loginFormElement.addEventListener('submit', handleLogin);

    // Signup form validation and submission
    const signupFormElement = document.getElementById('signupForm');
    signupFormElement.addEventListener('submit', handleSignup);

    // Real-time validation for signup form
    setupSignupValidation();
});

// Login form handler
async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;
    const submitBtn = document.getElementById('loginSubmit');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');

    // Clear previous errors
    clearErrors('login');

    // Validate
    let isValid = true;
    if (!email) {
        showError('loginEmailError', 'Email is required');
        isValid = false;
    } else if (!isValidKUEmail(email)) {
        showError('loginEmailError', 'Please enter a valid KU Mail address');
        isValid = false;
    }

    if (!password) {
        showError('loginPasswordError', 'Password is required');
        isValid = false;
    }

    if (!isValid) {
        return;
    }

    // Show loading state
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            showToast('Login successful!', 'success');
            // Redirect will be handled by backend
            setTimeout(() => {
                window.location.href = data.redirect || '/';
            }, 1000);
        } else {
            showToast(data.message || 'Login failed. Please check your credentials.', 'error');
            if (data.field) {
                showError(`login${data.field}Error`, data.message);
            }
        }
    } catch (error) {
        showToast('An error occurred. Please try again.', 'error');
        console.error('Login error:', error);
    } finally {
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

// Signup form handler
async function handleSignup(e) {
    e.preventDefault();
    
    const firstName = document.getElementById('signupFirstName').value.trim();
    const lastName = document.getElementById('signupLastName').value.trim();
    const email = document.getElementById('signupEmail').value.trim();
    const birthdate = document.getElementById('signupBirthdate').value;
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('signupConfirmPassword').value;
    const submitBtn = document.getElementById('signupSubmit');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');

    // Clear previous errors
    clearErrors('signup');

    // Validate all fields
    let isValid = true;

    if (!firstName) {
        showError('signupFirstNameError', 'First name is required');
        isValid = false;
    }

    if (!lastName) {
        showError('signupLastNameError', 'Last name is required');
        isValid = false;
    }

    if (!email) {
        showError('signupEmailError', 'Email is required');
        isValid = false;
    } else if (!isValidKUEmail(email)) {
        showError('signupEmailError', 'Please enter a valid KU Mail address (@ku.edu.tr)');
        isValid = false;
    }

    if (!birthdate) {
        showError('signupBirthdateError', 'Birthdate is required');
        isValid = false;
    }

    if (!password) {
        showError('signupPasswordError', 'Password is required');
        isValid = false;
    } else if (password.length < 8) {
        showError('signupPasswordError', 'Password must be at least 8 characters');
        isValid = false;
    }

    if (!confirmPassword) {
        showError('signupConfirmPasswordError', 'Please confirm your password');
        isValid = false;
    } else if (password !== confirmPassword) {
        showError('signupConfirmPasswordError', 'Passwords do not match');
        isValid = false;
    }

    if (!isValid) {
        return;
    }

    // Show loading state
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';

    try {
        const response = await fetch('/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                firstName,
                lastName,
                email,
                birthdate,
                password
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            showToast('Account created successfully!', 'success');
            // Switch to login tab after successful signup
            setTimeout(() => {
                document.getElementById('loginTab').click();
                // Pre-fill email
                document.getElementById('loginEmail').value = email;
            }, 1500);
        } else {
            showToast(data.message || 'Sign up failed. Please try again.', 'error');
            if (data.field) {
                showError(`signup${data.field}Error`, data.message);
            }
        }
    } catch (error) {
        showToast('An error occurred. Please try again.', 'error');
        console.error('Signup error:', error);
    } finally {
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

// Setup real-time validation for signup form
function setupSignupValidation() {
    const passwordInput = document.getElementById('signupPassword');
    const confirmPasswordInput = document.getElementById('signupConfirmPassword');
    const emailInput = document.getElementById('signupEmail');

    // Password strength indicator
    passwordInput.addEventListener('input', function() {
        const password = this.value;
        checkPasswordStrength(password);
        
        // Clear confirm password error if password changes
        if (confirmPasswordInput.value) {
            validatePasswordMatch();
        }
    });

    // Confirm password matching
    confirmPasswordInput.addEventListener('input', validatePasswordMatch);

    // Email validation
    emailInput.addEventListener('blur', function() {
        const email = this.value.trim();
        if (email && !isValidKUEmail(email)) {
            showError('signupEmailError', 'Please enter a valid KU Mail address (@ku.edu.tr)');
            emailInput.classList.add('error');
        } else if (email) {
            emailInput.classList.remove('error');
            emailInput.classList.add('success');
            clearError('signupEmailError');
        }
    });
}

// Validate password match
function validatePasswordMatch() {
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('signupConfirmPassword').value;
    const confirmInput = document.getElementById('signupConfirmPassword');

    if (confirmPassword && password !== confirmPassword) {
        showError('signupConfirmPasswordError', 'Passwords do not match');
        confirmInput.classList.add('error');
        confirmInput.classList.remove('success');
    } else if (confirmPassword && password === confirmPassword) {
        clearError('signupConfirmPasswordError');
        confirmInput.classList.remove('error');
        confirmInput.classList.add('success');
    }
}

// Check password strength
function checkPasswordStrength(password) {
    const strengthDiv = document.getElementById('passwordStrength');
    
    if (!password) {
        strengthDiv.innerHTML = '';
        strengthDiv.className = 'password-strength';
        return;
    }

    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[^a-zA-Z\d]/.test(password)) strength++;

    let strengthClass = 'weak';
    if (strength >= 3) strengthClass = 'medium';
    if (strength >= 4) strengthClass = 'strong';

    strengthDiv.className = `password-strength ${strengthClass}`;
    strengthDiv.innerHTML = '<div class="password-strength-bar"></div>';
}

// Validate KU Email format
function isValidKUEmail(email) {
    const kuEmailRegex = /^[a-zA-Z0-9._%+-]+@ku\.edu\.tr$/;
    return kuEmailRegex.test(email);
}

// Show error message
function showError(errorId, message) {
    const errorElement = document.getElementById(errorId);
    if (errorElement) {
        errorElement.textContent = message;
    }
}

// Clear error message
function clearError(errorId) {
    const errorElement = document.getElementById(errorId);
    if (errorElement) {
        errorElement.textContent = '';
    }
}

// Clear all errors for a form
function clearErrors(formType) {
    const errorIds = formType === 'login' 
        ? ['loginEmailError', 'loginPasswordError']
        : ['signupFirstNameError', 'signupLastNameError', 'signupEmailError', 'signupBirthdateError', 'signupPasswordError', 'signupConfirmPasswordError'];
    
    errorIds.forEach(id => clearError(id));

    // Remove error/success classes from inputs
    const form = document.getElementById(formType === 'login' ? 'loginForm' : 'signupForm');
    const inputs = form.querySelectorAll('input');
    inputs.forEach(input => {
        input.classList.remove('error', 'success');
    });
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}



