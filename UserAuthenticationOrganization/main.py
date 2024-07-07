import psycopg2


def main():
    conn = psycopg2.connect('postgres://avnadmin:AVNS_r5oGvveXjdxGHP2c0YE@austin-ahng.f.aivencloud.com:22211/defaultdb?sslmode=require')

    query_sql = 'SELECT VERSION()'

    cur = conn.cursor()
    cur.execute(query_sql)

    version = cur.fetchone()[0]
    print(version)


if __name__ == "__main__":
    main()