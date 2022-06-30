# url = 'http://webcode.me'
# url = 'https://en.wikipedia.org/wiki/Tartus' MemoryError
# url='https://lavasoft.gosearchresults.com/?q=store+sorted+dictionary+python&tt=vmn__webcompa__1_0__go__lvs__webcompa__1_0__go__ch_WCYID10270_200711__yrff__yrff&pid=5ac784309091147a162b4431'
# url = 'https://eclass.hiast.edu.sy'
# url= 'https://www.w3schools.com/'
# url = 'http://www.cad.zju.edu.cn/home/dengcai/VIPS/VIPS.html'
# url = 'https://www1.se.cuhk.edu.hk/~textmine/code/segmentation/' 5
# url = 'https://www.researchgate.net/publication/333576545_Alternative_Nonvisual_Web_Browsing_Techniques' #6
# url = 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5708566/' #8 child
# url = 'https://www.tutorialspoint.com/beautiful_soup/beautiful_soup_navigating_by_tags.htm'
# url = 'https://usabilitygeek.com/designing-content-heavy-websites/'
# url = 'https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/'
# url = 'https://stackoverflow.com/questions/12994442/how-to-append-data-to-a-json-file'
# url='http://03online.com/news/uzi_golovnogo_mozga/2014-10-13-40881'
import gc
import sys

with open('C:/Users/firas/Desktop/project/data/mydata.txt', 'r') as f:
    for line in f:
        line = line.rstrip()
        split_line = line.split(' ')
        site_id = split_line[0]
        site_url = split_line[1]
        page_id = split_line[2]
        page_url = split_line[3]
        print(page_id)
        script_descriptor = open("clustering.py")
        a_script = script_descriptor.read()
        sys.argv = [page_url, 10, 100000, page_id]
        exec(a_script)
        script_descriptor.close()
        del script_descriptor
        gc.collect()
