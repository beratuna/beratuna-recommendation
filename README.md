# beratuna-recommendation


Initially create a virtualenv (not necessarily)

```
virtualenv -p python3 <desired-path>
```

```
$ source <desired-path>/bin/activate
```

Then install required libraries using requirements.txt
```
$ pip3 install -r requirements.txt
```
After environmental setup, run reco.py with desired parameters to create the model and start the API to serve

```
$ python3 reco.py
```

Note: Flask API is running on DEBUG mode, if there will be no additional changes on the reco.py.
You could comment out that line. 

After reco.py competed generating the model, API will immediately become ready to serve. While the API is running, run example.py to see the sample which sends productids to API via request parameters in json format. API will return top ten recommended products with their scores.
```
$ source <desired-path>/bin/activate
```
Main Categories are as follows;

![image](https://user-images.githubusercontent.com/29654044/132079883-64096874-bcee-466c-a86d-23ada0201e23.png)
