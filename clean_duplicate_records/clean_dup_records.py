"""The program is meant to remove duplicates(user_id) of csv file base on the
 the level of details of each duplicate row. The row with the highest level of
 details(less empty column entry) will be selected for the final output.
"""

__author__ = "Zihao Cai"
__date__ = "07/01/2018"

import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog


class App:
    def __init__(self, master):
        master.title('UCLoud Simple Duplicate Remover')

        # example for input box
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

        # labels, input boxes, and file dialog
        self.textbox_note = tk.Text(frame1, height=5, width=62)
        self.textbox_note.pack()

        self.textbox_note.insert(tk.INSERT, "UCloud simple duplicate remover \r\n"
                                            "Only for csv file\r\n"
                                         "The import file's first column must "
                                            "be tag user id\r\n" 
                                            "Remove duplicate user_id based "
                                            "on the level of details of the "
                                            "input row")

        # import file label, input box, and file dialog
        self._label_import = tk.Label(frame2, text='import result '
                                                   'file', bg='grey').pack(
            side=tk.LEFT, expand=True)
        self._import_path_input = tk.Entry(frame2,
                                           textvariable=self.import_path_var,
                                           width=35)
        self._import_path_input.pack(side=tk.LEFT, expand=True)

        self._btn_import_file_chooser = tk.Button(frame2, text='open',
                                                  fg='blue', command=lambda:
            self.import_file_chooser())
        self._btn_import_file_chooser.pack(side=tk.LEFT, expand=True)

        # export file label, input box and file dialog
        self._label_export = tk.Label(frame3, text='export file', bg='grey').\
            pack(side=tk.LEFT, expand=True)
        self._export_path_input = tk.Entry(frame3,
                                           textvariable=self.export_path_var,
                                           width=35)
        self._export_path_input.pack(side=tk.LEFT, expand=True)

        self._btn_export_file_chooser = tk.Button(frame3, text='open',
                                                  fg='blue', command=lambda:
            self.export_file_chooser())
        self._btn_export_file_chooser.pack(side=tk.LEFT, expand=True)

        # buttons
        self._execute_button = tk.Button(frame4, text='execute', fg='blue',
                                         command=lambda: self.execute_event()).\
            pack()

    def import_file_chooser(self):
        filename = tk.filedialog.askopenfilename()
        self.import_path_var.set(filename)

    def export_file_chooser(self):
        filename = tk.filedialog.askopenfilename()
        self.export_path_var.set(filename)

    def execute_event(self):
        try:
            with open(self._import_path_input.get(), "r") as raw_data_file, \
                    open(self._export_path_input.get(),
                         "w") as processed_data_file:

                id_dict = dict()
                for row in raw_data_file:
                    processing_row = row.strip('\r\n')
                    row_list = processing_row.split(",")
                    if row_list[0] not in id_dict.keys():
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
                    processed_data_file.write(new_row + "\r\n")
                tk.messagebox.showinfo('message', 'job done! have a nice day!')
        except FileNotFoundError:
            tk.messagebox.showinfo('warning', 'invalid import or export path')
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


