from tabulate import tabulate
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Muscle Gains')
sheet_tinyurl = 'https://tinyurl.com/mr2cfuv8'


def get_lines_str(message):
    message_lines = message.split('\n')
    str_len = 0
    for line in message_lines:
        if len(line) > str_len:
            str_len = len(line)
    if str_len > 80: # avoid separator lines longer than terminal char limit
        str_len = 80    
    return f'{str_len*"-"}'


def get_message(message):
    lines_str = get_lines_str(message)
    return f'\n{lines_str}\n{message}\n{lines_str}\n'

def welcome_message():
    message = 'Welcome'
    return message


def main_menu_message():
    message = f'Please choose an option:\n\
    1. Create a new training plan\n\
    2. Display current training plan\n\
    3. Display calculated values'

    return message


def check_input(user_input, requirements_list):
    """
    This function takes in the user_input and a list of requirements
    the input must fulfil. Depending on the requirements list, it checks
    if the input is valid. If it's not valid it returns an appropriate
    response, otherwise it returns an empty string.
    """
    error_message = ''
    for req in requirements_list:
        if req == 'can skip': # in case user decides to skip entering values
            if user_input == '':
                break
        elif req == 'positive integer':
            try:
                user_input = int(user_input)
                if user_input <= 0:
                    raise ValueError
            except ValueError:
                error_message = '\nPlease enter a positive natural number.\n'
                break

        elif req == 'positive float':
            try:
                user_input = float(user_input)
                if user_input < 0:
                    raise ValueError
            except ValueError:
                error_message = '\nPlease enter a positive real number\n'
                break

        elif type(req) == tuple and (user_input < req[0] or user_input > req[1]):
            error_message = f'\nPlease enter a value between {req[0]} and {req[1]}\n'
            break

        elif req == 'yes or no':
            try:
                user_input = user_input.lower()
                if len(user_input) > 3: # random strings that might contain yes or no are not valid
                    raise error                
                elif user_input.find('yes') > -1:
                    user_input = 'yes'
                elif user_input.find('no') > -1:
                    user_input = 'no'
                else:
                    raise ValueError
            except ValueError:
                error_message = "Please enter a 'yes' or 'no' answer."
                break

        
        elif req == 'cadence': # input format required '2 4 5' or e.g. '2,4, 5'
            user_input, error_message = get_cadence_values(user_input)
            if error_message:
                break

    return user_input, error_message


def get_cadence_values(user_input):
    """
    This function expects three numbers separated by commas or spaces or both 
    as they should be entered by the user. If those criteria are not fulfilled,
    an appropriate error message is presented.
    """
    error_message = ''
    space_free_list = user_input.split()

    nums = []
    for element in space_free_list:
        comma_free_list = element.split(',')
        for el in comma_free_list:
            if el: # ignore empty strings '' separated after the commas
                try:
                    el = int(el)
                except:
                    try:
                        el = float(el)
                    except:
                        error_message = 'Please enter numbers only\n'
                        return user_input, error_message
                nums.append(el)
    if len(nums) != 3:
        error_message = 'Please enter three numbers\n'
    else:
        user_input = nums
    
    return user_input, error_message


def get_user_input(message, requirements_list):
    """
    Handle all input requests: print out message to user, check
    if their answer satisfies all requirements by calling the check_input
    function. Return user_input if user answer is valid.
    """
    lines_str = get_lines_str(message)
    while True:
        user_input = input(get_message(message))
        user_input, error_message = check_input(user_input, requirements_list)
        if error_message:
            print(error_message)
        else:
            break
    return user_input


def create_training_plan():
    """
    This function starts creating a new training plan. If an old plan
    exists, it asks the user for confirmation to delete previous data.
    """
    # if a training table already exists, ask user if they're sure
    #   they want to delete the current table and construct a new one
    #   If user says yes, delete all current objects and data first.
    global training_plan


    if training_plan != {}:
        message = "You have already created a plan. Do you want to edit it or replace it? Please choose an option:\n1. Add exercises to current training plan.\n2. Delete current plan and create a new one."
        user_input = get_user_input(message, ['positive integer', (1, 2)])
        if user_input == 1:
            pass
        else:
            training_plan = {}

    # ask user to "enter a new muscle group or choose an existent group"
    # get group name
    # construct basic muscle group object
    while True:
        group = get_group(training_plan)
        group.add_exercise(get_exercise())
        training_plan[group.name] = group # add new group to dictionary

        """
        Continue looping to add more exercises until user is done.
        """
        message = "Do you want to add another exercise? Please type 'yes' or 'no'"
        user_input = get_user_input(message, ['yes or no'])
        if user_input == 'no':
            break
    # choice: add another row?
    # choice: same group / different group?
    # if different group -> choose an existent group or enter a new one

    return 


def get_group(training_plan):
    if training_plan != {}:
        i = 1
        group_names = []
        message = 'Choose an option to enter a new muscle group or use an exsistent one:\n'
        message += f'{i}. New muscle group'
        for group_name in training_plan:
            i += 1
            group_names.append(group_name)
            message += f'\n{i}. {group_name}'
        user_input = get_user_input(message, ['positive integer', (1, i)])
        if user_input == 1:
            group = MuscleGroup()
            group.get_name()
        else:
            group = training_plan[group_names[user_input-2]]
    else:
        group = MuscleGroup()
        group.get_name()
    return group


def get_exercise():
    exercise = Exercise()
    exercise.get_name()
    exercise.get_sets()
    exercise.get_reps_and_weights()
    exercise.get_cadence()
    exercise.get_rest()
    return exercise


class MuscleGroup():
    """
    A class that contains all exercise rows which belong to a given muscle group
    """
    def __init__(self):
        self.name = ''
        self.exercises = {} # MuscleGroup contains a dictionary of exercises
  
    def get_name(self):
        message = 'Enter name of the muscle group'
        self.name = get_user_input(message, [''])
  
    def add_exercise(self, exercise):
        self.exercises[exercise.name] = exercise
  
    def calc_metrics(self):
        """
        A method to calculate volume of the muscle group
        """
        volume = 0
        tut = 0 # stands for 'time under tension': time during which the muscles are under tension
        exercise_time = 0 # total time of exercise
        total_reps = 0 # to get total number of repetitions in an exercise
        rest_time = 0 # time of resting after each exercises
        for exercise in self.exercises.values():
            for rnw in exercise.reps_and_weights:
                volume += rnw[0]*rnw[1]
                total_reps += rnw[0]
            if exercise.cadence !=[]:
                tut += total_reps * (exercise.cadence[0] + exercise.cadence[2])
                exercise_time = tut + (total_reps * exercise.cadence[1])
            if exercise.rest != '':
                rest_time += exercise.rest
        group_time = exercise_time + rest_time # total duration of training in this group

        return volume, tut, group_time


class Exercise():
    """
    A Class who's objects represent one row of the training plan.
    Each Object contains name of the exercise and its relevant metrics.
    Each Exercise object belongs to a unique MuscleGroup.
    """
    def __init__(self):
        self.name = ''
        self.sets = ''
        self.reps_and_weights = []
        self.cadence = []
        self.rest = ''

    def get_name(self):
        message = 'Enter name of the exercise'
        self.name = get_user_input(message, [''])
  
    def get_sets(self):
        message = 'How many sets?'
        self.sets = get_user_input(message, ['positive integer', 'minimum 1'])

    def get_reps_and_weights(self):
        for set in range(self.sets):
            message = f'How many reps in set Nr. {set+1}'
            reps = get_user_input(message, ['positive integer', 'minimum 1'])
            message = f'Which weight for set Nr. {set+1}'
            weight = get_user_input(message, ['positive float'])
            self.reps_and_weights.append([reps, weight])
  
    def get_cadence(self):
        message = 'Cadence: enter the duration of the contraction, pause and extension\nin that order as comma (or space) separated numbers:\ne.g. 2, 0, 4\n\nYou can skip this value by pressing enter instead.'
        cadence = get_user_input(message, ['can skip', 'cadence'])
        if cadence != '':
            self.cadence = cadence
    
    def get_rest(self):
        """
        Get the resting duration after the exercise in seconds.
        """
        message = 'How long should the resting duration be after this exercise?\n\nYou can skip this value by pressing enter instead.'
        rest = get_user_input(message, ['can skip', 'positive integer'])
        if rest != '':
            self.rest = rest


def print_training_plan():
    """
    This function fetches all exercise rows of defined muscle groups, orders them into lists
    and prints them out with the prettytable library function.
    """
    global training_plan
    """
    In this cascading for loop we only count the highest number of sets and register if cadence and rest variables were registered. We use this information to set equal row lengths for all exercises.
    """
    most_sets = 0 # Registers the highest number of sets in order to set all rows to equal lengths
    cadence = False
    rest = False
    for group in training_plan.values(): # training_plan is a dictionary containing the muscle_group objects
        for exercise in group.exercises.values(): # group.exercises is a dict containing the exercise objects
            if exercise.sets > most_sets:
                most_sets = exercise.sets
            if exercise.cadence !=[]:
                cadence = True
            if exercise.rest != '':
                rest = True
    """
    Next we create the title row for the table. We reserve the required number of Reps x Weights columns depending on the highest number of sets in all exercises. We add the 'cadence' and 'rest' columns if they exist in any exercise.
    """
    SHEET.worksheet('Training Table').clear() # clear worksheet
    sheet_headers = ["Muscle\nGroup", "Exercise", "Sets"]
    table_headers = ["Muscle\nGroup", "Exercise", "Sets", "Reps", "Weight\n(kg)"]
    for set_number in range(1, most_sets+1): # reserve a place holder for highest number of sets
        sheet_headers.extend([f'Set{set_number}\nReps', f'Set{set_number}\nWeight\n(kg)'])
    # if most_sets > 1: # add place holder for further sets in terminal output
    #             table_headers.append('more\nSets\n[..]')
    if cadence:
        sheet_headers.append('Cadence\n(s)')
        table_headers.append('Cadence\n(s)')
    if rest:
        sheet_headers.append('Rest\n(s)')
        table_headers.append('Rest\n(s)')
    SHEET.worksheet('Training Table').append_row(sheet_headers) # add row to google sheet

    """
    Now we can populate the rows of the table. Where a value is missing we set the cell to '--'.
    """
    sheet_row = []
    table_row = []
    table_rows = []
    for group in training_plan.values(): # training_plan is a dictionary containing the muscle_group objects
        for exercise in group.exercises.values(): # group.exercises is a dict containing the exercise objects
            sheet_row.extend([group.name, exercise.name, exercise.sets])
            table_row.extend([group.name, exercise.name, exercise.sets])
            table_row.extend(exercise.reps_and_weights[0]) # add only first set data to terminal table
            # if exercise.sets > 1: # add place holder for further sets in terminal table
            #     table_row.append('[..]')
            # else:
            #     table_row.append('--')
            for reps_and_weights in exercise.reps_and_weights:
                sheet_row.extend(reps_and_weights)
            for set_number in range(exercise.sets, most_sets): # In case of empty values, fill cells with '--'
                sheet_row.extend(['--', '--'])
            if cadence:
                if exercise.cadence:
                    cadence_str = f'{exercise.cadence[0]}, {exercise.cadence[1]}, {exercise.cadence[2]}'
                    sheet_row.append(cadence_str)
                    table_row.append(cadence_str)
                else:
                    sheet_row.append('--')
                    table_row.append('--')
            if rest:
                if exercise.rest:
                    sheet_row.append(exercise.rest)
                    table_row.append(exercise.rest)
                else:
                    sheet_row.append('--')
                    table_row.append('--')
            SHEET.worksheet('Training Table').append_row(sheet_row) # add row to google sheet
            table_rows.append(table_row)
            sheet_row = [] # reset sheet_row for the next exercise
            table_row = [] # reset table_row for the next exercise

    table = tabulate(table_rows, headers = table_headers, tablefmt = "fancy_grid", stralign = ("center"), numalign = ("center"))
    print(f'\n{table}')
    if most_sets > 1:
        print(f'\nWe printed out Reps and Weight for the first set only due to display limits.\nYou can view the complete table in google sheet:\n{sheet_tinyurl} -> worksheet: Training Table')
    else:
        print(f'\nYou can also view this table in google sheet:\n{sheet_tinyurl} -> worksheet: Training Table')
    return


def print_calculated_values():
    worksheet = 'Training Metrics'
    SHEET.worksheet(worksheet).clear() # clear worksheet
    sheet_headers = ["Muscle\nGroup", "Volume\n(kg)", "Time Under\nTension (s)"]
    table_headers = ["Muscle\nGroup", "Volume\n(kg)", "Time Under\nTension (s)"]
    SHEET.worksheet(worksheet).append_row(sheet_headers) # add headers row to google sheet

    sheet_row = []
    table_rows = []
    tot_session_time = 0 # total duration of training session
    for group in training_plan.values():
        volume, tut, group_time = group.calc_metrics()
        tot_session_time += group_time
        sheet_row.extend([group.name, volume, tut])
        table_rows.append([group.name, volume, tut])
        SHEET.worksheet(worksheet).append_row(sheet_row) # add row to google sheet
        sheet_row = [] # reset sheet_row for next row in google sheet
    table = tabulate(table_rows, headers = table_headers, tablefmt = "fancy_grid", stralign = ("center"), numalign = ("center"))
    print(f'\n{table}')
    print(f'\nTotal Duration Of Training: {tot_session_time}(s)')
    print(f'\nYou can also view this table in google sheet:\n{sheet_tinyurl} -> worksheet: Training Metrics')
    return



def main_menu():
    while True:
        global training_plan
        message = main_menu_message()
        user_input = get_user_input(message, ['positive integer', (1, 3)])
        if user_input == 1:
            create_training_plan()
            print('\nThank you for your participation!')
        elif user_input == 2:
            if training_plan == {}:
                print("Sorry, you didn't create a training plan yet!\n")
            else:
                print_training_plan()
        elif user_input == 3:
            if training_plan == {}:
                print("Sorry, you didn't create a training plan yet!\n")
            else:
                print_calculated_values()
        input('\nPress Enter to return to main menu.\n')


def main():
    print(welcome_message())
    main_menu()



training_plan = {}
main()
