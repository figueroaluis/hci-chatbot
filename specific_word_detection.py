import spacy
import string

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


def get_emotion_word(sentence):
    emotion_word_bank = {}
    with open("emotions.txt") as f:
        for line in f:
            key = str(line.rstrip())
            emotion_word_bank[key] = '0'

    sentenceLower = sentence.lower()
    sentenceLower = sentenceLower.split()
    emotion_word_list = []

    for word in sentenceLower:
        if word in emotion_word_bank:
            emotion_detected = word
            emotion_word_list.append(emotion_detected)

    return emotion_word_list


# def find_curse_word():

def detect_emotion_phrase(sentence):
    list = get_word_coord_list(sentence)
    distances = get_word_distance(list)
    for dist in distances:
        for word in get_subject_of_sentence(sentence):
            if (str(word).lower() == 'he'):
                word = get_emotion_word(sentence)[0]
                if dist <= 15:
                    return "Why is he " + word + "?"
                else:
                    return "Okay, please tell me more"
            elif (str(word).lower() == 'she'):
                word = get_emotion_word(sentence)[0]
                if dist <= 15:
                    return "Why is she " + word + "?"
                else:
                    return "Okay, please tell me more"
            elif (str(word).lower() == 'girlfriend'):
                word = get_emotion_word(sentence)[0]
                if dist <= 15:
                    return "Why is your girlfriend " + word + "?"
                else:
                    return "Okay, please tell me more"
            elif (str(word).lower() == 'boyfriend'):
                word = get_emotion_word(sentence)[0]
                if dist <= 15:
                    return "Why is your boyfriend " + word + "?"
                else:
                    return "Okay, please tell me more"
            elif (str(word).lower() == 'partner'):
                word = get_emotion_word(sentence)[0]
                if dist <= 15:
                    return "Why is your partner " + word + "?"
                else:
                    return "Okay, please tell me more"
            elif (str(word).lower() == 'i'):
                word = get_emotion_word(sentence)[0]
                if dist <= 15:
                    return "Why are you " + word + "?"
                else:
                    return "Okay, please tell me more"
            else:
                return "Okay, please tell me more"
    return "Okay, please tell me more"


def get_word_coord_list(sentence):
    dist_list = []
    subject_list = get_subject_of_sentence(sentence)
    emotion_word_list = get_emotion_word(sentence)
    for word in subject_list:
        for emotion in emotion_word_list:
            subject = str(word)

            sub_index = sentence.find(subject)
            dist_list.append(sub_index)
                # if sentence.__contains__("I'm"):
                #     dist_list.append(sentence.find("I'm"))
                # elif sentence.__contains__("i'm"):
                #     dist_list.append(sentence.find("i'm"))
            emotion_index = sentence.find(emotion)
            dist_list.append(emotion_index)

    return dist_list


def get_word_distance(word_list):
    distance = []
    # print(len(word_list))
    i = 0
    while i < int(len(word_list) - 1):
        # print(i)
        dist = word_list[i + 1] - word_list[i]
        distance.append(dist)
        i += 2
    return distance


def get_subject_of_sentence(input):
    nlp = spacy.load("en")
    doc = nlp(input)
    sub_tokens = [token for token in doc if (token.dep_ == "nsubj")]
    return sub_tokens

print(detect_emotion_phrase("I just don't know what to do because she is mad at me"))

