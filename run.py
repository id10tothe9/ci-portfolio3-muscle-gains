
def welcome_message():
  return "Welcome!\n"


def main_menu_message():
  return """Choose an option:
  1. Create a new training plan
  2. Display current training plan
  3. Display calculated values\n"""


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


def main():
  print(welcome_message())
  main_menu()