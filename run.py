
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


def main_menu():
  message = main_menu_message()
  user_input = get_user_input(message, ['integer', (1, 3)])
  if user_input == 1:
    create_training_table()
  elif user_input == 2:
    print_training_table()
  elif user_input == 3:
    print_calculated_values()


def main():
  print(welcome_message())
  main_menu()


main()