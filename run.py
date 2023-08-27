
def welcome_message():
  return "Welcome!\n"


def main_menu_message():
  return """Choose an option:
  1. Create a new training plan
  2. Display current training plan
  3. Display calculated values\n\n"""


def check_input(user_input, requirements_list):
  """
  This function takes in the user_input and a list of requirements
  the input must fulfil. Depending on the requirements list, it checks
  if the input is valid. If it's not valid it returns an appropriate
  response, otherwise it returns an empty string.
  """
  for req in requirements_list:
    if req == 'integer':
      try:
        user_input = int(user_input)
      except ValueError:
        return '\nPlease enter an integer.\n'

    elif req == 'positive float':
      try:
        user_input = float(user_input)
        if user_input < 0:
          raise ValueError
      except ValueError:
        return '\nPlease enter a positive floating number\n'

    elif type(req) == tuple and (user_input < req[0] or user_input > req[1]):
      return f'\nPlease enter a value between {req[0]} and {req[1]}\n'

  return ''


def get_user_input(message, requirements_list):
  """
  Handle all input requests: print out message to user, check
  if their answer satisfies all requirements by calling the check_input
  function. Return user_input if user answer is valid.
  """
  while True:
    user_input = input(message)
    error_message = check_input(user_input, requirements_list)
    if error_message:
      print(error_message)
    else:
      break
  return user_input

"""Conceptual design of the data structure and functions"""
# Exercise:
#   A class who's objects contain the data of one single row
#   (e.g. exercise_name, reps, weight etc)

# MuscleGroup:
#   A class who's objects describe one muscle group.
#   It contains several exercise objects belonging to a single
#   muscle group.
#   Methods():
#     calculate_volume(), calculate_tut()

def create_training_plan():
  """
  """
  # if a training table already exists, ask user if they're sure
  #   they want to delete the current table and construct a new one
  #   If user says yes, delete all current objects and data first.

  # construct plan database to contain all muscle groups:
  muscle_groups = {}
  # ask user to "enter a new muscle group or choose an existent group"
  # get group name
  # construct basic muscle group object
  group = get_group(muscle_groups)
  group.add_exercise(get_exercise())
  muscle_groups[group.name] = group # add new group to dictionary

  # choice: add another row?
  # choice: same group / different group?
  # if different group -> choose an existent group or enter a new one


def get_group(muscle_groups):
  if muscle_groups != {}:
    i = 1
    group_names = []
    message = 'Choose an option to enter a new muscle group or use an exsistent one:\n'
    message += f'{i}. New muscle group\n'
    for group in muscle_groups:
      i += 1
      group_names.append(group.name)
      message += f'{i}. {group.name}\n'
    user_input = get_user_input(message, ['integer', (1, i)])
    if user_input == 1:
      group = MuscleGroup()
      group.get_name()
    else:
      group = muscle_groups[group_names[i-2]]
  else:
    group = MuscleGroup()
    group.get_name()
  return group


def get_exercise():
  exercise = Exercise()
  exercise.get_name()
  exercise.get_sets()
  exercise.get_reps_and_weights()
  return exercise


class MuscleGroup():
  """
  A class that contains all exercise rows which belong to a given muscle group
  """
  def __init__(self):
    self.name = ''
    self.exercises = {} # MuscleGroup contains a dictionary of exercises
  
  def get_name(self, name):
    message = 'Enter name of the muscle group'
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

  def get_name(self):
    message = 'Enter name of the exercise'
    self.name = get_user_input(message, [''])
  
  def get_sets(self):
    message = 'How many sets?'
    self.sets = get_user_input(message, ['integer'])

  def get_reps_and_weights(self):
    for set in range(sets):
      message = f'How many reps in set Nr. {set+1}'
      reps = get_user_input(message, ['integer'])
      message = f'Which weight for set Nr. {set+1}'
      weight = get_user_input(message, ['positive float'])
      self.reps_and_weights.append([reps, weight])



def main_menu():
  message = main_menu_message()
  user_input = get_user_input(message, ['integer', (1, 3)])
  if user_input == 1:
    create_training_plan()
  elif user_input == 2:
    print_training_plan()
  elif user_input == 3:
    print_calculated_values()


def main():
  print(welcome_message())
  main_menu()


main()