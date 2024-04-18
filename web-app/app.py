from functions import *

# initialize session state values
if 'price_result' not in st.session_state:
    st.session_state.price_result = ''

if 'new_csv' not in st.session_state:
    st.session_state.new_csv = None

if 'new_data' not in st.session_state:
    st.session_state.new_data = False

if 'fitted' not in st.session_state:
    st.session_state.fitted = False

# handler for execution prediction function
def get_car_price():
    result = pirce_car(brand, model, year, milage, fuel, engine, trans, accident, c_title, use_new_data)
    st.session_state.price_result = result

# some html tweaks for better visuals
st.set_page_config(layout="wide")
st.markdown("""
<style>
.big-font {
    font-size:62px !important;
    font-weight: bold;
    line-height: 0.45;
}
</style>
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:2rem;
    }
</style>
""", unsafe_allow_html=True)
st.markdown('Project for Computing Processes Study<p class="big-font">Used cars pricing</p>created by Michał Koziński</br>', unsafe_allow_html=True)
st.write("")

# initialize tabs for layout creation
tab1, tab2, tab3 = st.tabs(["Browse offers", "Get your car priced", "Train model using new data"])

# flag that prevents of displaying errors if one of them was already catch, cause later errors are caused by previous ones
exception_caught = False

try:
    # get dataframe created from database records
    df = get_df_from_db()
    df_filtered = df.copy() # copy dataframe

    with tab1:
        # drop unneeded ID's
        df = df.drop('ID', axis = 1)

        # get list of columns
        columns = df.columns.tolist()
        # create selector for variables to filter
        filter_columns = st.multiselect('Choose columns to filter by', columns)

        # init filtration dictionary
        filter_dict = {}
        # perform filtering
        for col in filter_columns:
            # separate filtering for continuous and discrete variables
            if col in ['Milage', 'Price']:
                # continuous variables filtering is based on 2 pin sliders
                selected_range = st.slider(f'Choose range in {col} to filter by', min(df[col]), max(df[col]), (min(df[col]), max(df[col])))
                # filter dataframe with selected values
                filter_dict[col] = list(range(selected_range[0], selected_range[1] + 1))
            else:
                # discrete variables is based on simple selector
                # get possible values of filtered variable
                unique_values = df[col].unique().tolist()
                # create selector of obtained values
                selected_values = st.multiselect(f'Choose values in {col} to filter by', unique_values)
                # filter dataframe with selected values of the variable
                if selected_values:
                    filter_dict[col] = selected_values
                    df = df[df[col].isin(selected_values)]

        # filter dataframe with selected values of all variables
        for col, vals in filter_dict.items():
            df = df[df[col].isin(vals)]

        st.header('Data')
        # display dataframe
        st.dataframe(df.set_index(df.columns[0]))

    with tab2:
        # create container for value inputs
        input_cont1 = st.container()
        with input_cont1:
            # crete cols for first row of inputs
            input_c11, input_c12, input_c13 = st.columns([3, 8, 1])
            with input_c11:
                # input of brand name
                brand = st.selectbox('Brand', ['-'] + df_filtered['Brand'].unique().tolist())
                # filter dataframe to limit selection other variables to the ones that fits
                df_filtered = df_filtered[df_filtered['Brand'] == brand] if brand != '-' else df_filtered
            with input_c12:
                # input of model name
                model = st.selectbox('Model', ['-'] + df_filtered['Model'].unique().tolist())
                # filter dataframe to limit selection other variables to the ones that fits
                df_filtered = df_filtered[df_filtered['Model'] == model] if model != '-' else df_filtered
            with input_c13:
                # input of year value
                year = st.selectbox('Model year', ['-'] + df_filtered['Model_year'].unique().tolist())
                # filter dataframe to limit selection other variables to the ones that fits
                df_filtered = df_filtered[df_filtered['Model_year'] == year] if year != '-' else df_filtered
            input_c21, input_c22, input_c23 = st.columns([4, 6, 2])
            with input_c21:
                # input of engine model name
                engine = st.selectbox('Engine', ['-'] + df_filtered['Engine'].unique().tolist())
                # filter dataframe to limit selection other variables to the ones that fits
                df_filtered = df_filtered[df_filtered['Engine'] == engine] if engine != '-' else df_filtered
            with input_c22:
                # input of type of transmission
                trans = st.selectbox('Transmission', ['-'] + df_filtered['Transmission'].unique().tolist())
                # filter dataframe to limit selection other variables to the ones that fits
                df_filtered = df_filtered[df_filtered['Transmission'] == trans] if trans != '-' else df_filtered
            with input_c23:
                # input of type of fuel
                fuel = st.selectbox('Fuel type', ['-'] + df_filtered['Fuel_type'].unique().tolist())
                # filter dataframe to limit selection other variables to the ones that fits
                df_filtered = df_filtered[df_filtered['Fuel_type'] == fuel] if fuel != '-' else df_filtered
            input_c31, _, input_c32, input_c33, _, _, get_price_col = st.columns([3, 1, 2, 2, 2, 3, 2])
            with input_c31:
                # milage value input
                milage = st.number_input('Milage', min_value=0)
            with input_c32:
                st.write("")
                st.write("")
                # boolean input if car had accident reported before
                accident = st.checkbox('Accident reported')
            with input_c33:
                st.write("")
                st.write("")
                # boolean input if car has clean title
                c_title = st.checkbox('Clean title')
            with get_price_col:
                # create fancy style to make button for running prediction bigger
                st.markdown("""
                <style>
                button {
                    height: auto;
                    padding-top: 10px !important;
                    padding-bottom: 10px !important;
                }</style>""", unsafe_allow_html=True, )
                st.button('Get price', use_container_width=True, on_click=get_car_price)
        displayed_result = st.empty()
        # display result of prediction
        displayed_result.markdown('<font size ="10">' + st.session_state.price_result + '</font>',
                                  unsafe_allow_html=True)

    with tab3:
        # uploader of new data
        loaded_csv = st.file_uploader('Upload .csv file', type='csv')
        try:
            # if csv is loaded read it and save and cache it as dataframe in session state
            st.session_state.new_csv = pd.read_csv(loaded_csv)
        except:
            pass
        # update flag if new data is loaded
        if st.session_state.new_csv is None:
            new_df = False
        else:
            new_df = True
        train_c1, _, train_c2 = st.columns([4, 10, 3])
        with train_c1:
            train_c11, train_c12, _ = st.columns([3, 2, 2])
            with train_c11:
                try: # button to push file to database, enabled only if data was loaded to web-app
                    if st.button('Push file to database', on_click = setup_new_db, args=(st.session_state.new_csv,), disabled=not new_df):
                        # if data was successfully pushed to database set flag to True
                        st.session_state.new_data = True
                except Exception as e:
                    # display errors if any occurs
                    st.write(e)
            with train_c12:
                with st.spinner('Fitting new data...'):
                    try:
                        # fit model with new data button, enabled only if data was loaded to database
                        if st.button('Fit new data', on_click=fit_new, disabled=not st.session_state.new_data):
                            st.session_state.fitted = True
                    except Exception as e:
                        # display errors if any occurs
                        st.write(e)
        with train_c2:
            # display only if fitting operation was run successful
            if st.session_state.fitted:
                # checkbox for set flag of using model fitted on new data
                use_new_data = st.checkbox('Make predictions using new model')
            else:
                use_new_data = False

except Exception as e:
    st.write(str(e))

# reload page during initialization cause of streamlit malfunctioning 'st.tabs' otherwise
if not st.session_state.get('init_reload'):
    st.session_state.init_reload = True
    st.rerun()



# --server.port 8080
# --server.enableXsrfProtection false



