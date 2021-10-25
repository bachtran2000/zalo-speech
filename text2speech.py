
import requests
import datetime
import os
import re
import time
import nltk
from urllib.parse import quote


class text2voice:

    def get_payload():
        f = open('payload.txt','r')
        payload = f.read()
        return payload

    def zalo_api(payload):
        s = "2|1.0"
        settingArr = s.split("|")
        url = "https://zalo.ai/api/demo/v1/tts/synthesize"
        f = open("output.txt", "w")
        links = []
        for p in payload:
            text = quote(str(p))

            # text.encode('utf-8')  # Totally fine.
            payload = "input="+text+"&speaker_id=" + \
                settingArr[0]+"&speed="+settingArr[1]+"&dict_id=0"+"&encode_type=1"
            headers = {
                "content-type": "application/x-www-form-urlencoded; charset=utf-8",
                "origin": "https://zalo.ai",
                "referer": "https://zalo.ai/experiments/text-to-audio-converter",

                "cookie": "zpsid=eMKnVbo-PZEvNHqtDTKIOgHQ7p4nrWzalI47O4wZJssuT3bRV_irVuyWFcWShorgrNnyH1sN7H_cHL08DySx4jayN3Kgv2SblZf95sovCHgQRaSg; zai_did=8k9uAj3FNiTevcSSryzXoYYo64d0o6V3AB4PHJ8q; zpsidleg=eMKnVbo-PZEvNHqtDTKIOgHQ7p4nrWzalI47O4wZJssuT3bRV_irVuyWFcWShorgrNnyH1sN7H_cHL08DySx4jayN3Kgv2SblZf95sovCHgQRaSg; zai_sid=lf2zTzCfGqIZbxznrofUGhhifo2eNnvBlxcP6va7P5c8xPue-bDyJDAnt0JxQqmvuOZmID4xQZJUyVnrp1Xs0xdtwLUAHM0ydQFdQl1IIGRigkzd; __zi=3000.SSZzejyD0jydXQcYsa00d3xBfxgP71AM8Tdbg8yB7SWftQxdY0aRp2gIh-QFHXF2BvMWxp0mDW.1; fpsend=149569; _zlang=vn"
            }

            response = requests.request(
                "POST", url, data=payload.encode('utf-8'), headers=headers)
            f.write(response.text+"\n")
            time.sleep(5)

        out = open('output.txt', 'r').read()

        links = re.findall(
            r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}.m3u8)', out)
        f.close()
        return links

    def split_text(payload):
        text = []
        long_sentence = []
        if len(payload) <= 2000:
            text.append(payload)
            return text
        elif len(payload) > 2000:
            sentences = nltk.sent_tokenize(payload)
            sub_para = ''

            for sen in sentences:
                if sub_para == '':
                    sub_para = sen

                elif sub_para != '':
                    if len(sub_para)+len(sen) <= 2000 and sen != sentences[-1]:
                        sub_para = sub_para + " " + sen

                    elif len(sub_para)+len(sen) <= 2000 and sen == sentences[-1]:
                        sub_para = sub_para + " " + sen
                        long_sentence.append(sub_para)

                    elif len(sub_para)+len(sen) > 2000:
                        long_sentence.append(sub_para)
                        sub_para = ''
                        sub_para = sen

                    elif sen == sentences[-1]:
                        long_sentence.append(sub_para)

        return long_sentence

    def connect_audio(links):
        id = 1
        path = str(os.getcwd())
        full = path + '/tmp_audio/'
        command = 'cd '+full+' && rm -rf *'
        os.system(command)
        f = open('list_name.txt', 'w')
        for i in links:
            url = i
            des_fol = str(os.getcwd())+"/tmp_audio/"
            namefile = str(id)+".mp3"
            command = 'ffmpeg  -i '+url+' -ab 32k ' + des_fol + namefile + ' -y'
            id = id + 1
            os.system(command)
            f.write("file '"+full+namefile+"'\n")
        f.close()
        print("done")

    def get_links():
        out = open('output.txt', 'r').read()
        links = re.findall(
            r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}.m3u8)', out)
        return links

    def mer_audio(id):
        path_list = str(os.getcwd()) + "/list_name.txt"

        x = datetime.datetime.now()
        day = x.day
        month = x.month
        date = str(day)+'_'+str(month)+'/'
        path = str(os.getcwd())+"/audio/"+date

        if os.path.exists(path):
            mp3_path = path+id+".mp3"
            command = 'ffmpeg -f concat -safe 0 -i ' + \
                path_list + ' -c copy '+mp3_path + ' -y'
            os.system(command)

        else:
            aupath = os.getcwd() + "/audio/"
            os.system("cd " + aupath + " && mkdir "+date)
            mp3_path = path+id+".mp3"
            command = 'ffmpeg -f concat -safe 0 -i ' + \
                path_list + ' -c copy '+mp3_path + ' -y'
            os.system(command)

        mp3_path = mp3_path.replace(os.getcwd(), '.')

        return mp3_path

class final_path_mp3():
    def get_path_mp3(id,payload):
        data = text2voice.split_text(payload)
        text2voice.zalo_api(data)
        links = text2voice.get_links()
        text2voice.connect_audio(links)
        path = text2voice.mer_audio(id)

        return path


payload = text2voice.get_payload() # read file payload.txt for the payload send to zalo
print(payload)
id = 'test' # Change this for the name file mp3
path = final_path_mp3.get_path_mp3(id,payload)
print(path)
