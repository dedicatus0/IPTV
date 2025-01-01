import requests

# 下载文件
url = 'https://raw.githubusercontent.com/yuanzl77/IPTV/refs/heads/main/live.m3u'
response = requests.get(url)
lines = response.text.splitlines()

# 提取9901端口的地址和对应的#EXTINF行
filtered_lines = []
for i in range(len(lines)):
    if '9901' in lines[i]:
        filtered_lines.append(lines[i-1])
        filtered_lines.append(lines[i])

# 写入新的文件
with open('live.m3u', 'w') as f:
    for line in filtered_lines:
        f.write(line + '\n')
