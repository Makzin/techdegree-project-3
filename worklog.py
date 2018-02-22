from entry import Entry
from prompt import Prompt
from search import Search


class TaskLog(Prompt):
    def __init__(self):
        super(TaskLog, self).__init__()

    def welcome(self):
        self.prompt('Welcome to the Work Log program!')

    def main(self):
        while True:
            self.prompt("""What would you like to do today?
            1) Add a new entry. 
            2) Search for existing entries. 
            3) Quit
            """)

            user_input = input()
            if user_input == '1':
                self.clear()
                entry = Entry()
                entry.get_content()
            elif user_input == '2':
                self.clear()
                search = Search()
                search.get_input()
            elif user_input == '3':
                self.clear()
                print('Thanks for using the Task Logger program. Goodbye!')
                break


program = TaskLog()
program.welcome()
program.main()
