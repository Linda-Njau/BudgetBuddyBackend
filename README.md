![Logo of the project](https://raw.githubusercontent.com/jehna/readme-best-practices/master/sample-logo.png)

# BUDGET BUDDY
> A budgeting app for recording expenditures in different categories with an automated email system for overspending alerts.

## Table of Contents
  - [Setup Guide](#setup-guide)
    - [Prerequisites](#prerequisites)
    - [Clone the Repository](#clone-the-repository)
    - [Backend Setup](#backend-setup)
    - [Frontend Setup](#frontend-setup)
  - [Configuration](#configuration)
  - [Features](#features)
  - [Contributing](#contributing)
  - [Licensing](#licensing)

## Setup Guide
This section guides you on how to set up Budget Buddy on your own local enivronment.

### Prerequisites
Before setting up Budget Buddy, ensure you have the following installed:
- **Python 3:** Budget Buddy requires Python 3.7 or later. You can download the latest version from [python.org](https://www.python.org/downloads/).

- **Node.js and npm:** Ensure you have Node.js installed. Budget Buddy has been tested with Node.js version 14.0.0 and npm version 6.0.0. You can download the latest version of Node.js from [nodejs.org](https://nodejs.org/en/download/).

- **Poetry:** Budget Buddy uses Poetry for managing Python dependencies. Make sure you have Poetry installed by following the instructions at [python-poetry.org](https://python-poetry.org/docs/#installation).
### Clone the Repository
```shell
git clone git@github.com:Linda-Njau/BudgetBuddy.git
```

### Backend Setup
Navigate into the api folder.
```shell
cd api
```
Install Poetry(if not already installed)
```shell
curl -sSL https://install.python-poetry.org | python3 -
```
Install dependencies
```shell
poetry install
```
Activate the virtual environment created by Poetry
```shell
poetry shell
```
Run the Flask app
```shell
python3 run.py
```
This will start the backend server

### Frontend Setup
Navigate into the client folder.

```shell
cd client
```
Install Node.js dependencies.

```shell
npm install
```
Start the react app.

```shell
npm start
```

## Configuration
To send emails using SendGrid, you need to obtain an API key. Follow these steps to setup your own SendGrid API key:
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
   - Add the following line, replacing `<your_sendgrid_api_key>` with the API key you copied:

     ```plaintext
     SENDGRID_API_KEY=<your_sendgrid_api_key>
     ```
   - Save the file
 - Now you can use the `sendgrid_api_key` variable in your code to authenticate with SendGrid and send emails.
 - 
## Usage
To use BudgetBuddy, follow the following steps:
1. Create an account.
2. Add your exepnditure records by specifying thr amount, date and category.
3. Easily Filter and view your expenditure by month and category.
4. Keep an eye on your email for overspending notifications.
   
## Features
The follwing are the main features offered by BudgetBuddy:
* Automated email notification system whenever spending exceeds a certain threshold.
* Recording expenditure according to different categories.
* Filtering system by month and category

## Contributing
If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.


## Licensing
The code in this project is licensed under MIT license.
