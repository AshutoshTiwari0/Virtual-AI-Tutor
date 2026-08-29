from src.agents.agents import build_reader_agent,build_search_agent,recommend_yt_videos,make_pdf,make_notes_and_summary,make_ppt

def study_pipeline(topic:str)->dict:
    """Main pipeline for AI Tutor"""

    state={}

    #search agent is working now
    print("====Search Agent is working=====")
    search_agent=build_search_agent()
    search_result=search_agent.invoke({
        "messages":[("user",f"Search information about the mentioned {topic}")]
    })

    state["search_result"]=search_result['messages'][-1].content  #save each agent ka output taki ussi output ko next agent use kr pae

    print("search result is", state['search_result'])

    #now reader agent will work
    print("=======Reader Agent is Working==========")
    reader_agent=build_reader_agent()
    reader_result=reader_agent.invoke({
        "messages":[("user",f"Read information about the mentioned {topic}. Pick most relevant infromation for exams purposes."f"Search Results:\n{state['search_result'][:800]}")]
        })
    
    state['read_content'] = reader_result['messages'][-1].content

    print("\nscraped content: \n", state['read_content'])


    #now summariser agent will work
    print("=======Summariser Agent is Working==========")
    summary_agent=make_notes_and_summary()
    summary_result=summary_agent.invoke({
        "messages":[("user",f"Make notes and summary for {state['read_content']}")]
        })
    
    state['summary']=summary_result['messages'][-1].content
    print(summary_result)

    #now yt recommendations
    print("==========Recommendation youtube agent is working============")
    recommender_agent=recommend_yt_videos()
    recommender_output=recommender_agent.invoke({
        "messages":[("user",f"Recommend youtube videos for the mentioned topic {topic}")]
    })
    state['yt recommendations']=recommender_output['messages'][-1].content
    print(recommender_output)

    #make ppt and pdf for notes
    print("============PPT and PDF agent is working=============")
    ppt_agent = make_ppt()
    pdf_agent = make_pdf()

    ppt_output = ppt_agent.invoke({
        "messages": [
            (
                "user",
                f"Create a PPT for {topic} using these notes:\n{state['summary']}"
            )
        ]
    })

    pdf_output = pdf_agent.invoke({
        "messages": [
            (
                "user",
                f"Create a PDF for {topic} using these notes:\n{state['summary']}"
            )
        ]
    })

    state['ppt'] = ppt_output['messages'][-1].content
    state['pdf'] = pdf_output['messages'][-1].content

    return state