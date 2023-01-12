# ================================ Importing libraries ===================================================
import linecache
from datetime import date
from datetime import datetime

# =================================== Define Functions ====================================================


def reg_user():  # Registers a new user to the system
    if req_username == "admin":
        new_user = str(input("Please enter a new username: "))
        while True:
            if new_user in user_list:
                print("Username already in use")
                new_user = str(input("Please enter a new username: "))
            else:
                new_pass = str(input("Please enter the new users password: "))
                new_pass_confirm = str(input("Confirm new password: "))
                if new_pass == new_pass_confirm:
                    print("Match - adding new user")
                    submit_user = f"{new_user}, {new_pass}"
                    submit_user = submit_user.strip('(')
                    print(submit_user)
                    f = open('user.txt', 'a+')
                    f.write("\n" + str(submit_user))
                    f.close()
                    break
                else:
                    print("Passwords did not match, returning to main menu")
    else:
        print("You do not have authority to perform this action")


def find_last_task_number():  # Locates the last task identifier used. Called when adding a task.
    open_tasks = open('tasks.txt', 'r')
    lines = open_tasks.readlines()
    tasks_length = len(lines)
    open_line = linecache.getline('tasks.txt', tasks_length)
    open_line = open_line.split(", ")
    last_task_number = open_line[6]
    open_tasks.close()
    return last_task_number


def add_task():  # Adds a task under a specific user, prompts for details
    which_user = input("Which user is the task for?: ")
    task_title = input("What is the title of the task?: ")
    the_task = input("Describe the task: ")
    print(f"The last task number used was {find_last_task_number()}")
    task_number = input("Enter the next task number: ")
    due = input("When is the task due? DD Month YYYY: ")
    today = date.today()
    today_date = today.strftime("%d %b %Y")
    write_to_doc = f"{which_user}, {task_title}, {the_task}, {due}, {today_date}, No, {task_number}"
    f = open('tasks.txt', 'a+')
    f.write("\n" + str(write_to_doc))
    f.close()


def write_to_tasks_txt():  # Writes changes back to tasks text when requested
    with open('tasks.txt', 'w') as f:
        for line in lines:
            f.write(line)


def view_all():  # Displays all tasks stored in the tasks text file
    open_tasks = open('tasks.txt', 'r')
    lines = open_tasks.readlines()
    for line in lines:
        temp = line.split(", ")
        print(f'''
    ----------------------------------------------------------------------
    Task:               {temp[1]}
    Assigned to:        {temp[0]}
    Date assigned:      {temp[4]}
    Due date:           {temp[3]}
    Task complete?      {temp[5]}
    Task description:
        {temp[2]}
    ----------------------------------------------------------------------
                    ''')
        open_tasks.close()


def view_mine():  # Views all tasks associated with the logged in user
    open_tasks = open('tasks.txt', 'r')
    lines = open_tasks.readlines()
    for line in lines:
        temp = line.split(", ")
        if req_username == temp[0]:
            print(f'''
    ----------------------------------------------------------------------
    Task Number:        {temp[6]}
    Task:               {temp[1]}
    Assigned to:        {temp[0]}
    Date assigned:      {temp[4]}
    Due date:           {temp[3]}
    Task complete?      {temp[5]}
    Task description:
        {temp[2]}
    ----------------------------------------------------------------------
            ''')
            continue

    for x in lines:
        task_number = int(input("Enter a task number to edit or -1 for main menu: "))
        if task_number == -1:
            break
        else:
            specific_line = linecache.getline('tasks.txt', task_number)
            print(specific_line)
            specific_line = specific_line.split(", ")
            print(specific_line)

            decision = input("Mark task as complete (M) or edit the task (E): ")
            if decision == "M":
                specific_line[5] = "Yes"
                task_number = task_number - 1
                joined = ', '.join(specific_line)
                # noinspection PyTypeChecker
                lines[task_number] = str(joined)  # Lines element x = new string
                with open('tasks.txt', 'w') as f:
                    for line in lines:
                        f.write(line)
                break

            elif decision == "E":
                user_or_date = input("Edit user (U) or due date (D): ")
                if user_or_date == "U" and (specific_line[5] == "No"):
                    new_user = input("Enter new user: ")
                    specific_line[0] = new_user
                    task_number = task_number - 1
                    joined = ', '.join(specific_line)
                    # noinspection PyTypeChecker
                    lines[task_number] = str(joined)  # Lines element x = new string
                    with open('tasks.txt', 'w') as f:
                        for line in lines:
                            f.write(line)
                    break

                elif user_or_date == "D":
                    new_date = input("Enter a new due date: ")
                    specific_line[3] = new_date
                    task_number = task_number - 1
                    joined = ', '.join(specific_line)
                    # noinspection PyTypeChecker
                    lines[task_number] = str(joined)  # Lines element x = new string
                    with open('tasks.txt', 'w') as f:
                        for line in lines:
                            f.write(line)
                    break

                elif user_or_date == "-1":
                    break

                else:
                    print("Input not accepted")

            elif decison == "-1":
                break

            else:
                print("Input not accepted")
    open_tasks.close()


def generate_reports():  # Generates reports by calling the report functions
    report_task_overview()
    report_user_overview()


def report_task_overview():  # Creates a report for task overview
    open_tasks = open('tasks.txt', 'r')
    today = datetime.today()
    today_date = today.strftime("%d %b %Y")
    today_date = datetime.strptime(today_date, "%d %b %Y")
    lines = open_tasks.readlines()
    count_num_tasks = len(lines)  # Counts num of tasks

    num_completed_tasks = 0
    num_incomplete_tasks = 0
    num_incomplete_overdue = 0
    for line in lines:
        temp = line.split(", ")
        format_date = datetime.strptime(temp[4], "%d %b %Y")
        if temp[5] == "Yes":
            num_completed_tasks += 1
        if temp[5] == "No":
            num_incomplete_tasks += 1
        if format_date < today_date and temp[5] == "No":
            num_incomplete_overdue += 1

    percent_incomplete = (num_incomplete_tasks / count_num_tasks) * 100
    percent_overdue = (num_incomplete_overdue / count_num_tasks) * 100

    # Write to file
    with open('task_overview.txt', 'w+') as f:
        overview = (f'''
        Num total tasks =                   {count_num_tasks}
        Num completed tasks =               {num_completed_tasks}
        Num incomplete tasks =              {num_incomplete_tasks}
        Num incomplete and overdue =        {num_incomplete_overdue}
        % of tasks that are incomplete =    % {percent_incomplete}
        % of tasks that are overdue =       % {percent_overdue}
        ''')
        f.write(overview)
        f.close()


def report_user_overview():  # Creates a report for user overview
    open_users = open('user.txt', 'r')
    user_lines = open_users.readlines()
    open_users.close()
    open_tasks = open('tasks.txt', 'r')
    task_lines = open_tasks.readlines()
    open_tasks.close()

    today = datetime.today()
    today_date = today.strftime("%d %b %Y")
    today_date = datetime.strptime(today_date, "%d %b %Y")

    output = f"The total number of users registered: {len(user_lines)}\n" \
             f"The total number of tasks tracked is: {len(task_lines)}"

    for user_line in user_lines:
        user_line = user_line.split(", ")
        current_user = user_line[0]

        num_assigned = 0
        num_completed = 0


        percent_completed = 0
        percent_incomplete = 0
        percent_incomplete_overdue = 0

        for task_line in task_lines:
            task_line = task_line.split(", ")
            task_user = task_line[0]
            completion = task_line[-2].strip("\n")
            format_date = datetime.strptime(task_line[4], "%d %b %Y")

            if current_user == task_user:
                num_assigned += 1

                if completion == "Yes":
                    num_completed += 1

                if format_date < today_date and task_line[5] == "No":
                    percent_incomplete_overdue += 1

        if num_assigned > 0:
            percent_completed = (num_completed/num_assigned)*100
            percent_incomplete = ((num_assigned - num_completed)/num_assigned)*100
            percent_incomplete_overdue = ((percent_incomplete_overdue/num_assigned)*100)




        output += f"\n\n\t\t{current_user}: \n" \
                  f"Num tasks assigned: {num_assigned}\n" \
                  f"Percentage assigned: {(num_assigned/len(task_lines))*100}\n" \
                  f"Percentage assigned completed: {percent_completed}\n" \
                  f"Percentage assigned to complete: {percent_incomplete}\n" \
                  f"Percent incomplete and overdue: {percent_incomplete_overdue}"

    with open('user_overview.txt', 'w') as user_overview:
        user_overview.write(output)


def generate_stats():  # Displays stats to Admin, generates new reports if not already stored
    report_user_overview()
    report_user_overview()
    with open('task_overview.txt') as open_tasks:
        tasks = open_tasks.read()
        print(tasks)
    with open('user_overview.txt') as user_open:
        users = user_open.read()
        print(users)


# ==========================================     Lists      ======================================================
user_list = []
pass_list = []

# =========================================== Login Section ======================================================
# Opens the user and pass doc and stores the usernames in user list, passwords in pass list
with open('user.txt') as f:
    for line in f:
        lines = line.split(", ")
        user_list.append(lines[0])
        pass_list.append(lines[1].strip("\n"))


# Print information to the user and request login attempt
print('''
----------------------------------------------------------------------    
    Please enter your user name and password when requested.
    Note: Inputs are case sensitive
----------------------------------------------------------------------
''')
req_username = input("\nPlease enter your username: ")
while True:
    if req_username not in user_list:
        print("Incorrect")
        req_username = input("\nPlease enter your username: ")  # If user is incorrect, request another input
    else:
        print("User Correct")
        break

req_password = input("\nPlease enter your password: ")
while True:
    if req_password not in pass_list:
        print("Incorrect")
        req_password = input("\nPlease enter your password: ")  # If password is incorrect, request another inout
    else:
        print("Password Correct")
        break

f.close()  # Closes user.txt doc

# ============================================== Next Section ======================================================
# This code is built up of menus that are presented to the user when they log in
# The menu presented is dependant upon which user is logged in
# This first section is presented if the 'admin' logs in and adds an extra statistics option
# Please continue down to the next section to see then menu for all users 'If not admin'

while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    if req_username == "admin":  # If 'admin' logs in
        menu = input('''\nSelect one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    s - Statistics
    gr - Generate report
    e - Exit
    \n: ''').lower()

        # Registering a new user
        if menu == 'r':
            reg_user()

        # Adding a new task
        elif menu == 'a':
            add_task()

        # View all tasks stored in tasks.txt doc
        elif menu == 'va':
            view_all()

        # View only my tasks
        elif menu == 'vm':
            view_mine()

        # Shows the statistics of number of tasks and number of users registered
        elif menu == "s":
            generate_stats()

        # Generates reports
        elif menu == "gr":
            generate_reports()

        # Exits the menu
        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        # Incorrect input, request another input
        else:
            print("You have made a wrong choice, Please Try again")

# ==================================== IF NOT ADMIN =====================================================
# This bank is the menu presented to all other users
# It contains all the same options other than;
    # Cannot access stats
    # Cannot register a new user

    else:
        menu = input('''\nSelect one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    e - Exit
    \n: ''').lower()

        # Registering a new user, but no access
        if menu == 'r':
            reg_user()

        # Adding a new task
        elif menu == 'a':
            add_task()

        # Viewing all tasks
        elif menu == 'va':
            view_all()

        # View my tasks
        elif menu == 'vm':
            view_mine()

        # Exit the menu
        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        # Incorrect, request another input
        else:
            print("You have made a wrong choice, Please Try again")

# Complete
