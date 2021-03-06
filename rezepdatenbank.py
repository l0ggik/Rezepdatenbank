import sqlite3
import tkinter as tk
from tkinter import messagebox
import database_connection


def main():
    database_connection.init_database()
    gui_root = tk.Tk()
    init_app = GuiWindow(master=gui_root)
    init_app.mainloop()
    

class GuiWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.optionbutton1 = tk.Button(text="Neues Rezept erstellen", command=self.create_recipe)
        self.optionbutton2 = tk.Button(text="Rezept ändern", command=self.change_recipe)
        self.optionbutton3 = tk.Button(text="Rezept suchen", command=self.find_recipe)
        self.optionbutton4 = tk.Button(text="Zutaten suchen", command=self.find_component)

        self.optionbutton1.grid()
        self.optionbutton2.grid()
        self.optionbutton3.grid()
        self.optionbutton4.grid()

    def create_recipe(self):
        self.master.destroy()
        root = tk.Tk()
        recipe_gui = CreateRecipeGui(master=root)
        recipe_gui.mainloop()

    def change_recipe(self):
        pass

    def find_recipe(self):
        self.master.destroy()
        root = tk.Tk()
        find_recipe_gui = FindRecipeGui(master=root)
        find_recipe_gui.mainloop()

    def find_component(self):
        pass


class CreateRecipeGui(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.component_list = []
        self.recipe = ''
        self.recipe_name = ''
        self.recipe_description = ''
        self.recipe_id = 0
        self.component_name = ''
        self.component_amount = 0
        self.component_unit = ''

        # Einheiten
        self.units_optionmenue_frame = tk.Frame()  # Frame für die Plazierung der Zutaten-Textfelder
        self.units_optionmenue_list = [UnitOptionMenue(self.units_optionmenue_frame),
                                       UnitOptionMenue(self.units_optionmenue_frame),
                                       UnitOptionMenue(self.units_optionmenue_frame)]

        self.component_name_textfield_list = [tk.Text(height=1, width=30),
                                              tk.Text(height=1, width=30),
                                              tk.Text(height=1, width=30)]
        self.component_amount_textfield_list = [tk.Text(height=1, width=8),
                                                tk.Text(height=1, width=8),
                                                tk.Text(height=1, width=8)]

        # Rezeptname
        self.recipe_name_label = tk.Label(text='Rezeptname')
        self.recipe_name_text = tk.Text(height=1, width=60)

        # Rezeptzubereitung
        self.recipe_description_label = tk.Label(text='Zubereitung')
        self.recipe_description_text = tk.Text(height=30, width=60)

        # Labels für Zutat, Menge und Einheit
        self.recipe_component_label = tk.Label(text='Zutat')
        self.amount_label = tk.Label(text='Menge')
        self.unit_label = tk.Label(text='Einheit')

        # Buttons
        self.add_component_button = tk.Button(text='weitere Zutaten',
                                              command=self.push_add_components_to_gui_button)  #add_components)
        self.submit_recipe_button = tk.Button(text='Rezept speichern',
                                              command=self.push_submit_recipe_button)

        # Komponenten im Frame plazieren
        self.recipe_name_label.grid(column=1, row=1, columnspan=3)
        self.recipe_name_text.grid(column=1, row=2, columnspan=3)

        self.recipe_description_label.grid(column=1, row=3, columnspan=3)
        self.recipe_description_text.grid(column=1, row=4, columnspan=3)

        # labels for components, amount and unit
        self.recipe_component_label.grid(column=1, row=5, columnspan=3, sticky=tk.W, padx=20)
        self.amount_label.grid(column=2, row=5)
        self.unit_label.grid(column=3, row=5)

        for textfield in self.component_name_textfield_list:
            textfield.grid(column=1)

        rowcount = 6  # start at row 6 and add the component_amount_textfields
        for textfield in self.component_amount_textfield_list:
            textfield.grid(column=2, row=rowcount)
            rowcount += 1

        for units_optionmenue in self.units_optionmenue_list:
            units_optionmenue.grid()
        self.units_optionmenue_frame.grid(column=3, row=6, rowspan=3)

        self.add_component_button.grid(column=1)
        self.submit_recipe_button.grid(column=1)
        # self.go_back_button.grid(column=1)
        # self.add_unit_button(column=1)

    def push_submit_recipe_button(self):
        self.recipe_name = self.recipe_name_text.get("1.0", "end").strip()
        self.recipe_description = self.recipe_description_text.get("1.0", 'end').strip()
        self.recipe_id = self.create_recipe()
        for count, textfield in enumerate(self.component_name_textfield_list):
            self.component_name = textfield.get("1.0", "end").strip()
            self.component_amount = self.component_amount_textfield_list[count].get("1.0", "end")
            self.component_unit = self.units_optionmenue_list[count].stringvar.get()
            if self.component_name:
                self.create_component()

    def push_add_components_to_gui_button(self):
        for i in range(3):
            self.component_name_textfield_list.append(tk.Text(height=1, width=30))
            self.units_optionmenue_list.append(UnitOptionMenue(self.units_optionmenue_frame))
            self.component_amount_textfield_list.append(tk.Text(height=1, width=8))

        row_count = 6
        for textfield in self.component_name_textfield_list:
            textfield.grid_forget()
            textfield.grid(column=1, row=row_count)
            row_count += 1
        row_count = 6
        for textfield in self.component_amount_textfield_list:
            textfield.grid_forget()
            textfield.grid(column=2, row=row_count)
            row_count += 1

        # Remove some components from the grid
        self.add_component_button.grid_forget()
        self.submit_recipe_button.grid_forget()
        self.units_optionmenue_frame.grid_forget()
        for optionmenue in self.units_optionmenue_list:
            optionmenue.grid_forget()

        # Regrid components in the right order
        for optionmenue in self.units_optionmenue_list:
            optionmenue.grid()
        self.units_optionmenue_frame.grid(column=3, row=6, rowspan=len(self.component_name_textfield_list))
        self.add_component_button.grid(column=1)
        self.submit_recipe_button.grid(column=1)

    def create_component(self):
        conn = sqlite3.connect('rezepte.db')
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO zutaten (Zutat_Name, Zutat_Menge, Zutat_Einheit, Rezept_ID) VALUES (?,?,?,?)
                        """,
                       (self.component_name,
                       self.component_amount,
                       self.component_unit,
                       self.recipe_id))
        conn.commit()
        conn.close()

    def create_recipe(self):
        conn = sqlite3.connect('rezepte.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO rezepte (Rezept_Name, Rezept_Beschreibung) VALUES (?, ?)",
                       (self.recipe_name, self.recipe_description))
        conn.commit()
        conn.close()
        return cursor.lastrowid

    def add_component_to_list(self):
        self.component_list.append(self.recipe_component_text.get('1.0', 'end').strip())
        self.recipe_component_text.delete('1.0', 'end')

    def add_components(self):
        for i in range(3):
            self.component_name_textfield_list.append(tk.Text(height=1, width=30))
            self.units_stringvar_list.append(tk.StringVar())
            self.units_stringvar_list[i+3].set(self.units_list[0])
            self.units_optionmenue_list.append(tk.OptionMenu(self.units_optionmenue_frame, self.units_stringvar_list[i + 3], *self.units_list))
            self.component_amount_textfield_list.append(tk.Text(height=1, width=8))
        self.add_component_button.grid_forget()
        self.submit_recipe_button.grid_forget()
        self.units_optionmenue_frame.grid_forget()
        # for textfield in self.component_name_textfield_list:
        row_count = 6
        for textfield in self.component_name_textfield_list:
            textfield.grid_forget()
            textfield.grid(column=1, row=row_count)
            row_count += 1
        row_count = 6
        for textfield in self.component_amount_textfield_list:
            textfield.grid_forget()
            textfield.grid(column=2, row=row_count)
            row_count += 1
        for optionmenue in self.units_optionmenue_list:
            optionmenue.grid_forget()
        for optionmenue in self.units_optionmenue_list:
            optionmenue.grid()
        self.units_optionmenue_frame.grid(column=3, row=6, rowspan=len(self.component_name_textfield_list))
        self.add_component_button.grid(column=1)
        self.submit_recipe_button.grid(column=1)


class FindRecipeGui(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.recipe_name_label = tk.Label(text='Bitte gib den Rezeptnamen ein')
        self.recipe_name_text = tk.Text(height=1, width=60)
        self.find_recipe_button = tk.Button(text='Rezept laden', command=self.click_find_recipe_button)

        self.recipe_name_label.grid(column=1, row=1)
        self.recipe_name_text.grid(column=1, row=2)
        self.find_recipe_button.grid(column=1, row=3)

    def click_find_recipe_button(self):
        recipe_list = database_connection.read_from_database("SELECT Rezept_ID,"
                                                             "Rezept_Name, "
                                                             "Rezept_Beschreibung "
                                                             "FROM rezepte "
                                                             "WHERE Rezept_Name LIKE ?",
                                                             self.recipe_name_text.get("1.0", "end").strip())
        if recipe_list:
            self.master.destroy()
            root = tk.Tk()
            show_recipe_gui = ShowRecipeGui(recipe_list, master=root)
            show_recipe_gui.mainloop()
        else:
            messagebox.showerror(title='Rezept nicht gefunden',
                                         message='Das ausgewählte Rezept konnte nicht gefunden werden')


class ShowRecipeGui(tk.Frame):
    def __init__(self, recipe_list=None, master=None):
        super().__init__(master)
        self.recipe_list = recipe_list
        self.recipe_position = 0
        self.component_list = []

        self.recipe_name_label = tk.Label(height=1, width=60)
        self.recipe_text_label = tk.Label(height=30, width=60)
        self.recipe_components_label = tk.Label()
        self.next_recipe_button = tk.Button(text='nächstes Rezept', command=self.push_next_recipe_button)
        self.previous_recipe_button = tk.Button(text='vorheriges Rezept', command=self.push_previous_recipe_button)
        self.quit_button = tk.Button(text='Verlassen', command=self.push_quit_button)

        self.update_components()

    def push_next_recipe_button(self):
        self.recipe_position += 1
        self.update_components()

    def push_previous_recipe_button(self):
        self.recipe_position -= 1
        self.update_components()

    def push_quit_button(self):
        self.master.destroy()

    def grid_components(self):
        self.recipe_name_label.grid(columnspan=3, column=1)
        self.recipe_text_label.grid(columnspan=3, column=1)
        self.recipe_components_label.grid(columnspan=3, column=1)
        self.quit_button.grid(row=4, column=1)
        self.next_recipe_button.grid(row=4, column=2)
        self.previous_recipe_button.grid(row=4, column=3)

    def update_components(self):
        self.component_list = database_connection.read_from_database("SELECT * "
                                                                     "FROM zutaten "
                                                                     "WHERE Rezept_ID = ?",
                                                                     self.recipe_list[self.recipe_position][0])
        components_string = ''
        for component in self.component_list:
            components_string = components_string \
                                + str(int(component[2])) \
                                + ' ' + component[3] \
                                + ' ' + component[1] + '\n'
        self.recipe_components_label.config(height=len(self.component_list) + 1, width=60, text=components_string)
        self.recipe_name_label.config(text=self.recipe_list[self.recipe_position][1])
        self.recipe_text_label.config(text=self.recipe_list[self.recipe_position][2])
        if self.recipe_position == 0:
            self.previous_recipe_button.config(state='disabled')
            if len(self.recipe_list) <= 1:
                self.next_recipe_button.config(state='disabled')
            else:
                self.next_recipe_button.config(state='normal')
        elif self.recipe_position >= len(self.recipe_list-1):
            self.next_recipe_button.config(state='disabled')
            self.previous_recipe_button.config(state='normal')
        self.grid_components()


class UnitOptionMenue(tk.OptionMenu):
    units_list = ['g', 'kg', 'Stück', 'ml', 'Stangen', 'EL', 'TL', 'Dose', 'Becher', '']
    grid_position = 0

    def __init__(self, master=None):
        self.stringvar = tk.StringVar()
        self.stringvar.set(self.units_list[0])
        super().__init__(master, self.stringvar, *self.units_list)

    def grid_self(self):
        pass

    
if __name__=='__main__':
    main()
