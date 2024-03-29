# ![Logo of the project](./logo_clear_background.png)
live at: https://budget-buddy-frontend.vercel.app/

 *This repository is dedicated to the Backend. To view Frontend, please click [here](https://github.com/Linda-Njau/BudgetBuddyFrontend)*
 
 A budgeting app designed to track expenses across various in categories with an automated email system for overspending alerts.

## Table of Contents
  - [Setup Guide](#setup-guide)
    - [Prerequisites](#prerequisites)
    - [Clone the Repository](#clone-the-repository)
    - [Backend Setup](#backend-setup)
  - [Configuration](#configuration)
  - [Features](#features)
  - [Usage](#usage)
  - [Api Endpoints](#api-endpoints)
  - [Technologies](#technologies)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [Licensing](#licensing)

## Setup Guide
This section provides step-by-step guidance for setting up Budget Buddy on your local environment.

### Prerequisites
Before setting up Budget Buddy, ensure you have the following installed:
- Budget Buddy requires [Python 3.7](https://www.python.org/downloads/) or later.

- Budget Buddy uses [Poetry](https://python-poetry.org/docs/#installation) for managing Python dependencies.
  
### Clone the Repository
```shell
git clone git@github.com:Linda-Njau/BudgetBuddyBackend.git
```

### Backend Setup
Navigate into the BudgetBuddyBackend folder.

```shell
cd BudgetBuddyBackend
```
Install Poetry if not already installed. 
(*Please note that Poetry should always be installed within a virtual environment*)
```shell
curl -sSL https://install.python-poetry.org | python3 -
```
Install dependencies.
```shell
poetry install
```
Activate the virtual environment created by Poetry.
```shell
poetry shell
```
Run the Flask app
```shell
python3 run.py
```
This will start the backend server.

## Configuration
To access the email notification feature, you need to obtain a SendGrid API key. Follow these steps to set up your own SendGrid API key:
1. **Create a New API Key:**
    - Once logged in, navigate to the [SendGrid Dashboard](https://app.sendgrid.com/).
   - In the left sidebar, click on "Settings" and then select "API Keys."
   - Click the "Create API Key" button.
   - Provide a name for your API key and select the appropriate permissions.
   - Click "Create & View" to generate the API key.

2. **Copy Your API Key:**
   - Copy the generated API key. This key is sensitive information, so handle it with care.

3. **Set Up Environment Variable:**
   - Open the `.env` file in the root of your project.
   - Ensure you add the `.env` file to your .gitignore file.
   - Add the following line, replacing `<your_sendgrid_api_key>` with the API key you copied:

     ```plaintext
     SENDGRID_API_KEY=<your_sendgrid_api_key>
     ```
   - Save the file.
 - Now you can use the `sendgrid_api_key` variable in your code to authenticate with SendGrid and send emails.

## Features
The following are the main features offered by Budget Buddy:
* Automated email notification system whenever spending exceeds a certain threshold.
* Recording expenditure according to different categories.
* Filtering system by month and category.

## Usage
To use BudgetBuddy, follow the following steps:
1. Create an account.
2. Add your expenditure records by specifying the amount, date, and category.
3. Easily Filter and view your expenditure by month and category.
4. Keep an eye on your email for overspending notifications.

## API Endpoints
**Users**
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |
| POST | /users | Sign up a new user account |
| POST | /login | Log in an existing user |
| GET | /users/<int:user_id> | Retrieve a user's data|
| GET | /users | Retrieve all users and their respective data |
| PUT |/users/<int:user_id> | Update all the information of a user |
| PATCH | /users/<int:user_id> | Update select information of a user |
| DELETE | /users/<int:user_id> | Delete a single user |

**Payment Entries**
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |
| POST | /payment_entries| Create a new payment entry |
| GET | /payment_entries/<int:payment_entry_id> | Retrieve data for a specific payment entry |
| GET | /users/<int:user_id>/payment_entries | Retrieve all the payment entries of a specific user|
| PUT | /payment_entries/<int:payment_entry_id> | Update a payment entry's data |
| PATCH |/payment_entries/<int:payment_entry_id> | Update select information of a payment entry |
| DELETE | /payment_entries/<int:payment_entry_id> | Delete a single payment entry |

#### Query Parameters

The `/users/<int:user_id>/payment_entries` endpoint supports the following optional query parameters to filter results:

- **month (int):** Filter payment entries by month (1-12).
- **payment_category (PaymentCategory Enum):** Filter payment entries by category.
- **start_date (date):** Filter payment entries starting from the specified date.
- **end_date (date):** Filter payment entries until the specified date.

Example Usage:
```plaintext
GET /users/123/payment_entries?month=1&payment_category=FOOD&start_date=2023-01-01&end_date=2023-01-31
```
## Testing
 To run Tests:
- Navigate to the root folder

1. To runs all the tests:
```shell
python3 -m unittest discover -v
```

2. To run a specific Test suite:
```shell
python3 -m unittest app.tests.test_user.TestUserEndpoints
```
- Replace "test_user" with the filename and "TestUserEndpoints" with the class name.

3. To run a single test:
```shell
python3 -m unittest app.tests.test_payment_entries.TestPaymentEntriesEndpoints.test_create_payment_entry
```
- Replace "test_payment_entries" with the filename, "TestPaymentEntriesEndpoints" with the class name and "test_create_payment_entry" with the name of the test function.



## Technologies
1. **APScheduler**: In-process task scheduler with Cron-like capabilities.
2. **Flask**: A simple framework for building complex web applications.
3. **Sendgrid**: Email api third-party service.
4. **SQLalchemy**: Database Abstraction Library.
5. **SQLite**: file-based relational database commonly used for testing.


## Contributing
If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.


## Licensing
The code in this project is licensed under MIT license.
