import pandas as pd
import streamlit as st
from groq import Groq
from pandas import DataFrame
from ui import api_key_input, app_header, main_container


def model_df(groq_api_key):
    client = Groq(api_key=groq_api_key)

    models = client.models.list()

    data = [model.to_dict() for model in models.data]
    df = DataFrame(data)
    df["created"] = pd.to_datetime(df.created, unit="s").dt.strftime("%Y-%m-%d")
    sorted_df = df[df.active == True].sort_values(
        by=["created", "context_window"], ascending=False
    )[
        [
            "id",
            "created",
            "owned_by",
            "context_window",
            "max_completion_tokens",
        ]
    ]
    # change the column names to be more readable
    sorted_df.columns = [
        "Model ID",
        "Created",
        "Owned By",
        "Context",
        "Output Tokens",
    ]
    return st.dataframe(sorted_df, hide_index=True, use_container_width=True)


def body():
    c1, c2 = st.columns([3, 1], vertical_alignment="bottom")
    with c1:
        groq_api_key = api_key_input("Groq")

    c2.button(
        "Get Models",
        use_container_width=True,
        key="get-groq-models",
        disabled=not groq_api_key,
    )


def app():
    app_header(__name__)

    main_container(body)

    if st.session_state.get("get-groq-models"):
        st.write("")
        st.write("")
        st.markdown("#### ✨ &nbsp; Active Models")
        try:
            model_df(st.session_state["groq-api-key"])
        except Exception as e:
            st.error(e.__dict__["body"]["error"]["message"], icon="⚠️")
