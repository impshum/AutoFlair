import time
import praw
import sqlite3
from sqlite3 import Error
import configparser


class C:
    W, G, R, P, Y, C = '\033[0m', '\033[92m', '\033[91m', '\033[95m', '\033[93m', '\033[36m'


def db_connect():
    try:
        conn = sqlite3.connect('data.db')
        create_table(conn)
        return conn
    except Error as e:
        print(e)
    return None


def create_table(conn):
    create_table = """CREATE TABLE IF NOT EXISTS autoflair (
                                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        author TEXT NOT NULL,
                                        subreddit TEXT NOT NULL,
                                        level INT NOT NULL
                                        );"""
    conn.execute(create_table)


def insert_row(conn, author, subreddit, test_mode, level):
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM autoflair WHERE author = ? AND subreddit = ?", (author, subreddit))
    query = cur.fetchall()
    if not len(query):
        conn.execute(
            "INSERT INTO autoflair (author, subreddit, level) VALUES (?, ?, ?);", (author, subreddit, level))
    else:
        x = cur.execute(
            "UPDATE autoflair SET level = level + ? WHERE author = ? AND subreddit = ?", (level, author, subreddit))
        level = query[0][3] + level

    if not test_mode:
        conn.commit()
    return str(level)


def main():
    config = configparser.ConfigParser()
    config.read('conf.ini')
    target_subreddit = config['SETTINGS']['target_subreddit']
    points_per_post = int(config['SETTINGS']['points_per_post'])
    test_mode = config['SETTINGS'].getboolean('test_mode')

    tm = ''
    if test_mode:
        tm = f'{C.R}TEST MODE{C.Y}'

    print(f"""{C.Y}
╔═╗╦ ╦╔╦╗╔═╗╔═╗╦  ╔═╗╦╦═╗
╠═╣║ ║ ║ ║ ║╠╣ ║  ╠═╣║╠╦╝ {tm}
╩ ╩╚═╝ ╩ ╚═╝╚  ╩═╝╩ ╩╩╩╚═ {C.C}v1.0 {C.G}impshum{C.W}
    """)

    reddit = praw.Reddit(
        username=config['REDDIT']['reddit_user'],
        password=config['REDDIT']['reddit_pass'],
        client_id=config['REDDIT']['client_id'],
        client_secret=config['REDDIT']['client_secret'],
        user_agent='Autoflair (by u/impshum)'
    )

    flairs = {}
    skip_sections = {'REDDIT', 'SETTINGS'}
    sections = [e for e in config.sections() if e not in skip_sections]
    for section in sections:
        flair_text = config[section]['text']
        flair_class = config[section]['class']
        flairs.update(
            {str(section): {'text': flair_text, 'class': flair_class}})

    conn = db_connect()
    start_time = time.time()
    sub = reddit.subreddit(target_subreddit)

    for submission in sub.stream.submissions():
        if submission.created_utc > start_time:
            author = submission.author.name
            subreddit = submission.subreddit
            saved = submission.saved
            c = C.Y
            f_level = ''

            if not saved:
                new_level = insert_row(conn, str(author), str(subreddit), test_mode, 1)
                f_level = f'p/{new_level}'
                if new_level in flairs:
                    c = C.G
                    if not test_mode:
                        flair_text = flairs[new_level]['text']
                        flair_class = flairs[new_level]['class']
                        sub.flair.set(author, flair_text, css_class=flair_class)
                        submission.save()

            print(f'{c}u/{author} r/{subreddit} {f_level}{C.W}')


if __name__ == '__main__':
    main()
