
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

  # construct database to contain muscle groups:
  muscle_groups = {}
  # ask user "enter a new muscle group or choose an existent group"
  # get group name
  # construct group
  muscle_group = create_muscle_group(muscle_groups) # constructs an object of MuscleGroup with user input
    
  # add new group to dictionary:
  muscle_groups[muscle_group.name] = muscle_group
  # get exercise name and rest of the data
  # choice: add another row?
  # choice: same group / different group?
  # if different group -> choose an existent group or enter a new one

def create_muscle_group(muscle_groups):
  message = 'Please enter a new muscle group name'
  group_name = get_user_input(message, [''])
  # add functionality to check whether group  name already exists..
  muscle_group = MuscleGroup(group_name) # constructs an object muscle_group with name group_name
  return muscle_group


class MuscleGroup(name):
  """
  A class that contains all exercise rows which belong to a given muscle group
  """
  def __init__(self, name):
    self.name = name
    self.exercises = {} # MuscleGroup contains a dictionary of exercises
  
  def add_exercise(self, exercise):
    self.exercises[exercise.name] = exercise
  
  def calc_vol():
    """
    A method to calculate volume of the muscle group
    """
    return



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