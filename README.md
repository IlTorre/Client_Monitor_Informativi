# Monitor_client
Monitor_client: è un' applicazione in python pensata per interfacciarsi con [Server_Monitor_Informativi](https://github.com/IlTorre/Server_Monitor_Informativi).
Il suo scopo è quello di recuperare informazioni sul server e di mostrarle su uno schermo.

Software necessario per l'esecuzione del programma:

    -Python:
        sudo apt-get install python
    
    -Server_Monitor_Informativi:
        è necessario aver installato e in esecuzione il lato server.
        Tutte le informazioni sul server sono reperibili nel file README.md contenuto all'interno del relativo progetto
        raggiungibile all'indirizzo https://github.com/IlTorre/Server_Monitor_Informativi


Come eseguire il programma:

    -Spostarsi nella cartella in cui è presente il file Monitor_client.py
    -Modificare nel file Monitor_client.py l'id del monitor e l' url per raggiungere il server.
    -Digitare: python Monitor_client.py

Verrà eseguito il programma che mostra a schermo intero le notizie comunicate dal server.

Esempio di visualizzazione:
![alt text](esempio.bmp "Esempio di visualizzazione")
