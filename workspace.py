from imdb import Cinemagoer
import pprint
import math
from matplotlib import pyplot as plt
import seaborn as sns
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# nltk.download('vader_lexicon')


def main():
    '''The main function contains calls to each of the functions created along with allowing the user to choose which movie they want to analyze'''
    # call the cinemagoer data
    ia = Cinemagoer()
    # ask the user to insert the movie they want to analyze
    moviename = input("Insert Movie Name: ")
    # search for the movies data
    movie = ia.search_movie(moviename)[0]
    # ovtian the movie review data through the movieID
    movie_reviews = ia.get_movie_reviews(movie.movieID)

    print(reviewhist(movie_reviews))
    print()
    print(
        f"This is the list of ratings given to the movie by reviewers: {ratings(movie_reviews)}")
    plotratings(ratings(movie_reviews))
    print()
    print(
        f"This is a list of the reviewers and what percent of people believed the review was helpful: {helpful_percentage(movie_reviews)}")
    print()
    print(sentimentanalysis(movie_reviews))


def reviewhist(movie_reviews):
    ''' This function takes in a movie reviews list from a movie ID and returns the most unique words with frequencies, sorted 
    in order from most used to least used, that are in its reviews. '''
    # pprint.pprint(movie_reviews['data'])

    # collects each review from using the author name  as the dictionary key and the content as the values
    contentd = {}
    for i in range(len(movie_reviews['data']['reviews'])):
        contentd[movie_reviews["data"]['reviews'][i]['author']
                 ] = movie_reviews['data']['reviews'][i]['content']

    # intializes stopwords list
    f = open('stopwords.txt')
    stopwords = []
    for line in f:
        word = line.strip()
        stopwords.append(word)

    # makes a new list for histogram funciton (unique word counter)
    hist = {}
    # goes through all list of reviews
    for phrase in contentd.values():
        #puts content into a traversable, hashable state, Turns data into sentences
        phrase = tuple(phrase.split())
        #loop through each word in the review
        for word in phrase:
            # makes all words lowercase
            word = (word.lower())
            # makes words to string from list so to be hashable and used in dicitonary
            word = (word.split())
            word = "".join(word)

            # removes all the puntuation from each word
            punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~`'''
            for letter in word:
                if letter in punc:
                    word = word.replace(letter, "")
           
            # this makes sure that none of the words are stopwords ex: "the, and, what, a,""
            if word not in stopwords:
                # makes a list of all unique words and the count of their occurances
                if word not in hist.keys():
                    # counts frequencies or creates unique entries
                    hist[word] = 1
                else:
                    hist[word] += 1

    # sorts the words by count of occurances
    sorted_dict = sorted(hist.items(), key=lambda item: item[1], reverse=True)
    #returns the dicitonary
    return f"The word freuqencies are as follows {sorted_dict}"


def ratings(movie_reviews):
    '''This function takes in a movie reviews dictionary and returns a list of the ratings given by users'''
    # make a dictionary holding the keys as the authors and the ratings as values
    ratingsd = {}
    for i in range(len(movie_reviews['data']['reviews'])):
        ratingsd[movie_reviews["data"]['reviews'][i]['author']
                 ] = movie_reviews['data']['reviews'][i]['rating']
   # make a list of ratings from dictionary
    ratingslist = []
    for value in ratingsd.values():
        ratingslist.append(value)
    # make a final list removing all none types
    finalratings = []
    for rating in ratingslist:
        if rating != None:
            finalratings.append(rating)
    #return the final list of ratings
    return finalratings


def plotratings(ratingslist):
    '''This function plots a list of movie ratings on a histogram'''
    # setting bin edges to kepe constant scale for all movies
    bin_edges = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    # stylistic input
    sns.set()
    # define hist data and bins
    _ = plt.hist(ratingslist, bins=bin_edges)
    # label the axises (i think you spell it like this :^) )
    _ = plt.xlabel('Ratings')
    _ = plt.ylabel('Frequency')
    # display the histogram
    plt.show()


def helpful_percentage(movie_reviews):
    '''This funciton takes in a dictionary of movie reviews from a film and returns a dictionary displaying reviewer username as key and 
    the percentage of their reviews that are helpful (helpful+nonhelpful/total)'''
    votesd = {}
    # create a dictionary use author as the key and create a percentage as the value
    #traverse through the movie reviews
    for i in range(len(movie_reviews['data']['reviews'])):
        # create the function (upvotes/(total votes)) and multiply it by 100 and round to make it easily readable
        #Make the number a string
        rawpercentage = str(round((movie_reviews['data']['reviews'][i]['helpful'] /
                          (movie_reviews['data']['reviews'][i]['helpful'] + movie_reviews['data']['reviews'][i]['not_helpful']))*100))
        #add a percent sign to the percentage number to allow for bette undestanding by user
        percentage = f"{rawpercentage}%"
        #create a  new dictionary with author as key and the percent upvotes as value
        votesd[movie_reviews["data"]['reviews'][i]['author']
               ] = percentage
    #return the finished dictionary
    return (votesd)


def sentimentanalysis(movie_reviews):
    ''' This function take in a dictionary of movie reviews and returns a polarity analysis of each review and the review itself. The polarity analysis displays
    what percent of the review is negative (neg), neutral (neu), and positive (pos).'''
    # create a dictionary with author as a key and review as a value
    contentd = {}
    #traverse through the movie reviews
    for i in range(len(movie_reviews['data']['reviews'])):
        contentd[movie_reviews["data"]['reviews'][i]['author']
                 ] = movie_reviews['data']['reviews'][i]['content']
    # for each review, convert the review into a polarity analysis and return the review and the score given
    #create new dictionary to store polarity scores
    polarityd = {}
    #traverse through values
    for value in contentd.values():
        #apply sentiment analysis
        score = (SentimentIntensityAnalyzer().polarity_scores(value))
        #set the review content as the key and the score as the value
        polarityd[value] = score
    #return final dictionary
    return (polarityd)


if __name__ == "__main__":
    main()
