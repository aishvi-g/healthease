
import cohere
import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

from health_data import health_database, train_data
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem


train_data = [
    ("CBC", "What is CBC"),
("Why CBC is done", "Why do we do CBC"),
("CBC preparation", "How to prepare for CBC"),
("CBC Procedure", "How is CBC done"),
("CBC Results", "What are normal results of CBC"),
("CBC Results meaning", "What does CBC Results mean"),
("Ibuprofen", "What is price of Ibuprofen"),
("Vitamin D3", "What medicines have Vitamin D3"),
("STD", "What are STD ?"),
("HIV", "What is HIV?"),
("CRP", "What is CRP Test?"),
("Reasons for CRP Test", "Why do we do CRP Test"),
]
health_database = [
  ("CBC", "A measure of the number of red blood cells, white blood cells, and platelets in the blood. The amount of hemoglobin (substance in the blood that carries oxygen) and the hematocrit (the amount of whole blood that is made up of red blood cells) are also measured. A complete blood count is used to help diagnose and monitor many conditions. Also called blood cell count, CBC, and full blood count. \n\n (Source: National Cancer Institute (https://www.cancer.gov/publications/dictionaries/cancer-terms/def/complete-blood-count))"),
("Why CBC is done", "\nA complete blood count is a common blood test done for many reasons:\n\n\t• To look at overall health. A complete blood count can be part of a medical exam to check general health and to look for conditions, such as anemia or leukemia.\n\n\t• To diagnose a medical condition. A complete blood count can help find the cause of symptoms such as weakness, fatigue and fever. It also can help find the cause of swelling and pain, bruising, or bleeding.\n\n\t• To check on a medical condition. A complete blood count can help keep an eye on conditions that affect blood cell counts.\n\n\t• To check on medical treatment. A complete blood count may be used to keep an eye on treatment with medicines that affect blood cell counts and radiation. \n\n (Source: Mayo Clinic (https://www.mayoclinic.org/tests-procedures/complete-blood-count/about/pac-20384919))"),
("CBC preparation", "If your blood sample is being tested only for a complete blood count, you can eat and drink as usual before the test. If your blood sample also will be used for other tests, you might need to fast for a certain amount of time before the test. Ask your health care provider what you need to do. \n\n (Source: Mayo Clinic ( https://www.mayoclinic.org/tests-procedures/complete-blood-count/about/pac-20384919 ))"),
("CBC Procedure", "For a complete blood count, a member of the health care team takes a sample of blood by putting a needle into a vein in your arm, usually at the bend in your elbow. The blood sample is sent to a lab. After the test, you can return to your usual activities right away. \n\n (Source: Mayo Clinic ( https://www.mayoclinic.org/tests-procedures/complete-blood-count/about/pac-20384919 ))"),
("CBC Results", "The following are expected complete blood count results for adults. The blood is measured in cells per liter (cells/L) or grams per deciliter (grams/dL).\n\nRed blood cell count\nMale: 4.35 trillion to 5.65 trillion cells/L\nFemale: 3.92 trillion to 5.13 trillion cells/L\n\nHemoglobin\nMale: 13.2 to 16.6 grams/dL\n(132 to 166 grams/L)\nFemale: 11.6 to 15 grams/dL\n(116 to 150 grams/L)\n\nHematocrit\nMale: 38.3% to 48.6%\nFemale: 35.5% to 44.9%\n\nWhite blood cell count\n3.4 billion to 9.6 billion cells/L\n\nPlatelet count\nMale: 135 billion to 317 billion/L\nFemale: 157 billion to 371 billion/L \n\n (Source: Mayo Clinic ( https://www.mayoclinic.org/tests-procedures/complete-blood-count/about/pac-20384919 ))"),
("CBC Results meaning", "Results in the following areas above or below the typical ranges on a complete blood count might point to a problem.\n\nRed blood cell count, hemoglobin and hematocrit. The results of these three are related because they each measure a feature of red blood cells.\n\n\t• Lower than usual measures in these three areas are a sign of anemia. Anemia has many causes. They include low levels of certain vitamins or iron, blood loss, or another medical condition. People with anemia might feel weak or tired. These symptoms may be due to the anemia itself or the cause of anemia.\n\n\t• A red blood cell count that's higher than usual is known as erythrocytosis. A high red blood cell count or high hemoglobin or hematocrit levels could point to a medical condition such as blood cancer or heart disease.\n\nWhite blood cell count.\n\n\t• A low white blood cell count is known as leukopenia. A medical condition such as an autoimmune disorder that destroys white blood cells, bone marrow problems or cancer might be the cause. Certain medicines also can cause a drop in white blood cell counts.\n\n\t• A white blood cell count that's higher than usual most commonly is due to an infection or inflammation. Or it could point to an immune system disorder or a bone marrow disease. A high white blood cell count also can be a reaction to medicines or hard exercise.\n\nPlatelet count.\n\n\t• A platelet count that's lower than usual is known as thrombocytopenia. If it's higher than usual, it's known as thrombocytosis. Either can be a sign of a medical condition or a side effect from medicine. A platelet count that's outside the typical range will likely lead to more tests to diagnose the cause.\n\nYour health care provider can tell you what your complete blood count results mean. \n\n (Source: Mayo Clinic ( https://www.mayoclinic.org/tests-procedures/complete-blood-count/about/pac-20384919 ))"),
("Ibuprofen", "1. Drug code -> 14\nGeneric Name -> Ibuprofen 400mg and Paracetamol 325mg Tablets IP\nUnit size -> 10's\nMRP -> 8.00\n\n2. Drug code -> 15\nGeneric Name -> Ibuprofen Tablets IP 200 mg\nUnit size -> 10's\nMRP -> 3.00\n\n3. Drug code -> 16\nGeneric Name -> Ibuprofen Tablets IP 400 mg\nUnit size -> 15's\nMRP -> 8.00\n\n4. Drug code -> 1664\nGeneric Name -> Ibuprofen 100mg and Paracetamol/Acetaminophen 162.5mg Oral Suspension\nUnit size -> 100 ml\nMRP -> 23.00 \n\n (Source: Pharmaceuticals & Medical Devices Bureau of India (PMBI) (http://janaushadhi.gov.in/ProductList.aspx))"),
("Vitamin D3", "1. Drug Code -> 220\nGeneric Name -> Calcium 500mg and Vitamin D3 250IU Tablets IP\nUnit Size -> 10's\nMRP -> 7.70\n\n2. Drug Code -> 779\nGeneric Name -> Alpha Lipolic Acid 100mg, Vitamin D3 1000IU, Folic Acid 1.5mg, Pyridoxine 3mg and Methylcobalamin150 0mcg Tablets\nUnit Size -> 10's\nMRP -> 48.00\n\n3. Drug Code -> 817\nGeneric Name -> Calcium Carbonate 1250mg, Vitamin D3 250IU, Magnesium Oxide 40mg, Manganese Sulphate 1.8mg and Zinc 7.5mg Tablets\nUnit Size -> 10's\nMRP -> 14.30\n\n4. Drug Code -> 833\nGeneric Name -> Cholecalciferol (Vitamin D3) Drops 800 IU per ml\nUnit Size -> 15 ml\nMRP -> 27.00\n\n5. Drug Code -> 834\nGeneric Name -> Cholecalciferol (Vitamin D3) Drops 400 IU per ml\nUnit Size -> 15 ml\nMRP -> 20.00\n\n6. Drug Code -> 1252\nGeneric Name -> Calcium Phosphate 82mg, Vitamin D3 200IU and Vitamin B12 2.5mcg Suspension\nUnit Size -> 200 ml\nMRP -> 36.00\n\n7. Drug Code -> 1537\nGeneric Name -> Calcium and Vitamin D3 Capsules\nUnit Size -> 10's\nMRP -> 33.00\n\n8. Drug Code -> 1841\nGeneric Name -> Vitamin D3 Oral Solution 60000 IU\nUnit Size -> 5 ml\nMRP -> 25.00\n\n9. Drug Code -> 2003\nGeneric Name -> Calcium 500mg and Vitamin D3 500IU Tablets IP\nUnit Size -> 10's\nMRP -> 8.00\n\n10. Drug Code -> 2083\nGeneric Name -> Calcium Citrate Malate 250mg , Vitamin D3 100IU and Folic Acid 50mcg Tablets\nUnit Size -> 10's\nMRP -> 20.00 \n\n (Source: Pharmaceuticals & Medical Devices Bureau of India (PMBI) (http://janaushadhi.gov.in/ProductList.aspx))"),
("STD", "STDs are infectious diseases passed from person to person through sexual contact. Millions of new cases happen every year in the U.S. Half of the new infections happen in people between the ages of 15 and 24 years. \n (Source: Johns Hopkins Medicine)"),
("HIV", "HIV is a virus that destroys the body's ability to fight off infection. People who have HIV may not look or feel sick for a long time after infection. But if you are not diagnosed early and treated, you will eventually become very likely to get many life-threatening diseases and certain forms of cancer.\n- The virus is passed on most often during sexual activity. It can also be passed on by sharing needles used to inject IV drugs.\n- HIV can be passed to your baby during pregnancy, labor, delivery, and through breastfeeding. If you know early in your pregnancy that you are HIV positive, you can get treatment that greatly lowers your chance of passing on the virus to your child, the CDC says. \n (Source: Johns Hopkins Medicine)"),
("CRP", "C-reactive protein (CRP) is a protein made by the liver. The level of CRP increases when there's inflammation in the body. A simple blood test can check your C-reactive protein level.\n A high-sensitivity C-reactive protein (hs-CRP) test is more sensitive than a standard C-reactive protein test. That means the high-sensitivity test can find smaller increases in C-reactive protein than a standard test can. \n The hs-CRP test can help show the risk of getting coronary artery disease. In coronary artery disease, the arteries of the heart narrow. Narrowed arteries can lead to a heart attack. \n (Source: )"),
("Reasons for CRP Test", "Your health care provider might order a C-reactive protein test to:\n\nCheck for infection.\nHelp diagnose a chronic inflammatory disease, such as rheumatoid arthritis or lupus.\nLearn your risk of heart disease.\nLearn your the risk of a second heart attack \n  \n (Source: )"),

]


api_key = st.secrets["api_key"]
azure_key = st.secrets["azure_key"]
endpoints = st.secrets["endpoint"]
region = st.secrets["region"]

credential = TranslatorCredential(azure_key, region)
text_translator = TextTranslationClient(endpoint=endpoints, credential=credential)


st.set_page_config(page_title="MedEase")
co = cohere.Client(api_key)


class cohereExtractor():
    def __init__(self, examples, example_labels, labels, task_desciption, example_prompt):
        self.examples = examples
        self.example_labels = example_labels
        self.labels = labels
        self.task_desciption = task_desciption
        self.example_prompt = example_prompt

    def make_prompt(self, example):
        examples = self.examples + [example]
        labels = self.example_labels + [""]
        return (self.task_desciption +
                "\n---\n".join([examples[i] + "\n" +
                                self.example_prompt +
                                labels[i] for i in range(len(examples))]))

    def extract(self, example):
        extraction = co.generate(
            model='xlarge',
            prompt=self.make_prompt(example),
            max_tokens=15,
            temperature=0.1,
            stop_sequences=["\n"])
        return (extraction.generations[0].text[:-1])


cohereHealthExtractor = cohereExtractor([e[1] for e in train_data],
                                        [e[0] for e in train_data], [],
                                        "",
                                        "extract the Keywords from the medical terminology related answers:")
text = cohereHealthExtractor.make_prompt(
    'What are alternatives for paracetamol')
target_language_code = "en" 

with st.sidebar:
    colored_header(label='🌼 Welcome to MedEase 👩‍⚕️', description="Here to Help You", color_name='blue-30')
    st.header('Health Assistant Chatbot')
    target_language_code = st.text_input("Enter the language code for the response:")

    st.markdown('''
    ## About MedEase
    MedEase is your friendly health assistant chatbot designed to provide information and support for understanding test results and finding medicine prices.

    🚑  We believe in empowering individuals to take charge of their health and well-being.

    ### How MedEase Can Help You
    ####  🩺 Test Result Insights:
    - MedEase can provide you with easy-to-understand explanations of your test results, helping you gain a better understanding of your health status.
                
     #### 💊 Medicine Price Comparison: 
    - MedEase can help you find similar medicine prices, ensuring you make informed decisions and potentially save on your healthcare expenses.
    
    💡 Note: MedEase is an AI-powered chatbot and should not replace professional medical advice. Always consult with healthcare professionals for personalized guidance.

    🤝 Let MedEase be your trusted companion on your health journey. Together, we can strive for a healthier and happier you!
    ''')
    add_vertical_space(5)


if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I'm MedEase 👩‍⚕️, How may I help you?"]

if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

response_container = st.container()
colored_header(label='', description='', color_name='blue-30')

input_container = st.container()

def translate_text(text, target_language):
    
    target_languages = [target_language]
    input_text_elements = [ InputTextItem(text = text) ]

    response = text_translator.translate(content = input_text_elements, to = target_languages)
    translation = response[0] if response else None;
    if translation:
        for translated_text in translation.translations:
            return translated_text.text
    else:
        return text


def get_text():
    input_text = st.text_input("You: ", key="input")
    
    return input_text


with input_container:
    user_input = get_text()


def extract_keywords(input_text):
    extraction = cohereHealthExtractor.extract(input_text)
    keywords = extraction.split(',')
    keywords = [keyword.strip().lower() for keyword in keywords]
    return keywords


def search_answer(keywords):
    for keyword, answer in health_database:
        if keyword.lower() in keywords:
            return answer
    return "I'm sorry, but I'm unable to provide information on that topic. For accurate and reliable information, please consult a healthcare professional or trusted educational resources."


# def generate_response(prompt, thumbs_up_count, thumbs_down_count):
#     keywords = extract_keywords(user_input)
#     answer = search_answer(keywords)

#     return answer + "\n\n" + "Keywords: " + ", ".join(keywords)
def generate_response(prompt, target_language):

    keywords = extract_keywords(user_input)
    answer = search_answer(keywords)

    translated_answer = translate_text(answer, target_language)

    return translated_answer + "\n\n" + "Keywords: " + ", ".join(keywords)

with response_container:
    if user_input:
        if target_language_code == "":
            target_language_code = "en"
       
        response = generate_response(
            user_input,  target_language_code
        )
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
        st.empty()

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))

