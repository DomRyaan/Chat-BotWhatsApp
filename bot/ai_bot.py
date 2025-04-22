import os

from decouple import config

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEndpointEmbeddings

from Embedding.CustomEmbenddings import CustomEmbenddings

os.environ['GROQ_API_KEY'] = config('GROQ_API_KEY')
os.environ['HUGGINGFACEHUB_API_TOKEN'] = config('HUGGINGFACEHUB_API_TOKEN')


class AIBot:

    def __init__(self):
        self.__chat = ChatGroq(model='llama3-70b-8192')
        self.__retriever = self.__build_retriever()

    def __build_retriever(self):
        persist_directory = '/app/chroma_data'
        embedding = CustomEmbenddings(model="sentence-transformers/all-MiniLM-L6-v2", token=os.environ['HUGGINGFACEHUB_API_TOKEN'])

        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding,
        )
        return vector_store.as_retriever(
            search_kwargs={'k': 30},
        )

    def __build_messages(self, history_messages, question):
        messages = []
        for message in history_messages:
            message_class = HumanMessage if message.get('fromMe') else AIMessage
            messages.append(message_class(content=message.get('body')))
        messages.append(HumanMessage(content=question))
        return messages

    def invoke(self, history_messages, question):
        SYSTEM_TEMPLATE = '''
Você é uma atendente virtual simpática, eficiente e educada de uma Salgaderia chamada Gi Salgados.

Sua função é atender os clientes, anotar pedidos, responder dúvidas sobre o cardápio, horários de funcionamento. 

 **Nunca invente pratos, ingredientes, horários, valores ou formas de atendimento que não estejam especificadas.** Se o cliente pedir algo diferente, diga com gentileza que não é possível.

Siga estas diretrizes:

- Cumprimente o cliente com cordialidade e esteja sempre pronta para ajudar.
- Use uma linguagem informal e amigável, mas profissional.
- Seja clara e objetiva nas respostas, sem parecer robótica.
- Se o cliente quiser fazer um pedido, pergunte os itens e quantidades.
- Após o pedido, confirme os itens e forneça o valor total.
- Se não souber alguma informação, diga que vai verificar com a equipe.
- Sempre pergunte se o cliente deseja mais alguma coisa antes de encerrar o atendimento.
- No final, agradeça e deseje um bom dia/tarde.
- NUNCA diga que fazemos entregas.
- Responda sempre em portugues brasileiro

---

<context>
{context}
</context>
        
        '''

        docs = self.__retriever.invoke(question)
        question_answering_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    'system',
                    SYSTEM_TEMPLATE,
                ),
                MessagesPlaceholder(variable_name='messages'),
            ]
        )
        document_chain = create_stuff_documents_chain(self.__chat, question_answering_prompt)
        response = document_chain.invoke(
            {
                'context': docs,
                'messages': self.__build_messages(history_messages, question),
            }
        )
        return response
