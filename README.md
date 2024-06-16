# Mortgage Payment Calculator

A simple Python application to compute loan repayments, allowing users to manipulate interest rates and periods at will.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Features

- Calculate monthly mortgage payments
- Adjust interest rates and loan periods dynamically
- Simple and easy-to-use interface

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/jmmferrao/mortgage_payment.git
    ```
2. Navigate to the project directory:
    ```bash
    cd mortgage_payment
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the main script to start the calculator:
```bash
streamlit run main.py
```
To use the Streamlit interface, follow these steps:

1. Go to the app (https://loansimulation.streamlit.app/)
2. Enter the loan amount (capital).
3. Provide the interest rates (comma-separated if multiple).
4. Provide the loan periods in years (comma-separated if multiple).

The app will validate the inputs and display detailed loan payment information, including:

- Maximum monthly payment
- Total amount charged
- Total interest paid
- Principal repayment evolution
- Interest payment evolution
- Detailed monthly decomposition

## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes and commit them (git commit -am 'Add new feature').
4. Push to the branch (git push origin feature-branch).
5. Create a new Pull Request.
