from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import plotly.express as px
import streamlit as st
import pandas as pd
import time


def get_jobkorea_data(driver, temp_df):
    url = 'https://www.jobkorea.co.kr/Search/?stext=%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D'
    driver.get(url)
    time.sleep(3)

    html = driver.page_source
    soup = bs(html, 'html.parser')
    box_content = soup.find('article', class_='list')
    article_list = box_content.find_all('article', class_='list-item')

    for article in article_list:
        Col_Recruit = article.find('a', class_='information-title-link dev-view').get_text(strip=True)
        Col_Company = article.find('a', class_='corp-name-link dev-view').get_text(strip=True)
        detail = [li.text for li in article.find_all('li')]
        Col_url = 'www.jobkorea.co.kr' + article.find('a', class_='corp-name-link dev-view')['href']

        temp_df['Site'].append('Job_Korea')
        temp_df['Col_Company'].append(Col_Company)
        temp_df['Col_Recruit'].append(Col_Recruit)
        temp_df['Col_detail'].append(detail)
        temp_df['Col_url'].append(Col_url)

def get_saramin_data(driver, temp_df):
    url = 'https://www.saramin.co.kr/zf_user/search?searchword=%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D'
    driver.get(url)
    time.sleep(3)

    html = driver.page_source
    soup = bs(html, 'html.parser')
    box_content = soup.find('div', class_='content')
    article_list = box_content.find_all('div', class_='item_recruit')

    for article in article_list:
        Col_Company = article.find('a', class_='track_event data_layer').get_text(strip=True)
        Col_Recruit = article.find('h2', class_='job_tit').get_text(strip=True)
        detail = [span.get_text(strip=True) for span in article.find_all('span')]
        Col_url = 'www.saramin.co.kr' + article.find('a', class_='data_layer')['href']

        temp_df['Site'].append('Saramin')
        temp_df['Col_Company'].append(Col_Company)
        temp_df['Col_Recruit'].append(Col_Recruit)
        temp_df['Col_detail'].append(detail)
        temp_df['Col_url'].append(Col_url)

    
def pie_chart(df, names_col, values_col, title,hover_col,):
    fig = px.pie(df, 
                 names=names_col, 
                 values=values_col, 
                 title=title, 
                 hover_data=[hover_col])
    return fig

st.title('Title')

with st.form('form'):
    submit_button = st.form_submit_button('Recruit Searching')

    if submit_button:
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        temp_df = {'Site': [], 'Col_Company': [], 'Col_Recruit': [], 'Col_detail': [], 'Col_url': []}

        get_jobkorea_data(driver, temp_df)
        get_saramin_data(driver, temp_df)

        driver.quit()

        job_Sara_df = pd.DataFrame(temp_df)
        st.dataframe(job_Sara_df)

        job_Sara_Site = job_Sara_df.groupby('Site').size().reset_index(name = 'Count')
        total_count = job_Sara_Site['Count'].sum()
        job_Sara_Site['Ratio'] = round((job_Sara_Site['Count']/total_count) * 100,2)

        st.dataframe(job_Sara_Site)

        fig = pie_chart(job_Sara_Site,'Site','Count','Recruitment Ratio','Ratio')
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)