import csv
import datetime
import re

from prompt import Prompt


class Search(Prompt):
    def __init__(self):
        super(Search, self).__init__()
        self.result_list = None
        self.starting_date = None
        self.ending_date = None
        self.exact_search_query = None
        self.regex_pattern = None

    def write_new_content(self, new_csv_content):
        with open('logfile.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for entry in new_csv_content:
                writer.writerow(entry)

    def delete_entry(self, result):
        index_to_delete = result[0] + 1
        new_csv_content = []
        with open('logfile.csv') as csv_file:
            reader = csv.reader(csv_file)
            for reader_index, row in enumerate(reader):
                if index_to_delete == reader_index:
                    continue
                new_csv_content.append(row)
        self.write_new_content(new_csv_content)

    def edit_entry(self, result):
        self.prompt("What would you like to edit?")
        self.prompt("[D]ate, [T]ask Name, Time [S]pent, [N]otes.")
        edit_answer = input()
        if edit_answer.lower() == 'd':
            while True:
                self.prompt("What would you like the new Date to be? Please use DD/MM/YYYY. ")
                new_date = input()
                try:
                    task_date = datetime.datetime.strptime(new_date, "%d/%m/%Y").date()
                except ValueError:
                    print('That does not seem to be a valid date. Try again.')
                else:
                    result[1] = task_date
                    break
        elif edit_answer.lower() == 't':
            self.prompt("What would you like the new Task Name to be?")
            new_task_name = input()
            result[2] = new_task_name
        elif edit_answer.lower() == 's':
            self.prompt("What would you like the new Time Spent to be?")
            new_time_spent = input()
            result[3] = new_time_spent
        elif edit_answer.lower() == 'n':
            self.prompt("What would you like the new Notes to be?")
            new_notes = input()
            result[4] = new_notes

        index_to_modify = result[0] + 1
        new_csv_content = []
        with open('logfile.csv') as csv_file:
            reader = csv.reader(csv_file)
            for reader_index, row in enumerate(reader):
                if index_to_modify == reader_index:
                    row = result[1:]
                new_csv_content.append(row)
        self.write_new_content(new_csv_content)

    def display_result(self, **kwargs):
        self.result_list = kwargs['result_list']
        count = 0
        for index, result in enumerate(self.result_list):
            count += 1
            self.prompt("Found the following entry: ")
            print("Date: {}".format(result[1]))
            print("Task Name: {}".format(result[2]))
            print("Time Spent: {}".format(result[3]))
            print("Notes: {}".format(result[4]))
            print("")
            print("Result {} of {}".format(count, len(self.result_list)))

            self.prompt('[N]ext, [D]elete, [E]dit or [Q]uit.')
            user_answer = input()
            if user_answer.lower() == 'n':
                self.clear()
                continue
            elif user_answer.lower() == 'd':
                self.clear()
                self.delete_entry(result)
                self.prompt("The entry has been deleted. Press any key to continue.")
                input()
                # Need to handle the edge case where a user deletes a first entry in a series of entries
                # and then tries to edit the next.
                # This ensures the program keeps working off the original CSV file instead
                # of the constructed results list.
                if ('starting_date' and 'ending_date') in kwargs:
                    self.starting_date = kwargs['starting_date']
                    self.ending_date = kwargs['ending_date']
                    self.search_by_range_of_dates(starting_date=self.starting_date, ending_date=self.ending_date)
                elif 'exact_search_query' in kwargs:
                    self.exact_search_query = kwargs['exact_search_query']
                    self.search_by_exact_search(exact_search_query=self.exact_search_query)
                elif 'regex_pattern' in kwargs:
                    self.regex_pattern = kwargs['regex_pattern']
                    self.search_by_regex_pattern(regex_pattern=self.regex_pattern)
            elif user_answer.lower() == 'e':
                self.clear()
                self.edit_entry(result)
                self.prompt("The entry has been modified. Press any key to continue.")
                input()
                self.clear()
            elif user_answer.lower() == 'q':
                self.clear()
                break
            else:
                print("Not a valid input. Please try again.")
            if count == len(self.result_list):
                print("")
                self.prompt("You've reached the end of the result list. Press any key to go back to the search menu.")
                input()
                self.clear()
                break
            break

    def search_by_exact_date(self):
        while True:
            self.prompt("""What is the day you're looking for? Please use DD/MM/YYYY.
            (Press 'e' to go back to the previous menu)
            """)
            user_input = input()
            if user_input == 'e':
                self.clear()
                break
            try:
                requested_date = datetime.datetime.strptime(user_input, "%d/%m/%Y").date()
            except ValueError:
                print('That does not seem to be a valid date. Try again.')
            else:
                with open('logfile.csv') as csvfile:
                    reader = csv.DictReader(csvfile)
                    result_count = 0
                    result_list = []
                    for index, row in enumerate(reader):
                        if requested_date == datetime.datetime.strptime(row['Date'], "%d/%m/%Y").date():
                            result_count += 1
                            result_list.append([index, row['Date'], row['Task Name'], row['Time Spent'], row['Notes']])
                        else:
                            print("No entries found for that date! :( ")
                if result_list:
                    self.display_result(result_list=result_list)
            break

    def search_by_range_of_dates(self, **kwargs):
        while True:
            # Need to handle the edge case where a user deletes a first entry in a series of entries
            # and then tries to edit the next.
            if not ('starting_date' and 'ending_date') in kwargs:
                self.prompt("""Please enter a starting date. Please use DD/MM/YYYY.
                (Press 'e' to go back to the previous menu)
                """)
                starting_date = input()
                self.clear()
                if starting_date == 'e':
                    break
                try:
                    self.starting_date = datetime.datetime.strptime(starting_date, "%d/%m/%Y").date()
                except ValueError:
                    print('That does not seem to be a valid date. Try again.')

                self.prompt("""Please enter an ending date. Please use DD/MM/YYYY.
                            (Press 'e' to go back to the previous menu)
                            """)
                ending_date = input()
                self.clear()
                if ending_date == 'e':
                    break
                try:
                    self.ending_date = datetime.datetime.strptime(ending_date, "%d/%m/%Y").date()
                except ValueError:
                    print('That does not seem to be a valid date. Try again.')
            else:
                self.starting_date = kwargs['starting_date']
                self.ending_date = kwargs['ending_date']
            with open('logfile.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                result_count = 0
                result_list = []
                for index, row in enumerate(reader):
                    row_date = datetime.datetime.strptime(row['Date'], "%d/%m/%Y").date()
                    if self.starting_date <= row_date <= self.ending_date:
                        result_count += 1
                        result_list.append([index, row['Date'], row['Task Name'], row['Time Spent'], row['Notes']])
                if result_list:
                    self.display_result(
                        result_list=result_list,
                        starting_date=self.starting_date,
                        ending_date=self.ending_date
                    )
                else:
                    print("No entries found for that date range! :( ")
            break

    def search_by_exact_search(self, **kwargs):
        while True:
            if 'exact_search_query' not in kwargs:
                self.prompt("""Please enter your search query. (This will search in the Task Name or Notes)
                (Enter 'e' to return to the previous menu)
                                """)
                self.exact_search_query = input()
                self.clear()
                if self.exact_search_query == 'e':
                    break
            else:
                self.exact_search_query = kwargs['exact_search_query']
            with open('logfile.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                result_count = 0
                result_list = []
                for index, row in enumerate(reader):
                    task_name = row['Task Name']
                    task_notes = row['Notes']
                    if self.exact_search_query == task_name or self.exact_search_query == task_notes:
                        result_count += 1
                        result_list.append([index, row['Date'], row['Task Name'], row['Time Spent'], row['Notes']])
                if result_list:
                    self.display_result(
                        result_list=result_list,
                        exact_search_query=self.exact_search_query
                    )
                else:
                    print("No entries found for that search query! :( ")
            break

    def search_by_regex_pattern(self, **kwargs):
        while True:
            if 'regex_pattern' not in kwargs:
                self.prompt("""Please enter your regex pattern. (This will search in the Task Name or Notes)
                (Enter 'e' to return to the previous menu)
                                """)
                self.regex_pattern = input()
                self.clear()
                if self.regex_pattern == 'e':
                    break
            else:
                self.regex_pattern = kwargs['regex_pattern']
            with open('logfile.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                result_count = 0
                result_list = []
                for index, row in enumerate(reader):
                    task_name = row['Task Name']
                    task_notes = row['Notes']
                    if (
                            re.search(r"{}".format(self.regex_pattern), task_name) or
                            re.search(r"{}".format(self.regex_pattern), task_notes)
                    ):
                        result_count += 1
                        result_list.append([index, row['Date'], row['Task Name'], row['Time Spent'], row['Notes']])
                if result_list:
                    self.display_result(
                        result_list=result_list,
                        regex_pattern=self.regex_pattern
                    )
                else:
                    print("No entries found for that pattern :( ")
            break
        pass

    def get_input(self):
        while True:
            self.prompt("""Do you want to search by: 
            1) Exact Date
            2) Range of Dates
            3) Exact Search
            4) Regex Pattern
            5) Return to Menu
            """)

            user_input = input()
            if user_input == '1':
                self.clear()
                self.search_by_exact_date()
            elif user_input == '2':
                self.clear()
                self.search_by_range_of_dates()
            elif user_input == '3':
                self.clear()
                self.search_by_exact_search()
            elif user_input == '4':
                self.clear()
                self.search_by_regex_pattern()
            elif user_input == '5':
                self.clear()
                break
