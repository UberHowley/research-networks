# networks project
This project is to visualize networks of collaborators based on publishing together.

Given a list of researchers, it reads them in, and finds the titles of all their publications from the past 'n' years (author --> publication-titles)

Once each author has all their publications listed, it goes back through _all_ publications found, and creates a mapping of publication-title --> authors.

Once the data is arrange by title-->authors, we go through each publication, and construct a pairing of each of the authors listed. This is then used to construct (author1, author2) --> publication-titles. 

This last mapping is iterated through one last time, and printed as: author1, author2, number-of-publications

## Flaws
* Currently, only works for people who have Google Scholar pages?
* Some pubs don't have a year that is retrievable. What to do with these?

## TODO
* Check that -1 on the iterating through co-author tuple making
* Print out to file name,title (repetitive lines) see: [DataScienceCentral](https://www.datasciencecentral.com/profiles/blogs/some-social-network-analysis-with-python)