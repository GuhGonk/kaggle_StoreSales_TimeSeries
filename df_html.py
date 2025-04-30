from IPython.display import display, HTML

def display_dfs(dfs, titles=None, max_cols=3):
    n = len(dfs)
    if titles is None:
        titles = [f"DataFrame {i+1}" for i in range(n)]
    assert len(titles) == n, "Titles list must match number of DataFrames"
    rows = []
    for i in range(0, n, max_cols):
        row_dfs = dfs[i:i+max_cols]
        row_titles = titles[i:i+max_cols]
        html_row = "<div style='display: flex; gap: 25px; margin-bottom: 25px;'>"
        for df, title in zip(row_dfs, row_titles):
            html_row += f"<div><h4>{title}</h4>{df.to_html()}</div>"
        html_row += "</div>"
        rows.append(html_row)
    
    display(HTML("".join(rows)))