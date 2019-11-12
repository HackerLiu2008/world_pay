import json
import re
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/54.0.2840.99 Safari/537.36',
           'Cookie': "MoodleSession=ab45aa28ac2bfcf1fd34798957dc533a", }


def watch_mv(cour_id, sect_id, cm_id):
    # login_url = "http://jiangxi.ouchn.cn/theme/blueonionre/modulesCompletion.php?cmid={}&id={}&sectionid={}".format(
    #     cm_id, cour_id, sect_id)
    url = 'http://jiangxi.ouchn.cn/mod/page/view.php?id={}'.format(cm_id)
    rs = requests.get(url, headers=headers, allow_redirects=False)
    print(rs.headers)

    login_url = "http://jiangxi.ouchn.cn/course/view.php?id={}&sectionid={}&mid={}".format(cour_id, sect_id, cm_id)

    resp = requests.post(login_url, headers=headers)
    print(resp.headers)
    print(resp.text)


# watch_mv()


# 获取每一个专题的视屏id
def get_detail(sect_id, curse_id):
    url = "http://jiangxi.ouchn.cn/theme/blueonionre/sectionInfo.php"
    data = {'sectionid': sect_id,
            'courseid': curse_id}
    # courseid 在url中可以看到,修改是否观看视屏id相同

    resp = requests.post(url, data=data, headers=headers)
    one_zhuanti = json.loads(resp.text)
    kecheng_list = list()
    for values in one_zhuanti.values():
        if isinstance(values, dict):
            res_type = values.get('type')
            if res_type == 'page':
                # print(values)
                mv_id = values.get('id')
                kecheng_list.append(mv_id)
    return kecheng_list


# 课程i获取
def get_course_id():
    url = "http://jiangxi.ouchn.cn/my/"
    resp = requests.get(url, headers=headers)
    text = resp.text
    title = re.findall('data-key="([0-9]*)"', text)
    return title


def get_sectionid(course):
    url = "http://jiangxi.ouchn.cn/course/view.php?id={}".format(course)
    resp = requests.get(url, headers=headers)
    text = resp.text
    sectionid_url = re.findall('<a class="" onclick="" href="(.*?id=\d+)">', text)[0]
    res = requests.get(sectionid_url, headers=headers, allow_redirects=False)
    sect_index_url = res.headers.get('Location')
    sectionid = re.findall('\d+', sect_index_url)[1]
    courseid = re.findall('\d+', sect_index_url)[0]
    get_data = "http://jiangxi.ouchn.cn/theme/blueonionre/sectionInfo.php"
    data = {
        "sectionid": sectionid,
        "courseid": courseid
    }
    resp = requests.post(get_data, data=data, headers=headers)
    dict_info = json.loads(resp.text)
    data = dict_info.get('secinfo')
    sectionid_list = list()
    for i in data.values():
        if isinstance(i, dict):
            sectionid = i.get('id')
            sectionid_list.append(sectionid)
    return sectionid_list


def run():
    cour_list = get_course_id()
    for i in cour_list:
        print(i)
        sele = get_sectionid(i)
        print(sele)
        for n in sele:
            mid = get_detail(n, i)
            print(mid)
            for a in mid:
                watch_mv(i, n, a)


if __name__ == "__main__":
    run()
    # res = get_detail()
