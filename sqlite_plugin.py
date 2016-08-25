#! /usr/bin/env python
import sqlite3, sys

def perform_query(query):
    # determine if the query is insert or select
    connection = ''
    try:
        connection = sqlite3.connect('checksum.db')
        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        return cur.fetchone()
        # return cur.fetchone()
    except sqlite3.Error as er:
        raise er
    finally:
        if connection:
            connection.close()


def write_checksum(episode, checksum):
    perform_query("DELETE FROM checksums where episode=%d" % episode)
    query = "INSERT INTO checksums (episode, checksum) VALUES (%d, '%s');" % (episode, checksum)
    perform_query(query)


def read_checksum(episode):
    query = "SELECT checksum FROM checksums WHERE episode=%d LIMIT 1;" % (episode)
    return perform_query(query)[0]

def _delete_entry(episode):
    query = "DELETE FROM checksums where episode=(%d);" % (episode)
    return perform_query(query)

def nuke():
    query = "DELETE FROM checksums"
    return perform_query(query)
