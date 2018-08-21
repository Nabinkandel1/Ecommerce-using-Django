# eCommerce Django Project

## Steps
Steps
1. Requirements Gathering
2. Create Project (django-admin startproject ecommerce)
3. Create App (python manage.py startapp shop)
4. Create Models
5. Add app in settings.py
6. Register app in admin
7. Create migrations (python manage.py makemigrations shop)
8. Migrate (python manage.py migrate)
9. Install dependencies (pip install django-autoslug pillow)


### Installations
- pip install django-autoslug
- pip install pillow


### eCommerce Project Features
- Admin adds the category and products
- Browses all the products and categories
- Search all the products using filters
- Add products in cart
- User can signup and login
- User can chekout product
- User can add review for the product

### System Requirements
1. Categories
	- name
	- slug
	- image
	- description
	- featured
	- active

2. Products
	- name
	- slug
	- image
	- brand
	- shipping
	- description
	- price
	- category
	- featured
	- active
	- created
	- modified

3. Review
	- product
	- user
	- rate
	- review
	- created

4. User
	- username
	- email
	- password
