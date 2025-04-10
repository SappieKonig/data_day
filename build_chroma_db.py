#!/usr/bin/env python3
"""
Script to build a ChromaDB database from PDF files (like regioplannen) in a directory.
"""

import os
import sys
import argparse
import glob
from getpass import getpass
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

def setup_openai_api():
    """Set up the OpenAI API key from environment or prompt user"""
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        openai_api_key = getpass("Please enter your OpenAI API Key: ")
    
    os.environ["OPENAI_API_KEY"] = openai_api_key
    return openai_api_key

def process_pdf(pdf_path, text_splitter):
    """Process a single PDF file and return chunks"""
    try:
        print(f"Processing PDF: {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        print(f"  - Loaded {len(pages)} pages")
        
        # Split the document into chunks
        chunks = text_splitter.split_documents(pages)
        print(f"  - Split into {len(chunks)} chunks")
        return chunks
    except Exception as e:
        print(f"  ❌ Error processing {pdf_path}: {str(e)}")
        return []

def main():
    """Main function to process PDFs and build a Chroma database"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Build a ChromaDB database from PDF files.')
    parser.add_argument('pdf_directory', help='Directory containing PDF files to process')
    parser.add_argument('--output', '-o', default='chroma_db_regioplannen', 
                        help='Directory to store the ChromaDB database (default: chroma_db_regioplannen)')
    parser.add_argument('--chunk-size', type=int, default=1000, 
                        help='Size of text chunks (default: 1000)')
    parser.add_argument('--chunk-overlap', type=int, default=200, 
                        help='Overlap between chunks (default: 200)')
    parser.add_argument('--embedding-model', default='text-embedding-3-small', 
                        help='OpenAI embedding model to use (default: text-embedding-3-small)')
    
    args = parser.parse_args()
    
    # Check if the PDF directory exists
    if not os.path.isdir(args.pdf_directory):
        print(f"Error: Directory '{args.pdf_directory}' does not exist.")
        sys.exit(1)
    
    # Set up OpenAI API
    setup_openai_api()
    
    # Initialize the embedding model
    print(f"Initializing embedding model: {args.embedding_model}")
    try:
        embeddings_model = OpenAIEmbeddings(model=args.embedding_model)
    except Exception as e:
        print(f"Error initializing embedding model: {str(e)}")
        sys.exit(1)
    
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=args.chunk_size, 
        chunk_overlap=args.chunk_overlap,
        length_function=len, 
        is_separator_regex=False
    )
    
    # Find all PDF files in the directory
    pdf_files = glob.glob(os.path.join(args.pdf_directory, "*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in '{args.pdf_directory}'")
        sys.exit(1)
    
    print(f"Found {len(pdf_files)} PDF files in '{args.pdf_directory}'")
    
    # Process all PDFs and collect chunks
    all_chunks = []
    for pdf_file in pdf_files:
        chunks = process_pdf(pdf_file, text_splitter)
        all_chunks.extend(chunks)
    
    if not all_chunks:
        print("No chunks were generated from PDFs. Exiting.")
        sys.exit(1)
    
    print(f"Total chunks collected: {len(all_chunks)}")
    
    # Create the vector database directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    # Create or update the vector database
    print(f"Creating vector database in: {args.output}")
    try:
        vector_db = Chroma.from_documents(
            documents=all_chunks,
            embedding=embeddings_model,
            persist_directory=args.output
        )
        count = vector_db._collection.count()
        print(f"Successfully created vector database with {count} entries")
    except Exception as e:
        print(f"Error creating vector database: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 