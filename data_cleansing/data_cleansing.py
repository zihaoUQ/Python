"""
The Program is design to maintain the format of the data before importing to
database. The program will do the "data cleansing" which modify or mark the
corrupt rows. The data we are looking into is results of sporting events.
This program means to make sure that the data being imported to the database
follows the format and structure rules.
"""

__author__ = "Zihao Cai"


def get_column(row, column_number) :
    """Return a string containing the data at the indicated column in the row.

    Parameters:
        row (str): String of data with comma separators (CSV format).
        column_number (int): Index of the data to be returned.

    Return:
        str: Data at 'column_number' position in 'row'

    Preconditions:
        row != None
        0 <= column_number <= maximum number of columns in 'row'
    """
    row_data = row.split(',')
    return row_data[column_number]


def replace_column(row, data, column_number) :
    """Replace the data at the indicated column in the row.

    Parameters:
        row (str): String of data with comma separators (CSV format).
        data (str): Text to replace the data at the indicated column.
        column_number (int): Index of the data to be replaced.

    Return:
        str: Updated row with 'data' in the indicated column.

    Preconditions:
        row != None and data != None
        0 <= column_number <= maximum number of columns in 'row'
    """
    row_data = row.split(',')
    row_data[column_number] = data

    # Create resulting string with updated data in column_number
    resulting_row = ""
    for column_data in row_data :
        resulting_row += column_data + ","    # Add comma between each column
    return resulting_row[:-1]           # Remove extra comma at end of string



def truncate_string(string_to_truncate, max_length) :
    """Returns a string up to 'max_length' characters in size.

    Parameters:
        string_to_truncate (str): String to be truncated.
        max_length (int): Maximum length of returned string.

    Returns:
        str: Characters 0 to max_length-1 (or end of string) from
             string_to_truncate.

    Preconditions:
        len(string_to_truncate) >= 0
        max_length >= 0
    """
    return string_to_truncate[:max_length]


def remove_athlete_id(strx):
    """ Returns the string after the first appeared comma excluding the comma.
        Design for removing the first column of the athlete_data file

        Parameter:
            strx (str): a string with seperator = ","

        Return:
            str: without the values before the first appeared comma including
            comma
    """
    n = strx.index(',')
    return strx[n + 1:]


def truncate_name(rowx, n):
    """Returns the truncated strings up to 30 characters, If the length of the
       string is greater than 30, we call the truncate_string function to do the
       trick we defined earlier.

       Parameters:
            rowx (str): a row of strings to be modified.

            n (int): indicates which column of the row will be truncated

        Return:
            str: returns the truncated strings up to 30 characters.
    """
    a = get_column(rowx, n)
    truncated_row = rowx
    if len(a) > 30:
        b = truncate_string(a, 30)
        truncated_row = replace_column(rowx, b, n)
    return truncated_row


def format_rules_names(strx):
    """Returns boolean values indicating whether the string has something
       other than letters, digits, space, hyphen & apostrophe. Design for
       the column event_name, first_name and surname.

       Parameter:
           strx (str): the data of column event name, first name and surname
           which going to undergo a format check respectively.

       Return:
           boolean: a flag with boolean value indicating whether strx follow
           the format rules.
    """
    new_strx = ""
    for x in strx:
        if x not in ["-", "'", " "]:
            new_strx += x
    return new_strx.isalnum()


def format_upper_lower(strx):
    """Return the formatted string which has the first character in uppercase
        and the rest in lowercase. Design for the column Medal which expected
        to output Gold or Silver or Bronze

        Parameters:
            strx (str): the string to be formatted

        Return:
            strx (str): the formatted string with uppercase first character
            and lowercase for the rest.
    """
    new_strx = strx
    if strx != "":
        new_strx = strx[0].upper()
        for c in strx[1:]:
            new_strx += c.lower()
    return new_strx


def constraint_place_time_score(place, score, time):
    """Return boolean True or False indicating whether column place, score and time
       follows all domain constraints.

       Parameter:
           place (str): the column place data to help checking score and time

           score (str): the column score data to be checked

           time (str): the column time data to be checked

       Return:
           Boolean: True or False indicating whether the column place,
           score and time data satisfied the constraint.
    """
    if place.isdigit():
        return (score != '') != (time != '')
    return True


def constraint_medal_place(medal, place):
    """Returns boolean value True or False indicating whether column medal and place data
       satisfied the constraint.
       ex. if medal is Gold we should have number 1 in place.

       Paramenters:
           medal (str): the string to be checked against str2

           place (str): the string to be checked against str1

       Return:
           Boolean: True of False indicating whether medal and place is consistent
    """
    return (medal == "") or ((medal == "Gold" and place == "1")
                             or (medal == "Silver" and place == "2")
                             or (medal == "Bronze" and place == "3"))


def constraint_world_record(world, olympic):
    """Return the boolean value True or False to check if column world data is not
       null then wherther column world record and column olympic record is identical or not

       Parameters:
           world (str): the column world data to be checked against column
           olympic data

           olympic (str): the column olympic data to help check column world

       Return:
           Boolean: under condition world record data is not null.Returns True
           or False indicating whether world record and olympic record is
           identical or not
    """
    return (world == "") or (world == olympic)


def name_check(strx):
    """Return boolean True or False indicating whether the column event name,
       first name and surname follows all domain constraints.

       Parameter:
           strx (str): column event name, first name and surname data to be
           checked

       Return:
           Boolean: True or False for each column event name, first name and
           surname
    """
    return ((strx != "") and (len(strx) <= 30) and format_rules_names(strx))


def countrycode_check(strx):
    """Return boolean True or False indicating whether the column country code
       follows all domain constraints.

       Parameter:
           strx (str): column country code data to be checked

       Return:
           Boolean: True or False for column country code
    """
    return ((strx != "") and (len(strx) <= 3)) and (strx.isalpha())


def place_check(strx):
    """Return boolean True or False indicating whether the column place follows all
       domain constraints.

       Parameter:
           strx (str): column place data to be checked

       Return:
           Boolean: True or False for column place
    """
    return ((len(strx) <= 3) and ((strx.isdigit())
                                  or (strx == "")
                                  or (strx == "DNS")
                                  or (strx == "DNF")
                                  or (strx == "PEN")))


def score_check(strx):
    """Return boolean True or False indicating whether the column score follows all
       domain constraints.

       Parameter:
           strx (str): the column score data to be checked

       Return:
           Boolean: True or False for column score
    """
    return (len(strx) <= 6) and (strx.isdigit()
                                 or (strx.replace(".", "", 1)).isdigit()
                                 or strx == "")


def time_check(strx):
    """Return boolean True or False indicating whether the column time follows all
       domain constraints.

       Parameter:
           strx (str): column time data to be checked

       Return:
           Boolean: True or False for column time
    """
    return (len(strx) <= 8) and (strx.isdigit()
                                 or (strx.replace(".", "", 1)).isdigit()
                                 or strx == "")


def medal_check(strx):
    """Return boolean True or False indicating whether the column medal follows all
       domain constraints.

       Parameter:
           strx (str): column medal data to be checked

       Return:
           Boolean: True or False for column medal
    """
    return ((len(strx) <= 6) and ((strx == "") or (strx in ["Gold", "Silver", "Bronze"])))


def world_olympic_check(strx):
    """Return the Boolean value True or False indicating whether column World Record
       satisfy all constraints or not

       Parameters:
           str1 (str): column olympic and column world data to be checked

       Return:
            Boolean: True or False for column World Record
     """
    return ((len(strx) <= 8) and (strx.isdigit()
                                  or (strx.replace(".", "", 1)).isdigit()
                                  or strx == ""))


def trackrecord_check(strx):
    """Return boolean True or False indicating whether the column track_record
       follows all domain constraints.

       Parameter:
           strx (str): column track_record data to be checked

       Return:
           Boolean: True or False for column track_record
    """
    strx = strx[:-1]
    return ((len(strx) <= 8) and (strx.isdigit()
                                  or (strx.replace(".", "", 1)).isdigit()
                                  or strx == ""))


def main():
    """Main functionality of program."""
    with open("athlete_data.csv", "r") as raw_data_file, \
            open("athlete_data_clean.csv", "w") as clean_data_file:
        for row in raw_data_file:
            corrupt = False
            row = remove_athlete_id(row)
            row_to_process = row  # Saves row in original state, minus athlete id.
            # Save the row data to the cleaned data file.
            # the following block checks all constraints and do the truncation

            # column event name, first name, surname check
            n = 0
            while n < 3:
                row_to_process = truncate_name(row_to_process, n)
                if not name_check(get_column(row_to_process, n)):
                    corrupt = True
                n += 1

            # column country code check
            row_to_process = replace_column(row_to_process,
                                            get_column(row_to_process, 3).upper(), 3)

            if not countrycode_check(get_column(row_to_process, 3)):
                corrupt = True

            # column place check
            if not place_check(get_column(row_to_process, 4)):
                corrupt = True

            # column score check
            if not score_check(get_column(row_to_process, 5)):
                corrupt = True

            # column time check
            if not time_check(get_column(row_to_process, 6)):
                corrupt = True

            # column medal check
            row_to_process = replace_column(row_to_process, format_upper_lower
            (get_column(row_to_process, 7)), 7)

            if not medal_check(get_column(row_to_process, 7)):
                corrupt = True

            # column olympic record and world record check
            n = 8
            while n < 10:
                if not world_olympic_check(get_column(row_to_process, n)):
                    corrupt = True
                n += 1

            # column track_record check
            if not trackrecord_check(get_column(row_to_process, 10)):
                corrupt = True

            # constraint1 place, score and time
            if not constraint_place_time_score(get_column(row_to_process, 4),
                                               get_column(row_to_process, 5),
                                               get_column(row_to_process, 6)):
                corrupt = True

            # constraint2 medal and place
            if not constraint_medal_place(get_column(row_to_process, 7),
                                          get_column(row_to_process, 4)):
                corrupt = True

            # constraint3 world record and olympic record
            if not constraint_world_record(get_column(row_to_process, 9),
                                           get_column(row_to_process, 8)):
                corrupt = True

            if not corrupt:
                clean_data_file.write(row_to_process)
            else:
                row = row[:-1]  # Remove new line character at end of row.
                clean_data_file.write(row + ",CORRUPT\n")

            # Call the main() function if this module is executed


if __name__ == "__main__":
    main()
