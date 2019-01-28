"""The User Interface for the program tag translator for MOB. Only for csv file.
Tag file's first column must be tag id. Result file with user_id the same as
tag_id will cause error.
"""
import os
import csv
import codecs

__author__ = "Zihao Cai"
__date__ = "07/01/2018"

import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog


class App:
    def __init__(self, master):
        master.title('UCLoud Simple Tag Translator')
        master.geometry('700x400')


        #background setting
        background_image = tk.PhotoImage(file="background.gif")
        background_label = tk.Label(master, width = 30, height = 12,
                                    image=background_image)
        background_label.photo = background_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)


        # example for input box
        self.tag_path_var = tk.StringVar()
        self.tag_path_var.set('example: /Users/caizihao/Desktop/tag.csv')

        self.import_path_var = tk.StringVar()
        self.import_path_var.set('example: /Users/caizihao/Desktop/result.csv')

        self.export_path_var = tk.StringVar()
        self.export_path_var.set('example: '
                                 '/Users/caizihao/Desktop/processed_result.csv')

        # create frame for layout buttons and input boxes
        frame1 = tk.Frame(master, relief="groove", bd=1)
        frame1.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        frame2 = tk.Frame(master, relief="groove", bd=1)
        frame2.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        frame3 = tk.Frame(master, relief="groove", bd=1)
        frame3.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        frame4 = tk.Frame(master, relief="groove", bd=1)
        frame4.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        frame5 = tk.Frame(master, relief="groove", bd=1)
        frame5.pack(padx=5, pady=5, side=tk.TOP, expand=True)

        # labels, input boxes, and file dialog
        self.textbox_note = tk.Text(frame1, height=5, width=60)
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
        self._label_tag = tk.Label(frame2, text='mob tag files',
                                   bg='grey').pack(
            side=tk.LEFT, expand=True)

        self._tag_file_input = tk.Entry(frame2, textvariable=self.tag_path_var,
                                        width=35)
        self._tag_file_input.pack(side=tk.LEFT, expand=True)

        self._btn_tag_file_chooser = tk.Button(frame2, text='open', fg='blue',
                                               command=lambda:
                                               self.tag_file_chooser())
        self._btn_tag_file_chooser.pack(side=tk.LEFT, expand=True)

        # import file label, input box, and file dialog
        self._label_import = tk.Label(frame3, text='import result '
                                                   'file', bg='grey').pack(
            side=tk.LEFT, expand=True)
        self._import_path_input = tk.Entry(frame3,
                                           textvariable=self.import_path_var,
                                           width=35)
        self._import_path_input.pack(side=tk.LEFT, expand=True)

        self._btn_import_file_chooser = tk.Button(frame3, text='open',
                                                  fg='blue', command=lambda:
            self.import_file_chooser())
        self._btn_import_file_chooser.pack(side=tk.LEFT, expand=True)

        # export file label, input box and file dialog
        self._label_export = tk.Label(frame4, text='export file', bg='grey').\
            pack(side=tk.LEFT, expand=True)
        self._export_path_input = tk.Entry(frame4,
                                           textvariable=self.export_path_var,
                                           width=35)
        self._export_path_input.pack(side=tk.LEFT, expand=True)

        self._btn_export_file_chooser = tk.Button(frame4, text='open',
                                                  fg='blue', command=lambda:
            self.export_file_chooser())
        self._btn_export_file_chooser.pack(side=tk.LEFT, expand=True)

        # buttons
        self._execute_button = tk.Button(frame5, text='execute', fg='orange',
                                         command=lambda: self.execute_event()).pack()

    def tag_file_chooser(self):
        filename_list = tk.filedialog.askopenfilenames()
        self.tag_path_var.set(filename_list)

    def import_file_chooser(self):
        filename = tk.filedialog.askopenfilename()
        self.import_path_var.set(filename)

    def export_file_chooser(self):
        filename = tk.filedialog.askopenfilename()
        self.export_path_var.set(filename)

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
                    with open(file_path, 'r') as \
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
                        mistake_list_str = '[' + mistake_list_str[:-1] + ']'
                        column[i] = mistake_list_str

            # case 1 to 1 if this column needs translation, replace the tag
            #  code(key) with the value in the dictionary
            elif column[0] in tag_dict.keys():
                    for i in range(1, len(column)):
                        column[i] = tag_dict[column[0]].get(column[i], 'null')
            else:   # case that the column does not need translation
                pass
        return

    def execute_event(self):
        # step1: process the tag file and produce the tag dictionary
        try:
            tag_dict = self.tag_file_process(self._tag_file_input.get())
        except FileNotFoundError:
            tk.messagebox.showwarning('warning', 'invalid tag file path: ' +
                                   self._tag_file_input.get())
        except:
            tk.messagebox.showwarning('warning', 'tag file invalid data format'
                                   + self._tag_file_input.get())

        # step2: load the result csv file and the writing file
        try:
            with open(self._import_path_input.get(), 'r') as raw_data_file, \
                    open(self._export_path_input.get(),
                         'w', encoding='utf-8-sig') as \
                            processed_data_file:
                # to solved the chinese character output but it does not work
                # as expected
                #processed_data_file.write(codecs.BOM_UTF8)
                #file.write('\xEF\xBB\xBF')
                # at last the encoding = 'utf-8-sig' works in my pc

                reader = csv.reader(raw_data_file)
                writer = csv.writer(processed_data_file, dialect='excel')
                rows = []
                for row in reader:
                    row[0] = row[0].encode('utf-8').decode('utf-8-sig')
                    rows.append(row)
                print(rows)
                # now transform the row list to column list
                columns = self.row_to_column_helper(len(rows[0]), rows)

                # now process all the columns and translate all tags
                # do modifications directly on the columns list
                self.tag_translator(tag_dict, columns)

                # now transfer the columns back to rows
                output_rows = self.column_to_row_helper(columns)

                # write each row back to the csv file
                writer.writerows(output_rows)

            tk.messagebox.showinfo('message', 'job done! have a nice day!')

        except FileNotFoundError:
            tk.messagebox.showwarning('warning', 'invalid import or export path')
        # note: for debug, just comment the following except block
        except:
            tk.messagebox.showinfo('warning', 'import file invalid data '
                                              'format or export film invalid '
                                              'file type')


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()



