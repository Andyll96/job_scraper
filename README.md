TODO:
- Query Animation/VFX/Game Studio Directory Database
- get the current dataset
- For each entry look up the careers page property
    - navigate to each website
    - grab the HTML using selenium
        - must test out using bright.data to get the HTML without issues with blocking or captcha
    - Clean DOM content using beautifulSoup
    - Parsing content to LLM, basically reducing it down to what the LLM can handle
    - Create prompt that LLM can consistently understand and return what I want. Must make sure that it returns data as dictionary of jobs
- Somehow I need to make sure that the previous dataset is updated accurately. I shouldn't change old records because if I link the entry to another database it might mess things up
- I need to push that data back out to notion, to the Job Postings Database

LIBRARIES:
- notion api
- streamlit
    - front end
- langchain
- langchain_ollama
    - for OLLama LLM and prompts
- selenium
    - what allows me to run an instance of webdriver, either chrom or bright.data
- beautifulsoup4
    - cleaning DOM content
- lxml
- html5lib
- python-dotenv
