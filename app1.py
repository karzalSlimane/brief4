import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from database import setup_database  # À implémenter selon votre base de données
from queries import get_cities, get_equipment, get_filtered_ads
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    
    
    
    # Inject custom CSS to modify the styles of various components

    # Configurer la base de données
    Session = setup_database()  # La fonction setup_database doit retourner le moteur et sessionmaker
    session = Session()  # Créer une session

    st.title("Dashboard Immobilier")

    # **Barre latérale : filtres**
    st.sidebar.header("Filtres")

    # Sélection de la ville
    cities = get_cities(session)
    city = st.sidebar.selectbox("Sélectionner une ville", options=[""] + cities)

    # Gamme de prix
    price_min = st.sidebar.slider("Prix minimum", 0, 1000000, 1000)
    price_max = st.sidebar.slider("Prix maximum", 0, 1000000, 500000)

    # Nombre de pièces
    rooms_min = st.sidebar.slider("Nombre minimum de pièces", 1, 10, 1)
    rooms_max = st.sidebar.slider("Nombre maximum de pièces", 1, 10, 5)

    # Nombre de salles de bain
    bathrooms_min = st.sidebar.slider("Nombre minimum de salles de bain", 1, 5, 1)
    bathrooms_max = st.sidebar.slider("Nombre maximum de salles de bain", 1, 5, 2)

    # Sélection des équipements
    equipment_list = get_equipment(session)
    equipment = st.sidebar.multiselect("Sélectionner les équipements", options=equipment_list)

    # Plage de dates
    start_date = st.sidebar.date_input("Date de début", value=datetime(2024, 1, 1))
    end_date = st.sidebar.date_input("Date de fin", value=datetime.today())

    # Appliquer les filtres et récupérer les annonces filtrées
    filtered_ads = get_filtered_ads(
        session,
        price_min,
        price_max,
        rooms_min,
        rooms_max,
        bathrooms_min,
        bathrooms_max,
        city if city != "" else None,
        equipment,
        start_date,
        end_date
    )

    # Afficher le nombre d'annonces trouvées
    st.write(f"**{len(filtered_ads)} annonces trouvées**")

    if filtered_ads:
        ads_df = pd.DataFrame(filtered_ads, columns=["Title", "Price", "Date", "Rooms", "Bathrooms", "Surface Area", "Link", "City", "Equipment"])
        
        # Afficher les annonces filtrées
        st.dataframe(ads_df)

        # Graphiques interactifs
        st.subheader("Analyse des villes")
        city_count = ads_df['City'].value_counts().reset_index()
        city_count.columns = ['City', 'Count']
        st.bar_chart(city_count.set_index('City')['Count'])

        # Carte interactive (facultatif, nécessite un plugin comme `streamlit-folium` si nécessaire)
        # st.map(ads_df)

        st.subheader("Analyse des prix")
        st.write("Histogramme de la répartition des prix :")
        st.bar_chart(ads_df['Price'])

        st.subheader("Boxplot des prix par ville")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(x='City', y='Price', data=ads_df, ax=ax)
        st.pyplot(fig)

        st.subheader("Analyse des caractéristiques des biens")
        equipment_counts = ads_df['Equipment'].value_counts().reset_index()
        equipment_counts.columns = ['Equipment', 'Count']
        chart = alt.Chart(equipment_counts).mark_arc().encode(
            theta='Count',
            color='Equipment'
        )
        st.altair_chart(chart, use_container_width=True)

        st.subheader("Relation entre surface et prix")
        scatter_plot = alt.Chart(ads_df).mark_point().encode(
            x='Surface Area',
            y='Price',
            color='City',
            tooltip=['Surface Area', 'Price', 'City']
        ).interactive()
        st.altair_chart(scatter_plot, use_container_width=True)

        st.subheader("Analyse temporelle")
        ads_df['Date'] = pd.to_datetime(ads_df['Date'])
        date_count = ads_df.groupby('Date').size().reset_index(name='Count')
        st.line_chart(date_count.set_index('Date')['Count'])

        # Bouton pour télécharger les données filtrées
        st.download_button(
            label="Télécharger les données (CSV)",
            data=ads_df.to_csv(index=False),
            file_name="annonces_filtrees.csv",
            mime="text/csv"
        )
    else:
        st.write("Aucune annonce trouvée pour ces critères.")

    session.close()

if __name__ == "__main__":
    main()
