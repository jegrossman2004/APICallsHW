import requests.exceptions
import pandas as pd

if __name__ == '__main__':

    country = input("Enter a country name: ")
    file_name = "output.json"
    try:
        with open(file_name) as file:
            df = pd.read_json(file)
            # This is from the 1st link in my sources.
    except:
        # Need this try except because if output.json is empty, I need to manually initialize the data frame because it
        # gives an error when I try to read it in when its empty
        df = pd.DataFrame(columns=['name', 'capital', 'population'])
    url = "https://restcountries.com/v3.1/name/%s?fields=name,capital,population" % country
    try:
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        row = pd.json_normalize(result)[['name.common', 'capital', 'population']]
        if row.iloc[0, 0].lower() == country.lower():
            row = [row.iloc[0, 0], row.iloc[0, 1][0], row.iloc[0, 2]]
            # Gets the name, capital, and population into row
            df.loc[df.size] = row
            # Adds row into df
            for i in range(0, 3):
                print(df.columns.values[i] + ": " + str(row[i]))
                # I have this for loop here because just printing row only gave me the values, not the labels
            with open(file_name, 'w') as file:
                df.to_json(file_name, orient='records')
                # After appending the row to the df, it is put into output.json
        else:
            print("ERROR: Country is not in API")
            # If I entered "b" it would say it's valid, but it's not. That's what this else statement is for

    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred: No such country exists in the API " + repr(errh))
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the API occurred: " + repr(errc))
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred: " + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred: " + repr(err))

# Sources:
# https://web.stanford.edu/class/archive/cs/cs106a/cs106a.1204/handouts/py-file.html
# https://www.geeksforgeeks.org/what-does-s-mean-in-a-python-format-string/
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_json.html
