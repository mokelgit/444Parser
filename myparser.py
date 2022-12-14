import re
from index import index

keywords = {"select", "create", "insert", "table"}

datatypes = {"int", "varchar", "float"}

tables_map = {}
table_name = ""
column_name = ""
column_datatype = ""
pattern = re.compile('select [a-zA-Z0-9 | *]* from ([a-zA-Z0-9]*)*')


def check(string, tables_map):
    parts = string.split(" ")
    array = parts[parts.index("from") + 1:]
    #element = parts[1:parts[parts.index("FROM") - 1]]

    for i in range(len(array)):
        array[i] = array[i].replace(",", "")
        #element[i] = element[i].replace(",", "")
    for part in array:
        if part not in tables_map.keys():
            print(part + " does not exist")
            return

        if part in keywords:
            print("INVALID. " + part + " is a keyword.")
        else:
            table = tables_map.get(part)
            keys = ""
            values = ""
            print("Here is the table after the select statement")
            for key in table:
                keys = keys + "\t\t" + key[0]
            for value in table:
                values = values + "\t\t" + value[1]
            print(keys)
            print(values)

def select(test_string):
    if bool(re.match(pattern, test_string)):
        print("This is a valid statement")
        print(test_string + "\n")
        check(test_string, tables_map)
    else:
        print("This is not a valid statement")


def create(statement):
    global tables_map
    # checking if "table" after "create"
    if statement[0] == "table" or statement[0] == "TABLE":
        statement.pop(0)
        # Making sure a keyword isn't used for a table name
        if statement[0] in keywords or statement[0] in datatypes:
            print("****Error: Can not use a keyword as a table name ****")
            exit()
        # if table name is valid, go here
        else:
            # get the table name
            table_name = statement.pop(0)
            # Add the table name to the hashmap
            tables_map[table_name] = []
            # if the next token isn't an open paranthesis, throw an error and exit
            if statement[0] != "(":
                print("****Error: you are missing an open paranthesis in your create statement ****")
                exit()
            # if the next token is an open paranthesis, continue
            else:
                # pop the open parathesis from the list
                statement.pop(0)
                creating_iteration(statement, table_name)

    # if "table" after "create" is not provided you go here
    else:
        print("****Error: create statement should be followed by the `table` keyword ****")
        exit()
    return


def creating_iteration(statement, table_name):
    # check if column name isn't a keyword, if it is, throw and error and exit
    if statement[0] in keywords or statement[0] in datatypes:
        print("****Error: Can not use a keyword as a column name ****")
        exit()
    # if the column name is valid, go here
    else:
        column_name = statement.pop(0)
        # checking if the column datatype is a supported datatype by the language, if it isn't, throw an error and exit
        if statement[0][0:7] not in datatypes:
            print("****Error: Make sure you are using a supported datatype for the columns ****")
            exit()
        # if the column datatype is valid, go here
        else:
            # checking if the column datatype is a varchar
            if statement[0][0:7] == "varchar" or statement[0][0:7] == "VARCHAR":
                # checking if the varchar datatype is given valid arguments, we only want negative numbers in the paranthesis after the varchar ex: varchar(20)
                if bool(re.match('\\([0-9]+\\)$', statement[1])):
                    column_datatype = statement.pop(0) + " " + statement.pop(0)
                    tables_map[table_name].append((column_name, column_datatype))
                # if varchar isn't given valid argument, then throw an error and exit
                else:
                    print("****Error: Make sure the datatype varchar is of this format: varchar(+ve int) ****")
                    exit()
            else:
                column_datatype = statement.pop(0)
                tables_map[table_name].append((column_name, column_datatype))
                if statement[0] != "," and statement[0] != ")":
                    print("****Error: 000Make sure you are using a supported datatype for the columns ****")
                    exit()

        if len(statement) > 0 and statement[0] == ",":
            statement.pop(0)
            creating_iteration(statement, table_name)
        elif statement[0] == ")":
            print("Compiled Sucessfully")

    return


def insert(statement):
    pass


# def select(statement):
#     pass


# --------------------- MAIN ---------------------

with open('input.txt', "r") as f:
    statements = f.read().replace('\n', ' ')

statements_array = statements.split(";")

statements_array = statements_array[0:len(statements_array) - 1]

for statement_string in statements_array:
    statement_string = " ".join(statement_string.split())
    statement = statement_string.split(" ")
    # Create Statement
    if statement[0] == "create" or statement[0] == "CREATE":
        statement.pop(0)
        create(statement)
        print(tables_map)

    # Insert Statement
    elif statement[0] == "Insert" or statement[0] == "INSERT":
        # statement.pop(0)
        # insert(statement)
        pass

    # Select Statement
    elif statement[0] == "select" or statement[0] == "SELECT":
        statement.pop(0)
        select(statement_string)
        pass
    else:
        print("****Error: Beginning of an sql statement should start with create, insert, or select ****")
        exit()
