import datetime, requests, time, os

url_aids = 'https://vc.endcloud.cn/api/mysql/json_legendary.php'
url_av = 'http://api.bilibili.com/archive_stat/stat?aid='

len_count = 0
len_content = []
restart_count = 0

interval = input('\n请输入数据刷新间隔（单位-秒，默认10秒，建议不少于5秒）：')
if interval is None or interval == '':
    interval = 10
else:
    interval = int(interval)


def timestamp2time(stamp):
    time_array = time.localtime(stamp)
    other_style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return other_style_time


def get_aids():
    target = url_aids
    headers = {'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                             '537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
               'Accept': 'application/json, text/plain, */*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
               }
    try:
        req = requests.get(headers=headers, url=target, timeout=10)
    except Exception:
        print(Exception)
    else:
        html = req.json()['data']
        return html


def get_stat(aid):
    target = url_av + str(aid)
    headers = {'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                             '537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
               'Accept': 'application/json, text/plain, */*',
               'Referer': 'https://www.bilibili.com/v/music/vocaloid/#/',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
               }
    try:
        req = requests.get(headers=headers, url=target, timeout=10)
    except Exception:
        print(Exception)
    else:
        html = req.json()
        return html


def work():
    global aids, len_count, len_content

    hour = datetime.datetime.now().strftime('%H')
    minute = datetime.datetime.now().strftime('%M')
    if hour == 3 and minute == 40:
        aids = get_aids()
        print('\n'+datetime.datetime.now().strftime('%Y-%m-%d')+'\n')

    for index, aid in enumerate(aids):
        stat = get_stat(aid[0])
        view = str(stat['data']['view']).replace('--', '0')

        print(aid[1])
        print('av号：'+aid[0])

        if int(view) >= 1000000:
            print('传说啦！' + '\n' + '-' * 60)
            len_count += 1
            info = {'aid': aid[0], 'title': aid[1], 'time': timestamp2time(time.time())}
            len_content.append(info)

            aids.pop(index)
            break

        print('播放：' + view + '\n' + '-' * 60)

    endTime = int(time.time())
    last_time = endTime - startTime
    print("程序已运行：" + str(round(last_time / 60, 2)) + '分钟，当前达成传说：'+str(len_count)+'个。')
    if len_count > 0:
        for content in len_content:
            print(content['time']+'  '+'av'+content['aid']+'-'+content['title'])


def main():
    global restart_count

    if restart_count < 3:
        try:
            restart_count += 1

            count = 1
            while True:
                '''if count == 4:
                    break'''
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print('当前时间：' + now + '，已刷新' + str(count) + '次。\n')
                work()
                count += 1
                time.sleep(interval)
                os.system('cls')
        except Exception as e:
            with open('error.log', "a", encoding='utf-8') as f:
                f.write(timestamp2time(int(time.time()))+'   '+repr(e)+'\n')
            print("发生错误，已自动重启。")
            main()
    else:
        print('无法运行，请查看同目录下error.log并联系开发者QQ：1761009404。')
        input('按下任意键退出......')


if __name__ == '__main__':
    startTime = int(time.time())

    aids = get_aids()
    os.system('cls')

    main()
