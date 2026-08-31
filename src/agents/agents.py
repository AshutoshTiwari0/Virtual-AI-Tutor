from src.tools.tools import ppt_generator,pdf_generator,notes_and_summary_generator,read_research_papers,recommend_youtube_urls,web_search
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI


load_dotenv()


llm_search = ChatGroq(
    model="llama-3.1-8b-instant"
)

llm_generation = ChatGroq(
    model="llama-3.1-8b-instant"
)

#search agent 
def build_search_agent():
    return create_agent(model=llm_search,tools=[web_search])

#reader agent
def build_reader_agent():
    return create_agent(model=llm_search,tools=[read_research_papers])

#recommend youtube videos
def recommend_yt_videos():
    return create_agent(model=llm_search,tools=[recommend_youtube_urls])

#make ppt
def make_ppt():
    return create_agent(model=llm_generation,tools=[ppt_generator])

#make pdf
def make_pdf():
    return create_agent(model=llm_generation,tools=[pdf_generator])

#make notes and summary
def make_notes_and_summary():
    return create_agent(model=llm_generation,tools=[notes_and_summary_generator])

