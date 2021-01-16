import sqlite3
from sqlite3 import Error
import time
import uvicorn
from fastapi import FastAPI
from typing import Optional
from fastapi.responses import JSONResponse

app = FastAPI()

database = "sql.db"


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def delete_email(conn, email):
    """
    Delete a task by task id
    :param email:
    :param conn:  Connection to the SQLite database
    :return:
    """
    sql = 'DELETE FROM emails WHERE name=?'
    cur = conn.cursor()
    cur.execute(sql, (email,))
    conn.commit()
    return JSONResponse({'res': 'Email removed'})


def create_email(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO emails(name,time_now)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return JSONResponse({'res': 'Email added'})


def check_email(conn, email):
    all_emails = get_all_emails(conn)
    duplicate = email in all_emails

    if duplicate:
        return JSONResponse({'res': 'Duplicate email'})
    else:
        task = (email, time.time())
        return create_email(conn, task)


def get_all_emails(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM emails")

    emails = cur.fetchall()
    all_emails = []
    print(emails)
    for address in emails:
        all_emails.append(address[0])

    print(all_emails)
    return all_emails


@app.get("/direct-call")
async def direct_call(call_type: str, email: Optional[str] = None):
    # create a database connection
    conn = create_connection(database)

    with conn:
        if call_type == "get_emails":
            emails = get_all_emails(conn)
            return emails

        elif call_type == "duplicate_check":
            res = check_email(conn, email)
            return res

        elif call_type == "remove_email":
            res = delete_email(conn, email)
            return res


def transfer_data():
    with open('../emails.txt', 'r') as f:
        for line in f:
            clean = line.split('\n')[0]
            direct_call('add_email', clean)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
