import spacy
import re 
import markovify
import nltk
from nltk.corpus import gutenberg
import warnings

warnings.filterwarnings('ignore')

redditOne = open('Relationship.txt')
aita = redditOne.read()

redditTwo = open('Qanon.txt')
anon = redditTwo.read() 

redditThree = open('AITA.txt')
real = redditThree.read()

redditFour = open('Trump.txt')
trump = redditFour.read()

#print(real)

#utility function for text cleaning
def text_cleaner(text):
  text = re.sub(r'--', ' ', text)
  text = re.sub('[\[].*?[\]]', '', text)
  text = re.sub(r'(\b|\s+\-?|^\-?)(\d+|\d*\.\d+)\b','', text)
  text = ' '.join(text.split())
  return text
  
aita = re.sub(r'Chapter \d+', '', aita)
anon = re.sub(r'Chapter \d+', '', anon)
real = re.sub(r'Chapter \d+', '', real)
trump = re.sub(r'Chapter \d+', '', trump)
#apply cleaning function to corpus
aita = text_cleaner(aita)
real = text_cleaner(real)
anon = text_cleaner(anon)
trump = text_cleaner(trump)

nlp = spacy.load('en_core_web_md')
aita_doc = nlp(aita)
anon_doc = nlp(anon)
real_doc = nlp(real)
trump_doc = nlp(trump)

aita_sents = ' '.join([sent.text for sent in aita_doc.sents if len(sent.text) > 1])
anon_sents = ' '.join([sent.text for sent in anon_doc.sents if len(sent.text) > 1])
real_sents = ' '.join([sent.text for sent in real_doc.sents if len(sent.text) > 1])
trump_sents = ' '.join([sent.text for sent in trump_doc.sents if len(sent.text) > 1])

combined_sents = aita_sents + anon_sents + real_sents + trump_sents

#print(combined_sents)

#next we will use spacy's part of speech to generate more legible text
class POSifiedText(markovify.Text):
   def word_split(self, sentence):
      return ['::'.join((word.orth_, word.pos_)) for word in nlp(sentence)]
   def word_join(self, words):
      sentence = ' '.join(word.split('::')[0] for word in words)
      return sentence
#Call the class on our text
generator_2 = POSifiedText(combined_sents, state_size=3)

#Call for Google's Firebase




#now we will use the above generator to generate sentences

for i in range(5):
  sentence = generator_2.make_sentence()

  print(sentence)
 
#print 100 characters or less sentences
print("")

for i in range(5):

  captured = generator_2.make_short_sentence(max_chars=100)
  
  print(captured)


