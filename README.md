# platepal

Project Motivation
------------------

Speaking from personal experience, it can be difficult to dine out
safely when you have a special dietary need. As someone who cannot eat
gluten, I must be careful about where I eat. I was motivated to create
PlatePal to make it easier for people like myself to make dining
decisions.

PlatePal is designed to complement exisiting sites like Yelp by
providing a sentiment score for a restaurant review, evaluating it for
a relevant dietary category on a scale of 0 to 1, where 0 is bad and 1
is good. The scores are generated by performing sentiment analysis on
relevant sentences in reviews containing keywords in the categories.
Currently, PlatePal scores restaurants for the following categories:
Gluten-Free, Vegan, Kosher, Allergy, and Paleo.



Project Objectives
------------------

Being able to perform the sentiment analysis involved the following:

+ Find a large dataset containing relevant restaurant reviews.
+ Seed this information into a database.
+ Build a document classifier to be able to categorize reviews.
+ Build a sentiment analysis classifier to be able to score reviews.
+ Calculate aggregate scores for businesses.
+ Present the information in an intuitive, user-friendly format.

... easier said than done!



Wrangling Data
--------------

Good data is hard to find, but for my learning purposes, the [Yelp Academic Dataset](https://www.yelp.com/academic_dataset) was a great place to start. The dataset contains
more than 200,000 reviews for businesses clustered around 30
universities. Even though the dataset contains reviews of many kinds
of businesses, not just restaurants, a cursory review of the data
indicated that there were enough relevant reviews to explore my
project's concept. In addition to reviews, the dataset also contains
business and user information.

**Querying the Database: finding relevant reviews.**
![sql_queries_light](https://cloud.githubusercontent.com/assets/1440268/11493714/352b6b0a-97b0-11e5-8579-3886f73dec1a.png)




Working up to Big Data
----------------------

Admittedly, the Yelp dataset was a bit intimidating. The first time I
tried to load the JSON, the reviews dataset caused my computer to
crash. I anticipated that working with such a large dataset would be
part of the challenge with my project, so I devised a plan to test out
my components and concepts on smaller datasets and scale up after
successful testing.



Tricia's Plan for Data Sanity
-----------------------------


+ Use set of 45 personal reviews to test concepts.

    + Create helper functions and scripts to update and sort the reviews.

+ Load the Yelp Academic Dataset JSON into a database

    + Construct a data model with the flexibility to incorporate data from
      other sources.

+ Use a subset of the relevant Yelp reviews stored as txt files.

    + Automate generation of subset files and directories.
    + Model the subset directories to allow for use of sklearn's load
      module.

+ Classify documents in the entire dataset in the database.
+ Use all reviews in the database ... success!




Data Challenges
---------------

Although there was a large amount of relevant data in the datset, it
was not labeled, as least not in a way that I needed it to be. There
were two labels that I needed my data to have, as I was essentially
classifying each review twice:

+ Categorize the review for a dietary need (e.g. "vegan", "unknown").
+ Score the "goodness" of the review for each relevant dietary need.

**Outlining my Text Processing Process**
![classify_score](https://cloud.githubusercontent.com/assets/1440268/11493686/1429cfbe-97b0-11e5-926d-7118b24b1cf6.jpg)

Categorizing Reviews
--------------------

To get around hand-labeling reviews in the dataset -- ain't nobody got
time for that! -- I created helper functions to find reviews
containing simple keywords (e.g., 'gluten-free', 'vegan', 'paleo')
then labeled those reviews as belonging to the appropriate category.



Scoring "Goodness"
------------------

It was more difficult to label data for the sentiment analysis
classifier, especially because the number of relevant reviews for most
of the categories was quite small. I would need 1,000s of reviews to
adequately train a sentiment analysis classifier for each category. As
a first pass, I tried using the Yelp star ratings as a predicator of
goodness, although this violated my fundamental assumption that a
review could be good overall but bad for a particular dietary need, or
vice versa.



Initial Database Model: Businesses, Reviews, Users, and Categories
------------------------------------------------------------------



The goals:

+ Import the Yelp Academic Dataset JSON for businesses, reviews, and
   users.
    + These tables should be isolated from PlatePal tables and will not be updated.
+ Create PlatePal tables for businesses, reviews, and users.
    + These tables will be updated and should be able to store information from multiple sources.
+ Create tables for categorization
+ Create tables for sentiment analysis.
+ Nice to have: tables for users to create lists of their favorite
   restaurants by category.

**First Pass at a Data Model.** Things get much more complicated.
![img_4563](https://cloud.githubusercontent.com/assets/1440268/11493691/1b23c6f8-97b0-11e5-81ec-0ffe1010aa32.JPG)

Yelp Businesses, Reviews, and Users Tables
------------------------------------------

The reviews table serves as an associate table between businesses and
users, as a user can have many reviews and a business can have many
reviews.

There was some information contained in these tables that was beyond
the scope of this project, namely the votes associated with a review,
the neighborhoods associated with a business, and the universities
(schools) associated with a business. When whiteboarding to map out my
model, I included the tables as an exercise in association.



PlatePal Businesses, Reviews, and Users Tables
----------------------------------------------

Similar to the Yelp tables, the PlatePal Reviews (reviews) table is an
association table between users and businesses.

To allow for reference back to the Yelp tables, the PlatePal
Businesses table (biz) includes a field for the Yelp business ID.
Simiarly, the reviews table includes fields for Yelp Review ID, Yelp
stars, and Yelp User ID. The PlatePal Users table (users) does NOT
include a field for Yelp User ID because, after some consideration, I
decided against automatically rolling Yelp users into the PlatePal
system. The disadvantage with that choice is that Yelp users who sign
up for PlatePal would not be able to manually score their own reviews
imported from Yelp. However, because the Yelp Users table includes a
name but not an email, there was not a clear way to verify users'
identities.



Classification Tables
---------------------

It became clear rather early on that creating a separate Categories
table would be useful to allow for expansion of the categories
considered on the site.

The Classification table, ReviewCategories, is an association table
between reviews and categories, as a review can have many categories
and a category can have many reviews.



User-Generated Lists Tables
---------------------------

A user can generate many category-specific lists, and a list can
contain many entries, hence the one to many relationship from users to
lists to list entries.



Revised Data Model: Sentiment Analysis
--------------------------------------



The goals:
----------


1. Allow for sentiment analysis on a review-text level.

    + Business scores should be calculable by compiling review scores.

2. Allow for sentiment analysis on a sentence-text level.

    + Compare review-level scores to sentence-level scores.





RevCats and SentCats
--------------------

From the first draft of my data model, I recognized that I needed an
association table between reviews and classifications,
ReviewCategories (aka RevCats).

Similarly, once I stored all of the sentences associated with a review
in the Sentences table, there should be an association table between
Sentences and Categories, SentenceCategories (aka SentCats).

I debated whether or not to indirectly link SentCats to RevCats
through another table, ReviewSents, but decided against this
additional complication for the sake of clarity.

**Tables for Sentiment Analysis.** Many-to-many Relationships Galore!
![img_4602](https://cloud.githubusercontent.com/assets/1440268/11493692/1b3bf57a-97b0-11e5-9255-95e0502b1e78.JPG)


Text Classification
-------------------

Bag of Words (BOW), which is a non-deep learning method, 
[often out-performs other more complicated models]( https://www.kaggle.com/c/word2vec-nlp-tutorial/details/part-4-comparing-deep-and-non-deep-learning-methods), especially where resources
are limited. Therefore, I initially set out to build a BOW classifier.

If time allowed, I planned to explore distributed word vector
techniques, like Google's word2vec algorithm, that are part of deep
learning methods. Distributed word vector techinuqes are unsupervised
but [require much more data](https://www.kaggle.com/c/word2vec-nlp-tutorial/details/part-2-word-vectors) than BOW to make predictions more
accurate than BOW.

Also of note from my research on text classification is that [recent work out of Stanford](http://nlp.stanford.edu/sentiment/) has applied deep learning to sentiment analysis
using sentence parsing and a Paragraph Vector algorithm, which
preserves word-order information.

**Armadanno Supervising my Supervised Learning**
![Armadanno](https://cloud.githubusercontent.com/assets/1440268/11493684/1080d632-97b0-11e5-8f7e-b5bf6717269c.jpg)


Warming Up for Scikit-Learn: Buidling a Naive Classifier from Scratch
---------------------------------------------------------------------

As I initially explored the problem of text classification, I first
worked through document classification algorithms described in
"Programming Collective Intelligence" by Toby Segaram. Chapter 6 of
that book, "Document Filtering", provides a walkthrough of document
classification through the lens of filtering spam emails.

This book instructs the reader on the following:

+ Extracting features using regular expressions to break text on any
  character that isn't a letter.
+ Representing the classifier using a class, allowing for
  instantiation of multiple classifiers for different purposes.
+ Calculating probabilities: Using Bayes' Theorem to find **P(Category | Document)**

    + **P(Document | Category)**: Probability of an entire document being
      given a classification
    + **P(Category)**: Probability of a Category
    + **P(Document)**: Probability of a Document

+ Constructing a Naive Bayesian Classifier
+ Constructing a Fisher Classifier
+ Persisting a Classifier using SQLite


**Understanding the Differences between Naive Bayes and Fisher
Method**
![naive_fisher](https://cloud.githubusercontent.com/assets/1440268/11493700/23d81826-97b0-11e5-8933-e897bf51ee37.jpg)

Breaking Out the Big Guns: Scikit Learn
---------------------------------------

Although the algorithms presented in "Programming Collective
Intelligence" were a good starting point for learning about text
classification, I knew that I wanted to use more powerful Python
tools, specifically the Natural Language Toolkit (NLTK) and Scikit
Learn. Being interested in Data Science, I wanted to experiment with
as many libraries commonly used by data scientists as I could during
our short project time.

I had questions about what would be the best classifier for my task at
hand. I had been watching Coursera videos for a [Natural Language Processing course](https://www.coursera.org/course/nlp) taught by Stanford instructors, and the videos,
while thought provoking, gave me more questions than answers on how to
proceed.

... And then one of the Hackbright TAs showed me this handy [Machine Learning Map](http://scikit-learn.org/stable/tutorial/machine_learning_map/) on the Scikit Learn website:
**Finding the Right Estimator for the Job**
![ml_map](https://cloud.githubusercontent.com/assets/1440268/11493695/1fcc35be-97b0-11e5-9699-e8081880cdea.png)

With a literal road map in hand, I proceded to work through [this sklearn tutorial](http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html), using the 20 Newsgroups Dataset. I learned about
extracting features using sklearn's CountVectorizer, which, once
fitted, contains a dictionary of feature indices. The tutorial also
introduced me to the concept of term-frequence inverse-document-
frequency (TF-IDF) weighting. I had been curious about how to
emphasize the uniqueness of certain words, and TF-IDF seemed like a
sensible way to weight my features.

Perhaps the most important takeaway from the scikit tutorial was
learning how to evaluate the performance of my classifier. Being
familiar with the concept of garbage in, garbage out, I sought to make
sure that I was building something that didn't just work but worked
well. The tutorial presented a simple evaluation of the model's
predictive accuracy using numpy as well as scikit's built-in metrics
for a more detailed performance analysis.

And then I learned about cross validation.

The Stanford NLP Coursera videos first introduced me to the concept of
cross validation, but, again, it left me feeling uncertain of how to
proceed.
**Cross Validation Slide from Stanford NLP Coursera Course**
![cv](https://cloud.githubusercontent.com/assets/1440268/11493690/17f4231a-97b0-11e5-99c5-348bc82ec597.png)
Enter the same awesome Hackbright TA, who pointed me in the direction
of scikit's [Cross Validation module](http://scikit-learn.org/stable/modules/cross_validation.html). Once I figured out how to
implement KFold, I was able to assess my initial model's performance.

At last, after a week of reading and researching, tinkering and
training, I was ready to dive into coding up my own classifier.



Preprocessing
-------------

Scikit's CountVectorizer [can be customized](http://scikit-learn.org/stable/modules/feature_extraction.html) to add token-level
analysis, which was a breakthrough realization for me:
"Stemming, lemmatizing, compound splitting, filtering based on POS,
etc. are not included in sklearn but can be added by customizing
either the tokenizer or the analyzer."
I had been using CountVectorizer straight-out-of-the-box, so to speak.
This customization realization enabled me to easily encorporate some
NLTK features into my Scikit models, as follows:


+ Add sentence tokenization using nltk.tokenizer.sent_tokenizer
+ Use Penn Treebank Tokenizer using nltk.tokenizer.word_tokenizer

    + This tokenizer splits contractions (e.g. don't --> do n't; can't -->
      ca n't; I'll --> I 'll)



Zooming out, my preprocessing followed these steps:


1. Tokenize documents into sentences --> store in database

    + sentences = sent_tokenizer(document_text)

2. Tokenize sentences into words
3. Fix contractions (replace n't, 'll, with 'not', 'will', etc.)
4. Recombine (delimit on whitespace) and classify/train entire review
   (document)




To Stem, or Not To Stem
-----------------------

Although Scikit's CountVectorizer allows for incorporation of stemming
and lemmatization, after doing on research on the [Stanford NLP website](http://nlp.stanford.edu/IR-book/html/htmledition/stemming-and-lemmatization-1.html), I decided against doing so because there is not much to be
gained for English text analysis.
> Rather than using a stemmer, you can use a lemmatizer , a tool from Natural Language Processing which does full morphological analysis to
accurately identify the lemma for each word. Doing full morphological
analysis produces at most very modest benefits for retrieval. It is
hard to say more, because either form of normalization tends not to
improve English information retrieval performance in aggregate - at
least not by very much. While it helps a lot for some queries, it
equally hurts performance a lot for others. Stemming increases recall
while harming precision. As an example of what can go wrong, note that
the Porter stemmer stems all of the following words:
operate operating operates operation operative operatives operational
to oper. However, since operate in its various forms is a common verb,
we would expect to lose considerable precision on queries such as the
following with Porter stemming:
operational and research
operating and system
operative and dentistry

> For a case like this, moving to using a lemmatizer would not completely fix the problem because particular inflectional forms are
used in particular collocations: a sentence with the words operate and
system is not a good match for the query operating and system. Getting
better value from term normalization depends more on pragmatic issues
of word use than on formal issues of linguistic morphology.

> The situation is different for languages with much more morphology
(such as Spanish, German, and Finnish). Results in the European CLEF
evaluations have repeatedly shown quite large gains from the use of
stemmers (and compound splitting for languages like German).



Extracting Features
-------------------

The accuracy of a Bag-of-Words classifier, such as a Multinomial Naive
Bayes classifier, [can be greatly improved](http://streamhacker.com/2010/06/16/text-classification-sentiment-analysis-eliminate-low-information-features/)
 by improving the features
vectors using NLTK to remove stop words and improve tokenization while
still using sklearn classifiers. I decided to use the Chi-square
metric to determine the most useful features and to measure accuracy,
precision, and recall of models of different feature length (e.g.
1000, 10000, 50000 top features). In statistics, the chi-square test
is applied to test the independence of two events. A high chi-square
value indicates that the hypothesis of independence is incorrect.

Selecting features using Chi-square aims to simplify the classifier by
training on only the "most important" features. A "weaker" classifier
-- trained on fewer features -- is often preferable when training data
is limited. Chi-square is a test of feature independence.

From the Stanford NLP site on Feature Selection:
> We can view feature selection as a method for replacing a complex
classifier (using all features) with a simpler one (using a subset of
the features). It may appear counterintuitive at first that a
seemingly weaker classifier is advantageous in statistical text
classification, but when discussing the bias-variance tradeoff in
Section 14.6, we will see that weaker models are often preferable when
limited training data are available.

From the Stanford NLP site on using Chi-squre for Feature Selection:
> From a statistical point of view, chi-square feature selection is problematic. [...] However, in text classification it rarely matters
whether a few additional terms are added to the feature set or removed
from it. Rather, the relative importance of features is important. As
long as chi-square feature selection only ranks features with respect
to their usefulness and is not used to make statements about
statistical dependence or independence of variables, we need not be
overly concerned that it does not adhere strictly to statistical
theory.


Experimenting with Matplotlib
-----------------------------

As I worked on implementing `Cross Validation`_ on my toy dataset of
45 reviews that I had personally authored, I realized that some plots
would help me better understand my classifier's performance. I first
implemented some nicely styled plots for one k-value at a time (i.e.,
K = 2) that were formatted similar to graphs on `FiveThirtyEight`_:

Author Reviews, K=2
![k2_toyset](https://cloud.githubusercontent.com/assets/1440268/11493709/3076b646-97b0-11e5-9f97-221f49b64dd2.png)

Author Reviews, K=3
![k3_toyset](https://cloud.githubusercontent.com/assets/1440268/11493711/3238474c-97b0-11e5-9649-cd7df9516da6.png)

Author Reviews, K=4
![k4_toyset](https://cloud.githubusercontent.com/assets/1440268/11493712/323a9664-97b0-11e5-81a1-a320d2c79f15.png)

But the real power of these plots would be in comparing the results
across different numbers of folds. BEHOLD! Subplots!

Author Reviews, K=4 thru K=10
![k4-10_toyset_subplots](https://cloud.githubusercontent.com/assets/1440268/11493866/ec8bf08e-97b1-11e5-9502-4e7fb0c37a41.png)

Eventually, when I was ready to work with the Yelp dataset, these
plots became extremely helpful.

Yelp "Gluten" Dataset: Vectorizer for Sentiment Analysis
![sentiment_gltn_k2-10_oneplot](https://cloud.githubusercontent.com/assets/1440268/11493706/2e5bc78e-97b0-11e5-82d0-1bf99925efe3.png)
Yelp "Gluten" Dataset: Vectorizer for Sentiment Analysis
![sentiment_gltn_k2-10_subplots](https://cloud.githubusercontent.com/assets/1440268/11493707/2e5fd2f2-97b0-11e5-868e-49ab44d2f477.png)



Picking a Categorization Classifier: Multi-label vs. Single-label
-----------------------------------------------------------------

The problem that I initially set out to solve -- determining the
"goodness" of a restaurant review for a dietary need -- requires first
identifying relevant reviews for that dietary need. Hence the `need`_
for a document classifier that would categorize reviews.

For the first couple of weeks of my project, I was working with a
single label classifier. That is, given a document, my classifier
would return a single category that it predicted as the best category
for that text. And then, at the beginning of Week 4 of project time --
of 4 available weeks -- I had an epiphany. It was a [multilabel classifier](http://scikit-learn.org/stable/modules/multiclass.html) that I *truly* wanted, because I wanted my classifier to
return not a SINGLE label but MANY labels for a given document. After
all, a restaurant could potentially accommodate or alienate people
with varying dietary needs!

Multilabel classification assigns to each sample a set of target
labels. This can be thought as predicting properties of a data-point
that are not mutually exclusive, such as topics that are relevant for
a document. A text might be about any of religion, politics, finance
or education at the same time or none of these.

So I thought about how to come up with a way to store multiple labels
with my existing data model. It was too late to drop tables and reseed
most of my database. My computer was literally tired of seeding
tables. (It nearly died in Week 2 of project time when I had the CPU
crunching away at capacity for many hours a day over many days.)

**Thinking about Binarizing my Multilabel Classifier**
![img_4624](https://cloud.githubusercontent.com/assets/1440268/11493693/1b3f4a2c-97b0-11e5-9a4e-1af7f34b7942.JPG)

In the end, I experimented with using a OneVsRestClassifier built with
a RandomForest classifier, because scikit so helpfully summarized
classifiers capable of multiclass and classifiers supporting
multilabel classification.



Picking a Sentiment Analysis Classifier
---------------------------------------

So, after all of this, what did I learn about the performance of
different classifiers for the problems of categorization and sentiment
analysis?

A whole lot.

TLDR; Multinominal Naive Bayes really does perform well. I had worked
with a LinearSVC classifier, which had slightly better performance
than the Naive Bayes model. The disadvantage of LinearSVC, however,
was that [I could not extract a probability score for the prediction.]( http://stackoverflow.com/questions/26478000/converting-linearsvcs-decision-function-to-probabilities-scikit-learn-python)

According to the wisdom that is Stack Overflow:

> ... libsvm will train a probability transformation model on top of the
SVM's outputs based on idea of Platt Scaling. ...I actually don't know
 why this post-processing is not available for LinearSVC. Otherwise,
 you would just call predict_proba(X) to get the probability estimate.
-- greeness 

And also this:
> It's not available because it isn't built into Liblinear,
which implements LinearSVC, and also because LogisticRegression is
already available (though linear SVM + Platt scaling might have some
benefits over straight LR, I never tried that). The Platt scaling in
SVC comes from LibSVM. – larsmans

Therefore, for what I wanted to do, I needed to use MultinomialNB for
my sentiment classifiers. However, were I to have more data and more
time, Random Forest [could be a superior choice](http://www.ijcsit.com/docs/Volume%205/vol5issue05/ijcsit2014050557.pdf).



Sentiment Analysis with Python
------------------------------

What inspired me to learn about text classification and sentiment
analysis was a [blog post on indico.io](https://indico.io/blog/plotlines/) I read pre-Hackbright (even
before I was planning to apply to Hackbright) about the shape of
stories.

The author Kurt Vonnegut, whose novels include Breakfast of Champions
and Cat’s Cradle, surmised that a story’s shape can be graphed
following the main character’s ups (good fortune) and downs (ill
fortune). The indico.io post applied this concept to several Disney
movies, comparing the plotlines to see how formulaic Disney plots can
be.

**Exploring the Story Plotline for "The Lion King"**
![overlay-lk](https://cloud.githubusercontent.com/assets/1440268/11493701/25dec5e8-97b0-11e5-9561-9be354409fcc.gif)

When it came time for me to give a lightning talk at Hackbright on a
technical topic, my choice was clear -- I wanted to learn about
sentiment analysis and about NLTK. After much learning and several
iterations of my presentation -- from a high-level discussion of NLTK
to a detailed discussion on NLTK back to a high-level discussion of
sentiment analysis -- I gave [this talk](https://docs.google.com/presentation/d/1qLbHFT345-TR2DB9-wFkLJHxNxy4GlVUkfpSprlTLRE/edit?usp=sharing), which laid a solid
foundation for my understanding of sentiment analysis. Enjoy!






























