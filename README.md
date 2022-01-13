# Bloom-Filter-Python3
![](https://media2.giphy.com/media/CzKcxUlqNee8U/giphy.gif?cid=790b76110e35106a964a8b49578bb73c8f9750d2cbae697e&rid=giphy.gif&ct=g)

Bloom Filter implementation written in python3 using mmh3 for hashing. Must be run through command line and the inputs must be passed as arguments in the following order:
* Input: 
  * a single-column records.csv file that works as the database
  * a single-column test.csv file with the desired records to check in the database
* Output:
  * a Results.csv file with a new column indicating the membership of each row to the initial records.csv file

## Example
```python3 BloomFilter.py records.csv test.csv```

