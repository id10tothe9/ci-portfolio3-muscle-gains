from tabulate import tabulate
from colorama import just_fix_windows_console
from termcolor import colored
import gspread
from google.oauth2.service_account import Credentials


"""
Define needed variables to access google sheet and write data.
"""
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


def get_lines_str(message, symb):
    """
    Return a separator line with symbol symb (- or +)
    to be printed before or after the prompt for the user.
    Its length is determined by the longest line in the message.
    """
    message_lines = message.split('\n')
    str_len = 0
    for line in message_lines:
        if len(line) > str_len:
            str_len = len(line)
    if str_len > 80:  # avoid separator lines longer than terminal char limit
        str_len = 80
    return f'{str_len*symb}'


def get_message(message):
    """
    Add the separator lines before and after the message
    that's to be shown to the user.
    """
    lines_str = get_lines_str(message, '-')
    plus_str = get_lines_str(message, '+')
    return f'\n{plus_str}\n{message}\n{lines_str}\n'


def welcome_message():
    """
    Return the welcome message that's to be printed at the start
    of the user's interaction with the app. It explains the purpose
    of the app and how to interact with it.
    """
    message = " Welcome To Muscle Gains!\n\n\
    This application is meant for a training instructor.\n\
    It will help you design training plans for your customers.\n\n\
    The app will guide you to enter the required data for each exercise:\n\
    e.g. exercise name, number of sets, repetitions and weights\n\
    After that you can let it show you the plan you have created thus far,\n\
    or let it calculate the metrics you need for each muscle group to help\n\
    you in the design process.\n\n\
    The data will be saved to a google sheet for your later review, and you\n\
    can continue editing your current plan by choosing option 1."
    return get_message(message)


def main_menu_message():
    """
    Return the main menu options text that will be printed for the user.
    """
    message = ' Please choose an option:\n\
    1. Create a training plan\n\
    2. Display current training plan\n\
    3. Display calculated metrics'

    return message


def color_error_message(message):
    """
    Use the termcolor library to style error messages for the user
    with a red background.
    """
    return colored(message, 'white', 'on_red')


def check_input(user_input, requirements_list):
    """
    This function takes in the user_input and a list of requirements
    the input must fulfil. Depending on the requirements list, it checks
    if the input is valid. If it's not valid it returns an appropriate
    error message for the user, otherwise it returns the processed user_input.
    """
    error_message = ''
    for req in requirements_list:
        if req == 'can skip':  # user can skip entering some values
            if user_input == '':
                break

        elif req == 'name':  # names must be at least 4 chars long
            try:
                if len(user_input) < 4:
                    raise ValueError
            except ValueError:
                error_message = '\nName must be at least 4 characters long!'
                error_message = color_error_message(error_message)

        elif req == 'positive integer':
            try:
                user_input = int(user_input)
                if user_input <= 0:
                    raise ValueError
            except ValueError:
                error_message = '\nPlease enter a positive natural number.'
                error_message = color_error_message(error_message)
                break

        elif req == 'positive float':
            try:
                user_input = float(user_input)
                if user_input < 0:
                    raise ValueError
            except ValueError:
                error_message = '\nPlease enter a positive real number'
                error_message = color_error_message(error_message)
                break

        # user can choose a number only from the available options list
        elif (
            type(req) == tuple and
            (user_input < req[0] or user_input > req[1])
        ):
            error_message = f'\nPlease enter a value between\
            {req[0]} and {req[1]}.'
            error_message = color_error_message(error_message)
            break

        elif req == 'yes or no':  # for yes or no answers
            try:
                user_input = user_input.lower()
                if len(user_input) > 3:  # random strings are not valid
                    raise ValueError
                elif user_input.find('yes') > -1:
                    user_input = 'yes'
                elif user_input.find('no') > -1:
                    user_input = 'no'
                else:
                    raise ValueError
            except ValueError:
                error_message = "\nPlease enter a 'yes' or 'no' answer."
                error_message = color_error_message(error_message)
                break

        # validate that the user has entered exactly three numbers
        elif req == 'cadence':  # input format required e.g. '2 4 5'
            user_input, error_message = get_cadence_values(user_input)
            if error_message:
                break

    return user_input, error_message


def get_cadence_values(user_input):
    """
    This function expects three numbers separated by commas or spaces or both
    as they should be entered by the user. If these criteria are not met,
    an appropriate error message is presented.
    """
    error_message = ''
    space_free_list = user_input.split()

    nums = []
    for element in space_free_list:
        comma_free_list = element.split(',')
        for el in comma_free_list:
            if el:  # ignore empty strings '' separated after the commas
                try:
                    el = int(el)
                except ValueError:
                    try:
                        el = float(el)
                    except ValueError:
                        error_message = color_error_message(
                            '\nPlease enter numbers only'
                        )
                        return user_input, error_message
                nums.append(el)
    if len(nums) != 3:
        error_message = color_error_message('\nPlease enter three numbers')
    else:
        user_input = nums

    return user_input, error_message


def get_user_input(message, requirements_list):
    """
    This function handles all input requests: print out prompt message to
    user, check if their answer satisfies all requirements by calling the
    check_input function. It keeps prompting the user with an appropriate
    error message until the answer is valid.
    """
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
    This function creates a new training plan. If the user has already
    created a plan, it asks the user for confirmation to delete previous
    data or to continue modifying current plan.
    """
    global training_plan

    if training_plan != {}:  # in case user has already created a training plan
        message = "You have already created a plan. Do you want to edit it or \
        replace it?\nPlease choose an option:\n1. Add exercises to current \
        training plan.\n2. Delete current plan and create a new one."
        user_input = get_user_input(message, ['positive integer', (1, 2)])
        if user_input == 1:  # continue modifying current plan
            pass
        else:  # delete old plan and create a new one
            training_plan = {}

    # construct muscle group objects and/or add exercises by prompting the user
    while True:
        group = get_group(training_plan)
        group.add_exercise(get_exercise())
        training_plan[group.name] = group  # add new group to dictionary

        """
        Continue looping to add more exercises until user is done.
        """
        message = "Do you want to add another exercise? \
        Please type 'yes' or 'no'"
        user_input = get_user_input(message, ['yes or no'])
        if user_input == 'no':
            break

    return


def get_group(training_plan):
    """
    This function constructs a MuscleGroup object which will
    contain the user's data for exercises in a muscle group.
    If other MuscleGroup objects already exist, ask the user
    to choose from them or to create a new muscle group.
    """
    if training_plan != {}:  # other MuscleGroup objects already exist
        i = 1
        group_names = []
        message = ('Choose an option to enter a new muscle group or '
                   'use an exsistent one:\n')
        message += f'{i}. New muscle group'
        for group_name in training_plan:
            i += 1
            group_names.append(group_name)
            message += f'\n{i}. {group_name}'
        user_input = get_user_input(message, ['positive integer', (1, i)])
        if user_input == 1:  # user chooses to create a new muscle group
            group = MuscleGroup()
            group.get_name()
            """
            If user enters name of a group that already exists,
            let them know and use it instead
            """
            if training_plan.get(group.name) is not None:
                print(f'\nYou have already entered this muscle group!\n\
                Will be adding the exercise to it :)\nChosen muscle group: \
                {group.name}')
                group = training_plan[group.name]
        else:  # user chooses to use a muscle group that already exists
            group = training_plan[group_names[user_input-2]]
    else:  # in case no muscle group exists just create a new one
        group = MuscleGroup()
        group.get_name()
    return group


def get_exercise():
    """
    Create an Exercise object and prompt user to define its data.
    This object will then be added to the already constructed
    MuscleGroup in create_training_plan().
    """
    exercise = Exercise()
    exercise.get_name()
    exercise.get_sets()
    exercise.get_reps_and_weights()
    exercise.get_cadence()
    exercise.get_rest()
    return exercise


class MuscleGroup():
    """
    This class defines muscle group objects. Thsse can contain several
    Exercise objects to contain data for the rows of the training table
    which belong to a given muscle group. This class also contains methods
    to calculate the metrics needed for each muscle group from all contained
    row data.
    """
    def __init__(self):
        self.name = ''
        self.exercises = {}  # each object contains a dictionary of exercises

    def get_name(self):
        message = 'Enter name of the muscle group\n(e.g. Biceps, Chest, Abs)'
        self.name = get_user_input(message, ['name'])

    def add_exercise(self, exercise):
        self.exercises[exercise.name] = exercise

    def calc_metrics(self):
        """
        A method to calculate volume of the muscle group.
        """
        volume = 0
        tut = 0  # 'time under tension': time where muscles are under tension
        exercise_time = 0  # total time of exercise
        total_reps = 0  # to get total number of repetitions in an exercise
        rest_time = 0  # time of resting after each exercises
        for exercise in self.exercises.values():
            for rnw in exercise.reps_and_weights:
                volume += rnw[0]*rnw[1]
                total_reps += rnw[0]
            if exercise.cadence != []:
                tut += total_reps * (exercise.cadence[0] + exercise.cadence[2])
                exercise_time = tut + (total_reps * exercise.cadence[1])
            if exercise.rest != '':
                rest_time += exercise.rest
        # total duration of training in this group
        group_time = exercise_time + rest_time

        return volume, tut, group_time


class Exercise():
    """
    This class defines objects which represent one row of the training plan.
    Each Object contains the name of the exercise and its relevant metrics.
    """
    def __init__(self):
        self.name = ''
        self.sets = ''
        self.reps_and_weights = []
        self.cadence = []
        self.rest = ''

    def get_name(self):
        message = 'Enter name of the exercise\n\
        (e.g. Curls, Front Squats, French press)'
        self.name = get_user_input(message, ['name'])

    def get_sets(self):
        message = 'How many sets?'
        self.sets = get_user_input(message, ['positive integer', 'minimum 1'])

    def get_reps_and_weights(self):
        """
        Get data for repetitions and weight for each set
        """
        for set in range(self.sets):
            message = f'How many repetitions (Reps) in set Nr. {set+1}'
            reps = get_user_input(message, ['positive integer', 'minimum 1'])
            message = f'Enter weight in kg for set Nr. {set+1}'
            weight = get_user_input(message, ['positive float'])
            self.reps_and_weights.append([reps, weight])

    # get the cadence values (a set of three numbers) in seconds
    def get_cadence(self):
        message = 'Cadence (in seconds): enter the duration of the \
        contraction, pause and extension\n of the muscle in that \
        order as comma (or space) separated numbers:\ne.g. 2, 0, 4\
        \n\nYou can skip this value by pressing enter instead.'
        cadence = get_user_input(message, ['can skip', 'cadence'])
        if cadence != '':
            self.cadence = cadence

    # Get the resting duration after the exercise set in seconds
    def get_rest(self):
        message = 'Please enter the resting duration after each set \
        in seconds?\n\nYou can skip this value by pressing enter instead.'
        rest = get_user_input(message, ['can skip', 'positive integer'])
        if rest != '':
            self.rest = rest


def print_training_plan():
    """
    This function fetches all exercise data from all muscle groups,
    orders them into lists and prints them out to the terminal as a
    table using the tabulate library.
    It also saves them into google sheet for better usability.
    """
    global training_plan

    most_sets = 0  # register the highest number of sets
    cadence = False
    rest = False
    """
    In this cascading for loop we only count the highest number of
    sets and register whether cadence and rest variables were entered
    by the user. We will use this information to set equal row lengths
    for all exercises.
    """
    for group in training_plan.values():
        for exercise in group.exercises.values():
            if exercise.sets > most_sets:  # get the highest number of sets
                most_sets = exercise.sets
            if exercise.cadence != []:
                cadence = True
            if exercise.rest != '':
                rest = True

    """
    Next we create the title row for the table. Due to the 80 character length
    restriction on Heroku terminal, we will only print first Reps and Weights
    columns to the terminal, while printing the rest of them to google sheet.
    We add the 'cadence' and 'rest' columns if they exist in any exercise.
    """
    # clear worksheet on google sheet
    SHEET.worksheet('Training Table').clear()
    # header row for google sheet
    sheet_headers = ["Muscle\nGroup", "Exercise", "Sets"]
    # header row for terminal table
    table_headers = ["Muscle\nGroup", "Exercise", "Sets"]

    # Add all Reps and Weight columns to sheet but not to terminal table
    for set_number in range(1, most_sets+1):
        sheet_headers.extend(
            [f'Set{set_number}\nReps', f'Set{set_number}\nWeight\n(kg)']
            )
    # add cadence and rest columns if entered by the user
    if cadence:
        sheet_headers.append('Cadence\n(s)')
        table_headers.append('Cadence\n(s)')
    if rest:
        sheet_headers.append('Rest\n(s)')
        table_headers.append('Rest\n(s)')

    # add row to google sheet
    SHEET.worksheet('Training Table').append_row(sheet_headers)

    """
    Now we can populate the rows of the table.
    Where a value is missing we set the cell to '--'.
    """
    sheet_row = []
    table_row = []
    table_rows = []
    for group in training_plan.values():
        for exercise in group.exercises.values():
            sheet_row.extend([group.name, exercise.name, exercise.sets])
            table_row.extend([group.name, exercise.name, exercise.sets])
            # Add all Reps and Weight columns to sheet
            for reps_and_weights in exercise.reps_and_weights:
                sheet_row.extend(reps_and_weights)
            # In case of empty values, fill cells with '--'
            for set_number in range(exercise.sets, most_sets):
                sheet_row.extend(['--', '--'])
            if cadence:
                if exercise.cadence:
                    cadence_str = (f'{exercise.cadence[0]}, '
                                   f'{exercise.cadence[1]}, '
                                   f'{exercise.cadence[2]}')
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
            SHEET.worksheet('Training Table').append_row(sheet_row)
            table_rows.append(table_row)
            sheet_row = []  # reset sheet_row for the next exercise
            table_row = []  # reset table_row for the next exercise

    # create table for terminal
    table = tabulate(table_rows, headers=table_headers,
                     tablefmt="fancy_grid", stralign=("center"),
                     numalign=("center"))
    print(f'\n{table}')

    # notify user that not all data were printed to the terminal
    print(f'\nThis table does not shows Reps and Weight data due \
    to display width limits.\nYou can view the complete table in \
    google sheet:\n{sheet_tinyurl} -> worksheet: "Training Table"')

    return


def print_calculated_values():
    """
    This function calculates the metrics of each muscle group
    and prints them out in a table to the terminal. A copy is
    also saved to google sheet.
    """
    worksheet = 'Training Metrics'
    SHEET.worksheet(worksheet).clear()  # clear worksheet
    sheet_headers = ["Muscle\nGroup",
                     "Volume\n(kg)",
                     "Time Under\nTension (s)"]
    table_headers = ["Muscle\nGroup",
                     "Volume\n(kg)",
                     "Time Under\nTension (s)"]
    SHEET.worksheet(worksheet).append_row(sheet_headers)

    sheet_row = []
    table_rows = []
    tot_session_time = 0  # total duration of training session
    for group in training_plan.values():
        volume, tut, group_time = group.calc_metrics()
        tot_session_time += group_time
        sheet_row.extend([group.name, volume, tut])
        table_rows.append([group.name, volume, tut])
        SHEET.worksheet(worksheet).append_row(sheet_row)
        sheet_row = []  # reset sheet_row for next row in google sheet
    table = tabulate(table_rows, headers=table_headers,
                     tablefmt="fancy_grid", stralign=("center"),
                     numalign=("center"))
    print(f'\n{table}')
    print(f'\nTotal Duration Of Training: {tot_session_time}(s)')
    print(f'\nYou can also view this table in google sheet:\n\
    {sheet_tinyurl} -> worksheet: "Training Metrics"')
    return


def main_menu():
    """
    This function presents the user with the main menu options
    to choose from. It presents them with the option to create a
    training plan, print the training plan or calculate the metrics.
    After each option that's executed the user is brought back
    to the main menu again.
    """
    while True:
        global training_plan

        message = main_menu_message()  # print main menu options to the user
        # get user's choice as a number: 1, 2 or 3
        user_input = get_user_input(message, ['positive integer', (1, 3)])
        if user_input == 1:  # option create training plan
            create_training_plan()
            print('\nThank you for your participation!')
        elif user_input == 2:  # option print out current plan
            if training_plan == {}:  # in case no plan has been created
                message = "\nSorry, you didn't create a training plan yet!"
                print(color_error_message(message))
            else:
                print_training_plan()
        elif user_input == 3:  # option print out training metrics
            if training_plan == {}:  # in case no plan has been created
                message = "\nSorry, you didn't create a training plan yet!"
                print(color_error_message(message))
            else:
                print_calculated_values()
        input('\nPress Enter to return to main menu.\n')


def main():
    """
    Print the welcome message and present the
    main menu options to the user.
    """
    print(welcome_message())
    main_menu()


"""
Define the training plan as a global variable for all functions
to access independently, then call the main function.
"""
training_plan = {}
main()
