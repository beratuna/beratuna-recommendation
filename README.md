# beratuna-recommendation
## Explanation
The main idea of the project is to recommend related products to customers. There are various methods for recommendation systems (i.e., content-based systems, collaborative filtering-based systems, hybrid systems and session-based systems). Considering the available datasets, there is no user information (e.g., user likes or user ratings), thus collaborative filtering is not the proper way for this project. Also, product content information is insufficient. In the events dataset, there is a session information which could be used to produce session-based systems.

Therefore, in this project a session-based system association rule mining is applied as the main approach. 

To remove irrelevant data associations and recommendations, transections are divided into sub-transections using the category information. There are total of 20 main categories as seen from the Figure 3. Transactions are generated for each category separately.

![image](https://user-images.githubusercontent.com/29654044/132079883-64096874-bcee-466c-a86d-23ada0201e23.png)

## Datasets
There are two datasets (i.e., meta data and events data) given for the projects. Initially contents of those datasets are inspected after they are read and converted to pandas dataframe. In the events data, the rows with missing ‘sessionid’ or ‘productid’ information is removed. In the meta data, ‘productid’ or ‘category’ or ‘subcategory’ or ‘name’. After those processes, dataset information is shown in figures below.

After cleaning raw datasets, they are merged on the ‘productid’ column. After generating merged dataframe, 'event', 'eventtime', 'price' and 'brand' columns are dropped from the merged dataframe since they will not be used on the project as shown in the figure.

![image](https://user-images.githubusercontent.com/29654044/132080026-f7228893-a0f6-4e1d-876e-5b3562f0c22b.png)


## Setup

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

