#!/usr/bin/env python

import os
import sys
import json
import sqlite3
import argparse
import random

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d



class ParksDB(object):
    #A connection to the parks database
      
    def __init__(self, data_dir):
        
        self.db_file = os.path.join(data_dir, "parks.db")
        self.data_file = os.path.join(data_dir, "parks.json")
        self.fact_file = os.path.join(data_dir, "facts.txt")

        self.conn     = sqlite3.connect(self.db_file)
        self.conn.row_factory = dict_factory
        self.conn.text_factory = str
        self.conn.execute('PRAGMA foreign_keys = ON')
       
        self._create_table()
        self._populate_table()

    def _create_table(self):
        #Create the new tables

        cur = self.conn.cursor()

        cur.execute('''
        DROP TABLE IF EXISTS Park
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS Park (
                park_id  INTEGER PRIMARY KEY,
                name     TEXT,
                state    TEXT,
                date     TEXT,
                area     TEXT,
                visitors TEXT,
                descrip  TEXT,
                url      TEXT,
                page     TEXT
            )
        ''')

        cur.execute('''
        DROP TABLE IF EXISTS Fact
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS Fact (
                park_id  INTEGER PRIMARY KEY,
                fact     TEXT
            )
        ''')

    def _populate_table(self):
        #Populate the table from the json file

        cur = self.conn.cursor()

        insert_sql = '''
        INSERT INTO Park VALUES (NULL, :name, :state, :date, :area, :visitors, :descrip, :url, :page)
        '''
    
        with open(self.data_file) as fh:
            data = json.load(fh)
            for rec in data:
                cur.execute(insert_sql, rec)

        insert_sql = '''
        INSERT INTO Fact VALUES (NULL, ?)
        '''

        with open(self.fact_file) as fh:
            for line in fh:
                cur.execute(insert_sql, (line,))

        self.conn.commit()

    def search(self, park_name, state):
        #Return parks matching name criteria

        cur = self.conn.cursor()

        sql_query = '''
        SELECT 
            *
        FROM 
            Park
        WHERE
            name LIKE ? AND
            state LIKE ?
        '''
        
        cur.execute(sql_query, (park_name, state))
        result = cur.fetchall()
        return result

    def detail(self, park_id):
        #Return one row based on exact match of park_id

        cur = self.conn.cursor()

        sql_query = '''
        SELECT 
            *
        FROM 
            Park
        WHERE
            park_id == ?
        '''
        
        cur.execute(sql_query, (park_id,))
        result = cur.fetchone()
        return result

    def states(self):
        #Get possible values for the state field

        cur = self.conn.cursor()

        sql_query = '''
        SELECT DISTINCT
            state
        FROM
            Park
        '''

        states = []

        cur.execute(sql_query)
        result = cur.fetchall()

        for state in result:
            states.append(state['state'])

        return sorted(states)

    def random_fact(self):
        #Return random fact

        cur = self.conn.cursor()

        sql_query = '''
        SELECT
            fact
        FROM
            Fact
        '''

        cur.execute(sql_query)

        row = random.choice(cur.fetchall())

        return row['fact']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = 'test the ParksDB interface'
    )
    args = parser.parse_args()
    db = ParksDB('data')
    
    print json.dumps(db.search('Acadia','%'), indent=1)
    print db.random_fact()