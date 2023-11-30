from mrjob.job import MRJob
from mrjob.step import MRStep
import re

class Bucket_sort_dsc(MRJob):
    #set bucket_size
    bucket_size = 5  

    def mapper(self, _, line):
        pattern = r'\"(.+?)\"\t(\d+)'
        year_company, count = re.findall(pattern, line)[0]
        
        #find bucket_id for each count by bucket_size 
        bucket_id = int(count) // self.bucket_size
        yield bucket_id, (year_company, int(count))

    def reducer1(self, bucket_id, counts_pairs):
        #sorting by count within each bucket in descending order
        sorted_values = sorted(counts_pairs, key=lambda x: (x[1], x[0]), reverse=True)
        for pair, count in sorted_values:
            #set 'dummy_key' just for set not-real key and put bucket_id into value.
            yield 'dummy_key', (bucket_id, pair, count)
    
    def reducer2(self, _, bucket_data):
        #all data comes with the same dummy_key, it can be sorted by bucket_id in descending order
        sorted_data = sorted(bucket_data, key=lambda x: (x[0], x[2], x[1]), reverse=True)
        
        for bucket_id, pair, count in sorted_data:
            yield pair, count

    def steps(self):
        return [MRStep(mapper=self.mapper, reducer=self.reducer1), 
                       MRStep(reducer=self.reducer2)]

if __name__ == "__main__":
    Bucket_sort_dsc().run()

