import pickle
import streamlit as st

#from dotenv import load_dotenv
#load_dotenv()

###Initial UI configuration:###
st.set_page_config(page_title='Conestoga AIML', page_icon="🦙", layout="wide")


def model_run(model, prompt):
    print("Calling model...")
    if model == 'PROG8245':
        with open('model/prog8245nlp.pkl', 'rb') as file:
            pickle_model = pickle.load(file)
        with open('model/prog8245nlp-tfidf.pkl', 'rb') as file:
            pickle_tfidf = pickle.load(file)

        return 'Spam' if pickle_model.predict(pickle_tfidf.transform([prompt]))[0] == 1 else 'Ham'
    elif model == 'CSCN8010':
        print('a')
        return 'b'


def render_app():
    # reduce font sizes for input text boxes
    custom_css = """
        <style>
            .stTextArea textarea {font-size: 13px;}
            div[data-baseweb="select"] > div {font-size: 13px !important;}
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    #Left sidebar menu
    st.sidebar.header('Conestoga AIML')

    #Set config for a cleaner menu, footer & background:
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    if 'chat_dialogue' not in st.session_state:
        st.session_state['chat_dialogue'] = []

    if 'pre_prompt' not in st.session_state:
        st.session_state['pre_prompt'] = ''

    #Dropdown menu to select the model edpoint:
    selected_option = st.sidebar.selectbox('Choose a Model:', ['PROG8245NLP', 'CSCN8010VGG'], key='model')
    if selected_option == 'PROG8245NLP':
        st.session_state['page'] = 'PROG8245'
    elif selected_option == 'CSCN8010VGG':
        st.session_state['page'] = 'CSCN8010'
    else:
        st.session_state['page'] = 'c'

    #Model hyper parameters:
    #st.session_state['temperature'] = st.sidebar.slider('Temperature:', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    #st.session_state['top_p'] = st.sidebar.slider('Top P:', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    #st.session_state['max_seq_len'] = st.sidebar.slider('Max Sequence Length:', min_value=64, max_value=4096, value=2048, step=8)

    btn_col1, btn_col2 = st.sidebar.columns(2)

    def clear_history():
        st.session_state['chat_dialogue'] = []
    clear_chat_history_button = btn_col1.button("Clear History",
                                            use_container_width=True,
                                            on_click=clear_history)


    # add links to relevant resources for users to select
    st.sidebar.write(" ")

    text1 = 'llama2-chatbot'
    text2 = 'bckgmail'
    text3 = 'email-spam-classification-merged'

    text1_link = 'https://github.com/a16z-infra/llama2-chatbot'
    text2_link = 'https://github.com/KajPe/bckgmail'
    text3_link = 'https://huggingface.co/h-e-l-l-o/email-spam-classification-merged'

    logo1 = 'https://cdn.pixabay.com/photo/2022/01/30/13/33/github-6980894_1280.png'
    logo2 = 'https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo.svg'

    st.sidebar.markdown(
        "**Reference Code and Model:**  \n"
        f"<img src='{logo1}' style='height: 2em'> [{text2}]({text2_link})  \n"
        f"<img src='{logo1}' style='height: 2em'> [{text1}]({text1_link})  \n"
        f"<img src='{logo2}' style='height: 2em'> [{text3}]({text3_link})",
        unsafe_allow_html=True)

    icon_arcadio = 'https://avatars.githubusercontent.com/u/122412860?v=4'
    icon_givors = 'https://avatars.githubusercontent.com/u/17698876?v=4'
    icon_kyle = 'https://avatars.githubusercontent.com/u/777378?v=4'

    st.sidebar.write(" ")
    st.sidebar.markdown(
        "**Contributors:**  \n"
        f"<img src='{icon_arcadio}' style='height: 2em'> [{'**Arcadio**'}]({'https://github.com/arcadiopfz'})  \n"
        f"<img src='{icon_givors}' style='height: 2em'> [{'**Givors Ku**'}]({'https://github.com/guggg'})  \n"
        f"<img src='{icon_kyle}' style='height: 2em'> [{'**Kyle**'}]({'https://github.com/onlyxool'})",
        unsafe_allow_html=True)

    if st.session_state['page'] == 'CSCN8010':
        st.title('CSCN8010')
        uploaded_file = st.file_uploader("Upload a Image", type=('bmp', 'jpg', 'png', 'jpeg'))

        if uploaded_file:
            article = uploaded_file.read().decode()
            print(article)

    elif st.session_state['page'] == 'PROG8245':
        st.title('PROG8245')

        for message in st.session_state.chat_dialogue:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input('Type your mail content here to detect Spam'):
            st.session_state.chat_dialogue.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                string_dialogue = st.session_state['pre_prompt']
                output = model_run('PROG8245', string_dialogue)
                message_placeholder.markdown(output)

            st.session_state.chat_dialogue.append({"role": "assistant", "content": output})


render_app()