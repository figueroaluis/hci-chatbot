import spacy 

###
#TESTGIT
###

############ Curse words to filter ################

emotion_detected = ""

def emotion_word_found(sentence):
	emotion_word_bank = {}
	with open("emotions.txt") as f:
		for line in f:
			key = str(line.rstrip())
			emotion_word_bank[key] = '0'

	sentenceLower = sentence.lower()
	sentenceLower = sentenceLower.split()

	for word in sentenceLower:
		if word in emotion_word_bank:
			emotion_detected = word
			# print("This emotion was detected: ", word)
			return True

def get_emotion_word():
	return emotion_detected


# def find_curse_word():


def get_subject_of_sentence(input):
	nlp = spacy.load('en')
	doc = nlp(input)
	sub_toks = [token for token in doc if (token.dep_ == "nsubj")]
	return sub_toks


# print(get_subject_of_sentence("She's such a bitch about it. I don't know what I'm gonna do about it"))


# print(find_emotion_word("I'm feeling annoyed"))