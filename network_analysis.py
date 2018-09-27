__author__ = 'iris howley'
__project__ = 'networks'
"""
This module takes in a list of authors (rather, strings) to query
on Google Scholar, finds all their co-authors, and constructs a
network file to be visualized as a social network analysis.

(c) 2018 iris howley
"""
import scholarly

CONST_DELIMITER = "," # for CSV files
CONST_YEAR = 2018
articles = [] # titles of publications we've already considered (no double count)
anonymized = {} # names of authors we're not including in the analysis


def makeList(file_name):
    """ Reads in a list with a search query for Google Scholar on each line.
    This is intended to read in a list of author names, for authors that
    are members of our networks of interest.

    :param file_name: name of CSV file to open, one author name/query per line,
    first column should be the author's name
    :return: list of each author name/query
    """
    lines = [] 
    f = open(file_name)
    for line in f:
        all_cols = line.split(CONST_DELIMITER)
        lines.append(all_cols[0].strip()) # assumes first column is author name
    return lines

def get_coauthors(author_name="Iris Howley", num_years=10):
    """ Given an author's name, find all their co-authors

    :param author_name: the name of the author of interest
    :param num_years: go back how many years?
    :return: a list of all the co-authors
    """
    
    # Retrieve the author's data, fill-in
    search_query = scholarly.search_author(author_name)
    author = next(search_query).fill()
    #print(author)

    # Print the titles of the author's publications
    #print([pub.bib['title'] for pub in author.publications])

    # yes, there's a more python way to do this...
    for pub in author.publications:
        pub.fill()
        
        # check to see if we've already counted this article
        # and ensure it's not too old
        title = pub.bib['title']
        year = pub.bib['year']
        if title not in articles and CONST_YEAR-year <= num_years:
            articles.append(title)
        
            coauthors = pub.bib['author'].split(" and ")
            print(coauthors)
        

def example(author_name="Iris Howley"):
    """
    Example function from the scholarly website.
    'Here’s a quick example demonstrating how to retrieve an author’s 
    profile then retrieve the titles of the papers that cite hermost 
    popular (cited) paper.'

    https://pypi.org/project/scholarly/

    :param author_name: Name of author to p[rint data for
    :return: None
    """
    # Retrieve the author's data, fill-in, and print
    search_query = scholarly.search_author(author_name)
    author = next(search_query).fill()
    print(author)

    # Print the titles of the author's publications
    print([pub.bib['title'] for pub in author.publications])

    # Take a closer look at the first publication
    pub = author.publications[0].fill()
    print(pub)

    # Which papers cited that publication?
    print([citation.bib['title'] for citation in pub.get_citedby()])

if __name__=='__main__':
    """
    This is the main function. This is what is called when the file
    is run as a script (and not as a library or in interactive python)
    """
    #example()
    get_coauthors()
