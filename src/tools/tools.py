#web search tavily tool for collecting relevant data
from langchain.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
import os
from rich import print
import json

from youtube_search import YoutubeSearch

load_dotenv()

tavily_api_key=os.getenv("TAVILY_API_KEY")

content=[]

@tool
def web_search(query)-> str:
    """
    Search the internet for given user query and collect relevant points which can be useful for teaching the mentioned topic.
    """
    tavily_client=TavilyClient(api_key=tavily_api_key)
    response=tavily_client.search(query)


    # print(response)
    for r in response['results']:
       content.append(r["content"])

    return content


recommendations=[]
@tool 
def recommend_youtube_urls(topic)-> str:
    """
    Recommend Youtube Videos for given topic. The video should have 1000+ views and within 1 year time 
    """ 
    results=json.loads(YoutubeSearch(topic,max_results=20).to_json()) #search for 20 videos on given topic. Filter videos having 1k+ views and less than 1 year upload time for relevancy

    for videos in results['videos']:
        if int(videos['views'].split(' views')[0].replace(',',''))>=1000 and checkRelevancy(videos['publish_time']):
            recommendations.append(videos)

    return recommendations
    
#function to check if the youtube video is a year old or less
def checkRelevancy(date:str)->bool:
    Date=date.split(" ")[0]
    relevancy=date.split(" ")[1]
    
    d=int(Date)

    if relevancy in ['weeks', 'week'] and d <= 4 \
or relevancy in ['days', 'day'] and d <= 7 \
or relevancy in ['month', 'months'] and d <= 12:
        return True
    
    return False




# search_res=web_search.invoke("What is Artificial Intelligence?")
# print("=========== search content ============")
# print(search_res)

print(recommend_youtube_urls.invoke("LangGraph"))