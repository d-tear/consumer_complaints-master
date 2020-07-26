

# Python 3.7 code for Insight data challenege analyzing consumer complaints

The federal government provides a way for consumers to file complaints against companies regarding different financial products, such as payment problems with a credit card or debt collection tactics. 

This repository contains python code (`./src/consumer_complaints.py`) to generate a single csv file that shows for each financial product and year, the total number of complaints, number of companies receiving a complaint, and the highest percentage of complaints directed at a single company.

Below are the contents of an example `complaints.csv` file: 
```
Date received,Product,Sub-product,Issue,Sub-issue,Consumer complaint narrative,Company public response,Company,State,ZIP code,Tags,Consumer consent provided?,Submitted via,Date sent to company,Company response to consumer,Timely response?,Consumer disputed?,Complaint ID
2019-09-24,Debt collection,I do not know,Attempts to collect debt not owed,Debt is not yours,"transworld systems inc. is trying to collect a debt that is not mine, not owed and is inaccurate.",,TRANSWORLD SYSTEMS INC,FL,335XX,,Consent provided,Web,2019-09-24,Closed with explanation,Yes,N/A,3384392
2019-09-19,"Credit reporting, credit repair services, or other personal consumer reports",Credit reporting,Incorrect information on your report,Information belongs to someone else,,Company has responded to the consumer and the CFPB and chooses not to provide a public response,Experian Information Solutions Inc.,PA,15206,,Consent not provided,Web,2019-09-20,Closed with non-monetary relief,Yes,N/A,3379500
2020-01-06,"Credit reporting, credit repair services, or other personal consumer reports",Credit reporting,Incorrect information on your report,Information belongs to someone else,,,Experian Information Solutions Inc.,CA,92532,,N/A,Email,2020-01-06,In progress,Yes,N/A,3486776
2019-10-24,"Credit reporting, credit repair services, or other personal consumer reports",Credit reporting,Incorrect information on your report,Information belongs to someone else,,Company has responded to the consumer and the CFPB and chooses not to provide a public response,"TRANSUNION INTERMEDIATE HOLDINGS, INC.",CA,925XX,,Other,Web,2019-10-24,Closed with explanation,Yes,N/A,3416481
2019-11-20,"Credit reporting, credit repair services, or other personal consumer reports",Credit reporting,Incorrect information on your report,Account information incorrect,I would like the credit bureau to correct my XXXX XXXX XXXX XXXX balance. My correct balance is XXXX,Company has responded to the consumer and the CFPB and chooses not to provide a public response,"TRANSUNION INTERMEDIATE HOLDINGS, INC.",TX,77004,,Consent provided,Web,2019-11-20,Closed with explanation,Yes,N/A,3444592
```

Assuming you are in the top-level directory of this repository, if the above `complaints.csv` file is located within `./input` ,  a `results.csv` file can be generated inside the `./output` directory with the following command from the linux/macOS terminal:


```shell
#same command is also found inside run.sh
$ python3.7 ./src/consumer_complaints.py ./input/complaints.csv ./output/results.csv
```
Below is the expected contents of `./output/results.csv`

```
"credit reporting, credit repair services, or other personal consumer reports",2019,3,2,67
"credit reporting, credit repair services, or other personal consumer reports",2020,1,1,100
debt collection,2019,1,1,100
```

Although the example complaints.csv file is small, a real dataset may contain hundereds of thousands of lines. To ensure scalability, a stable sort of the columns `Date recieved` and `Product` are first performed on complaints.csv. This initial sorting ensures that the rows are organized by year, and by product name within year, and this allows us to make only one pass over the complaints.csv file to gather our summarized data for each year and product for that year (i.e. once product name changes, we know we've collected all relevant data for that product on that year, and once year changes, we know that we've collected all relevant data for that year). 

To ensure that the final results file is organized alphabetically by product name, a nested list of product info for each year is sorted by product name each time new summarized data is added. Although this leads to a lot of potential sorting, in practice, this approach is fast because the data are already sorted by product name within year. I found this approach approx. 3X faster than doing one large sort by product name at the end, and it required a smaller memory footprint. However, this maintained alphabetical ordering could also likely be achieved with a heap/priority queue structure and future work should explore that approach.

Note that the problem solving code is located in the `generate_report` function inside `consumer_complaints.py`



## Installing / Getting started

This project was written in Python 3.7 (3.7.6 default, Jan  8 2020, 13:42:34) 

Earlier and later versions of Python 3 also likely work, however they haven't been tested.

Note that consumer_complaints.py uses only the built-in/standard libraries. So there is no need to install any third party libraries.

Just ensure you have python 3.7 installed on your machine/server, and clone the repository.

