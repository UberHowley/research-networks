__author__ = 'iris howley'
__project__ = 'networks'
"""
This module takes in a list of authors (rather, strings) to query
on Google Scholar, finds all their co-authors, and constructs a
network file to be visualized as a social network analysis.

(c) 2018 iris howley
"""
import scholarly


def makeList(file_name):
    """ Reads in a list with a search query for Google Scholar on each line.
    This is intended to read in a list of author names, for authors that
    are members of our networks of interest.

    :param file_name: name of file to open, one author name/query per line
    :return: list of each author name/query
    """
    lines = [] 
    f = open(file_name)
    for line in f:
        lines.append(line.strip())
    return lines
        

def example(author_name="Iris Howley"):
    """
    Example function from the scholarly website.
    'Here’s a quick example demonstrating how to retrieve an author’s 
    profile then retrieve the titles of the papers that cite his most 
    popular (cited) paper.'

    https://pypi.org/project/scholarly/
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
    #pass # remove this later
    example()