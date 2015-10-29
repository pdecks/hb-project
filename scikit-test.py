"""
Performing NLP using scikit-learn. Supervised machine learning.

by Patricia Decker, 10/28/2015, Hackbright Academy Independent Project

review_dict = {'type': 'review',
               'business_id': rest_name,
               'user_id': 'greyhoundmama',
               'stars': rest_stars,
               'text': review_text,
               'date': yelp_date,
               'votes': vote_dict
               'target': default=None
               }

The classifier will be classifying on review_dict['text'], the review.
target
"""

from sklearn.datasets import base as sk_base
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline

# import reviewfilter as rf


#### LOAD DATA ########################################################

# directory containing toy data set: reviews by pdecks as .txt files
# must be preprocessed with 'preprocess-reviews.py'
container_path = '/Users/pdecks/hackbright/project/Yelp/mvp/pdecks-reviews/'

categories = ['bad', 'excellent', 'good', 'limited', 'neutral', 'shady']

# load the list of files matching the categories
# BEWARE OF LURKING .DS_Store files!! those are not 'utf-8'
# and will throw a UnicodeDecodeError
pdecks_train = sk_base.load_files(container_path,
                                  categories=categories,
                                  encoding='utf-8')
## for un-processed .txt. ##
# # create list of filenames
# filelist = rf.generate_filelist(container_pay)

# # convert .txt review files to list of dictionaries (matches Yelp JSON)
# my_reviews = rf.generate_reviews_dict(filelist)

# for review in my_reviews:
#     print review['business_id']

## end un-processed .txt ##


#### EXTRACTING FEATURES #####

## TOKENIZATION ##
# create an instance of CountVectorize feature extractor
# using ngram_range flage, enable bigrams in addition to single words
count_vect = CountVectorizer(ngram_range=(1, 2))

# extract features from pdecks_train data
X_train_counts = count_vect.fit_transform(pdecks_train.data)

## PART OF SPEECH TAGGING ##

## REMOVING PUNCTUATION ##

## REMOVING STOPWORDS ##

## STEMMING / LEMMATIZATION ##

## FREQUENCY DISTRIBUTIONS ##

## COLLOCATIONS, BIGRAMS, TRIGRAMS ##

## CHUNKING ##


## TF-IDF ##
# create an instance of TfidTransformer that performs both tf & idf
tfidf_transformer = TfidfTransformer()

# transform the pdecks_train features
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)


## SPLITTING TRAINING SETS & TEST SETS ###############################


## DEVELOP CLASSIFIER / PIPELINE ##
# Linear SVC, recommended by sklearn machine learning map
# clf = Classifier().fit(features_matrix, targets_vector)
clf = LinearSVC().fit(X_train_tfidf, pdecks_train.target)

new_doc = ['I love gluten-free foods. This restaurant is the best.']

X_new_counts = count_vect.transform(new_doc)  # transform only, as vectorizer is fit to training data
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

# predict label (target) for new document
predicted = clf.predict(X_new_tfidf)

# retrieve label name
for doc, category in zip(new_doc, predicted):
    print "%r => %s" % (doc, pdecks_train.target_names[category])

## CROSS-VALIDATING CLASSIFIERS ##


## CREATING PIPELINES FOR CLASSIFIERS ##
# Pipeline([(vectorizer), (transformer), (classifier)])
text_clf = Pipeline([('vect', CountVectorizer(ngram_range=(1, 2))),
                     ('tfidf', TfidfTransformer()),
                     ('clf', LinearSVC()),
                     ])

# train the model
text_clf = text_clf.fit(pdecks_train.data, pdecks_train.target)
