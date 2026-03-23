# 📦 Inventory Management System
A Python CLI program to manage a clothing store inventory. Tracks products, sales, removals, and financial results using PostgreSQL.

--------------------------------------------------------------------------------------------

🛠 Features

- Register products with automatic profit calculation.
- Record sales and update stock automatically.
- Remove products with reason (loss, defect, inventory error) and calculate losses.
- Quick stock lookup and low-stock alerts (<5 units).
- Generate financial reports for a chosen period.
- View tables (stock, sales, removed) in the terminal with pretty tables.

--------------------------------------------------------------------------------------------

📝 Technologies Used

- Python 3.x
- SQLAlchemy (ORM)
- PostgreSQL / psycopg2
- Colorama
- Tabulate
- Datetime
- Custom utility module (fanymodules) for input validation

--------------------------------------------------------------------------------------------

⚙ Setup Instructions

- Clone the repository
- git clone https://github.com/YOUR_USERNAME/inventory_management.git
- cd inventory_management
- Install dependencies
- pip install sqlalchemy psycopg2-binary colorama tabulate
- Configure PostgreSQL
- Update the DATABASE_URL in main.py:
- DATABASE_URL = "postgresql+psycopg2://username:password@localhost:5432/database_name"
- Make sure the PostgreSQL server is running.
- Run the program
- python main.py

--------------------------------------------------------------------------------------------

🧭 How to Use

- Menu Options

Register Product – Add or update products with quantity and prices.
Record Sale – Register a sale, update stock, calculate profit.
Remove Product – Remove items with reason and calculate loss.
Check Stock – Quickly see product availability and low-stock alerts.
Financial Report – Calculate total sales, losses, and profit for a period.
View Tables – Display stock, sales, and removed tables in the terminal.

- Exit Program

--------------------------------------------------------------------------------------------

💡 Notes

- All inputs are validated using the custom fanymodules library.
- Dates must be entered in DD/MM/YYYY format.
- Automatic calculations for profit, loss, and stock updates.
