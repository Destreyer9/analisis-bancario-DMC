import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


st.sidebar.title("Modulos")

modulo = st.sidebar.selectbox("Seleccione un modulo",["Home","Carga del dataset","Análsis Exploratorio de Datos (EDA)"])

if modulo == "Home":
    st.title ("Título del proyecto: Análisis de datos bancarios Factores Aceptación de Campañas")
    st.subheader("Objetivo")
    objetivo = "Entender los factores que influyen en la aceptación de sus campañas de marketing de la empresa del sector Financiero"
    st.write(objetivo)

    with st.container():
        st.subheader("Datos de Autor")
        st.write("Nombre: Mauricio Alonso Paredes Mejia")
        st.write("Curso: Python for Analytics")
        st.write("Año: 2026")
    st.subheader("Detalle del Dataset")
    st.write("Dataset contiene la información de clientes de una institución financiera, con el fin de averiguar los factores que influyen en la aceptación de una campaña generada. El dataset incluye información demográfica, así como información de indices del cliente y detalles de contactos previos")
    st.subheader("Tecnología empleada")
    st.write("Streamlit,Pandas,Python,etc")
elif modulo == "Carga del dataset":

    try: 
        carga = st.file_uploader("Sube un CSV", type=["csv"])
        df=pd.read_csv(carga, sep=";")
        st.write("Se ingreso el archivo correctamente")
        df2=pd.DataFrame(df)
        st.write(df2.head())
        dimensión = df2.shape
        st.write("Dimensiones del Dataset")
        col1, col2 = st.columns(2)
        col1.metric("Líneas", df.shape[0])
        col2.metric("Columnas", df.shape[1])
        st.session_state["df2"] = df2
    except: "No se ingreso un archivo correctamente"
    
elif modulo == "Análsis Exploratorio de Datos (EDA)":
        if "df2" not in st.session_state:
            st.warning("⚠️ Primero debes cargar un dataset")
        else:
            df2 = st.session_state["df2"]
            df2=pd.DataFrame(df2)
            Ventanas=["Item 1 & 2","Item 3 & 4","Item 5 & 6","Item 7 & 8","Item 9 & 10"]
        tab1, tab2, tab3, tab4, tab5= st.tabs(Ventanas)
        with tab1:
            col1,col2 = st.columns(2)
            with col1:
                st.title("📄Información general del dataset")
                st.subheader("Info")
                st.write(df2.info())
                st.subheader("Tipos de datos")
                st.write(df2.dtypes)
                st.subheader("Conteo de valores nulos")
                st.write(df2.isna().sum())
            with col2:
                st.title("Clasificación de variables")
                st.subheader("Tipos de variables")
                numeric_cols = df2.select_dtypes(include="number").columns
                st.write("Numericas",numeric_cols)
                catego_cols = df2.select_dtypes(include="object").columns
                st.write("categoricas",catego_cols)
                def marcar_doble_credito(df2):
                    df3 = df2.copy()
                    df3["marcar_doble_credito"] = ((df3["loan"] == "yes") & (df3["housing"] == "yes")).astype(int)
                    return df3
                a=marcar_doble_credito(df2)
                st.write("Función que marca clientes de doble desembolso (Crédito Loan y Housing)")
                st.write(a.head())
                contar=a["marcar_doble_credito"].sum()
                st.write("Número de clientes que han tenido un doble desembolso Housing + Loan",contar)
        with tab2:
            col1,col2 = st.columns(2)
            with col1:
                st.title("Estadística descriptiva")
                st.subheader("Desribe()")
                st.write(df2.describe())

                class Estadisticas:
                        def __init__(self, df2: pd.DataFrame):
                            self.df2 = df2

                        def numericas(self):

                            return self.df2.select_dtypes(include="number").describe().T
                        def categoricas(self):
                            data = {}

                            for col in self.df2.select_dtypes(include=["object", "category"]):
                                serie = self.df2[col]
                                data[col] = {
                                    "conteo": serie.count(),
                                    "unicos": serie.nunique(),
                                    "moda": serie.mode().iloc[0] if not serie.mode().empty else None
            }
                            return pd.DataFrame(data).T
                        
                columnas_totales = df2.columns

                columna = st.selectbox(
                "Selecciona una columna",
                df2.columns)

                aplicacion=Estadisticas(df2[[columna]])

                if df2[columna].dtype in ["object","category"]:
                    st.dataframe(aplicacion.categoricas())
                else:
                    st.dataframe(aplicacion.numericas())

                st.title("interpretación básica media, mediana y dispersión")
                st.write("Se analiza algunas de las métricas principales númericas") 
                st.subheader("Edad")
                st.write("El promedio de edad de los clientes es 40, con una mediana de 38, indica que la distribución de edad de los clientes es símetrica teniendo la mayoría de los clientes entre 30 y 50 años acorde a la dispersión de 10")
                st.subheader("Duración de contacto")
                st.write("El promedio de 258 segundos con una desviación de 259 indica una alta variación de tiempos de contacto, la mediana nos muestra que una gran cantidad de clientes se atienden por debajo del promedio, indicando que existen clientes que tienen tiempos de contactos muy superiores al promedio generando la dispersión")
                st.subheader("campaña")
                st.write("El promedio de contactos es 2, similar a la mediana, indicando simetría; sin embargo, al tener una dispersión alta indica que hay una gran cantidad de clientes con 0 a 1 contactos, así como de 3 a 4")
                st.subheader("pdays")
                st.write("las medidas nos indican que casi todos los clientes llevan más de 900 días sin contactar")
                st.subheader("previous")
                st.write("las medidas nos indican que a excepción de unos cuantos, casi ningún cliente habia sido contactado previamente")
                st.subheader("Emp Var Rate")
                st.write("las medida nos indican que la tasa de variación de empleo es similar entre la mediana y el promedio; sin embargo, la distribución nos muestra que el promedio se reduce por los datos atípicos por debajo el P25 mientras que existe una alta concentración entre 1.1 y 1.4 de tasa de variación, significa que la mayoría de los clientes tiene una variación de empleo mayor a 1")
                st.subheader("Cons Price idx")
                st.write("las medidas nos indican que los precios al consumidor son iguales para todos los clientes del banco, debido a que la mediana y la media son iguales, y la desviación es menor a 1")
            with col2:
                st.title("Análisis valores faltantes")
                st.write(df2.isna().sum())
                st.subheader("discusión")
                st.write("El caso actual no presenta variables o valores nulos dentro de las bases de clientes, por lo que no debe imputarse datos o eliminar datos para entender el problema de negocio")
        with tab3:
            col1,col2=st.columns(2)
            with col1:
                st.title("Distribución de variables númericas")
                bins = st.slider("Bins", 5, 50, 20)
                col = st.selectbox("Selecciona variable numérica", numeric_cols)
                fig, ax = plt.subplots(figsize=(10,20))
                sns.histplot(df2[col], bins=bins, kde=True, ax=ax)
                st.pyplot(fig)
                st.subheader("Analizando Age")
                st.write("Se observa que una gran cantidad de clientes se concetran entre los 25 y 40 años, con una menor concentración entre 20 a 25 y entre 40 y 60. De esta forma, podemos concluir que la entidad financiera posee 3 grupos marcados de tipos de clientes, y algunos rangos atípicos de 20 a menos y de 60 a más")
            with col2:
                st.title("Análisis de variables categóricas")
                st.subheader("Conteos de unicos")
                st.write(df2[catego_cols].describe())
                coll=st.selectbox("Selecciona variable categórica", catego_cols)
                fag, ax = plt.subplots(figsize=(10, 10))
                sns.countplot(data=df2, x=coll, ax=ax)
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
                st.pyplot(fag)
                porcentaje = df2[coll].value_counts(normalize=True) * 100
                st.write(porcentaje.round(2))
                st.bar_chart(porcentaje)
        with tab4:
            col1,col2=st.columns(2)
            with col1:
                st.title("Análisis bivariado (numérico vs categórico)")
                st.subheader("Age Vs Y")
                fig, ax = plt.subplots()
                df2.boxplot(column="age", by="y", ax=ax)
                ax.set_title("Age per final decision distribution")
                ax.set_xlabel("Took campaign")
                ax.set_ylabel("Age")

                st.pyplot(fig)
                
                st.subheader("Duration Vs Y")
                durationvsY= df2.groupby("y")["duration"].mean()
                fig, ax = plt.subplots()
                durationvsY.plot(kind="bar",ax=ax)
                ax.set_xlabel("Took campaign")
                ax.set_ylabel("Contact duration")
                ax.set_title("Mean contact duration per decision distribution")
                st.pyplot(fig)

            with col2:
                
                st.title("Análisis bivariado (categórico vs categórico)")
                st.subheader("Day_of_week Vs Y")
                Day_of_weekVsY = pd.crosstab(df2["day_of_week"], df2["y"])

                fig, ax = plt.subplots()
                Day_of_weekVsY.plot(kind="bar", ax=ax)

                ax.set_xlabel("day_of_week")
                ax.set_ylabel("Yes or No")
                ax.set_title("Day_of_week Vs Decision")

                st.pyplot(fig)
                st.subheader("Campaign Vs Y")
                campaign_filtered=df2[df2["campaign"]< 5]

                campaignVsY = pd.crosstab(campaign_filtered["campaign"], campaign_filtered["y"])

                fig, ax = plt.subplots()
                campaignVsY.plot(kind="bar", ax=ax,figsize=(10,10))

                ax.set_xlabel("Times contacted on current campaign")
                ax.set_ylabel("Yes or No")
                ax.set_title("campaign Vs Decision")
                st.pyplot(fig)

        with tab5:
            col1,col2=st.columns(2)
            with col1:
                st.title("Análisis basado en parámetros seleccionados")
                cat_col1 = st.selectbox("Category column1", df2.select_dtypes("object").columns)
                cat_col2 = st.selectbox("Category column2", df2.select_dtypes("object").columns)

                if cat_col1 == cat_col2:
                    st.warning("Análisis bivariado misma columna")
                    st.stop()

                categories = df2[cat_col1].dropna().unique().tolist()

                selected_cats = st.multiselect(
                    "Select categories",
                    categories,
                    default=categories
                )

                df_filtered = df2[df2[cat_col1].isin(selected_cats)]

                counts = pd.crosstab(df_filtered[cat_col1], df_filtered[cat_col2])

                fig, ax = plt.subplots()
                counts.plot(kind="bar", ax=ax)

                ax.set_xlabel(cat_col1)
                ax.set_ylabel(cat_col2)
                ax.set_title(f"{cat_col1} vs {cat_col2}")


                st.pyplot(fig)

                cat_col = st.selectbox(
                "Categorical column",
                df2.select_dtypes(include="object").columns
                )

                num_col = st.selectbox(
                "Numeric column",
                df2.select_dtypes(include="number").columns
                )

                df_plot = (
                    df2.dropna(subset=[cat_col, num_col])
                    .groupby(cat_col)[num_col]
                    .mean()
                    .sort_values(ascending=False)
                )

                st.bar_chart(df_plot)
            
            with col2:
                st.title("Hallazgos clave")
                st.subheader("Visualización Resumen")
                st.write("A continuación algunos de los gráficos para visualizar las conclusiones del EDA")
                counts = pd.crosstab(df2["contact"], df2["y"])
                fig, ax = plt.subplots()
                counts.plot(kind="bar", ax=ax)
                ax.set_xlabel("contact")
                ax.set_ylabel("y")
                st.write("Punto 1")
                st.write("Amount of clients accepting or rejecting an offer depending on how they were contacted")
                st.pyplot(fig)

                counts2 = pd.crosstab(df2["month"], df2["y"])
                fig, ax = plt.subplots()
                counts2.plot(kind="bar", ax=ax)
                ax.set_xlabel("month")
                ax.set_ylabel("y")
                st.write("Punto 2")
                st.write("Amount of clients accepting or rejecting an offer depending on the month of contact")

                st.pyplot(fig)

                st.write("Punto 3")

                st.write("Total of clients grouped by level of education")

                agrupacion = (
                    df2[df2["y"] == "yes"].groupby("education").size()
                    / df2.groupby("education").size()
                )

                tota_porEd=df2.groupby("education").size()

                st.write(tota_porEd)

                st.write("Conversion rate depending on level of education")
                st.write(agrupacion*100)

                st.write("Punto 4")

                st.write("Average number of times a client that said yes or no to an offer was contacted before")

                df_plot = (
                    df2.dropna(subset=["y","previous"])
                    .groupby(df2["y"])["previous"]
                    .mean()
                    .sort_values(ascending=False)
                )

                st.bar_chart(df_plot)

                st.write("Punto 5")
                st.write("Total of clients grouped by Job")

                agrupacion2 = (
                    df2[df2["y"] == "yes"].groupby("job").size()
                    / df2.groupby("job").size()
                )

                tota_porEd=df2.groupby("job").size().sort_values(ascending=False)

                st.write(tota_porEd)

                st.write("Conversion rate depending on job")
                st.write(agrupacion2*100)


                st.subheader("Insights")
            

                telefono = df2[df2["contact"]== "telephone"].value_counts().sum()
                celular = df2[df2["contact"]== "cellular"].value_counts().sum()


                Ventatelefono = df2[(df2["y"] == "yes") & (df2["contact"]== "telephone")]
                Pct_telefono = round((Ventatelefono.value_counts().sum())/telefono*100,2)

                Ventacelular = df2[(df2["y"] == "yes") & (df2["contact"]== "cellular")]
                Pct_celular = round((Ventacelular.value_counts().sum())/celular*100,2)



                st.write(f"1. Se encontro que la efectividad de la venta por celular es mayor a la efectividad de la venta por telefóno, a pesar de ello se contacto por telefono,{telefono} clientes, con una efectividad de {Pct_telefono}%, por otro lado, se recomienda enfocar en la venta de celular y concentrar esfuerzos donde el porcentaje de conversión es {Pct_celular}%")

                st.write(f"2. Se demuestra que a través de los meses la cantidad de las aceptaciones mantiene un nivel estable; sin embargo, la cantidad de denegaciones crece en gran medida en algunos meses (A pesar de que el numero de aceptaciones no lo acompañe), es decir en algunos meses se están generando miles de clientes que no son convertibles, y por ello debe recortarse la cantidad de clientes distribuidos acorde al perfil de los clientes que aceptan, debido a que se realiza el esfuerzo de contactar hasta 10,000 personas, pero solamente 500 a 1000 se convierten de forma regular aunque la cantidad de clientes contactados sea mayor")

                st.write(f"3. se observa que dentro de los niveles educativos contactados el nivel de university,high school,professional course resaltan en conversión y mayor cantidad de clientes para contacto, por lo que debe concentrarse mayor capacidad de los ejecutivos en estos Leads que muestran mayor propensión")

                st.write(f"4. Se debe enfocar los esfuerzos en clientes que previamente han sido contactados en campañas previas, en promedio los clientes que tienen almenos 1 campaña contactado previamente son más propensos a aceptar una propuesta de campaña, mientras que los clientes que no han sido contactados o leads frescos comúnmente no aceptan, por lo que se debería enfocar los esfuerzos en contactar leads con contacto previo y buscar automatizar el primer contacto mediante herramientas digitales para reducir el tiempo de 1er ofrecimiento")

                st.write(f"5. Se encuentra un nicho a explotar entre los estudiantes y retirados con conversiones mayores a 25%, que debería ser explotado ampliando las bases de contacto para incrementar la venta en estos tipos de trabajadores, asimismo, los trabajos administrativos deberian mantenerse como el foco principal de la venta al ser más numeroso, por otro lado, el contacto de Blue-collar deberia limitarse, ya que la volumetría es muy alta con una conversión de 6%")