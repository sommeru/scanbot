import justpy as jp
from pdf2image import convert_from_path
from os import listdir
from os.path import isfile, join
import re
import os
import time

class RefreshButton(jp.Div):
    def __init__(self, renamerComponent, **kwargs):
        self.renamerComponent = renamerComponent
        super().__init__(**kwargs)
        self.classes = 'text-center w-full text-xl m-2 p-1 bg-yellow-500 text-white font-bold rounded-full col-span-8'
        self.update_refreshbutton()
        self.on('click', self.clicked)

    def clicked(self, msg):
         self.renamerComponent.previewer.update_preview()

    def update_refreshbutton(self):
        self.text = '↻ Neu laden... [' + str(self.renamerComponent.pdf_index +1 ) + '/' + str(self.renamerComponent.pdf_index_max + 1) + ']'

class NextButton(jp.Div):
    def __init__(self, renamerComponent, **kwargs):
        super().__init__(**kwargs)
        self.renamerComponent = renamerComponent
        self.text = '→'
        self.classes = 'text-center w-full text-xl m-2 p-1 bg-yellow-500 text-white font-bold rounded-full col-span-1'
        self.on('click', self.clicked)
    def clicked(self, msg):
        self.renamerComponent.pdf_index += 1
        self.renamerComponent.previewer.update_preview()

class PrevButton(jp.Div):
    def __init__(self, renamerComponent, **kwargs):
        super().__init__(**kwargs)
        self.renamerComponent = renamerComponent
        self.text = '←'
        self.classes = 'text-center w-full text-xl m-2 p-1 bg-yellow-500 text-white font-bold rounded-full col-span-1'
        self.on('click', self.clicked)
    def clicked(self, msg):
        self.renamerComponent.pdf_index -= 1
        self.renamerComponent.previewer.update_preview()

class DeleteButton(jp.Div):
    def __init__(self, renamerComponent, **kwargs):
        self.renamerComponent = renamerComponent
        super().__init__(**kwargs)
        self.classes = 'text-center w-full text-xl m-2 p-1 bg-red-500 text-white font-bold rounded-full col-span-1'
        self.text = '♺'
        self.on('click', self.clicked)
    def clicked(self, msg):
        print('delete!')
        fname = self.renamerComponent.previewer.fname
        if fname is None:
            return
        else:
            try:
                basename = os.path.basename(fname)
                os.rename(fname, "bin/" + basename)
            except Exception as ex:
                print("alles kaputt: {}".format(ex))
                pass
            self.renamerComponent.previewer.update_preview()

class RenameButton(jp.Div):
    def __init__(self, renamerComponent, **kwargs):
        self.renamerComponent = renamerComponent
        super().__init__(**kwargs)
        self.classes = 'text-center w-full text-xl m-2 p-1 bg-green-500 text-white font-bold rounded-full col-span-9'
        self.text = 'Archiv'
        self.on('click', self.rename_clicked)

    def construct_filename(self):
        filename = self.renamerComponent.active_category + '/'
        if self.renamerComponent.active_category == 'ssms' or self.renamerComponent.active_category == 'ifs':
            filename = filename + self.renamerComponent.active_subcategory + '/'
            if self.renamerComponent.active_subcategory == 'invoice':
                filename = filename + self.renamerComponent.input_desc.my_input_field.value
            elif self.renamerComponent.active_subcategory == 'doc':
                filename = filename + self.renamerComponent.input_date.my_input_field.value + ' - '
                filename = filename + self.renamerComponent.input_desc.my_input_field.value
            else:
                print('Subcategory Error')
        elif self.renamerComponent.active_category == 'general':
            filename = filename + self.renamerComponent.input_date.my_input_field.value + '-'
            filename = filename + self.renamerComponent.input_number.my_input_field.value + '-'
            filename = filename + self.renamerComponent.input_desc.my_input_field.value
        else:
            print('Category Error')
            
        filename=filename + '.pdf'
        return(filename)

    def rename_clicked(self, msg):
        print('renaaaaame!')
        fname = self.renamerComponent.previewer.fname
        date = self.renamerComponent.input_date.my_input_field.value
        number = self.renamerComponent.input_number.my_input_field.value
        desc = self.renamerComponent.input_desc.my_input_field.value

        if fname is None:
            return
        else:
            try:
                os.rename(fname, "out/" + self.construct_filename())
                print(self.construct_filename())
            except Exception as ex:
                print("alles kaputt: {}".format(ex))
                pass
            self.renamerComponent.previewer.update_preview()

class InputField(jp.Div):
    def __init__(self, description, placeholder, initial_value, **kwargs):
        super().__init__(**kwargs)

        classes_form_labels = 'block w-full uppercase tracking-wide text-gray-700 text-s font-bold m-2 mb-2'
        classes_form_input ='w-full p-3 m-2 form-input'

        jp.Div(a=self, text=description, classes=classes_form_labels)
        self.my_input_field = jp.Input(a=self, placeholder=placeholder, value=initial_value, classes=classes_form_input)

class PdfPreviewer(jp.Div):
    def __init__(self, renamerComponent, **kwargs):
        super().__init__(**kwargs)
        self.renamerComponent = renamerComponent

        self.fname = None
        self.image = jp.Div(a=self)
        self.update_preview()

    def update_preview(self):
        pdfpath='./in/'
        files = [f for f in listdir(pdfpath) if isfile(join(pdfpath, f))]
        pdffiles = list(filter(re.compile(".*.pdf").match, files))

        self.renamerComponent.pdf_index_max = len(pdffiles) - 1

        if self.renamerComponent.pdf_index < 0:
            self.renamerComponent.pdf_index = 0
        elif self.renamerComponent.pdf_index > self.renamerComponent.pdf_index_max:
            self.renamerComponent.pdf_index = self.renamerComponent.pdf_index_max

        if len(pdffiles) > 0:
            pdffile = pdfpath + pdffiles[self.renamerComponent.pdf_index]

            pages = convert_from_path(pdffile, 100)
            pages[0].save('tmp-img.jpg', 'JPEG')

            self.remove_component(self.image)
            self.image.delete()
            self.image = jp.Img(a=self,src='static/tmp-img.jpg?r={}'.format(time.time()), classes='w-full')
            self.fname = pdffile
        else:
            self.remove_component(self.image)
            self.image.delete()
            self.image = jp.Div(a=self, text="Kein PDF gefunden :(")
            self.fname = None

class CategoryButton(jp.Div):

    def __init__(self, category_desc, category, renamerComponent, **kwargs):
        self.renamerComponent = renamerComponent
        self.category = category
        super().__init__(**kwargs)
        

        self.button = jp.Div(a=self, text=category_desc)
        self.button.on('click', self.category_button_clicked)
        self.update_active()

    def category_button_clicked(self, msg):
        self.renamerComponent.active_category = self.category

    def update_active(self):
        classes_category_button = 'text-center w-full text-xl m-2 p-1 bg-blue-500 text-white font-bold rounded-full'
        classes_category_button_active = 'text-center w-full text-xl m-2 p-1 bg-blue-300 text-black font-bold rounded-full'
        if self.renamerComponent.active_category == self.category:
            self.button.classes = classes_category_button_active
        else:
            self.button.classes = classes_category_button

class SubcategoryButton(jp.Div):

    def __init__(self, subcategory_desc, subcategory, renamerComponent, **kwargs):
        self.renamerComponent = renamerComponent
        self.subcategory = subcategory
        super().__init__(**kwargs)
        

        self.subbutton = jp.Div(a=self, text=subcategory_desc)
        self.subbutton.on('click', self.subcategory_button_clicked)
        self.update_active()

    def subcategory_button_clicked(self, msg):
        self.renamerComponent.active_subcategory = self.subcategory

    def update_active(self):
        classes_subcategory_button = 'text-center w-full text-xl m-2 p-1 bg-blue-500 text-white font-bold rounded-full'
        classes_subcategory_button_active = 'text-center w-full text-xl m-2 p-1 bg-blue-300 text-black font-bold rounded-full'
        if self.renamerComponent.active_subcategory == self.subcategory:
            self.subbutton.classes = classes_subcategory_button_active
        else:
            self.subbutton.classes = classes_subcategory_button

class RenamerComponent(jp.Div):

    def __init__(self, active_category, active_subcategory, **kwargs):
        self.active_category = active_category
        self.active_subcategory = active_subcategory
        self.entered_date = '20210101'
        self.entered_number = '123'
        self.entered_description = 'Beschreibung'
        self.pdf_index = 0
        self.pdf_index_max = 0

        super().__init__(**kwargs)

        root = self

        container = jp.Div(a=root, classes='grid grid-cols-2 gap-2 w-full')
        div_left = jp.Div(a=container, classes='relative')
        div_right = jp.Div(a=container)

        self.previewer = PdfPreviewer(self,a=div_right)

        prev_refresh_next_container = jp.Div(a=div_left, classes='grid grid-cols-10 gap-2 w-full')
        PrevButton(self, a=prev_refresh_next_container)
        self.refreshbutton = RefreshButton(self, a=prev_refresh_next_container)
        NextButton(self, a=prev_refresh_next_container)
        
        category_container = jp.Div(a=div_left, classes='grid grid-cols-3 gap-2 w-full')
        self.btn1 = CategoryButton('General', 'general', self, a=category_container)
        self.btn2 = CategoryButton('SSMS', 'ssms', self, a=category_container)
        self.btn3 = CategoryButton('IFS', 'ifs', self, a=category_container)

        self.subcategory_container = jp.Div(a=div_left, classes='grid grid-cols-2 gap-2 w-full')
        self.subbtn1 = SubcategoryButton('Rechnung', 'invoice', self, a=self.subcategory_container)
        self.subbtn2 = SubcategoryButton('Dokument', 'doc', self, a=self.subcategory_container)
        

        self.input_date = InputField("Dokumentendatum", "z.B. 19830520", "", a=div_left)
        self.input_number = InputField("Fortlaufende Nummer", "z.B. 210123", "", a=div_left)
        self.input_desc = InputField("Beschreibung", "Beschreibender Text", "", a=div_left)

        delete_rename_container = jp.Div(a=div_left, classes='absolute grid grid-cols-10 gap-2 w-full bottom-0')
        DeleteButton(self, a=delete_rename_container)
        RenameButton(self, a=delete_rename_container)

        self.react(self.data)

    def react(self, data):
        if self.active_category == 'general':
            self.subcategory_container.show = False
        else:
            self.subcategory_container.show = True

        if self.active_category == 'ssms' or self.active_category == 'ifs':
            self.input_number.show = False
        else:
            self.input_number.show = True

        self.btn1.update_active()
        self.btn2.update_active()
        self.btn3.update_active()
        self.subbtn1.update_active()
        self.subbtn2.update_active()
        self.refreshbutton.update_refreshbutton()

async def scanbot(request):
    wp = jp.WebPage()
    rc = RenamerComponent(a=wp, active_category='general', active_subcategory='doc')
    return wp

jp.justpy(scanbot)
