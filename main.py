import spacy
import re 
import markovify
import nltk
from nltk.corpus import gutenberg
import warnings
import sqlite3

connection = sqlite3.connect("Markov.db")
cursor = connection.cursor()
#cursor.execute("CREATE TABLE chatter (sentence TEXT, chat_number INTEGER)")

print(connection.total_changes)

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
  text = re.sub(r"won\'t", "will not", text)
  text = re.sub(r"can\'t", "can not", text)
  text = re.sub(r"n\'t", " not", text)
  text = re.sub(r"\'re", " are", text)
  text = re.sub(r"\'s", " is", text)
  text = re.sub(r"\'d", " would", text)
  text = re.sub(r"\'ll", " will", text)
  text = re.sub(r"\'t", " not", text)
  text = re.sub(r"\'ve", " have", text)
  text = re.sub(r"\'m", " am", text)
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

#now we will use the above generator to generate sentences
# I (grant) commented this one out as the sentences "some what" string together and would like to do more research
#for i in range(5):
  #sentence = generator_2.make_sentence()

  #print(sentence)
 
#print 100 characters or less sentences
#print("")

#this sentence gen makes tweet size lengts of 140, google say new is 280 gonna keep simple til i do some research 
for i in range(5):
 # print("----------")
  loop = i
  captured = generator_2.make_short_sentence(max_chars=140)
  #print(f'This is the orignal text:.... {captured}')
  
    
  comma = captured.replace(' ,',',')
  period = comma.replace(' .', '.')
  qMark = period.replace(' ?', '?')
  poss = qMark.replace("'", "''")
  
  def decontracted(phrase):
    # specific
    phrase = re.sub(r"won\’t", "will not", phrase)
    phrase = re.sub(r"can\’t", "can not", phrase)

    # general
    phrase = re.sub(r"n\’t", " not", phrase)
    phrase = re.sub(r"\’re", " are", phrase)
    phrase = re.sub(r"\’s", " is", phrase)
    phrase = re.sub(r"\’d", " would", phrase)
    phrase = re.sub(r"\’ll", " will", phrase)
    phrase = re.sub(r"\’t", " not", phrase)
    phrase = re.sub(r"\’ve", " have", phrase)
    phrase = re.sub(r"\’m", " am", phrase)
    return phrase

  output = decontracted(poss)
  sql = "INSERT INTO chatter VALUES (?,?)"
  cursor.execute(sql, (output, loop))
  connection.commit()
  print(decontracted(poss))
 # print("----------")
