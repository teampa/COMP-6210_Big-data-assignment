#5. MapReduce Implementation: Implement a MapReduce program using mrjob to calculate the 
#frequency of each <year, company> pair. In other words, determine how many movies were 
#released by each production company for each year.



from mrjob.job import MRJob
from mrjob.step import MRStep

class Year_company_frequency(MRJob):

    def mapper(self, _, line):
        #split on comma and consider first split_parts as year and rest as company
        split_parts = line.strip().split(', ')
        year = split_parts[0]
        company = ', '.join(split_parts[1:])
        yield (year, company), 1

    def reducer(self, key, values):
        #sum the values for each <year, company> pair
        total = sum(values)
        year, company = key
        yield f"{year}, {company}", total

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer)
        ]

if __name__ == '__main__':
    Year_company_frequency.run()

