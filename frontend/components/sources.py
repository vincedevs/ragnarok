import streamlit as st


def render_sources(sources: list[dict]) -> None:
    """Render retrieved source locations and excerpts."""
    if not sources:
        return

    with st.expander("Retrieved Sources", expanded=False):
        for source in sources:
            with st.container(border=True):
                st.markdown(f"**📄 {source['filename']}**")
                page_number = source.get("page_number")
                location = (
                    f"Page {page_number}"
                    if page_number
                    else f"Chunk {source['chunk_index']}"
                )
                if source.get("section_heading"):
                    location += f" · {source['section_heading']}"
                if source.get("relevance_score") is not None:
                    location += f" · {source['relevance_score']:.0%} rank score"
                st.caption(location)
                if source.get("excerpt"):
                    st.write(source["excerpt"])
