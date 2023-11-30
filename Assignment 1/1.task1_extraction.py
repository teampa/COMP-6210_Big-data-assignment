import pymongo

connection = pymongo.MongoClient("localhost:27017")
connection.list_database_names()

#To create new db
db = connection['movies']
Movies = db['movies']



#1 Data Retrieval: Access the 'movie -> date' path to obtain the release date. Extract the last four
#characters of the release date to obtain the movie’s release year

#2. Company Identification: Access the 'movie -> companies' path to identify the production 
#companies associated with the movie. Note that a movie may be jointly produced by multiple 
#companies, but for our task, we only need to count the top three production companies. This 
#means that if a movie is produced by five companies, only the first three will be considered.

#3 Data Formatting: Generate a series of pairs for each movie in the following format: <year, 
#company>. This can be achieved by combining the movie's release year (extracted in Step 1) 
#with the names of the top three production companies (identified in Step 2).

year_comp = []
for movie_doc in Movies.find():
    if 'companies' in movie_doc and len(movie_doc['companies']) > 0:
        date = movie_doc.get('date')
        year = date.split()[-1]
    #To iterate over the indices 0, 1, and 2 (or fewer if there are less than three companies)
        for i in range(min(len(movie_doc['companies']), 3)):        
            company_name = movie_doc['companies'][i]["name"]
            year_comp.append((year, company_name))


# 4. Data Storage: Store <year, company> pairs of all movies into a text file. This text file will 
# serve as the input data for the subsequent MapReduce program
# Save the pairs to a text file

with open('year_and_company.txt', 'w') as file:
    for pair in year_comp:
        file.write(f"{pair[0]}, {pair[1]}\n")
































