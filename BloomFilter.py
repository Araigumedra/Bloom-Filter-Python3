import sys
import math
import csv
import mmh3
import numpy

# Bloom filter class with all required params, as well as the list itself


class BloomFilter:
    def __init__(self, input):
        self.probability = 0.0000001
        self.records = generateCountCSV(input)
        self.size = generateFilterSize(self.records, self.probability)
        self.k = generateHashCount(self.records, self.size)
        self.filterList = populateFilter(self.size,
                                         input,
                                         numpy.zeros(self.size, dtype=int),
                                         self.k)

    # Print bloom filter parameters
    def printInfo(self):
        print("n = ", self.records)
        print("p = ", self.probability)
        print("m = ", self.size)
        print("k = ", self.k)

    # Run tester file and generate output
    def runTest(self, test):
        outputList = generateOutputList(self.size,
                                        test,
                                        self.filterList,
                                        self.k)
        generateOutputFile(outputList)


'''
        Filter Helpers
'''


# Calculate how many hash functions are needed
def generateHashCount(records, size):
    return round((size / records) * math.log(2))


# Calculate how large the filter must be
def generateFilterSize(records, prob):
    dividend = records * math.log(prob)
    divisor = math.log(1 / math.pow(2, math.log(2)))
    return math.ceil(dividend / divisor)


'''
        CSV Helpers
'''


# Calculate the number of records in file
def generateCountCSV(input):
    with open(input, newline='') as emails:
        reader = csv.reader(emails)
        count = 0
        try:
            next(reader, None)
            for row in reader:
                count += 1
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(emails, reader.line_num, e))
        finally:
            return count


# Populate the bloom filter with correct bits indexed based on params
def populateFilter(size, input, filterList, hashCount):
    with open(input, newline='') as emails:
        reader = csv.reader(emails)
        result = filterList
        try:
            next(reader, None)  # Skipping headers
            for row in reader:
                for hash in range(1, hashCount):
                    # Utilizing mmh3 function with multiplicative prime
                    result[mmh3.hash128(row[0], hash*6661) % size] = 1
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(emails, reader.line_num, e))
        finally:
            return result


# Generate a list containing the test input with their evaluation
def generateOutputList(size, test, filterList, hashCount):
    with open(test, newline='') as tester:
        reader = csv.reader(tester)
        result = list()
        try:
            next(reader, None)  # Skipping headers
            for row in reader:
                for hash in range(1, hashCount):
                    # If a hash function fails break the loop, append not found
                    if filterList[
                        # Utilizing mmh3 function with multiplicative prime
                        mmh3.hash128(row[0], hash*6661) % size
                    ] != 1:
                        result.append([row[0], "Not in the DB"])
                        break
                # If item is not found continue the reader loop
                if result.count([row[0], "Not in the DB"]) > 0:
                    continue
                # Else append item as found
                else:
                    result.append([row[0], "Probably in the DB"])
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(size, reader.line_num, e))
        finally:
            return result


# Generates output CSV of evaluated tester in "Email", "Result" format
def generateOutputFile(output):
    with open("Results.csv", "w") as out:
        writer = csv.writer(out)
        writer.writerow(["Email", "Result"])
        for row in output:
            writer.writerow(row)


'''
        Main
'''


def main():
    # Read arguments
    input = sys.argv[1]
    test = sys.argv[2]

    # Calculate records and generate filter
    filter = BloomFilter(input)
    filter.printInfo()
    filter.runTest(test)


if __name__ == '__main__':
    main()
