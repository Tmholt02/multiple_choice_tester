import random
import textwrap
import colorama as color


class Question:

    __wrapper = textwrap.TextWrapper(width=50)

    def __init__(self, topic: str, prompt: str, choices: list, correct_idx: int = 0):
        self.__topic: str = topic
        self.__prompt: str = prompt
        self.__choices: list = choices
        self.__correct_idx: int = correct_idx

    def get_topic(self):
        return self.__topic

    def get_prompt(self):
        return self.__prompt

    def get_choices(self):
        return self.__choices.copy()

    def correct_idx(self):
        return self.__correct_idx

    def make_shuffled(self):
        new_choices = self.get_choices()
        random.shuffle(new_choices)
        new_correct_idx = new_choices.index(self.__choices[self.__correct_idx])
        return Question(
            self.get_topic(),
            self.get_prompt(),
            new_choices,
            new_correct_idx
        )

    def __str__(self):
        out = ""
        out += "\n".join(Question.__wrapper.wrap(self.__prompt))
        for i in range(len(self.__choices)):
            out += f"\n  {chr(i + ord('a'))})  "
            out += "\n      ".join(Question.__wrapper.wrap(self.__choices[i]))
        return out


def main():
    # Use a breakpoint in the code line below to debug your script.
    print("Hello user, please enter your file path below")
    file_name = input("FileName: ")
    file = open(file_name, 'r')

    # This dude can be used for some good formatting
    wrapper = textwrap.TextWrapper(width=50)

    # We need to know where the topics start and stop, and
    topics = {0: "default"}
    current_topic = 0
    questions = []

    # We will search through each item within the file, and record it
    for item in file.read().strip('\n').split("\n\n"):

        # If this item is a topic marker, change the current topic
        # based on our position within questions
        if item[0] == '@':
            current_topic = len(questions)
            topics[current_topic] = item[1:]
            continue

        # Since its a question, we must split it into parts, and
        # add the question to the main list of Questions
        lines = item.split('\n')
        questions.append(Question(
            topics[current_topic],
            lines[0],
            lines[1:]
        ))

    # This is an independent copy of all the questions
    question_set = questions.copy()

    # The main loop will endlessly quiz the user
    while True:
        random.shuffle(question_set)
        quiz(question_set)
        print("------------------------------")
        print()
        print("Would you like to continue?")
        print("  r)  Restart")
        print("  q)  Quit")
        print()
        a = input("Response: ").lower()
        while len(a) != 1 or a not in "rq":
            a = input("Response: ").lower()

        if a == 'r':
            continue
        elif a == 'q':
            break


def quiz(question_set):
    # Keep track of total correct
    correct = 0

    # Copy and shuffle all questions and loop through them all
    for question in question_set:

        # We will make a shuffled copy of the question
        q = question.make_shuffled()
        print("------------------------------\n\n" + str(q) + '\n')

        # Get a valid response. If its the wrong length
        # or out of range, delete it and try again
        a = input("Response: ").lower()
        while len(a) != 1 or not 0 <= (ord(a) - ord('a')) < len(q.get_choices()):
            a = input("Response: ").lower()

        # Check for validity and print feedback
        if ord(a) - ord('a') == q.correct_idx():
            print(color.Fore.GREEN + "Correct!" + color.Fore.RESET)
            correct += 1
        else:
            print(color.Fore.RED + "Wrong! Correct answer is " +
                  color.Fore.GREEN + chr(q.correct_idx() + ord('a')) + color.Fore.RESET)

    # The whole study set has been attempted, give them results
    print("------------------------------")
    print()
    print("You're doing great!")
    print(f"    Score:  {correct} / {len(question_set)}")
    print(f"            {int(100 * correct / len(question_set))}%")
    input("Continue: ")
    print()


if __name__ == "__main__":
    main()

