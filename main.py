import tkinter
import json
import random
import time
import tkinter.messagebox
import os
s=3
with open("result.txt",'r',encoding="utf-8") as f:
    dict = json.load(f)
with open("flag.txt",'r',encoding="utf-8") as f1:
    flag_dict = json.load(f1)
with open("wait.txt",'r',encoding="utf-8") as f2:
    movie_dict=json.load(f2)
movie_flag=[]
List = []
y=[]
name_list = []
movie_list=[" "," "," "]
for it in flag_dict.values():
    movie_flag.append(it)
def item_distance(list1,list2):
    i = 0
    dis = 0
    for it in list1:
        dis+=(it - list2[i]) * (it - list2[i])
        i+=1
    return dis
#算两个向量相似度的函数
def random_movie_list():
    global List,y,movie_flag,name_list,movie_list,dict
    movie_list = [" "," "," "]
    movie_list[0] = random.choice(name_list)
    movie_list[1] = random.choice(name_list)
    while movie_list[1] == movie_list[0]:
        movie_list[1] = random.choice(name_list)
    movie_list[2] = random.choice(name_list)
    while movie_list[2] == movie_list[1] or movie_list[2] == movie_list[0]:
        movie_list[2] = random.choice
    for list in movie_list:
        flag_dict[list] = 0
    for it in flag_dict.values():
        movie_flag.append(it)
    return movie_list
#初始产生随机电影列表
def movie_judge(movie_list):
    global List,y,movie_flag,name_list,dict,s,root
    i = 0
    input_list=[0,0,0]
    for list in input_list:
        judge_score(root,movie_list[i]).judge()
        input_list[i]=s
        i+=1
    i = 0
    max = -1
    movie_tag = -1
    while i < 3:
        if input_list[i] > max:
            max = input_list[i]
            movie_tag = i
        i+=1
    return movie_list[movie_tag]
#让用户评分，借此探测用户爱好
def judge_watched(flag):
    global List,y,movie_flag,name_list,movie_list,dict
    i=0
    watched_flag=0
    for list in List:
        if y[i]==flag and movie_flag[i]:
            watched_flag=1
        i+=1
    return watched_flag
#检验一个簇是否都被观看
def left_watched():
    global List,y,movie_flag,name_list,movie_list,dict
    sum=0
    i=0
    num=len(List)
    while i<num:
        sum+=y[i]
        i+=1
    return sum
#计算还剩几部电影未看
def write_back():
    global List,y,movie_flag,name_list,movie_list,dict
    i = 0
    for it in dict.keys():
        dict[it] = List[i]
        i+=1
    i=0
    for it in movie_dict.keys():
        movie_dict[it]=movie_list[i]
        i+=1
    i=0
    for it in flag_dict.keys():
        flag_dict[it]=movie_flag[i]
        i+=1
    with open("result.txt",'w',encoding="utf-8") as f:
        json.dump(dict,f)
    with open("flag.txt",'w',encoding="utf-8") as f1:
        json.dump(flag_dict,f1)
    with open("wait.txt",'w',encoding="utf-8") as f2:
        json.dump(movie_dict,f2)
    #关闭程序前将改变的数据写回
def means(list):
    temp_list=[]
    i=0
    while i<len(list[0]):
        sum=0
        for it in list:
            sum+=it[i]
        temp_list.append(sum/int(len(list)))
        i+=1
    return temp_list
def kmeans():
    global List,movie_flag,name_list,movie_list,dict
    result=[]
    center=[]
    for list in List:
        result.append(-1)
    i=0
    while i!=8:
        flag=1
        while flag==1:
            choosed_list=random.choice(List)
            if choosed_list not in center:
                center.append(choosed_list)
                i+=1
                flag=0
    i=0
    for list in List:
        j=0
        min=1000
        tag=-1
        for center_point in center:
            temp=item_distance(center_point,list)
            if temp<min:
                min=temp
                tag=j
            j+=1
        result[i]=tag
        i+=1
    temp_result=[]
    while temp_result!=result:
        temp_result=result
        k=0
        while k<len(center):
            i=0
            temp_list=[]
            for list in List:
                if result[i]==k:
                    temp_list.append(list)
                i+=1
            center[k]=means(temp_list)
            k+=1
        i=0
        for list in List:
            j=0
            min=1000
            tag=-1
            for center_point in center:
                temp=item_distance(center_point,list)
                if temp<=min:
                    min=temp
                    tag=j
                j+=1
            result[i]=tag
            i+=1
    return result
def init():
    global List,y,movie_flag,name_list,movie_list,dict
    for it1,it2 in dict.items():
        name_list.append(it1)
        List.append(it2)
    #将文件中储存的字典分成两个列表
    minlist = []
    maxlist = []
    i = 0
    while i < len(List[0]):
        min = 1000
        max = 0
        for list in List:
            if list[i] < min:
                min = list[i]
            if list[i] > max:
                max = list[i]
        minlist.append(min)
        maxlist.append(max)
        i+=1
    i = 0
    while i < len(List[0]):
        for list in List:
            list[i] = (list[i] - minlist[i]) / (maxlist[i] - minlist[i])
        i+=1
    #将电影的属性映射到（0，1）区间
    if movie_dict[str(0)]==" ":
        movie_list = random_movie_list()
    else:
        i=0
        for it in movie_dict.values():
            movie_list[i]=it
            i+=1
def do():
    global List,y,movie_flag,name_list,movie_list,dict,root
    y=kmeans()
    if left_watched()<3:
        tkinter.messagebox.showinfo("提示","所有优质电影推荐完毕\n若想重置软件请用文件下的三个txt文档替换dist下的三个对应文档")
        #exit(1)
        os._exit(1)
    #用K-means去聚类，并将结果保存在y当中
    i = 0
    love_one = movie_judge(movie_list)
    for it in name_list:
        if it == love_one:
            break
        i+=1
    flag = y[i]
    #找到用户较喜欢的那部及其所在的簇
    if judge_watched(flag)!=1:
        y_other = random.choice(range(0,8))
        while y_other==flag or judge_watched(y_other)!=1:
            y_other=random.choice(range(0,8))
        flag=y_other
    #如果这个簇电影看完了，切换到另一个簇
    j = 0
    dis = 1000
    min_item = -1
    for one in List:
        if y[j] == flag and (i != j) and movie_flag[j]:
            temp = item_distance(one,List[i])
            if temp < dis:
                min_item = j
                dis = temp
        j+=1
    movie_list[0] = name_list[min_item]
    movie_flag[min_item] = 0
    #找出同一类电影中与用户偏向电影最接近的
    if judge_watched(flag)!=1:
        y_other = random.choice(range(0,8))
        while y_other==flag or judge_watched(y_other)!=1:
            y_other=random.choice(range(0,8))
        flag=y_other
    j = 0
    dis = 1000
    min_item = -1
    for one in List:
        if flag == y[j] and (i != j) and name_list[j] != movie_list[0] and movie_flag[j]:
            temp = item_distance(one,List[i])
            if temp < dis:
                min_item = j
                dis = temp
        j+=1
    movie_list[1] = name_list[min_item]
    movie_flag[min_item] = 0
    #找出同一类电影中与用户偏向电影第二接近的
    y_other = random.choice(range(0,8))
    while y_other == flag or judge_watched(y_other)!=1:
        y_other = random.choice(range(0,8))
    j = 0
    dis = 1000
    min_item = -1
    for one in List:
        if y[j] == y_other and movie_flag[j]:
            temp = item_distance(one,List[i])
            if temp < dis:
                min_item = j
                dis = temp
        j+=1
    movie_list[2] = name_list[min_item]
    movie_flag[min_item] = 0
    #在其他随机一个簇里找出一个与用户偏向最接近的电影，对用户爱好的偏向进行拓展试探
    min = 1
    max = -1
    flag_min = -1
    flag_max = -1
    k = 0
    for it in List[i]:
        if it >= max:
            max = it
            flag_max = k
        if it < min:
            min = it
            flag_min = k
        k+=1
    #找出用户偏爱电影的属性中最突出与最低的属性
    for list in List:
        list[flag_min] = 0.95 * list[flag_min]
        list[flag_max] = 1.1 * list[flag_max]
        if(list[flag_max] > 1):
            list[flag_max] = 1
    #根据最突出属性对该属性所占权值加强，对用户较不在意的属性权值减小
    #（注意属性值低的不代表用户不在意，也有可能是瑕不掩瑜，所以权值不可减少过多）
def close():
    if(tkinter.messagebox.askquestion("告知","未完成完整评论流程退出程序将不会存档，是否退出")=="yes"):
        os._exit(1)

class Recommandation():
    def __init__(self,root):
        self.root=root
        self.frame1=tkinter.Frame(root)
        self.frame2=tkinter.LabelFrame(root,text="这是根据您喜好生成的推荐",padx=5,pady=5)
        self.frame3=tkinter.LabelFrame(root,text="是否全部看过",padx=10,pady=10)
        self.choose_label=tkinter.Label(self.frame3,text="若全看过可直接进行评分\n没有则请选否(此时系统自动进行保存和退出)\n观看完毕再下次启动后进行评分")
        self.frame1.pack(side=tkinter.BOTTOM,padx=10,pady=10)
        self.recommandation=tkinter.Button(self.frame1,text="评价并获取推荐",fg="blue",command=self.recommandate)
        self.recommandation.pack(padx=10,pady=10)
        self.okbutton=tkinter.Button(self.frame2,text="知道了",fg="blue",command=self.ask)
        self.label_list=[tkinter.Label(self.frame2),tkinter.Label(self.frame2),tkinter.Label(self.frame2)]
        self.yes_button=tkinter.Button(self.frame3,text="是",padx=2,pady=5,command=self.yes)
        self.no_button=tkinter.Button(self.frame3,text="否",padx=2,pady=5,command=self.no)
        self.recommandation.mainloop()
    def yes(self):
        self.frame3.forget()
        self.frame3.quit()
        self.frame1.pack(side=tkinter.BOTTOM)
        self.recommandation.pack()
        self.recommandation.mainloop()
    def no(self):
        write_back()
        os._exit(1)
    def recommandate(self):
        global movie_list
        self.frame1.forget()
        self.frame1.quit()
        do()
        self.frame2.pack()
        i=0
        for list in movie_list:
            self.label_list[i].config(text=list,pady=5,height=3)
            self.label_list[i].pack()
            i+=1
        self.okbutton.pack(side=tkinter.BOTTOM,pady=10)
        self.frame2.mainloop()
    def ask(self):
        self.frame2.forget()
        self.frame2.quit()
        self.frame3.pack()
        self.choose_label.pack(padx=10,pady=20)
        self.yes_button.pack(side=tkinter.LEFT)
        self.no_button.pack(side=tkinter.RIGHT)
    def hide(self):
        self.frame1.quit()
class Exitbutton():
    global root
    def __init__(self,root):
        frame=tkinter.Frame(root)
        frame.pack(side=tkinter.BOTTOM,padx=10,pady=10)
        exitbutton=tkinter.Button(frame,text="退出程序",fg="red",command=self.exit_recommandation)
        exitbutton.pack(padx=10,pady=10)
    def exit_recommandation(self):
        if(tkinter.messagebox.askquestion("告知","未完成完整评论流程退出程序将不会存档，是否退出")=="yes"):
            os._exit(1)
class judge_score():
    def __init__(self,root,name):
        self.root=root
        self.lb=tkinter.Label(root)
        self.master=tkinter.LabelFrame(root,text=name,padx=5,pady=5)
        self.v=tkinter.IntVar()
        self.v.set(6)
        self.new_button=tkinter.Button(root)
        self.reminder_label=tkinter.Label(root,text="为保证合理推荐请在看过后电影做出客观评价\n若没看过可先退出在观看后再评论\n若跳过表示不准备观看该电影")
    def get_back(self):
        global s
        s=self.v.get()
        self.master.forget()
        self.new_button.forget()
        self.lb.forget()
        self.reminder_label.forget()
        self.root.quit()
    def selection_print(self):
        if self.v.get()!=0:
            self.lb.config(text="确定给出"+str(self.v.get())+"分？",pady=3)
        else:
            self.lb.config(text="确定跳过?",pady=3)
        self.lb.pack()
        self.new_button.config(text="确认",command=self.get_back,pady=3)
        self.new_button.pack()
    def judge(self):
        self.master.pack()
        scores=[
            ("1分",1),
            ("2分",2),
            ("3分",3),
            ("4分",4),
            ("5分",5),
            ("跳过",0)
            ]
        for score,num in scores:
            button=tkinter.Radiobutton(self.master,text=score,variable=self.v,value=num,command=self.selection_print)
            button.pack(padx=40,pady=2)
        self.reminder_label.pack()
        self.root.mainloop()
if __name__=="__main__":
    init()
    root=tkinter.Tk()
    root.geometry('400x400')
    root.minsize(400, 400)
    root.title("影视推荐系统")
    root.protocol('WM_DELETE_WINDOW',close)
    myexl=Exitbutton(root)
    myre=Recommandation(root)