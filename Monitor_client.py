import os
from urllib.request import urlopen
import tkinter as tk
import tkinter.font as font
from PIL import Image, ImageTk


class MiaApp:

    def __init__(self, id_monitor):

        _URL_BASE_ = "http://127.0.0.1:8000"
        URL_NOTIZIE = _URL_BASE_ + "/monitor/notizie/" + str(id_monitor)
        URL_IMPOSTAZIONI = _URL_BASE_ + "/monitor/impostazioni/"

        self.impostazioni = self.scarica_impostazioni(URL_IMPOSTAZIONI)

        # Costruzione della finestra
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)

        # Creazione font
        fonttitolo = font.Font(family="Calibri", size="35", weight="bold", underline=1)
        fontdescrizione = font.Font(family="Calibri", size="20")
        fontnews = font.Font(family="Calibri", size="18", slant="italic", weight="bold")

        image = Image.open(os.path.join("default", "top.png"))
        [image_size_width, image_size_height] = image.size

        # Costanti di configurazione
        PADDING = 5
        MAX_WIDTH = self.root.winfo_screenwidth()

        heightbanner = int(MAX_WIDTH / image_size_width * image_size_height)

        MAX_HEIGHT = self.root.winfo_screenheight() - PADDING - heightbanner
        self.MAX_HEIGHT_IMAGE = MAX_HEIGHT - PADDING * 6 - 100
        self.MAX_WIDTH_IMAGE = int(MAX_WIDTH / 2 - PADDING * 4)

        image = image.resize((MAX_WIDTH, heightbanner), Image.ANTIALIAS)
        ban = ImageTk.PhotoImage(image)
        topbanner = tk.Label(image=ban)

        # POPOLAMENTO finestra
        self.titolo = tk.Label(text="Nessuna notizia disponibile",
                               font=fonttitolo,
                               fg="red")
        self.descrizione = tk.Label(text="Siamo spiacenti ma non è possibile visualizzare nessuna notizia.",
                                    font=fontdescrizione)
        self.news = tk.Label(text="Notizie in aggiornamento...",
                             font=fontnews,
                             bg="#0099CC")
        image = Image.open(os.path.join("default", "vuoto.jpg"))
        image = self.ridimensiona_immagine(image, self.MAX_WIDTH_IMAGE, self.MAX_HEIGHT_IMAGE)
        photo = ImageTk.PhotoImage(image)
        self.immagine = tk.Label(image=photo)

        # Posizionamento
        topbanner.grid(row=0, column=0, columnspan=2, sticky=tk.N)
        self.titolo.grid(row=1, column=0, columnspan=2, sticky=tk.S, padx=PADDING, pady=PADDING)
        self.descrizione.grid(row=2, column=0, sticky=tk.N + tk.S, padx=PADDING, pady=PADDING)
        self.immagine.grid(row=2, column=1, sticky=tk.S, padx=PADDING, pady=PADDING)
        self.news.grid(row=3, column=0, columnspan=2, sticky=tk.E + tk.W, padx=0, pady=PADDING)

        # Definisco le dimensioni di righe e colonne per far si che il layout sia definito in modo statico.
        self.root.rowconfigure(0, weight=1, minsize=heightbanner)
        self.root.columnconfigure(0, weight=1, minsize=self.MAX_WIDTH_IMAGE + 2 * PADDING)
        self.root.columnconfigure(1, weight=1, minsize=self.MAX_WIDTH_IMAGE + 2 * PADDING)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)

        # scarico dati
        self.lista_news = self.scarica_dati(URL_NOTIZIE)

        # Avvio
        self.aggiorna_schermo(0)
        self.root.mainloop()

    def scarica_impostazioni(self, url):
        """
        Funzione che recupera le impostazioni dei monitor
        :param url: l'url dal quale recuperare le informazioni
        :return: il dizionario delle impostazioni
        """
        # impostazioni = json.load(url)
        impostazioni = {'freq_agg': 5000}
        return impostazioni

    def ridimensiona_immagine(self, immagine, max_width_image, max_height_image):
        """
        Funzione che ridimensiona l'immagine in modo che occupi il giusto spazio nella finestra
        :param immagine: l'immagine da redimensionare
        :param max_width_image: la larghezza massima
        :param max_height_image: l'altezza massima
        :return: l'immagine redimensionata
        """

        [image_size_width, image_size_height] = immagine.size

        # cerco fattore di scalo
        if max_width_image / image_size_width < max_height_image / image_size_height:
            fattore = max_width_image / image_size_width
        else:
            fattore = max_height_image / image_size_height

        new_image_size_width = int(image_size_width * fattore)
        new_image_size_height = int(image_size_height * fattore)
        nuova_immagine = immagine.resize((new_image_size_width, new_image_size_height), Image.ANTIALIAS)
        return nuova_immagine

    def download_immagine(self, img_url, filename):
        """
        Scarica le immagini dal server e ne effettua la copia nella memoria della macchina
        :param img_url: l'url remoto dal quale reperire l'immagine
        :param filename: il nome da dare al file
        :return: il path del file salvato in locale oppure false in caso di errore di rete
        """
        try:
            a, file_extension = os.path.splitext(img_url)
            image_on_web = urlopen(img_url)
            buf = image_on_web.read()
            path = os.path.join(os.getcwd(), 'immagini', str(filename) + file_extension)
            downloaded_image = open(path, "wb")
            downloaded_image.write(buf)
            downloaded_image.close()
            image_on_web.close()
        except IOError:
            return False
        return path

    def scarica_dati(self, url):
        """
        Ricava i dati dall'url remoto
        :param url: l'url da cui prendere i dati
        :return: la lista di notizie
        """
        # lista_temp = json.load(url)
        # scalo immagine

        lista_temp = [{'id': 1, 'titolo': 'Bel tempo domani', 'descrizione': 'Il tempo domani sarà soleggiato',
                       'immagine': 'http://www.astronomy2009.it/wp-content/uploads/2016/05/sole.jpg'},
                      {'id': 2, 'titolo': 'Ultima sfilata di carnevale',
                       'descrizione': 'Domenica si terrà l''ultima sfilata di carnevale\nQuindi tutti in piazza',
                       'immagine': 'http://www.guidatorino.com/wp-content/uploads/2016/01/carnevale-piemonte.jpg'}]
        lista_news = []
        for i in lista_temp:
            image = self.download_immagine(i['immagine'], i['id'])
            if not image:
                image = os.path.join("default", "vuoto.jpg")
            del i['immagine']
            image = Image.open(image)
            image = self.ridimensiona_immagine(image, self.MAX_WIDTH_IMAGE, self.MAX_HEIGHT_IMAGE)
            photo = ImageTk.PhotoImage(image)
            i['immagine'] = photo
            lista_news.append(i)
        return lista_news

    def conta_righe(self, testo, dim_riga):
        """
        Funziona che conta il numero dirighe che occupa una stringa di testo
        :param testo: il testo el quale si vuole stimare il numero di righe
        :param dim_riga: il numero di caratteri che può contenere una riga
        :return: il numero di righe
        """
        if not testo or not dim_riga:
            return 0
        else:
            righe = 0
            caratteri_letti = 0
            for i in range(len(testo) - 1):
                if testo[i] == '\n':
                    righe += 1
                else:
                    caratteri_letti += 1
                if caratteri_letti >= dim_riga:
                    righe += 1
                    caratteri_letti = 0
            if caratteri_letti > 0:
                righe += 1
            return righe

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
        news = ""
        for i in self.lista_news:
            news = news + i['titolo'] + " - "
        news = news[:-3]
        self.news.configure(text=news)

        if indice < len(self.lista_news) - 1:
            indice += 1
        else:
            indice = 0

        self.root.after(self.impostazioni['freq_agg'], self.aggiorna_schermo, indice)


app = MiaApp(1)
