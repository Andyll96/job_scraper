TODO:
    - Clean DOM content using beautifulSoup
    - Parsing content to LLM, basically reducing it down to what the LLM can handle
    - Create prompt that LLM can consistently understand and return what I want. Must make sure that it returns data as dictionary of jobs
- Somehow I need to make sure that the previous dataset is updated accurately. I shouldn't change old records because if I link the entry to another database it might mess things up. Possibly implement an active property in database
- I need to push that data back out to notion, to the Job Postings Database

Note:
    - The intention of this project was to consolidate all job postings from Animation/VFX/Gaming studios in Canada
    - The code would retrieve the studio's career pages from a notion database.
    - Then scrape the html from each careers page and, using an LLM, analyze the html to output a dictionary of job postings
    - Using this dictionary it would push the data back out to notion 

Problems:
    - In order to scrape the website without having my ip address blocked, and to be able to solve CAPTCHAs, bright data's scraping browser was utilized
    - However this is a paid service and currently, for obvious reasons, is not economically viable
    - Will be pausing this development until alternative is determined