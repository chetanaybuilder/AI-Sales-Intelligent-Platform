# all the important tools we need 

import pandas as pd
from google import genai
import os

# adding ai brain to our project
print("=" * 70)
print("          AI SALES INTELLIGENCE PLATFORM")
print("     Enterprise E-Commerce Analytics & AI Assistant")
print("                 Version 1.0.0")
print("=" * 70)
print()
client = genai.Client(api_key="paste_your_key_here")
personality = ("""You are SalesMind AI, an elite E-commerce Sales Intelligence Consultant.

Your job is to analyze sales data and help business owners increase revenue, profit, and business growth.

Rules:

• Always answer professionally.
• Give practical business advice, not generic AI responses.
• Base every recommendation on the provided sales data.
• Explain WHY a product performs well or poo *rly.
• Suggest ways to increase revenue and profit.
• Identify best-selling and worst-selling products.
• Recommend marketing, pricing, inventory, bundling, discounts, and upselling strategies.
• If data is insufficient, clearly say what additional data is needed.
• Never invent numbers that are not present in the dataset.
• Keep answers concise, actionable, and business-focused.
• Use bullet points whenever possible.
• Think like a senior business analyst working for a million-dollar e-commerce company.
Your goal is to help businesses make smarter decisions using data""")
try:
# using pandas so it can perform calculations and read the csv file.

   data = pd.read_csv("sales.csv.txt")
except FileNotFoundError:
    print("error csv file not found check its location again!")
    exit()
    print("===========================================")
    print(" AI ANALYSIS 💳")
    print("============================================")

try:
# peforming basic calculations and overall ai analysis

    data["Revenue"] = data["Price"] * data["Units_Sold"]
    category_revenue = data.groupby("Category")["Revenue"].sum()
    data["profit"] = data["Revenue"] - data["Cost"]
    category_profit = data.groupby("Category")["profit"].sum()
    best_product = data.loc[data["Revenue"].idxmax()]
    worst_product = data.loc[data["Revenue"].idxmin()]
    total_revenue = data["Revenue"].sum()
    average_order = data["Revenue"].mean()
    total_quantity = data["Units_Sold"].sum()
    most_sold = data.loc[data["Units_Sold"].idxmax()]
    least_sold = data.loc[data["Units_Sold"].idxmin()]
    average_profit = data["profit"].mean()
    total_cost = data["Cost"].sum()
    total_orders = len(data["Revenue"])
    top_3_products = data.sort_values("Revenue", ascending=False).head(3)

# if a column name doesnt match the csv,tell the user exactly which one is missing

except KeyError as e:
    print(f"error: missing column {e}")
    exit()
# printing all ai sales data here
print("=====================================================")
print("AI OVERVIEW 💸")
print("======================================================")

print(" best product 👑 ")
print(best_product)
print("worst product 🤮 ")
print(worst_product)
print("total revenue 💰 ")
print(total_revenue)
print("average_order 💲 ")
print(average_order)
print("total_orders  🥳  ")
print(total_orders)
print("top 3 best products 🙌 ")
print(top_3_products)
print("total profit 💎")
print(data["profit"].sum())
print("category revenue  💲 ")
print(category_revenue)
print("category profit 💲 ")
print(category_profit)
print("total quantity sold 🥳 ")
print(total_quantity)
print("most sold product 💲")
print(most_sold)
print("least sold product 😭 ")
print(least_sold)
print("average profit  💸")
print(average_profit)
print("total cost 💸 ")
print(total_cost)
# final ai chatbot work
while True:
# keep  asking  users for new question forever,until they close the program

    question = input("ask me something about sales! ")
    prompt = personality + f"""
    best product : {best_product['Product']},Revenue :{best_product['Revenue']}
    worst product : {worst_product['Product']},Revenue :{worst_product['Revenue']}
    total revenue : {total_revenue}
    average order : {average_order}
    most sold product : {most_sold['Product']},units sold:{most_sold['Units_Sold']}
    least sold product : {least_sold['Product']},units sold:{least_sold['Units_Sold']}
    total order : {total_orders}
    Category revenue: {category_revenue.to_dict()}
    Category profit: {category_profit.to_dict()}
    Top 3 products by revenue: {top_3_products[['Product', 'Revenue']].to_dict('records')}
    user question : {question} """
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    print(response.text)

    







     
     
     

