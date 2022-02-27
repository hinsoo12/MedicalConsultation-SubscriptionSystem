from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from .models import News, Our_Service
from HealthForAll.models import Feedback, subscribe
from.models import Disease, News
from Accounts.models import Doctor, Patient
from django.contrib import messages
from sklearn.metrics import accuracy_score
from django.core.mail import send_mail

import pyttsx3 
import pandas as pd


#from sklearn import svm
#from sklearn import datasets
#clf = svm.SVC()
#X, y= datasets.load_iris(return_X_y=True)
#clf.fit(X, y)


#from sklearn import datasets
#model = datasets.load_breast_cancer()

#loading trained_model

#import pickle
import joblib as jb

testdataset = '../FayyaanFaaya/Training.csv'

test_data = pd.read_csv(testdataset)

#print(test_data.head())

#model = RandomForestRegressor()
#model.fit(X, y)

#jb.dump(test_data,'model_trained') # converting dataset into trained model

model = jb.load('trained_model')

#model = model.values.reshape(1,-1)

def welcome(request):
    return render(request,'English/base/welcome.html')

def index(request):

    services1 = Our_Service()
    services1.id = 0
    services1.service_name = 'Get common Information about disease'
   
    services2 = Our_Service()
    services2.id = 1
    services2.service_name = 'Check Symptom of your condition'

    services3 = Our_Service()
    services3.id = 2
    services3.service_name = 'Get Consultation for your Conditions'

    services4 = Our_Service()
    services4.id = 3
    services4.service_name = 'Get Care Service for your special condition'

    services = [services1,services2,services3,services4]

    return render(request,'English/base/index.html',{'services':services})


def contact(request):
   if request.method == 'POST':
      fullname = request.POST['cf_name']
      email = request.POST['cf_email']
      message = request.POST['cf_message']
      if len(fullname)<2 or len(email)<3 or len(message)<4:
          messages.error(request, "Please fill the form correctly")
      else:
         send_mail(
                'Fayyaan Faaya Medical Consultation',
                'Hello, Thank you for contacting Us. We will reply as soon as possible.',
                'fayyaanfaaya@gmail.com',
            [email],
            fail_silently=False,
            )
         contact=Feedback(fullname=fullname, email=email, message=message)
         contact.save()
         messages.success(request, "Your message has been successfully sent")

   return render(request,'English/base/contact.html')


def about(request):
    return render(request, 'English/base/about.html')

def subscriber(request):
    if request.method == "POST":
        subscriber = request.POST["email"]
        if subscribe.objects.filter(subscriber=subscriber).exists():
            messages.error(request,"You already subscribe to our website! Thank for being our member!")
        else:
            
            send_mail(
            'Fayyaan Faaya Medical Consultation',
            'Hello, Thank you for being our subscriber. We will notify you daily news.',
            'fayyaanfaaya4all@gmail.com',
            [subscriber],
            fail_silently=False,
            )
            
            done = subscribe(subscriber=subscriber)
            messages.info(request, "You subscribe to our website!. Thank you for being our subscriber!")
            done.save()
            
            return redirect('index')

    return render(request,'English/account/subscriber.html')

def news(request):
    news = News.objects.all()
    return render(request, 'English/base/news.html',{'news': news})

def doctor_profile(request):
    information = Doctor.objects.all()
    return render(request,'English/doctor/doctor_profile.html', {'information': information })

def notfound(request):
    return render(request, 'English/base/404.html')

def checkdisease(request):

  diseaselist=['Fungal infection','Allergy','GERD','Chronic cholestasis','Drug Reaction','Peptic ulcer diseae','AIDS','Diabetes ',
  'Gastroenteritis','Bronchial Asthma','Hypertension ','Migraine','Cervical spondylosis','Paralysis (brain hemorrhage)',
  'Jaundice','Malaria','Chicken pox','Dengue','Typhoid','hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D',
  'Hepatitis E', 'Alcoholic hepatitis','Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
  'Heart attack', 'Varicose veins','Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis',
  'Arthritis', '(vertigo) Paroymsal  Positional Vertigo','Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']

  symptomslist=['Itching','Skin rash','Nodal skin eruptions','Continuous Sneezing','shivering','Chills','Joint pain',
  'Stomach pain','Acidity','Ulcers on tongue','Muscle wasting','Vomiting','Burning micturition','Spotting urination',
  'Fatigue','Weight gain','Anxiety','Cold hands and feets','Mood swings','Weight loss','Restlessness','Lethargy',
  'Patches in throat','Irregularsugar level','Cough','High fever','Sunken eyes','Breathlessness','Sweating',
  'Dehydration','Indigestion','Headache','Yellowish skin','Dark urine','Nausea','Loss of appetite','Pain behind the eyes',
  'Back pain','Constipation','Abdominal pain','Diarrhoea','Mild fever','Yellow urine',
  'Yellowing of eyes','Acute liver failure','Fluid overload','Swelling of stomach',
  'Swelled lymph nodes','Malaise','Blurred and distorted vision','Phlegm','Throat irritation',
  'Redness of eyes','Sinus pressure','Runny nose','Congestion','Chest pain','Weakness in limbs',
  'Fast heart rate','Pain during bowel movements','Pain in anal region','Bloody stool',
  'Irritation in anus','Neck pain','Dizziness','Cramps','Bruising','Obesity','Swollen legs',
  'Swollen blood vessels','Puffy face and eyes','Enlarged thyroid','Brittle nails',
  'Swollen extremeties','Excessive hunger','Extra marital contacts','Drying and tingling lips',
  'Slurred speech','Knee pain','Hip joint pain','Muscle weakness','Stiff neck','Swelling joints',
  'Movement stiffness','Spinning movements','Loss of balance','Unsteadiness',
  'Weakness of one body side','Loss of smell','Bladder discomfort','Foul smell of urine',
  'Continuous feel of urine','Passage of gases','Internal itching','Toxic look (typhos)',
  'Depression','Irritability','Muscle pain','Altered sensorium','Red spots over body','Belly pain',
  'Abnormal menstruation','Dischromic patches','Watering from eyes','Increased appetite','Polyuria','Family history','Mucoid sputum',
  'Rusty sputum','Lack of concentration','Visual disturbances','Receiving blood transfusion',
  'Receiving unsterile  injections','Coma','Stomach bleeding','Distention of abdomen',
  'History of alcohol consumption','Fluid overload','Blood in sputum','Prominent veins on calf',
  'Palpitations','Painful walking','Pus filled pimples','Blackheads','Scurring','Skin peeling',
  'Silver like dusting','Small dents in nails','Inflammatory nails','Blister','Red sore around nose',
  'Yellow crust ooze']

  alphabaticsymptomslist = sorted(symptomslist)
  
  
  #model = np.reshape(-1, 1)

  print(model)

  #print(model.shape)

  if request.method == 'GET':
    
     return render(request,'English/disease/checkdisease.html', {"list2":alphabaticsymptomslist})


  elif request.method == 'POST':
       
      ## access you data by playing around with the request.POST object
      
      inputno = int(request.POST["noofsym"])
      print(inputno)
      if (inputno == 0 ) :
          return JsonResponse({'predicteddisease': "none",'confidencescore': 0 })
      else :
        psymptoms = []
        psymptoms = request.POST.getlist("symptoms[]")
        print("The symptom You enter is : ")
        print(psymptoms)

      
        """      #main code start from here...
        """
        testingsymptoms = []
        #append zero in all coloumn fields...
        for x in range(0, len(symptomslist)):
          testingsymptoms.append(0)


        #update 1 where symptoms gets matched...
        for k in range(0, len(symptomslist)):

          for z in psymptoms:
              if (z == symptomslist[k]):
                  testingsymptoms[k] = 1

        

        inputtest = [testingsymptoms]
        
    
        print(inputtest)
        
        predicted = model.predict([testingsymptoms])
        print("predicted disease is : ")
        print(predicted)


        y_pred_2 = model.predict_proba(inputtest)
        confidencescore=y_pred_2.max() * 100
        print(" confidence score of : = {0} ".format(confidencescore))

        confidencescore = format(confidencescore, '.0f')
        predicted_disease = predicted[0]

        if predicted_disease == "Malaria":
           description = "Malaria is n infectious disease which is caused by protozoan parasites from the Plasmodium family that can be transmitted by the bite of the Anopheles mosquito or by a contaminated needle or transfusion. Falciparum malaria is the most deadly type."
           treatment = "Consult nearest hospital , avoid oily food , avoid non vegetables food, and keep mosquitos out"
        

        elif predicted_disease == "Allergy":
           description = "An allergy is an immune system response to a foreign substance that's not typically harmful to your body.They can include certain foods, pollen, or pet dander. Your immune system's job is to keep you healthy by fighting harmful pathogens."
           treatment = "apply calamine	cover area with bandage, and use ice to compress itching."


        elif predicted_disease == "Hypothyroidism":
           description = "	Hypothyroidism, also called underactive thyroid or low thyroid, is a disorder of the endocrine system in which the thyroid gland does not produce enough thyroid hormone."
           treatment = "reduce stress, 	exercise	eat healthy, and	get proper sleep."
       

        elif predicted_disease == "Psoriasis":
            description = "Psoriasis is a common skin disorder that forms thick, red, bumpy patches covered with silvery scales. They can pop up anywhere, but most appear on the scalp, elbows, knees, and lower back. Psoriasis can't be passed from person to person. It does sometimes happen in members of the same family."
            treatment = "wash hands with warm soapy water,	stop bleeding using pressure, 	consult doctor, and	salt baths"
         

        elif predicted_disease == "GERD":
            description = "GERD is Gastroesophageal reflux disease, or GERD, is a digestive disorder that affects the lower esophageal sphincter (LES), the ring of muscle between the esophagus and stomach. Many people, including pregnant women, suffer from heartburn or acid indigestion caused by GERD."
            treatment = "avoid fatty, spicy food,	avoid lying down after eating, and	maintain healthy weight	exercise."


        elif predicted_disease == "Chronic cholestasis":
            description = "Chronic cholestatic diseases, whether occurring in infancy, childhood or adulthood, are characterized by defective bile acid transport from the liver to the intestine, which is caused by primary damage to the biliary epithelium in most cases"
            treatment = "cold baths, anti itch medicine,	consult doctor,  and	eat healthy"


        elif predicted_disease == "hepatitis A":
            description = "Hepatitis A is a highly contagious liver infection caused by the hepatitis A virus. The virus is one of several types of hepatitis viruses that cause inflammation and affect your liver's ability to function."
            treatment = "Consult nearest hospital,	wash hands through,	avoid fatty,  spicy food, and	medication"
            

        elif predicted_disease == "Osteoarthritis":
            description = "Osteoarthritis is the most common form of arthritis, affecting millions of people worldwide. It occurs when the protective cartilage that cushions the ends of your bones wears down over time."
            treatment = "acetaminophen,	consult nearest hospital,	follow up, and salt baths"
         

        elif predicted_disease == "(vertigo) Paroymsal Positional Vertigo":
           description = "Benign paroxysmal positional vertigo (BPPV) is one of the most common causes of vertigo â€” the sudden sensation that you're spinning or that the inside of your head is spinning. Benign paroxysmal positional vertigo causes brief episodes of mild to intense dizziness."
           treatment = "lie down	avoid sudden change in body, 	avoid abrupt head movment, and relax"
         
        elif predicted_disease == "Hypoglycemia":
            description = "Hypoglycemia is a condition in which your blood sugar (glucose) level is lower than normal. Glucose is your body's main energy source. Hypoglycemia is often related to diabetes treatment. But other drugs and a variety of conditions â€” many rare â€” can cause low blood sugar in people who don't have diabetes."
            treatment = "lie down on side,	check in pulse	drink sugary drinks, and	consult doctor"
         
        elif predicted_disease == "Acne":
            description = "Acne vulgaris is the formation of comedones, papules, pustules, nodules, and/or cysts as a result of obstruction and inflammation of pilosebaceous units (hair follicles and their accompanying sebaceous gland). Acne develops on the face and upper trunk. It most often affects adolescents."
            treatment = "bath twice,	avoid fatty spicy food, 	drink plenty of water, and	avoid too many products"
        
        elif predicted_disease == "Diabetes":
            description = "Diabetes is a disease that occurs when your blood glucose, also called blood sugar, is too high. Blood glucose is your main source of energy and comes from the food you eat. Insulin, a hormone made by the pancreas, helps glucose from food get into your cells to be used for energy."
            treatment = "have balanced diet, do	exercise, consult doctor,  and follow up"

        elif predicted_disease == "Impetigo":
            description = "Impetigo (im-puh-TIE-go) is a common and highly contagious skin infection that mainly affects infants and children. Impetigo usually appears as red sores on the face, especially around a child's nose and mouth, and on hands and feet. The sores burst and develop honey-colored crusts."
            treatment = "soak affected area in warm water,	use antibiotics,	remove scabs with wet compressed cloth,and consult doctor"
                    
        elif predicted_disease == "Hypertension":
            description = "Hypertension (HTN or HT), also known as high blood pressure (HBP), is a long-term medical condition in which the blood pressure in the arteries is persistently elevated. High blood pressure typically does not cause symptoms."
            treatment = "meditation	salt baths,	reduce stress, and	get proper sleep"

        elif predicted_disease == "Peptic ulcer disease ":
            description = "Peptic ulcer disease (PUD) is a break in the inner lining of the stomach, the first part of the small intestine, or sometimes the lower esophagus. An ulcer in the stomach is called a gastric ulcer, while one in the first part of the intestines is a duodenal ulcer."
            treatment = "avoid fatty spicy food,	consume probiotic food, eliminate milk, and 	limit alcohol"
        
        elif predicted_disease == "Dimorphic hemorrhoids(piles)":
            description = "Dimorphic hemorrhoids(piles) Hemorrhoids, also spelled haemorrhoids, are vascular structures in the anal canal. In their ... Other names, Haemorrhoids, piles, hemorrhoidal disease ."
            treatment = "avoid fatty, spicy food,	consume witch hazel,	warm bath with epsom salt, and	consume alovera juice"

        elif predicted_disease == "Common Cold":
            description = "The common cold is a viral infection of your nose and throat (upper respiratory tract). It's usually harmless, although it might not feel that way. Many types of viruses can cause a common cold."
            treatment = "drink vitamin c rich drinks,	take vapour, 	avoid cold food, and	keep fever in check"
      
        elif predicted_disease == "Chicken pox":
            description = "Chickenpox is a highly contagious disease caused by the varicella-zoster virus (VZV). It can cause an itchy, blister-like rash. The rash first appears on the chest, back, and face, and then spreads over the entire body, causing between 250 and 500 itchy blisters."
            treatment = "use neem in bathing,	consume neem leaves,	take vaccine, and	avoid public places"

       
        elif predicted_disease == "Hyperthyroidism":
            description = "Hyperthyroidism (overactive thyroid) occurs when your thyroid gland produces too much of the hormone thyroxine. Hyperthyroidism can accelerate your body's metabolism, causing unintentional weight loss and a rapid or irregular heartbeat."
            treatment = "eat healthy, do massage,	use lemon balm, take radioactive, and iodine treatment"
         

        elif predicted_disease == "Cervical spondylosis":
            description = "Cervical spondylosis is a general term for age-related wear and tear affecting the spinal disks in your neck. As the disks dehydrate and shrink, signs of osteoarthritis develop, including bony projections along the edges of bones (bone spurs)."
            treatment = "use heating pad or cold pack	exercise	, take otc pain reliver, and consult doctor"
      

        elif predicted_disease == "Urinary tract infection":
            description = "Urinary tract infection: An infection of the kidney, ureter, bladder, or urethra. Abbreviated UTI. Not everyone with a UTI has symptoms, but common symptoms include a frequent urge to urinate and pain or burning when urinating."
            treatment = "drink plenty of water,	increase vitamin c intake,	drink cranberry juice, and take probiotics"
        

        elif predicted_disease == "Varicose veins":
            description = "A vein that has enlarged and twisted, often appearing as a bulging, blue blood vessel that is clearly visible through the skin. Varicose veins are most common in older adults, particularly women, and occur especially on the legs."
            treatment = "lie down flat and raise the leg high,	use oinments,	use vein compression, and	dont stand still for long"
         

        elif predicted_disease == "AIDS":
            description = "Acquired immunodeficiency syndrome (AIDS) is a chronic, potentially life-threatening condition caused by the human immunodeficiency virus (HIV). By damaging your immune system, HIV interferes with your body's ability to fight infection and disease."
            treatment = "avoid open cuts,	wear ppe, if possible consult doctor and follow up"
            
         
        elif predicted_disease == "Paralysis (brain hemorrhage)":
            description = "Intracerebral hemorrhage (ICH) is when blood suddenly bursts into brain tissue, causing damage to your brain. Symptoms usually appear suddenly during ICH. They include headache, weakness, confusion, and paralysis, particularly on one side of your body."
            treatment = "do massage,	eat healthy, do exercise, and	consult doctor"


        elif predicted_disease == "Typhoid":
            description = "Typhoid	is An acute illness characterized by fever caused by infection with the bacterium Salmonella typhi. Typhoid fever has an insidious onset, with fever, headache, constipation, malaise, chills, and muscle pain. Diarrhea is uncommon, and vomiting is not usually severe."
            treatment = "eat high calorie vegitables,	antiboitic therapy, and	consult doctor, and medication"


        elif predicted_disease == "Hepatitis B":
            description = "Hepatitis B is an infection of your liver. It can cause scarring of the organ, liver failure, and cancer. It can be fatal if it isn't treated. It's spread when people come in contact with the blood, open sores, or body fluids of someone who has the hepatitis B virus."
            treatment = "consult nearest hospital,	vaccination	eat healthy	medication"


        elif predicted_disease == "Fungal infection":
            description = "In humans, fungal infections occur when an invading fungus takes over an area of the body and is too much for the immune system to handle. Fungi can live in the air, soil, water, and plants. There are also some fungi that live naturally in the human body. Like many microbes, there are helpful fungi and harmful fungi."
            treatment = "bath twice,  use detol or neem in bathing water,	keep infected area dry, and use clean cloths"


        elif predicted_disease == "Hepatitis C":
            description = "Inflammation of the liver due to the hepatitis C virus (HCV), which is usually spread via blood transfusion (rare), hemodialysis, and needle sticks. The damage hepatitis C does to the liver can lead to cirrhosis and its complications as well as cancer."
            treatment = "Consult nearest hospital,	vaccination, and	eat healthy	medication"

        elif predicted_disease == "Bronchial asthma":
            description = "Bronchial asthma is a medical condition which causes the airway path of the lungs to swell and narrow. Due to this swelling, the air path produces excess mucus making it hard to breathe, which results in coughing, short breath, and wheezing. The disease is chronic and interferes with daily working."
            treatment = "switch to loose cloothing,	take deep breaths	get away from trigger seek help"


        elif predicted_disease == "Alcoholic hepatitis":
            description = "Alcoholic hepatitis is a diseased, inflammatory condition of the liver caused by heavy alcohol consumption over an extended period of time. It's also aggravated by binge drinking and ongoing alcohol use. If you develop this condition, you must stop drinking alcohol"
            treatment = "stop alcohol consumption,	consult doctor	medication	follow up"

       
        elif predicted_disease == "Jaundice":
            description = "Yellow staining of the skin and sclerae (the whites of the eyes) by abnormally high blood levels of the bile pigment bilirubin. The yellowing extends to other tissues and body fluids. Jaundice was once called the morbus regius (the regal disease) in the belief that only the touch of a king could cure it"
            treatment = "drink plenty of water,	consume milk thistle,	eat fruits and high fiberous food, medication"


        elif predicted_disease == "Hepatitis E":
            description = "A rare form of liver inflammation caused by infection with the hepatitis E virus (HEV). It is transmitted via food or drink handled by an infected person or through infected water supplies in areas where fecal matter may get into the water. Hepatitis E does not cause chronic liver disease."
            treatment = "stop alcohol consumption,	take rest, consult doctor medication"


        elif predicted_disease == "Dengue":
            description = "Dengue is an acute infectious disease caused by a flavivirus (species Dengue virus of the genus Flavivirus), transmitted by aedes mosquitoes, and characterized by headache, severe joint pain, and a rash. â€” called also breakbone fever, dengue fever."
            treatment = "drink papaya leaf juice, avoid fatty spicy food, keep mosquitos away, and keep hydrated"

        
        elif predicted_disease == "Hepatitis D":
            description = "Hepatitis D, also known as the hepatitis delta virus, is an infection that causes the liver to become inflamed. This swelling can impair liver function and cause long-term liver problems, including liver scarring and cancer. The condition is caused by the hepatitis D virus (HDV)."
            treatment = "consult doctor, medication, eat healthy, and follow up"

      
        elif predicted_disease == "Heart attack":
            description = "The death of heart muscle due to the loss of blood supply. The loss of blood supply is usually caused by a complete blockage of a coronary artery, one of the arteries that supplies blood to the heart muscle."
            treatment = "call ambulance, chew or swallow asprin, and keep calm"

      
        elif predicted_disease == "Pneumonia":
            description = "Pneumonia is an infection in one or both lungs. Bacteria, viruses, and fungi cause it. The infection causes inflammation in the air sacs in your lungs, which are called alveoli. The alveoli fill with fluid or pus, making it difficult to breathe."
            treatment = "consult doctor, medication, take rest,and follow up"

      
        elif predicted_disease == "Arthritis":
            description = "Arthritis is the swelling and tenderness of one or more of your joints. The main symptoms of arthritis are joint pain and stiffness, which typically worsen with age. The most common types of arthritis are osteoarthritis and rheumatoid arthritis."
            treatment = "exercise, use hot and cold therapy	try acupuncture, and make massage"

      
        elif predicted_disease == "Gastroenteritis":
            description = "Gastroenteritis is an inflammation of the digestive tract, particularly the stomach, and large and small intestines. Viral and bacterial gastroenteritis are intestinal infections associated with symptoms of diarrhea , abdominal cramps, nausea , and vomiting ."
            treatment = "stop eating solid food for while	try taking small sips of water	rest	ease back into eating"

      
        elif predicted_disease == "Tuberculosis":
            description = "Tuberculosis (TB) is an infectious disease usually caused by Mycobacterium tuberculosis (MTB) bacteria. Tuberculosis generally affects the lungs, but can also affect other parts of the body. Most infections show no symptoms, in which case it is known as latent tuberculosis."
            treatment = "cover your mouth, consult doctor , medication, take rest"

        elif predicted_disease == "Drug Reaction":
            description = "An adverse drug reaction (ADR) is an injury caused by taking medication. ADRs may occur following a single dose or prolonged administration of a drug or result from the combination of two or more drugs."
            treatment = "stop irritation,	consult nearest hospital,	stop taking drug and do follow up"

        else:
            description = "Please go to nearest hospital."
            treatment = "please seen by doctor and get consulted."

        

        #code for consult doctor codes assisting----------

        #   doctor_specialization = ["Rheumatologist","Cardiologist","ENT specialist","Orthopedist","Neurologist",
        #                             "Allergist/Immunologist","Urologist","Dermatologist","Gastroenterologist"]
        

        Rheumatologist = [  'Osteoarthristis','Arthritis']
       
        Cardiologist = [ 'Heart attack','Bronchial Asthma','Hypertension ']
       
        ENT_specialist = ['(vertigo) Paroymsal  Positional Vertigo','Hypothyroidism' ]

        Orthopedist = []

        Neurologist = ['Varicose veins','Paralysis (brain hemorrhage)','Migraine','Cervical spondylosis']

        Allergist_Immunologist = ['Allergy','Pneumonia',
        'AIDS','Common Cold','Tuberculosis','Malaria','Dengue','Typhoid']

        Urologist = [ 'Urinary tract infection',
         'Dimorphic hemmorhoids(piles)']

        Dermatologist = [  'Acne','Chicken pox','Fungal infection','Psoriasis','Impetigo']

        Gastroenterologist = ['Peptic ulcer diseae', 'GERD','Chronic cholestasis','Drug Reaction','Gastroenteritis','Hepatitis E',
        'Alcoholic hepatitis','Jaundice','hepatitis A',
         'Hepatitis B', 'Hepatitis C', 'Hepatitis D','Diabetes ','Hypoglycemia']
         
        if predicted_disease in Rheumatologist :
           consultdoctor = "Rheumatologist"
           
        if predicted_disease in Cardiologist :
           consultdoctor = "Cardiologist"
           

        elif predicted_disease in ENT_specialist :
           consultdoctor = "ENT specialist"
     
        elif predicted_disease in Orthopedist :
           consultdoctor = "Orthopedist"
     
        elif predicted_disease in Neurologist :
           consultdoctor = "Neurologist"
     
        elif predicted_disease in Allergist_Immunologist :
           consultdoctor = "Allergist or Immunologist"
     
        elif predicted_disease in Urologist :
           consultdoctor = "Urologist"
     
        elif predicted_disease in Dermatologist :
           consultdoctor = "Dermatologist"
     
        elif predicted_disease in Gastroenterologist :
           consultdoctor = "Gastroenterologist"
     
        else :
           consultdoctor = "other"

 
        diseasename = predicted_disease
        treatment = treatment
        description = description

        #def deleting(request,id=None):
            #do = get_object_or_404(Disease,id=id)
            #do.delete()
  
        Disease.objects.all().delete()   #deleting all existing datas from table.

        faaye = pyttsx3.init()
        voices = faaye.getProperty("voices")

        faaye.setProperty('rate', 180) # rate of voice
        faaye.setProperty('voice', voices[1].id) # to change voice to female

        #print(type(confidencescore))
       
        score = int(confidencescore)   

        if score < 50:
            
            #faaye.say("Ani maqaan koo Faaxeedha. Ana jechuun Haadha mana Khalid Abdellati. Waa tokko hin yaadina isin martu ni eebbifamtu, hojii dhabas ni taatu.")
            #faaye.say("Waaqni Hanga hardha jaalala fi kabajan wal wajjiin isin jiraachise,  ammas nagaa isin haa xumursiisu. ")
            #faaye.say("Boru Yilmaas ta'ee Ataklit, Beyenas ta'ee Tilahunin hin sodaatina. Ni xumura ni eebbiffamna.")

            faaye.say("Hello!  how are you doing ? you give me " + str(inputno) + " Symptoms. Depend up on the symptom you give me, the accuracy and confidence score is " + confidencescore )
            faaye.say("Which is less than 50. With this Accuracy I can predict your disease, and you may have " + predicted_disease + ", but its not accurate and recommended to predict disease with this confidence score.")
            faaye.say("To get accurately predicted disease, please enter all of your conditions and symptoms.")
            faaye.say("Thank for being here and using Fayyaan Faaya Medical Consultation System.")
            faaye.runAndWait()

        else:
            diseaseinfo = Disease(diseasename = predicted_disease, diseasedescription = description, diseasetreatment = treatment)
            #diseaseinfo.delete() deleting the existing and new one to database
            diseaseinfo.save()
            
            
            faaye.say("Hello!  how are you doing ? you give me " + str(inputno) + " Symptom. Which includes")
            faaye.say(psymptoms)
            faaye.say(" depend up on your symptom ")
            faaye.say("Your predicted disease is " + predicted_disease + " with confidence score or accuracy of " + confidencescore)
            faaye.say(description)
            faaye.say("  Please take the following measures and treatments. ")
            faaye.say(treatment)
            faaye.say("And also you need seen and consulted by " + consultdoctor + " Doctor. " + " To get detail description of "+ predicted_disease+ " click the link below predicted disease label. " + " Thank for being here and using Fayyaan Faaya Medical Consultation System.")
        
            
            faaye.runAndWait()
            
            #return render(request,'English/disease/checkdisease.html', {'predicteddisease':predicted_disease},{'confidencescore':confidencescore},{'consultdoctor': consultdoctor},{'information':information})
            
        return JsonResponse({'predicteddisease': predicted_disease ,'confidencescore':confidencescore , "consultdoctor": consultdoctor, "description":description, "treatment":treatment})
       
def diseaseinfo(request):
    information = Disease.objects.all()
    return render(request,'English/disease/diseaseinfo.html', {'information': information})

# Views of diseases

def consult_option(request):
    return render(request,'English/disease/consult_option.html')


def cancer(request):
    return render(request,'English/disease/category/cancer.html')

   

