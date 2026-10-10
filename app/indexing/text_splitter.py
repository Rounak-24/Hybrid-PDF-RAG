from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import asyncio

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 3000,
    chunk_overlap = 200
)


async def split_docs(docs:list[Document]):
    try:
        chunks = await asyncio.to_thread(
            splitter.split_documents,
            documents = docs
        )

        print("Dconumet breaked into chunks....")
        return chunks

    except Exception as e:
        print("Something went wrong while split docs....")
        raise e