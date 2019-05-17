import json
import csv
import requests
import threading
from lxml import etree
from multiprocessing import Queue


def requests_get():
    f = open('奔驰.csv', 'a+', encoding='gbk', newline='')
    wri = csv.writer(f)
    wri.writerow(['公司', '地区', '市级', '地址', '品牌', '类型', '前台', '职位', '姓名', '电话'])
    city_dict = {'北京': '北京市',
                 '天津': '天津市',
                 '上海': '上海市',
                 '重庆': '重庆市',
                 '河北': '石家庄市、唐山市、秦皇岛市、邢台市、保定市、张家口市、承德市、沧州市、廊坊市、衡水市',
                 '山西': '太原市、大同市、朔州市、阳泉市、长治市、晋城市、忻州市、晋中市、临汾市、运城市、吕梁市',
                 '内蒙古': '呼和浩特市、包头市、乌海市、赤峰市、通辽市、鄂尔多斯市、呼伦贝尔市、巴彦淖尔市、乌兰察布市',
                 '辽宁': '沈阳市、大连市、鞍山市、抚顺市、本溪市、丹东市、锦州市、营口市、阜新市、辽阳市、盘锦市、铁岭市、朝阳市、葫芦岛市',
                 '吉林': '长春市、吉林市、四平市、辽源市、通化市、白山市、松原市、白城市',
                 '黑龙江': '哈尔滨市、齐齐哈尔市、牡丹江市、佳木斯市、七台河市、大庆市、黑河市、绥化市、伊春市、鹤岗市、双鸭山市、鸡西市',
                 '江苏': '常州市、徐州市、南京市、淮安市、南通市、宿迁市、无锡市、扬州市、盐城市、苏州市、泰州市、镇江市、连云港市',
                 '浙江': '杭州市、湖州市、嘉兴市、金华市、丽水市、宁波市、衢州市、绍兴市、台州市、温州市、舟山市',
                 '安徽': '合肥市、蚌埠市、芜湖市、淮南市、马鞍山市、淮北市、铜陵市、安庆市、黄山市、阜阳市、宿州市、滁州市、六安市、宣城市、巢湖市、池州市、亳州市',
                 '福建': '福州市、龙岩市、南平市、宁德市、莆田市、泉州市、三明市、厦门市、漳州市',
                 '江西': '南昌市、九江市、上饶市、抚州市、宜春市、吉安市、赣州市、景德镇市、萍乡市、新余市、鹰潭市',
                 '山东': '枣庄市、济南市、德州市、济宁市、临沂市、青岛市、泰安市、威海市、淄博市、菏泽市、烟台市、莱芜市、滨州市、东营市、聊城市、日照市、潍坊市',
                 '河南': '郑州市、开封市、洛阳市、平顶山市、安阳市、鹤壁市、新乡市、焦作市、濮阳市、许昌市、漯河市、三门峡市、南阳市、商丘市、信阳市、周口市、驻马店市',
                 '湖北': '武汉市、黄石市、襄阳市、荆州市、宜昌市、十堰市、孝感市、荆门市、鄂州市、黄冈市、咸宁市、随州市',
                 '湖南': '长沙市、株洲市、湘潭市、衡阳市、邵阳市、岳阳市、常德市、张家界市、益阳市、郴州市、永州市、怀化市、娄底市',
                 '广东': '广州市、深圳市、珠海市、汕头市、佛山市、韶关市、湛江市、肇庆市、江门市、茂名市、惠州市、梅州市、汕尾市、河源市、阳江市、清远市、东莞市、中山市、潮州市、揭阳市、云浮市',
                 '广西': '南宁市、柳州市、桂林市、梧州市、北海市、防城港市、钦州市、贵港市、玉林市、百色市、贺州市、河池市、来宾市、崇左市',
                 '海南': '海口市、三亚市',
                 '四川': '成都市、绵阳市、自贡市、攀枝花市、泸州市、德阳市、广元市、遂宁市、内江市、乐山市、资阳市、宜宾市、南充市、达州市、雅安市、广安市、巴中市、眉山市',
                 '贵州': '贵阳市、遵义市、安顺市、六盘水市、毕节市、铜仁市、清镇市、赤水市、仁怀市、盘州市、凯里市、都匀市、福泉市、兴义市、兴仁市',
                 '云南': '昆明市、曲靖市、昭通市、玉溪市、普洱市、保山市、丽江市、临沧市',
                 '西藏': '拉萨市',
                 '陕西': '西安市、宝鸡市、咸阳市、铜川市、渭南市、延安市、榆林市、汉中市、安康市、商洛市',
                 '甘肃': '兰州市、嘉峪关市、金昌市、白银市、天水市、武威市、张掖市、平凉市、酒泉市、庆阳市、定西市、陇南市',
                 '青海': '西宁市',
                 '宁夏': '银川市、石嘴山市、吴忠市、固原市、中卫市',
                 '新疆': '乌鲁木齐市、克拉玛依市、吐鲁番市、哈密市',



                 }

    headers = {
        'Origin': 'https://www.mercedes-benz.com.cn',
        'Referer': 'https://www.mercedes-benz.com.cn/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }
    url = "https://api.oneweb.mercedes-benz.com.cn/ow-dealers-location/dealers/query?"
    for key, value in city_dict.items():
        municipal_level_list = value.split('、')
        for city in municipal_level_list:
            params = {
                'sort': 'alphabetical',
                'city': '{}'.format(city),
                'longitude': '',
                'latitude': '',
                'keywords': '',
                'dealerId': '',
                'needFilterByModel': 'false',
                'modelName': '',
                'serviceTypeCode': '',
            }
            response = requests.get(url, params=params, headers=headers)
            data = json.loads(response.text)
            result_list = data['result']
            for result in result_list:
                websiteUrl = result['websiteUrl']
                try:
                    response = requests.get(url=websiteUrl, headers=headers)
                except:
                    print(websiteUrl)
                html = etree.HTML(response.text)
                root_node = html.xpath(".//div[@class='retail-team-container__item']")
                # 公司
                company = result['displayName'].replace('\xa0', '').replace('\u202d', '').replace('\u202c', '')
                # 地址
                address = result['address'].replace('\xa0', '').replace('\u202d', '').replace('\u202c', '')
                # 前台电话
                Reception = result['phoneNumber'].replace('\xa0', '').replace('\u202d', '').replace('\u202c', '')
                # 地区
                region = key
                # 市级
                Municipal_level = city
                # 品牌
                brand = '奔驰'
                # 类型
                brand_type = '奔驰(进口)'
                for node in root_node:
                    # 职位
                    position_name = ''.join(node.xpath(".//span[@class='job']/text()")).strip().replace('\xa0', '').replace('\u202d', '').replace('\u202c', '')

                    # 姓名
                    name = ''.join(node.xpath(".//span[@class='name']/text()")).replace('\xa0', '').replace('\u202d', '').replace('\u202c', '')

                    # 电话
                    tel = ''.join(node.xpath(".//div[@class='retail-team-container__item-mob hidden-xs']/span[@class='mob-number']/text()")).replace('\xa0', '').replace('\u202d', '').replace('\u202c', '')

                    print(company, region, Municipal_level, address, brand, brand_type, Reception, position_name, name, tel)
                    wri.writerow([company, region, Municipal_level, address, brand, brand_type, Reception, position_name, name, tel])


if __name__ == '__main__':
    all_list = []
    pageQueue = Queue()
    threadcrawl = []
    for i in all_list:
        pageQueue.put(i)
    for _ in range(3):
        t = threading.Thread(target=requests_get(), args=(pageQueue,))
        t.start()
        threadcrawl.append(t)
    for th_crawl in threadcrawl:
        th_crawl.join()
    # websiteUrl_list = requests_get()
