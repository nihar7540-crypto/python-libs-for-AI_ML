import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class retail_sales_analyzer:
    def load_data(self, file_path):
            if file_path.endswith(".csv"):
                self.df = pd.read_csv(file_path)
                print("file loaded successfully")
            else:
                print("error:plz give .csv file")
                return False
            req_cols=["Date","Product","Category","Price","Quantity Sold","Total Sales"]
            col_hai=True
            for c in req_cols:
                if c in self.df.columns:
                    print("column is present")
                else:
                     print("required column is missing")
                     col_hai=False
            if col_hai==False:
                  print("main column of the dataset is not proper than required")
                  return False
            missing_row=0
            invalid_row=0
            for i in range(len(self.df)):
                  for i in range(len(self.df)):
                        d_val= self.df["Date"].isnull()[i]
                        p_val= self.df["Product"].isnull()[i]
                        c_val= self.df["Category"].isnull()[i]
                        pr_val= self.df["Price"].isnull()[i]
                        q_val= self.df["Quantity Sold"].isnull()[i]
                        ts_val= self.df["Total Sales"].isnull()[i]     

                        if d_val==True and p_val==True and c_val==True and pr_val==True and q_val==True and ts_val==True:
                               print("missing value on row",i)  
                               missing_row=missing_row+ 1
                        else:
                            if self.df["Price"][i] <=0 or self.df["Quantity Sold"][i] <= 0:
                                print("invalid zero or negative value at row number:", i)
                                invalid_row= invalid_row+ 1 
            print("total rows with missing values:", missing_row)
            print("total rows with invalid values:", invalid_row)
            if missing_row >0:
                mean_price = self.df["Price"].mean()
                self.df["Price"] = self.df["Price"].fillna(mean_price)
                self.df["Quantity Sold"] = self.df["Quantity Sold"].fillna(1)
                self.df["Total Sales"] = self.df["Price"] * self.df["Quantity Sold"]
                self.df["Product"] = self.df["Product"].fillna("Unknown Product")
                self.df["Category"] = self.df["Category"].fillna("General")
                self.df = self.df.dropna()
                print("all missing values filled")
    def calculate_metrics(self):
            sales_list = []
            qty_list = []
            price_list = []       
            for i in self.df["Total Sales"]:
                sales_list.append(i)       
            for i in self.df["Quantity Sold"]:
                qty_list.append(i)
            for i in self.df["Price"]:
                price_list.append(i)   
            sales_arr=np.array(sales_list)
            qty_arr=np.array(qty_list)
            price_arr=np.array(price_list)  
            self.total_sales=np.sum(sales_arr)
            self.average_sales=np.mean(sales_arr)
            self.max_sales=np.max(sales_arr)
            self.min_sales=np.min(sales_arr)
            self.total_qty=np.sum(qty_arr)
            self.avg_price=np.mean(price_arr) 
            perc_arr=(sales_arr/self.total_sales)*100
            self.df["Sales_Percentage"]=perc_arr  

            self.growth_list=[0,0]
            for i in range(1,len(sales_arr)):
                 prev_sales=sales_arr[i-1]
                 current_sales=sales_arr[i]
                 if prev_sales > 0:
                    g_rate=((current_sales - prev_sales)/prev_sales)*100
                 else:
                    g_rate=0
            self.growth_list.append(g_rate)
            growth_arr=np.array(self.growth_list)
            self.df["Growth_Rate"] = growth_arr
            self.avg_growth = np.mean(growth_arr)
            print("all metrics and extra columns calculated successfully")

    def filter_data(self):
        ("""
        1.Category filter
        2.Date Range filter
        3.Product filter""")
        condition= input("enter filter choice: ")
        if condition =="1":
            for c in self.df["Category"].unique():
                print(c)
            user_cat=input("enter category:")
            filtered_df=self.df[self.df["Category"]==user_cat]
            if len(filtered_df)>0:
                print(filtered_df)
                sub_total=np.sum(np.array(filtered_df["Total Sales"]))
                print("total sales of this category:",sub_total)
            else:
                print("error:no data found")

        elif condition =="2":
            print("enter date range in YYYY-MM-DD format")
            start_d =input("enter start date")
            end_d =input("enter end date:")
            filtered_df =self.df[(self.df["Date"] >= start_d) & (self.df["Date"] <= end_d)]

            if len(filtered_df)>0:
                print(filtered_df)
                sub_total = np.sum(np.array(filtered_df["Total Sales"]))
                print("total sales in this date range:", sub_total)
            else:
                print("no records found between these dates")

        elif condition =="3":
            user_prod = input("enter product name to search: ")
            filtered_df = self.df[self.df["Product"] == user_prod]
            if len(filtered_df) > 0:
                print("filtered records for product:", user_prod)
                print(filtered_df)
            else:
                print("product not found in dataset")
        else:
            print("invalid choice")

    def display_summary(self):
         print(f"""
        total sales:{self.date_agg}
        total sales amount:{self.total_sales}
        average sales:{self.average_sales}
        highest sale :{self.max_sales}
        lowest sale :{self.min_sales}
        total qty sold :{self.total_qty}
        average prd price :{self.avg_price}
        average growth rate:{self.avg_growth}%""")

    def make_charts(self):
        plt.figure(figsize=(8, 5))
        cat_data = self.df.groupby("Category",index=False)["Total Sales"].sum()
        sns.barplot("Category","Total Sales",cat_data)
        plt.title("bar chart of total sales by product category")
        plt.xlabel("Product category")
        plt.ylabel("Total Sales Amount")
        plt.legend()
        plt.show()

        plt.figure(figsize=(10, 5))
        date_data =self.df.groupby("Date", index=False)["Total Sales"].sum()
        sns.lineplot("Date","Total Sales",date_data,marker="o",)
        plt.title("Line Graph:salles by time")
        plt.xlabel("Date")
        plt.ylabel("Total sales amount")
        plt.legend()
        plt.show()

        plt.figure(figsize=(6, 5))
        num_df =self.df[["Price", "Quantity Sold", "Total Sales"]]
        corr_mat =num_df.corr()
        sns.heatmap(corr_mat,anot=True)
        plt.title("Heatmap: Correlation Between Price and Quantity Sold")
        plt.xlabel("array")
        plt.ylabel("array")
        plt.legend()
        plt.show()

analyzer = retail_sales_analyzer()
while True:
    fname= input("enter retail sales csv file name: ")
    status= analyzer.load_data(fname)
    if status== True:
        break
    print("""
    1.calculate metrics
    2.display summary report
    3.filter data
    4.maps visualizations
    5.Show full cleaned dataset
    6.Exit Program""")
    ch = input("enter your choice:")
    if ch == "1":
        analyzer.calculate_metrics()
    elif ch == "2":
        analyzer.display_summary()
    elif ch == "3":
        analyzer.filter_data()
    elif ch == "4":
        analyzer.make_charts()
    elif ch == "6":
        print("thank you exiting retail analyzer...")
        break
    else:
        print("invalid choice ")  

       