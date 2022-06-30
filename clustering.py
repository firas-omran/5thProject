import math
import os

from bs4 import BeautifulSoup
from selenium import webdriver
import sys
import json
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
#options=options
driver = webdriver.Firefox()


# Find the largest nodes in the dictionary list
def find_largest_nodes(elements):
    for i in range(0, len(elements)):
        # If a node is empty or not amenable segmentation because it is the result of aggregation of two nodes
        if (elements[i][i]['tagName'] != "" and elements[i][i]['seg'] != "false"):
            # Getting the first non-empty node
            large_node = float(elements[i][i]['space'])
            break
    large = []
    # Get the biggest node
    for i in range(0, len(elements)):
        if (elements[i][i]['tagName'] != "" and elements[i][i]['seg'] != "false"):
            if large_node <= float(elements[i][i]['space']):
                large_node = float(elements[i][i]['space'])
    # Get the biggest nodes
    for i in range(0, len(elements)):
        if (elements[i][i]['tagName'] != "" and elements[i][i]['seg'] != "false"):
            if large_node == float(elements[i][i]['space']):
                large.append(i)
    return large


# Find the smallest nodes in the dictionary list
def find_smallest_nodes(elements):
    for i in range(0, len(elements)):
        # If a node is empty or not amenable segmentation because it is the result of aggregation of two nodes
        if (elements[i][i]['tagName'] != ""):
            # Getting the first non-empty node
            small_node = float(elements[i][i]['space'])
            break
    small = []
    # Get the smallest node
    for i in range(0, len(elements)):
        if (elements[i][i]['tagName'] != ""):
            if small_node >= float(elements[i][i]['space']):
                small_node = float(elements[i][i]['space'])
    # Get the smallest nodes
    for i in range(0, len(elements)):
        if (elements[i][i]['tagName'] != ""):
            if small_node == float(elements[i][i]['space']):
                small.append(i)
    return small


# Find the nearest nodes
def find_nearest_nodes(elements, index):
    mindistance = math.inf
    nearest_nodes = []
    for i in range(0, len(elements)):
        if (elements[i][i]['tagName'] != ""):
            # same node
            if (i == index):
                continue
            else:
                # distance calculator
                distane = math.sqrt((float(tagSpa[i][i]['xCentre']) - float(tagSpa[index][index]['xCentre'])) ** 2 + (
                        float(tagSpa[i][i]['yCentre']) - float(tagSpa[index][index]['yCentre'])) ** 2)
                if (distane < mindistance):
                    mindistance = distane
    # Get all nodes that are the same distance
    for i in range(0, len(elements)):
        if (elements[i][i]['tagName'] != ""):
            distane = math.sqrt((float(tagSpa[i][i]['xCentre']) - float(tagSpa[index][index]['xCentre'])) ** 2 + (
                    float(tagSpa[i][i]['yCentre']) - float(tagSpa[index][index]['yCentre'])) ** 2)
            if mindistance == distane:
                nearest_nodes.append(i)
    return nearest_nodes, mindistance


# Find the farthest nodes
def find_farthest_nodes(elements, index):
    maxdistance = 0
    farthest_nodes = []
    for i in range(0, len(elements)):
        if (elements[i][i]['tagName'] != ""):
            # same node
            if (i == index):
                continue
            else:
                # distance calculator
                distane = math.sqrt((float(tagSpa[i][i]['xCentre']) - float(tagSpa[index][index]['xCentre'])) ** 2 + (
                        float(tagSpa[i][i]['yCentre']) - float(tagSpa[index][index]['yCentre'])) ** 2)
                if (distane > maxdistance):
                    maxdistance = distane
    # Get all nodes that are the same distance
    for i in range(0, len(elements)):
        distane = math.sqrt((float(tagSpa[i][i]['xCentre']) - float(tagSpa[index][index]['xCentre'])) ** 2 + (
                float(tagSpa[i][i]['yCentre']) - float(tagSpa[index][index]['yCentre'])) ** 2)
        if maxdistance == distane:
            farthest_nodes.append(i)
    return farthest_nodes, maxdistance


def clustering(url, n_zone, max_iter):
    try:
        driver.get(url)
    except:
        global error
        error = 1
        file_error = open("C:/Users/firas/Desktop/error.txt", "a")
        file_error.write(sys.argv[3] + '\n')
        print("page not found " + sys.argv[3])
    # injection Dimensions, css and filter hidden nodes
    driver.execute_script(open("injection.js").read())
    # injection path
    driver.execute_script(open("injectXpath.js").read())
    html_code = driver.page_source
    original_stdout = sys.stdout
    # save page in html file
    with open('pagecode.html', 'w', encoding="utf-8") as f:
        sys.stdout = f
        print(html_code)
        sys.stdout = original_stdout
    f.close()
    with open('pagecode.html', 'r', encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser')
    # Delete empty paragraphs added by BeautifulSoup
    for p_tage in soup.findAll('p'):
        if len(str.strip(p_tage.text)) == 1:
            if ord(str.strip(p_tage.text)[0]) == 65279:
                p_tage.extract()
    global n_list_dom, newtagSpa, tagSpa
    # Take the direct children of the body
    zones = []
    try:
        zones = soup.find("body").findChildren(recursive=False)

    except:
        error = 1
        file_error = open("C:/Users/firas/Desktop/error.txt", "a")
        file_error.write(sys.argv[3] + '\n')
        print("page not found " + sys.argv[3])
    n_list_dom = len(zones)
    newN_list_dom = n_list_dom
    tagSpa = []
    for zone in zones:
        # Ignore hidden nodes
        if zone.get('data-cleaned'):
            newN_list_dom = newN_list_dom - 1
        elif (zone.get('data-bbox') == None):
            newN_list_dom = newN_list_dom - 1
        else:
            # Save node information in a dictionary
            boundingVal = zone.get('data-bbox').split()
            tagName = zone.name
            text = zone.text
            xPath = zone.get('data-xpath')
            tSpace = {len(tagSpa): {'tagName': tagName,
                                    'x': float(boundingVal[0]),
                                    'y': float(boundingVal[1]),
                                    'width': float(boundingVal[2]),
                                    'height': float(boundingVal[3]),
                                    'space': float(boundingVal[4]),
                                    'xCentre': float(boundingVal[2]) / 2 + float(boundingVal[0]),
                                    'yCentre': float(boundingVal[3]) / 2 + float(boundingVal[1]),
                                    'text': text,
                                    'seg': "true",
                                    'xPath': xPath}}
            tagSpa.append(tSpace)
    n_list_dom = newN_list_dom
    newtagSpa = []

    ##################################################
    def segmentation():
        global tagSpa, newtagSpa, n_list_dom
        n_iter = 1
        # n_list_dom is number of tags in body
        # To reach the maximum number of iteration
        while n_iter < max_iter:
            # Reaching the required number of clusters
            if n_zone == n_list_dom:
                break
            # The number of nodes in the dictionary is greater than the number of nodes required, so we compile
            elif n_zone < n_list_dom:
                # We find the smallest nodes
                mintagspace = find_smallest_nodes(tagSpa)
                distance = math.inf
                list_index_nearest = []
                min_node = mintagspace[0]
                # For each node, we calculate the closest nodes to it
                for mint in mintagspace:
                    ind_nearest, dist = find_nearest_nodes(tagSpa, mint)
                    if (distance > dist):
                        distance = dist
                        list_index_nearest = ind_nearest
                        min_node = mint
                index_nearest = list_index_nearest[0]
                for node in range(0, len(tagSpa)):
                    # If it is not the small node and not the proximal node
                    if (node != min_node and node != index_nearest):
                        newtagSpa.append(tagSpa[node])
                    # If the small node
                    elif (node == min_node):

                        x = min(tagSpa[min_node][min_node]['x'], tagSpa[index_nearest][index_nearest]['x'])
                        y = min(tagSpa[min_node][min_node]['y'], tagSpa[index_nearest][index_nearest]['y'])
                        w = max(tagSpa[min_node][min_node]['x'] + tagSpa[min_node][min_node]['width'],
                                tagSpa[index_nearest][index_nearest]['x'] + tagSpa[index_nearest][index_nearest][
                                    'width'])
                        h = max(tagSpa[min_node][min_node]['y'] + tagSpa[min_node][min_node]['height'],
                                tagSpa[index_nearest][index_nearest]['y'] + tagSpa[index_nearest][index_nearest][
                                    'height'])
                        width = w - x
                        height = h - y
                        mixtagSpace = {min_node: {
                            'tagName': tagSpa[min_node][min_node]['tagName'] + tagSpa[index_nearest][index_nearest][
                                'tagName'],
                            'x': x,
                            'y': y,
                            'width': width,
                            'height': height,
                            'space': width * height,
                            'xCentre': str(width / 2 + x),
                            'yCentre': str(height / 2 + y),
                            'text': tagSpa[min_node][min_node]['text'] + tagSpa[index_nearest][index_nearest]['text'],
                            'seg': "false",
                            'xPath': tagSpa[min_node][min_node]['xPath'] + tagSpa[index_nearest][index_nearest][
                                'xPath']}}
                        newtagSpa.append(mixtagSpace)
                    # If the proximal node
                    else:
                        emptytagSpace = {index_nearest: {
                            'tagName': "",
                            'x': "",
                            'y': "",
                            'width': "",
                            'height': "",
                            'space': "",
                            'xCentre': "",
                            'yCentre': "",
                            'text': "",
                            'seg': "false",
                            'xPath': ""}}
                        newtagSpa.append(emptytagSpace)
                tagSpa = newtagSpa
                newtagSpa = []

                n_iter = n_iter + 1
                n_list_dom = n_list_dom - 1
            # The number of nodes in the dictionary is less than the number of nodes required, so we segmentation
            else:
                # find the largest nodes
                maxtagspace = find_largest_nodes(tagSpa)
                # If there is no large nodes
                if (len(maxtagspace) == 0):
                    break
                largechildren = maxtagspace[0]
                minchildren = math.inf
                # We calculate for each large node the number of its direct children and choose who has the least number of children
                for maxt in maxtagspace:
                    nodepath = tagSpa[maxt][maxt]['xPath']
                    directchildren = soup.find(attrs={'data-xpath': nodepath}).findChildren(recursive=False)
                    if len(directchildren) < minchildren and len(directchildren) != 0:
                        minchildren = len(directchildren)
                        largechildren = maxt
                nodepath = tagSpa[largechildren][largechildren]['xPath']
                directchildren = soup.find(attrs={'data-xpath': nodepath}).findChildren(recursive=False)
                # If the chosen knot has no children, we set a special one that does not divide
                if len(directchildren) == 0:
                    tagSpa[largechildren][largechildren]['seg'] = 'false'
                    continue
                # We store the same node values in the dictionary except for the largest node
                for node in range(0, len(tagSpa)):
                    if node != largechildren:
                        newtagSpa.append(tagSpa[node])
                    else:
                        emptytagSpace = {largechildren: {
                            'tagName': "",
                            'x': "",
                            'y': "",
                            'width': "",
                            'height': "",
                            'space': "",
                            'xCentre': "",
                            'yCentre': "",
                            'text': "",
                            'seg': "false",
                            'xPath': ""}}
                        newtagSpa.append(emptytagSpace)
                tagSpa = newtagSpa
                newtagSpa = []
                n_list_dom = n_list_dom + len(directchildren) - 1
                # We add the sons of the biggest node in the dictionary
                for ch in directchildren:
                    if ch.get('data-cleaned'):
                        n_list_dom = n_list_dom - 1
                    elif (ch.get('data-bbox') == None):
                        n_list_dom = n_list_dom - 1
                    else:
                        boundingVal = ch.get('data-bbox').split()
                        tagName = ch.name
                        text = ch.text
                        xPath = ch.get('data-xpath')
                        tSpace = {len(tagSpa): {'tagName': tagName,
                                                'x': float(boundingVal[0]),
                                                'y': float(boundingVal[1]),
                                                'width': float(boundingVal[2]),
                                                'height': float(boundingVal[3]),
                                                'space': float(boundingVal[4]),
                                                'xCentre': float(boundingVal[2]) / 2 + float(boundingVal[0]),
                                                'yCentre': float(boundingVal[3]) / 2 + float(boundingVal[1]),
                                                'text': text,
                                                'seg': "true",
                                                'xPath': xPath}}
                        tagSpa.append(tSpace)
                n_iter = n_iter + 1
        return tagSpa

    zon = segmentation()
    return zon


global error
error = 0
zon = clustering(sys.argv[0], sys.argv[1], sys.argv[2])
driver.close()
driver.quit()
if error == 0:
    id_web_page = sys.argv[3]
    with open('C:/Users/firas/Desktop/project/data/webis-webseg-20-ground-truth/' + id_web_page + '/ground-truth.json',
              'r') as f:
        ground_data = json.load(f)
    height_web_page = ground_data['height']
    width_web_page = ground_data['width']
    list_coordinates = []
    for node in range(0, len(zon)):
        if zon[node][node]['tagName'] != "":
            x = zon[node][node]['x']
            y = zon[node][node]['y']
            width = zon[node][node]['width']
            height = zon[node][node]['height']
            list_coordinates.append([[[[x, y], [x, y + height], [x + width, y + height], [x + width, y], [x, y]]]])

    dictionary_j = {
        "id": id_web_page,
        "height": height_web_page,
        "width": width_web_page,
        "segmentations": {
            "FBO": list_coordinates
        }
    }
    path_segmentation = r'C:\Users\firas\Desktop\segmentations\\' + id_web_page
    if not os.path.exists(path_segmentation):
        os.makedirs(path_segmentation)
    with open(path_segmentation + "\clusters.json", "w") as outfile:
        json.dump(dictionary_j, outfile)
