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
    global last_names # all last names of interest
    last_names = []
    lines = [] 
    f = open(file_name)
    for line in f:
        all_cols = line.split(CONST_DELIMITER)
        assert(len(all_cols)>0) # if this throws an error, you have a blank line

        # col[0] = Project
        # col[1] = Role
        # col[2] = Name
        # col[3] = Institution at Time of Project
        # col[4] = Current Institution
        # col[5] = Still there?
        lines.append((all_cols[2].strip(), all_cols[4].strip()))

        # pull out the last names
        last_names.append(all_cols[2].strip().split(" ")[-1])

    print("DONE making initial author list.")
    return lines

def is_GoogleScholar(author):
    """ Returns true if the author (tuple, all info used) has
    a Google Scholar page.
    :param author: a tuple with all author info to search with
    :return: True if the author has a Google Scholar page
    """    
    # Retrieve the author's data, fill-in
    search_query = scholarly.search_author(" ".join(author))

    # Search for the author's Google Scholar page
    try:
        cur_author = next(search_query).fill()
    except StopIteration:
        print("WARNING: " + str(author) + " does not have Google Scholar page.")
        return False
    return True

def make_GoogleScholars(author_list):
    """ Goes through author list and checks to see if
    each author has a scholar page or not. Adds to appropriate list
    :param author_list: a list of author tuples
    :return: None
    """
    global no_google_scholar # authors who don't have a GS page
    global google_scholars
    no_google_scholar = []
    google_scholars = []
    
    for author in author_list:
        if is_GoogleScholar(author):
            google_scholars.append(author)
        else:
            no_google_scholar.append(author)
    print("DONE making Google Scholar lists.")            

def print_GoogleScholars(file_name="gs_"+CONST_FNAME.split(".")[0]+".csv"):
    """ Prints a CSV with authors who do/not have Google Scholar pages
    :param author_list: a list of author tuples
    :return: None
    """
    global no_google_scholar # authors who don't have a GS page
    global google_scholars
    
    with open(file_name, 'w') as f:
        f.write("hasGoogleScholar"+CONST_DELIMITER+"Name"+CONST_DELIMITER+"Current Institution"+"\n")
        
        for author in no_google_scholar:
            f.write("N"+CONST_DELIMITER+CONST_DELIMITER.join(author)+"\n")

        for author in google_scholars:
            f.write("Y"+CONST_DELIMITER+CONST_DELIMITER.join(author)+"\n")
    print("DONE outputting Google Scholar Info.")
        

def make_coauthors(author_list):
    """ Helper function for adding pairs of co-authors to the dictionary.
    Goes through all items in a list, and pairs them each with every
    other item in a list (tuple is alphabetical).
    :param author_list: a list of authors to make co-cauthors
    :return: a list of tuples, of all authors paired with each other
    """
    coauthors = []
    for i in range(0, len(author_list)-1): 
        auth1 = author_list[i]
        for j in range(i+1, len(author_list)):
            auth2 = author_list[j]
            coauthors.append(((sorted([auth1, auth2])[0], sorted([auth1, auth2]))[1]))
    return coauthors

def get_articles_by(author=("Iris Howley", "Williams College"), num_years=CONST_NUM_YEARS):
    """ Given an author's name, find all their articles

    :param author: (author's name, insitutitional affiliation) tuple
    :param num_years: go back how many years?
    :return: a list of all the articles by this author
    
    """
    articles = [] # all the author's pub titles in given year range
    global no_google_scholar # authors who don't have a GS page
    
    # Retrieve the author's data, fill-in
    search_query = scholarly.search_author(author[0]+" "+author[1])
    

    try:
        cur_author = next(search_query).fill()
            
        # Construct a dictionary of author --> publications
        for pub in cur_author.publications:
            pub.fill()
            
            # check to see if article is too old
            # TODO: what to do with articles that don't have a year?!
            year = -1
            try:
                year = pub.bib['year']        
                
                if year > 1900 and CONST_YEAR-year <= num_years: # assumes no duplicate titles!
                    title = pub.bib['title']
                    title = title.replace(CONST_DELIMITER, '') # removing commas
                    print("\tAdding: " + author[0] + ": " + title + " ("+str(year)+")")
                    articles.append(title)
                print("DONE get_articles_by(" + author[0] + ")")
                return articles
            except KeyError:
                print("-------------------\n")
                print("ERROR no year available for: " +  pub.bib['title'])
                #print(pub)
                print("-------------------\n")    
    except StopIteration:
        print("WARNING: " + str(author) + " does not have Google Scholar page.")
        no_google_scholar.append(author[0]+CONST_DELIMITER+author[1])
    
        
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
    author_list = make_list(CONST_FNAME)
    ##-------- step-by-step processing
    make_GoogleScholars(author_list)
    print_GoogleScholars()
    print("DONE step-by-step processing.")
    ##--------

    """
    # fill our coauthor-->publications list with empty lists
    for coauth in make_coauthors(author_list):
        coauth_titles[coauth]:[] 
        
    for author in author_list:
        author_pubs[author] = get_articles_by(author)
        print("\tReversing: " + str(author) + " --> " +str(author_pubs[author]))

        for pub in author_pubs[author]:
            # if we haven't seen this title before, add it
            if pub not in pub_authors.keys():
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

    # write to file names of authors who don't have a google scholar profile
    with open("no_google_scholar.txt", 'w') as f:
        for auth in no_google_scholar:
            f.write(auth+"\n")
"""

class Coauthors(object):
    def __init__(self, first=None, second=None):
        """ Creates new Coauthors object by alphabetizing two author names"""
        authors = sorted([first,second])
        
        self.first = authors[0]
        self.second = authors[1]

    def add_publication(pub):
        """ Add a publication to our list of publications """
        if len(self.pubs)<1:
            self.pubs = []
        self.pubs.apend(pub)

    def get_lastname0():
        """ Returns the last name of the first author"""
        return self.first.split()[-1]
    
    def get_lastname1():
        """ Returns the last name of the second author"""
        return self.first.split()[-1]

    def is_in(author):
        """ Returns true if given author is one of the ones in coauthors"""
        return author == self.first or self.second

    def equals(authors):
         return authors.get_lastname0() == self.get_lastname0() and authors.get_lastname1() == self.get_lastname1()
