import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # no of links in 'page'
    linksN = len(corpus[page])

    # initialize dictionary
    distributions = dict()

    # if no of links is >= 1
    if linksN is not None:
        for p in corpus:
            distributions[p] = (1 - damping_factor) / len(corpus)
        for p in corpus[page]:
            distributions[p] += damping_factor / linksN

    # if page has no links--> assume that it is connected to all pages
    else:
        for p in corpus:
            distributions[p] = 1 / len(corpus)

    return distributions


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initialize dictionary
    distributions = dict()
    for i in corpus:
        distributions[i] = 0

    sample_page = random.choice(list(corpus.keys()))

    for i in range(n):
        sample_dist = transition_model(corpus, sample_page, damping_factor)
        for page in sample_dist:
            distributions[page] = (i * distributions[page] + sample_dist[page]) / (i + 1)
        sample_page = random.choices(list(distributions.keys()), list(distributions.values()), k=1)[0]

    return distributions


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)

    # initialize dictionary
    PR = dict()
    pagesNames = set()
    for i in corpus:
        PR[i] = 1 / N
        pagesNames.add(i)

    while True:

        count = 0

        for page in corpus:
            if corpus[page] == "":
                corpus[page] = pagesNames

            current_PR = PR[page]
            new_PR = (1 - damping_factor) / N
            sigma = 0

            for next_page in corpus:
                if page in corpus[next_page]:
                    sigma+= PR[next_page] / len(corpus[next_page])
            sigma *= damping_factor
            new_PR += sigma
            change = abs(current_PR - new_PR)
            if change <= 0.0005:
                count += 1
            PR[page] = new_PR
        if count == N:
            break

    return PR


if __name__ == "__main__":
    main()
