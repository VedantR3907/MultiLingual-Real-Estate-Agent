
# Real Estate Chatbot

The chatbot is integrated with normal conversation from FAQ's, chatting with documents without Crewai agents, chatting with documents with crewai agents, Chatting with image with autodetection and custom language selection from English, French and German.


First git pull the following branch

Image-chatting-integration


### Installing requriements.txt
```
pip install requirements.txt
```

After this you might want to install some packages manually:

In the below installation the cuda version depends upon your graphics card, for me it was 11.8
https://pytorch.org/get-started/locally/
```
pip install "pinecone-client[grpc]"
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## Loaders

I have created 2 loaders PDF and weblink. For the PDF I am using pypdf loader and for weblinks I am using Crawl4ai loader for crawling weblinks in a markdown format.
Currently loaders have only been implemented in backend, for using loaders you might want to follow these steps:

1. First place all your files at the input directory which is at 
app/db/documents (Note for now it only supports pdf, I have created other loaders but due to time constraint I have only integrated pdf loader).

2. Run the below command to load the documents.

```
cd app/utils/loaders
python pdf_loader.py
```

3. The files are loaded into a text file inside the output directory which is at app/db/extracted_output

4. For loading weblinks you might need to go to app/utils/loaders/webloader.py

5. inside the webloader.py place the url you want to extract the data will be loaded to the output directory (same as pdf).

## Creating Embeddings and storing in vector database.

Due to time constraint I was not able to integrate this in frontend but you might need only to run a single file to store data in Pinecone vector store, You might need pinecone API key to do so.

1. Create a env file and get a pinecone api key from https://www.pinecone.io/ 

2. Then paste your pinecone key in the env file as following: 
```
PINECONE_API_KEY=a**********
```

3. Now for inserting documents inside vector database go to following path app/db/CRUD/insert_records.py

4. Scroll to the end where the main function is called inside asyncio, For inserting PDF documents write 'pdf' for inserting weblinks type 'weblinks'

5. Go to your pinecone console you will see a new index with name realestatebot and all the data has been stored there.

6. For deleting and updating records just pass the file name at the end of the files it will be deleted or updated accordingly.


## Using the Chatbot

1. Finally after doing this we will run our streamlit Using

2. NOTE: Before doing that you need to create a groq_api_key and gemini_api_key (gemini for image and groq for RAG). Finally pass those to env file as below:

```
GROQ_API_KEY=g**********************************
GEMINI_API_KEY=A*********************************
```

3. Finally run the following command
```
streamlit run app.py
```
