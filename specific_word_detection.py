import spacy 


############ Curse words to filter ################



# def find_emotion_word():


# def find_curse_word():




def get_subject_of_sentence(input):
	nlp = spacy.load('en')
	doc = nlp(input)
	sub_toks = [token for token in doc if (token.dep_ == "nsubj")]
	return sub_toks


print(get_subject_of_sentence("She's such a bitch about it. I don't know what I'm gonna do about it"))