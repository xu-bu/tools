import json
import os
import re
import shutil
import sys

import requests
from tqdm import tqdm

# if cookie expires, open a bilibili video, F12, network, choose the file starts with '?spm_id.....' and copy the cookie
headers={
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "cookie": "buvid3=1078803D-6D76-FC69-2D28-201F6ADF0D7736482infoc; nostalgia_conf=-1; _uuid=8121A1CE-368F-C8DD-9ECB-82BC71A101A7A38542infoc; b_nut=100; CURRENT_FNVAL=4048; rpdid=|(JkY||)kkRm0J'uYYmRuRRl~; buvid_fp_plain=undefined; DedeUserID=5797178; DedeUserID__ckMd5=b76dc25ffe023481; CURRENT_QUALITY=0; blackside_state=1; buvid4=328CF533-6A51-F28A-96EB-819CB224519971101-022080908-sZiQyrxq7Q6JZ/hoabJScA==; fingerprint=027dfe34b121c104cc6d5baa5632013d; buvid_fp=d64cc827e753a1afb8137786e573e892; i-wanna-go-back=-1; b_ut=5; PVID=1; balh_server_inner=__custom__; balh_server_custom=https://api.atri.ink; balh_is_closed=; SESSDATA=1c3fa7b1,1690842432,20799*22; bili_jct=2ef7af59652332decca402c41f9fea5a; bp_video_offset_5797178=758015368070430800; b_lsid=DC1E4E2F_1861233A78A; innersign=1; sid=8plnkx7i; theme_style=light",
    "Referer":"http://www.bilibili.com/"
}


def downLoad(url,fileName):
    resp=requests.get(url=url,headers=headers,stream=True)
    with open(fileName, 'wb') as file, tqdm(
            desc=fileName,
            total = int(resp.headers.get('content-length', 0)),
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

def main():
    video_url=sys.argv[1]
    response = requests.get(url=video_url, headers=headers).text
    # print(response)
    video_name = re.findall('name="title" content="(.*?)">', response)[0]
    print('下载中---请稍等---')
    jsonData = re.findall("window.__playinfo__=(.*?)</script>", response)[0]
    dic = json.loads(jsonData)
    video_link = dic['data']['dash']['video'][0]['baseUrl']
    audio_link = dic['data']['dash']['audio'][0]['baseUrl']
    # if no extra option, download video, otherwise just download audio
    downLoad(audio_link, "audio.mp3")
    if (len(sys.argv) == 2):
        downLoad(video_link, "video.mp4")
        print(video_link)
    else:
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        shutil.move('audio.mp3', desktop)
        return

    os.system(f'ffmpeg -i "video.mp4" -i "audio.mp3" -c copy "{video_name}.mp4"')
    os.remove("video.mp4")
    os.remove("audio.mp3")
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    shutil.move(f'{video_name}.mp4', desktop)

main()