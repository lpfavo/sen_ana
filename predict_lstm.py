from keras.models import load_model
import re
from bs4 import BeautifulSoup
from keras.preprocessing.sequence import pad_sequences
from gensim.models import Word2Vec
import keras


def load_stopwords(filepath):
    stopwords_final = []
    #2 ollect words from files. Each word is on one line
    file = open(filepath,"r",encoding="utf-8") #"stopwords-master/baidu.txt"
    for line in file:
        line = line.strip()
        stopwords_final.append(line)
    file.close()
    return stopwords_final


def clean_review(raw_review,stop_words):
    # 1. 评论是爬虫抓取的，存在一些 html 标签，需要去掉
    review_text = BeautifulSoup(raw_review, 'html.parser').get_text()
    # 2. 标点符号只保留 “-” 和 上单引号
    rex = re.compile(r'[!"#$%&\()*+,./:;<=>?@\\^_{|}~]+')
    review_text = rex.sub(' ', review_text)
    # 3. 全部变成小写
    review_text = review_text.lower()
    # 4. 分词
    word_list = review_text.split()
    # 5. 词性还原
#     tokens = list(map(lemmatizer.lemmatize, word_list))
#     lemmatized_tokens = list(map(lambda x: lemmatizer.lemmatize(x, "v"), tokens))
    # 6. 去停用词
    meaningful_words = [x for x in word_list if x not in stop_words] #list(filter(lambda x: not x in stop_words))#, lemmatized_tokens
    return meaningful_words


def get_predict_index(sentence,word_index):
    sequence = []
    for word in sentence:
        try:
            sequence.append(word_index[word])
        except KeyError:
            continue
    return sequence


def predict(text):
    keras.backend.clear_session()
    word2_vecpath='./word2vec_100dim_sg1_hs1.model'
    model_path='./imdb_train_test_model_BILSTM2.h5'
    predict_model = load_model(model_path)
    stopwords = load_stopwords("stop_all.txt")
    sentence = clean_review(text,stopwords)
    w2v = Word2Vec.load(word2_vecpath)
    # 取得所有单词
    vocab_list = list(w2v.wv.vocab.keys())
    # 每个词语对应的索引
    word_index = {word: index for index, word in enumerate(vocab_list)}
    seq_sentence = get_predict_index(sentence,word_index)
    maxlen = 100
    X_pad = pad_sequences([seq_sentence], maxlen=maxlen)
    # y_pred = predict_model.predict_classes(X_pad)
    t_prob = predict_model.predict_proba(X_pad)
    pos = 100*(t_prob[0][0])
    neg = 100*(1 - t_prob[0][0])
    #print(y_pred,t_prob)
    return [pos, neg]

# text="""The prospect of living his last days in one of those institutions that cater to the old, the sick and the infirm, Carl Fredricksen opts for an escape. His beloved house serves as the vehicle where he will reach the Paradise Falls in South America. Unknown to him, Russell, the boy scout wanting to get another badge for assisting the elderly, comes along for a trip to the unknown. Little did he know the dangers he and Russell will have to face while at their destination, battling the egotistical explorer that once was his idol. Because of his determination, and with the help of Russell, he ends up being the real hero of the story, having escaped the indignities of the stay in the nursing home.
# "Up" is an excellent film that will give pleasure to all kinds of audiences as it wants to appeal to the child quality hidden, perhaps, in all of us."""
# print(predict(text))