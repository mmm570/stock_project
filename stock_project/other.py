from django.db import connection

def sql(data):   
    with connection.cursor() as cursor:
        command = "SELECT * FROM stocktest where id='{0}' or name='{0}'"
        cursor.execute(command.format(data))
        stock = cursor.fetchone()
        return stock