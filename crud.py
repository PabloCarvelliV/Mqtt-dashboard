import sqlite3

class Crud():

    db_name = "bdmqtt-dashboar.db"

    def __init__(self):
        pass

    def run_query(self, query, parameters = ()):

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def add_broker(self, hostName, ip, port):
        query = "INSERT INTO brokers VALUES(?,?,?)"
        parameters = (hostName, ip, port)
        self.run_query(query, parameters)
    
    def edit_records(self, newHostName, oldHostName, newIp, oldIp, newPort, oldPort):
        query = "UPDATE brokers SET hostName = ?, ip = ?, port = ? WHERE hostName = ? AND ip = ? AND port = ?"
        parameters = (newHostName, newIp, newPort, oldHostName, oldIp, oldPort)
        self.run_query(query, parameters)