__author__ = 'ihowley'
__project__ = 'networks'
"""
This module takes in a list of authors (rather, strings) to query
on Google Scholar, finds all their co-authors, and constructs a
network file to be visualized as a social network analysis.

(c) 2018 ihowley
"""
import scholarly
import datetime

CONST_DELIMITER = "," # for CSV files
CONST_YEAR = datetime.datetime.now().year
CONST_FNAME = "authors.txt" # filename with author names in first column
CONST_NUM_YEARS = 1 # default number of years to look back


def make_list(file_name=CONST_FNAME):
    """ Reads in a list with a search query for Google Scholar on each line.
    This is intended to read in a list of author names, for authors that
    are members of our networks of interest. First column is author names

    TODO: Handle including institutional affiliation for common names?

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

def get_articles_by(author_name="Iris Howley", num_years=CONST_NUM_YEARS):
    """ Given an author's name, find all their articles

    :param author_name: the name of the author of interest
    :param num_years: go back how many years?
    :return: a list of all the articles by this author
    
    """
    articles = [] # all the author's pub titles in given year range
    
    # Retrieve the author's data, fill-in
    search_query = scholarly.search_author(author_name)
    author = next(search_query).fill()
    
    # Construct a dictionary of author --> publications
    for pub in author.publications:
        pub.fill()
        
        # check to see if article is too old
        year = -1
        try:
            year = pub.bib['year']
        except KeyError:
            print("-------------------\n")
            print("ERROR no year available for: " +  pub.bib['title'])
            #print(pub)
            print("-------------------\n")            
            
        if year > 1900 and CONST_YEAR-year <= num_years: # assumes no duplicate titles!
            title = pub.bib['title']
            title = title.replace(CONST_DELIMITER, '') # removing commas
            print("\tAdding: " + author_name + ": " + title + " ("+str(year)+")")
            articles.append(title)
    print("DONE get_articles_by(" + author_name + ")")
    return articles

        
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

    # authors = pub.bib['author'].split(" and ")

    # Take a closer look at the first publication
    pub = author.publications[0].fill()
    print(pub)

    # Which papers cited that publication?
    print([citation.bib['title'] for citation in pub.get_citedby()])

def test():
    author_pubs["Alpha Beta"] = ["Paper 1", "Paper 2", "Paper 3"]
    author_pubs["Kappa Delta"] = ["Paper 2", "Paper 5", "Paper 3", "Paper 4"]
    
    for author in author_pubs:
        print("\tReversing: " + author + " --> " +str(author_pubs[author]))
        for value in author_pubs[author]:
            # if we haven't seen this title before, add it
            if value not in pub_authors.keys():
                pub_authors[value] = []
                print("\tAdding new pub: " + value)
            pub_authors[value].append(author) # add the author to this pub
    print("DONE constructing publication --> authors")

    # construct (auth1, auth2) --> [title1, title2, title3...]
    for pub in pub_authors:
        author_list = pub_authors[pub]
        for i in range(0, len(author_list)-1): # TODO -1?
            auth1 = author_list[i]
            for j in range(i+1, len(author_list)):
                auth2 = author_list[j]
                coauthors = (sorted([auth1, auth2])[0], sorted([auth1, auth2])[1])
                # if we haven't seen this author pairing, add it
                if coauthors not in coauth_titles.keys():
                    coauth_titles[coauthors] = []
                    print("\tAdding new coauthors: " + str(coauthors))
                # add the pub title to this author pairing
                coauth_titles[coauthors].append(pub)
    print("DONE constructing auth1,auth2 --> publications")
    
    # go back through coauth_titles and print author1, author2, num_pubs
    o_fname = CONST_FNAME.split(".")[0] + "-coauthors" + ".txt"
    with open(o_fname, 'w') as f:
        for auths in coauth_titles:
            f.write(CONST_DELIMITER.join([auths[0],auths[1],str(len(coauth_titles[auths]))])+"\n")


if __name__=='__main__':
    """
    This is the main function. This is what is called when the file
    is run as a script (and not as a library or in interactive python)
    """
    #example()
    
    author_pubs = {} # author --> publications
    pub_authors = {} # publications --> authors
    coauth_titles = {} # (auth1, auth2) --> [title1, title2, title3...]

    #test()

    for author in make_list(CONST_FNAME):
        print("\tReversing: " + author + " --> " +str(author_pubs[author]))
        for value in author_pubs[author]:
            # if we haven't seen this title before, add it
            if value not in pub_authors.keys():
                pub_authors[value] = []
                print("\tAdding new pub: " + value)
            pub_authors[value].append(author) # add the author to this pub
    print("DONE constructing publication --> authors")

    # construct (auth1, auth2) --> [title1, title2, title3...]
    for pub in pub_authors:
        author_list = pub_authors[pub]
        for i in range(0, len(author_list)-1): # TODO -1?
            auth1 = author_list[i]
            for j in range(i+1, len(author_list)):
                auth2 = author_list[j]
                coauthors = (sorted([auth1, auth2])[0], sorted([auth1, auth2])[1])
                # if we haven't seen this author pairing, add it
                if coauthors not in coauth_titles.keys():
                    coauth_titles[coauthors] = []
                    print("\tAdding new coauthors: " + str(coauthors))
                # add the pub title to this author pairing
                coauth_titles[coauthors].append(pub)
    print("DONE constructing auth1,auth2 --> publications")
    
    # go back through coauth_titles and print author1, author2, num_pubs
    o_fname = CONST_FNAME.split(".")[0] + "-coauthors" + ".txt"
    with open(o_fname, 'w') as f:
        for auths in coauth_titles:
            f.write(CONST_DELIMITER.join([auths[0],auths[1],str(len(coauth_titles[auths]))])+"\n")
