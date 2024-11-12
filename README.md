Django eCommerce Website

This project is a fully functional eCommerce website built with Django, featuring a full authentication system (registration, login, and logout), along with essential eCommerce functionalities like product listings, wishlists, shopping carts, and order management. The site includes a user-friendly admin panel to manage products, categories, orders, and customer information.

Features
User Authentication: Registration, login, logout, and password management for secure access.
Product Catalog: Dynamic product listing and categorization.
Wishlist: Save favorite products to a wishlist for future reference.
Shopping Cart: Add, update, or remove items from the cart before checkout.
Order Management: Place orders with address management, review order details, and view order history.
Admin Panel: Manage products, categories, users, and orders from Django’s built-in admin interface.
Technologies Used
Backend: Django (Python)
Frontend: HTML, CSS, JavaScript
Database: SQLite (default) or other Django-supported databases
Authentication: Django's built-in authentication system
Setup Instructions
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
Create a virtual environment:

bash
Copy code
python -m venv env
source env/bin/activate   # On Windows use `env\Scripts\activate`
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run migrations to set up the database:

bash
Copy code
python manage.py migrate
Create a superuser for admin panel access:

bash
Copy code
python manage.py createsuperuser
Start the development server:

bash
Copy code
python manage.py runserver
Access the website and admin panel:

eCommerce Website: Visit https://ourshop.pythonanywhere.com

Project Structure
core: Contains main Django settings and configuration files.
accounts: Manages user authentication (registration, login, and logout).
store: Handles product listings, wishlist, cart, and order management.
models.py: Defines data models for products, categories, wishlist, cart, orders, and addresses.
views.py: Manages the logic for displaying products, handling cart actions, and placing orders.
templates/: Includes HTML templates for different pages, including product listings, cart, checkout, and user profile.
static/: Contains CSS, JavaScript, and images for frontend styling.
Customization
Admin Panel: Use the admin panel to add or update products, categories, and manage orders and customers.
Frontend Design: Modify HTML, CSS, and JavaScript in the templates/ and static/ directories to update the website’s design and branding.
Contributing
Contributions are welcome! Fork the repository and create a pull request to add features or make improvements.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

