import psycopg2

conn = psycopg2.connect(
    dbname='subsidie',
    user='stan',
    password='g9jflc1mtXF7H0q2IFF',
    host='cg1.postgres.database.azure.com',
    port='5432'
)

cur = conn.cursor()

cur.execute('SELECT 1;')

print("Succesvol verbonden met de database.")

cur.close()


