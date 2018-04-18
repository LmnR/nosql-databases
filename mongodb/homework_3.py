# Jin Peng
# jjp2172

import pprint
import pymongo
from pymongo import MongoClient

# database name is 'db'
# collection name is 'movies'
client = MongoClient()
database = client.db
movies = database.movies

# A
movies.update({'rated':'NOT RATED'}, {'$set': {'rated': 'Pending rating'}}, multi=True)
pprint.pprint('number of movies updated: ' + str(movies.find({'rated':'Pending rating'}).count()))

# B
if not list(movies.find({'title': 'Silicon Valley'})):
	movies.insert_one({'title': 'Silicon Valley', 'year': 2014, 'countries': ['USA'], 'genres': ['Comedy'], 'directors': ['Mike Judge', 'Alec Berg', 'Jamie Babbit', 'Eric Appel', 'Charlie McDowell', 'Tricia Brock', 'Maggie Carey', 'Tim Roche', 'Clay Tarver', 'Gillian Robespierre'], 'imdb': {'id': 789, 'rating': 8.6, 'votes': 89658}})

# C
pipeline_c = [{'$unwind': '$genres'}, {'$group': {'_id': '$genres', 'count': {'$sum': 1}}}, {'$match': {'_id': 'Comedy'}}]
pprint.pprint(list(movies.aggregate(pipeline_c)))

# D
pipeline_d = [{'$unwind': '$countries'}, {'$group': {'_id': { 'country': '$countries', 'rated': '$rated'}, 'count': {'$sum': 1}}}, {'$match': {'_id': { 'country': 'Australia', 'rated': 'Pending rating'}}}]
pprint.pprint(list(movies.aggregate(pipeline_d)))

# E
films = database.films
# films.insert_one({'title2': 'Silicon Valley', 'data': 'test 1'})
# films.insert_one({'title2': 'Silicon Valley', 'data': 'test 2'})
pipeline_e = [{'$lookup': {'from': 'films', 'localField': 'title', 'foreignField': 'title2', 'as': 'new'}}]
count = 0
for d in movies.aggregate(pipeline_e):
	if count > 2:
		break
	pprint.pprint(d)
	count += 1