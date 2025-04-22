import os

from decouple import config
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEndpointEmbeddings


# Constantes de configuração
PERSIST_DIRECTORY = "/app/chroma_data"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHAT_MODEL = "llama3-70b-8192"

# Template do sistema
SYSTEM_TEMPLATE = '''
Você é uma atendente virtual simpática, eficiente e educada de uma Salgaderia chamada Gi Salgados.

Sua função é atender os clientes, anotar pedidos, responder dúvidas sobre o cardápio, horários de funcionamento. 

**Nunca invente pratos, ingredientes, horários, valores ou formas de atendimento que não estejam especificadas.** 
Se o cliente pedir algo diferente, diga com gentileza que não é possível.

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
- Responda sempre em português brasileiro.

---

<context>
{context}
</context>
'''


class AIBot:
    def __init__(self):
        self.chat_model = ChatGroq(
            model=CHAT_MODEL,
            groq_api_key=config("GROQ_API_KEY")
        )
        self.retriever = self._create_retriever()

    def _create_retriever(self):
        embedding_function = HuggingFaceEndpointEmbeddings(
            model=EMBEDDING_MODEL,
            huggingfacehub_api_token=config("HUGGINGFACEHUB_API_TOKEN")
        )

        vector_store = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=embedding_function,
        )

        return vector_store.as_retriever(search_kwargs={"k": 30})

    def _format_messages(self, history, user_question):
        messages = [
            (HumanMessage if m.get("fromMe") else AIMessage)(content=m.get("body"))
            for m in history
        ]
        messages.append(HumanMessage(content=user_question))
        return messages

    def invoke(self, history_messages, question):
        context_docs = self.retriever.invoke(question)

        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_TEMPLATE),
            MessagesPlaceholder(variable_name="messages"),
        ])

        document_chain = create_stuff_documents_chain(
            llm=self.chat_model,
            prompt=prompt,
        )

        response = document_chain.invoke({
            "context": context_docs,
            "messages": self._format_messages(history_messages, question),
        })

        return response
