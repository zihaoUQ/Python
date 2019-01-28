"""The program combines all the little helpers into one user interface.
"""
__author__ = "Zihao Cai"
__date__ = "07/01/2018"

import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
import csv
import hashlib
import os
import urllib.request


class InitPage:
    def __init__(self, master):
        self._master = master
        self._master.title('Little Helper')
        self._master.geometry('700x400')
        self._initPage_main_frame = tk.Frame(self._master)
        self._initPage_main_frame.pack(fill=tk.BOTH, expand=True)

        #background setting
        background_image = tk.PhotoImage(file="background.gif")
        background_label = tk.Label(self._initPage_main_frame, width = 30, height = 12,
                                    image=background_image)
        background_label.photo = background_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # frames for all the buttons
        self._frame1 = tk.Frame(self._initPage_main_frame, relief="groove", bd=1)
        self._frame1.pack(padx=2, pady=2, side=tk.TOP, expand=True)
        self._frame2 = tk.Frame(self._initPage_main_frame, relief="groove", bd=1)
        self._frame2.pack(padx=2, pady=2, side=tk.TOP, expand=True)
        self._frame3 = tk.Frame(self._initPage_main_frame, relief="groove", bd=1)
        self._frame3.pack(padx=2, pady=2, side=tk.TOP, expand=True)
        self._frame4 = tk.Frame(self._initPage_main_frame, relief="groove", bd=1)
        self._frame4.pack(padx=2, pady=2, side=tk.TOP, expand=True)
        self._frame5 = tk.Frame(self._initPage_main_frame, relief="groove", bd=1)
        self._frame5.pack(padx=2, pady=2, side=tk.TOP, expand=True)
        self._frame6 = tk.Frame(self._initPage_main_frame, relief="groove", bd=1)
        self._frame6.pack(padx=2, pady=2, side=tk.TOP, expand=True)

        # buttons to switch to different functionality/master page
        btn_md5 = tk.Button(self._frame1, text='md5加密小助手', fg='orange',
                            cursor='heart', width=18, height=2, command=lambda:
            self.change_to_md5()).pack()

        btn_clean_dup = tk.Button(self._frame2, text='去重小助手',fg='orange',
                            cursor='heart', width=18, height=2,
                                  command=lambda: self.change_to_clean_dup()).pack()

        btn_tag_translator = tk.Button(self._frame3, text='mob标签翻译小助手',
                                       fg='orange', cursor='heart', width=18,
                                       height=2, command=lambda:
            self.change_to_tag_translator()).pack()

        btn_applist_search = tk.Button(self._frame4, text='applist查询统计小助手',
                                       fg='orange', cursor='heart', width=18,
                                       height=2, command=lambda:
            self.change_to_applist_search()).pack()

        btn_api_match = tk.Button(self._frame5, text='api接口碰撞小助手',
                                  fg='orange', cursor='heart', width=18,
                                  height=2, command=lambda:
            self.change_to_api_match()).pack()

        btn_csv_file_combiner = tk.Button(self._frame6, text='大型csv文件合并小助手',
                                  fg='orange', cursor='heart', width=18,
                                  height=2, command=lambda:
            self.change_to_csv_file_combiner()).pack()

    def change_to_md5(self):
        self._initPage_main_frame.destroy()
        Md5Encrypt(self._master)

    def change_to_clean_dup(self):
        self._initPage_main_frame.destroy()
        CleanDuplicates(self._master)

    def change_to_tag_translator(self):
        self._initPage_main_frame.destroy()
        MobTagTranslator(self._master)

    def change_to_applist_search(self):
        self._initPage_main_frame.destroy()
        ApplistSearch(self._master)

    def change_to_api_match(self):
        self._initPage_main_frame.destroy()
        ApiMatch(self._master)

    def change_to_csv_file_combiner(self):
        self._initPage_main_frame.destroy()
        CsvFileCombiner(self._master)


"""
the program is meant to use md5_algorithm to encrypt a series of id
"""


class Md5Encrypt:
    def __init__(self, master):
        self._master = master
        self._master.title('MD5 Encrypt Little Helper')
        self._md5encrypt_main_frame = tk.Frame(self._master)
        self._md5encrypt_main_frame.pack(fill=tk.BOTH, expand=True)

        # example for input box
        self._import_path_var = tk.StringVar()
        self._import_path_var.set('example: /Users/caizihao/Desktop/input.csv')

        self._export_path_var = tk.StringVar()
        self._export_path_var.set('example: /Users/caizihao/Desktop/output.csv')

        # create frame for layout buttons and input boxes
        self._frame1 = tk.Frame(self._md5encrypt_main_frame, relief="groove", bd=1)
        self._frame1.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame2 = tk.Frame(self._md5encrypt_main_frame, relief="groove", bd=1)
        self._frame2.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame3 = tk.Frame(self._md5encrypt_main_frame, relief="groove", bd=1)
        self._frame3.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame4 = tk.Frame(self._md5encrypt_main_frame, relief="groove", bd=1)
        self._frame4.pack(padx=5, pady=5, side=tk.TOP, expand=True)

        # labels, input boxes, and file dialog
        self._textbox_note = tk.Text(self._frame1, height=5, width=60)
        self._textbox_note.pack()

        self._textbox_note.insert(tk.INSERT, "md5 encryption tool;"
                                            "Only for txt file\naccept only 1 "
                                            "column of string for encrption\n"
                                         "Each single file name and path can "
                                            "not contain space\nSuggest using"
                                            " dash '_' instead of space in "
                                            "path")

        # import file label, input box, and file dialog
        self._label_import = tk.Label(self._frame2, text='import file',
                                      bg='grey').pack(
            side=tk.LEFT, expand=True)
        self._import_path_input = tk.Entry(self._frame2,
                                           textvariable=self._import_path_var,
                                           width=35)
        self._import_path_input.pack(side=tk.LEFT, expand=True)

        self._btn_import_file_chooser = tk.Button(self._frame2, text='open',
                                                  fg='blue', command=lambda:
            self.import_file_chooser())
        self._btn_import_file_chooser.pack(side=tk.LEFT, expand=True)

        # export file label, input box and file dialog
        self._label_export = tk.Label(self._frame3, text='export file',
                                      bg='grey').\
            pack(side=tk.LEFT, expand=True)
        self._export_path_input = tk.Entry(self._frame3,
                                           textvariable=self._export_path_var,
                                           width=35)
        self._export_path_input.pack(side=tk.LEFT, expand=True)

        self._btn_export_file_chooser = tk.Button(self._frame3, text='open',
                                                  fg='blue', command=lambda:
            self.export_file_chooser())
        self._btn_export_file_chooser.pack(side=tk.LEFT, expand=True)

        # buttons
        self._execute_button = tk.Button(self._frame4, text='execute',
                                         fg='blue',
                                         command=lambda: self.execute_event())
        self._execute_button.pack(side=tk.LEFT, expand=True, padx=10)
        self._back_button = tk.Button(self._frame4, text='Home', fg='orange',
                                      command=lambda: self.back())
        self._back_button.pack(side=tk.RIGHT, expand=True, padx=10)

    def back(self):
        """back to homepage"""
        self._md5encrypt_main_frame.destroy()
        InitPage(self._master)

    def import_file_chooser(self):
        """pick an input file"""
        filename = tk.filedialog.askopenfilename()
        self._import_path_var.set(filename)

    def export_file_chooser(self):
        """choose the output file"""
        filename = tk.filedialog.askopenfilename()
        self._export_path_var.set(filename)

    def md5_encrypt(self, key):
        """the method takes in a key and return the md5_encrypted key. The
        core of this functionality

        Parameter: key (str) a 'nake' key
        Return: encrypted_key (str) the encrypted key
        """
        # instantiate the md5 object in hashlib module
        md5_object = hashlib.md5()
        # encrypt the key
        md5_object.update(key)
        # return the encrypted key
        encrypted_key = md5_object.hexdigest()
        return encrypted_key

    def execute_event(self):
        """the main entry point of this functionality, the event-handler for
        execute button"""
        try:
            with open(self._import_path_input.get(), 'r') as \
                    raw_data_file, \
                    open(self._export_path_input.get(),
                         'w', newline='') as \
                            processed_data_file:
                for line in raw_data_file:
                    # windows might be different \r\n
                    clean_line = line.strip().strip('\r\n')
                    result_key = self.md5_encrypt(clean_line.encode('utf-8'))
                    processed_data_file.write(result_key+'\r\n')

            tk.messagebox.showinfo('Good News', 'Job Done!')

        except Exception as e:
            tk.messagebox.showerror('error', e)


"""The program is meant to remove duplicates(user_id) of csv file base on the
 the level of details of each duplicate row. The row with the highest level of
 details(less empty column entry) will be selected for the final output.
"""


class CleanDuplicates:
    def __init__(self, master):
        self._master = master
        self._master.title('Simple Duplicate Remover')
        self._clean_dup_main_frame = tk.Frame(self._master)
        self._clean_dup_main_frame.pack(fill=tk.BOTH, expand=True)

        # example for input box
        self._import_path_var = tk.StringVar()
        self._import_path_var.set('example: /Users/caizihao/Desktop/result.csv')

        self._export_path_var = tk.StringVar()
        self._export_path_var.set('example: '
                                 '/Users/caizihao/Desktop/processed_result.csv')

        # create frame for layout buttons and input boxes
        self._frame1 = tk.Frame(self._clean_dup_main_frame, relief="groove",
                               bd=1)
        self._frame1.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame2 = tk.Frame(self._clean_dup_main_frame, relief="groove",
                               bd=1)
        self._frame2.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame3 = tk.Frame(self._clean_dup_main_frame, relief="groove",
                               bd=1)
        self._frame3.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame4 = tk.Frame(self._clean_dup_main_frame, relief="groove",
                               bd=1)
        self._frame4.pack(padx=5, pady=5, side=tk.TOP, expand=True)

        # labels, input boxes, and file dialog
        self.textbox_note = tk.Text(self._frame1, height=5, width=62)
        self.textbox_note.pack()

        self.textbox_note.insert(tk.INSERT, "Simple duplicate remover\n"
                                            "Only for csv file and Windows "
                                            "OS\n"
                                         "The import file's first column must "
                                            "be tag user id\n" 
                                            "Remove duplicate user_id based "
                                            "on the level of details of the "
                                            "input row")

        # import file label, input box, and file dialog
        self._label_import = tk.Label(self._frame2, text='import file',
                                      bg='grey').pack(
            side=tk.LEFT, expand=True)
        self._import_path_input = tk.Entry(self._frame2,
                                           textvariable=self._import_path_var,
                                           width=35)
        self._import_path_input.pack(side=tk.LEFT, expand=True)

        self._btn_import_file_chooser = tk.Button(self._frame2, text='open',
                                                  fg='blue', command=lambda:
            self.import_file_chooser())
        self._btn_import_file_chooser.pack(side=tk.LEFT, expand=True)

        # export file label, input box and file dialog
        self._label_export = tk.Label(self._frame3, text='export file',
                                      bg='grey').\
            pack(side=tk.LEFT, expand=True)
        self._export_path_input = tk.Entry(self._frame3,
                                           textvariable=self._export_path_var,
                                           width=35)
        self._export_path_input.pack(side=tk.LEFT, expand=True)

        self._btn_export_file_chooser = tk.Button(self._frame3, text='open',
                                                  fg='blue', command=lambda:
            self.export_file_chooser())
        self._btn_export_file_chooser.pack(side=tk.LEFT, expand=True)

        # buttons
        self._execute_button = tk.Button(self._frame4, text='execute',
                                         fg='blue',
                                         command=lambda: self.execute_event())
        self._execute_button.pack(side=tk.LEFT, expand=True, padx=10)
        self._back_button = tk.Button(self._frame4, text='Home', fg='orange',
                                      command=lambda: self.back())
        self._back_button.pack(side=tk.RIGHT, expand=True, padx=10)

    def back(self):
        """back to homepage"""
        self._clean_dup_main_frame.destroy()
        InitPage(self._master)

    def import_file_chooser(self):
        """choose the import file"""
        filename = tk.filedialog.askopenfilename()
        self._import_path_var.set(filename)

    def export_file_chooser(self):
        """choose the export file"""
        filename = tk.filedialog.askopenfilename()
        self._export_path_var.set(filename)

    def execute_event(self):
        """the main entry point of this functionality. the EventHandler for
        the execute button"""
        try:
            with open(self._import_path_input.get(), "r", encoding='UTF-8') as raw_data_file, \
                    open(self._export_path_input.get(), "w", encoding='UTF-8') as processed_data_file:

                id_dict = dict()
                for row in raw_data_file:
                    processing_row = row.strip('\r\n')
                    row_list = processing_row.split(",")
                    if 'unknown' in row_list[1:]:
                        pass
                    elif row_list[0] not in id_dict.keys():
                        id_dict[row_list[0]] = row_list[1:]
                    else:
                        count_dict_null = 0
                        for i in id_dict[row_list[0]]:
                            if i == '':
                                count_dict_null += 1
                        count_new_entry_null = 0
                        for i in row_list[1:]:
                            if i == '':
                                count_new_entry_null += 1
                        if count_dict_null > count_new_entry_null:
                            id_dict[row_list[0]] = row_list[1:]

                for key, value in id_dict.items():
                    new_row = ''.join(key) + ',' + ','.join(value)
                    processed_data_file.write(new_row + "\n")
                tk.messagebox.showinfo('Good News', 'Job Done!')
        except Exception as e:
            tk.messagebox.showerror('error', e)


"""The User Interface for the program tag translator for MOB. Only for csv file.
Tag file's first column must be tag id. Result file with user_id the same as
tag_id will cause error.
"""


class MobTagTranslator:
    def __init__(self, master):
        self._master = master
        master.title('Simple MOB Tag Translator')
        self._tag_translator_main_frame = tk.Frame(self._master)
        self._tag_translator_main_frame.pack(fill=tk.BOTH, expand=True)

        # example for input box
        self._tag_path_var = tk.StringVar()
        self._tag_path_var.set('example: /Users/caizihao/Desktop/tag.csv')

        self._import_path_var = tk.StringVar()
        self._import_path_var.set('example: /Users/caizihao/Desktop/result.csv')

        self._export_path_var = tk.StringVar()
        self._export_path_var.set('example: '
                                 '/Users/caizihao/Desktop/processed_result.csv')

        # create frame for layout buttons and input boxes
        self._frame1 = tk.Frame(self._tag_translator_main_frame,
                               relief="groove", bd=1)
        self._frame1.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame2 = tk.Frame(self._tag_translator_main_frame,
                               relief="groove", bd=1)
        self._frame2.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame3 = tk.Frame(self._tag_translator_main_frame,
                               relief="groove", bd=1)
        self._frame3.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame4 = tk.Frame(self._tag_translator_main_frame,
                               relief="groove", bd=1)
        self._frame4.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame5 = tk.Frame(self._tag_translator_main_frame,
                               relief="groove", bd=1)
        self._frame5.pack(padx=5, pady=5, side=tk.TOP, expand=True)

        # labels, input boxes, and file dialog
        self.textbox_note = tk.Text(self._frame1, height=5, width=60)
        self.textbox_note.pack()

        self.textbox_note.insert(tk.INSERT, "Mob tag translator;"
                                            "Only for csv file\n"
                                            "Do not use alias in SQL query,"
                                            "\n"
                                            "column name of the result table "
                                            "needs to be consistent with MOB\n"
                                         "Each single file name and path can "
                                            "not contain space\nSuggest using"
                                            " dash '_' instead of space in "
                                            "path")

        # tag file label, input box, and file dialog button
        self._label_tag = tk.Label(self._frame2, text='mob tag files',
                                   bg='grey').pack(
            side=tk.LEFT, expand=True)

        self._tag_file_input = tk.Entry(self._frame2,
                                        textvariable=self._tag_path_var,
                                        width=35)
        self._tag_file_input.pack(side=tk.LEFT, expand=True)

        self._btn_tag_file_chooser = tk.Button(self._frame2, text='open',
                                               fg='blue',
                                               command=lambda:
                                               self.tag_file_chooser())
        self._btn_tag_file_chooser.pack(side=tk.LEFT, expand=True)

        # import file label, input box, and file dialog
        self._label_import = tk.Label(self._frame3, text='import file',
                                      bg='grey').pack(side=tk.LEFT, expand=True)
        self._import_path_input = tk.Entry(self._frame3,
                                           textvariable=self._import_path_var,
                                           width=35)
        self._import_path_input.pack(side=tk.LEFT, expand=True)

        self._btn_import_file_chooser = tk.Button(self._frame3, text='open',
                                                  fg='blue', command=lambda:
            self.import_file_chooser())
        self._btn_import_file_chooser.pack(side=tk.LEFT, expand=True)

        # export file label, input box and file dialog
        self._label_export = tk.Label(self._frame4, text='export file',
                                      bg='grey').\
            pack(side=tk.LEFT, expand=True)
        self._export_path_input = tk.Entry(self._frame4,
                                           textvariable=self._export_path_var,
                                           width=35)
        self._export_path_input.pack(side=tk.LEFT, expand=True)

        self._btn_export_file_chooser = tk.Button(self._frame4, text='open',
                                                  fg='blue', command=lambda:
            self.export_file_chooser())
        self._btn_export_file_chooser.pack(side=tk.LEFT, expand=True)

        # buttons
        self._execute_button = tk.Button(self._frame5, text='execute',
                                         fg='blue',
                                         command=lambda: self.execute_event())
        self._execute_button.pack(side=tk.LEFT, expand=True, padx=10)
        self._back_button = tk.Button(self._frame5, text='Home', fg='orange',
                                      command=lambda: self.back())
        self._back_button.pack(side=tk.RIGHT, expand=True, padx=10)

    def back(self):
        """back to homepage"""
        self._tag_translator_main_frame.destroy()
        InitPage(self._master)

    def tag_file_chooser(self):
        """choose multiple tag files"""
        filename_list = tk.filedialog.askopenfilenames()
        self._tag_path_var.set(filename_list)

    def import_file_chooser(self):
        """choose the file for processing"""
        filename = tk.filedialog.askopenfilename()
        self._import_path_var.set(filename)

    def export_file_chooser(self):
        """choose the output file"""
        filename = tk.filedialog.askopenfilename()
        self._export_path_var.set(filename)

    def tag_file_process(self, multiple_files):
        """Open the tag csv file and load all the tags with their id into a
        dictionary. A dictionary inside a dictionary structure.
        file format: 1st col is the dictionary key for an inner key value
        pair where the inner key is the 2nd col tag id and the inner value is
        the 3rd col tag with real meaning, the 1st col is the column name of
        the original mob fact table.

        Parameters: multiple_files (list) multiple tag files

        Return: tag_dict (dictionary) a dictionary contains all the tags info
        """
        # the path is now becoming a string since it goes through the UI
        # text entry box, not a list or tuple any more, so we turn it to a
        # list of paths
        file_list = multiple_files.split(' ')
        # the main dictionary to store all tags
        tag_dict = dict()
        rows = []
        # now for all the tag file under the folder(root directory), we load
        # the data into the dictionary
        if len(file_list) == 0:
            tk.messagebox.showwarning('warning', 'no files chosen')
        else:
            for file_path in file_list:
                if os.path.isfile(file_path):
                    with open(file_path, 'r', encoding='utf-8') as \
                            current_tag_file:
                        # initialize the dictionary and the inner dictionary
                        reader = csv.reader(current_tag_file)
                        for row in reader:
                            # the encode, decode is use to resolve the "\ueffa"
                            # BOM-utf8 problem
                            row[0] = row[0].encode('utf-8').decode('utf-8-sig')
                            tag_dict[row[0]] = dict()
                            rows.append(row)
                        # store the tag into the dictionary
                        for row in rows:
                            # the 1st column is the main key(mob fact col name)
                            # the 2nd column is the tag id
                            # the 3rd column is the tag with real meaning
                            tag_dict[row[0]][row[1]] = row[2]

                else:
                    tk.messagebox.showinfo('warning', 'can not obtain: ' +
                                           file_path)
        return tag_dict

    def row_to_column_helper(self, col_num, rows):
        """Convert row list to column list

        Parameters:
             col_num (int) an integer specifying number of columns in a row
             rows (list) a list of row list

        Return: columns (list) the columns list contains lists of columns
        """
        columns = []
        for i in range(col_num):
            column = []
            # generate each column
            for row in rows:
                column.append(row[i])
            # append the column to the columns list
            columns.append(column)
        return columns

    def column_to_row_helper(self, columns):
        """Convert column list to row list

        Parameters:
            columns (list) a list of column list

        Return: rows (list) a list of row list
        """
        rows = []
        for i in range(len(columns[0])):
            row = []
            for col in columns:
                row.append(col[i])
            rows.append(row)
        return rows

    def tag_translator(self, tag_dict, columns_list):
        """ The core of the program. Translate the tag code to tag with real
        meaning or null if the tag code is not in the dictionary column by
        column

        Parameters:
             tag_dict (dictionary) the tag dictionary
             columns_list (list) a list contains all the column lists

        Returns: translated_columns (list) a list contains all the translated
        column lists
        """
        # translate tags column by column
        for column in columns_list:
            # first deal with special cases (group_list and tag_list)
            if column[0] == 'group_list':
                for i in range(1, len(column)):
                    group_li = column[i].split(',')
                    # translate and replace the tag code in group list directly
                    for j in range(len(group_li)):
                        group_li[j] = tag_dict[column[0]].get(group_li[j],
                                                              'null')
                    # now transfer the translated list to a string and write
                    # the string back to the column to replace the current code
                    # group; first create a str to replace each group
                    group_translated_str = ''
                    for tag in group_li:
                        group_translated_str += tag + ','
                    # now write the string back to the list, remove trailing
                    # comma
                    column[i] = group_translated_str[:-1]
            elif column[0] == 'tag_list':
                for i in range(1, len(column)):
                    if '=' in column[i]:
                        tag_prob_sep_list = column[i].split('=')
                        # so the first entry is a str of tags, the 2nd entry is
                        # a str of probability in the tag_prob_sep_list
                        tag_code_list = tag_prob_sep_list[0].split(',')
                        for j in range(len(tag_code_list)):
                            tag_code_list[j] = tag_dict[column[0]].get(
                                tag_code_list[j], 'null')
                        # now transfer the translated list to a string and write
                        # back to the column
                        tag_list_translated_str = ''
                        for tag in tag_code_list:
                            tag_list_translated_str += tag + ','
                        tag_list_translated_str = tag_list_translated_str[
                                                  :-1] + '=' + tag_prob_sep_list[1]
                        column[i] = tag_list_translated_str
                    else:   # for some mistakes without equal sign or empty
                        mistake_list = column[i].split(',')
                        for k in range(len(mistake_list)):
                            mistake_list[k] = tag_dict[column[0]].get(
                                mistake_list[k], 'null')
                        mistake_list_str = ''
                        for tag in mistake_list:
                            mistake_list_str += tag + ','

                        column[i] = mistake_list_str[:-1]

            # case 1 to 1 if this column needs translation, replace the tag
            #  code(key) with the value in the dictionary
            elif column[0] in tag_dict.keys():
                    for i in range(1, len(column)):
                        column[i] = tag_dict[column[0]].get(column[i], 'null')
            else:   # case that the column does not need translation
                pass
        return

    def execute_event(self):
        """The entry point of this functionality"""
        # step1: process the tag file and produce the tag dictionary
        try:
            tag_dict = self.tag_file_process(self._tag_file_input.get())
        except Exception as e:
            tk.messagebox.showerror('error', e)

        # step2: load the result csv file and the writing file
        try:
            with open(self._import_path_input.get(), 'r', encoding='utf-8') as raw_data_file, \
                    open(self._export_path_input.get(), 'w', encoding='utf-8-sig', newline='') as \
                            processed_data_file:
                # to solved the chinese character output but it does not work
                # as expected
                #processed_data_file.write(codecs.BOM_UTF8)
                reader = csv.reader(raw_data_file)
                writer = csv.writer(processed_data_file, dialect='excel')
                rows = []
                for row in reader:
                    row[0] = row[0].encode('utf-8').decode('utf-8-sig')
                    rows.append(row)

                # now transform the row list to column list
                columns = self.row_to_column_helper(len(rows[0]), rows)

                # now process all the columns and translate all tags
                # do modifications directly on the columns list
                self.tag_translator(tag_dict, columns)

                # now transfer the columns back to rows
                output_rows = self.column_to_row_helper(columns)

                # write each row back to the csv file
                writer.writerows(output_rows)

            tk.messagebox.showinfo('Good News', 'Job Done!')

        except Exception as e:
            tk.messagebox.showerror('error', e)


"""The User Interface for the program Applist Count. Only for csv file.
The pkg_app translation file is not necessary.
The program is meant to count the occurrence for specific search terms among
the app-lists.
Input file must follow the following format: first column must be user_id,
Second column must be AppList.
Multiple search terms must seperate by comma ','
"""


class ApplistSearch:
    def __init__(self, master):
        self._master = master
        self._master.title('Simple Applist Count')
        self._applist_search_main_frame = tk.Frame(self._master)
        self._applist_search_main_frame.pack(fill=tk.BOTH, expand=True)

        # example for input box
        self._input_path_var = tk.StringVar()
        self._input_path_var.set('example: /Users/caizihao/Desktop/input.csv')

        self._pkg_app_path_var = tk.StringVar()
        self._pkg_app_path_var.set('example: '
                                  '/Users/caizihao/Desktop/pkg_app.csv')

        self._search_term_var = tk.StringVar()
        self._search_term_var.set('example: com.xx.xxx, com.xx.xx.xxx')

        self._export_path_var = tk.StringVar()
        self._export_path_var.set('example: '
                                 '/Users/caizihao/Desktop/output.csv')

        # create frame for layout buttons and input boxes
        self._frame1 = tk.Frame(self._applist_search_main_frame, relief="groove", bd=1)
        self._frame1.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame2 = tk.Frame(self._applist_search_main_frame, relief="groove", bd=1)
        self._frame2.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame3 = tk.Frame(self._applist_search_main_frame, relief="groove", bd=1)
        self._frame3.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame4 = tk.Frame(self._applist_search_main_frame, relief="groove", bd=1)
        self._frame4.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame5 = tk.Frame(self._applist_search_main_frame, relief="groove", bd=1)
        self._frame5.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame6 = tk.Frame(self._applist_search_main_frame, relief='groove', bd=1)
        self._frame6.pack(padx=5, pady=5, side=tk.TOP, expand=True)

        # labels, input boxes, and file dialog
        self.textbox_note = tk.Text(self._frame1, height=5, width=60)
        self.textbox_note.pack()

        self.textbox_note.insert(tk.INSERT, "Simple AppList Count；"
                                            "Only for csv file\n"
                                            "multiple search terms delimit "
                                            "by comma\nThe pkg_app translation file is "
                                            "not a must\n"
                                            "Input file should have a user_id"
                                            " column as the first column,\nand "
                                            "an applist second column\n"
                                         "Each single file name and path can "
                                            "not contain space\nSuggest using"
                                            " dash '_' instead of space in "
                                            "path")

        # app_list file label, input box, and file dialog button
        self._label_applist = tk.Label(self._frame2, text='input file',
                                       bg='grey').pack(
            side=tk.LEFT, expand=True)

        self._applist_file_input = tk.Entry(self._frame2,
                                            textvariable=self._input_path_var,
                                            width=35)
        self._applist_file_input.pack(side=tk.LEFT, expand=True)

        self._btn_applist_file_chooser = tk.Button(self._frame2, text='open',
                                                fg='blue',
                                               command=lambda:
                                               self.input_file_chooser())
        self._btn_applist_file_chooser.pack(side=tk.LEFT, expand=True)

        # pkg_app_file label, input box, and file dialog button
        self._label_pkg_app = tk.Label(self._frame3, text='pkg app file',
                                       bg='grey').pack(side=tk.LEFT, expand=True)
        self._pkg_app_input = tk.Entry(self._frame3,
                                       textvariable=self._pkg_app_path_var,
                                       width=35)
        self._pkg_app_input.pack(side=tk.LEFT, expand=True)
        self._pkg_app_file_chooser = tk.Button(self._frame3, text='open',
                                               fg='blue', command=lambda:
            self.pkg_app_file_chooser())

        self._pkg_app_file_chooser.pack(side=tk.LEFT, expand=True)

        # search term label and input box
        self._label_search_terms = tk.Label(self._frame4, text='search terms',
                                      bg='grey').pack(side=tk.LEFT, expand=True)
        self._search_terms_input = tk.Entry(self._frame4,
                                           textvariable=self._search_term_var,
                                           width=35)
        self._search_terms_input.pack(side=tk.LEFT, expand=True)

        # output file label, input box and file dialog
        self._label_export = tk.Label(self._frame5, text='output file', bg='grey').\
            pack(side=tk.LEFT, expand=True)
        self._export_path_input = tk.Entry(self._frame5,
                                           textvariable=self._export_path_var,
                                           width=35)
        self._export_path_input.pack(side=tk.LEFT, expand=True)

        self._btn_export_file_chooser = tk.Button(self._frame5, text='open',
                                                  fg='blue', command=lambda:
            self.export_file_chooser())
        self._btn_export_file_chooser.pack(side=tk.LEFT, expand=True)

        # buttons
        self._execute_button = tk.Button(self._frame6, text='execute',
                                         fg='blue',
                                         command=lambda: self.execute_event())
        self._execute_button.pack(side=tk.LEFT, expand=True, padx=10)

        self._back_button = tk.Button(self._frame6, text='Home', fg='orange',
                                      command=lambda: self.back())
        self._back_button.pack(side=tk.RIGHT, expand=True, padx=10)

    def back(self):
        """back to homepage"""
        self._applist_search_main_frame.destroy()
        InitPage(self._master)

    def input_file_chooser(self):
        """choose the input file"""
        filename = tk.filedialog.askopenfilename()
        self._input_path_var.set(filename)

    def pkg_app_file_chooser(self):
        """choose the pkg_app_name file"""
        filename = tk.filedialog.askopenfilename()
        self._pkg_app_path_var.set(filename)

    def export_file_chooser(self):
        """choose the output file"""
        filename = tk.filedialog.askopenfilename()
        self._export_path_var.set(filename)

    def pkg_appname_file_process(self, file_path):
        """Open the pkg_appname csv file(MOB) and load all the pkg name with
        app name into a dictionary. The key is the pkg name, the value is the
        app name. The file should have the following structure: 1st column
         is the pkg name, second column is the app name

        Parameters: file_path (str) the pkg_appname_file path

        Return: tag_dict (dictionary) a dictionary contains all the pkg and
        app_name info
        """
        pkg_app_dict = dict()
        with open(file_path, 'r', encoding='utf-8') as pkg_app_file:
            reader = csv.reader(pkg_app_file)
            for row in reader:
                row[0] = row[0].encode('utf-8').decode('utf-8-sig')
                pkg_app_dict[row[0].strip()] = row[1].strip()

        return pkg_app_dict

    def search_term_counter(self, search_terms, rows_list):
        """ The core of the program. Search the target app name in each
        user's app-list and count the occurrence, and also output a sum for
        each search terms.

        Parameters:
             search_terms (str) a str of search terms
             rows_list (list) a list contains all the column lists

        Returns: (list) a list of lists, each inner list represents a
        processed row with user_id, applist, frequency for each search terms
        """

        # step1 process the search terms
        search_terms_list = search_terms.split(',')
        for i in range(len(search_terms_list)):
            search_terms_list[i] = search_terms_list[i].strip()
        # step2 process the rows_list and output the calculated rows_list
        # add a header row to the rows_list
        for ls in rows_list:
            applist = ls[1].strip('[').strip(']').split(',')
            for i in range(len(applist)):
                applist[i] = applist[i].strip()

            # now the applist for a single row is ready for search
            for search_term in search_terms_list:
                if search_term in applist:
                    ls.append(1)
                else:
                    ls.append(0)

        # step3 add a sum row
        last_row_list = ['total', 'sum(frequency)']
        # for each index except the first 2 column which are the user_id and
        # the applist, create a counter to sum the frequency for each app pkg
        for i in range(2, len(rows_list[0])):
            count = 0
            for list in rows_list[1:]:
                count += list[i]
            last_row_list.append(count)

        # now sum up all pkg sum
        sum = 0
        for number in last_row_list[2:]:
            sum += number
        last_row_list.append(sum)

        # now add the last row list to the rows_list
        rows_list.append(last_row_list)

        # append header row
        header = ['user_id', 'app_list']
        header.extend(search_terms_list)
        rows_list.insert(0, header)

        return rows_list

    def pkg_app_translator(self, translation_dict, rows_list):
        """The program is meant to translate pkg names to real app names

        Parameters:
            translation_dict: (dict) the pkg_app dictionary
            rows_list: (list) a big list of lists of rows in the original file

        Returns: (list) the modified rows_list
        """
        for ls in rows_list:
            # transform the applist str to a list for each row
            app_list = ls[1].split(',')
            for i in range(len(app_list)):
                # translation of app_list on each row
                # if the pkg is in the dict, then translate; otw, stick with
                # the pkg
                # get rid of the space, [, and ] in applist
                processed_key = app_list[i].strip().strip('[').strip(']')
                app_list[i] = translation_dict.get(processed_key,
                                                   processed_key)
            ls[1] = ', '.join(app_list)

        # also translate the first row
        for i in range(len(rows_list[0])):
            rows_list[0][i] = translation_dict.get(rows_list[0][i], rows_list[0][i])

        return rows_list

    def execute_event(self):
        """the main entry point of the whole program"""
        # step1: load the app_list csv file
        try:
            with open(self._applist_file_input.get(), 'r', encoding='utf-8') as \
                    raw_data_file:

                reader = csv.reader(raw_data_file)
                rows = []
                for row in reader:
                    row[0] = row[0].encode('utf-8').decode('utf-8-sig')
                    rows.append(row)

        except Exception as e:
            tk.messagebox.showerror('error', e)

        # step2: do the count and sum operation with the search terms and the
        # app_list
        output_rows = self.search_term_counter(self._search_terms_input.get(),
                                            rows)

        # step3: if the client wants to translate the pkg to app name
        try:
            pkg_app_dict = self.pkg_appname_file_process(
                self._pkg_app_input.get())
            # now write the result to the output file
            output_rows = self.pkg_app_translator(pkg_app_dict, output_rows)

            try:
                with open(self._export_path_input.get(), 'w',
                          encoding='utf-8-sig') as output_data_file:
                    writer = csv.writer(output_data_file, dialect='excel')
                    writer.writerows(output_rows)
                    tk.messagebox.showinfo('message',
                                           'job done! have a nice day!')

            except Exception as e:
                tk.messagebox.showerror('error', e)

        except:
            try:
                with open(self._export_path_input.get(), 'w',
                          encoding='utf-8-sig') as output_data_file:
                    writer = csv.writer(output_data_file, dialect='excel')
                    writer.writerows(output_rows)
                    tk.messagebox.showinfo('message',
                                           'job done! have a nice day!')
            except Exception as e:
                tk.messagebox.showerror('error', e)



"""
the program is meant to take in a series of id and an api, after the
communication between the id and api, we store the output in txt file
"""


class ApiMatch:
    def __init__(self, master):
        self._master = master
        master.title('SIMPLE API MATCHER')
        self._api_match_main_frame = tk.Frame(self._master)
        self._api_match_main_frame.pack(fill=tk.BOTH, expand=True)

        # example for input box
        self._import_path_var = tk.StringVar()
        self._import_path_var.set('example: /Users/caizihao/Desktop/input.csv')

        self._url_path_var = tk.StringVar()
        self._url_path_var.set('example: '
                              'http://120.132.88.888:8888/match/b50a99cb/<target>')

        self._export_path_var = tk.StringVar()
        self._export_path_var.set('example: /Users/caizihao/Desktop/output.csv')

        self._ratio_var = tk.StringVar()

        # create frame for layout buttons and input boxes
        self._frame1 = tk.Frame(self._api_match_main_frame, relief="groove", bd=1)
        self._frame1.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame2 = tk.Frame(self._api_match_main_frame, relief="groove", bd=1)
        self._frame2.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame3 = tk.Frame(self._api_match_main_frame, relief="groove", bd=1)
        self._frame3.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame4 = tk.Frame(self._api_match_main_frame, relief="groove", bd=1)
        self._frame4.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame5 = tk.Frame(self._api_match_main_frame, relief="groove", bd=1)
        self._frame5.pack(padx=5, pady=5, side=tk.TOP, expand=True)

        # labels, input boxes, and file dialog
        self.textbox_note = tk.Text(self._frame1, height=5, width=60)
        self.textbox_note.pack()

        self.textbox_note.insert(tk.INSERT, "API_ID match tool;"
                                            "Only for txt file\naccept only 1 "
                                            "column of string for the "
                                            "match\nMake sure the input txt "
                                            "does not have any extra space,\n"
                                            "empty newline in the end\n"
                                         "Each single file name and path can "
                                            "not contain space\nSuggest using"
                                            " dash '_' instead of space in "
                                            "path")

        # import file label, input box, and file dialog
        self._label_import = tk.Label(self._frame2, text='import file', bg='grey').pack(
            side=tk.LEFT, expand=True)
        self._import_path_input = tk.Entry(self._frame2,
                                           textvariable=self._import_path_var,
                                           width=35)
        self._import_path_input.pack(side=tk.LEFT, expand=True)

        self._btn_import_file_chooser = tk.Button(self._frame2, text='open',
                                                  fg='blue', command=lambda:
            self.import_file_chooser())
        self._btn_import_file_chooser.pack(side=tk.LEFT, expand=True)

        # the api url label, input box
        self._label_url = tk.Label(self._frame3, text='API(URL)', bg='grey').pack(
            side=tk.LEFT, expand=True)
        self._url_input = tk.Entry(self._frame3, textvariable=self._url_path_var,
                                   width=35)
        self._url_input.pack(side=tk.LEFT, expand=True)

        # export file label, input box and file dialog
        self._label_export = tk.Label(self._frame4, text='export file', bg='grey').\
            pack(side=tk.LEFT, expand=True)
        self._export_path_input = tk.Entry(self._frame4,
                                           textvariable=self._export_path_var,
                                           width=35)
        self._export_path_input.pack(side=tk.LEFT, expand=True)

        self._btn_export_file_chooser = tk.Button(self._frame4, text='open',
                                                  fg='blue', command=lambda:
            self.export_file_chooser())
        self._btn_export_file_chooser.pack(side=tk.LEFT, expand=True)

        # buttons and rate label
        self._label_ratio = tk.Label(self._frame5, text='ratio:', bg='grey').pack(
            side=tk.LEFT, expand=True)
        # the disabled state make the entry box looks sexy and untouchable
        self._Entry_ratio = tk.Entry(self._frame5, textvariable=self._ratio_var,
                                   width=10, state='disabled')
        self._Entry_ratio.pack(side=tk.LEFT, expand=True, padx=10)
        self._execute_button = tk.Button(self._frame5, text='execute',
                                         fg='blue', command=lambda:
            self.execute_event()).pack(side=tk.LEFT, expand=True)

        self._back_button = tk.Button(self._frame5, text='Home', fg='orange',
                                      command=lambda: self.back())
        self._back_button.pack(side=tk.LEFT, expand=True, padx=5)

    def back(self):
        """back to homepage"""
        self._api_match_main_frame.destroy()
        InitPage(self._master)

    def import_file_chooser(self):
        """select import file"""
        filename = tk.filedialog.askopenfilename()
        self._import_path_var.set(filename)

    def export_file_chooser(self):
        """choose output file"""
        filename = tk.filedialog.askopenfilename()
        self._export_path_var.set(filename)

    def api_dealer(self, api_url):
        """the core of the program. the function send request to api and get
        the response
        Parameters: api_url (str) the url of the api
        Return: response (str) the response without any stupid space
        """
        # send request to api
        http_request = urllib.request.urlopen(api_url)
        # get the response( convert bytes response to str)
        response = bytes.decode(http_request.read())

        return response.strip()


    def execute_event(self):
        """the main entry point of this functionality, the event-handler for
        execute
        button"""
        try:
            with open(self._import_path_input.get(), 'r') as \
                    raw_data_file, \
                    open(self._export_path_input.get(),
                         'w', newline='') as processed_data_file:

                # all situation counter
                count_true = 0
                count_false = 0
                count_tag = 0
                count_not_found = 0

                # get the user input api(url)
                original_url = self._url_input.get()

                # true/false and tag/NotFound flags
                flag_true_false = False
                flag_tag_notfound = False

                # set the flag
                temp_line = raw_data_file.readline().strip().strip('\r\n')
                temp_clean_url = original_url[:-8] + temp_line
                temp_response = self.api_dealer(temp_clean_url)
                if temp_response == 't' or temp_response == 'f':
                    flag_true_false = True
                else:
                    flag_tag_notfound = True

                # process the file
                for line in raw_data_file:
                    clean_line = line.strip().strip('\r\n')
                    if clean_line == '':
                        tk.messagebox.showinfo('info', 'end of file or '
                                                       'unexpected newline in '
                                                       'the end')
                        break
                    # get rid of the '<target>' ending of the original url
                    # and combine with the real target
                    clean_url = original_url[:-8] + clean_line
                    response = self.api_dealer(clean_url)

                    # deal with different kinds of output and update the counter
                    if response == 't':
                        count_true += 1
                    elif response == 'f':
                        count_false += 1
                    elif response == 'Not Found':
                        count_not_found += 1
                    else:
                        count_tag += 1

                    # create the output row and write to file
                    output_row = clean_line + '     ' + response + '\r\n'
                    processed_data_file.write(output_row)

                # now output the ratio
                if flag_true_false:
                    self._ratio_var.set(str(count_true) + '/' + str(
                        count_true + count_false))
                elif flag_tag_notfound:
                    self._ratio_var.set(str(count_tag) + '/' + str(count_tag
                                                                   + count_not_found))

            tk.messagebox.showinfo('message', 'job done! have a nice day!')

        except Exception as e:
            tk.messagebox.showerror('error', e)


"""This functionality is about to take several large csv files with huge 
number of rows of data, and combine them into one csv file"""


class CsvFileCombiner:
    def __init__(self, master):
        self._master = master
        master.title('Simple Csv File Combiner')
        self._combiner_main_frame = tk.Frame(self._master)
        self._combiner_main_frame.pack(fill=tk.BOTH, expand=True)

        # example for input box
        self._import_path_var = tk.StringVar()
        self._import_path_var.set(
            'example: /Users/caizihao/Desktop/result.csv')

        self._export_path_var = tk.StringVar()
        self._export_path_var.set('example: '
                                  '/Users/caizihao/Desktop/processed_result.csv')

        self._num_of_rows_var = tk.StringVar()

        # create frame for layout buttons and input boxes
        self._frame1 = tk.Frame(self._combiner_main_frame,
                                relief="groove", bd=1)
        self._frame1.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame2 = tk.Frame(self._combiner_main_frame,
                                relief="groove", bd=1)
        self._frame2.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame3 = tk.Frame(self._combiner_main_frame,
                                relief="groove", bd=1)
        self._frame3.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        self._frame4 = tk.Frame(self._combiner_main_frame,
                                relief="groove", bd=1)
        self._frame4.pack(padx=5, pady=5, side=tk.TOP, expand=True)

        # labels, input boxes, and file dialog
        self.textbox_note = tk.Text(self._frame1, height=5, width=60)
        self.textbox_note.pack()

        self.textbox_note.insert(tk.INSERT, "CSV file row combiner;"
                                            "Only for csv file\n"
                                            "Each single file name and path can "
                                            "not contain space\nSuggest using"
                                            " dash '_' instead of space in "
                                            "path")


        # import file label, input box, and file dialog
        self._label_import = tk.Label(self._frame2,
                                      text='import file', bg='grey').pack(
            side=tk.LEFT, expand=True)
        self._import_path_input = tk.Entry(self._frame2,
                                           textvariable=self._import_path_var,
                                           width=35)
        self._import_path_input.pack(side=tk.LEFT, expand=True)

        self._btn_import_file_chooser = tk.Button(self._frame2,
                                                  text='open',
                                                  fg='blue',
                                                  command=lambda:
                                                  self.import_file_chooser())
        self._btn_import_file_chooser.pack(side=tk.LEFT, expand=True)

        # export file label, input box and file dialog
        self._label_export = tk.Label(self._frame3, text='export file',
                                      bg='grey'). \
            pack(side=tk.LEFT, expand=True)
        self._export_path_input = tk.Entry(self._frame3,
                                           textvariable=self._export_path_var,
                                           width=35)
        self._export_path_input.pack(side=tk.LEFT, expand=True)

        self._btn_export_file_chooser = tk.Button(self._frame3,
                                                  text='open',
                                                  fg='blue',
                                                  command=lambda:
                                                  self.export_file_chooser())
        self._btn_export_file_chooser.pack(side=tk.LEFT, expand=True)

        # buttons
        # buttons and rate label
        self._label_ratio = tk.Label(self._frame4, text='number of rows:',
                                     bg='grey').pack(
            side=tk.LEFT, expand=True)
        # the disabled state make the entry box looks sexy and untouchable
        self._Entry_ratio = tk.Entry(self._frame4, textvariable=self._num_of_rows_var,
                                     width=10, state='disabled')
        self._Entry_ratio.pack(side=tk.LEFT, expand=True, padx=10)
        self._execute_button = tk.Button(self._frame4, text='execute',
                                         fg='blue', command=lambda:
            self.execute_event()).pack(side=tk.LEFT, expand=True)

        self._back_button = tk.Button(self._frame4, text='Home', fg='orange',
                                      command=lambda: self.back())
        self._back_button.pack(side=tk.LEFT, expand=True, padx=5)

    def back(self):
        """back to homepage"""
        self._combiner_main_frame.destroy()
        InitPage(self._master)

    def import_file_chooser(self):
        """choose multiple import files"""
        filename = tk.filedialog.askopenfilenames()
        self._import_path_var.set(filename)

    def export_file_chooser(self):
        """choose export file"""
        filename = tk.filedialog.askopenfilename()
        self._export_path_var.set(filename)

    def execute_event(self):
        """the main entry point of this functionality"""
        try:
            file_list = self._import_path_input.get().split(' ')
            # the main dictionary to store all tags
            all_rows = []
            count = 0
            # now for all the tag file under the folder(root directory), we load
            # the data into the dictionary
            if len(file_list) == 0:
                tk.messagebox.showwarning('warning', 'no files chosen')
            else:
                for file_path in file_list:
                    if os.path.isfile(file_path):
                        with open(file_path, 'r', encoding='utf-8') as \
                                input_file:
                            # initialize the dictionary and the inner dictionary
                            reader = csv.reader(input_file)
                            for row in reader:
                                count += 1
                                row[0] = row[0].encode('utf-8').decode('utf-8-sig')
                                all_rows.append(row)
                    else:
                        tk.messagebox.showerror('warning', 'can not obtain: ' +
                                                file_path)

            with open(self._export_path_input.get(), 'w',
                      encoding='utf-8-sig', newline='') \
                    as output_file:
                writer = csv.writer(output_file, dialect='excel')
                writer.writerows(all_rows)
                self._num_of_rows_var.set(count)
                tk.messagebox.showinfo('Good News', 'Job Done!')

        except Exception as e:
            tk.messagebox.showerror('error', e)


def main():
    root = tk.Tk()
    InitPage(root)
    root.mainloop()


if __name__ == '__main__':
    main()



