
from bs4 import BeautifulSoup
import requests
from tabulate import tabulate


stock = input("What stock would you like to analyse-->").upper()
header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
#Getting Website

page1_text = requests.get(f'https://ca.finance.yahoo.com/quote/{stock}', headers = header).text
page2_text = requests.get(f'https://ca.finance.yahoo.com/quote/{stock}/key-statistics?p={stock}', headers = header).text
page3_text = requests.get(f'https://ca.finance.yahoo.com/quote/{stock}/financials?p={stock}', headers = header).text
page4_text = requests.get(f'https://ca.finance.yahoo.com/quote/{stock}/cash-flow?p={stock}', headers = header).text
page5_text = requests.get(f'https://ca.finance.yahoo.com/quote/{stock}/balance-sheet?p={stock}', headers = header).text


soup1 = BeautifulSoup(page1_text, "lxml")
soup2 = BeautifulSoup(page2_text, "lxml")
soup3 = BeautifulSoup(page3_text, "lxml")
soup4 = BeautifulSoup(page4_text, "lxml")
soup5 = BeautifulSoup(page5_text, "lxml")

#Price
Price= soup1.find("fin-streamer", class_="Fw(b) Fz(36px) Mb(-4px) D(ib)").text

#P/E Ratio 
PE_ratio = soup1.find_all("td", class_="Ta(end) Fw(600) Lh(14px)")[10].text


#Profit Margin
Profit_Margin = soup2.find_all('td')
run=True
for x in Profit_Margin:
    if run == False:
        Profit_Margin=x.text
        break
    if "Profit Margin" in x.text:
        run=False

#Net imcome growth

Net_Income = []
run = False
Table = soup3.find('div', class_="M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)").find_all('span')
for x in Table:
    if run==True:
        if "Net Income" in x.text:
            break
        Net_Income.append(x.text)
        
    if "Net Income" in x.text:
        run=True


#Total Revenue
run=False
Total_Revenue = []
for x in Table:
    if run==True:
        if "Cost of Revenue" in x.text:
            break
        Total_Revenue.append(x.text)
        
    if "Total Revenue" in x.text:
        run=True



#Free cashflow
run=False
run1=False
Cash_Flow=[]
Table = soup4.find('div', class_="M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)").find_all('span')
for x in Table:
    if "Capital Expenditure" in x.text:
        run=True
        
    if run1==True:
            Cash_Flow.append(x.text)

    if run==True:
        if "Free Cash Flow" in x.text:
            run1=True
    


#Assets and Liabilities
Assets=[]
Liabilities=[]
run=False

Table = soup5.find('div', class_="M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)").find_all('span')
for x in Table:
    if run==True:
        if "Non-current liabilities" in x.text:
            break
        Liabilities.append(x.text)
        
    if "Total Current Liabilities" in x.text:
        run=True



run=False
for x in Table:
    if run==True:
        if "Non-current assets" in x.text:
            break
        Assets.append(x.text)
        
    if "Total Current Assets" in x.text:
        run=True



#Shares Outstanding
run=False
Shares_Outstanding = []
page6_text=requests.get(f'https://www.sharesoutstandinghistory.com/?symbol={stock.lower()}').text
soup6=BeautifulSoup(page6_text, "lxml")
Table=soup6.find_all('td', class_="tstyle")
Shares_data=[]
for x in Table:
    Shares_data.append(x.text)

Shares_data=Shares_data[::-1]

if len(Shares_data)>32:
    Shares_Outstanding=Shares_data[0:31:2]
else:
    Shares_Outstanding=Shares_data[::2]


    
#Market Cap
Market_Cap = soup1.find_all("td", class_="Ta(end) Fw(600) Lh(14px)")[8].text

Cash_Flow.pop(0)
Avg_Cash=0
for count,x in enumerate(Cash_Flow):
    x=float(x.replace(",", ""))
    Cash_Flow[count]=x
    Avg_Cash+=x
Avg_Cash=(Avg_Cash/len(Cash_Flow))*1000  

if Market_Cap[-1] == 'B':
    Market_Cap=float(Market_Cap.replace('B',''))*1000000000
elif Market_Cap[-1] == 'M':
    Market_Cap=float(Market_Cap.replace('M',''))*1000000
elif Market_Cap[-1] == 'T':
    Market_Cap=float(Market_Cap.replace('T',''))*1000000000000

Price_TO_Cash=round(Market_Cap/float(Avg_Cash),2)

#printing as table
Table = [['Pillars','Details','']]
PE_List=['P/E Ratio',f"{PE_ratio}<20"]
Profit_List=['Profit Margin',f"{Profit_Margin}>10%"]
Net_List=['Net Income',f"{Net_Income[1]}>{Net_Income[-1]}"]
Revunue_List=['Revenue Growth',f"{Total_Revenue[1]}>{Total_Revenue[-1]}"]
if len(Shares_Outstanding)>1:
    Shares_List=['Shares Outstanding',f"{Shares_Outstanding[0]}<{Shares_Outstanding[-1]}"]
Free_List=['Free Cash Flow',f"{int(Cash_Flow[0])}>{int(Cash_Flow[-1])}"]
Assets_List=['Assests & Liabilities',f"{Assets[1]}>{Liabilities[1]}"]
Price_List=['Price to Free Cash',f"{Price_TO_Cash}<20"]



#Pillar Analyising
check="✓"
uncheck="X"
num_of_checks=0

#Checking P/E Ratio
if PE_ratio=="N/A":
    PE_ratio=0
if float(PE_ratio) <= 20 and float(PE_ratio)>0:
    PE_List.append(check)
    num_of_checks+=1
else:
    PE_List.append(uncheck)

#Checking profit margin
Profit_Margin=Profit_Margin.replace("%","")
if float(Profit_Margin) >= 10:
    Profit_List.append(check)
    num_of_checks+=1
else:
    Profit_List.append(uncheck)


#Checking Net income growth
Net_Income.pop(0)

for count,x in enumerate(Net_Income):
    x=float(x.replace(",", ""))
    Net_Income[count]=x

if float(Net_Income[0])>float(Net_Income[-1]):
    Net_List.append(check)
    num_of_checks+=1
else:
    Net_List.append(uncheck)

#Checking revenue growth
Total_Revenue.pop(0)

for count,x in enumerate(Total_Revenue):
    x=float(x.replace(",", ""))
    Total_Revenue[count]=x

if float(Total_Revenue[0])>float(Total_Revenue[-1]):
    Revunue_List.append(check)
    num_of_checks+=1
else:
    Revunue_List.append(uncheck)

#Checking for Shares outstanding
if len(Shares_Outstanding)>1:
    for count,x in enumerate(Shares_Outstanding):
        if x[-1]=='M':
            x=x[0:-1]
            x=float(x)*1000000
        elif x[-1]=='B':
            x=x[0:-1]
            x=float(x)*1000000000
        Shares_Outstanding[count]=x

    if float(Shares_Outstanding[0])<=float(Shares_Outstanding[-1]):
        Shares_List.append(check)
        num_of_checks+=1
    else:
        Shares_List.append(uncheck)
else:
   Shares_List=['Shares Outstanding',"Not Given","-"]

#Checking free cash flow
if float(Cash_Flow[0])>float(Cash_Flow[-1]) and float(float(Cash_Flow[0]))>0:
    Free_List.append(check)
    num_of_checks+=1
else:
    Free_List.append(uncheck)

#Checking assets and liabilities
Assets.pop(0)
Liabilities.pop(0)

for count,x in enumerate(Assets):
    x=float(x.replace(",", ""))
    Assets[count]=x

for count,x in enumerate(Liabilities):
    x=float(x.replace(",", ""))
    Liabilities[count]=x

if float(Assets[0])>float(Liabilities[0]):
    Assets_List.append(check)
    num_of_checks+=1
else:
    Assets_List.append(uncheck)

#8th pillar
if 0<(Market_Cap/Avg_Cash)<20 :
    Price_List.append(check)
    num_of_checks+=1
else:
    Price_List.append(uncheck)


Table.append(PE_List)
Table.append(Profit_List)
Table.append(Net_List)
Table.append(Revunue_List)
Table.append(Shares_List)
Table.append(Free_List)
Table.append(Assets_List)
Table.append(Price_List)

print(f"\n\n{stock}-->${Price}")
print(tabulate(Table[1:], headers=Table[0], tablefmt='fancy_grid', showindex=range(1,9)))
print("\n\n")
run=True
while run:
    if input("Press enter to end...") == "":
        run=False

with open(f'{stock}-{num_of_checks}.txt', 'w', encoding="utf-8") as f:
    f.write(stock+"-->"+Price+"\n")
    f.write(tabulate(Table[1:], headers=Table[0], tablefmt='fancy_grid', showindex=range(1,9)))
