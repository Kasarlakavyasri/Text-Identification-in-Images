#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: Prathyusha Reddy Thumma(pthumma) and Kavya Sri Kasarla(kkasarla)
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys
import math

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25

trans_dict1={}
alpha_dict={}
init_alpha_dict={}
trans_dict2={}
trans_dict3={}

def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    
    res = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        res += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return res

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

#####
# main program

if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

def load_file():
    s=""
    with open("train-text.txt") as text_file:
        lines = [line.strip() for line in text_file]
    return lines


def simplified(test_letters,train_letters):
    simp=""
    keys=[]
    for key in train_letters.keys():
        keys.append(key)

    res=[""]*len(test_letters)
    for i in range(0,len(test_letters)):
        list_cnt=[]
        tmp=0
        tmp_1=0
        for let in train_letters.keys():
             cnt_1=0
             cnt_2=0
             cnt_3=0
             for j in range(0,25):
                for k in range(0,14):
                    if train_letters[let][j][k]==test_letters[i][j][k]=="*":
                        cnt_1+=1
                    elif train_letters[let][j][k]==test_letters[i][j][k]==" ":
                        cnt_3+=1
                    else:
                        cnt_2+=1
             list_cnt.append((0.9*cnt_1+0.05*cnt_2+0.4*cnt_3)/350)

        for p in range(0,len(list_cnt)):
            if list_cnt[p]>tmp:
                tmp=list_cnt[p]
                tmp_1=p
        simp=simp+keys[tmp_1]


    return simp

print("Simple:",simplified(test_letters,train_letters))

def calc_probability(st,obs_pixels):
    prb_1=1
    prb_2=0
    prb_3=0
    n=0
    for i in range(0,25):
        for j in range(0,14):

            if obs_pixels[i][j]==train_letters[st][i][j]=="*":
                prb_1=prb_1+1
            elif obs_pixels[i][j]==train_letters[st][i][j]==" ":
                prb_3=prb_3+1
            elif obs_pixels[i][j]!=train_letters[st][i][j]:
                prb_2=prb_2+1
    n = (0.3 * prb_3 + 0.6 * prb_1 + 0.1 * prb_2) / 350

    return n

def trans_probability():
    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    lin=load_file()
    n=0
    for i in range(0,len(lin)):
        for j in range(0,len(lin[i])):
            n+=1

            if lin[i][j] in alpha_dict.keys():
                alpha_dict[lin[i][j]]+=1
            else:
                alpha_dict[lin[i][j]]=1

    for i in range(0,len(lin)):
        if lin[i]!="":
            if lin[i][0] in init_alpha_dict.keys():
                init_alpha_dict[lin[i][0]]+=1
            else :
                init_alpha_dict[lin[i][0]] = 1

    for i in init_alpha_dict.keys():
        init_alpha_dict[i]=init_alpha_dict[i]/len(lin)

    for i in range(0,len(TRAIN_LETTERS)):
        if TRAIN_LETTERS[i] not in init_alpha_dict.keys():
            init_alpha_dict[TRAIN_LETTERS[i]]=10**-9

    for i in range(0,len(lin)):
        for j in range(0,len(lin[i])-1):

            it=""
            it=it+lin[i][j]+"."+lin[i][j+1]
            if it in trans_dict1.keys():
                trans_dict1[it]+=1
            else:
                trans_dict1[it]=1

    for i in range(0,len(TRAIN_LETTERS)):
        for j in range(0,len(TRAIN_LETTERS)):
            it_new=""
            it_new=it_new+TRAIN_LETTERS[j]+"."+TRAIN_LETTERS[i]
            if it_new in trans_dict1.keys() and TRAIN_LETTERS[j] in alpha_dict.keys():
                trans_dict1[it_new]=trans_dict1[it_new]/alpha_dict[TRAIN_LETTERS[j]]
            elif it_new not in trans_dict1.keys():
                trans_dict1[it_new]=10**-12
    for i in alpha_dict.keys():
        alpha_dict[i]=alpha_dict[i]/n

    for i in range(0,len(TRAIN_LETTERS)):
        if TRAIN_LETTERS[i] not in alpha_dict.keys():
            alpha_dict[TRAIN_LETTERS[i]]=10**-7

def trans_probability_new():
    new_dict_alpha={}
    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    lin=load_file()
    for i in range(0,len(lin)):
        for j in range(0,len(lin[i])-1):
            it=lin[i][j]+lin[i][j+1]
            if it in trans_dict2.keys():
                trans_dict2[it]+=1
            else:
                trans_dict2[it]=1

    for i in range(0,len(lin)):
        for j in range(0,len(lin[i])):
            if lin[i][j] in new_dict_alpha.keys():
                new_dict_alpha[lin[i][j]]+=1
            else:
                new_dict_alpha[lin[i][j]]=1
    lst_1=[]
    lst_1=new_dict_alpha.keys()
    lst_2=[]
    lst_2=trans_dict2.values()
    
    for i in lst_1:
        for j in lst_1:
            if i+j in trans_dict2.keys() and i+j in new_dict_alpha.keys():
                
                trans_dict2[i + j] = trans_dict2[i + j] /(new_dict_alpha[i]+init_alpha_dict[j])
                
            else:
                trans_dict2[i+j]=10**-7

    for i in TRAIN_LETTERS:
        for j in TRAIN_LETTERS:
            if i+j in trans_dict2.keys():
                trans_dict3[i+j]=trans_dict2[i+j]
            else:
                trans_dict3[i+j]=10**-5

    for i in TRAIN_LETTERS:
        for j in TRAIN_LETTERS:
            if i+j not in trans_dict2.keys():
                trans_dict2[i+j]=10**-9
trans_probability()
trans_probability_new()


def viterbi(train_letters,test_letters):
    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    res_1 = []
    res_2=[]
    for j in range(0,len(TRAIN_LETTERS)):
        res_2.append(math.log(calc_probability(TRAIN_LETTERS[j],test_letters[0]),2))
    res_1.append(res_2)
    for i in range(1,len(test_letters)):
        res_2=[]
        tmp_2=[]
        tmp_3=[]
        for k in range(0,len(TRAIN_LETTERS)):
            tmp=0
            tmp_1=0
            for j in range(0,len(TRAIN_LETTERS)):
                temp3=0
                it=TRAIN_LETTERS[k]+TRAIN_LETTERS[j]
                temp3=res_1[i-1][j]+math.log(trans_dict3[it],2)
                if temp3>tmp:
                    tmp=temp3
                    tmp_1=j
            res_2.append(tmp+math.log(calc_probability(TRAIN_LETTERS[k],test_letters[i]),2))
            tmp_2.append(tmp_1)
        res_1.append(res_2)
        tmp_3.append(tmp_2)
    res=""
    for i in range(0,len(test_letters)):
        tmp_5 = 0
        tmp=-9999999999999
        for j in range(0,len(TRAIN_LETTERS)):
            if res_1[i][j]>tmp:
                tmp=res_1[i][j]
                tmp_5=j
        res=res+TRAIN_LETTERS[tmp_5]
    print("HMM :",res)
viterbi(train_letters,test_letters)




# The final two lines of your output should look something like this:
#print("Simple: " + "Sample s1mple resu1t")
#print("   HMM: " + "Sample simple result") 


