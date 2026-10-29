"""Streamlit user interface."""
import json
import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
st.set_page_config(page_title="AI Resume Parser", page_icon="📄", layout="wide")
st.title("AI-Powered Resume Parser")
st.write("Upload a PDF or DOCX resume to extract information using an LLM.")
uploaded = st.file_uploader("Choose resume", type=["pdf", "docx"])
if st.button("Extract Resume Information", type="primary", disabled=uploaded is None):
    try:
        with st.spinner("Extracting resume information..."):
            response = requests.post(
                f"{API_URL}/api/upload",
                files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type or "application/octet-stream")},
                timeout=120,
            )
        if not response.ok:
            st.error(f"Error {response.status_code}: {response.json().get('detail', 'Request failed')}")
        else:
            payload = response.json()
            resume = payload["resume"]
            st.success("Resume parsed successfully.")
            st.caption(f"Document ID: {payload['document_id']}")
            st.subheader("Contact Information")
            st.json(resume["contact_information"])
            st.subheader("Professional Summary")
            st.write(resume.get("professional_summary") or "Not provided")
            st.subheader("Work Experience")
            for item in resume.get("work_experience", []):
                with st.expander(f"{item.get('role') or 'Role'} — {item.get('company') or 'Company'}"):
                    st.write(f"Duration: {item.get('duration') or 'Not provided'}")
                    st.write("\n".join("- " + x for x in item.get("responsibilities", [])) or "Not provided")
            st.subheader("Education")
            st.dataframe(resume.get("education", []), use_container_width=True, hide_index=True)
            c1, c2 = st.columns(2)
            c1.subheader("Technical Skills")
            c1.write(", ".join(resume.get("technical_skills", [])) or "Not provided")
            c2.subheader("Soft Skills")
            c2.write(", ".join(resume.get("soft_skills", [])) or "Not provided")
            st.subheader("Certifications")
            st.write("\n".join("- " + x for x in resume.get("certifications", [])) or "Not provided")
            st.download_button("Download JSON", json.dumps(payload, indent=2),
                               file_name="parsed_resume.json", mime="application/json")
    except requests.RequestException:
        st.error("Cannot connect to FastAPI. Start the backend first.")
