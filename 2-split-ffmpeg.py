import csv
import subprocess
import os
import re
import datetime

def TimestampToDatetime(string = "00:00:00,000",Flag = False):
    date = datetime.datetime.strptime(string, "%H:%M:%S,%f")
    if Flag:
        date = date + datetime.timedelta(seconds=1)
    return date.strftime("%H:%M:%S.%f")

if __name__=="__main__":
    if os.path.isfile("whisper.csv") == False:
        raise Exception("There's not whisper.csv. Run 1-run-whisper.py first.") 
    with open('whisper.csv', encoding='utf_8_sig') as f:
        reader = csv.reader(f)
        l = [row for row in reader]
    re_pattern = r'[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}'
    regex = re.compile(re_pattern)
    filename = None
    for list in l:
        filename = list[1] if list[0] == "file" else filename
        if list[0] == "file" or list[0] == "" or list[0] == "start":
            continue
        if filename == None:
            raise Exception("Strange csv.")
        try:
            os.mkdir(filename.split("\/")[-1].split(".")[0])
        except:
            pass
        if re.match(re_pattern, list[0]):
            list[0] = TimestampToDatetime(list[0])
            list[1] = TimestampToDatetime(list[1],True)
            subprocess.run(["ffmpeg","-ss", list[0],"-to",list[1], "-i", filename, filename.split("\/")[-1].split(".")[0]+"\\"+re.sub(r'[\\/:*?"<>|]+','-',list[0].split(".")[0]+"_"+list[2])+".mp3"])
    os.rename("whisper.csv", filename.split("\/")[-1].split(".")[0]+".csv")