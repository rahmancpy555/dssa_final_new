import os
import sys
from math import log
import numpy as np

import time

from pip._vendor.requests import Session
from sklearn.naive_bayes import MultinomialNB
# import numpy as np
from flask import *
from werkzeug.utils import secure_filename
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
app = Flask(__name__)
app.secret_key = 'qwertyu'
import string
import MySQLdb
import joblib
import PyPDF2
import docx

import glob


# p=PorterStemmer()
# print(p.stem("played"))
con = MySQLdb.connect(host='localhost', charset="utf8", user='root', password='', port=3306, db='document_similarity')
cmd = con.cursor()


@app.route('/')
def main():
    return render_template('indexhome.html')


@app.route('/vl')
def vl():
    return render_template('login.html')


@app.route('/userhome')
def userhome():
    if 'user_name' in session:
        return render_template('upload.html')
    else:
        return ''' <script> alert('You are not logged in to the website'); window.location='/'</script>'''
   


@app.route('/searchdocument')
def searchdocument():
    return render_template('Upload.html')


@app.route('/home')
def home():
    if 'uname' in session:
        return render_template('adminhome.html')
    else:
        return ''' <script> alert('You are not logged in to the website'); window.location='/'</script>'''




@app.route('/registration')
def registration():
    return render_template('userregistration.html')


@app.route('/adminaproval')
def adminapproval():
    if 'uname' in session:
        return render_template('approval.html')
    else:
        return ''' <script> alert('You are not logged in to the website'); window.location='/'</script>'''


@app.route('/trendingarea')
def trendingarea():
    if 'uname' in session:
        cmd.execute("SELECT * FROM domain where domains !='uploaddocs'")
        s = cmd.fetchall()
        return render_template('AddDomain.html', data=s)
    else:
        return ''' <script> alert('You are not logged in to the website'); window.location='/'</script>'''



@app.route('/adddataset')
def adddataset():
    if 'uname' in session:
        cmd.execute("SELECT * FROM domain where domains !='uploaddocs'")
        s2 = cmd.fetchall()
        cmd.execute(
                    "SELECT `domain`.*,`addfiles`.`file`,`addfiles`.`id` FROM `addfiles` JOIN `domain` ON `addfiles`.`did`=`domain`.`id`")
        s3 = cmd.fetchall()
        return render_template("AddDataset.html", val2=s2, val=s3)
    else:
        return ''' <script> alert('You are not logged in to the website'); window.location='/'</script>'''
    


@app.route('/deletefile')
def deletefile():
    id = request.args.get('id')
    print(id)
    cmd.execute("delete from addfiles where id='" + str(id) + "'")
    con.commit()
    return ''' <script> alert('Deleted successfully'); window.location='/adddataset'</script>'''


@app.route('/login', methods=['post'])
def login():
    uname = request.form['textfield']
    password = request.form['textfield2']
    print(uname)
    print(password)
    cmd.execute("select * from login where username='" + uname + "'and password='" + password + "'")
    s = cmd.fetchone()
    if s is not None:
        if s[3] == 'admin':
            session['uname'] = 'user'
            return ''' <script>  alert('login successfull'); window.location='/home'</script>'''
        if s[3] == 'user':
            session['user_name'] = 'user'
            return ''' <script>  alert('login success'); window.location='/userhome'</script>'''
        else:
            return ''' <script>  alert('login success but not approved'); window.location='/'</script>'''

    else:
        return ''' <script> alert('Invalid Username or Password'); window.location='/'</script>'''






@app.route('/logout')
def logout():
    session.pop('uname', None)
    session.pop('user_name', None)
    return ''' <script> alert('log out successfully'); window.location='/'</script>'''







@app.route('/trendingarea1', methods=['post'])
def trendingarea1():
    trendingarea = request.form['textfield']
    cmd.execute("insert into domain values ( null,'" + trendingarea + "')")
    con.commit()
    os.mkdir("static/New dataset/" + trendingarea)
    return ''' <script> alert('registered successfully'); window.location='/trendingarea'</script>'''


@app.route('/delete')
def delete():
    id = request.args.get('id')
    cmd.execute("delete from domain where id='" + id + "'")
    con.commit()
    return ''' <script> alert('Deleted successfully'); window.location='/trendingarea'</script>'''


@app.route('/addkeyword')
def addkeyword():
    id = request.args.get('id')
    session['did'] = id
    cmd.execute("SELECT * FROM addkeyword where did='" + id + "'")
    s = cmd.fetchall()
    return render_template('AddKeyword.html', val=s)
    # classification()

@app.route('/insertkeyword', methods=['post'])
def insertkeyword():
    keyword = request.form['textfield']
    cmd.execute("insert into addkeyword values(null,'" + str(session['did']) + "','" + keyword + "')")
    con.commit()
    cmd.execute("SELECT * FROM addkeyword where did='" + str(session['did']) + "'")
    s = cmd.fetchall()
    return render_template('AddKeyword.html', val=s)


@app.route('/deletekeyword')
def deletekeyword():
    id = request.args.get('id')
    cmd.execute("delete from addkeyword where id='" + id + "'")
    con.commit()
    cmd.execute("SELECT * FROM addkeyword where did='" + str(session['did']) + "'")
    s = cmd.fetchall()
    return render_template('AddKeyword.html', val=s)


# @app.route('/select')
# def select():
#     cmd.execute("select * from addfiles")
#     s=cmd.fetchall()
#     cmd.execute("select * from domain")
#     s2 = cmd.fetchall()
#     return render_template("AddDataset.html",val=s,val2=s2)

@app.route('/upload', methods=['post', 'get'])
def upload():
    did = request.form['select']
    print(did)
    qry = "select domains from domain where id='" + str(did) + "'"
    cmd.execute(qry)
    domain = cmd.fetchall()[0][0]
    file = request.files['file']
    img = secure_filename(file.filename)
    file.save(os.path.join("./static/New dataset/" + domain, img))
    cmd.execute(" insert into addfiles values(null,'" + str(did) + "','" + img + "')")
    con.commit()
    classification()
    return ''' <script> alert('file uploaded successfully'); window.location='/adddataset'</script>'''


@app.route('/userdetails', methods=['get', 'post'])
def userdetails():
    fname = request.form['textfield']
    lname = request.form['textfield2']
    email = request.form['textfield3']
    contact = request.form['textfield7']
    uname = request.form['textfield4']
    password = request.form['textfield5']
    cmd.execute("insert into login values(null,'" + uname + "','" + password + "','pending') ")
    id = con.insert_id()
    cmd.execute("insert into registration values(null,'" + str(
        id) + "','" + fname + "','" + lname + "','" + email + "','" + contact + "')")
    con.commit()
    return ''' <script> alert('Registered successfully'); window.location='/'</script>'''


@app.route('/viewuserdetails')
def viewuserdetails():
    if 'uname' in session:
        cmd.execute(
                    "select registration.*,login.* from registration,login where login.id=registration.login_id and login.type='pending'")
        s = cmd.fetchall()
        return render_template('approval.html', val=s)
    else:
        return ''' <script> alert('You are not logged in to the website'); window.location='/'</script>'''


@app.route('/approveuser')
def approveuser():
    id = request.args.get('id')
    cmd.execute("update login set type='user'where id='" + str(id) + "'")
    con.commit()
    return ''' <script> alert('Approved'); window.location='/viewuserdetails'</script>'''


@app.route('/rejectuser')
def rejectuser():
    id = request.args.get('id')
    cmd.execute("delete from registration where login_id='" + str(id) + "'")
    cmd.execute("delete from login where id='" + str(id) + "'")
    con.commit()
    return ''' <script> alert('Rejected'); window.location='/viewuserdetails'</script>'''


@app.route('/viewapprovedusers')
def viewapprovedusers():
    if 'uname' in session:
        cmd.execute(
                    "select registration.*,login.* from registration,login where login.id=registration.login_id and login.type='user'")
        s = cmd.fetchall()
        return render_template('viewapprovedusers.html', val=s)
    else:
        return ''' <script> alert('You are not logged in to the website'); window.location='/'</script>'''
    


# path = r'C:\Users\Acer\PycharmProjects\documentsimilarity\src\static\useruploadfiles'


# @app.route('/saveuderfile', methods=['get', 'post'])
# def saveuserfile():
# file = request.files['file']
# img = secure_filename(file.filename)
# file.save(os.path.join(path, img))
# filename = os.path.join(path, img)

# import PyPDF2
# pdfFileObj = open(filename, 'rb')
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
# num_pages = pdfReader.numPages
# count = 0
# text = ""
# print(num_pages)
# while count < num_pages:
# pageObj = pdfReader.getPage(count)
# count += 1
# text += pageObj.extractText()
# print("---------------------------------------------------------")
# print(text)
# cmd.execute("SELECT * FROM domain")
# s = cmd.fetchall()
# dic = {}
# for d in s:
# dic[d[1]] = []
# cmd.execute("SELECT * FROM addkeyword where did='" + str(d[0]) + "'")
# ss = cmd.fetchall()
# for dd in ss:
# dic[d[1]].append(dd[2])

# print(dic)

# from nltk.tokenize import word_tokenize
# words = word_tokenize(text)

# fcount = 0
# res = ''

# for k in dic.keys():
# count = 0

# for w in dic[k]:
# if words.__contains__(w):
#  count += 1
# if fcount < count:
# fcount = count
# res = k
# print(k, count)

# return render_template('domainspecification.html', val=res)

stopwords = []
stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards', 'again', 'against', 'all', 'almost', 'alone',
             'along', 'already', 'also', 'although', 'always',
             'am', 'among', 'amongst', 'amoungst', 'amount', 'an', 'and', 'another', 'any', 'anyhow', 'anyone',
             'anything', 'anyway', 'anywhere', 'are', 'around',
             'as', 'at', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before',
             'beforehand', 'behind', 'being', 'below', 'beside', 'besides',
             'between', 'beyond', 'bill', 'both', 'bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant', 'co',
             'computer', 'con', 'could', 'couldnt', 'cry', 'de', 'describe',
             'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight', 'either', 'eleven', 'else',
             'elsewhere', 'empty', 'enough', 'etc', 'even', 'ever', 'every',
             'everyone', 'everything', 'everywhere', 'except', 'few', 'fifteen', 'fify', 'fill', 'find', ' fire',
             'first', 'five', 'for', 'former', 'formerly', 'forty', 'found',
             'four', 'from', 'front', 'full', 'further', 'get', 'give', 'go', 'had', 'has', 'hasnt', 'have', 'he',
             'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'hereupon',
             'hers', 'herse', 'him', 'himse', 'his', 'how', 'however', 'hundred', 'i', 'ie', 'if', 'in', 'inc',
             'indeed', 'interest', 'into', 'is', 'it', 'its', 'itse', 'keep', 'last',
             'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me', 'meanwhile', 'might', 'mill',
             'mine', 'more', 'moreover', 'most', 'mostly', 'move', 'much', 'must',
             'my', 'myse', 'name', 'namely', 'neither', 'never', 'nevertheless', 'next', 'nine', 'no', 'nobody', 'none',
             'noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of',
             'off', 'often', 'on', 'once', 'one', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours',
             'ourselves', 'out', 'over', 'own', 'part', 'per', 'perhaps',
             'please', 'put', 'rather', 're', 'same', 'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several',
             'she', 'should', 'show', 'side', 'since', 'sincere', 'CSEIT183320'.lower(), 'IJSRSET'.lower(), 'irjet',
             'journal', 'international'
             'six', 'sixty', 'so', 'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere',
             'still', ',such', 'system', 'take', 'ten', 'than', 'that', 'the',
             'their', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'therefore', 'therein',
             'thereupon', 'these', 'they', 'thick', 'thin', 'third', 'this', 'those',
             'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'top', 'toward',
             'towards', 'twelve', 'twenty', 'two', 'un', 'under', 'until', 'up', 'upon',
             'us', 'very', 'via', 'was', 'we', 'well', 'were', 'what', 'whatever', 'when', 'whence', 'whenever',
             'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever',
             'whether', 'which', 'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with',
             'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself', 'yourselves']


def read_docfile(input_file_name):

    # import docx
    wholedoc = ""
    with open(input_file_name, "rb") as input_file:
        doc = docx.Document(input_file)

        for para in doc.paragraphs:
            wholedoc += para.text
    return wholedoc


@app.route('/saveuserfile', methods=['get', 'post'])
def saveuserfile():
    file = request.files['file']
    file_name_new = secure_filename(file.filename)
    file_name = os.path.join("./static/New dataset/uploaddocs", file_name_new)
    file.save(file_name)
    ext= file_name.split('.')[-1]
    if ext !="pdf" and ext!="docx":
        return ''' <script> alert('file not supported'); window.location='/userhome'</script>'''

    # import docx
    # wholedoc=read_docfile(file_name)
    #session['curdoc'] = wholedoc


    cmd.execute("SELECT * FROM domain")

    dic = []
    for ditem in cmd.fetchall():
        print(ditem)
        dic.append(ditem[1])
    sim, dsfiles, resultclass = similarity_check(file_name)
    t = float(len([x for x in sim if x > 20]) / len(sim)) > .2
    cn=""
    if resultclass[0]==-1:
        cn="no related class found in dataset"

    elif len(sim)==0:
        cn="error in reading input file"
    else:
        cn=dic[resultclass[0]]


    if cn=='uploaddocs':
         cn="no related class found in dataset"
        



    result=[]
    x=10
    for i in range(len(dsfiles)):
        if i >= x:
            break
        if dsfiles[i] != file_name_new:
            result.append([dsfiles[i], sim[i]])
        

    





    







    return render_template('domainspecification.html', val=dsfiles, val1=sim, classname=cn,trending=t,res=result)


def remove_stopwords(curdoc):
    res = curdoc
    re = list(res)
    for word in res:

        if word in stopwords:
            re.remove(word)

    return re


symbols = []
symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ':', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~', '?', '$',
           '%', '#', '@', '!', '^', "'", '_', '\n', '\r','\t','\\','ˆ']

def symbol_removal(text):
    re=text
    for symb in symbols:
        if symb == "-":
            re = re.replace(symb, "")
        re = re.replace(symb," ")
    return re
def read_pdf(filename):
    pdfFileObj = open(filename, "rb")
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    num_pages = pdfReader.numPages
    count = 0
    text = ""
    # print(num_pages)
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count += 1
        text += pageObj.extractText().lower()
    return text


ds_documents={}
ds_path = r"static\New dataset"
def extract_words(filepath):
    if filepath.split(".")[-1] == "pdf":
        text = read_pdf(filepath)
    else:
        text = read_docfile(filepath)
    symb_rmv = symbol_removal(text).split(" ")
    text_words = remove_stopwords(symb_rmv)

    text_words = preprocess_text(text_words)
    return text_words

def read_directory(directory_path):
    files_ds = os.listdir(directory_path)
    # ds_documents[sub_dir]=files_ds
    # print(files_ds)
    # ========================
    sub_dir_list = []
    unique_words = []
    for file_name in files_ds:
        filepath = os.path.join(directory_path, file_name)
        text_words = extract_words(filepath)
        ###--------------###
        unique_words.extend([x for x in text_words if x not in unique_words])
        sub_dir_list.append(text_words)
    return (sub_dir_list, unique_words)
#
def similarity_check(input_filename):
    dir_dataset = os.listdir(ds_path)
    con = MySQLdb.connect(host='localhost', charset="utf8", user='root', passwd='', port=3306,
                          db='document_similarity')

    cur = con.cursor()
    cur.execute("select max(id) from addkeyword ")
    cnt = cur.fetchone()[0]
    print(cnt)
    id = 0
    idf_list = []
    unique_kw = []
    cur.execute("select idf,keyword from addkeyword")
    time.sleep(2)

    for ditem in cur.fetchall():
        idf_list.append(ditem[0])
        unique_kw.append(ditem[1])
    id = len(unique_kw)
    try:
      input_text = extract_words(input_filename)
    except:
        return ([],[],[])
    input_term_vector = [0 for x in range(len(unique_kw))]
    input_term_vector = [input_text.count(y) for y in unique_kw]
    print(len(input_term_vector))
    result_class=[-1]
    if sum(input_term_vector)!=0:

        it = [x / sum(input_term_vector) for x in input_term_vector]
        print("-------------")
        print(it)
        input_term_vector = it
        tfidf_input = [a * b for a, b in zip(idf_list, input_term_vector)]
        print(len(tfidf_input), len(unique_kw))
        result_class = predict(it)
        print(result_class)
    dict_ds_termvector = {}

    #
    # cmd.execute("select domains from domain")
    # s = cmd.fetchall()
    # dict_key_words = []
    # class_names = []
    # filenames_ds = []
    # i = 0
    # for dbitem in s:
    #     class_names.append(dbitem[0])
    #     subdirpath = os.path.join(ds_path, dbitem[0])
    #     sub_dir_kw = read_directory(subdirpath)[0]
    #     dict_key_words.extend(sub_dir_kw)
    #     filenames_ds.extend(os.listdir(subdirpath))
    #     i += 1
    # dict_ds_termvector=[]
    # for document in dict_key_words:
    #     termvector = [document.count(x)  for x in unique_kw]
    #     its=[x/sum(termvector) for x in termvector]
    #     termvector=its
    #
    #     dict_ds_termvector.append(termvector)
    #     tfidf_docs = []
    # for doc_termvector in dict_ds_termvector:
    #     tfidf = [a * b for a, b in zip(doc_termvector, idf_list)]
    #     tfidf_docs.append(tfidf)
    #
    #
    # sim_result=[]
    #
    # sim=[cosine_similarity(doc_tfidf,input_term_vector) for doc_tfidf in dict_ds_termvector]
    # x,y=(list(x) for x in zip(*sorted(zip(sim, filenames_ds), key=lambda pair: pair[0])))
    # ind=sim.index(max(sim))
    # print(max(sim),filenames_ds[ind])
    # x.reverse()
    # y.reverse()
    x, y = similarity_check1(input_filename)

    return (x, y, result_class)


def similarity_check1(input_filename):
    dir_dataset = os.listdir(ds_path)
    # con = MySQLdb.connect(host='localhost', charset="utf8", user='root', passwd='root', port=3308,
    #                       db='document_similarity')
    #
    # cur=con.cursor()
    # cur.execute("select max(id) from addkeyword ")
    # cnt=cur.fetchone()[0]
    # print(cnt)
    # id=0
    # idf_list = []
    # unique_kw = []
    # while id <cnt:
    #
    #     cur.execute("select idf,keyword from addkeyword where id>"+str(id))
    #     time.sleep(2)
    #
    #     for ditem in cur.fetchall():
    #         idf_list.append(ditem[0])
    #         unique_kw.append(ditem[1])
    #     id=len(unique_kw)
    #



    input_text = extract_words(input_filename)
    # input_term_vector=[0 for x in range(len(unique_kw))]
    # input_term_vector=[input_text.count(y) for y in unique_kw]
    # it=[x/sum(input_term_vector) for x in input_term_vector]
    # input_term_vector=it
    # tfidf_input = [a * b for a, b in zip(idf_list, input_term_vector)]
    # print(len(tfidf_input),len(unique_kw))
    # result_class = predict(tfidf_input)
    # print(result_class)
    # dict_ds_termvector={}


    cmd.execute("select domains from domain")
    s = cmd.fetchall()
    dict_key_words = []
    class_names = []
    filenames_ds = []



    i = 0
    for dbitem in s:
        class_names.append(dbitem[0])
        subdirpath = os.path.join(ds_path, dbitem[0])
        sub_dir_kw = read_directory(subdirpath)[0]
        dict_key_words.extend(sub_dir_kw)
        filenames_ds.extend(os.listdir(subdirpath))
        i += 1
    dict_ds_termvector = []
    sim_result = []
    for document in dict_key_words:
        totkwords = input_text + document
        unique_kw = list(set(totkwords))
        termvector = [document.count(x) for x in unique_kw]
        its = [x / sum(termvector) for x in termvector]
        termvector = its
        inputtermvector = [input_text.count(x) for x in unique_kw]
        inputvect = [x / sum(termvector) for x in inputtermvector]
        idflist = [0 for x in unique_kw]
        for x in range(len(unique_kw)):
            if unique_kw[x] in input_text:
                idflist[x] += 1
            if unique_kw[x] in document:
                idflist[x] += 1
            idflist[x] = log(1 + (2 / idflist[x]))
            inputvect[x] *= idflist[x]
            its[x] *= idflist[x]

        sim_result.append(cosine_similarity(inputvect, its))

    # dict_ds_termvector.append(termvector)
    #     tfidf_docs = []
    # for doc_termvector in dict_ds_termvector:
    #     tfidf = [a * b for a, b in zip(doc_termvector, idf_list)]
    #     tfidf_docs.append(tfidf)
    #
    #
    #
    #
    # sim=[cosine_similarity(doc_tfidf,input_term_vector) for doc_tfidf in dict_ds_termvector]
    x, y = (list(x) for x in zip(*sorted(zip(sim_result, filenames_ds), key=lambda pair: pair[0])))
    ind = sim_result.index(max(sim_result))
    print(max(sim_result), filenames_ds[ind])
    x.reverse()
    y.reverse()
    return (x, y)


def cosine_similarity(v1, v2):
    sim = 0
    nr = sum([a * b for a, b in zip(v1, v2)])
    dr1 = sum(a ** 2 for a in v1)
    dr2 = sum(b ** 2 for b in v2)
    dr = (dr1 * dr2) ** .5
    try:
     sim = nr / dr
    except:
        sim=0
    if sim > 1:
        sim = 1
    return sim * 100


def preprocess_text(re):
    st_removed_text = re
    root_words = []
    for word in st_removed_text:
        P_stemmer = PorterStemmer()
        if not word.isnumeric() and word.isalnum():
            stemmed_word = word  # P_stemmer.stem(word)

            if len(stemmed_word) > 1:
                root_words.append(stemmed_word)
    return root_words

def classification():
    cmd.execute("select domains from domain")
    s = cmd.fetchall()

    unique_words = []
    dict_key_words = []
    class_names=[]
    ytrain = []
    i=0
    for dbitem in s:
        class_names.append(dbitem[0])
        subdirpath = os.path.join(ds_path, dbitem[0])
        rwords = read_directory(subdirpath)
        sub_dir_kw = rwords[0]
        for x in rwords[1]:
            if not x in unique_words:
                unique_words.append(x)
        dict_key_words.extend(sub_dir_kw)
        ytrain.extend([i for x in range(len(os.listdir(subdirpath)))])
        i += 1
    print(class_names)
    unique_words_cnt = [0 for x in unique_words]

    idf_list = []
    litemp=[]
    for x in range(len(unique_words)):
        for tempdoc in dict_key_words:

            if unique_words[x] in tempdoc:
                unique_words_cnt[x] += tempdoc.count(unique_words[x])
    uniquewords = []
    uniquewords_cnt = []
    print(max(unique_words_cnt))
    for x in range(len(unique_words)):
        if (unique_words_cnt[x] > 80):
            uniquewords.append(unique_words[x])
            uniquewords_cnt.append(unique_words_cnt[x])
    cmd.execute("truncate table addkeyword")
    con.commit()
    for x in range(len(uniquewords)):
        try:
            idf_list.append(log(len(dict_key_words) / uniquewords_cnt[x]))
            try:

                cmd.execute("insert into addkeyword values(null,'" + str(idf_list[x]) + "','" + uniquewords[x] + "')")
                con.commit()
            except Exception as ex:
                try:
                    cmd.execute(
                        "update addkeyword set idf='" + str(idf_list[x]) + "' where keyword='" + uniquewords[x] + "'")
                    con.commit()
                except Exception as ex:
                    litemp.append(uniquewords[x])
        except Exception as ex:
            print("error",ex)
    dict_ds_termvector = []

    for x in litemp:
        ind = uniquewords.index(x)
        uniquewords.remove(x)
        idf_list.remove(idf_list[ind])

    for document in dict_key_words:
        termvector = [document.count(x) for x in uniquewords]
        its = [x / sum(termvector) for x in termvector]
        print(its)
        print(document)
        dict_ds_termvector.append(its)
    tfidf_docs = []
    for doc_termvector in dict_ds_termvector:
        tfidf = [a * b for a, b in zip(doc_termvector, idf_list)]
        tfidf_docs.append(tfidf)
        print(len(tfidf))
    print(dict_ds_termvector, ytrain)
    mnb = MultinomialNB()
    mnb.fit(dict_ds_termvector, ytrain)
    print(ytrain, class_names)
    joblib.dump(mnb, "mnb.joblib")
    tc = 0
    fc = 0
    mnb = joblib.load("mnb.joblib")

    for xd in range(len(dict_ds_termvector)):
        p = mnb.predict([dict_ds_termvector[xd]])
        if p[[0]] == ytrain[xd]:
            tc += 1
        else:
            fc += 1
    print(tc / len(ytrain))

def predict(input_tfidf):
    mnb = joblib.load("mnb.joblib")
    return mnb.predict([input_tfidf])






























if __name__ == '__main__':
    app.debug=True
    app.run()
    #  similarity_check(r"static/New dataset/Artificial Intelligence/2bciabstract.docx")
    # l=[1,0,0]
    # j=[2,1,1]
    #
    # print(cosine_similarity([l], [j]))
    # print(cosine_similarity(l,j))
    # k=[a*b for a,b in zip(l,j)]
    #print(k)
    # k=np.array(l)*np.array(j)
    # k=list(k)
    # print(k)


    # a=[1,2,3,1,2,1,1,2,3,1,1,2]
    # b=[1,2,3]
    # c=[a.count(x) for x in b]
    # print(c)
    # printz("asd1".isalnum(),"'˙˘ˇ˝˙˛˚˜˙'asdf".isalnum(),"123".isalnum())
    # symbol_removal("hello, killed! heloo}")
    # remove_stopwords("you are a good person.")
    # app.run(debug=True)


# print(remove_stopwords("you are a good person."))
# print(dir_dataset())
# print(preprocess_text("Architecture Design for Hadoop No-SQL ")
#   classification()
