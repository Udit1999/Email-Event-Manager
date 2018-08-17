import pandas as pd

data = pd.DataFrame.from_csv('sample.csv')
data['class'] = "NaN"

for i in range(len(data)):
    print(data['Snippets'][i])
    data.at[i,'class'] = input("Enter I or NI\n")

print(data)
data.to_csv('sample.csv')
