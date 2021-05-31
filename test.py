import pkuseg
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

text=open('test.txt','r',encoding='UTF-8').readlines()
seg = pkuseg.pkuseg()
youxiaoci=[]
for i in text:
    i=i.split('\t')
    text_a=i[0]
    text_b=i[1]
    pkusegx=seg.cut(text_a)
    pkusegy=seg.cut(text_b)
    ngram_a=create_uni_bi_tri(list(text_a))
    ngram_b=create_uni_bi_tri(text_b.split(' '))
    a_youxiao=Judgeyouxiao(pkusegx,ngram_a)
    b_youxiao=Judgeyouxiao(pkusegx,ngram_b)
    youxiaolv=a_youxiao*b_youxiao
    youxiaoci.append(youxiaolv)
print(youxiaoci)
