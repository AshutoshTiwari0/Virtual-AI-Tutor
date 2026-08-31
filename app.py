import streamlit as st
from pathlib import Path

from src.pipelines.pipeline import study_pipeline


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Virtual AI Tutor",
    page_icon="🎓",
    layout="wide"
)


# ---------------- HEADER ----------------

st.title("🎓 Virtual AI Tutor")
st.caption("AI-powered study material generator")

st.divider()


# ---------------- INPUT ----------------

topic = st.text_input(
    "📚 Enter topic to study",
    placeholder="e.g. Convolutional Neural Networks"
)


# ---------------- START BUTTON ----------------

if st.button("🚀 Start Learning", type="primary", use_container_width=True):

    if not topic.strip():
        st.warning("⚠️ Please enter a topic first.")

    else:

        with st.spinner(
            "🤖 AI Tutor is researching, summarizing and preparing your study material..."
        ):

            result = study_pipeline(topic.strip())

        st.success("✅ Study material generated successfully!")

        st.divider()


        # =====================================================
        # SUMMARY
        # =====================================================

        st.header(f"📖 {topic.strip()}")

        st.subheader("📝 Exam-Oriented Notes")

        summary = result.get("summary", "")

        if summary:
            st.markdown(summary)
        else:
            st.info("No summary was generated.")


        # =====================================================
        # DOWNLOAD SECTION
        # =====================================================

        st.divider()

        st.subheader("📦 Your Study Material")

        col1, col2 = st.columns(2)

        # ---------- PPT ----------

        ppt_path = Path(result.get("ppt", "notes.pptx"))

        with col1:

            st.markdown("### 📊 PowerPoint Presentation")

            if ppt_path.exists():

                with open(ppt_path, "rb") as file:

                    st.download_button(
                        label="⬇️ Download PPT",
                        data=file,
                        file_name=f"{topic.strip()}_presentation.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        use_container_width=True
                    )

            else:
                st.warning("PPT file was not found.")


        # ---------- PDF ----------

        pdf_path = Path(result.get("pdf", "notes.pdf"))

        with col2:

            st.markdown("### 📄 PDF Notes")

            if pdf_path.exists():

                with open(pdf_path, "rb") as file:

                    st.download_button(
                        label="⬇️ Download PDF",
                        data=file,
                        file_name=f"{topic.strip()}_notes.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

            else:
                st.warning("PDF file was not found.")


        # =====================================================
        # YOUTUBE
        # =====================================================

        st.divider()

        st.subheader("🎥 Recommended YouTube Videos")

        yt_result = result.get("yt recommendations", "")

        if yt_result:
            st.markdown(yt_result)
        else:
            st.info("No YouTube recommendations available.")


        # =====================================================
        # RESEARCH CONTENT
        # =====================================================

        st.divider()

        with st.expander("🔬 View Research Content"):

            read_content = result.get("read_content", "")

            if read_content:
                st.markdown(read_content)
            else:
                st.info("No research content available.")


        # =====================================================
        # WEB SEARCH
        # =====================================================

        with st.expander("🌐 View Web Search Results"):

            search_result = result.get("search_result", "")

            if search_result:
                st.markdown(search_result)
            else:
                st.info("No web search results available.")