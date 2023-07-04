import pandas as pd



def get_file_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = file.read().strip().split('\n')
    return data


data = get_file_data('responses.txt')
headers  = data[0]
body = data[1:]

# body is a list of strings, each string is a row and cells are separated by pipes |

df = pd.DataFrame([x.split('|') for x in body], columns=headers.split('|'))
df.to_csv('responses.csv', index=False)