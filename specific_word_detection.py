import spacy 


############ Curse words to filter ################



def find_emotion_word(sentence):
	emotion_word_bank = {}
	with open("emotions.txt") as f:
		for line in f:
			key = str(line.rstrip())
			emotion_word_bank[key] = '0'

	sentenceLower = sentence.lower()
	sentenceLower = sentenceLower.split()

	for word in sentenceLower:
		if word in emotion_word_bank:
			# print("This emotion was detected: ", word)
			return True


# def find_curse_word():




def get_subject_of_sentence(input):
	nlp = spacy.load('en')
	doc = nlp(input)
	sub_toks = [token for token in doc if (token.dep_ == "nsubj")]
	return sub_toks


# print(get_subject_of_sentence("She's such a bitch about it. I don't know what I'm gonna do about it"))


print(find_emotion_word("I'm feeling annoyed"))