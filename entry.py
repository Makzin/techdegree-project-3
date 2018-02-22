import csv
import os.path
from prompt import Prompt
import datetime


class Entry(Prompt):

    def save(self, new_content):
        # Check if CSV file exists - if not create a new file and write headers
        file_exists = os.path.isfile('logfile.csv')
        with open('logfile.csv', 'a') as csvfile:
            if not file_exists:
                fieldnames = ['Date', 'Task Name', 'Time Spent', 'Notes']
                dict_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                dict_writer.writeheader()
            writer = csv.writer(csvfile, delimiter=',')
            for entry in new_content:
                writer.writerow(entry)

    def get_content(self):
        content = []
        self.prompt("""Please enter the date of the task.
                    Please use DD/MM/YYYY: """)
        user_input = input()
        self.clear()
        try:
            task_date = datetime.datetime.strptime(user_input, "%d/%m/%Y").date()
            content.append(task_date.strftime('%m/%d/%Y'))
        except ValueError:
            print('That does not seem to be a valid date. Try again.')

        self.prompt('Please enter the title of the task. ')
        task_title = input()
        content.append(task_title)
        self.clear()

        self.prompt('Time spent (rounded minutes):  ')
        time_spent = input()
        content.append(time_spent)
        self.clear()

        self.prompt('Notes (optional): ')
        notes = input()
        content.append(notes)
        self.clear()

        self.save([content])
        self.prompt('Your entry has been added. Press any key to return to the main menu.')
        input()
        self.clear()
