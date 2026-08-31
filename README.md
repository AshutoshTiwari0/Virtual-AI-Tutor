# 🎓 Virtual AI Tutor

An **agentic AI-powered study assistant** built with Python and LangChain that turns a topic into a complete study package — including research material, exam-oriented notes, YouTube recommendations, PowerPoint presentations, and PDF notes.

The project uses multiple specialized AI agents, with each agent responsible for a specific stage of the learning workflow.

## ✨ Features

* 🔎 **Web Research** — Searches the web for information related to the requested topic.
* 📚 **Research Paper Reading** — Extracts and processes relevant information from research papers.
* 🧠 **Exam-Oriented Notes & Summary** — Converts gathered information into concise study notes.
* 🎥 **YouTube Recommendations** — Finds relevant educational videos and filters recommendations based on views and recency.
* 📊 **Automatic PPT Generation** — Creates a structured PowerPoint presentation from the generated study material.
* 📄 **Automatic PDF Generation** — Generates PDF study notes from the summarized content.
* 🤖 **Specialized AI Agents** — Uses separate agents for research, reading, summarization, recommendations, PPT generation, and PDF generation.
* 🖥️ **Streamlit Interface** — Provides a simple web interface where users can enter a topic and generate the complete study package.

## 🧩 Architecture

The application follows a sequential multi-agent workflow:

```text
                    ┌─────────────────┐
                    │   User Topic    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Search Agent   │
                    │   Web Search     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Reader Agent   │
                    │ Research Papers │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Summary Agent   │
                    │ Notes + Summary │
                    └───────┬─┬───────┘
                            │ │
                ┌───────────┘ └───────────┐
                ▼                         ▼
      ┌─────────────────┐       ┌─────────────────┐
      │ YouTube Agent   │       │  PPT / PDF      │
      │ Recommendations │       │   Generation     │
      └─────────────────┘       └─────────────────┘
```

Each stage passes its output to the next stage through a shared pipeline state.

## 🤖 Agents

The project separates responsibilities into specialized agents:

| Agent            | Responsibility                                  |
| ---------------- | ----------------------------------------------- |
| 🔎 Search Agent  | Researches the requested topic using web search |
| 📖 Reader Agent  | Processes relevant research-paper information   |
| 📝 Summary Agent | Creates exam-oriented notes and summaries       |
| 🎥 YouTube Agent | Recommends relevant educational videos          |
| 📊 PPT Agent     | Generates a structured PowerPoint presentation  |
| 📄 PDF Agent     | Generates PDF study material                    |

The agents are constructed independently using LangChain's agent framework and can use different language models depending on the task.

## 🔧 Tools

The agents interact with dedicated tools for their individual tasks:

* `web_search`
* `read_research_papers`
* `recommend_youtube_urls`
* `notes_and_summary_generator`
* `ppt_generator`
* `pdf_generator`

This separation keeps the tool logic independent from the agent orchestration.

## 🔄 Pipeline

The main study pipeline follows these steps:

### 1. Topic Input

The user provides a topic such as:

```text
Convolutional Neural Networks
```

### 2. Web Research

The Search Agent gathers information relevant to the topic.

### 3. Research Reading

The Reader Agent processes relevant research content and extracts useful information, particularly from an exam/study perspective.

### 4. Summarization

The Summary Agent converts the gathered material into concise notes and a summary.

### 5. Video Recommendations

The YouTube Agent searches for educational videos and applies filtering based on:

* Minimum number of views
* Recency of publication

### 6. Study Material Generation

The summarized material is passed to:

* PPT Agent → PowerPoint presentation
* PDF Agent → PDF notes

### 7. Streamlit Output

The generated study material is presented through the Streamlit interface, including:

* Exam-oriented notes
* PPT download
* PDF download
* YouTube recommendations
* Research content
* Web-search results

## 🛠️ Tech Stack

* **Python**
* **LangChain**
* **LangChain Agents**
* **Groq / Google Gemini compatible LLM integrations**
* **Streamlit**
* **Pydantic**
* **YouTube Search**
* **PowerPoint generation**
* **PDF generation**
* **Web search**
* **Research paper processing**

## 📁 Project Structure

```text
Virtual-AI-Tutor/
│
├── app.py
├── main.py
│
└── src/
    ├── agents/
    │   └── agents.py
    │
    ├── pipelines/
    │   └── pipeline.py
    │
    └── tools/
        └── tools.py
```

### `app.py`

Contains the Streamlit interface and displays the generated study material.

### `src/agents/`

Contains functions responsible for creating the specialized agents.

### `src/pipelines/`

Contains the main orchestration logic that runs the agents sequentially and maintains the state between stages.

### `src/tools/`

Contains the actual tools used by the agents for searching, research-paper processing, YouTube recommendations, summarization, PPT generation, and PDF generation.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/AshutoshTiwari0/Virtual-AI-Tutor.git
cd Virtual-AI-Tutor
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the project root and add the API keys required by the tools and language-model provider you are using.

Example:

```env
MISTRAL_API_KEY=your_api_key
```

Do **not** commit your `.env` file or API keys to GitHub.

### 5. Run the Streamlit application

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## 🎯 Example Workflow

Input:

```text
Convolutional Neural Networks
```

The tutor can produce:

```text
🔎 Web Research
       ↓
📚 Research Content
       ↓
📝 Exam-Oriented Notes
       ↓
   ┌───┴────────────┐
   ↓                ↓
🎥 YouTube      📊 PPT + 📄 PDF
```

The goal is to reduce the effort required to collect, organize, and revise study material from multiple sources.

## 🧠 Why a Multi-Agent Approach?

Instead of asking one LLM call to perform every task, the project separates the workflow into specialized agents.

This provides:

* Clear separation of responsibilities
* Easier debugging
* Reusable tools
* Independent agent configuration
* Ability to use different models for different tasks
* Easier expansion of the system with additional capabilities

For example, a stronger model can be used for research-heavy tasks while a smaller/faster model can handle formatting and content-generation tasks.

## ⚠️ Project Status

This project is currently a **learning / portfolio project** focused on exploring:

* AI agents
* LangChain
* Tool calling
* Agent orchestration
* LLM-based content generation
* Automated study-material generation


## 🤝 AI-Assisted Development

AI tools were used during the development of this project.

Specifically, AI assistance was used for:

* Understanding and implementing some LangChain/LangGraph concepts
* Developing and refining individual tools
* Debugging errors and integration issues
* Troubleshooting API/model and library compatibility problems
* Improving prompts and structured outputs
* Iterating on the PPT/PDF generation workflow
* Getting guidance while designing parts of the agent architecture

The overall project idea, experimentation, integration, testing, debugging decisions, and implementation were iteratively developed by the author.

This disclosure is intentional: the project demonstrates **AI-assisted software development**, while the author remains responsible for integrating, testing, and understanding the resulting system.

## 👨‍💻 Author

**Ashutosh Tiwari**

Built as an exploration of agentic AI, LangChain, and AI-powered educational workflows.

⭐ If you find the project interesting, consider giving the repository a star.
