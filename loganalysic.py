#!/usr/bin/env python3
# fullstacknanodegreeproject
# number-3

# import postgresql library
import psycopg2

from datetime import date
# Connect to the database and feed query to extract results


lover = ('-', 'views', '%', 'errors', '--')


def get_output(data):
    try:
        db = psycopg2.connect("dbname = news")
        a = db.cursor()
        a.execute(data)
        anu = a.fetchall()
        db.close()
        return anu
    except BaseException:
        print("Unable to connect database")
ques_1 = "What are the most popular articles of all time?"

articles = ("SELECT title, count(*) as views FROM articles \n"
            "join log\n"
            "on articles.slug = substring(log.path, 10)\n"
            "group by title ORDER BY views DESC LIMIT 3;")

ques_2 = "Who are the most popular article authors of all time?"

authors = ("select authors.name, count(*) as views\n"
           "from articles \n"
           "join authors\n"
           "on articles.author = authors.id \n"
           "join log \n"
           "on articles.slug = substring(log.path, 10)\n"
           "where log.status LIKE '200 OK'\n"
           "group by authors.name ORDER BY views DESC;")

ques_3 = "On which days more than 1% of the requests led to error?"

errors = """
           select * from (
           select a.day,
           round(cast((100*b.hits) as numeric) / cast(a.hits as numeric), 2)
           as errp from
           (select date(time) as day, count(*) as hits
           from log group by day) as a
           inner join
           (select date(time) as day, count(*) as hits from log where status
           not like '200 OK' group by day) as b
           on a.day = b.day)
           as t where errp > 1.0
           """

l = get_output(articles)
v = get_output(authors)
r = get_output(errors)

# Create a function to print query results


def print_solution(c):
    for i in range(len(c)):
        print("%s - %d" % (c[i][0], c[i][1]) + lover[1])
    print("\n")

print(ques_1)
print_solution(l)
print(ques_2)
print_solution(v)
print(ques_3)


def errors_percentage():
    for i, j in r:
        print "{:%B %d, %Y}".format(i), lover[4], j, lover[2], lover[3]

if __name__ == '__main__':
    errors_percentage()
