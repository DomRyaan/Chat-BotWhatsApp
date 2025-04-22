from huggingface_hub import InferenceClient
from langchain_core.embeddings import Embeddings

class CustomEmbenddings(Embeddings):
    def __init__(self, model: str, token: str):
        self.cliente = InferenceClient(model=model, token=token)

        def embed_documents(self, texts: list[str]) -> list[list[float]]:
            return [self.cliente.feature_extracion(text) for text in texts]
        
        def embed_query(self, text:str) -> list[float]:
            return self.cliente.feature_extraction(text)
        