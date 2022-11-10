import csv
import datetime
import re
import time

# Console color
class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OKCYAN = '\033[96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Get data and store in list , so dong
def getBufferData(path):
    buffer_data = []

    with open(path, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if len(row) > 0:
                buffer_data.append(row)
    csv_file.close()

    return buffer_data

# Write csv
def write_csv(path, new_data):
    path_log = r"E:\BI\log.txt"

    new_head = new_data[0]
    # Write new data to path_new
    with open(path_new, mode="w", newline='') as new_file:
        new_file_writer = csv.writer(new_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(new_data)):
            if i == 0:
                new_file_writer.writerow(new_head)
            else:
                new_file_writer.writerow(new_data[i])
    new_file.close()

    # Write to log, and inform to screen
    with open(path_log, "a", encoding='utf-8', newline='') as log:
        log_content = str(datetime.datetime.now()) + "\t|" + str(path_new) + "\n"
        log.write(log_content)
        log.write("-" * (len(log_content)) + "\n")
    log.close()

    # Read log and print time create file
    f = open(path_log, "r", encoding="utf-8", newline='')
    lines = f.read().split()
    str_time_new = lines[-3]
    print("+ The file has been created successfully : " + bc.OKBLUE + str(path_new) + bc.ENDC)
    print("+ Time created       : " + bc.OKBLUE + str_time_new + bc.ENDC)
    print(bc.OKCYAN + "> Write file successful !!!" + bc.ENDC)
    f.close()

# Display data of csv file . number of line read
def display_data_csv(path, num_of_lines=10):
    list_csv = []

    try:
        with open(path, mode="r", newline='') as csv_file:
            cus_reader = csv.reader(csv_file, delimiter=',')
            for i, row in enumerate(cus_reader, 0):
                list_csv.append(row)
                if i == num_of_lines:
                    break
        csv_file.close()
        head = list_csv[0]

        if len(list_csv) != 0:
            # print("\n" + bc.FAIL + "█" * 5 + bc.ENDC + " = NULL")
            print(bc.WARNING + "File content: " + bc.ENDC)
            for h in range(len(head)):
                print("{0:17s} |".format(head[h]), end='')
            print("\n" + "-" * len(head) * 19)

            regex = re.compile('[@_!#$%^&*()<>?|}{~:]')

            for row in range(1, len(list_csv)):
                for el in range(len(list_csv[row])):
                    if list_csv[row][el] == "":
                        print(bc.FAIL + "{0:17s}".format("█" * 5) + bc.ENDC + " |", end='')
                    elif regex.search(list_csv[row][el]):
                        print(bc.FAIL + bc.UNDERLINE + "{0:17s}".format(list_csv[row][el]) + bc.ENDC + " |", end='')
                    else:
                        print("{0:17s} |".format(list_csv[row][el]), end='')
                print()
        else:
            print(bc.OKCYAN + "File empty !!!" + bc.ENDC)
    except FileNotFoundError:
        print(bc.FAIL + ">> File does not exist !!!" + bc.ENDC)

# Merger data of 2 file, write to new file
def combine2file(path1, path2, path_new, encoding):
    # Get data in 2 files , add to list
    path1_data = getBufferData(path1)
    path2_data = getBufferData(path2)

    # Store new data after merge
    new_data = []
    new_head = []

    # Merge data of 2 files to new_data
    for i in range(0, len(path1_data)):
        new_data.append([])
        for j in range(9):
            if j < 2:
                new_data[i].append(path2_data[i][j])
            elif 2 <= j < 4:
                new_data[i].append(path1_data[i][j])
            elif 5 <= j:
                new_data[i].append(path2_data[i][j - 3])
        new_head = new_data[0]

    # Display new structure
    print("+ The new file will have the following columns: ")
    print("-" * 153)
    print("|", end='')
    for h in range(len(new_head)):
        print(bc.OKCYAN + "{0:17s}".format(new_head[h]) + bc.ENDC + " |", end='')
    print("\n" + "-" * 153)

    #  Confirm write new file
    confirm = input(
        "\n> Confirm file creation(" + bc.OKBLUE + "yes" + bc.ENDC + "/" + bc.ENDC + bc.FAIL + "no" + bc.ENDC + "): ")
    if confirm == "yes":
        write_csv(path_new, new_data)

# Cleaning data (clean invalid data in new file
def clean_data(path, pattern):
    data = getBufferData(path)
    new_data = []

    regex = re.compile('['+ pattern + ']')
    # Clean data
    for i in range(0, len(data)):
        new_data.append([])
        for j in range(len(data[i])):
            if j < 2:
                if data[i][j] == "":
                    new_data[i].append("NaN")
                elif regex.search(data[i][j]):
                    data[i][j] = re.sub('['+ pattern + ']', '', data[i][j])
                    new_data[i].append(data[i][j])
                else:
                    new_data[i].append(data[i][j])
            else:
                if data[i][j] == "":
                    new_data[i].append(0)
                elif regex.search(data[i][j]):
                    data[i][j] = re.sub('['+ pattern + ']', '', data[i][j])  # Replace data
                    new_data[i].append(data[i][j])
                else:
                    new_data[i].append(data[i][j])

    # Override file
    write_csv(path, new_data)

    # Read file after clean
    print("+ File after cleaning: ")
    print("\t> Empty space       : [" + bc.FAIL + "█" * 5 + bc.ENDC + "] will replace by " + bc.OKCYAN + "NaN" + bc.ENDC)
    print("\t> Special characters: [" + bc.FAIL + pattern + bc.ENDC + "] will remove")

if __name__ == '__main__':

    # Path of files
    path_revenue = r"E:\BI\movie_data.csv"
    path_quantity = r"E:\BI\tv_shows.csv"
    path_new = r"E:\BI\tets1.csv"
    bc = Bcolors()

    while True:
        print("\n" + "*" * 20 + bc.BOLD + bc.HEADER + "FILE CSV HANDING PROGRAM" + bc.ENDC + "*" * 20)
        print("-" * 18 + bc.HEADER + "The functions of the program" + bc.ENDC + "-" * 18)
        print("|\t\t\tEnter (" + bc.OKBLUE + "1" + bc.ENDC + ") : " + bc.WARNING + "{0:38s}".format("Display data") + bc.ENDC + " |")
        print("|\t\t\tEnter (" + bc.OKBLUE + "2" + bc.ENDC + ") : " + bc.WARNING + "{0:38s}".format("Merge data") + bc.ENDC + " |")
        print("|\t\t\tEnter (" + bc.OKBLUE + "3" + bc.ENDC + ") : " + bc.WARNING + "{0:38s}".format("Display data was merged") + bc.ENDC + " |")
        print("|\t\t\tEnter (" + bc.OKBLUE + "4" + bc.ENDC + ") : " + bc.WARNING + "{0:38s}".format("Clean data") + bc.ENDC + " |")
        print("|\t\t\tEnter (" + bc.OKBLUE + "5" + bc.ENDC + ") : " + bc.FAIL + "{0:38s}".format("Exit") + bc.ENDC + " |")
        print("-" * 64)
        choice = int(input("> Enter choice: "))

        # Function read file csv
        if choice == 1:
            while True:
                print("\n+ You have chosen: " + bc.OKGREEN + "Display data" + bc.ENDC)
                print("+ Choice: "
                      "\n\t\t1. Display: " + bc.OKCYAN + " tv shows." + bc.ENDC +
                      "\n\t\t2. Display: " + bc.OKCYAN + " movie data." + bc.ENDC +
                      "\n\t\t3. " + bc.FAIL + "Exit function." + bc.ENDC)

                choice_1 = int(input("> Enter choice: "))
                if choice_1 == 1:
                    num_of_line = int(input("Enter number of rows display: "))
                    print("\n+ You choose to read the file with the path:" + bc.OKBLUE + path_quantity + bc.ENDC)
                    display_data_csv(path_quantity, num_of_line)

                elif choice_1 == 2:
                    num_of_line = int(input("Enter number of rows display: "))
                    print("\n+ You choose to read the file with the path:" + bc.OKBLUE + path_revenue + bc.ENDC)
                    display_data_csv(path_revenue, num_of_line)
                elif choice_1 == 3:
                    break
                else:
                    print(bc.WARNING + "> Invalid choice, please choose again !!!" + bc.ENDC)

        # Function combine 2 files csv
        elif choice == 2:
            print("\n+ You have chosen: " + bc.OKGREEN + "Merge data" + bc.ENDC)
            combine2file(path_quantity, path_revenue, path_new)

        # Function read file csv and display invalid data
        elif choice == 3:
            print("+ You have chosen: " + bc.OKGREEN + "Display data was merged" + bc.ENDC)
            print("+ With path: " + bc.OKBLUE + path_new + bc.ENDC)
            display_data_csv(path_new)

        # Function cleaning data in new file
        elif choice == 4:
            print("+ You have chosen: " + bc.OKGREEN + "Cleaning data" + bc.ENDC)
            pattern = input("> Enter character you want to remove: ")

            clean_data(path_new, pattern)
            num_of_line = int(input("Enter number of rows display: "))
            display_data_csv(path_new)
            print(bc.OKCYAN + "> Clean data successful !!!" + bc.ENDC)

        # Exit program
        elif choice == 5:
            print(bc.OKCYAN + "> Goodbye !!!" + bc.ENDC)
            break

        # Invalid choice, return action choose function
        else:
            print(bc.WARNING + "> Invalid choice, please choose again !!!" + bc.ENDC)