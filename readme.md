# DocTrees
Python Code to Implement Phonetic and levenshtein distance for text correction as part of our project in 5th semester engineering in Indian Institute of Information Technology, SriCity. 


## Requirements

* [Python](https://www.python.org/)   (3.6.3 tested)
* [NLTK](https://www.nltk.org/) (3.4 tested)
* [Phonetics for Python]( https://pypi.org/project/phonetics/)



## Getting Started

To clone and run this application, you'll need Git,Python,NLTK,Phonetics installed on your computer. I assume you already setup the Django environment on your machine, if not yet, then follow the below steps. From your command line:

### Create a virtual environment
#### Ubuntu
```
$ virtualenv -p python3 .env
```
#### Windows
```
$ python3 -m virtualenv .env
```
### Activate the virtualenv
#### Ubuntu
```
$ source .env/bin/activate
```
#### Windows
```
$ source .env/Scripts/activate
```
### Clone this repository
```
$ git clone https://github.com/preethihena/IR_Project.git
```

### Install the requirements
```
$ pip install -r requirements.txt
```
### Working With Project
Go to main project folder. 
``` 
$ cd IR_Project
```
### Create a Inverted Index
```
$ python inverted_index.py
```
### Search for a query
```
$ python project.py
```

Note: If those commands is not working, please open issue with detailed error messages.
## Contributers

* [Krishna Kumar Dey](https://github.com/krishnadey30)
* [Preethi Hena](https://github.com/preethihena)