# given a dictionary, determine key given certain value
def value_to_key(dict,val):
    key_list = list(dict.keys())
    val_list = list(dict.values())

    position = val_list.index(val)
    key = key_list[position]
    return key

# converts dataframe column to list of ints
def df_to_intlist(df, column_name):
    list = df.loc[:,column_name].values.tolist()
    return [int(el) for el in list]