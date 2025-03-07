import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import geopandas as gpd
from shapely.geometry import Point
import contextily as ctx
sns.set(style='dark')

with st.sidebar:
    # Multibox to select what data want to be shown
    genre = st.multiselect(
        label="Data Shown:",
        options=('Reviews Impact', 'Product Detail Impact', 'Geographics')
    )

# made-up name and description
st.title('ShopEase')
st.markdown('''ShopEase is your go-to online marketplace for a seamless and enjoyable shopping experience.
        We offer a wide range of high-quality products, from electronics and fashion to home essentials and beauty products. 
        With fast delivery, secure payment options, and excellent customer service, ShopEase ensures that your shopping journey is convenient, affordable, and hassle-free.''')

st.subheader('Sales Level')
st.markdown(
    '''
    Our sellers usually from South America while the customers may vary. The city with the most sales order is Sao Paulo.
    '''
)

# Import data
order_per_city = pd.read_csv("dashboard/order_per_city.csv")

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

home_fig, ax = plt.subplots()

sns.barplot(
    data=order_per_city.head(5), 
    y="customer_city", 
    x="order_id", 
    palette=colors,
    ax=ax
)

ax.set_xlabel("Number of Orders")
ax.set_ylabel("City")
ax.set_title("Top 5 Cities by Orders")
st.pyplot(home_fig)

st.markdown(
    '''
    For the other sales information, you can pick which data you want to display by checking the multibox on the sidebar.
    '''
)

# Display different sections based on selection        
if 'Reviews Impact' in genre:
    st.title('Reviews Impact Analysis')
    st.write("This section evaluates how reviews impact sales in two ways.")
    st.markdown(
        '''
        The first one is based on the good and bad products:
        - Good products: review score > 3
        - Bad products: review score <= 3
        

        The second way is by separating the products based on their average review score:
        - One-star products: review score between 1.0 to 1.5
        - Two-star products: review score between 1.5 to 2.5
        - Three-star products: review score between 2.5 to 3.5
        - Four-star products: review score between 3.5 to 4.5
        - Five-star products: review score between 4.5 to 5.0
        '''
    )

    # import data
    score_per_product = pd.read_csv("dashboard/score_per_product.csv", skiprows=1)
    score_per_product.columns = ["product_id", "order_id", "review_score_min", "review_score_max", "review_score_mean"]

    score_per_store = pd.read_csv("dashboard/score_per_store.csv", skiprows=1)
    score_per_store.columns = ["seller_id", "order_id", "review_score_min", "review_score_max", "review_score_mean"]

    # tabs to seperate the good vs bad product and each review score product
    tab1, tab2 = st.tabs(["Good vs Bad Review", "Each Review Score"])

    #============ Good vs Bad Product =================#
    with tab1:
        # Calculation
        # bad product
        bad_product = score_per_product[(score_per_product["review_score_mean"] <= 3.0)]

        sales_per_bad_product = bad_product["order_id"].sum()/bad_product["product_id"].nunique()

        sales_bad_product = bad_product["order_id"].sum()

        # good product
        good_product = score_per_product[(score_per_product["review_score_mean"] > 3.0)]

        sales_per_good_product = good_product["order_id"].sum()/good_product["product_id"].nunique()

        sales_good_product = good_product["order_id"].sum()

        # Create the bar plot to compare the total sales
        plot_data = pd.DataFrame({
            "Product Review": ["Good Review", "Bad Review"],
            "Total Sales": [float(sales_good_product), float(sales_bad_product)]
        })

        # Create fig and subplots
        good_bad_product_sales_fig, good_bad_product_sales_ax = plt.subplots(1, 2)

        sns.barplot(x="Product Review", y="Total Sales", data=plot_data, palette=["green", "red"],\
                    ax=good_bad_product_sales_ax[0])

        # Add labels and title
        good_bad_product_sales_ax[0].set_xlabel("Product Review")
        good_bad_product_sales_ax[0].set_ylabel("Total Sales")

        # Create the bar plot to compare the average sales
        plot_data = pd.DataFrame({
            "Product Review": ["Good Review", "Bad Review"],
            "Average Sales": [float(sales_per_good_product), float(sales_per_bad_product)]
        })

        sns.barplot(x="Product Review", y="Average Sales", data=plot_data, palette=["green", "red"],\
                    ax=good_bad_product_sales_ax[1])

        # Add labels and title
        good_bad_product_sales_ax[1].set_xlabel("Product Review")
        good_bad_product_sales_ax[1].set_ylabel("Average Sales")

        # Add a single title for both subplots
        good_bad_product_sales_fig.suptitle("Comparison of Sales for Good and Bad Reviewed Products", fontsize=14, fontweight="bold")

        # Adjust spacing between subplots
        plt.subplots_adjust(wspace=0.4)  

        # Show the plot
        st.pyplot(good_bad_product_sales_fig)

        # Add explanation
        with st.expander("See explanation"):
            st.markdown(
            '''
            The product with a good review (i.e., higher than 3) surpass the ones with bad review by a significant amount.
            '''
            )

    #============ Each Star Product =================#
    with tab2:
        # one star
        one_star_product = score_per_product[(score_per_product["review_score_mean"] >= 1.0) & (score_per_product["review_score_mean"] <= 1.5)]

        sales_per_one_star_product = one_star_product["order_id"].sum()/one_star_product["product_id"].nunique()

        sales_one_star_product = one_star_product["order_id"].sum()

        # two star
        two_star_product = score_per_product[(score_per_product["review_score_mean"] > 1.5) & (score_per_product["review_score_mean"] <= 2.5)]

        sales_per_two_star_product = two_star_product["order_id"].sum()/two_star_product["product_id"].nunique()

        sales_two_star_product = two_star_product["order_id"].sum()

        # three star
        three_star_product = score_per_product[(score_per_product["review_score_mean"] > 2.5) & (score_per_product["review_score_mean"] <= 3.5)]

        sales_per_three_star_product = three_star_product["order_id"].sum()/three_star_product["product_id"].nunique()

        sales_three_star_product = three_star_product["order_id"].sum()

        # four star
        four_star_product = score_per_product[(score_per_product["review_score_mean"] > 3.5) & (score_per_product["review_score_mean"] <= 4.5)]

        sales_per_four_star_product = four_star_product["order_id"].sum()/four_star_product["product_id"].nunique()

        sales_four_star_product = four_star_product["order_id"].sum()

        # five star
        five_star_product = score_per_product[(score_per_product["review_score_mean"] > 4.5) & (score_per_product["review_score_mean"] <= 5.0)]

        sales_per_five_star_product = five_star_product["order_id"].sum()/five_star_product["product_id"].nunique()

        sales_five_star_product = five_star_product["order_id"].sum()

        # Create fig and subplots
        each_product_sales_fig, each_product_sales_ax = plt.subplots(2, 1)
        
        # Create the bar plot to compare the total sales for each product
        plot_data = pd.DataFrame({
            "Product Review": ["One-star", "Two-star", "Three-star", "Four_star", "Five_star"],
            "Total Sales": [float(sales_one_star_product), float(sales_two_star_product), float(sales_three_star_product), float(sales_four_star_product), float(sales_five_star_product)]
        })
        sns.barplot(x="Product Review", y="Total Sales", data=plot_data, palette=["red", "red", "yellow", "green", "green"],\
                    ax=each_product_sales_ax[0])

        # Add labels
        each_product_sales_ax[0].set_xlabel("Product Review")
        each_product_sales_ax[0].set_ylabel("Total Sales")

        # Create the bar plot to compare the average sales for each product
        plot_data = pd.DataFrame({
            "Product Review": ["One-star", "Two-star", "Three-star", "Four_star", "Five_star"],
            "Average Sales": [float(sales_per_one_star_product), float(sales_per_two_star_product), float(sales_per_three_star_product), float(sales_per_four_star_product), float(sales_per_five_star_product)]
        })
        sns.barplot(x="Product Review", y="Average Sales", data=plot_data, palette=["red", "red", "yellow", "green", "green"],\
                    ax=each_product_sales_ax[1])

        # Add labels
        each_product_sales_ax[1].set_xlabel("Product Review")
        each_product_sales_ax[1].set_ylabel("Average Sales")

        # Add a single title for both subplots
        each_product_sales_fig.suptitle("Comparison of Sales for Each Review Score of Products", fontsize=14, fontweight="bold")

        # Adjust spacing between subplots
        plt.subplots_adjust(wspace=0.8)  

        # Show the plot
        st.pyplot(each_product_sales_fig)

        # Add explanation
        with st.expander("See explanation"):
            st.markdown(
            '''
            The product with more than 3-star review surpass the 1-star, 2-star, and 3-star review in both total and average sales.
            However, the most sales for both total and average is in the 4-star product. The 5-star product surprisingly has less sales than the
            4-star and 3-star product, but still better than the low star (i.e., 1-star and 2-star) product.
            '''
            )
    
    st.markdown(
        '''
        Review score also impacts the sales level of each seller.
        We only use the second way to analyze it to give a better insight.
        
        
        The sellers are separated based on their average review score:
        - One-star sellers: review score between 1.0 to 1.5
        - Two-star sellers: review score between 1.5 to 2.5
        - Three-star sellers: review score between 2.5 to 3.5
        - Four-star sellers: review score between 3.5 to 4.5
        - Five-star sellers: review score between 4.5 to 5.0
        '''
    )

    #========= Each Review Seller ===========#
    # one star
    one_star_store = score_per_store[(score_per_store["review_score_mean"] >= 1.0) & (score_per_store["review_score_mean"] <= 1.5)]

    sales_per_one_star_store = one_star_store["order_id"].sum()/one_star_store["seller_id"].nunique()

    sales_one_star_store = one_star_store["order_id"].sum()

    # two star
    two_star_store = score_per_store[(score_per_store["review_score_mean"] > 1.5) & (score_per_store["review_score_mean"] <= 2.5)]

    sales_per_two_star_store = two_star_store["order_id"].sum()/two_star_store["seller_id"].nunique()

    sales_two_star_store = two_star_store["order_id"].sum()

    # three star
    three_star_store = score_per_store[(score_per_store["review_score_mean"] > 2.5) & (score_per_store["review_score_mean"] <= 3.5)]

    sales_per_three_star_store = three_star_store["order_id"].sum()/three_star_store["seller_id"].nunique()

    sales_three_star_store = three_star_store["order_id"].sum()

    # four star
    four_star_store = score_per_store[(score_per_store["review_score_mean"] > 3.5) & (score_per_store["review_score_mean"] <= 4.5)]

    sales_per_four_star_store = four_star_store["order_id"].sum()/four_star_store["seller_id"].nunique()

    sales_four_star_store = four_star_store["order_id"].sum()

    # five star
    five_star_store = score_per_store[(score_per_store["review_score_mean"] > 4.5) & (score_per_store["review_score_mean"] <= 5.0)]

    sales_per_five_star_store = five_star_store["order_id"].sum()/five_star_store["seller_id"].nunique()

    sales_five_star_store = five_star_store["order_id"].sum()

    # Create fig and subplots
    each_store_sales_fig, each_store_sales_ax = plt.subplots(2, 1)
    
    # Create the bar plot to compare the total sales for each store
    plot_data = pd.DataFrame({
        "Store Review": ["One-star", "Two-star", "Three-star", "Four_star", "Five_star"],
        "Total Sales": [float(sales_one_star_store), float(sales_two_star_store), float(sales_three_star_store), float(sales_four_star_store), float(sales_five_star_store)]
    })
    sns.barplot(x="Store Review", y="Total Sales", data=plot_data, palette=["red", "red", "yellow", "green", "green"],\
                ax=each_store_sales_ax[0])

    # Add labels
    each_store_sales_ax[0].set_xlabel("Store Review")
    each_store_sales_ax[0].set_ylabel("Total Sales")

    # Create the bar plot to compare the average sales for each product
    plot_data = pd.DataFrame({
        "Store Review": ["One-star", "Two-star", "Three-star", "Four_star", "Five_star"],
        "Average Sales": [float(sales_per_one_star_store), float(sales_per_two_star_store), float(sales_per_three_star_store), float(sales_per_four_star_store), float(sales_per_five_star_store)]
    })
    sns.barplot(x="Store Review", y="Average Sales", data=plot_data, palette=["red", "red", "yellow", "green", "green"],\
                ax=each_store_sales_ax[1])

    # Add labels
    each_store_sales_ax[1].set_xlabel("Store Review")
    each_store_sales_ax[1].set_ylabel("Average Sales")

    # Add a single title for both subplots
    each_store_sales_fig.suptitle("Comparison of Sales for Good and Bad Reviewed Store", fontsize=14, fontweight="bold")

    # Adjust spacing between subplots
    plt.subplots_adjust(wspace=0.8)  

    # Show the plot
    st.pyplot(each_store_sales_fig)

    # Add Explanation
    with st.expander("See explanation"):
        st.markdown(
            '''
            The store with more than 3-star review surpass the 1-star, 2-star, and 3-star review in both total and average sales.
            However, the most sales for both total and average is in the 4-star store. The 5-star store surprisingly has less sales than the
            4-star and 3-star store, but still better than the low star (i.e., 1-star and 2-star) store.
            '''
        )

    # Add Conclusion
    st.subheader("Conclusion")
    st.markdown(
        '''
        From the above figures, we can see that the review score is mostly directly proportional to the total sales and average sales.
        This fact is true for both product review and store review.
        '''
    )

if 'Product Detail Impact' in genre:
    st.title('Product Detail Impact Analysis')
    st.write("This section explores how product details influence purchases.")

    st.markdown(
            '''
            The impact of product details are analyzed based on it's impact on review score and sales level.
            The review score impact is analyzed using box plot to give a better insight of the min, max, mean, or even outlier.
            The sales level is analyzed using bar plot to show a better comparison.
            '''
        )

    tab1, tab2 = st.tabs(["Review Score", "Sales Level"])

    with tab1:
        # ============= Product Detail to Review Score ========== #
        # import data
        detailed_product_review = pd.read_csv("dashboard/detailed_product_review.csv", skiprows=1)
        detailed_product_review.columns = ["product_id", "review_score_min", "review_score_max", "review_score_mean"]

        non_detailed_product_review = pd.read_csv("dashboard/non_detailed_product_review.csv", skiprows=1)
        non_detailed_product_review.columns = ["product_id", "review_score_min", "review_score_max", "review_score_mean"]

        # Create a boxplot with 1 row and 2 columns of subplots
        detail_to_review_fig, detail_to_review_ax = plt.subplots(1, 2, figsize=(12, 6))

        # Boxplot for detailed_review
        sns.boxplot(data=detailed_product_review, y=detailed_product_review["review_score_mean"], ax=detail_to_review_ax[0], palette="Set2")
        detail_to_review_ax[0].set_ylabel("Review Score")
        detail_to_review_ax[0].set_xlabel("Detailed Product")

        # Boxplot for non_detailed_review
        sns.boxplot(data=non_detailed_product_review, y=non_detailed_product_review["review_score_mean"], ax=detail_to_review_ax[1], palette="Set1")
        detail_to_review_ax[1].set_ylabel("Review Score")
        detail_to_review_ax[1].set_xlabel("Non Detailed Product")

        # Add a single title for both subplots
        detail_to_review_fig.suptitle("Comparison of Review Score: Detailed vs Non Detailed Products", fontsize=14, fontweight="bold")

        # Adjust spacing between subplots
        plt.subplots_adjust(wspace=0.8)  

        st.pyplot(detail_to_review_fig)

        # Add Explanation
        with st.expander("See explanation"):
            st.markdown(
                '''
                The products with detailed information have a better review score than the one with non-detailed information.
                Its review scores mostly spread from 5-star to approximately 3.6-star, while the non-detailed products spread
                from 5-star to approximately 3-star. The average review score of the detailed products also better for approximatelly 4.65%.
                '''
            )
    
    with tab2:
        # ============= Product Detail to Sales Level ========== #
        # import data
        detailed_product_sales = pd.read_csv("dashboard/detailed_product_sales.csv")
        # detailed_product_sales.columns = ["product_id", "review_score_min", "review_score_max", "review_score_mean"]

        non_detailed_product_sales = pd.read_csv("dashboard/non_detailed_product_sales.csv")
        # non_detailed_product_sales.columns = ["product_id", "review_score_min", "review_score_max", "review_score_mean"]

        # Compute mean sales
        detailed_product_mean_sales = detailed_product_sales["order_id"].mean()
        non_detailed_product_mean_sales = non_detailed_product_sales["order_id"].mean()

        # Create a DataFrame for plotting
        sales_data = pd.DataFrame({
            "Product Type": ["Detailed Product", "Non-Detailed Product"],
            "Sales Value": [detailed_product_mean_sales, non_detailed_product_mean_sales]
        })

        # Create subplots
        detail_to_sales_fig, detail_to_sales_ax = plt.subplots(figsize=(12, 6))

        # Plot using Seaborn
        sns.barplot(data=sales_data, x="Product Type", y="Sales Value", palette=["green", "red"])

        # Add labels and title
        detail_to_sales_ax.set_xlabel("Product Type")
        detail_to_sales_ax.set_ylabel("Average Sales")
        detail_to_sales_ax.set_title("Comparison of The Average Sales: Detailed vs Non-Detailed Products")

        st.pyplot(detail_to_sales_fig)

        with st.expander("See explanation"):
            st.markdown(
                '''
                The products with detailed information have a better average sales than the one with non-detailed information
                for approximately 37.2%.
                '''
            )
        
    # Add conclusion
    st.subheader("Conclusion")
    st.markdown(
        '''
        The detail information about each product significantly affects the total sales but slightly affects review score.
        '''
    )

if 'Geographics' in genre:
    st.title('Geographics Analysis')
    st.write("This section analyzes geographics data.")

    # Import data
    geolocation_df = pd.read_csv("dashboard/geolocation_df.csv")
    customers_geo_count = pd.read_csv("dashboard/customers_geo_count.csv")
    sellers_geo_count = pd.read_csv("dashboard/sellers_geo_count.csv")

    # Create tabs for seller and costumer geographics
    tab1, tab2 = st.tabs(["Customers", "Sellers"])

    with tab1:
        # ==== Top 20 Customers ==== #
        top_20_cities = order_per_city.head(20)

        top_20_cities_geo_df = geolocation_df[geolocation_df["geolocation_city"].isin(top_20_cities["customer_city"])]
        
        # Convert to GeoDataFrame
        top_city_geolocation_gdf = gpd.GeoDataFrame(
            top_20_cities_geo_df, 
            geometry=gpd.points_from_xy(top_20_cities_geo_df["geolocation_lng"], top_20_cities_geo_df["geolocation_lat"])
        )

        # Set a coordinate reference system (CRS) - WGS 84
        top_city_geolocation_gdf.set_crs(epsg=4326, inplace=True)

        # Plot the locations
        fig, ax = plt.subplots(figsize=(10, 6))

        top_city_geolocation_gdf.to_crs(epsg=3857).plot(ax=ax, markersize=5, alpha=0.5, cmap="Reds")

        # Add basemap
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        # Add title
        ax.set_title("Geolocation of Top 20 Orders")
        st.pyplot(fig)

        # Add Explanation
        with st.expander("See explanation"):
            st.markdown(
                '''
                It can be seen that most customers are located near the coast.
                The darker the red color, the higher the number of buyers in that area.
                '''
            )
    with tab2:
        # ==== Top 20 Sellers ==== #
        top_20_sellers = sellers_geo_count.head(20)

        # top_20_sellers_geo_df = geolocation_df[geolocation_df["geolocation_city"].isin(top_20_sellers["seller_city"])]
        
        # Convert to GeoDataFrame
        sellers_geolocation_gdf = gpd.GeoDataFrame(
            top_20_sellers, 
            geometry=gpd.points_from_xy(top_20_sellers["geolocation_lng"], top_20_sellers["geolocation_lat"])
        )

        # Set a coordinate reference system (CRS) - WGS 84
        sellers_geolocation_gdf.set_crs(epsg=4326, inplace=True)

        # Plot the locations
        fig, ax = plt.subplots(figsize=(10, 6))

        sellers_geolocation_gdf.to_crs(epsg=3857).plot(ax=ax, markersize=20, alpha=0.5, cmap="Reds")

        # Add basemap
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        # Add title
        ax.set_title("Geolocation of Top 20 Sellers")
        st.pyplot(fig)

        # Add Explanation
        with st.expander("See explanation"):
            st.markdown(
                '''
                It can be seen that the top 20 sellers are located near Ibitinga, which is a city in the state of São Paulo, 
                Brazil and pretty far from the coast.
                '''
            )
    
    # Add Conclusion
    st.subheader("Conclusion")
    st.markdown(
        '''
        It can be seen that most top 20 cities located near the coast, while the 20 top sellers located pretty far from the top cities.
        The reason why those top 20 cities have more order may be caused by the lack of resources near their area.
        '''
    )
