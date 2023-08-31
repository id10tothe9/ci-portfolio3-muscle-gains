# Muscle Gains
This application was built to provide a tool for a personal trainer. The trainer will be able to use it to create detailed exercise plans for his customers at the gym.

The app calculates the metrics he needs as a professional for designing suitable training plans. It also prints these data to the screen in table form and saves them to a google sheet for further usage. Furthermore it's meant as a beta version which contains the basic functionalities that will be required to build a more sophisticated application in the future.

The app was programmed with Python and uses a terminal as a user interface. A deployed version can be found [here](https://muscle-gains-c4df5a0703a2.herokuapp.com/).

![screenshot of the user terminal interface](/img/screenshot_terminal_interface.png)

## User Experience Design (UX)
### General Design
The user interacts with the program through a text interface via a terminal. The application presents the user with a list of options or with prompts and requests the entry of a piece of data or to choose an option. Depending on the goal of the user it guides them through the process of entering the necessary data.

#### User Stories
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

![Edit plan or start a new one](/img/edit_plan_or_start_new.png)

- The training plan consists of muscle groups, each muscle group can contain several exercises. Each exercise contains: number of sets, repetitions and weight for each set, cadence and rest duration.
    - A set is one continuous session of moving a specified weight repeatedly for a number of times (repetitions).
    - Cadence consists of three numbers which describe the time needed for contraction, a pause and then extension of the muscle in each set of the exercise.
    - Rest duration: the time given for a resting period after executing one set.
- Not all data is required, in that case the user can skip entering the data and the related metrics will not be calculated as a result.

![Skip entering a value](/img/skip_entering_value.png)

- If the user chooses to enter a new muscle group, but enters a name that already exists, the app recognises that and uses the available object instead of creating a new one. The user is notified accordingly.

![Entering an existent group name](/img/manual_testing/18.png)

- Choosing the second option: the training plan will be put into a table and displayed to the user. Due to the 80 characters limit of the terminal, the Reps and Weights will not be displayed, but the entire data is saved to google sheet. The user is notified as such.
    - App is designed for only one user in mind, so right now the data is being saved to one google sheet and overwritten when the user enters a new plan.

![Training plan in terminal](/img/table_terminal.png)

![Training plan in google sheet](/img/table_sheet.png)

- For missing data, the cells will be filled with '--' to indicate that no data is present here. See screenshot of google sheet above.
- Choosing the third option, the training metrics are calculated and displayed in a table to the terminal and also saved to google sheet in a separate worksheet. The following metrics are calculated for each muscle group:
    - Volume: describes the total weight that has been lifted and is calculated as:

        $\sum_{Sets} Reps * Weight$
    - Time under tension: describes the total amount of time for which the muscle group has been under tension and is calculated as:

        $\sum_{Sets} Reps * (contraction duration + extension duration)$
    - Total session duration: describes the total amount of time needed for doing all exercises of a muscle group:

        $Session Duration = Time Under Tension + (Sets * Rest Duration)$

![Metrics table in terminal](/img/metrics_terminal.png)

![Metrics table in google sheets](/img/metrics_sheet.png)


### Data Model
An object oriented programming approach was used to save and process the data entered by the user. The main class is called MuscleGroup which defines a separate object for each muscle group the user enters. This in turn contains a dictionary of objects of the class Exercise, with each Exercise object describing one exercise row entered by the user. Here is a diagram to show each of these objects along with their attributes and methods:
![Class definitions](/img/classes.jpg)

### Flowchart
The possible paths of the algorithm are depicted in the following flowchart. It shows all decision processes through which the user can go starting from the main menu options:
![Flowchart](/img/flowchart.jpg)

## Testing
In order to make sure that all user input is valid and errors are handled gracefully, a validation function was used through which all user input is sent along with specific criteria it needs to fulfil. In case of an error, the user is notified of the reason and prompted to enter the data in the correct format.
### Manual Testing

<table>
    <tr>
        <th>User Prompt</th>
        <th>Required Format</th>
        <th>Invalid Test Input</th>
        <th>Error Handling Message</th>
        <th>Test</th>
    </tr>
    <tr>
        <td>Main Menu</td>
        <td>1, 2 or 3</td>
        <td>kj</td>
        <td><img src=/img/manual_testing/1.png alt="Error 1"></td>
        <td>Pass</td>
    </tr>
    <tr>
        <td>Main Menu</td>
        <td>1, 2 or 3</td>
        <td>4</td>
        <td><img src=/img/manual_testing/2.png alt="Error 2"></td>
        <td>Pass</td>
    </tr>
    <tr>
        <td>Enter name of muscle group</td>
        <td>4 characters or more</td>
        <td>ffz</td>
        <td><img src=/img/manual_testing/3.png alt="Error 3"></td>
        <td>Pass</td>
    </tr>
    <tr>
        <td>Enter name of exercise</td>
        <td>4 characters or more</td>
        <td>12u</td>
        <td><img src=/img/manual_testing/4.png alt="Error 4"></td>
        <td>Pass</td>
    </tr>
    <tr>
        <td>How many sets?</td>
        <td>a positive integer</td>
        <td>ui</td>
        <td><img src=/img/manual_testing/5.png alt="Error 5"></td>
        <td>Pass</td>
    </tr>
    <tr>
        <td>How many sets?</td>
        <td>a positive integer</td>
        <td>2.5</td>
        <td><img src=/img/manual_testing/6.png alt="Error 6"></td>
        <td>Pass</td>
    </tr>
    <tr>
        <td>Number of repetitions</td>
        <td>a positive integer</td>
        <td>ui</td>
        <td><img src=/img/manual_testing/7.png alt="Error 7"></td>
        <td>Pass</td>
    </tr>
    <tr>
        <td>Number of repetitions</td>
        <td>a positive integer</td>
        <td>2.3</td>
        <td><img src=/img/manual_testing/8.png alt="Error 8"></td>
        <td>Pass</td>
    </tr>
    <tr>
        <td>Number of repetitions</td>
        <td>a positive integer</td>
        <td>-2</td>
        <td><img src=/img/manual_testing/9.png alt="Error 9"></td>
        <td>Pass</td>
    </tr>
    <tr>
        <td>Weight in kg</td>
        <td>a positiv float</td>
        <td>test</td>
        <td><img src=/img/manual_testing/10.png alt="Error 10"></td>
        <td>Pass</td>
    </tr>
    <tr>
        <td>Weight in kg</td>
        <td>a positiv float</td>
        <td>-20</td>
        <td><img src=/img/manual_testing/11.png alt="Error 11"></td>
        <td>Pass</td>
    </tr>
    <tr>
        <td>Cadence values</td>
        <td>three comma- or space-separated numbers</td>
        <td>2, 4 j</td>
        <td><img src=/img/manual_testing/12.png alt="Error 12"></td>
        <td>Pass</td>
    </tr>
    <tr>
        <td>Cadence values</td>
        <td>three comma- or space-separated numbers</td>
        <td>4 4 2 2</td>
        <td><img src=/img/manual_testing/13.png alt="Error 13"></td>
        <td>Pass</td>
    </tr>
    <tr>
        <td>Resting duration</td>
        <td>a positiv integer</td>
        <td>zzz</td>
        <td><img src=/img/manual_testing/14.png alt="Error 14"></td>
        <td>Pass</td>
    </tr>
    <tr>
        <td>Add another exercise?</td>
        <td>yes or no</td>
        <td>haha yes sure</td>
        <td><img src=/img/manual_testing/15.png alt="Error 15"></td>
        <td>Pass</td>
    </tr>
    <tr>
        <td>Add new muscle group or choose one</td>
        <td>1 for new group or option number of an available group</td>
        <td>3 (outside of options range)</td>
        <td><img src=/img/manual_testing/16.png alt="Error 16"></td>
        <td>Pass</td>
    </tr>
    <tr>
        <td>Add new muscle group or choose one</td>
        <td>1 for new group or option number of an available group</td>
        <td>Back</td>
        <td><img src=/img/manual_testing/17.png alt="Error 17"></td>
        <td>Pass</td>
    </tr>
</table>

Bugs discovered: table printed to terminal was long for long exercise names and does not fit in the 80 character terminal limit ➝ remove all Reps x Weight columns.

### Validator Testing
The [PEP8 online check](https://pep8ci.herokuapp.com/#) provided by CodeInstitute was used to validate the Python code. The error messages were handled until all code was clean.

[PEP8 validation before](/img/validation_pep8_before.png)

[PEP8 validation after](/img/validation_pep8_after.png)

## Deployment
This code was deployed using Code Institute's mock terminal for Heroku.
Steps for deployment:
- Fork or clone this repository
- Create a new Heroku app
- Go to the settings tab and choose 'config vars'
- Add the Key: CREDS and copy your creds.json file content to the value field
- Add the Key: PORT and its value 8000
- Go to 'Build Packs' section and add a buildpack
- Choose 'python' first, then repeat previous step and choose 'nodejs'
- Under the 'Deploy' tab choose to deploy via GitHub and connect your project
- Do a manual deploy and choose the automatic deploys option if desired

## Technologies Used:
- Python as a programming language
- [GitHub]() for hosting the repository of the project
- [GitPod]() for writing code and pushing it to GitHub
- [Heroku]() for deployment of the application
- [PEP8 online check]() to validate the python code
- [tabulate](https://pypi.org/project/tabulate/) library to display tables in the terminal
- [gspread](https://docs.gspread.org/en/latest/user-guide.html) and [google-oauth](https://pypi.org/project/google-oauth/) libraries to connect to google sheets and edit them
- [Colorama](https://pypi.org/project/colorama/) and [termcolor](https://pypi.org/project/termcolor/) libraries to print the error messages in colours

## Acknowledgement
- My brother who is a personal trainer for the inspiration for the idea of this project
- I wish to thank my mentor Marcel for his continuous guidance and encouragement!
- Code Institute for all I've learned during this programme.