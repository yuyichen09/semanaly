# -*- coding:utf-8 -*-

import json
import os
import shutil
import jieba
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

data_set = "./dataset/me_train.json"
target = "./dataset/train_questions.txt"
stopwords_dict = "./dataset/stop_words_ch.txt"


def rm_stopwords(file_path, word_dict):
    """
        rm stop word for {file_path}, stop words save in {word_dict} file.
        file_path: file path of file generated by function splitwords.
                    each lines of file is format as <file_unique_id> <file_words>.
        word_dict: file containing stop words, and every stop words in one line.
        output: file_path which have been removed stop words and overwrite original file.
    """

    # read stop word dict and save in stop_dict
    stop_dict = {}
    with open(word_dict) as d:
        for word in d:
            stop_dict[word.strip("\n")] = 1
    # remove tmp file if exists
    if os.path.exists(file_path + ".tmp"):
        os.remove(file_path + ".tmp")

    print "now remove stop words in %s." % file_path
    # read source file and rm stop word for each line.
    with open(file_path) as f1, open(file_path + ".tmp", "w") as f2:
        for line in f1:
            tmp_list = []  # save words not in stop dict
            words = line.split()
            for word in words:
                if word not in stop_dict:
                    tmp_list.append(word)
            words_without_stop = " ".join(tmp_list)
            to_write = words_without_stop + "\n"
            f2.write(to_write.encode("utf8"))

    # overwrite origin file with file been removed stop words
    shutil.move(file_path + ".tmp", file_path)
    print "stop words in %s has been removed." % file_path


with open(data_set, "r") as f, open(target, "w") as f2:
    data = json.load(f)
    count = 0
    for key, value in data.iteritems():
        question = data[key]["question"]
        words = jieba.cut(question, cut_all=False)
        f2.write(" ".join(words) + "\n")
        for k, v in data[key]['evidences'].iteritems():
            words2 = jieba.cut(data[key]['evidences'][k]['evidence'], cut_all=False)
            f2.write(" ".join(words2) + "\n")
            count += 1
        count += 1
    print "all question num is %s" % count

rm_stopwords(target, stopwords_dict)

