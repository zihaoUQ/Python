"""The User Interface for the program Applist Count. Only for csv file.
The pkg_app translation file is not necessary.
The program is meant to count the occurrence for specific search terms among
the app-lists.
Input file must follow the following format: first column must be user_id,
Second column must be AppList.
Multiple search terms must seperate by comma ','
"""
import sys
import csv


__author__ = "Zihao Cai"
__date__ = "22/01/2019"

import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog


class App:
    def __init__(self, master):
        master.title('Simple Applist Count')
        master.geometry('560x400')

        # example for input box
        self.input_path_var = tk.StringVar()
        self.input_path_var.set('example: /Users/caizihao/Desktop/input.csv')

        self.pkg_app_path_var = tk.StringVar()
        self.pkg_app_path_var.set('example: '
                                  '/Users/caizihao/Desktop/pkg_app.csv')

        self.search_term_var = tk.StringVar()
        self.search_term_var.set('example: com.xx.xxx, com.xx.xx.xxx')

        self.export_path_var = tk.StringVar()
        self.export_path_var.set('example: '
                                 '/Users/caizihao/Desktop/output.csv')

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
        frame6 = tk.Frame(master, relief='groove', bd=1)
        frame6.pack(padx=5, pady=5, side=tk.TOP, expand=True)

        # labels, input boxes, and file dialog
        self.textbox_note = tk.Text(frame1, height=5, width=60)
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
        self._label_applist = tk.Label(frame2, text='input file',
                                       bg='grey').pack(
            side=tk.LEFT, expand=True)

        self._applist_file_input = tk.Entry(frame2,
                                            textvariable=self.input_path_var,
                                            width=35)
        self._applist_file_input.pack(side=tk.LEFT, expand=True)

        self._btn_applist_file_chooser = tk.Button(frame2, text='open',
                                                fg='blue',
                                               command=lambda:
                                               self.input_file_chooser())
        self._btn_applist_file_chooser.pack(side=tk.LEFT, expand=True)

        # pkg_app_file label, input box, and file dialog button
        self._label_pkg_app = tk.Label(frame3, text='pkg app file',
                                       bg='grey').pack(side=tk.LEFT, expand=True)
        self._pkg_app_input = tk.Entry(frame3,
                                       textvariable=self.pkg_app_path_var,
                                       width=35)
        self._pkg_app_input.pack(side=tk.LEFT, expand=True)
        self._pkg_app_file_chooser = tk.Button(frame3, text='open',
                                               fg='blue', command=lambda:
            self.pkg_app_file_chooser())

        self._pkg_app_file_chooser.pack(side=tk.LEFT, expand=True)

        # search term label and input box
        self._label_search_terms = tk.Label(frame4, text='search terms',
                                      bg='grey').pack(side=tk.LEFT, expand=True)
        self._search_terms_input = tk.Entry(frame4,
                                           textvariable=self.search_term_var,
                                           width=35)
        self._search_terms_input.pack(side=tk.LEFT, expand=True)

        # output file label, input box and file dialog
        self._label_export = tk.Label(frame5, text='output file', bg='grey').\
            pack(side=tk.LEFT, expand=True)
        self._export_path_input = tk.Entry(frame5,
                                           textvariable=self.export_path_var,
                                           width=35)
        self._export_path_input.pack(side=tk.LEFT, expand=True)

        self._btn_export_file_chooser = tk.Button(frame5, text='open',
                                                  fg='blue', command=lambda:
            self.export_file_chooser())
        self._btn_export_file_chooser.pack(side=tk.LEFT, expand=True)

        # buttons
        self._execute_button = tk.Button(frame6, text='execute', fg='orange',
                                         command=lambda: self.execute_event()).pack()

    def input_file_chooser(self):
        filename = tk.filedialog.askopenfilename()
        self.input_path_var.set(filename)

    def pkg_app_file_chooser(self):
        filename = tk.filedialog.askopenfilename()
        self.pkg_app_path_var.set(filename)

    def export_file_chooser(self):
        filename = tk.filedialog.askopenfilename()
        self.export_path_var.set(filename)

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
        for list in rows_list:
            applist = list[1].strip('[').strip(']').split(',')
            for i in range(len(applist)):
                applist[i] = applist[i].strip()

            # now the applist for a single row is ready for search
            for search_term in search_terms_list:
                if search_term in applist:
                    list.append(1)
                else:
                    list.append(0)

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
        for list in rows_list:
            # transform the applist str to a list for each row
            app_list = list[1].split(',')
            for i in range(len(app_list)):
                # translation of app_list on each row
                # if the pkg is in the dict, then translate; otw, stick with
                # the pkg
                # get rid of the space, [, and ] in applist
                processed_key = app_list[i].strip().strip('[').strip(']')
                app_list[i] = translation_dict.get(processed_key,
                                                   processed_key)
            list[1] = ', '.join(app_list)

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

        except FileNotFoundError:
            tk.messagebox.showwarning('warning', 'invalid import path / file '
                                                 'not found')
            sys.exit(1)
        # note: for debug, just comment the following except block
        except:
            tk.messagebox.showinfo('warning', 'import file invalid data format')
            sys.exit(2)


        # step2: do the count and sum operation with the search terms and the
        # app_list
        output_rows = self.search_term_counter(self._search_terms_input.get(),
                                            rows)

        # step3: if the client wants to translate the pkg to app name
        try:
            pkg_app_dict= self.pkg_appname_file_process(self._pkg_app_input.get())
            # now write the result to the output file
            output_rows = self.pkg_app_translator(pkg_app_dict, output_rows)

            try:
                with open(self._export_path_input.get(), 'w',
                          encoding='utf-8-sig') as output_data_file:
                    writer = csv.writer(output_data_file, dialect='excel')
                    writer.writerows(output_rows)
                    tk.messagebox.showinfo('message',
                                           'job done! have a nice day!')

            except FileNotFoundError:
                tk.messagebox.showwarning('warning',
                                          'invalid output file path / '
                                          'file not found')
                sys.exit(5)
            # note: for debug, just comment the following except block
            except:
                tk.messagebox.showinfo('warning',
                                       'output file invalid file type')
                sys.exit(6)

        except:
            try:
                with open(self._export_path_input.get(), 'w',
                          encoding='utf-8-sig') as output_data_file:
                    writer = csv.writer(output_data_file, dialect='excel')
                    writer.writerows(output_rows)
                    tk.messagebox.showinfo('message',
                                           'job done! have a nice day!')
            except FileNotFoundError:
                tk.messagebox.showwarning('warning',
                                          'invalid output file path / '
                                          'file not found')
                sys.exit(7)
            # note: for debug, just comment the following except block
            except:
                tk.messagebox.showinfo('warning',
                                       'output file invalid file type')
                sys.exit(8)


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
