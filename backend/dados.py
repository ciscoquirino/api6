import chromadb
from tqdm import tqdm
import re
import spacy # python -m spacy download en_core_web_sm
import nltk 
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer


client = chromadb.PersistentClient(path="client")

collection_name = 'test_collection_chunknized'

old_collection = client.get_collection(name=collection_name)

new_collection = client.get_or_create_collection(name="new_collection")

# Para tratamento de texto


# nltk.download('stopwords') # rodar apenas uma vez

# PLN

# Carregar o modelo de linguagem do spaCy
nlp = spacy.load("en_core_web_sm")

# Definir stopwords
stop_words = set(stopwords.words('english'))

# Função para fazer o tratamento de linguagem natural usando spaCy
def tratamento_pln(texto):

    # 1. Normalização: Colocar o texto em minúsculas
    texto = texto.lower()

    # 2. Remoção de pontuações e caracteres especiais
    texto = re.sub(r'[^\w\s]', '', texto) 

    # 3. Tokenização com spaCy
    doc = nlp(texto)
    tokens = [token.text for token in doc]

    # 4. Remoção de stopwords, remoção de pontuação
    #    e Lematização (clean_tokens = tokens lematizados e sem stopwords)
    clean_tokens = [token.lemma_ for token in doc if token.text not in stop_words and not token.is_punct]
 
    # 5. Juntar tokens lematizados de volta em uma string
    clean_text = ' '.join(clean_tokens)

    return clean_text


model = SentenceTransformer('all-MiniLM-L6-v2')


def embedding_func(texts):
    return model.encode(texts).tolist()

def process_batch(documents, your_nlp_function):
    docs_tratados = [your_nlp_function(doc) for doc in documents]
    return docs_tratados

def batch_process_chroma_documents(batch_size: int, your_nlp_function, embed_function):
    """
    Retrieves and processes documents from a ChromaDB collection in batches.

    Args:
        client: The ChromaDB client instance.
        collection_name: The name of the collection to process.
        batch_size: The number of documents to process in each batch.
        your_nlp_function: The function you want to apply to each document.
    """

    #total_count = old_collection.count() #reduzir aqui
    total_count = 100000
    offset = 0

    with tqdm(total=total_count, desc="Processing Documents") as pbar:
        while offset < total_count:
            # Get a batch of data (including documents)
            batch_data = old_collection.get(
                limit=batch_size,
                offset=offset,
                include=['documents', 'metadatas']  # Ensure we only fetch the documents
            )

            if not batch_data['documents']:
                break  # No more documents

            documents_to_process = batch_data['documents']
            ids_in_batch = batch_data['ids']
            metadatas_in_batch = batch_data['metadatas']
            # Process the current batch of documents
            processed_batch = process_batch(documents_to_process, your_nlp_function)
            
            batch_embeds = [embed_function(doc) for doc in processed_batch]

            # Do something with the processed batch (e.g., update the collection, store elsewhere)
            # Example: If you want to update the documents in the same collection
            # You'd need to fetch the IDs corresponding to these documents in the batch
            if ids_in_batch:
                new_collection.add(
                    ids=ids_in_batch,
                    documents=processed_batch,
                    embeddings=batch_embeds,
                    metadatas=metadatas_in_batch 
                )
                
                
                print(f"Added {len(processed_batch)} documents.")

            offset += batch_size
            pbar.update(len(documents_to_process))

    print("Finished processing all documents.")
    
    
batch_size = 100

batch_process_chroma_documents(batch_size, tratamento_pln, embedding_func)



