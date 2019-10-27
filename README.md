# FlaskAPI

Repozytorium mieści samo API oraz aplikację kliencką, która pozwala wygodnie przetestować jego działanie.
<h1>Początek pracy</h1>
W kodzie użyłem takich bibliotek `requests,flask, flask_sqlalchemy`, dlatego przed rozpoczęciem testowania API, należy je zainstalować:
```
pip install flask flask_sqlalchemy requests
```

Po tym należy przejść do folderu,gdzie był pobrany repozytorium i wpisać polecenie, żeby uruchomić serwer.
```
python api.py
```
<h1> Testowanie </h1>

Do wygodnego testowania był napisany skrypt `client.py` który, w zależności od podanej opcji wysyła odpowiedni requesty
na serwer.
Żeby sprawdzić dostępne opcji można wpisać `client.py -h`.
```
usage: client.py [-h] [-A ADDONE] [-R] [-D | -d DELETEONE] [-g GETONE | -G]
                 [-o OUTPUT | -a APPEND] [-H HOSTNAME]

Wrapper to works with api from command line

optional arguments:
  -h, --help            show this help message and exit
  -A ADDONE, --addOne ADDONE
                        Command in format: -a FILENAME Add's all test examples
                        from file
  -R, --readable        If passed, convert timestamps from server output to
                        human-readable format
  -D, --deleteAll       Delete all records from database
  -d DELETEONE, --deleteOne DELETEONE
                        Command in format: -d TEST_ID Delete test with
                        specific id from server
  -g GETONE, --getOne GETONE
                        Command in format: -g TEST_ID Return test with
                        specific id
  -G, --getAll          Return all data from the server
  -o OUTPUT, --output OUTPUT
                        Command in format: -o FILENAME File to store output
  -a APPEND, --append APPEND
                        If given -- append data from server to existing file
  -H HOSTNAME, --hostname HOSTNAME
                        Send requests to specified hostname. Hostname should
                        be in format: http://some_address/ If argument not
                        passed - default hostname is http://127.0.0.1:5000/
```


<h1> Opis opcji </h1>

- ` -A ADDONE, --addOne ADDONE` -- polecenie dodaje do bazy danych wszystkie dane z pliku, który był podany jako argument. Wymagania do pliku:
musi mieścić sekcję `data`

```
"data":[
  {
      .....
  }
]
```

Przykład:

```
login@hostname:~path/$ python client.py -A sample_data.json
Success !
```

- `-R, --readable ` -- konwertuje dane z serwera w wygodny dla człowieka format. Motywacja: dane na serwerze są przechowywane w formacie `timestamp`,
co jest wygodnie w przypadku jeżeli z danymi potrzeba będzie pracować dalej, jednak nie wygodnie w przypadku jeżeli z danymi będzie pracował człowiek.
*Może być użyta tylko z opcją pobierającą dane z serwera*
Przykład:

```
login@hostname:~path/$ python client.py -g 1 -R

      "timestamp": 1970-01-01 07:00:00,
      "value": 1615789
    
The data was added to the file:  data_from_server22_14_34_26.json
login@hostname:~path/$ cat data_from_server22_14_34_26.json
{
    "data": [
        {
            "timestamp": "1970-01-01 07:00:00",
            "value": 1615789
        }
    ]
}  
```
 
 
