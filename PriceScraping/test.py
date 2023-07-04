
import pandas as pd


df_1 = pd.read_csv('products.csv')
df_2 = pd.read_csv('products_x.csv')


urls = df_2['URL'].tolist()
fixed_price = df_2['Discounted Price'].tolist()
old_price = df_2['Original Price'].tolist()
retailers = df_2['Retailer'].tolist()



for row_index, single_link in enumerate(urls):
    if str(retailers[row_index]) == "noon":
        # change column 9th and where the link is same
        df_1.loc[df_1['Web Link.1'] == single_link, 'Discounted Price.1'] = fixed_price[row_index]
        df_1.loc[df_1['Web Link.1'] == single_link, 'Original Price.1'] = old_price[row_index]

    elif str(retailers[row_index]) == "sharafdg":
        df_1.loc[df_1['Web Link.4'] == single_link, 'Discounted Price.4'] = fixed_price[row_index]
        df_1.loc[df_1['Web Link.4'] == single_link, 'Original Price.4'] = old_price[row_index]

    elif str(retailers[row_index]) == "menakart":
        df_1.loc[df_1['Web Link.3'] == single_link, 'Discounted Price.3'] = fixed_price[row_index]
        df_1.loc[df_1['Web Link.3'] == single_link, 'Original Price.3'] = old_price[row_index]

    elif str(retailers[row_index]) == "amazon":
        df_1.loc[df_1['Web Link'] == single_link, 'Discounted Price'] = fixed_price[row_index]
        df_1.loc[df_1['Web Link'] == single_link, 'Original Price'] = old_price[row_index]

    elif str(retailers[row_index]) == "istyle":
        df_1.loc[df_1['Web Link.2'] == single_link, 'Discounted Price.2'] = fixed_price[row_index]
        df_1.loc[df_1['Web Link.2'] == single_link, 'Original Price.2'] = old_price[row_index]






# save in new csv file: rock.csv
df_1.to_csv('rock.csv', index=False)





