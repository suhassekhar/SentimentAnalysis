# -*- coding: utf-8 -*-
"""
basic_sentiment_analysis
~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the code and examples described in
http://fjavieralba.com/basic-sentiment-analysis-with-python.html

"""

from pprint import pprint
import nltk
import yaml
import sys
import os
import re
import datetime


class Splitter(object):
    def __init__(self):
        self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self, text):
        """
        input format: a paragraph of text
        output format: a list of lists of words.
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        """
        sentences = self.nltk_splitter.tokenize(text)
        tokenized_sentences = [self.nltk_tokenizer.tokenize(sent) for sent in sentences]
        return tokenized_sentences


class POSTagger(object):
    def __init__(self):
        pass

    def pos_tag(self, sentences):
        """
        input format: list of lists of words
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        output format: list of lists of tagged tokens. Each tagged tokens has a
        form, a lemma, and a list of tags
            e.g: [[('this', 'this', ['DT']), ('is', 'be', ['VB']), ('a', 'a', ['DT']), ('sentence', 'sentence', ['NN'])],
                    [('this', 'this', ['DT']), ('is', 'be', ['VB']), ('another', 'another', ['DT']), ('one', 'one', ['CARD'])]]
        """

        pos = [nltk.pos_tag(sentence) for sentence in sentences]
        # adapt format
        pos = [[(word, word, [postag]) for (word, postag) in sentence] for sentence in pos]
        return pos


class DictionaryTagger(object):
    def __init__(self, dictionary_paths):
        files = [open(path, 'r') for path in dictionary_paths]
        dictionaries = [yaml.load(dict_file) for dict_file in files]
        map(lambda x: x.close(), files)
        self.dictionary = {}
        self.max_key_size = 0
        for curr_dict in dictionaries:
            for key in curr_dict:
                if key in self.dictionary:
                    self.dictionary[key].extend(curr_dict[key])
                else:
                    self.dictionary[key] = curr_dict[key]
                    self.max_key_size = max(self.max_key_size, len(key))

    def tag(self, postagged_sentences):
        return [self.tag_sentence(sentence) for sentence in postagged_sentences]

    def tag_sentence(self, sentence, tag_with_lemmas=False):
        """
        the result is only one tagging of all the possible ones.
        The resulting tagging is determined by these two priority rules:
            - longest matches have higher priority
            - search is made from left to right
        """
        tag_sentence = []
        N = len(sentence)
        if self.max_key_size == 0:
            self.max_key_size = N
        i = 0
        while (i < N):
            j = min(i + self.max_key_size, N)  # avoid overflow
            tagged = False
            while (j > i):
                expression_form = ' '.join([word[0] for word in sentence[i:j]]).lower()
                expression_lemma = ' '.join([word[1] for word in sentence[i:j]]).lower()
                if tag_with_lemmas:
                    literal = expression_lemma
                else:
                    literal = expression_form
                if literal in self.dictionary:
                    # self.logger.debug("found: %s" % literal)
                    is_single_token = j - i == 1
                    original_position = i
                    i = j
                    taggings = [tag for tag in self.dictionary[literal]]
                    tagged_expression = (expression_form, expression_lemma, taggings)
                    if is_single_token:  #if the tagged literal is a single token, conserve its previous taggings:
                        original_token_tagging = sentence[original_position][2]
                        tagged_expression[2].extend(original_token_tagging)
                    tag_sentence.append(tagged_expression)
                    tagged = True
                else:
                    j = j - 1
            if not tagged:
                tag_sentence.append(sentence[i])
                i += 1
        return tag_sentence


def value_of(sentiment):
    if sentiment == 'positive': return 1
    if sentiment == 'negative': return -1
    return 0


def sentence_score(sentence_tokens, previous_token, acum_score):
    if not sentence_tokens:
        return acum_score
    else:
        current_token = sentence_tokens[0]
        tags = current_token[2]
        token_score = sum([value_of(tag) for tag in tags])
        if previous_token is not None:
            previous_tags = previous_token[2]
            if 'inc' in previous_tags:
                token_score *= 2.0
            elif 'dec' in previous_tags:
                token_score /= 2.0
            elif 'inv' in previous_tags:
                token_score *= -1.0
        return sentence_score(sentence_tokens[1:], current_token, acum_score + token_score)


def sentiment_score(review):
    return sum([sentence_score(sentence, None, 0.0) for sentence in review])

def pos_perc(pos,count):
    #positive_tweet = 0
    percent_pos = ((float(pos)/count)*100)
    return percent_pos

def neg_perc(neg,count):
    #negative_tweet = 0
    percent_neg = ((float(neg)/count)*100)
    return percent_neg


if __name__ == "__main__":
    positive_tweet = 0
    score = 0
    negative_tweet = 0
    line_count = 0
    total_score = 0
    percent_positive = 0
    percent_negative = 0
    text = "text"
    for line in sys.stdin:
        if line.split(':', 1)[0] == 'ERROR':
            print "none"
        else:
            text = line
            line_count += 1
            print(line_count)
    #print text
    # text = """PM #NarendraModi visits ailing former #BJP leader Jaswant Singh in hospital."""

            splitter = Splitter()
            postagger = POSTagger()
            dicttagger = DictionaryTagger(['dicts/positive.yml', 'dicts/negative.yml',
                                   'dicts/inc.yml', 'dicts/dec.yml', 'dicts/inv.yml'])

            splitted_sentences = splitter.split(text)
    #pprint(splitted_sentences)

            pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
    #pprint(pos_tagged_sentences)

            dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
    #pprint(dict_tagged_sentences)

    #print("analyzing sentiment...")
            score = sentiment_score(dict_tagged_sentences)
            print (text)
        #print "score is %d" % score
        if score > 0.0:
            print "score is %d" % score
            positive_tweet += 1
            percent_positive = pos_perc(positive_tweet,line_count)
            #print "positive percent of view %d" % percent_positive
        elif score < 0.0:
            print "score is %d" % score
            negative_tweet += 1
            percent_negative = neg_perc(negative_tweet,line_count)
            #print "negative percent of view %d" % percent_negative
        elif score == 0.0:
            print "score is %d" % score
            print "normal tweet"

        total_score = total_score + score
        ##time calculation
        current_time = datetime.datetime.now().time()
        time = current_time.strftime('%H%M%S')
        time_int = int(time)
        print "time taken %d" %time_int
        print "total score is %d" % total_score
        print "positive percent of view %d" % percent_positive
        print "negative percent of view %d" % percent_negative
        print "\n"
        #print "the positive percent of tweets are %d" % percent_positive
        #print "the negative tweets percent are %d" % percent_negative