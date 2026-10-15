"""Вкладка 'Зависимости'."""

import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from app.core.config import BIG_GRAPH_THRESHOLD


def render(G: nx.DiGraph):
    if G.number_of_nodes() == 0:
        st.info("Граф зависимостей пуст (нет Python-модулей с импортами).")
        return

    st.subheader(
        f"Граф зависимостей ({G.number_of_nodes()} модулей, "
        f"{G.number_of_edges()} связей)"
    )

    if G.number_of_nodes() <= BIG_GRAPH_THRESHOLD:
        pos = nx.spring_layout(G, k=0.6, iterations=60, seed=42)
    else:
        st.info(f"Граф большой ({G.number_of_nodes()} узлов) — раскладка упрощена.")
        pos = nx.spring_layout(G, k=0.3, iterations=15, seed=42)

    edge_x, edge_y = [], []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(width=0.6, color="#666"),
        hoverinfo="none",
    )

    node_x = [pos[n][0] for n in G.nodes()]
    node_y = [pos[n][1] for n in G.nodes()]
    degs = [G.degree(n) for n in G.nodes()]
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        marker=dict(
            size=[8 + 2 * d for d in degs],
            color=degs,
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title="Degree"),
            line=dict(width=1, color="#222"),
        ),
        text=list(G.nodes()),
        hoverinfo="text",
    )

    fig = go.Figure([edge_trace, node_trace])
    fig.update_layout(
        showlegend=False,
        height=650,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Наиболее зависимые модули (in-degree)**")
        indeg = sorted(G.in_degree, key=lambda x: x[1], reverse=True)[:10]
        st.dataframe(
            pd.DataFrame(indeg, columns=["Модуль", "Импортируется"]),
            use_container_width=True,
            hide_index=True,
        )
    with col2:
        st.markdown("**Модули с наибольшим числом зависимостей (out-degree)**")
        outdeg = sorted(G.out_degree, key=lambda x: x[1], reverse=True)[:10]
        st.dataframe(
            pd.DataFrame(outdeg, columns=["Модуль", "Импортирует"]),
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("**Циклические зависимости**")
    if G.number_of_nodes() < BIG_GRAPH_THRESHOLD:
        try:
            cycles = list(nx.simple_cycles(G))
            if cycles:
                st.warning(f"⚠️ Найдено циклических зависимостей: {len(cycles)}")
                with st.expander("Показать циклы"):
                    for c in cycles[:20]:
                        st.code(" → ".join(c + [c[0]]))
            else:
                st.success("Циклов не найдено 👍")
        except Exception:
            st.info("Не удалось выполнить поиск циклов.")
    else:
        st.info("Граф слишком большой — пропускаю поиск циклов.")
