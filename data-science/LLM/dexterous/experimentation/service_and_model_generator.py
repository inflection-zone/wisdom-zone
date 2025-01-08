import json
import ast
from langchain_community.chat_models import ChatOpenAI
from datetime import date
from langchain.schema import StrOutputParser
from langchain.chains import LLMChain, SequentialChain
from apikey import openapi_key
from langchain.prompts import MessagesPlaceholder,HumanMessagePromptTemplate,ChatPromptTemplate

openapi_key=openapi_key
llm=ChatOpenAI(model="gpt-3.5-turbo",openai_api_key=openapi_key,temperature=0.1)
project_info={}


# Add logs to the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            '''You are a software architect with vast experience in designing microservice architectures, 
            You have a deep understanding of database modeling principles and best practices.''',
        ),
        ("human", "{question}"),
    ]
)

chain = LLMChain(llm=llm, prompt=prompt)

def get_project_info():
    print("************I am your friendly Chatbot! who is expert in development***************\n")
    print(f"CHATBOT: please provide your project name?\n")
    pro_Name=input("USER: ")
    project_info['Name']=pro_Name
    print(f"\nCHATBOT: Describe shortly about your system.. \n")
    project_info['project_Descri']=input("User: ")
    result=chain.run(question=f"do not describe, list the services in the form of dictionary for {pro_Name}")
    print(result)
    print("CHATBOT: These are the services suggested to your system\n")
    def dict_key(dictionary):
        print("\nCHATBOT: Do you want to add any service? type Yes or No\n")
        check_use=input("USER: ")
        if check_use=="yes":
            print("\nCHATBOT: please enter which service you want to Add:\n")
            add_use=input("USER: ")
            if add_use in hospital_features.keys():
                print("\n This use case is already present")
            else:
                print("\n CHATBOT: please describe about this service:\n")
                hospital_features[add_use]=input("USER: ")        
        else:
            print("dont want to add")
        print("\nCHATBOT: Do you want to remove any service? type Yes or No\n")
        check_use=input("USER: ")
        if check_use=="yes":
            print("\nCHATBOT: please enter which service you want to Remove:\n")
            del_use=input("USER: ")
            key_del = del_use.casefold() 
            for key in hospital_features.keys():  # Iterate over a copy to avoid RuntimeError
                if key.casefold() == key_del:
                    del hospital_features[key]
                    break
                else:
                    print("\n please enter correct service.\n")
        else:
            print("")
            print("\nCHATBOT: These are your final service for project:\n")
    try:
        hospital_features = json.loads(result)
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e)      
    dict_key(hospital_features)
    for key in hospital_features:
        print(key)
    
    return hospital_features   


service=get_project_info()

services=[]
for key in service:
    services.append(key)


New_Service={}
for item in services:
    model_list=chain.run(f'''I am designing a database for a new service and need to create database models along with their descriptions. 
    Please provide a list of database models (as keys) and their corresponding descriptions (as values) for the following service: {item}. 
    The response should be in the form of key-value pairs where each key is a model name and each value is a description of that model. do not give the any extra line just return the dictionary ''')
    try:
        item1 = json.loads(model_list)
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e) 
    for key in item1:
        New_Service[item]=[]
        
    for key in item1:
        New_Service[item].append(key)



refining=chain.run(f''' These are the models for the service {New_Service}. Remove the repeated models, ensuring each model belongs to only one service if necessary and if it is a part of that service. Otherwise, add it to another appropriate service. Finally, return the finalized dictionary. Only return the dictionary without any extra sentences''')

services_dict = ast.literal_eval(refining)

for service, models in services_dict.items():
    print(f"Service:\n {service}")
    print(f"Models:")
    for model in models:
        print("\t",model)


def add_model(services_dict,serv):
        for service, models in services_dict.items():
            if service==serv:
                print(f"Chatbot: Enter which model you want to Add")
                mod=input(f"User:")
                services_dict[service].append(mod)
                for model in models:
                    print(model)
            else:
                print("") 
    
def del_model(services_dict,serv):
    for service, models in services_dict.items():
            if service==serv:
                print(f"Chatbot: Enter which model you want to Add")
                mod=input(f"User:")
                services_dict[service].remove(mod)
                for model in models:
                    print(model)
print(f"Chatbot: Do you want to Add any models to above services.")
check=input().lower()
if(check=="yes"):
    print(f"model belongs to which service:")
    serv=input()
    add_model(services_dict,serv)
else:
    print("")
print(f"Chatbot: Do you want to delete any models from above services.")
check=input().lower()
if(check=="yes"):
    print(f"model belongs to which service:")
    serv=input()
    del_model(services_dict,serv)
else:
    print("")


print("final services and there models")
for service, models in services_dict.items():
    print(f"Service:\n {service}")
    print(f"Models:")
    for model in models:
        print("\t",model)