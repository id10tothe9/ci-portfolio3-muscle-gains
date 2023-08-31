# Muscle Gains
This application was built to provide a tool for a personal trainer. The trainer will be able to use it to create detailed exercise plans for his customers at the gym.

The app calculates the metrics he needs as a professional for designing suitable training plans. It also prints these data to the screen in table form and saves them to a google sheet for further usage. Furthermore it's meant as a beta version which contains the basic functionalities that will be required to build a more sophisticated application in the future.

The app was programmed with Python and uses a terminal as a user interface. A deployed version can be found [here](https://muscle-gains-c4df5a0703a2.herokuapp.com/).

![screenshot of the user terminal interface](/img/screenshot_terminal_interface.png)

## User Experience Design (UX)
### General Design
The user interacts with the program through a text interface via a terminal. The application presents the user with a list of options or with prompts and requests the entry of a piece of data or to choose an option. Depending on the goal of the user it guides them through the process of entering the necessary data.

#### User Stories:
- As a user I want to easily understand what the application is about and how to use it
- As a user I want to be guided step by step to provide the data needed for the program
- As a user I want to be gracefully notified when I enter bad data and to be informed about the exact reason and how to provide the needed data correctly.
- As a user I want to get the results I'm looking for in an organised format that I can easily read and understand
- As a user I want to have the data I generated available for later use (google sheet)

### Features
- Welcome message: at the beginning the user is greeted with a message that explains the purpose of the application and the scope of the available functionalities (see screenshot of terminal above).
- Main menu options (a list of options for the user to choose from):
    1. Create a training plan
    2. Display current training plan
    3. Display calculated metrics
- Choosing the first option: the user is guided through a series of prompts to enter the required data for each new exercise. All data is validated and if not valid, the user is notified with a clarifying message (in red) and asked to enter a new response.
- Edit available plan: the user can continue editing their plan after returning to the main menu by choosing option 1 again. In that case they're asked if they want to start a new plan or continue with the current one.