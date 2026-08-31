#web search tavily tool for collecting relevant data
from langchain.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
import os
from rich import print
import json
from youtube_search import YoutubeSearch
import arxiv
from trafilatura import fetch_url, extract
from pypdf import PdfReader
import requests
from io import BytesIO

from fpdf import FPDF
from pptx_renderer import PPTXRenderer
from langchain_groq import ChatGroq



from pydantic import BaseModel, Field
from langchain.agents import create_agent


from pathlib import Path

load_dotenv()

tavily_api_key=os.getenv("TAVILY_API_KEY")
google_api_key=os.getenv("GOOGLE_API_KEY")


@tool
def web_search(query)-> str:

    """
    Search the internet for given user query and collect relevant points which can be useful for teaching the mentioned topic.
    """
    tavily_client=TavilyClient(api_key=tavily_api_key)
    response=tavily_client.search(query,max_results=2,search_depth="basic")

    results=[]
    # print(response)
    for r in response["results"]:
        title = r.get("title", "")
        content = r.get("content", "")

        results.append(
            f"Title: {title}\n"
            f"Content: {content[:1200]}"
        )

    return "\n\n---\n\n".join(results)


@tool 
def recommend_youtube_urls(topic)-> str:
    """
    Recommend Youtube Videos for given topic. The video should have 1000+ views and within 1 year time 
    """ 
    
    recommendations=[]


    try:
        results=json.loads(YoutubeSearch(topic,max_results=20).to_json()) #search for 20 videos on given topic. Filter videos having 1k+ views and less than 1 year upload time for relevancy
    except Exception as e:
        print("YouTube search failed:", e)
        return "Unable to fetch YouTube recommendations right now."
    

    for videos in results['videos']:
        if int(videos['views'].split(' views')[0].replace(',',''))>=1000 and checkRelevancy(videos['publish_time']):
            recommendations.append(videos)

    return recommendations
    
#function to check if the youtube video is a year old or less
def checkRelevancy(date:str)->bool:
    Date=date.split(" ")[0]
    relevancy=date.split(" ")[1]
    if "Streamed" in Date:
        return False
    
    if Date.endswith("y"):
        return False

    d=int(Date)

    if relevancy in ['weeks', 'week'] and d <= 4 \
or relevancy in ['days', 'day'] and d <= 7 \
or relevancy in ['month', 'months'] and d <= 12:
        return True
    
    return False




# search_res=web_search.invoke("What is Artificial Intelligence?")
# print("=========== search content ============")
# print(search_res)

# print(recommend_youtube_urls.invoke("LangGraph"))


#reader agent tool 
#searches research papers from arxiv
@tool
def read_research_papers(topic)->str:
    """
    Read research papers for the mentioned topic and gather information for it
    """
    # Construct the default API client.
    client = arxiv.Client()

    # Search for the 10 most relevant articles matching the keyword "topic."
    search = arxiv.Search(
    query = topic,
    max_results = 10,
    sort_by = arxiv.SortCriterion.Relevance
    )

        # `results` is a generator; you can iterate over its elements one by one...
    for r in client.results(search):
        # a url is "http://arxiv.org/abs/2608.23566v1" for pdf we need to replace each /abs/ with /pdf/
        url=r.pdf_url #now we have the pdf. Now extract it's content using pdf reader
        
        print(url)
        
        #download pdf
        response = requests.get(url)
        response.raise_for_status()

        # Create PDF reader from downloaded bytes
        reader = PdfReader(BytesIO(response.content))

        number_of_pages = len(reader.pages)

        print("Title:", r.title)
        print("Pages:", number_of_pages)

        # Extract text from every page
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text[:6000]


# research_paper_content.append(read_research_papers.invoke("machine learning for heart disease classification"))

# print(research_paper_content)


# @tool 
def notes_and_summary_generator(text):
    """Take the text provided and generate notes and summary for it. Use proper headings for notes introduction, methodology, result, summary, exam centric questions. Try to answer in less than 600 words"""
    model = ChatGroq(
        model_name="openai/gpt-oss-120b",max_tokens=800)

    text = text[:8000]

    response = model.invoke(
        f"""
Create concise exam-oriented notes from the following text.

Use these headings:
1. Introduction
2. Methodology
3. Results / Key Points
4. Summary
5. Exam-Centric Questions

Keep the response under 400 words.

TEXT:
{text}
"""
    )

    return response.content


# print(notes_and_summary_generator.invoke("""How to Train a Critic Stably and Efficiently\nHOW TOTRAIN ACRITICSTABLY       
# ANDEFFICIENTLY\nPenghui Qi1, Xiangxin Zhou 2, Wee Sun Lee 1\n1National University  
# of Singapore 2Tencent
# Hunyuan\n{penghuiq,leews}@comp.nus.edu.sg\nABSTRACT\nGroup-based reinforcement     
# learning methods such as GRPO for large language\nmodels avoid training a critic by
# sampling multiple responses for each prompt. A\nreliable critic could instead      
# estimate token-level advantages from one response,\nbut standard critic-based      
# training recipes are often unstable. We study this in-\nstability and
# developBest-Practice Critic Optimization (BPCO), a recipe that\ncombines DPPO,     
# value predictions bounded to the reward range, Monte Carlo\nvalue targets,
# unnormalized policy advantages, and length-adaptive generalized\nadvantage
# estimation. Because the critic is used only during training, BPCO can\nalso        
# condition it on reward-defining information, such as a reference answer or\ngrading
# rubric, that is hidden from the policy. Controlled experiments isolate the\neffect 
# of each design choice. Across mathematical reasoning tasks with models\nranging    
# from 1.5B parameters to 30B-A3B mixtures of experts, BPCO improves\na strong       
# critic-based baseline consistently, and matches or exceeds a group-based\nbaseline 
# while sampling one response per prompt. The same recipe also improves\nlearning    
# with rubric-based rewards. These results show that a carefully designed\ncritic    
# provides a reliable alternative to group-relative advantage estimation. Code\nis   
# available athttps://github.com/QPHutu/golden_critic.\n1 INTRODUCTION\nReinforcement
# learning (RL) has become a standard approach for improving the reasoning
# and\ninstruction-following abilities of large language models (LLMs) (Ouyang et    
# al., 2022; Guo et al.,\n2025; Qi et al., 2026a). Effective RL depends on assigning 
# credit to the sampled tokens (Sutton\n& Barto, 2018). Group-based methods such as  
# GRPO estimate this signal by sampling several\nresponses for each prompt and       
# comparing their rewards (Shao et al., 2024; Liu et al., 2025). This\napproach      
# avoids training a value function, but it uses multiple rollouts per prompt and     
# assigns the\nsame outcome-based advantage to every token in a response.\nA learned 
# critic offers a direct alternative (Schulman et al., 2017). By estimating the      
# expected return\nof each response prefix, a critic can construct token-level       
# advantages from one rollout (Schulman\net al., 2015; Hou et al., 2026). In
# practice, however, critic-based LLM training remains fragile.\nPPO’s ratio clipping
# treats low- and high-probability tokens unevenly (Qi et al., 2026b).
# Boot-\nstrapped value targets can inherit critic error (Yuan et al., 2025), and a  
# fixed GAE parameter gives\nthe terminal reward very different weights in short and 
# long responses (Yue et al., 2025). We iden-\ntify two additional mismatches in     
# common implementations. First, a linear value head can predict\noutside the known  
# range of the return. Second, batch-wise advantage normalization forces every\nbatch
# to have unit-scale advantages, even when the residual policy signal has become     
# small. Our\ncontrolled study shows that both choices can destabilize training.\nA  
# critic also creates an opportunity that group-relative estimators do not directly  
# exploit. Because\nthe critic is discarded after training, it may receive
# reward-defining information that is unavailable to\nthe policy. Examples include a 
# reference answer or official solution in mathematical reasoning and
# a\nprompt-specific rubric in open-ended evaluation. Such information is determined 
# by the prompt and\ntherefore does not change the ideal value function. Presenting  
# it explicitly can nevertheless make that\nfunction easier to approximate, without  
# changing the policy’s inputs or deployment requirements.\nWe combine these choices 
# into Best-Practice Critic Optimization (BPCO), a single-rollout actor–\ncritic     
# recipe. BPCO uses DPPO to define clipping in terms of the sampled token’s
# probability\n1\narXiv:2608.23566v1  [cs.LG]  24 Aug 2026How to Train a Critic      
# Stably and Efficiently\nchange. It bounds value predictions to the reward range and
# trains the critic directly on observed\noutcomes. For the policy update, it        
# preserves the scale of the raw advantages and adapts the GAE\nparameter to response
# length. BPCO can additionally use reward-defining information as privileged\ncritic
# input when such information is available. Together, these choices align the        
# critic’s output,\ntarget, and inputs with the policy signal it produces.\nWe       
# develop the recipe incrementally in a controlled sanity test (Section 3), where    
# failure to fit a\nsmall, solvable dataset reveals optimization problems. We then   
# evaluate BPCO on a 40.3K-problem\nmathematical dataset (Section 4.1), two 30B-A3B  
# mixture-of-experts models (Section 4.2), and a\nrubric-reward task (Section 4.3).  
# The experiments support three findings. First, BPCO improves the\ncritic-based     
# baseline across model and dataset scales. Second, privileged information can       
# accelerate\ncritic learning, but its policy benefit depends on the task and the    
# degree of overfitting. Third, BPCO\nmatches or exceeds a group-based baseline while
# using one response per prompt. These results\nestablish a practical recipe for     
# single-rollout critic-based LLM RL.\n2 BACKGROUND\n2.1
# PROXIMALPOLICYOPTIMIZATION\nGiven a promptx, a language model with
# parametersθgenerates a responsey= (y 1, . . . , yT )\nautoregressively. At stept,  
# the state is the prefixs t = (x, y<t), the action is the next tokeny t, and\nthe   
# policy isπ θ(yt |s t). We consider outcome rewards: a completed response receives a
# scalar\nrewardR(x, y), and all intermediate rewards are zero.\nProximal Policy     
# Optimization (PPO) uses a clipped surrogate objective (Schulman et al., 2017).     
# Let\nµbe the behavior policy that generated the rollouts, and define sampled-token 
# probability ratio as\nρt(θ) = πθ(yt |s t)\nµ(yt |s t) .\nGiven an advantage        
# estimate bAt, PPO maximizes\nLPPO(θ) =E t\nh\nmin\n\x10\nρt(θ)bAt,clip(ρ t(θ),1−ϵ,1
# +ϵ) bAt\n\x11i\n.(1)\nThe clipped term removes the incentive to move the
# sampled-token ratio farther beyond the clipping\nboundary in the direction favored 
# by bAt, forming a trust region to stabilize training.\n2.2 
# DIVERGENCEPROXIMALPOLICYOPTIMIZATION\nPPO applies the same ratio threshold to every
# token. In a large vocabulary, this rule clips small\nabsolute changes to
# low-probability tokens while allowing much larger absolute changes to
# high-\nprobability tokens (Qi et al., 2026b). Divergence Proximal Policy
# Optimization (DPPO) instead\ndefines the clipping boundary in terms of the sampled 
# token’s probability change. The binary total-\nvariation variant used in this work 
# replacesϵin Equation (1) withϵ/µ(y t |s t):\nLDPPO(θ) =E
# t\n\x14\nmin\n\x12\nρt(θ)bAt,clip\n\x12\nρt(θ),1− ϵ\nµ(yt |s t) ,1 + ϵ\nµ(yt |s    
# t)\n\x13\nbAt\n\x13\x15\n.(2)\nEquivalently, DPPO constrains the probability shift 
# of the sampled token under the policy update,\ni.e.,|π θ(yt |s t)−µ(y t |s t)| ≤ϵ. 
# This gives sampled tokens a common absolute-probability\nthreshold rather than a   
# common ratio threshold.\n2.3 CRITIC-BASEDMETHODS\nCritic-based methods estimate the
# expected return of each prefix. For rollouts fromµ, the value\nfunction is\nV µ(st)
# =E µ[R(x, y)|s t],\nand the criticV ϕ(st)approximates this quantity. Letϕ old      
# denote the frozen critic parameters used to\nconstruct targets. Generalized        
# advantage estimation (GAE) (Schulman et al., 2015) first computes\n2How to Train a 
# Critic Stably and Efficiently\ntemporal-difference residuals and then forms an     
# exponentially weighted sum:\nδt =r t +γV ϕold(st+1)−V ϕold(st),(3)\nbAGAE(λ)\nt    
# =\nT−tX\nl=0\n(γλ)lδt+l.(4)\nHerer t = 0fort < T,r T =R(x, y), andV ϕold(sT+1 ) =  
# 0. The discount factor isγ, andλcontrols\nthe degree of bootstrapping. Smallerλcan 
# reduce variance but makes the estimate more sensitive\nto critic error. Withγ=     
# 1andλ= 1, the sum telescopes toR(x, y)−V ϕold(st)and contains no\nbootstrapped     
# value target.\nMany implementations construct the critic target as\nbVt(λ) =       
# bAGAE(λ)\nt +V ϕold(st)(5)\nand minimize\nLV(ϕ) =E t\n\x14\x10\nVϕ(st)−
# bVt(λ)\n\x112\x15\n.(6)\nThe policy update uses bAGAE(λ)\nt in Equation (1) or     
# Equation (2). In outcome-reward LLM training,\nγ= 1is commonly used.\n2.4
# GROUP-BASEDMETHODS\nGroup-based methods avoid a critic by samplingGresponses{y     
# (i)}G\ni=1 for each prompt (Shao et al.,\n2024). LetR i =R(x, y (i)), and letµ R   
# andσ R be the mean and standard deviation of theGrewards.\nGRPO assigns every token
# in responseithe advantage\nbAGRPO\nt,i = Ri −µ R\nσR\n.(7)\nDr. GRPO removes the   
# standard-deviation normalization, which can otherwise reweight prompts\naccording  
# to their within-group reward variance (Liu et al., 2025). Its advantage
# is\nbADr.GRPO\nt,i =R i −µ R.(8)\n3 BUILDINGBPCO: A CONTROLLEDSTUDY\nWe begin from 
# a verl commit from June 16, 2026 and study critic stability in a controlled        
# sanity\ntest (Qi et al., 2025; 2026b). We fine-tune DeepSeek-R1-Distill-Qwen-1.5B  
# (Guo et al., 2025) on\n1,460 mathematical problems that the initial model can      
# solve. A suitable training recipe should fit\nthis deliberately small dataset to   
# nearly 100% reward. Failure to do so exposes an optimization\nproblem rather than a
# lack of model capacity or reward signal.\nEach iteration contains 1,024
# trajectories. We use a minibatch size of 256 and one optimization\nepoch, giving   
# four optimizer minibatches per iteration. Following the verl defaults (Sheng et    
# al.,\n2025), the policy and critic learning rates are10 −6 and10 −5, respectively. 
# We observed no benefit\nfrom critic warm-up in this small-data setting and
# therefore update the policy and critic from the first\niteration."""
# )
# )



@tool
def pdf_generator(text):
    """takes text and generates pdf"""

    # Replace problematic unicode chars with latin-1 safe equivalents
    replacements = {
        '\u2013': '-',   # en-dash
        '\u2014': '--',  # em-dash
        '\u2018': "'",   # left single quote
        '\u2019': "'",   # right single quote
        '\u201c': '"',   # left double quote
        '\u201d': '"',   # right double quote
        '\u2022': '-',   # bullet
        '\u2026': '...', # ellipsis
    }
    for uni_char, ascii_char in replacements.items():
        text = text.replace(uni_char, ascii_char)
    
    # Fallback: strip any remaining non-latin1 chars
    text = text.encode('latin-1', 'ignore').decode('latin-1')


    pdf = FPDF()

    pdf.set_margins(15, 15, 15)
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 8, text)

    BASE_DIR = Path(__file__).resolve().parent

    output_path = BASE_DIR / "notes.pdf"

    pdf.output(str(output_path))

    return str(output_path) 

#works perfectly hehe
#pdf_generator.invoke("""Machine-learning-based anomaly detection is increasingly used in industrial control systems (ICS), yet most studies assume that detector training data is trustworthy. In practice, training data may be corrupted through compromised logs, labeling errors, manipulated historian records, or unsafe retraining processes. This paper evaluates the robustness of offline ICS anomaly-detection pipelines on the Secure Water Treatment (SWaT) benchmark under training-time contamination. We assess 11 heterogeneous anomaly detectors under three contamination strategies: random injection, similarity-targeted injection, and feature-noise injection. The first two insert attack samples into the nominal training pool, while the third adds bounded Gaussian noise to selected normal training samples. These attacks are contamination-based rather than gradient-driven poisoning methods. Contamination budgets from 1% to 10% are evaluated using clean validation and test sets under a unified offline protocol. The results show that robustness is strongly model-dependent and cannot be predicted from clean-data performance alone. Injection-based contamination causes the greatest degradation, particularly for local-density and distance-based detectors, whereas feature-noise contamination has a comparatively limited effect. PCA, SVM, HBOS, and IForest remain relatively stable, while the tuned neural detectors demonstrate intermediate robustness. Overall, the findings highlight the importance of training-data integrity in ML-enabled ICS monitoring, subject to the evaluated dataset, models, and threat assumptions.""")


class PPT(BaseModel):
    heading: str = Field(description="Short title of the topic")
    introduction: str = Field(description="Short introduction")
    core_concept: str = Field(description="Main concepts in simple words")
    methodology: str = Field(description="Main methods or working steps")
    examples: str = Field(description="Important examples")
    advantages: str = Field(description="Main advantages")
    limitations: str = Field(description="Main limitations")
    key_takeaways: str = Field(description="Important points to remember")
    exam_questions: str = Field(description="Short exam questions")

def clean_text(text):
    if isinstance(text, str):
        return text.encode("latin-1", "replace").decode("latin-1")

    elif isinstance(text, list):
        return [clean_text(item) for item in text]

    elif isinstance(text, dict):
        return {
            key: clean_text(value)
            for key, value in text.items()
        }

    return text


@tool
def ppt_generator(content:str):
    """Generate a PowerPoint presentation from plain study material.

    The input must be plain text study notes.
    Do NOT provide JSON, slide objects, dictionaries,
    lists, or pre-structured PPT content.

    The function itself will organize the material
    into the required PPT slides.
    
    """
    content = str(content)[:4000]
    # Initialize Groq LLM
    llm = ChatGroq(
        model_name="openai/gpt-oss-20b",
        temperature=0.3,
        max_tokens=4000
    )

    #agent for getting output in correct fornat
    agent = create_agent(
    model=llm,
    response_format=PPT  # Auto-selects ProviderStrategy
    )

    content=str(content)[:4000]


    result = agent.invoke({
    "messages": [{"role": "user", "content": f"""
                Extract and organize the important study information
                from the following material.

                Create content suitable for an educational PPT.
            
            IMPORTANT:
            - Do not use LaTeX.
            - Do not use formulas.
            - Do not use special mathematical symbols.
            - Use simple plain English.
            - Keep every field short.
            - Fill every field in the PPT schema.

                Study material:
                {content} """}]
    })

    print(result["structured_response"])

    ppt_data = result["structured_response"]

    variables = {
        "topic_name": ppt_data.heading,
    "introduction": ppt_data.introduction,
    "core_concept": ppt_data.core_concept,
    "methodology": ppt_data.methodology,
    "examples": ppt_data.examples,
    "advantages": ppt_data.advantages,
    "limitations": ppt_data.limitations,
    "key_takeaways": ppt_data.key_takeaways,
    "exam_questions": ppt_data.exam_questions
    }

    variables = clean_text(variables)

    # renderer = PPTXRenderer(
    # r"C:\Users\Dell\Desktop\Generative AI\LangGraph\Virtual AI Tutor\src\tools\template.pptx")

    # output_path = "notes.pptx"

    # renderer.render(output_path, variables)

    # return output_path

    BASE_DIR = Path(__file__).resolve().parent
    template_path = BASE_DIR / "template.pptx"

    renderer = PPTXRenderer(str(template_path))

    output_path = BASE_DIR / "notes.pptx"

    renderer.render(str(output_path), variables)

    return str(output_path)


# ppt_generator.invoke("""Optimization) enables stable, single-rollout actor-critic RL training for Large Language Models (LLMs).",\n "It matches or exceeds multi-sample group-based methods (like GRPO) while using only 1 response per prompt.",\n "Introduces a suite of 6 targeted engineering and algorithmic fixes to overcome standard PPO instabilities."\n ],\n "Core Concepts": [\n "Identifies 5 root failure modes in standard LLM PPO: ratio clipping flaws, bootstrapping errors, fixed GAE mismatches, unbounded value heads, and advantage normalization noise.",\n "Token-level advantage estimation provides fine-grained credit assignment across generated responses.",\n "Privileged critic design utilizes ground-truth reference data during training without modifying policy inference."\n ],\n "Methodology": [\n "Divergence PPO (DPPO): Constrains absolute probabiliy shifts rather than probability ratios to avoid over-clipping low-probability tokens.",\n "Bounded Value Head & MC Targets: Binds critic predictions to valid reward ranges (e.g., via sigmoid/tanh) and uses full-episode targets to prevent error propagation.",\n "Length-Adaptive GAE & Unnormalized Advantages: Scales lambda based on response length T and removes batch advantage normalization to preserve raw signal."\n ],\n "Application": [\n "Targeted at reinforcement learning alignment for LLMs on mathematical reasoning and rubric-following tasks.",\n "Proven scalable across diverse architectures, from small 1.5B parameter models up to 30B Mixture-of-Experts (MoE) models.",\n "Used strictly during training; the critic is discarded afterward, maintaining standard inference inputs."\n ],\n "Advantages and Limitations": [\n "Advantage: Significantly higher rollout efficiency, needing only 1 response per prompt instead of G >= 4 samples.",\n "Advantage: Combines the stability of group-based methods with the fine-grained credit assignment of token-level critics.",\n "Limitation: Requires memory and compute overhead to maintain a separate critic model during the training phase."\n ],\n "Summary": [\n "BPCO stabilizes single-rollout actor-critic RL for LLMs using six key algorithmic adjustments.",\n "Proves that regularized token-level critics are a compute-efficient alternative to multi-sample group-relative estimators.",\n "Delivers state-of-the-art RL efficiency and performance across varied model sizes and reasoning domains.""")






# print(web_search.invoke("machine learning"))