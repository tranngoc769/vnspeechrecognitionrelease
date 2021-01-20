#Tool phải được sử dụng chung với Model của chuẩn hóa Comma

import re
import ujson
import codecs
import random
import os
import tensorflow as tf
import numpy as np
from tensorflow.python.ops.rnn import bidirectional_dynamic_rnn, dynamic_rnn
from tensorflow.contrib.crf import crf_log_likelihood, viterbi_decode
from preprocessing import word_convert
from BiModel import  batchnize_dataset, BiLSTM_Attention_model, process_batch_data
#from train_BiLSTM_Attention_model import config

model = None
# embedding path
Word2vec_path = "/work/Punctuation/"
char_lowercase = True
# dataset for train, validate and test
vocab = "/work/Punctuation/Vietnamese_newspapers/dataset/vocab.json"
word_embedding = "/work/Punctuation/Vietnamese_newspapers/dataset/word_emb.npz"


# network parameters
num_units = 300
emb_dim = 300
char_emb_dim = 52
filter_sizes = [25, 25]
channel_sizes = [5, 5]
# training parameters
lr = 0.001
lr_decay = 0.05
minimal_lr = 1e-5
keep_prob = 0.5
batch_size = 32
max_to_keep = 1
no_imprv_tolerance = 20
checkpoint_path = "/work/Punctuation/Vietnamese_newspapers/checkpoint_BiLSTM_Att/"
summary_path = "/work/Punctuation/Vietnamese_newspapers/checkpoint_BiLSTM_Att/summary/"
model_name = "punctuation_model"
config = {
          
          "Word2vec_path":Word2vec_path,\
          "char_lowercase": char_lowercase,\
          "vocab": vocab,\
          "word_embedding": word_embedding,\
          "num_units": num_units,\
          "emb_dim": emb_dim,\
          "char_emb_dim": char_emb_dim,\
          "filter_sizes": filter_sizes,\
          "channel_sizes": channel_sizes,\
          "lr": lr,\
          "lr_decay": lr_decay,\
          "minimal_lr": minimal_lr,\
          "keep_prob": keep_prob,\
          "max_to_keep": max_to_keep,\
          "no_imprv_tolerance": no_imprv_tolerance,\
          "checkpoint_path": checkpoint_path,\
          "summary_path": summary_path,\
          "model_name": model_name}
def load_TextFromFile(filename, keep_number=False, lowercase=True, max_len_seq = 100):
    dataset = []
    with codecs.open(filename, mode="r", encoding="utf-8") as f:
        line=f.readlines()[0]
        line = word_convert(line, keep_number=keep_number, lowercase=lowercase)#convert chữ thường, 
        words=line.split()
    dataset.append({"words": words})
    return dataset
def load_TextFromString(filename, keep_number=False, lowercase=True, max_len_seq = 100):
    dataset = []
    line = word_convert(filename, keep_number=keep_number, lowercase=lowercase)#convert chữ thường, 
    words=line.split()
    dataset.append({"words": words})
    return dataset
def load_data(filename):
    with codecs.open(filename, mode='r', encoding='utf-8') as f:
        dataset = ujson.load(f)
    return dataset

def build_dataset(data, word_dict, char_dict):
    dataset = []
    for record in data:
        chars_list = []
        words = []
        for word in record["words"]:
            chars = [char_dict[char] if char in char_dict else char_dict['<UNK>'] for char in word]
            chars_list.append(chars)#lấy mã ascii trong char_dict
            word = word_convert(word, keep_number=False, lowercase=True)
            words.append(word_dict[word] if word in word_dict else word_dict['<UNK>'])

        dataset.append({"words": words, "chars": chars_list})
    return dataset

def process_data(filename,dict_data,word_dict,char_dict):
    transcribe_data = load_TextFromString(filename)
    transcribe_set = build_dataset(transcribe_data, word_dict, char_dict)#gồm chars, lables, words. chars, là mã ascii của từng từ, vd chars=[[4,5,12,5], [6,9,10,11]]
    return transcribe_set#giống đọc từ file train.json
def dataset_batch_iter(dataset, batch_size):
    batch_words, batch_chars= [], []
    i = 0
    for record in dataset:
        batch_words.append(record["words"])
        batch_chars.append(record["chars"])
        if len(record["chars"]) == 0:
            print(i)
        i += 1
        if len(batch_words) == batch_size:
            yield process_batch_data(batch_words, batch_chars)
            batch_words, batch_chars, batch_labels = [], [], []
    if len(batch_words) > 0:
        yield  process_batch_data(batch_words, batch_chars)
def batchnize_dataset(data, batch_size=None, shuffle=True):
    if type(data) == str:
        dataset = load_data(data)
    else:
        dataset = data
    if shuffle:
        random.shuffle(dataset)
    batches = []
    if batch_size is None:
        for batch in dataset_batch_iter(dataset, len(dataset)):
            batches.append(batch)
#        return batches[0]
    else:
        for batch in dataset_batch_iter(dataset, batch_size):
            batches.append(batch)
        return batches
def transcribe_model(transcribe_set, model):
    tf.reset_default_graph()
    print("Load models...")
    # model = BiLSTM_Attention_model(config)
    # model.restore_last_session(config["checkpoint_path"])
    for data in transcribe_set:
        logits = model._predict_op(data)
    return logits#mảng đánh dấu dấu câu
def punctuation(i):
    switcher={1:'.',2:',',3:'!', 4:':',5:'?',6:';'}
    return switcher.get(i)

def convertToStringReference(filename,logits):
    res=""
    word_dict=load_TextFromString(filename)[0]["words"]
    for i in range(0,len(logits[0])):
        pun=logits[0][i]
        if(pun!=0):
            word=word_dict[i]+punctuation(pun)
        else:
            word=word_dict[i]
        res=res+word+" "
    return res.strip()

import time
def Capitalize(text):
    punc_filter = re.compile('([.!?]\s*)')
    split_with_punctuation = punc_filter.split(text)
    final = ''.join([i.capitalize() for i in split_with_punctuation])
    return final
# return loaded_model,dict_data,  word_dict, char_dict
def loadModel():
    tim1 = time.time()
    model = BiLSTM_Attention_model(config)
    model.restore_last_session(config["checkpoint_path"])
    tim2 = time.time()
    dict_data = load_data(config["vocab"])
    word_dict, char_dict = dict_data["word_dict"], dict_data["char_dict"]
    print("Loading model cost : "+ str(tim2 - tim1))
    tim1 = time.time()
    return model,dict_data,  word_dict, char_dict
chars=[',','.','?','!']
def strip(string):
    string = string.strip()
    if (string[len(string)-1]) in chars:
        return string()
    return string+"."
def runTranscribe(loaded_model,dict_data,  word_dict, char_dict):
    tim1 = time.time()
    filename="""ra mắt website thương mại điện tử riêng cho ngành audio hơn 1 000 mặt hàng từ loa tai nghe micro âm thanh ô tô của các thương hiệu như jbl harman/kardon akg được phân phối thông qua trang thương mại điện tử riêng với quy trình xử lý khoa học phúc giang pgi là nhà phân phối các thương hiệu âm thanh chính hãng tại việt nam như: jbl harman/kardon akg soundcraft polk audio wharfedale pro teac luxman website thương mại điện tử mới được tối ưu theo xu hướng mua sắm trực tuyến của khách hàng cho phép mua sắm hơn 1 000 mặt hàng từ loa tai nghe micro đến thiết bị hifi/hiend âm thanh ô tô tất cả các đơn hàng đều đi kèm quy trình xử lý khoa học từ kho vận giao hàng bảo hành hậu mãi trong bối cảnh mua sắm trực tuyến ngày càng được ưa chuộng bản thân ngành audio hiện tại cũng đã tiếp cận các phương thức kinh doanh trực tuyến từ lập website bán hàng riêng đến tham gia các gian hàng online trên các sàn thương mại điện tử ông nguyễn mạnh tuấn đại diện pgi chia sẻ tuy nhiên trải nghiệm mua sắm trực tuyến dành riêng cho ngành audio vẫn chỉ ở mức sơ khai vì vậy chúng tôi đã ra mắt website với mong muốn nâng cấp điều này sự ra đời của một trang thương mại điện tử chuyên về audio cũng giúp hạn chế được tình trạng hàng giả hàng nhái - một trong những vấn nạn lớn của ngành sản phẩm đặc thù này nhờ việc số hóa thông tin nên dữ liệu đăng ký kích hoạt hay tra cứu bảo hành có thể làm online thay cho giấy tờ truyền thống chỉ có một cú click chuột là người dùng đã có thể tra cứu được thông tin thuận tiện cho cả khách hàng có nhu cầu mua đi bán lại tương tự các sàn thương mại điện tử khác trang online chuyên cho audio cũng tận dụng được lợi thế về công nghệ khi cho phép lọc theo khoảng giá phân khúc… từ đó thu hẹp thông tin cần thiết các hình thức mua sắm thông qua thẻ tín dụng ví điện tử hay trả góp cũng dễ dàng hơn so với hình thức mua sắm truyền thống đương nhiên mua sắm online không thể đem đến 100% trải nghiệm cho khách hàng mà vẫn cần đến trải nghiệm offline website lúc này đóng vai trò sắp xếp lịch hẹn đặt trước hay nhận tư vấn từ các chuyên gia trong những thời điểm cần hạn chế tập trung đông người thì hình thức đặt hẹn này sẽ phát huy hơn lợi thế của công nghệ đem lại gia an
    """.strip()
    transcribe_set_process=process_data(filename, dict_data, word_dict, char_dict)
    transcribe_set = batchnize_dataset(transcribe_set_process, batch_size=2000, shuffle=False)
    logits=transcribe_model(transcribe_set, loaded_model)
    result=convertToStringReference(filename,logits)
    tim2 = time.time()
    print("\033[94m",Capitalize(strip(result)),"\033[0m")
    print("Transcribe cost : "+ str(tim2 - tim1))
# loaded_model,dict_data,  word_dict, char_dict = loadModel()
# runTranscribe(loaded_model,dict_data,  word_dict, char_dict)
