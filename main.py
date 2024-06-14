from house_loan import LoanDetails
import streamlit as st


########################
#CREATING STREAMLIT APP
########################

def main():
    #title and inputs
    st.write('<h1 style="text-align: center;">Simulação de empréstimo</h1>', unsafe_allow_html=True)

    st.write('<h3 style="text-align: center;"> Inputs </h3>', unsafe_allow_html=True)
    capital = st.number_input("Capital (em €)", min_value=1, value=300000)
    rate = st.text_input("Taxa de juro (em %)", value = 3.00)
    years = st.text_input("Número de períodos (em anos)", value = 30)

    #data validation
    rates_list = rate.split(',')
    years_list = years.split(',')

    no_rates = len(rates_list)
    no_years = len(years_list)

    if no_rates == no_years:
        
        try:
            #converting text input to float
            rates_list_float = [float(rate) for rate in rates_list]
            data_validation = True
            
            #check if all rates are bigger than 0
            if not all(rate > 0 for rate in rates_list_float):
                st.error('Interest rates must be bigger than 0')
                data_validation = False
            
        except:
            st.error("Could not convert interest rate inputs to float")
            data_validation = False
        
        #if all data from previous validation step is ok, check the next condition
        if data_validation:
            try:
                years_list_integer = [float(year) for year in years_list]
                data_validation = True
                if not all(year >= 1 for year in years_list_integer):
                    st.error('All year periods must be at least 1')
                    data_validation = False
            except:
                st.error("Could not convert year inputs to integer")
                data_validation = False
        
        #creating an instance of the class if no error exist
        if data_validation:
             house_1 = LoanDetails(principal=capital, annual_rates=rates_list_float, years=years_list_integer)
             df_house_1 = house_1.payment_decomposition()
             #criar as 3 variáveis principais a mostrar ao user
             st.write('<h3 style="text-align: center;">Visão geral</h3>', unsafe_allow_html=True)
             col1, col2, col3 = st.columns(3)
             
             col1.metric(label="Prestação Mensal Máxima", value=f'€ {max(df_house_1["Payment (€)"]):,.2f}')
             col2.metric(label="MTIC", value = f'€ {house_1.total_amount_to_repay():,.2f}')
             col3.metric(label="Total de juros", value=f'€ {df_house_1["Interest Accumulated (€)"].iloc[-1]:,.2f}')
             
             #criar line chart para capital em dívida
             st.write('<h3 style="text-align: center;"> Evolução do capital em dívida </h3>', unsafe_allow_html=True)
             chart_df = df_house_1[["Month", "Principal left (€)"]].groupby("Month").min()
             st.line_chart(chart_df)
             
             #criar line chart para juros em dívida
             st.write('<h3 style="text-align: center;"> Evolução do pagamento de juros </h3>', unsafe_allow_html=True)
             chart_df = df_house_1[["Month", "Interest Accumulated (€)"]].groupby("Month").min()
             st.line_chart(chart_df)
             
             #criar dataframe com o detalhe
             st.write('<h3 style="text-align: center;"> Detalhe mensal do pagamento do empréstimo </h3>', unsafe_allow_html=True)
             st.write(df_house_1)
        
    else:
        st.error(f'The number of interest rates ({no_rates}) does not match the number of periods ({no_years})') 

if __name__ == '__main__':
    main()