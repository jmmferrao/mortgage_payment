from house_loan import LoanDetails
import streamlit as st


#########################
# CREATING STREAMLIT APP
#########################

def main():
    
    ########################
    #Settings
    ########################
    
    page_title = 'Loan simulation'
    page_icon = ":money_with_wings"
    layout = "centered"
    
    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
    
    ########################
    #Title and instructions
    ########################
    
    st.write('<h1 style="text-align: center;"> Loan Simulation </h1>', unsafe_allow_html=True)
    
    instruction_text = "Hey there!<br><br>\
    \
    This is a simple app that simplifies the loan simulation process.<br><br> \
    \
    The user should provide three inputs: the loan amount (capital), the interest rate or interest rates to consider and the number of years. If one or more inputs are provided, they should be comma separated. <br><br> \
    \
    Please note that the number of entries in the interest rates input must match the number of entries in the number of years input.<br><br> \
    \
    For example, if there is only one interest rate (such as 3), then there should only be one entry in the number of years input (such as 40); if there are two interest rates (such as 4.5, 3), then there should be two entries in the number of years input (such as 25, 15) and so on.<br><br>"
    
    st.markdown(f'<div style="text-align: justify;"> {instruction_text} </div>', unsafe_allow_html=True)
    
    #########################
    # Inputs sections
    #########################

    st.write('<h3 style="text-align: center;"> Inputs </h3>', unsafe_allow_html=True)
    capital = st.number_input("Capital (€)", min_value=1, value=300000)
    rate = st.text_input("Interest rates (%)", value = '4.5, 3')
    years = st.text_input("Number of periods (in years)", value = '25, 15')
    st.markdown("<br>", unsafe_allow_html=True)

    #########################
    # Data validation
    #########################
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
        
        
        ######################################################
        # Creating LoanDetails instance according to inputs
        ######################################################
        if data_validation:
             house_1 = LoanDetails(principal=capital, annual_rates=rates_list_float, years=years_list_integer)
             df_house_1 = house_1.payment_decomposition()
             #criar as 3 variáveis principais a mostrar ao user
             st.write('<h3 style="text-align: center;"> Overview </h3>', unsafe_allow_html=True)
             col1, col2, col3 = st.columns(3)
             
             col1.metric(label="Maximum monthly payment*", value=f'€ {max(df_house_1["Payment (€)"]):,.2f}')
             
             text_note_prestacao_max = '*Without considering other costs that may be charged by banks, such as taxes or insurance.'
             
             st.write(f'<div style="text-align: justify;">{text_note_prestacao_max}</div>', unsafe_allow_html=True)
             
             col2.metric(label="Total amount charged*", value = f'€ {house_1.total_amount_to_repay():,.2f}')
                          
             col3.metric(label="Total interest", value=f'€ {df_house_1["Interest Accumulated (€)"].iloc[-1]:,.2f}')
             
             st.markdown("<br><br>", unsafe_allow_html=True)
             
            #########################
            # Line charts
            #########################
             st.write('<h3 style="text-align: center;"> Principal repayment evolution </h3>', unsafe_allow_html=True)
             chart_df = df_house_1[["Month", "Principal left (€)"]].groupby("Month").min()
             st.line_chart(chart_df)
             
             st.write('<h3 style="text-align: center;"> Interest payment evolution </h3>', unsafe_allow_html=True)
             chart_df = df_house_1[["Month", "Interest Accumulated (€)"]].groupby("Month").min()
             st.line_chart(chart_df)
             
            #########################
            # Data frame
            #########################
             st.write('<h3 style="text-align: center;"> Detailed monthly decomposition </h3>', unsafe_allow_html=True)
             
             # Formatting the euro columns to two decimal places
             df_house_1_style = df_house_1.style.format({
                'Month': '{:.0f}',
                'Payment (€)': '{:.2f}',
                'Interest part (€)': '{:.2f}',
                'Interest percentage': '{:.2f}',
                'Capital part (€)': '{:.2f}',
                'Capital percentage': '{:.2f}',
                'Principal left (€)': '{:.2f}',
                'Interest Accumulated (€)': '{:.2f}'
                })
             
             # Displaying the DataFrame in Streamlit
             st.dataframe(df_house_1_style, hide_index=True, width=120000)
        
    else:
        st.error(f'The number of interest rates ({no_rates}) does not match the number of periods ({no_years})') 

if __name__ == '__main__':
    main()