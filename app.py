import streamlit as st
from pymongo import MongoClient
import bcrypt
from PIL import Image
import io
import datetime

# Configuração do MongoDB
client = MongoClient('mongodb+srv://analistasergiosantos:7JytXMbp1iWzecxu@cluster0.u6arcnr.mongodb.net/')
db = client['Clientes']
usuarios = db['Barbearia']
comentarios = db['Comentarios']  # Nova coleção para comentários


# Funções auxiliares
def register_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    usuarios.insert_one({'username': username, 'password': hashed_password, 'photo': None})

def authenticate_user(username, password):
    user = usuarios.find_one({'username': username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return user
    return None

def save_user_photo(username, image_bytes):
    user = usuarios.find_one({'username': username})
    if user:
        photo = image_bytes.getvalue()  # Converte a imagem para bytes
        usuarios.update_one({'username': username}, {'$set': {'photo': photo}})

def show_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    st.image(image, caption="Imagem Capturada", use_column_width=True)

# Função para salvar comentários
def save_comment(video_id, username, comment_text):
    comentario = {
        "video_id": video_id,
        "username": username,
        "comment": comment_text,
        "date": datetime.datetime.now()
    }
    comentarios.insert_one(comentario)

# Função para exibir os comentários de um vídeo
def display_comments(video_id):
    st.subheader("Comentários")

    video_comments = comentarios.find({"video_id": video_id}).sort("date", -1)

    for comment in video_comments:
        st.write(f"**{comment['username']}**: {comment['comment']} (em {comment['date'].strftime('%d/%m/%Y %H:%M')})")
        st.markdown("---")

# Função para exibir e comentar sobre vídeos por nível
def display_videos(level):
    st.subheader(f"Vídeos Nível {level}")

    # Lista de vídeos a serem exibidos por nível
    videos_by_level = {
        1: [
            {"id": "video1", "title": "01 - Conhecendo o Intrumento", "url": "https://www.youtube.com/watch?v=KYGtdSuTiAA"},
            {"id": "video2", "title": "02 - Afinação e Fundamentos", "url": "https://www.youtube.com/watch?v=HTDs9kDLhKc"},
             {"id": "video3", "title": "03 - Primeira Música", "url": "https://www.youtube.com/watch?v=liC49Dol6OY"},
            {"id": "video4", "title": "04 - Exércícios mão direita ", "url": "https://www.youtube.com/watch?v=DoXEI1mAbu8"},
             {"id": "video5", "title": "05 -Segunda Música ", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
            {"id": "video6", "title": "06 - Terceira Música", "url": "https://www.youtube.com/watch?v=abc123example"},
             {"id": "video7", "title": "07- Exercícios mão esquerda", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
            {"id": "video8", "title": "08- Quarta Música", "url": "https://www.youtube.com/watch?v=abc123example"},
             {"id": "video9", "title": "09 - Quinta Música", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
            {"id": "video10", "title": "10- Sexta Música  - Fundamentos", "url": "https://www.youtube.com/watch?v=abc123example"},
        ],
       
        2: [
            {"id": "video3", "title": "Vídeo Nível 2 - Intermediário", "url": "https://www.youtube.com/watch?v=def456example"},
            {"id": "video4", "title": "Vídeo Nível 2 - Técnicas Avançadas", "url": "https://www.youtube.com/watch?v=ghi789example"}
        ],
        3: [
            {"id": "video5", "title": "Vídeo Nível 3 - Avançado", "url": "https://www.youtube.com/watch?v=jkl012example"},
            {"id": "video6", "title": "Vídeo Nível 3 - Prática Avançada", "url": "https://www.youtube.com/watch?v=mno345example"}
        ],
        4: [
            {"id": "video7", "title": "Vídeo Nível 4 - Profissional", "url": "https://www.youtube.com/watch?v=pqr678example"},
            {"id": "video8", "title": "Vídeo Nível 4 - Expert", "url": "https://www.youtube.com/watch?v=stu901example"}
        ],
        5: [
            {"id": "video9", "title": "Vídeo Nível 5 - Especialista", "url": "https://www.youtube.com/watch?v=vwx234example"},
            {"id": "video10", "title": "Vídeo Nível 5 - Masterclass", "url": "https://www.youtube.com/watch?v=yza567example"}
        ]
    }

    # Exibir vídeos em duas colunas
    col1, col2 = st.columns(2)

    for idx, video in enumerate(videos_by_level.get(level, [])):
        if idx % 2 == 0:
            with col1:
                if st.button(video["title"]):
                    st.video(video["url"])
                    st.write(f"Você está assistindo {video['title']}")
                    display_comments(video["id"])

                    # Área para enviar comentários
                    if st.session_state["logged_in"]:
                        comment_text = st.text_area(f"Deixe seu comentário no {video['title']}")
                        if st.button(f"Enviar Comentário {video['title']}"):
                            save_comment(video["id"], st.session_state["username"], comment_text)
                            st.success("Comentário enviado com sucesso!")
                    else:
                        st.warning("Faça login para comentar.")
        else:
            with col2:
                if st.button(video["title"]):
                    st.video(video["url"])
                    st.write(f"Você está assistindo {video['title']}")
                    display_comments(video["id"])

                    # Área para enviar comentários
                    if st.session_state["logged_in"]:
                        comment_text = st.text_area(f"Deixe seu comentário no {video['title']}")
                        if st.button(f"Enviar Comentário {video['title']}"):
                            save_comment(video["id"], st.session_state["username"], comment_text)
                            st.success("Comentário enviado com sucesso!")
                    else:
                        st.warning("Faça login para comentar.")

# Interface com Streamlit
def main():
    # Iniciar sessão para armazenar estado de login
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""

    st.title("Login e Cadastro")

    # Mostrar nome do usuário logado na barra lateral
    if st.session_state["logged_in"]:
        st.sidebar.write(f"Usuário logado: {st.session_state['username']}")
        if st.sidebar.button("Deslogar"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.success("Você foi deslogado com sucesso!")
    else:
        st.sidebar.write("Você não está logado")

    # Menu de navegação lateral
    menu = st.sidebar.selectbox("Menu", ["Login", "Cadastro", "Captura de Foto", "Vídeos"])

    if menu == "Cadastro":
        st.subheader("Criar Conta")
        username = st.text_input("Nome de usuário")
        password = st.text_input("Senha", type="password")

        if st.button("Cadastrar"):
            if username and password:
                if usuarios.find_one({'username': username}):
                    st.error("Usuário já existe.")
                else:
                    register_user(username, password)
                    st.success("Usuário cadastrado com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos.")

    elif menu == "Login":
        st.subheader("Entrar")
        username = st.text_input("Nome de usuário")
        password = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            user = authenticate_user(username, password)
            if user:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success("Login bem-sucedido!")
                st.write("Bem-vindo à área restrita!")

                # Captura de foto usando a webcam
                camera_image = st.camera_input("Tire uma foto")

                if camera_image:
                    image_bytes = io.BytesIO(camera_image.read())
                    show_image(image_bytes)
                    save_user_photo(username, image_bytes)
                    st.success("Foto salva com sucesso!")

                # Exibir foto armazenada
                if user.get('photo'):
                    st.subheader("Sua Foto")
                    st.image(io.BytesIO(user['photo']), caption="Foto Armazenada", use_column_width=True)
            else:
                st.error("Credenciais inválidas.")

    elif menu == "Captura de Foto":
        if not st.session_state["logged_in"]:
            st.warning("Por favor, faça login para acessar esta aba.")
        else:
            st.subheader("Captura de Foto")

            # Captura de foto usando a webcam
            camera_image = st.camera_input("Tire uma foto")

            if camera_image:
                show_image(camera_image.read())
                st.success("Foto capturada com sucesso!")

    elif menu == "Vídeos":
        if not st.session_state["logged_in"]:
            st.warning("Por favor, faça login para acessar esta aba.")
        else:
            st.subheader("Seu ambiente de estudo ")

            # Escolher o nível de vídeos
            nivel = st.selectbox("Escolha o Nível", [1, 2, 3, 4, 5])
            display_videos(nivel)

if __name__ == "__main__":
    main()
