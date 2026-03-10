import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\ahmad\Desktop\مشاريع تحليل البيانات\Python\online_retail_II.csv")
# print(df)

# info = df.info()
desc = df.describe()
# print(desc)
samp = df.sample(10)
# print(samp)
sh = df.shape
# print(sh)
head = df.head()
# print(head)
tail = df.tail(20)
# print(tail)
is_n = df.isnull().sum()
# print(is_n)
lo = df.loc[0:10, 'Customer ID':'Country']
# print(lo)
ilo = df.iloc[5:25, 1:5]
# print(ilo)

# dup = df.duplicated().sum()
# print(dup)
df = df.drop_duplicates()

# print('1' , df['Customer ID'].isnull().sum()) # عدد المعرفات الناقصة
# print('2' , (df['Quantity'] < 0).sum()) # القيم السالبة
# print('3' , (df['Price'] == 0).sum()) # الاسعار اللي = 0
# print('4' , df['Invoice'].astype(str).str.startswith('C')) # معرفة الفواتير الملغية

df = df.dropna(subset=['Customer ID']) #حذف البيانات اللي لا تحتوي على معرف للعميل
df = df[df['Quantity'] > 0] # حذف الكميات السالبة

df['Revenue'] = df['Quantity'] * df['Price']
price_group = df[['Revenue', 'Quantity', 'Price', 'Country']]
# print(price_group.describe())
# print(price_group)
df['Description'] = df['Description'].str.title()
total_revenue = df['Revenue'].sum() # اجمالي المبيعات
# print("Total Revenue = ", total_revenue)
total_customer = df['Customer ID'].nunique() # عدد العملاء بدون تكرار
# print("Total Customer = ", total_customer)
total_order = df['Invoice'].nunique() # عدد الفواتير بدون تكرار
# print("Total Invoice = ", total_order)

avg_order_value = (total_revenue / total_order) # متوسط قيمة الطلب
# print("Avg Order = ", avg_order_value)

thous = df.head(10000)
# print(thous.groupby('Country').sum()) # تجميع اول 100000 حسب الدولة
# print(price_group.groupby('Country').agg(['sum','mean'])) # تجميع حسب الدولة مع حساب المجموع والمتوسط 

def price_level(row):
    if row >= 1000:
        return 'High'
    else:
        return 'Low'
df['Status'] = df['Revenue'].apply(price_level)
country_count = df['Country'].value_counts()
# print(country_count)

pivot = df.pivot_table(index='Country', columns='Status', values='Price', aggfunc=('sum','mean') )
# print(pivot)


# df2 = df.select_dtypes(include='number')
# corr = df2.corr() # لازم الجداول تكون رقمبة فقط
# print(corr)

rev_by_country = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False)
top10 = rev_by_country.head(10)
other = rev_by_country.iloc[10:].sum()
top10['other'] = other
# print(rev_by_country)

plt.bar(top10.index, top10.values)
plt.xticks(rotation=45)
plt.title('Revenue by Countries')
plt.xlabel('Country')
plt.ylabel('Revenue')

st = df['Status'].value_counts()
myLable= st.values / st.values.sum()*100
plt.pie(st, startangle=90, labels=myLable, autopct='%1.1f%%', shadow=True, colors=['#2d3250','#f6b17a'])
plt.legend(labels=st.index, loc='upper right')

Quan = df.groupby('Country')['Quantity'].sum().sort_values(ascending=False)
Quan10 = Quan.head(10)
other_Ouan = Quan.iloc[10:].sum()
Quan10['other_Ouan'] = other_Ouan
# print(Quan)

plt.plot(Quan10, 'go-')
plt.xticks(rotation=90)
plt.title('Quantity by Countries')
plt.xlabel('Country')
plt.ylabel('Quantity')
plt.show()

Con_Quan_TotRev = df.groupby('Country')[['Revenue', 'Quantity']].sum().sort_values(ascending=False, by='Revenue').head(10)
s_axis = Con_Quan_TotRev.plot(y='Revenue', kind='bar', color='g', ylabel='Revenue (Million)')
Con_Quan_TotRev.plot(y='Quantity', kind='line', secondary_y=True, ax=s_axis, color='r', ylabel='Quantity', rot=90)
# print(Con_Quan_TotRev)
plt.show()


df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Month'] = df['InvoiceDate'].dt.to_period('M')
monthly_rev = df.groupby('Month')['Revenue'].sum()

monthly_rev.plot()
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.show()

df.to_csv(r"C:\Users\ahmad\Desktop\مشاريع تحليل البيانات\Python\clean_online_retail_II.csv", index=False)