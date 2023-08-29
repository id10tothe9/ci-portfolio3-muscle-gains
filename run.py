from prettytable import PrettyTable


def welcome_message():
    return """\n----------------------------------
    Welcome!"""


def main_menu_message():

    return """\n----------------------------------
    Please choose an option:
    1. Create a new training plan
    2. Display current training plan
    3. Display calculated values\n----------------------------------\n\n"""


def check_input(user_input, requirements_list):
    """
    This function takes in the user_input and a list of requirements
    the input must fulfil. Depending on the requirements list, it checks
    if the input is valid. If it's not valid it returns an appropriate
    response, otherwise it returns an empty string.
    """
    error_message = ''
    for req in requirements_list:
        if req == 'positive integer':
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
        print(comma_free_list)
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
    
    print(nums)
    return user_input, error_message


def get_user_input(message, requirements_list):
    """
    Handle all input requests: print out message to user, check
    if their answer satisfies all requirements by calling the check_input
    function. Return user_input if user answer is valid.
    """
    while True:
        user_input = input(message)
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
        message = "You have already created a plan. Do you want to edit it or replace it? Please choose an option:\n1. Add exercises to current training plan.\n2. Delete current plan and create a new one.\n"
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
        message = "Do you want to add another exercise? Please type 'yes' or 'no'.\n"
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
        message += f'{i}. New muscle group\n'
        for group_name in training_plan:
            i += 1
            group_names.append(group_name)
            message += f'{i}. {group_name}\n'
        user_input = get_user_input(message, ['positive integer', (1, i)])
        if user_input == 1:
            group = MuscleGroup()
            group.get_name()
        else:
            group = training_plan[group_names[i-2]]
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
        message = 'Enter name of the muscle group\n'
        self.name = get_user_input(message, [''])
  
    def add_exercise(self, exercise):
        self.exercises[exercise.name] = exercise
  
    def calc_vol():
        """
        A method to calculate volume of the muscle group
        """
        return


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
        message = 'Enter name of the exercise\n'
        self.name = get_user_input(message, [''])
  
    def get_sets(self):
        message = 'How many sets?\n'
        self.sets = get_user_input(message, ['positive integer'])

    def get_reps_and_weights(self):
        for set in range(self.sets):
            message = f'How many reps in set Nr. {set+1}\n'
            reps = get_user_input(message, ['positive integer'])
            message = f'Which weight for set Nr. {set+1}\n'
            weight = get_user_input(message, ['positive float'])
            self.reps_and_weights.append([reps, weight])
  
    def get_cadence(self):
        message = 'Cadence: enter the duration of the contraction, pause and extension in that order as comma (or space) separated numbers\ne.g. 2, 0, 4\nYou can skip this value by pressing enter instead:\n'
        self.cadence = get_user_input(message, ['cadence'])
    
    def get_rest(self):
        """
        Get the resting duration after the exercise in seconds.
        """
        message = 'How long should the resting duration be after this exercise?\n'
        self.rest = get_user_input(message, ['positive integer'])


def print_training_plan():
    global training_plan




def main_menu():
    while True:
        global training_plan
        message = main_menu_message()
        user_input = get_user_input(message, ['positive integer', (1, 3)])
        if user_input == 1:
            create_training_plan()
            print(training_plan)
        elif user_input == 2:
            if training_plan == {}:
                print("Sorry, you didn't create a training plan yet!\n")
            else:
                print_training_plan()
        elif user_input == 3:
            print_calculated_values()
        input('Press Enter to return to main menu:\n')


def main():
    print(welcome_message())
    main_menu()



training_plan = {}
main()
