import datetime
import json


def h_filter(json_dict, num):
    output_dict = {'articles': []}
    counter = 0
    for x in json_dict['articles']:
        if (x['author'] != '' and x['author'] is not None and
                x['description'] != '' and x['description'] is not None and
                x['title'] != '' and x['title'] is not None and
                x['url'] != '' and x['url'] is not None and
                x['urlToImage'] != '' and x['urlToImage'] is not None and
                x['publishedAt'] != '' and x['publishedAt'] is not None and
                x['source']['id'] != '' and x['source']['id'] is not None and
                x['source']['name'] != '' and x['source']['name'] is not None
        ):
            # print(x)
            # print("\n")
            output_dict['articles'].append(x)
            counter = counter + 1
        if counter == num:
            break
    return output_dict


def search_filter(headlines):
    print(headlines)
    output_dict = {'articles': [],'num' : 0}
    for x in headlines['articles']:
        if (x['author'] != '' and x['author'] is not None and
                x['description'] != '' and x['description'] is not None and
                x['title'] != '' and x['title'] is not None and
                x['url'] != '' and x['url'] is not None and
                x['urlToImage'] != '' and x['urlToImage'] is not None and
                x['publishedAt'] != '' and x['publishedAt'] is not None and
                x['source']['name'] != '' and x['source']['name'] is not None
        ):
            output_dict['articles'].append(x)
            output_dict['num'] = output_dict['num'] + 1
    print(output_dict['num'])
    return output_dict
