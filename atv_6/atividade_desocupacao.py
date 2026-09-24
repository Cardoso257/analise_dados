import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------------
# 1) Abrir as duas Tabelas 5 (2012 e 2026)
# ---------------------------------------------------------------
# Os arquivos usam ";" como separador, vírgula como separador decimal
# e vêm com um "BOM" no início do arquivo -> por isso encoding="utf-8-sig"
t2012 = pd.read_csv(
    "Tabela5-sem_emprego_2012.csv",
    sep=";",
    decimal=",",
    encoding="utf-8-sig",
)

t2026 = pd.read_csv(
    "Tabela5-sem_emprego_2026.csv",
    sep=";",
    decimal=",",
    encoding="utf-8-sig",
)

# Renomeia as colunas de valores para nomes curtos e únicos por ano,
# assim dá pra usar exatamente os nomes do exemplo (mulheres_2012, mulheres_2026...)
t2012 = t2012.rename(columns={
    "Desocupados - homens (2012 T1)": "homens_2012",
    "Desocupados - mulheres (2012 T1)": "mulheres_2012",
})

t2026 = t2026.rename(columns={
    "Desocupados - homens (2026 T1)": "homens_2026",
    "Desocupados - mulheres (2026 T1)": "mulheres_2026",
})

# ---------------------------------------------------------------
# 2) Juntar as duas tabelas (merge)
# ---------------------------------------------------------------
comp = t2012.merge(t2026, on=["Sigla", "Código", "Estado"], how="inner")

# ---------------------------------------------------------------
# 3) Preparar os dados para o gráfico
# ---------------------------------------------------------------
# Ordena os estados pela participação das mulheres em 2026 (do maior para o menor)
ordem = comp.sort_values("mulheres_2026", ascending=False)["Estado"]

# "Derrete" o dataframe: pega as colunas mulheres_2012 e mulheres_2026
# e transforma em duas colunas: "Ano" e "Participacao_mulheres"
longo = comp.melt(
    id_vars=["Sigla", "Código", "Estado"],
    value_vars=["mulheres_2012", "mulheres_2026"],
    var_name="Ano",
    value_name="Participacao_mulheres",
)
longo["Ano"] = longo["Ano"].map({"mulheres_2012": "2012 T1", "mulheres_2026": "2026 T1"})

# ---------------------------------------------------------------
# 4) Fazer o gráfico
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 10))

sns.barplot(
    data=longo,
    y="Estado",
    x="Participacao_mulheres",
    hue="Ano",
    order=ordem,
    ax=ax,
)

ax.axvline(50, color="red", linestyle="--", linewidth=1)
ax.set_xlabel("Participação das mulheres entre as pessoas desocupadas (%)")
ax.set_ylabel("")
ax.set_title("Desocupação: participação feminina em 2012 T1 e 2026 T1")
ax.legend(title="Ano")
fig.tight_layout()
plt.show()
