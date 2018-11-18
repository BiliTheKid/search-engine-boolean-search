# Imports
import pymysql.cursors

# Create DB
def create_db():
    db = pymysql.connect("localhost","root","","projectRet",charset='utf8' )
    cursor = db.cursor()
    # Drop table if it already exist using execute() method.
    cursor.execute("DROP TABLE IF EXISTS Postinglist")
    # Create table as per requirement
    sql_postinglist = """CREATE TABLE Postinglist(
    Term  CHAR(20) NOT NULL,
    DocId int,
   Hits int )"""
    cursor.execute(sql_postinglist)
    db.close()
    create_Doc_file()

# Create doc file
def create_Doc_file():
    db = pymysql.connect("localhost", "root", "", "projectRet",charset='utf8')
    cursor = db.cursor()
    # Drop table if it already exist using execute() method.
    cursor.execute("DROP TABLE IF EXISTS docFile")
    # create docFile
    sql_Doc_file = """CREATE TABLE docFile(
        docId  int,
        Title  CHAR(70) NOT NULL,
        Author  CHAR(50) NOT NULL, 
        Languages  CHAR(50) NOT NULL,
        Brief char(250),
        Location char(255)
        )"""
    cursor.execute(sql_Doc_file)
    db.close()

# Insert to port list
def insert_to_post_list(word_details):
    db = pymysql.connect("localhost", "root", "", "projectRet",charset='utf8')
    cursor = db.cursor()
    cursor.execute('''INSERT into Postinglist (Term,DocId , Hits)
                     values (%s, %s, %s)''', (word_details.w,word_details.n, word_details.h))
    try:
        # Execute the SQL command
        #cursor.execute(sql1)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    db.close()

# Insert to doc list
def insert_to_doc_list(doc_id):
    db = pymysql.connect("localhost", "root", "", "projectRet",charset='utf8')
    cursor = db.cursor()
    cursor.execute('''INSERT into docFile (docId, Title, Author, Languages, Brief, Location)
                     values (%s, %s, %s, %s, %s, %s)''',
                   (doc_id.d, doc_id.title, doc_id.autor, doc_id.language, doc_id.brief, doc_id.location))
    try:
        # Execute the SQL command
        #cursor.execute(sql1)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    db.close()

def sort_ab():
    db = pymysql.connect("localhost", "root", "", "projectRet",charset='utf8')
    cursor = db.cursor()
    alpha_bet='''select * from Postinglist ORDER BY Term'''
    cursor.execute(alpha_bet)
    try:
        # Execute the SQL command
        #cursor.execute(sql1)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    db.close()


##genertae id
def genrate_docId():
    db = pymysql.connect("localhost", "root", "", "projectRet",charset='utf8')

    cursor = db.cursor()
    alpha_bet='''select MAX(docID) from docfile'''
    cursor.execute(alpha_bet)
    data = cursor.fetchall()
    db.close()

    if data is not None:
        print("here:", data[0][0])
        return int(data[0][0])
    else:
        print("not found any")
        return -1

