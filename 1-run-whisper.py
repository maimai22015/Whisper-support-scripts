import csv
import os
import subprocess
import re

if __name__=="__main__":
    inputfile = input("音声ファイルを選択 Select sound.")
    inputfile = inputfile[1:-2] if inputfile[0]=="\"" else inputfile
    if os.path.isfile(inputfile) == False:
        raise Exception('ファイルパスを入力してください input file path.') 
    subprocess.run(["whisper", inputfile, "--model","large","--language", "Japanese"])

    # This part of code is from https://bit.ly/3UcmWeN
    with open(inputfile.split("\\")[-1]+'.srt', 'r', encoding="utf-8") as h:
        sub = h.readlines()
    re_pattern = r'[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3} -->'
    regex = re.compile(re_pattern)
    # Get start times
    start_times_list = list(filter(regex.search, sub))
    start_times = [time.split(' ')[0] for time in start_times_list]
    end_times = [time.split(' ')[-1] for time in start_times_list]
    # Get lines
    lines = [[]]
    for sentence in sub:
        if re.match(re_pattern, sentence):
            lines[-1].pop()
            lines.append([])
            lines[-1].append(sentence.split(' ')[0])
            lines[-1].append(sentence.split(' ')[-1][:-1])
        else:
            lines[-1].append(sentence[:-1])
    lines = lines[1:]
    # end

    with open("whisper.csv", 'w', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["file", inputfile, "","",""])
        writer.writerow(["", "", "","",""])
        writer.writerow(["start", "end", "text","pre","post"])
        writer.writerows(lines)

    print("Memo : 同じ出力が続いている場合は認識に失敗している可能性が高いです。再実行するかファイルを分割してください。")
    print("Memo : 同じファイルでも再実行すると出力が変わる場合があります")
    print("Memo : 出力されたWhisper.csvの中身を確認し、誤認識を修正の上 2-split-ffmpeg.py を実行してください")

    subprocess.call('PAUSE', shell=True)