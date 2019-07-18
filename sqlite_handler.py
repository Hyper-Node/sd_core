from conditional_print import ConditionalPrint
from configuration_handler import ConfigurationHandler

import os
import sqlite3
from sqlite3 import Error


class SQLiteHandler(object):

    def __init__(self):
        config_handler = ConfigurationHandler(first_init=False)

        self.config = config_handler.get_config()
        self.cpr = ConditionalPrint(self.config.PRINT_SQLITE_HANDLER, self.config.PRINT_EXCEPTION_LEVEL,
                                    self.config.PRINT_WARNING_LEVEL, leading_tag=self.__class__.__name__)

        self.cpr.print("init sqlite_handler")

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(db_file)
            self.cpr.print(sqlite3.version)
        except Error as e:
            self.cpr.printex(e)

        return conn

    def create_table(self, conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return: if success in creation return True, otherwise (if exception) return False
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            self.cpr.printex("Exception creating table:", e)
            return False
        return True

    def create_whitelist_table(self, database_path, do_delete_first=False):
        """
        From telegram table take unique values for chat_title and put them in a table to create a whitelist
        user can delete non-wished entries from whitelist then manually
        :param database_path:
        :param do_delete_first:
        :return:
        """

        sql_create_whitelist_table = """CREATE TABLE whitelist_chats AS SELECT distinct chat_title  FROM telegram"""
        # create database and connection object
        conn = self.create_connection(database_path)
        if conn is not None:
            # if configured, delete lemmas table at first
            if do_delete_first:
                conn.execute("DROP TABLE IF EXISTS whitelist_chats")

            # create whitelist table
            self.create_table(conn, sql_create_whitelist_table)
        else:
            self.cpr.printex("Error! cannot create the database connection.")







        return conn

    def create_whitelist_ids_table(self, database_path, do_delete_first=False):
        """
        Create table with necessary message id for whitelisting in table
        :param database_path:
        :param do_delete_first:
        :return:
        """
        sql_create_whitelist_ids = """CREATE TABLE whitelist_ids AS SELECT id FROM telegram WHERE chat_title in whitelist_chats"""

        # create database and connection object

        conn = self.create_connection(database_path)
        if conn is not None:
            # if configured, delete lemmas table at first
            if do_delete_first:
                conn.execute("DROP TABLE IF EXISTS whitelist_ids")

            # create whitelist table
            self.create_table(conn, sql_create_whitelist_ids)
        else:
            self.cpr.printex("Error! cannot create the database connection.")

        return conn

    def create_lemmas_table_at_telegram_database(self, database_path, do_delete_first=False):
        sql_create_lemmas_table = """ CREATE TABLE IF NOT EXISTS lemmas (
                                            id integer PRIMARY KEY,
                                            telegram_id integer,
                                            message text,
                                            pos_tag text,
                                            lemmatized_text text,
                                            FOREIGN KEY(telegram_id) REFERENCES telegram(id)
                                        ); """




        # create database and connection object
        conn = self.create_connection(database_path)
        if conn is not None:
            # if configured, delete lemmas table at first
            if do_delete_first:
                conn.execute("DROP TABLE IF EXISTS lemmas")

            # create lemmas table
            self.create_table(conn, sql_create_lemmas_table)
        else:
            self.cpr.printex("Error! cannot create the database connection.")

        return conn

    def create_pers_adjectives_table_at_telegram_database(self, database_path, do_delete_first=False):
        sql_create_lemmas_table = """ CREATE TABLE IF NOT EXISTS personality_adjectives (
                                            id integer PRIMARY KEY,
                                            page_number integer,
                                            related_column integer,
                                            content text,
                                            content_de text,
                                            translation_de_done integer,
                                            addition text,
                                            is_content_line integer
                                         ); """


        # create database and connection object
        conn = self.create_connection(database_path)
        if conn is not None:
            # if configured, delete lemmas table at first
            if do_delete_first:
                conn.execute("DROP TABLE IF EXISTS personality_adjectives")

            # create lemmas table
            self.create_table(conn, sql_create_lemmas_table)
        else:
            self.cpr.printex("Error! cannot create the database connection.")

        return conn

    def create_telegram_database(self, database_path, do_delete_first=False, do_delete_db_first=False):
        """
        Creates the telegram sqlite database at specified path
        :param database_path: specified path
        :param do_delete_first: delete telegram database first before doing creation steps
        :return: connection object
        """
        sql_create_telegram_table = """ CREATE TABLE IF NOT EXISTS telegram (
                                            id integer PRIMARY KEY,
                                            chat_title text,
                                            type_of_chat text,
                                            current_date text,
                                            timestamp text, 
                                            from_name text, 
                                            message text 
                                        ); """



        # delete database at path if enabled in settings to prevent multi logging the same tables
        if do_delete_db_first:
            if os.path.exists(database_path):
                os.remove(database_path)



        # create database and connection object
        conn = self.create_connection(database_path)

        if do_delete_first:
            conn.execute("DROP TABLE IF EXISTS telegram")

        if conn is not None:
            # open connection
            conn.execute("PRAGMA foreign_keys = ON")  # enable foreign keys explicitly

            # create telegram table
            self.create_table(conn, sql_create_telegram_table)
            # create projects table
            # self.create_table(conn, sql_create_projects_table)
            # create tasks table
            # self.create_table(conn, sql_create_tasks_table)
        else:
            self.cpr.printex("Error! cannot create the database connection.")

        return conn

    def write_data_to_telegram_database(self, conn, chat_title, type_of_chat, current_date, timestamp,
                                        from_name_txt, texts_txt, primary_key_counter):
        cursor = conn.cursor()

        rows = []
        for text in texts_txt:
            my_row = (primary_key_counter, chat_title, type_of_chat, current_date, timestamp, from_name_txt, text)
            rows.append(my_row)
            primary_key_counter += 1

        cursor.executemany('insert into telegram values (?,?,?,?,?,?,?)', rows)
        conn.commit()
        return primary_key_counter

    def write_data_to_lemmas_table(self, conn, message_tuple):
        cursor = conn.cursor()
        cursor.executemany('insert into lemmas values (?,?,?,?,?)', message_tuple)
        conn.commit()


    def write_data_to_personality_adjectives_table(self, conn, message_tuple):
        cursor = conn.cursor()
        cursor.executemany('insert into personality_adjectives values (?,?,?,?,?,?,?,?)', message_tuple)
        conn.commit()
