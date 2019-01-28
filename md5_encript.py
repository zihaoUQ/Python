"""
the program is meant to use md5_algorithm to encrypt a series of id
"""

import hashlib
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog


class App:
    def __init__(self, master):
        master.title('UCLoud Simple Tag Translator')
        master.geometry('560x400')

        # example for input box
        self.import_path_var = tk.StringVar()
        self.import_path_var.set('example: /Users/caizihao/Desktop/input.csv')

        self.export_path_var = tk.StringVar()
        self.export_path_var.set('example: /Users/caizihao/Desktop/output.csv')

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
        self.textbox_note = tk.Text(frame1, height=5, width=60)
        self.textbox_note.pack()

        self.textbox_note.insert(tk.INSERT, "md5 encryption tool;"
                                            "Only for txt file\naccept only 1 "
                                            "column of string for encrption\n"
                                         "Each single file name and path can "
                                            "not contain space\nSuggest using"
                                            " dash '_' instead of space in "
                                            "path")

        # import file label, input box, and file dialog
        self._label_import = tk.Label(frame2, text='import file', bg='grey').pack(
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
        self._execute_button = tk.Button(frame4, text='execute', fg='orange',
                                         command=lambda: self.execute_event()).pack()

    def import_file_chooser(self):
        filename = tk.filedialog.askopenfilename()
        self.import_path_var.set(filename)

    def export_file_chooser(self):
        filename = tk.filedialog.askopenfilename()
        self.export_path_var.set(filename)

    def md5_encrypt(self, key):
        """the method takes in a key and return the md5_encrypted key

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
        '''the main entry point of the program, the eventhandler for execute
        button'''
        try:
            with open(self._import_path_input.get(), 'r') as \
                    raw_data_file, \
                    open(self._export_path_input.get(),
                         'w') as \
                            processed_data_file:
                for line in raw_data_file:
                    # windows might be different \r\n
                    clean_line = line.strip().strip('\n')
                    result_key = self.md5_encrypt(clean_line.encode('utf-8'))
                    processed_data_file.write(result_key+'\n')

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
