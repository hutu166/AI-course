import sqlite3

class SQLiteDB:
    def __init__(self):
        self.connection = None
        self.db_file = 'ai.db'

    def connect(self):
        self.connection = sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.connection.cursor()

    def executescript(self, sql_script_file):
        self.connect()
        with open(sql_script_file) as f:
            self.cursor.executescript(f.read().decode('utf8'))

    # query = 'INSERT INTO restaurant (name, address) VALUES (?,?)'
    # params = ('McDonald', '123 Main St')
    def execute(self, query, params=()):
        self.connect()
        self.cursor.execute(query, params)
        self.connection.commit()
        self.connection.close()

    def fetchall(self, query, params=()):
        self.connect()
        self.cursor.execute(query, params)
        results = self.cursor.fetchall()
        self.connection.close()
        return results

    # query = 'SELECT * FROM restaurant WHERE id = ?'
    # params = (id,)
    def fetchone(self, query, params=()):
        self.connect()
        self.cursor.execute(query, params)
        result = self.cursor.fetchone()
        self.connection.close()
        return result


db = SQLiteDB()


def init_all_tables():
    db.execute('drop table sys_user')
    db.execute('drop table course')
    db.execute('''
    CREATE TABLE IF NOT EXISTS sys_user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        first_name TEXT,
        last_name TEXT,
        role TEXT NOT NULL
    )
    ''')
    db.execute('''
    CREATE TABLE IF NOT EXISTS course (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        lecture_pdf TEXT NOT NULL,
        task_desc TEXT NOT NULL,
        dataset_file TEXT
    )
    ''')
    db.execute('''
    CREATE TABLE IF NOT EXISTS course_completion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        course_id TEXT NOT NULL
    )
    ''')
    db.execute('insert into sys_user (email, password, first_name, last_name, role) values (?,?,?,?,?)',
               ('teacher', '1', 'Jim', 'Lee', 'teacher'))
    db.execute('insert into sys_user (email, password, first_name, last_name, role) values (?,?,?,?,?)',
               ('student', '1', 'Tom', 'Kim', 'student'))
    db.execute('insert into course (name, lecture_pdf, task_desc, dataset_file) values (?,?,?,?)',
               ('Week 1: Data Science Basic', 'compressed.tracemonkey-pldi-09.pdf', '''
    <div>In this task, you will analyze the customer spending behavior of an online retailer. The goal is to discover sales trends based on a customer's purchase data and advise that retailer on strategies to increase sales and customer loyalty. The analysis focuses on the segmentation of customer groups, sales trends of common products, seasonal sales peaks, etc.</div>
    <div>
        <b>Task requirements:</b>
        <li>Customer group segmentation: Based on customer purchase behavior (such as order quantity, order amount, product category, etc.), classify customers to find high-value customer groups.</li>
        <li>Product sales analysis: Identify the best-selling product categories and product names and analyze their sales performance in different seasons or regions.</li>
        <li>Customer loyalty analysis: Analyze the customer's buyback rate (the situation of multiple purchases by the same customer) and make recommendations to improve customer loyalty.</li>
        <li>Trend analysis: Identify sales peaks and troughs in different time periods (e.g., quarters, months) and explain possible causes.</li>
        <li>Payment method analysis: Analyze the use of different payment methods to find the most commonly used payment methods.</li>
    </div>''', 'dataset1.csv'))
    db.execute('insert into course (name, lecture_pdf, task_desc, dataset_file) values (?,?,?,?)',
               ('Week 2: Data Collection and Processing', '', '111', 'dataset1.csv'))
    db.execute('insert into course (name, lecture_pdf, task_desc, dataset_file) values (?,?,?,?)',
               ('Week 3: Exploratory Data Analysis (EDA)', '', '111', 'dataset1.csv'))
    db.execute('insert into course (name, lecture_pdf, task_desc, dataset_file) values (?,?,?,?)',
               ('Week 4: Statistics and Probability Basics', '', '111', 'dataset1.csv'))
    db.execute('insert into course (name, lecture_pdf, task_desc, dataset_file) values (?,?,?,?)',
               ('Week 5: Regression Analysis and Model Evaluation', '', '111', 'dataset1.csv'))
    db.execute('insert into course (name, lecture_pdf, task_desc, dataset_file) values (?,?,?,?)',
               ('Week 6: Classification and Cluster Analysis', '', '111', 'dataset1.csv'))
    db.execute('insert into course (name, lecture_pdf, task_desc, dataset_file) values (?,?,?,?)',
               ('Week 7: Feature Engineering and Data Dimensionality Reduction', '', '111', 'dataset1.csv'))
    db.execute('insert into course (name, lecture_pdf, task_desc, dataset_file) values (?,?,?,?)',
               ('Week 8: Time Series Analysis', '', '111', 'dataset1.csv'))
    db.execute('insert into course (name, lecture_pdf, task_desc, dataset_file) values (?,?,?,?)',
               ('Week 9: Deep Learning Basics', '', '111', 'dataset1.csv'))
    db.execute('insert into course (name, lecture_pdf, task_desc, dataset_file) values (?,?,?,?)',
               ('Week 10: Natural Language Processing (NLP)', '', '111', 'dataset1.csv'))
    db.execute('insert into course (name, lecture_pdf, task_desc, dataset_file) values (?,?,?,?)',
               ('Week 11: Big Data and Distributed Computing', '', '111', 'dataset1.csv'))
    db.execute('insert into course (name, lecture_pdf, task_desc, dataset_file) values (?,?,?,?)',
               ('Week 12: Ethics and Privacy in Data Science', '', '111', 'dataset1.csv'))
# init_all_tables()
