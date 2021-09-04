import random
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from apyori import apriori
import sys
import json
import argparse

def data_preprocessing(metadata, eventsdata, verbose=False):
    """
    Reads meta data and events data
    Returns cleaned meta data and merged data as dataframe

    Arguments:
        metadata -- Path to meta data
        eventsdata -- Path to events data
    """
    # read json data
    f = open(eventsdata,)
    cart = json.load(f)
    df_cart = pd.DataFrame(cart['events'])

    f = open(metadata,)
    meta = json.load(f)
    df_meta = pd.DataFrame(meta['meta'])

    # clear missing data
    df_cart.dropna(subset = ['sessionid', 'productid'], how='any', inplace=True)
    df_meta.dropna(subset = ['productid', 'category', 'subcategory', 'name'], inplace=True)

    # clear duplicates
    df_cart.drop_duplicates(subset = ['sessionid', 'productid'], inplace=True)
    df_meta.drop_duplicates(subset = ['productid'], inplace=True)

    # join meta data and cart data by productid
    df_merged = pd.merge(df_cart, df_meta, on='productid')

    # drop columns that are out of use
    df_merged.drop(['event', 'eventtime', 'price', 'brand'], axis=1, inplace=True)
    
    # show dataset information
    if verbose:
        print(df_cart.info(), df_meta.info(), df_merged.info())

    return df_meta, df_merged


def get_transactions(df, verbose=False):
    """
    Returns category-wise transactions of products
    Arguments:
        df -- merged dataframe generated by data_preprocessing function
    """

    if verbose:
        print(df.groupby(['category']).size())

    # group dataframe by firstly 'category' then 'sessionid'
    groupby_cat = df.groupby(['category', 'sessionid'])
    cat_transactions = {}

    # generate category-wise transections 
    for cat, sub_cat in groupby_cat:
        if cat[0] not in cat_transactions:
            cat_transactions[cat[0]] = []
        cat_transactions[cat[0]].append(list(sub_cat['productid']))

    return cat_transactions

    
def get_association_rules(transactions, min_support, min_confidence, min_lift, max_length):
    """
    Returns category-wise association rules using apriori algorithm
    Arguments:
        transactions -- transactions generated by get_transactions() function
        min_support -- minumum support value for apriori algorithm
        min_confidence -- minumum confidence value for apriori algorithm
        min_lift -- minumum lift value for apriori algorithm
        max_length -- maximum length for apriori algorithm
    """
    cat_rules = {}
    # generate category-wise association rules using the transactions
    for cat in transactions:
        association_rules = list(apriori(transactions[cat], min_support=min_support, min_confidence=min_confidence, min_lift=min_lift, max_length=max_length))
        cat_rules[cat] = association_rules
    return cat_rules


def recommend(cart_prods, df_meta, df_merged, rules, verbose=False):
    """
    Returns related products
    Arguments:
        cart_prods -- cart products which will be used for inference
        df_meta -- processed meta data
        df_merged -- processed merged data
        rules -- association rules created by get_association_rules() function
    """
    # # convert productid to name for visibility
    # for p in cart_prods:
    #     cart_prods = df_meta[df_meta['name'] == prod]['category'].values[0]
    related_prods = {}
    for prod in cart_prods:
        cat = df_meta[df_meta['productid'] == str(prod)]['category'].values[0]
        for item in rules[cat]:
            pair = item[0]
            items = [x for x in pair]
            if len(items) > 1 and prod == items[0]:
                    items.remove(prod)
                    for i in items:
                        related_prods[i] = item[1]
    related_prods = dict(sorted(related_prods.items(), key=lambda item: item[1]))
    print(related_prods)

    if len(related_prods) < 10:
        related_prods = recommend_best_sub_cat(cart_prods, related_prods, df_meta, df_merged)
        print(related_prods)
    elif  len(related_prods) > 10:
        best_prods = list(related_prods.keys())[-9:]
        temp_related_prods = {}
        for prod in best_prods:
            temp_related_prods[prod] = related_prods[prod]
        related_prods = temp_related_prods
        
    # convert product id results to product names
    temp_related_prods = {}
    for prod in related_prods:
        cart_prods = df_meta[df_meta['productid'] == prod]['name'].values[0]
        temp_related_prods[cart_prods] = related_prods[prod]
    related_prods = temp_related_prods

    if True:
        print(related_prods)    
    return related_prods


def recommend_best_sub_cat(cart_prods, related_prods, df_meta, df_merged):
    """
    Returns best subcategory results
    Arguments:
        cart_prods -- cart products which will be used for inference
        related_prods -- already recommended products
        df_meta -- processed meta data
        df_merged -- processed merged data
    """
    n = 10
    for prod in cart_prods:
        sub_cat = df_meta[df_meta['productid'] == prod]['subcategory'].values[0]
        rec_list = df_merged[df_merged['subcategory'] == sub_cat]['productid'].value_counts()[:n].index.tolist()
        for rec in rec_list:
            if len(related_prods) < n and rec not in related_prods:
                related_prods[rec] = 0.0000001
    return related_prods

def parse_args(argv):
    """
    Parse commandline arguments.
    Arguments:
        argv -- An argument list without the program name.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l', '--max-length', metavar='int',
        help='Max length.',
        type=int, default=None)
    parser.add_argument(
        '-s', '--min-support', metavar='float',
        help='Minimum support.',
        type=float, default=0.003)
    parser.add_argument(
        '-c', '--min-confidence', metavar='float',
        help='Minimum confidence.',
        type=float, default=0.1)
    parser.add_argument(
        '-t', '--min-lift', metavar='float',
        help='Minimum lift.',
        type=float, default=1.2)
    parser.add_argument(
        '-v', '--verbose', metavar='bool',
        help='Verbose.',
        type=bool, default=False)
    args = parser.parse_args(argv)
    return args


def main(**kwargs):
    """
    Executes recommendation system.
    """
   # Parse the arguments.
    _parse_args = kwargs.get('_parse_args', parse_args)
    args = _parse_args(sys.argv[1:])

    # Check arguments.
    if args.min_support <= 0:
        raise ValueError('minimum support should be higher than zero')

    print("Rules are being produced...")
    df_meta, df_merged = data_preprocessing('data/meta.json', 'data/events.json', args.verbose)
    transactions = get_transactions(df_merged, args.verbose)
    rules = get_association_rules(transactions, args.min_support, args.min_confidence, args.min_lift, args.max_length)
    print("Rule generation is completed!")

    # set flask api
    app = Flask(__name__)
    app.config["DEBUG"] = True
    
    @app.route('/recommendations', methods=['GET'])
    def api():
        data = json.loads(request.get_json())
        print(data)
        return jsonify(recommend(data, df_meta, df_merged, rules))

    app.run()

if __name__ == "__main__":
    main()

