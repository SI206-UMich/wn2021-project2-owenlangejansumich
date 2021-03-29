from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """

    current_dir = os.path.dirname(__file__)
    full_filename = os.path.join(current_dir, filename)

    with open(full_filename, 'r') as fh:
        file_text = fh.read()

    soup = BeautifulSoup(file_text, 'html.parser')
    soup = soup.find('html')

    tr_tags = soup.find('table', class_ = "tableList").find('tbody').find_all('tr', recursive = False)
    book_titles = [tr.find_all('td')[1].find('a').find('span').text.strip('\n') for tr in tr_tags]
    authors = [tr.find_all('td')[1].find('a', class_ = "authorName").text.strip('\n') for tr in tr_tags]

    return list(zip(book_titles, authors))


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    tr_tags = soup.find('table', class_ = "tableList").find_all('tr', recursive = False)
    base_url = "https://www.goodreads.com"
    urls = [base_url + tr.find_all('td')[1].find('a').get('href') for tr in tr_tags]
    return urls


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """

    r = requests.get(book_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    book_title = soup.find(id = "bookTitle").text.strip()
    author_name = soup.find(id = "bookAuthors").find('span', itemprop = "author").find('a', class_ = "authorName").text.strip()
    
    reg_exp = r'\b(\d+) pages\b'
    page_number_matches = [int(i) for i in re.findall(reg_exp, soup.find(id = "details").text)]

    if len(page_number_matches) != 1 and len(page_number_matches) != 0:
        raise Exception("Could not find accurate page number count")
    if len(page_number_matches) == 1:
        page_number = page_number_matches[0]
    else:
        page_number = None

    return (book_title, author_name, page_number)


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    
    current_dir = os.path.dirname(__file__)
    full_filename = os.path.join(current_dir, filepath)

    with open(full_filename, 'r', encoding='utf8') as fh:
        file_text = fh.read()

    soup = BeautifulSoup(file_text, 'html.parser')
    soup = soup.find('html')

    div_books = soup.find(id = 'categories').find_all('div', class_ = "category clearFix")

    categories = [div.find('a').text.strip() for div in div_books]
    book_titles = [div.find('img').get('alt').strip() for div in div_books]
    urls = [div.find('a').get('href').strip() for div in div_books]

    return_list = []

    for cat, book, url in zip(categories, book_titles, urls):
        return_list.append((cat, book, url))
    
    return return_list

def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    with open(filename, 'w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
        writer.writerow(['Book title', 'Author Name'])

        for row in data:
            writer.writerow(list(row))

def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    current_dir = os.path.dirname(__file__)
    full_filename = os.path.join(current_dir, filepath)

    with open(full_filename, 'r', encoding='utf8') as fh:
        file_text = fh.read()

    soup = BeautifulSoup(file_text, 'html.parser')
    description = soup.find(id = "description")
    description = description.find_all('span')[1].text

    reg_exp = "(?:[A-Z][a-z]{2,})(?: [A-Z][a-z]*)+"
    
    return re.findall(reg_exp, description)

class TestCases(unittest.TestCase):
    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        book_and_titles = get_titles_from_search_results("search_results.htm")

        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(book_and_titles), 20)

        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(book_and_titles), list)

        # check that each item in the list is a tuple
        for item in book_and_titles:
            self.assertEqual(type(item), tuple)

        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(book_and_titles[0], ('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'))

        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(book_and_titles[-1], ('Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'))

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(type(TestCases.search_urls), list)

        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 20)

        # check that each URL in the TestCases.search_urls is a string
        for item in TestCases.search_urls:
            self.assertEqual(type(item), str)

        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for item in TestCases.search_urls:
            self.assertTrue(item.startswith('https://www.goodreads.com/book/show/'))


    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        summaries = []

        
        # for each URL in TestCases.search_urls (should be a list of tuples)
        for url in TestCases.search_urls:
            summaries.append(get_book_summary(url))
        
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 20)
            
        for summary in summaries:
            # check that each item in the list is a tuple
            self.assertEqual(type(summary), tuple)
        
        for summary in summaries:
            # check that each tuple has 3 elements
            self.assertEqual(len(summary), 3)
        
        for summary in summaries:
            # check that the first two elements in the tuple are string
            self.assertEqual(type(summary[0]), str)
            self.assertEqual(type(summary[1]), str)
        
        for summary in summaries:
            # check that the third element in the tuple, i.e. pages is an int
            self.assertTrue(summary[2] is None or type(summary[2]) == int)

        # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2], 337)


    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        s = summarize_best_books("best_books_2020.htm")

        # check that we have the right number of best books (20)
        self.assertEqual(len(s), 20)

        for item in s:
            # assert each item in the list of best books is a tuple
            self.assertEqual(type(item), tuple)

            # check that each tuple has a length of 3
            self.assertEqual(len(item), 3)

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(s[0], ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))

        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(s[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))


    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        s = get_titles_from_search_results("search_results.htm")

        # call write csv on the variable you saved and 'test.csv'
        write_csv(s, 'test.csv')

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        with open('test.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            csv_lines = []
            for row in csv_reader:
                csv_lines.append(row)

        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)

        # check that the header row is correct
        self.assertEqual(csv_lines[0], ['Book title', 'Author Name'])

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1], ['Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'])

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_lines[-1], ['Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'])



if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



