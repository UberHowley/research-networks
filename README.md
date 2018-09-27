# networks project
This project is to visualize networks of collaborators based on publishing together.

Given a list of researchers, it reads them in, and finds the titles of all their publications from the past 'n' years (author --> publication-titles)

Once each author has all their publications listed, it goes back through _all_ publications found, and creates a mapping of publication-title --> authors.

Once the data is arrange by title-->authors, we go through each publication, and construct a pairing of each of the authors listed. This is then used to construct (author1, author2) --> publication-titles. 

This last mapping is iterated through one last time, and printed as: author1, author2, number-of-publications