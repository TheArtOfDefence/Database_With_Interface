import PySimpleGUI as sg
from MyDatabase import MyDatabase

class GUI():
    def __init__(self):
        self.text=""
        self.megatrend = MyDatabase()
        self.layout = [
            [sg.Button('Prikazi')],
            [sg.Button('Izmeni')],
            [sg.Button('Unesi')],
            [sg.Button('Obrisi')],
            [sg.Button('Tabela polaganja prevedena i sortirana po ocenama')],
            [sg.Button('Promeni naziv tabele')],
            [sg.Button('Prosek studenta')]
        ]
        self.window = sg.Window('MEGATREND UNIVERZITET',self.layout,size=(1000,600))
        self.main_window()

    def main_window(self):
        while True:
            event,values = self.window.read()
            if event == sg.WIN_CLOSED:
                break;
            #Ovom komandom u slucaju pritiska x ima da se zatvori aplikacija.
            elif event == 'Prikazi':
                try:
                    self.get_input('Unesite naziv tabele koju zelite da prikazete.')
                    self.megatrend.show_results(self.text)
                    self.show_table(self.megatrend.rows,self.megatrend.columns)
                    self.window.refresh()
                except Exception as e:
                    sg.popup('ERROR','You entered some value wrong, try again.',e)
                    pass

            elif event == 'Izmeni':
                try:
                    self.get_input('U kojoj tabeli se nalazi podatak koji zelite da izmenite.')
                    podatak1=self.text
                    self.get_input('Unesite sifru podatka kojeg zelite da izmenite')
                    podatak2 = self.text
                    self.get_input('Unesite podatak koji zelite da zamenite')
                    podatak3 = self.text
                    self.get_input('Unesite novu vrednost podatka')
                    podatak4 = self.text
                    self.megatrend.update_data(podatak1,podatak2,podatak3,podatak4)
                    self.window.refresh()
                except Exception as e :
                    sg.popup('ERROR','You have entered some value wrong, please try again.',e)
                    pass

            elif event == 'Unesi':
                try:
                    self.get_input('U kojoj tabeli zelite da unesete ove podatke.')
                    podatak1=self.text
                    self.get_input('Unesite sve vrednosti podatka.')
                    podatak2 = self.text
                    self.megatrend.insert_data(podatak1,podatak2)
                    self.window.refresh()
                except Exception as e:
                    sg.popup('ERROR','You have entered some value wrong, please try again.',e)
                    pass

            elif event == 'Obrisi':
                try:
                    self.get_input('U kojoj tabeli zelite da obrisete podatak.')
                    podatak1=self.text
                    self.get_input('Unesite sifru podatka koji zelite da obrisete.')
                    podatak2 = self.text
                    self.megatrend.delete_data(podatak1,podatak2)
                    self.window.refresh()
                except Exception as e:
                    sg.popup('ERROR','You have entered some value wrong, please try again.',e)
                    pass

            elif event == 'Tabela polaganja prevedena i sortirana po ocenama':
                try:
                    self.megatrend.show_polaganja_without_keys()
                    self.show_table(self.megatrend.rows,self.megatrend.columns)
                    self.window.refresh()
                except Exception as e:
                    sg.popup('ERROR','You have entered some value wrong, please try again.',e)
                    pass

            elif event == 'Promeni naziv tabele':
                try:
                    self.get_input('Kojoj tabeli zelite da promenite naziv?')
                    podatak1 = self.text
                    self.get_input('U koji naziv zelite da promenite?')
                    podatak2=self.text
                    self.megatrend.change_name_of_table(podatak1,podatak2)
                    self.window.refresh()
                except Exception as e:
                    sg.popup('ERROR','You have entered some value wrong, please try again.',e)
                    pass
            elif event == 'Prosek studenta':
                try:
                    self.get_input('Unesite sifru studenta ciji prosek zelite da vidite.')
                    podatak1 = self.text
                    self.megatrend.show_average_grade_of_student(podatak1)
                    podatak2=self.megatrend.prosecna_ocena
                    sg.popup('Prosecna ocena studenta je ' + str(podatak2[0][0]))
                    self.window.refresh()
                except Exception as e:
                    sg.popup('ERROR','You have entered some value wrong, please try again.',e)
                    pass

        self.window.close()

    def get_input(self,nekitekst):
        self.text = sg.popup_get_text('Unos',nekitekst)
        if self.text == "":
            raise Exception("Ne moze prazna vrednost, probajte sa NULL ali i tada mozda nece moci ako je zabranjeno.")
            #Zbog toga sto obican korisnik ne zna sta znaci rec NULL, on ce za nesto bez vrednosti samo predati prazan unos, ovom komandom se korisnik tera da unese vrednost NULL, sa ovim se kasnije omogucava to da izlazi error NOT NULL.

    def show_table(self,rows,columns):
        show_table_layout=[
                [sg.Table(
                    values = rows,
                    headings = columns,
                    max_col_width=100,
                    auto_size_columns = False,
                    display_row_numbers = False,
                    justification = 'center',
                    num_rows=500,
                    key='-TABLE-',
                    row_height=20,
                    expand_x=True,
                    expand_y=True,
                )]
        ]
        self.show_table_window = sg.Window('TABELA',show_table_layout,size=(1000,600))
        while True:
            event,values = self.show_table_window.read()
            if event == sg.WIN_CLOSED:
                break;
        self.show_table_window.close()
  #Ovom komandom se otvara novi window gde ce biti tabela.
