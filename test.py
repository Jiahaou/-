import pkuseg
import numpy as np
#seg = pkuseg.pkuseg()           # 以默认配置加载模型
#text, scores = seg.cut('手机号码没有更改 手机号码更改了') # 进行分词
#pkuseg.test('test.txt', 'test_out.txt', 'test_score.txt')
#print(text)
#print(scores)
def Judgeyouxiao(pkuseg,ngram):
    youxiao=0
    flags=0
    for i in ngram:
        for pk in pkuseg:
            for y in pk:
                if i ==y:
                    youxiao+=1
                    flags=1
                    break
            if flags==1:
                flags=0
                break
    return youxiao/len(ngram)


def create_uni_bi_tri(values):
    left_once = list(values)
    left_twice = list(values)
    for i in range(1):
        left_once.insert(len(left_once), left_once[0])
        left_once.remove(left_once[0])
    for i in range(2):
        left_twice.insert(len(left_twice), left_twice[0])
        left_twice.remove(left_twice[0])
    bigram = []
    trigram = []
    for i in range(0, len(values)):
        bigram.append(values[i] + left_once[i])
        trigram.append(values[i] + left_once[i] + left_twice[i])
    output = values + bigram + trigram
    return output




def main():
    text=open('train.txt','r',encoding='UTF-8').readlines()
    seg = pkuseg.pkuseg()
    youxiaoci=[]
    zhuyili=[]
    k=0
    a = np.load('attention_x.npy')
    for i in text:
        i=i.split('\t')
        text_a=i[0]
        text_b=i[1]
        pkusegx=seg.cut(text_a)
        pkusegy=seg.cut(text_b)
        ngram_a=create_uni_bi_tri(list(text_a))
        ngram_b=create_uni_bi_tri(list(text_b))
        a_youxiao=Judgeyouxiao(pkusegx,ngram_a)
        b_youxiao=Judgeyouxiao(pkusegy,ngram_b)
        youxiaolv=a_youxiao*b_youxiao
        youxiaoci.append(youxiaolv)
        #sum是总的高注意力的词，有效是这些词里面的有效词
        sum = 0
        youxiao=0
        length_a=len(text_a)
        length_b=len(text_b)
        b = a[k]
        for i in enumerate(384):
            for j in enumerate(384):
                if b[i][j] >= 0.02:
                    if j==length_a+1 or j==length_a+length_b+2 or j== length_a+128 or j== length_a+128+1 or j== length_a+length_b+128+1 or j==length_a+length_a+2 or j==256+length_a-1 or j==256+length_a or j==256+length_a+1 or j==256+length_a+length_b or j==256+length_a+length_b+1 or j==256+length_a+length_b+2:
                        break
#a长度加一，a+b的长度+2，128+a长度，128+a长度+1，128+ab长度+1,128+ab长度+2，256+a长度-1，256+a长度，256+a长度+1，
#256+ab长度，256+ab长度+1，256+ab长度+2
                    sum += 1
                    for z in pkusegx:
                        if ngram_a[i] in z:
                            for zz in pkusegy:
                                if ngram_b[j] in zz:
                                    youxiao+=1
        zhuyili.append(youxiao/sum)
                    # 大于0.02就是高注意力，需要1.记录有多少个高注意力2.两个text_a[i],text_b[j]是否在正确分词中
        k+=1
    s=open('test_youxiaoout.txt','w',encoding='UTF-8')
    '''把两句话分词，然后做ngram处理，判断有多少个gram是符合分词中的词，即有效词几率'''
    for i in youxiaoci:
        s.write(str(i)+'\n')
    s.close()



main()

