from django.shortcuts import render
from .models import Chatbot 

import pandas as pd
import pyttsx3
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier,_tree
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
import csv
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


training = pd.read_csv('Training.csv')
testing= pd.read_csv('Testing.csv')
cols= training.columns
cols= cols[:-1]
x = training[cols]
y = training['prognosis']
y1= y

reduced_data = training.groupby(training['prognosis']).max()

#mapping strings values to numbers
le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
testx    = testing[cols]
testy    = testing['prognosis']  
testy    = le.transform(testy)


clf1  = DecisionTreeClassifier()
clf = clf1.fit(x_train,y_train)


scores = cross_val_score(clf, x_test, y_test, cv=3)

#print (scores.mean())

model=SVC()  # Support Vector Classifier
model.fit(x_train,y_train)
#print("for : Support Vector Classifier")
#print(model.score(x_test,y_test))

importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]
features = cols



severityDictionary=dict()
description_list = dict()
precautionDictionary=dict()
symptoms_dict = {}

for index, symptom in enumerate(x):
       symptoms_dict[symptom] = index

chatbot = Chatbot()

# Create your views here.

def chatbot(request):
    
    def readn(nstr):  # for accepting voice 
        engine = pyttsx3.init()
        engine.setProperty('voice', "english+f5")
        engine.setProperty('rate', 130)
        engine.say(nstr)
        engine.runAndWait()
        engine.stop()

    def calc_condition(exp,days):
        sum=0
        for item in exp:
         sum=sum+severityDictionary[item]
        if((sum*days)/(len(exp)+1)>13):
            print("\n\tYou should take the consultation from doctor\n")
        else:
            print("\tIt might not be that bad but you should take precautions.")
    
    def getDescription():
        global description_list
        with open('../FayyaanFaaya/symptom_Description.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                _description={row[0]:row[1]}
                description_list.update(_description)


    def getSeverityDict():
        global severityDictionary
        with open('../FayyaanFaaya/symptom_severity.csv') as csv_file:

            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            try:
                for row in csv_reader:
                    _diction={row[0]:int(row[1])}
                    severityDictionary.update(_diction)
            except:
                pass

    def getprecautionDict():
        global precautionDictionary
        with open('../FayyaanFaaya/symptom_precaution.csv') as csv_file:

            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                _prec={row[0]:[row[1],row[2],row[3],row[4]]}
                precautionDictionary.update(_prec)
    
    
    #def getInfo():
        # name=input("Name:")
       # print("Are you ready? Yes or no \n\t\t",end="->")
       # option=input("")
       # if option == "yes" or option == "Yes":
           # return True
       # elif option == "No" or option == "no":
            #exit()
    
    def check_pattern(dis_list,inp):
        import re
        pred_list=[]
        ptr=0
        patt = "^" + inp + "$"
        regexp = re.compile(inp)
        for item in dis_list:
            if regexp.search(item):
                pred_list.append(item)
        if(len(pred_list)>0):
            return 1,pred_list
        else:
            return ptr,item
        
    def sec_predict(symptoms_exp):
        df = pd.read_csv('../FayyaanFaaya/Training.csv')
        X = df.iloc[:, :-1]
        y = df['prognosis']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)
        rf_clf = DecisionTreeClassifier()
        rf_clf.fit(X_train, y_train)

        symptoms_dict = {}

        for index, symptom in enumerate(X):
            symptoms_dict[symptom] = index

        input_vector = np.zeros(len(symptoms_dict))
        for item in symptoms_exp:
            input_vector[[symptoms_dict[item]]] = 1

        return rf_clf.predict([input_vector])


    def print_disease(node):  
        node = node[0]
        #print(len(node))
        val  = node.nonzero() 
        # print(val)
        disease = le.inverse_transform(val[0])
        return disease


    def tree_to_code(tree, feature_names):

        tree_ = tree.tree_
        # print(tree_)
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]

        chk_dis=",".join(feature_names).split(",")
        symptoms_present = []


        # conf_inp=int()
        while True:
            
            print("\n\tHello there I'm Fayyaan Faaya AI Made Chatbot.")
            print("\tTell me your symptom, I will assist you.")
            print("\n\tEnter here : ", end="")
            
            disease_input = input("")

            chatbot = Chatbot()
            chatbot.id = 0
            
            chatbot.disease = "\tEnter the symptom you are experiencing :\t"

            conf,cnf_dis=check_pattern(chk_dis,disease_input)
            if conf==1:
                print("\tsearches related to input : \n")
                for num,it in enumerate(cnf_dis):
                    print("\t",num+1,")",it)
                if num!=0:
                    print("\tI will help if you don't the name of symptom you are experiencing\n")
                    print("\tPlease read symptom name carefully and select only number")
                    print("\tSelect the one you meant (1 - "+ str(num+1) + ") : ", end="")
                    conf_inp = int(input(""))
                else:
                    conf_inp=0

                disease_input=cnf_dis[conf_inp]
                break
            print("\t Did you mean: ",cnf_dis,"?(yes/no) :",end="")
            conf_inp = input("")
            if(conf_inp=="yes"):
                break
            else:
                print("\tPlease enter valid symptom.")

        while True:
            try:
                num_days=int(input("\tOkay! For how many days ? : "))
                break
            except:
                print("\tEnter number of days.")

        def recurse(node, depth):
            indent = "  " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]

                if name == disease_input:
                    val = 1
                else:
                    val = 0
                if  val <= threshold:
                    recurse(tree_.children_left[node], depth + 1)
                else:
                    symptoms_present.append(name)
                    recurse(tree_.children_right[node], depth + 1)
            else:
                present_disease = print_disease(tree_.value[node])
                red_cols = reduced_data.columns 
                symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero()]

                print("\tAre you experiencing any of these ?" + "(yes/no) \n")
                symptoms_exp=[]
                for syms in list(symptoms_given):
                    inp=""
                    print("\n")
                    print("\t",syms,"? : ",end='')
                    while True:
                        inp=input("")
                        if(inp=="yes" or inp == "no" or inp == "Yes" or inp == "No" or inp == "Y" or inp == "N" or inp == "y" or inp == "n" or inp == "YES" or inp == "NO"):
                            break
                        else:
                            print("\tProvide proper answers i.e. (yes/no) : ",end="")
                    if(inp=="yes" or inp == "y" or inp == "Yes" or inp == "YES"):
                        symptoms_exp.append(syms)

                second_prediction=sec_predict(symptoms_exp)
                calc_condition(symptoms_exp,num_days)
                if(present_disease[0]==second_prediction[0]):
                    print("\n")
                    print("\tYou may have ", present_disease[0])
                    print(description_list[present_disease[0]])

                else:
                    print("\tYou may have ", present_disease[0], "or ", second_prediction[0])
                    print("\t",description_list[present_disease[0]])
                    print("\t",description_list[second_prediction[0]])

                precution_list=precautionDictionary[present_disease[0]]

                print("\tTake following measures : ")
                for  i,j in enumerate(precution_list):
                    print("\t" , i+1,")",j)
                print("\n")
                print("\t Thank You for being here and using Fayyaan Faaya Medical Consultation.\n")
                print("")

        recurse(0, 1)


    getSeverityDict()
    getDescription()
    getprecautionDict()
    tree_to_code(clf,cols)

    return render(request, 'English/disease/chatbot.html',{'chatbot':chatbot})
