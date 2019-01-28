"""
the program is meant to take in a series of id and an api, after the
communication between the id and api, we store the output in txt file
"""

import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
import urllib.request


class App:
    def __init__(self, master):
        self._master = master
        self._master.title('SIMPLE API MATCHER')
        self._master.geometry('560x400')
        self._app_main_frame = tk.Frame(self._master).pack()

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
        frame1 = tk.Frame(self._app_main_frame, relief="groove", bd=1)
        frame1.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        frame2 = tk.Frame(self._app_main_frame, relief="groove", bd=1)
        frame2.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        frame3 = tk.Frame(self._app_main_frame, relief="groove", bd=1)
        frame3.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        frame4 = tk.Frame(self._app_main_frame, relief="groove", bd=1)
        frame4.pack(padx=5, pady=5, side=tk.TOP, expand=True)
        frame5 = tk.Frame(self._app_main_frame, relief="groove", bd=1)
        frame5.pack(padx=5, pady=5, side=tk.TOP, expand=True)

        # labels, input boxes, and file dialog
        self.textbox_note = tk.Text(frame1, height=5, width=60)
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
        self._label_import = tk.Label(frame2, text='import file', bg='grey').pack(
            side=tk.LEFT, expand=True)
        self._import_path_input = tk.Entry(frame2,
                                           textvariable=self._import_path_var,
                                           width=35)
        self._import_path_input.pack(side=tk.LEFT, expand=True)

        self._btn_import_file_chooser = tk.Button(frame2, text='open',
                                                  fg='blue', command=lambda:
            self.import_file_chooser())
        self._btn_import_file_chooser.pack(side=tk.LEFT, expand=True)

        # the api url label, input box
        self._label_url = tk.Label(frame3, text='API(URL)', bg='grey').pack(
            side=tk.LEFT, expand=True)
        self._url_input = tk.Entry(frame3, textvariable=self._url_path_var,
                                   width=35)
        self._url_input.pack(side=tk.LEFT, expand=True)

        # export file label, input box and file dialog
        self._label_export = tk.Label(frame4, text='export file', bg='grey').\
            pack(side=tk.LEFT, expand=True)
        self._export_path_input = tk.Entry(frame4,
                                           textvariable=self._export_path_var,
                                           width=35)
        self._export_path_input.pack(side=tk.LEFT, expand=True)

        self._btn_export_file_chooser = tk.Button(frame4, text='open',
                                                  fg='blue', command=lambda:
            self.export_file_chooser())
        self._btn_export_file_chooser.pack(side=tk.LEFT, expand=True)

        # buttons and rate label
        self._label_ratio = tk.Label(frame5, text='ratio:', bg='grey').pack(
            side=tk.LEFT, expand=True)
        # the disabled state make the entry box looks sexy and untouchable
        self._Entry_ratio = tk.Entry(frame5, textvariable=self._ratio_var,
                                   width=10, state='disabled')
        self._Entry_ratio.pack(side=tk.LEFT, expand=True, padx=10)
        self._execute_button = tk.Button(frame5, text='execute', fg='orange',
                                         command=lambda: self.execute_event(

                                         )).pack(side=tk.RIGHT, expand=True)

    def import_file_chooser(self):
        filename = tk.filedialog.askopenfilename()
        self._import_path_var.set(filename)

    def export_file_chooser(self):
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
        '''the main entry point of the program, the event-handler for execute
        button'''
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
                    print(clean_url)
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
                    print(output_row)
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


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()


