
malicious_queries = [
    ("192.168.0.10", "SELECT * FROM artists LIMIT 5;", "low"),
    ("192.168.0.11", "SELECT FirstName, LastName FROM customers;", "medium"),
    ("192.168.0.12", "UPDATE customers SET Country = 'Mars';", "high"),
    ("192.168.0.13", "DELETE FROM employees WHERE EmployeeId = 3;", "high"),
    ("192.168.0.14", "INSERT INTO invoices (CustomerId, InvoiceDate, Total) VALUES (1, '2023-01-01', 9999.99);", "high"),
    ("192.168.0.15", "SELECT name FROM sqlite_master WHERE type='table';", "medium"),
    ("10.0.0.1", "SELECT * FROM customers WHERE CustomerId = 1 OR 1=1;", "high"),
    ("10.0.0.2", "SELECT * FROM customers WHERE Email = '' OR '1'='1';", "high"),
    ("10.0.0.3", "'; DROP TABLE employees;--", "high"),
    ("10.0.0.4", "SELECT Name FROM tracks UNION SELECT Password FROM users;", "high"),
    ("10.0.0.5", "SELECT * FROM customers WHERE Email = 'admin@example.com'; WAITFOR DELAY '00:00:10';", "high"),
    ("10.0.0.6", "SELECT sql FROM sqlite_master WHERE tbl_name = 'customers';", "medium"),
    ("10.0.0.7", "SELECT load_extension('malicious_lib');", "high"),
    ("10.0.0.8", "UPDATE invoices SET Total = 0.00;", "high"),
    ("10.0.0.9", "DELETE FROM invoice_items;", "high"),
    ("10.0.0.10", "SELECT * FROM customers WHERE Email = 'admin@example.com' AND 1=CASE WHEN (1=1) THEN 1 ELSE 0 END;", "high"),
]
