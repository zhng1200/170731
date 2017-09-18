#coding:utf-8
import os
import uniout
import time
import glob
import gensim
import numpy as np
class Model:#词向量语料，给出词语，得出词语的词向量
    def __init__(self):
        self.model = gensim.models.Word2Vec.load('BurstEventDetect50_model.m')
    def getVec(self,word):
        return self.model[word]
    
class getFile:#获取一周的工单
    def __iter__(self):
        filenames=glob.glob(u"*.seg")
        
        for file in filenames:
            
            with open(file) as fr:
                for line in fr:
                    yield line.strip()
                    
def getSentenceVec(models,allSentences): #models为加载在内存中的词向量语料
    num=0  
    for line in allSentences:
        num+=1
        newline = line.strip().split('\001\002\003')[1]
        
        xlen = len(newline)
        if num==840:
            break
    sententsVec = 0
    for j in newline:
        try:
            data = models.getVec(j)
            sententsVec += np.array(data)
        except:
            data = np.random.rand(50)
            sententsVec += np.array(data)     
    return sententsVec/xlen    


allSentences= getFile()
# 
models = Model()
print models.getVec(u'账号/n')
# newSentensVec = getSentenceVec(models,allSentences)

     
#获得句子向量
# def getInputVec(models):#models为加载在内存中的词向量语料
#     sentsVec = []
#     #filepath = "../../BurstEventTrainCorpus/test.txt"
#     filepath = "20170705_311.seg"
#     f=open(filepath,"r")
#     with open(filepath) as fr:
#         for line in fr:
#             newline = line.strip().split('\001\002\003')[1]
#             xlen = len(newline)
#         sententsVec = 0
#         for j in newline:
#             try:
#                 data = models.getVec(j)
#                 sententsVec += np.array(data)
#             except:
#                 data = np.random.rand(50)
#                 sententsVec += np.array(data)
#     
#     return sententsVec/xlen

cluster="clusterResult.txt"
#根据SinglePass聚类结果，将聚类结果转换成一个个小文本
def clusterText(cluster):
    cluster_dic={}
    #fw=open('clusterSen.txt','w')
    num=0
    with open(cluster) as fr:
        for line in fr:
            num+=1
            if "cluster:" in line:
                cluster_id=line.strip().split(":")[-1]
                nextline=fr.next().strip()
                if nextline.startswith("["):
                    tmp=[]
                    for x in nextline[1:-1].split(","):
                        tmp.append(int(x))
                    cluster_dic[cluster_id]=tmp    
                else:
                    continue
            if num==10:
                break
        sortlist=sorted(cluster_dic.iteritems(),key=lambda a:a[0],reverse=False)       
        line,number,filename,linelist=getfile()
        cluster_sen={}
        for k,v in sortlist:         
#             sentence=[]
#             for j in range(len(v)):
#                 if j<len(v)-1:
#                    v[j]=linelist[j]
#                    sentence.append(v[j]+"****")
#                 if j==len(v)-1:
#                     v[j]=linelist[j]
#                     sentence.append(v[j])
            
            cluster_sen[k]=["#####".join([linelist[y] for y in [x for x in v]])]
        
        resultorder=[]
        for  key,value in cluster_sen.items():
            sen="".join(value)
            final=key+"&&&"+sen
            
            resultorder.append(final)
        
        return resultorder 
#读取文件，将聚类后的结果按照聚类号存储到list里面
def singleClusterText(sortlist):
    #clusterlist=[]  
    for cluster in sortlist:
        newlinelist=[]
        clustertext=cluster.strip().split("&&&")[0]+"cluster.txt"
        #clusterlist.append(clustertext)
        fw=open(clustertext,"w")
        newsentence=cluster.strip().split("&&&")[-1].split("#####")
        sen="\n".join(newsentence)
        num=len(newsentence)
        fw.write(sen+'\n')
        newlinelist.append(newsentence)
        fw.close()  
#     return sen,num,clustertext,newlinelist

def getfile():
    number=0
    linelist=[]
    filename="20170705_311.seg"
    with open(filename,'r') as fr:
        for line in fr:
            number+=1
            linelist.append(line.strip())
            if number==900:
                break          
        return line,number,filename,linelist
def stop_words():
    results = []
    fr = open('stopword.txt', 'r')
    for one in fr.readlines():
        results.append(one.rstrip())
    fr.close()
    return results
#存储聚类的文件名
def clusterfilename():
    filenames=glob.glob('*cluster.txt')
    return filenames
#循环读每一个聚类文本，并去除停用词
def delstopword(clusterfile): 
        dic={}
        num=0 
        with open(clusterfile) as fr:      
            for line in fr: 
                num+=1 
                data=line.strip().split("|")[20].split(' ')[1]
            #timeId=(time.mktime(time.strptime(data,'%Y-%m-%d %H:%M:%S')))
                data=timeTrans(data)
                newline = [x for x in line.strip().split('\001\002\003')[1].split(' ') if x.split('/')[0] not in stop_words()]
              
                dic[str(data)]=newline
                if num==100:
                    break
     
        return  dic
    
#去除文本中的停用词，得到时间为键值，工单内容为value的字典
# def delstopword():
#     dic={}
#     num=0
#     with open('20170705_311.seg') as fr: 
#         for line in fr: 
#             num+=1 
#             data=line.strip().split("|")[20].split(' ')[1]
#             #timeId=(time.mktime(time.strptime(data,'%Y-%m-%d %H:%M:%S')))
#              
#             data=timeTrans(data)
#             newline = [x for x in line.strip().split('\001\002\003')[1].split(' ') if x.split('/')[0] not in stop_words()]
#              
#             dic[str(data)]=newline
#             if num==3:
#                 break
#         return  dic
#将时间转换成秒数，并归一化到0和1之间
def timeTrans(data):
    h,m,s=data.split(":")
    return ((int(h) * 3600 + int(m) * 60 + int(s)))/86400.0
#获取一个词在所有时间段出现的时间序列
def wordAlltime(dic):
    dic_word_time={}
    dic_word=[]#存储每个词
    dic_tim=[]#存储时间序列
    for k in dic.keys():
        for x in  dic[k]:
            dic_word.append(x)
    dic_word=set(dic_word)
    dic_word=list(dic_word)
    for i in range(len(dic_word)):
        for k in dic.keys():
            if dic_word[i] in dic[k]:
                dic_tim.append(k)
        dic_word_time[dic_word[i]]=dic_tim
        for word in dic_word_time.keys():
            dic_word_time[word].sort()        
        dic_tim=[]
    return   dic_word_time         
#寻找每个话题中的突发词            
def findBurstword(dic_word_time):
    result=[]
    for k in dic_word_time.keys():#k表示每个词
        stime=time.time()
        templist=(k,[float(x) for x in dic_word_time[k]])#存储词和时间序列
        #print templist[1]
        if len(templist[1])<=1:
            continue       
        burst=pybursts.kleinberg(templist[1])#返回突发词列表      
        if burst[-1][0]>2.0:
            result.append([k]+[float(x) for x in burst[-1]]+[len(templist[1]),float(time.time()-stime)])    
   
    return result
#获得含有突发词的工单，传入参数为突发词，要读文件的每一行，文件句子数，文件名，及返回突发度为topk的突发词

def getOrder(time_list,line,number,filename,k):
    
    fenzi=0
    burstdic={}#存储文件名：突发度的字典
    burstlist={}#存储含有突发词的工单内容
    burstline=[]
    orderlist={}#存储文件名：含突发词的工单
    for word in time_list:
        
        if word[0] in [x for x in line.strip().split("\001\002\003")[-1].split(" ")]:
            fenzi+=1
            if line.strip() not in burstline:
                burstline.append(line.strip())        
            continue
    percent=float(fenzi)/number
    
    burstdic[filename]=percent
    burstlist[filename]=burstline
    filenameIndex = [x[0] for x in sorted(burstdic.iteritems(),key=lambda a:a[1],reverse=True)[:k]]
    for filenamekey  in filenameIndex:
#         print filenamekey,burstlist[filenamekey]
        orderlist[filenamekey]=burstlist[filenamekey]
     
    return orderlist 
def getclusterNum(clusterfile):
    fp=open(clusterfile,"r")
    num=0
    for x in fp:
        num+=1
    return num
#根据词向量语料，得出给定句子的句子向量
# cluster=SinglePass()
# sortlist=clusterText(cluster)
# singleClusterText(sortlist)
# clusterfiles=clusterfilename()
# for clusterfile in clusterfiles: 
#     num=getclusterNum(clusterfile)
#     clusterlist=[]
#     fp=open(clusterfile,"r")
#     dictionary=delstopword(clusterfile)    
#     result=wordAlltime(dictionary)
#    
#     time_list=findBurstword(result)
#     
#     resultlist=[] 
#     for line in fp: 
#         clusterlist.append(line.strip())
#         burstorder=getOrder(time_list,line,num,clusterfile,1)
#         print burstorder
        
#         resultlist.append(burstorder)
#     result=clusterfile+"_order.txt"
#     fw2=open(result,"w")
#      
#     for k in resultlist:
#         for key,value in k.items():
#             order="\n".join(value) 
#             fw2.write(key+" "+order+"\n")
#     fw2.close()
    
print "end"



