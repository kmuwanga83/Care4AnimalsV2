# SETUP_SMS_GATEWAY.md

## Documentation for Configuring and Testing Africa's Talking SMS Gateway Integration

This document provides step-by-step instructions for configuring and testing the Africa's Talking SMS Gateway integration for the Care 4 Animals V2 application.

### Table of Contents
1. [Prerequisites](#prerequisites)
2. [Step 1: Create an Africa's Talking Account](#step-1-create-an-africas-talking-account)
3. [Step 2: Obtain API Credentials](#step-2-obtain-api-credentials)
4. [Step 3: Install Africa's Talking SDK](#step-3-install-africas-talking-sdk)
5. [Step 4: Configure the SDK](#step-4-configure-the-sdk)
6. [Step 5: Testing the SMS Gateway Integration](#step-5-testing-the-sms-gateway-integration)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites
- A registered account with Africa's Talking.
- Basic knowledge of how to work with APIs.
- Development environment for the Care 4 Animals V2 application.

## Step 1: Create an Africa's Talking Account
1. Go to the [Africa's Talking website](https://africastalking.com).
2. Click on the 'Sign Up' button and complete the registration process.

## Step 2: Obtain API Credentials
1. Log in to your Africa's Talking account.
2. Navigate to the 'Dashboard'.
3. Under the API section, take note of your 'Username' and 'API Key'.

## Step 3: Install Africa's Talking SDK
For Node.js:
```bash
npm install africastalking
```

For PHP:
```bash
composer require africastalking/africastalking
```

## Step 4: Configure the SDK
1. In your application, create a configuration file (e.g., `config.js` or `config.php`).
2. Add the following code:

### For Node.js
```javascript
const africastalking = require('africastalking')('YOUR_API_USERNAME', 'YOUR_API_KEY');
```

### For PHP
```php
require 'vendor/autoload.php';
use Africastalking\Africastalking;

Africastalking::initialize('YOUR_API_USERNAME', 'YOUR_API_KEY');
```

## Step 5: Testing the SMS Gateway Integration
1. Create a file named `test_sms.js` (Node.js) or `test_sms.php` (PHP) and insert the following code:

### For Node.js
```javascript
const africastalking = require('africastalking')('YOUR_API_USERNAME', 'YOUR_API_KEY');

const sendSMS = () => {
    africastalking.SMS.send({
        to: '+254701234567', // Change to a valid number
        message: 'Hello from Care 4 Animals!'
    }).then(response => {
        console.log(response);
    }).catch(error => {
        console.error(error);
    });
};

sendSMS();
```

### For PHP
```php
use Africastalking\Africastalking;

$recipients = '+254701234567'; // Change to a valid number
$message = 'Hello from Care 4 Animals!';

Africastalking::sendSMS($recipients, $message);
```

2. Run the file to test if the SMS is sent successfully.
 
## Troubleshooting
- Ensure that you have internet access.
- Verify that your API credentials are correct.
- Check the recipients' phone number format.
- Refer to the [Africa's Talking API Documentation](https://africastalking.com/docs) for further assistance.

---

### Conclusion
Following this guide will help you successfully integrate and test the Africa's Talking SMS Gateway in your Care 4 Animals V2 application.