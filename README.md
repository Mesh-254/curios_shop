# Curio Shop Ecommerce Application

Welcome to the Curio Shop Ecommerce Application! This application is designed to provide a seamless online shopping experience for unique and rare items. Below you will find detailed information about the application's features, installation instructions, and usage guidelines.

## Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Admin Section](#admin-section)
6. [Contributing](#contributing)
7. [License](#license)

## Features

- **Grid Layout for Items**: The landing page displays all items in a visually appealing grid layout, making it easy for users to browse and find products.
- **Admin Management**: Admins have a dedicated section to manage stock, sales, purchases, and calculate profit margins.
- **User Authentication**: Secure user authentication for both customers and admins.
- **Responsive Design**: The application is fully responsive, ensuring a great user experience on both desktop and mobile devices.

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap, CSS
- **Database**: MySQL
- **Language**: Python

## Installation

### Prerequisites

- Python 3.x
- MySQL
- Flask
- pip (Python package installer)

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/curio-shop.git
   cd curio-shop
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database**:
   - Create a MySQL database named `curio_shop`.
   - Update the `config.py` file with your database credentials.

5. **Initialize the database**:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. **Run the application**:
   ```bash
   flask run
   ```

7. **Access the application**:
   Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage

### Landing Page

The landing page is the heart of the Curio Shop. Here, customers can:

- Browse through a grid of curated items.
- Click on items to view detailed descriptions, prices, and availability.
- Add items to their cart and proceed to checkout.

### User Account

Users can create an account or log in to access personalized features such as:

- Viewing order history.
- Managing shipping addresses.
- Saving items to a wishlist.

## Admin Section

The admin section is accessible only to authenticated admin users. It provides a comprehensive dashboard to manage the store's operations.

### Features

- **Manage Stock**: Add, update, or remove items from the inventory.
- **Sales Tracking**: Monitor sales data and generate reports.
- **Purchases Management**: Track and manage purchases from suppliers.
- **Profit Margin Calculation**: Automatically calculate and analyze profit margins for better financial planning.

### Accessing Admin Section

1. Log in with admin credentials.
2. Navigate to the admin dashboard using the URL `http://127.0.0.1:5000/admin`.

## Contributing

We welcome contributions to enhance the Curio Shop application. To contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
