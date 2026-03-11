"""AI Resume + Cover Letter Generator Streamlit app."""

from __future__ import annotations

import os
from dataclasses import dataclass
from textwrap import dedent

import streamlit as st

from openai import OpenAI


@dataclass
class CandidateProfile:
    full_name: str
    email: str
    phone: str
    location: str
    linkedin: str
    portfolio: str
    summary: str
    skills: str
    experience: str
    education: str
    projects: str
    certifications: str


SYSTEM_PROMPT = dedent(
    """
    You are an expert career coach and technical writer.
    Generate concise, ATS-friendly documents tailored to the job description.
    Use action verbs, measurable impact, and clear formatting.
    """
).strip()


def build_user_prompt(profile: CandidateProfile, job_description: str, tone: str) -> str:
    """Build the user prompt sent to the language model."""
    return dedent(
        f"""
        Candidate Profile:
        - Full name: {profile.full_name}
        - Email: {profile.email}
        - Phone: {profile.phone}
        - Location: {profile.location}
        - LinkedIn: {profile.linkedin}
        - Portfolio: {profile.portfolio}
        - Professional Summary: {profile.summary}
        - Skills: {profile.skills}
        - Work Experience: {profile.experience}
        - Education: {profile.education}
        - Projects: {profile.projects}
        - Certifications: {profile.certifications}

        Job Description:
        {job_description}

        Desired Tone: {tone}

        Return output in two markdown sections:
        1) ## Resume (targeted, one page equivalent)
        2) ## Cover Letter (3-5 concise paragraphs)
        """
    ).strip()


def generate_with_openai(user_prompt: str, model: str) -> str:
    """Generate response with OpenAI chat completions API."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        temperature=0.5,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content or "No content returned from model."


def generate_fallback(profile: CandidateProfile, job_description: str) -> str:
    """Generate deterministic fallback output when no API key is provided."""
    jd_preview = " ".join(job_description.split())[:320]
    return dedent(
        f"""
        ## Resume

        **{profile.full_name}**  
        {profile.location} • {profile.phone} • {profile.email}  
        {profile.linkedin} • {profile.portfolio}

        ### Professional Summary
        {profile.summary}

        ### Core Skills
        {profile.skills}

        ### Experience Highlights
        {profile.experience}

        ### Projects
        {profile.projects}

        ### Education
        {profile.education}

        ### Certifications
        {profile.certifications}

        ---

        ## Cover Letter

        Dear Hiring Manager,

        I am excited to apply for this role. My background in {profile.skills.split(',')[0].strip() if profile.skills else 'relevant technologies'} and my experience delivering measurable outcomes align well with your needs.

        Based on your posting, I understand you are seeking someone who can contribute in areas like: "{jd_preview}..." I have delivered similar results by owning end-to-end execution, collaborating cross-functionally, and continuously improving quality.

        I would welcome the opportunity to bring my experience and problem-solving mindset to your team. Thank you for your time and consideration.

        Sincerely,  
        {profile.full_name}
        """
    ).strip()


def main() -> None:
    """Render the Streamlit UI."""
    st.set_page_config(page_title="AI Resume + Cover Letter Generator", page_icon="🧠", layout="wide")
    st.title("🧠 AI Resume + Cover Letter Generator")
    st.caption("Paste your details and a job description to generate a tailored resume and cover letter.")

    with st.sidebar:
        st.header("Model Settings")
        model = st.text_input("OpenAI model", value="gpt-4o-mini")
        tone = st.selectbox("Writing tone", ["Professional", "Confident", "Friendly", "Executive"])
        use_openai = st.toggle("Use OpenAI API (requires OPENAI_API_KEY)", value=bool(os.getenv("OPENAI_API_KEY")))

    left, right = st.columns(2)

    with left:
        st.subheader("Candidate Profile")
        full_name = st.text_input("Full name", value="Jane Doe")
        email = st.text_input("Email", value="jane.doe@email.com")
        phone = st.text_input("Phone", value="+1-555-123-4567")
        location = st.text_input("Location", value="Austin, TX")
        linkedin = st.text_input("LinkedIn", value="https://linkedin.com/in/janedoe")
        portfolio = st.text_input("Portfolio", value="https://janedoe.dev")
        summary = st.text_area("Professional summary", height=120, value="Results-driven software engineer with 6+ years building scalable web applications.")
        skills = st.text_area("Skills (comma separated)", height=80, value="Python, FastAPI, React, PostgreSQL, AWS, Docker")
        experience = st.text_area("Experience highlights", height=180, value="- Led migration to microservices reducing deployment time by 40%.\n- Built analytics dashboard improving retention by 18%.")
        education = st.text_area("Education", height=80, value="B.S. Computer Science, University of Texas at Austin")
        projects = st.text_area("Projects", height=100, value="- AI Resume Matcher: NLP app scoring resume-job fit.\n- Internal CI Optimizer reducing pipeline runtime by 30%.")
        certifications = st.text_area("Certifications", height=80, value="AWS Certified Developer – Associate")

    with right:
        st.subheader("Target Role")
        job_description = st.text_area(
            "Paste job description",
            height=460,
            value="We are hiring a Software Engineer to design and build cloud-native applications, collaborate with product and design, and improve platform reliability.",
        )

    profile = CandidateProfile(
        full_name=full_name,
        email=email,
        phone=phone,
        location=location,
        linkedin=linkedin,
        portfolio=portfolio,
        summary=summary,
        skills=skills,
        experience=experience,
        education=education,
        projects=projects,
        certifications=certifications,
    )

    if st.button("Generate Resume + Cover Letter", type="primary"):
        with st.spinner("Generating tailored documents..."):
            prompt = build_user_prompt(profile, job_description, tone)
            try:
                if use_openai:
                    result = generate_with_openai(prompt, model=model)
                else:
                    result = generate_fallback(profile, job_description)
            except Exception as exc:
                st.error(f"Generation failed: {exc}")
                return

        st.success("Done! Review and copy your documents below.")
        st.markdown(result)
        st.download_button(
            "Download as markdown",
            data=result,
            file_name=f"{profile.full_name.lower().replace(' ', '_')}_resume_cover_letter.md",
            mime="text/markdown",
        )


if __name__ == "__main__":
    main()
