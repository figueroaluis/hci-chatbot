#!/usr/bin/env python3
"""A tag-based chatbot framework."""
import random
import re
from collections import Counter
from specific_word_detection import emotion_word_found


class ChatBot:
    """A tag-based chatbot framework

    This class is not meant to be instantiated. Instead, it provides helper
    functions that subclasses could use to create a tag-based chatbot. There
    are two main components to a chatbot:

    * A set of STATES to determine the context of a message.
    * A set of TAGS that match on words in the message.

    Subclasses must implement two methods for every state (except the
    default): the `on_enter_*` method and the `respond_from_*` method. For
    example, if there is a state called "confirm_delete", there should be two
    methods `on_enter_confirm_delete` and `respond_from_confirm_delete`.

    * `on_enter_*()` is what the chatbot should say when it enters a state.
        This method takes no arguments, and returns a string that is the
        chatbot's response. For example, a bot might enter the "confirm_delete"
        state after a message to delete a reservation, and the
        `on_enter_confirm_delete` might return "Are you sure you want to
        delete?".

    * `respond_from_*()` determines which state the chatbot should enter next.
        It takes two arguments: a string `message`, and a dictionary `tags`
        which counts the number of times each tag appears in the message. This
        function should always return with calls to either `go_to_state` or
        `finish`.

    The `go_to_state` method automatically calls the related `on_enter_*`
    method before setting the state of the chatbot. The `finish` function calls
    a `finish_*` function before setting the state of the chatbot to the
    default state.

    The TAGS class variable is a dictionary whose keys are words/phrases and
    whose values are (list of) tags for that word/phrase. If the words/phrases
    match a message, these tags are provided to the `respond_from_*` methods.
    """

    STATES = []
    TAGS = {}

    def __init__(self, default_state):
        """Initialize a Chatbot.

        Arguments:
            default_state (str): The starting state of the agent.
        """
        if default_state not in self.STATES:
            print(' '.join([
                f'WARNING:',
                f'The default state {default_state} is listed as a state.',
                f'Perhaps you mean {self.STATES[0]}?',
            ]))
        self.default_state = default_state
        self.state = self.default_state
        self.tags = {}
        self._check_states()
        self._check_tags()

    def _check_states(self):
        """Check the STATES to make sure that relevant functions are defined."""
        for state in self.STATES:
            prefixes = []
            if state != self.default_state:
                prefixes.append('on_enter')
            prefixes.append('respond_from')
            for prefix in prefixes:
                if not hasattr(self, f'{prefix}_{state}'):
                    print(' '.join([
                        f'WARNING:',
                        f'State "{state}" is defined',
                        f'but has no response function self.{prefix}_{state}',
                    ]))

    def _check_tags(self):
        """Check the TAGS to make sure that it has the correct format."""
        for phrase in self.TAGS:
            tags = self.TAGS[phrase]
            if isinstance(tags, str):
                self.TAGS[phrase] = [tags]
            tags = self.TAGS[phrase]
            assert isinstance(tags, (tuple, list)), ' '.join([
                'ERROR:',
                'Expected tags for {phrase} to be str or List[str]',
                f'but got {tags.__class__.__name__}',
            ])

    def go_to_state(self, state):
        """Set the chatbot's state after responding appropriately.

        Arguments:
            state (str): The state to go to.

        Returns:
            str: The response of the chatbot.
        """
        assert state in self.STATES, f'ERROR: state "{state}" is not defined'
        assert state != self.default_state, ' '.join([
            'WARNING:',
            f"do not call `go_to_state` on the default state {self.default_state};",
            f'use `finish` instead',
        ])
        on_enter_method = getattr(self, f'on_enter_{state}')
        response = on_enter_method()
        self.state = state
        return response

    def chat(self):
        """Start a chat with the chatbot."""
        try:
            message = input('> ')
            while message.lower() not in ('exit', 'quit'):
                print()
                print(f'{self.__class__.__name__}: {self.respond(message)}')
                print()
                message = input('> ')
        except (EOFError, KeyboardInterrupt):
            print()
            exit()

    def respond(self, message):
        """Respond to a message.

        Arguments:
            message (str): The message from the user.

        Returns:
            str: The response of the chatbot.
        """
        respond_method = getattr(self, f'respond_from_{self.state}')
        return respond_method(message, self._get_tags(message))

    def finish(self, manner):
        """Set the chatbot back to the default state

        This function will call the appropriate `finish_*` method.

        Arguments:
            manner (str): The type of exit from the flow.

        Returns:
            str: The response of the chatbot.
        """
        response = getattr(self, f'finish_{manner}')()
        self.state = self.default_state
        return response

    def _get_tags(self, message):
        """Find all tagged words/phrases in a message.

        Arguments:
            message (str): The message from the user.

        Returns:
            Dict[str, int]: A count of each tag found in the message.
        """
        counter = Counter()
        msg = message.lower()
        for phrase, tags in self.TAGS.items():
            if re.search(r'\b' + phrase.lower() + r'\b', msg):
                counter.update(tags)
        return counter


class OxyCSBot(ChatBot):
    """A simple chatbot that directs students to office hours of CS professors."""

    STATES = [
        'waiting',
        'hi',
        'tell_me_more',
        'emotion_detection',
        'anecdote',
        'suggestion',
        'feel_better_question',
        'feels_better',
    ]

    TAGS = {
        # # intent
        # 'office hours': 'office-hours',
        # 'help': 'office-hours',
        #
        # # professors
        # 'kathryn': 'kathryn',
        # 'leonard': 'kathryn',
        # 'justin': 'justin',
        # 'li': 'justin',
        # 'jeff': 'jeff',
        # 'miller': 'jeff',
        # 'celia': 'celia',
        # 'hsing-hau': 'hsing-hau',

        # generic
        'okay': 'success',
        'bye': 'success',
        'hi': 'hi',
        'hello': 'hi',
        'what\'s up': 'hi',
        'bye': 'bye',
        'see ya': 'bye',
        'see you': 'bye',
        'good bye': 'bye',
        'alright then': 'bye',
        'never thought about that': 'bye',
        'thanks': 'thanks',
        'thank you': 'thanks',
        'good idea': 'thanks',

        #state2

        #state3
        # state4 Anecdote
        'I don\'t know': 'idk',
        'I\'m confused': 'idk',
        'What should I do': 'idk',
        'idk': 'idk',
        #'no idea': 'idk',
        #'fix': 'idk',
        #'make it up': 'idk',

        # state 5 confirm help
        'yes': 'yay',
        'yep': 'yay',
        'of course': 'yay',
        'yeah': 'yay',

        # states 5 not helping
        'not really': 'no',
        'no': 'no',
        'nope': 'no',

    }

    # PROFESSORS = [
    #     'celia',
    #     'hsing-hau',
    #     'jeff',
    #     'justin',
    #     'kathryn',
    # ]

    def __init__(self):
        """Initialize the OxyCSBot.

        The `professor` member variable stores whether the target
        professor has been identified.
        """
        super().__init__(default_state='waiting')
        # self.professor = None

    # "waiting" state functions

    def respond_from_waiting(self, message, tags):
        if emotion_word_found(message):
            return self.go_to_state('emotion_detection')
        elif 'hi' in tags:
            if len(message) < 20:
                return self.go_to_state('hi')
            else:
                if emotion_word_found(message):
                    return self.go_to_state('emotion_detection')
        elif 'bye' in tags:
            return self.finish('success')
        else:
            return self.finish_confused()

    def on_enter_emotion_detection(self):
        response_emotion0 = "Oh no, I'm sorry about that:/ Why do you feel that way?"
        response_emotion2 = "Sounds awful. Let it out, tell me more"
        response_emotion1 = "I'm really sorry to hear that. What are you going to do?"

        responses = [response_emotion0, response_emotion1, response_emotion2]
        return random.choice(responses)

    def respond_from_emotion_detection(self, message, tags):
        if 'idk' in tags:
            return self.go_to_state('anecdote')
        elif emotion_word_found(message):
            return self.go_to_state('emotion_detection')
        else:
            return self.go_to_state('tell_me_more')

    def on_enter_hi(self):
        greet0 = "Hello."
        greet1 = "What's up?"
        greet2 = "Yo."
        question0 = "How you doing?"
        question1 = "How are you?"
        question2 = "Are you alright?"
        question3 = "How's it going?"

        greetings = [greet0, greet1, greet2]
        questions = [question0, question1, question2, question3]

        return random.choice(greetings) + " " + random.choice(questions)

    def respond_from_hi(self, message, tags):
        return self.go_to_state('tell_me_more')

    def on_enter_tell_me_more(self):
        response0 = "What happened?"
        response1 = "Can you tell me more about it?"
        response2 = "Why?"
        responses = [response0, response1, response2]
        return random.choice(responses)

    def respond_from_tell_me_more(self, message, tags):
        return self.go_to_state('emotion_detection')

    def on_enter_anecdote(self):
        anecdote1 = "I'm sorry:/ I remember one time when my girlfriend was mad at me, I bought her chocolate. " \
                    "I also told her she means so much to me, and that I know I messed up. I gave her time and space," \
                    " and waited until she came back around. We're still together to this day. I just rambled..." \
                    "but does this help? "
        return anecdote1

    def respond_from_anecdote(self, message, tags):
        if 'yay' in tags:
            return self.go_to_state('feels_better')
        elif 'no' in tags:
            return self.go_to_state('suggestion')
        elif 'thanks' in tags:
            return self.finish('thanks')
        else:
            return self.go_to_state('tell_me_more')

    def on_enter_suggestion(self):
        suggestion0 = "Um. I have some idea if you need more help."
        suggestion1 = "Why not talk to her first? "
        more_suggestion0 = "It's not as hard as you think."
        more_suggestion1 = "Tell her how you feel. It's better to communicate than thinking by yourself."

        return random.choice([suggestion0, suggestion1]) + random.choice([more_suggestion0, more_suggestion1])

    def respond_from_suggestion(self, message, tags):
        if emotion_word_found(message):
            return self.go_to_state('emotion_detection')
        elif 'thanks' in tags:
            return self.finish('thanks')
        else:
            return self.go_to_state('feel_better_question')

    def on_enter_feel_better_question(self):
        return "Do you feel better now?"

    def respond_from_feel_better_question(self, message, tags):
        if 'yay' in tags:
            return self.go_to_state('feels_better')
        elif 'no' in tags:
            return self.go_to_state('suggestion')
        elif 'thanks' in tags:
            return self.finish('thanks')
        else:
            return self.go_to_state('tell_me_more')

    def on_enter_feels_better(self):
        return "Good to hear! Need anything else?"

    def respond_from_feels_better(self, message, tags):
        if 'no' in tags:
            return self.finish('success')
        elif 'yay' in tags:
            return self.go_to_state('tell_me_more')
        elif 'thanks' in tags:
            return self.finish('thanks')
        else:
            return self.go_to_state('waiting')

    # "finish" functions

    def finish_confused(self):
        return "Sorry, what did you say?"

    def finish_success(self):
        return 'Awesome:) Glad we could talk this out! I gotta go to some stuff now, later!'

    def finish_fail(self):
        return "Sorry man, I don't know what to say."

    def finish_thanks(self):
        return "You're always welcome! But I gotta go now, see ya."


if __name__ == '__main__':
    OxyCSBot().chat()
