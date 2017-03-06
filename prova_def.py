import os
from urllib.request import urlopen
import tkinter as tk
from tkinter.font import Font

from PIL import Image, ImageTk



class MiaApp():

    def scarica_impostazioni(self,URL):
        """
        Funzione che recupera le impostazioni dei monitor
        :param URL: l'url dal quale recuperare le informazioni
        :return: il dizionario delle impostazioni
        """
        #impostazioni = json.load(URL)
        impostazioni = {'freq_agg':5000}
        return impostazioni

    def ridimensiona_immagine(self,immagine, MAX_WIDTH_IMAGE, MAX_HEIGHT_IMAGE):
        """
        Funzione che ridimensiona l'immagine in modo che occupi il giusto spazio nella finestra
        :param immagine: l'immagine da redimensionare
        :param MAX_WIDTH_IMAGE: la larghezza massima
        :param MAX_HEIGHT_IMAGE: l'altezza massima
        :return: l'immagine redimensionata
        """

        [imageSizeWidth, imageSizeHeight] = immagine.size

        # cerco fattore di scalo
        if MAX_WIDTH_IMAGE / imageSizeWidth < MAX_HEIGHT_IMAGE / imageSizeHeight:
            fattore = MAX_WIDTH_IMAGE / imageSizeWidth
        else:
            fattore = MAX_HEIGHT_IMAGE / imageSizeHeight

        newImageSizeWidth = int(imageSizeWidth * fattore)
        newImageSizeHeight = int(imageSizeHeight * fattore)
        nuova_immagine = immagine.resize((newImageSizeWidth, newImageSizeHeight), Image.ANTIALIAS)
        return nuova_immagine

    def download_immagine(self, img_url, filename):
        """
        Scarica le immagini dal server e ne effettua la copia nella memoria della macchina
        :param filename: il nome da dare al file
        :return: il path del file salvato in locale
        """
        a, file_extension = os.path.splitext(img_url)
        image_on_web = urlopen(img_url)
        buf = image_on_web.read()
        path = os.getcwd() + 'immagini'
        path = os.path.join(os.getcwd(), 'immagini', str(filename) + file_extension)
        downloaded_image = open(path, "wb")
        downloaded_image.write(buf)
        downloaded_image.close()
        image_on_web.close()
        return path


    def scarica_dati(self, URL):
        """
        Ricava i dati dall'url remoto
        :param URL: l'url da cui prendere i dati
        :return: la lista di notizie
        """
        #lista_temp = json.load(URL)
        #scalo immagine

        lista_temp=[{'id':1,'titolo':'Bel tempo domani','descrizione':'Il tempo domani sarà soleggiato','immagine':'http://www.astronomy2009.it/wp-content/uploads/2016/05/sole.jpg'},
                    {'id':2,'titolo':'Ultima sfilata di carnevale','descrizione':'Domenica si terrà l''ultima sfilata di carnevale','immagine':'http://www.guidatorino.com/wp-content/uploads/2016/01/carnevale-piemonte.jpg'}]
        lista_news=[]
        for i in lista_temp:
            image = self.download_immagine(i['immagine'],i['id'])
            del i['immagine']
            image = Image.open(image)
            image = self.ridimensiona_immagine(image, self.MAX_WIDTH_IMAGE, self.MAX_HEIGHT_IMAGE)
            photo = ImageTk.PhotoImage(image)
            i ['immagine']=photo
            lista_news.append(i)
        return lista_news

    def __init__(self, id_monitor):

        _URL_BASE_ = "http://127.0.0.1:8000"
        URL_NOTIZIE = _URL_BASE_+"/monitor/notizie/" + str(id_monitor)
        URL_IMPOSTAZIONI = _URL_BASE_ + "/monitor/impostazioni/"

        self.impostazioni = self.scarica_impostazioni(URL_IMPOSTAZIONI)
        self.root = tk.Tk()



        #Creazione font
        fonttitolo=Font(family="Calibri", size="25", weight="bold", underline=1)

        #Costruzione della finestra
        image = Image.open(os.path.join("default","top.png"))
        [imageSizeWidth, imageSizeHeight] = image.size

        # Costanti di configurazione
        PADDING = 5
        MAX_WIDTH = self.root.winfo_screenwidth()

        heightbanner = int(MAX_WIDTH/imageSizeWidth*imageSizeHeight)

        MAX_HEIGHT = self.root.winfo_screenheight() - PADDING - heightbanner
        self.MAX_HEIGHT_IMAGE = MAX_HEIGHT - PADDING * 6 - 100
        self.MAX_WIDTH_IMAGE = int(MAX_WIDTH / 2 - PADDING * 4)

        image=image.resize((MAX_WIDTH, heightbanner), Image.ANTIALIAS)
        ban = ImageTk.PhotoImage(image)
        topbanner=tk.Label(image=ban)
        self.titolo = tk.Label(text="Nessuna notizia disponibile",
                               font=fonttitolo,
                               fg="red")
        self.descrizione = tk.Label(text="Siamo spiacenti ma non è possibile visualizzare nessuna notizia.")
        self.news = tk.Label(text="Notizie in aggiornamento...")
        image = Image.open("default/vuoto.jpg")
        image = self.ridimensiona_immagine(image, self.MAX_WIDTH_IMAGE, self.MAX_HEIGHT_IMAGE)
        photo = ImageTk.PhotoImage(image)
        self.immagine = tk.Label(image=photo)

        # Posizionamento
        topbanner.grid(row=0, column=0, columnspan=2, sticky=tk.S)
        self.titolo.grid(row=1, column=0, columnspan=2, sticky=tk.S, padx=PADDING, pady=PADDING)
        self.descrizione.grid(row=2, column=0, sticky=tk.N, padx=PADDING, pady=PADDING)
        self.immagine.grid(row=2, column=1, sticky=tk.S, padx=PADDING, pady=PADDING)
        self.news.grid(row=3, column=0, columnspan=2, sticky=tk.S, padx=PADDING, pady=PADDING)

        # Definisco le dimensioni di righe e colonne per far si che il layout sia definito in modo statico.
        self.root.rowconfigure(0,weight=1,minsize=heightbanner)
        self.root.columnconfigure(0, weight=1, minsize=self.MAX_WIDTH_IMAGE + 2*PADDING)
        self.root.columnconfigure(1, weight=1, minsize=self.MAX_WIDTH_IMAGE + 2*PADDING)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)

        #scarico dati
        self.lista_news = self.scarica_dati(URL_NOTIZIE)

        #Avvio
        #self.indice = 0
        self.aggiorna_schermo(0)
        self.root.mainloop()


    def aggiorna_schermo(self, indice):
        """
        Si occupa di aggiornare il contenuto delle label in modo da aggiornare la notizia visualizzata
        :param indice: l'indice della notizia da mostrare
        :return: l'indice della notizia successiva
        """
        elemento = self.lista_news[indice]
        self.titolo.configure(text=elemento['titolo'])
        self.descrizione.configure(text=elemento['descrizione'])
        self.immagine.configure(image=elemento['immagine'])
        news=""
        for i in self.lista_news:
            news = news + i['titolo']+ " - "
        news = news[:-3]
        self.news.configure(text=news)

        if indice < len(self.lista_news)-1:
            indice = indice + 1
        else:
            indice = 0

        self.root.after(self.impostazioni['freq_agg'],self.aggiorna_schermo, indice)


app=MiaApp(1)