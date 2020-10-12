from datetime import datetime
from datetime import timedelta
import urllib.request
import json

district = ""
state = ""

def main():
#main routine which call all other functions
    print("Starting main routine")
    urlName = "https://api.covid19india.org/v4/data.json"
    json_data = retrieve_json_data(urlName)
    curr_data = read_json_current_day(json_data)

    #urlName - "https://api.covid19india.org/v4/data-YYYY-MM-DD.json"
    curr_date = datetime.now() - timedelta(days=1)
    prev_date = curr_date - timedelta(days=1)
    curr_date_str = curr_date.strftime('%Y-%m-%d')
    prev_date_str = prev_date.strftime('%Y-%m-%d')
    
    urlName = "https://api.covid19india.org/v4/data-" + prev_date_str + ".json"
    json_data = retrieve_json_data(urlName)
    prev_data = read_json_past_day(json_data)

    print("Data from " + curr_date_str)
    print("Confirmed cases  - ", curr_data["confirmed"])
    print("Deceased cases   - ", curr_data["deceased"])
    print("Recovered cases  - ", curr_data["recovered"])
    print("Total tests done - ", curr_data["tested"])

    print("\nData from " + prev_date_str)
    print("Confirmed cases  - ", prev_data["confirmed"])
    print("Deceased cases   - ", prev_data["deceased"])
    print("Recovered cases  - ", prev_data["recovered"])
    print("Total tests done - ", prev_data["tested"])

    confDelta = int(curr_data["confirmed"]) - int(prev_data["confirmed"])
    decDelta = int(curr_data["deceased"]) - int(prev_data["deceased"])
    recvrDelta = int(curr_data["recovered"]) - int(prev_data["recovered"])

    print("\nDelta values - ")
    print("Case count increase     - ", str(confDelta))
    print("Deceased count increase - ", str(decDelta))
    print("Recovery count increase - ", str(recvrDelta))
    print("\n")


def print_dict_key_list(dict, columns = 5):
#Prints the keys of a dictionary object
#columns = how many keys will be printed per newline, default = 5
    i = 0
    keys_list = list(dict.keys())
    keylist_str = ""
    for item in keys_list:
        if keylist_str == "":
            if len(item) >= 8:
                keylist_str = item + "\t"
            else:
                keylist_str = item + "\t\t"
        else:
            if len(item) >= 8:
                keylist_str = keylist_str + item + "\t"
            else:
                keylist_str = keylist_str + item + "\t\t"
        i = i + 1
        if (i % columns) == 0:
            print(keylist_str)
            keylist_str = ""
    if keylist_str != "":
        print(keylist_str + "\n")


def read_json_current_day(json_data):
#reads the json data retreived from https://api.covid19india.org/v4/data.json
#provides current covid stats for chosen state > district in a dictionary
#returns dictionary
    global state
    global district

    print("Starting json_data\n")
    dict_json = json.loads(json_data)
    print("List of States - \n")
    print_dict_key_list(dict_json, 6)

    state = input("\nEnter state from list - ").upper()
    print("\n")
    if state in dict_json:
        print("Districts in chosen state - \n")
        print_dict_key_list(dict_json[state]["districts"],4)
        district = input("\nEnter district from list - ").capitalize()
        print("\n")
        if district in dict_json[state]["districts"]:
            print("\nPrinting data for - " + district)
            case_data = dict_json[state]["districts"][district]["total"]
            # print(type(case_data))
            return case_data
        else:
            print("Error - District data not available for past dates")
    else:
        print("Error - State data not available for past dates")


def read_json_past_day(json_data):
#reads the json data retrieved from "https://api.covid19india.org/v4/data-YYYY-MM-DD.json"
# for a specified date
# does not ask user for state/district but uses the values provided earlier when running read_json_current_day
#returns dictionary
    global state
    global district

    dict_json = json.loads(json_data)

    if state in dict_json:
        if district in dict_json[state]["districts"]:
            case_data = dict_json[state]["districts"][district]["total"]
            # print(type(case_data))
            return case_data
        else:
            print("Error - District data not available for past dates")
    else:
        print("Error - State data not available for past dates")


def retrieve_json_data(urlName):
#returns json-data from a URL
    urlData = urlName
    webUrl = urllib.request.urlopen(urlData)
    #print("result code : " + str(webUrl.getcode()))
    if(webUrl.getcode() == 200):
        print("Url access successful\n")
        data = webUrl.read()
        return data
    else:
        print("Error accessing json")


if __name__ == "__main__":
    main()
