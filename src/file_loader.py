from langchain_community.document_loaders import PDFMinerLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

file_path = (
    "./Documents/link_product.pdf"
)
loader = PDFMinerLoader(file_path)
pages = loader.load_and_split()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # chunk size (characters)
    chunk_overlap=0,  # chunk overlap (characters)
    add_start_index=True,  # track index in original document
)
all_splits = text_splitter.split_documents(pages)


file_path_2 = (
    "./Documents/blog_goatbeauty.pdf"
)
loader = PDFMinerLoader(file_path_2)
pages = loader.load_and_split()
all_splits_2 = text_splitter.split_documents(pages)