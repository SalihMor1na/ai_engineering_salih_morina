import streamlit as st
from taxipred.utils.helpers import post_api_endpoint, get_ors_driving_distance 

API_BASE_URL = "http://127.0.0.1:8000"
TIME_OPTIONS = ["Evening", "Morning", "Night", "Daytime"] 
DAY_OPTIONS = ["Weekend", "Weekday"]
TRAFFIC_OPTIONS = ["Low", "Medium", "High"]
WEATHER_OPTIONS = ["Clear", "Rain", "Snow"]


st.set_page_config(page_title="TaxiPris Dashboard (Riktig Körsträcka)", layout="wide")
st.title("🗺️ Taxi App: Prisprediktion")
st.markdown("Ange adresser för att få en prisuppskattning baserad på den **faktiska körsträckan** via OpenRouteService.")


if 'distance' not in st.session_state:
    st.session_state['distance'] = None
if 'duration' not in st.session_state:
    st.session_state['duration'] = None


with st.form("prediction_form"):
    st.header("1. Resans Platser")
    
    pickup_location = st.text_input("📍 Upphämtningsplats", "Kungsgatan 34, Göteborg")
    dropoff_location = st.text_input("🏁 Avlämningsplats", "Göteborg Landvetter flygplats")

 
    if st.form_submit_button("Hämta Sträcka och Tid (ORS)"):
        with st.spinner('Anropar OpenRouteService för körsträcka och restid...'):
            ors_result = get_ors_driving_distance(pickup_location, dropoff_location)
        
        if "error" in ors_result:
            st.error(f"ORS Fel: {ors_result['error']}. Kontrollera din API-nyckel i .env-filen.")
            st.session_state['distance'] = None
            st.session_state['duration'] = None
        else:
          
            st.session_state['distance'] = ors_result['distance_km']
            st.session_state['duration'] = ors_result['duration_minutes']
            st.success(f"**Distans**: {st.session_state['distance']:.2f} km | **Tid**: {st.session_state['duration']:.1f} minuter")
            
   
    calculated_distance_km = st.session_state.get('distance')
    calculated_duration_minutes = st.session_state.get('duration')


    st.subheader("2. Detaljer & Taxa")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        passenger_count = st.number_input("Antal passagerare", min_value=1, max_value=6, value=1)
        
      
        manual_duration = st.number_input(
            "Använd restid (minuter)", 
            min_value=1.0, 
            max_value=300.0, 
            value=calculated_duration_minutes if calculated_duration_minutes else 25.0,
            step=1.0
        )
        
    with col2:
        time_of_day = st.selectbox("Tid på dagen", options=TIME_OPTIONS)
        day_of_week = st.selectbox("Dag i veckan", options=DAY_OPTIONS)
        traffic_conditions = st.selectbox("Trafikförhållanden", options=TRAFFIC_OPTIONS)
        
    with col3:
        weather = st.selectbox("Väder", options=WEATHER_OPTIONS)
        base_fare = st.number_input("Basavgift (kr)", min_value=0.0, value=3.0, step=0.5, format="%.1f")
        per_km_rate = st.number_input("Pris per km (kr)", min_value=0.0, value=1.5, step=0.1, format="%.2f")
        per_min_rate = st.number_input("Pris per minut (kr)", min_value=0.0, value=0.2, step=0.05, format="%.02f")
        
 
    predict_button = st.form_submit_button("⚡ Prediktera Pris med AI")


if predict_button:
    
    if not calculated_distance_km:
        st.error("Klicka först på 'Hämta Sträcka och Tid (ORS)' för att beräkna avståndet innan du predikterar priset.")
        st.stop()


    payload = {
        "Trip_Distance_km": calculated_distance_km, 
        "Time_of_Day": time_of_day,
        "Day_of_Week": day_of_week,
        "Passenger_Count": passenger_count,
        "Traffic_Conditions": traffic_conditions,
        "Weather": weather,
        "Base_Fare": base_fare,
        "Per_Km_Rate": per_km_rate,
        "Per_Minute_Rate": per_min_rate,
        "Trip_Duration_Minutes": manual_duration,
    }


    with st.spinner():
        api_result = post_api_endpoint(endpoint="/predict", data=payload, base_url=API_BASE_URL)


    st.subheader("4. Slutgiltigt Resultat")
    
    if "predicted_price" in api_result:
        price = api_result['predicted_price']
        
        with st.container(border=True):
            st.success(f"### Uppskattat Pris: **{price:.2f} kr**")
            st.balloons()
    else:
        st.error(f"Ett fel uppstod i API-anropet. Detaljer: {api_result.get('error', 'Okänt fel')}")
