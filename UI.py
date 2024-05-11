import streamlit as st
import requests

# Define the URL of your FastAPI server
FASTAPI_URL = "http://localhost:8000"


# Streamlit UI for adding item to cart
def add_to_cart():
    st.title("Add Item to Cart")

    # Call the /opencv endpoint to scan barcode
    btn = st.button("scan")
    if btn:
        response_opencv = requests.get(f"{FASTAPI_URL}/opencv")
        if response_opencv.status_code == 200:
            barcode_data = response_opencv.json().get('text_barcode')
            if barcode_data:
                payload = {"cart_item": barcode_data}
                response_add_to_cart = requests.post(f"{FASTAPI_URL}/AddCart/", json=payload)
                if response_add_to_cart.status_code == 200:
                    st.success("Item added to cart successfully.")
                    # Show the cart items after adding to cart
                    view_cart()
                else:
                    st.error("Failed to add item to cart.")
            else:
                st.warning("No barcode detected.")
        else:
            st.error("Failed to scan barcode.")


def purchase():
    btnpurchase = st.button("Purchase")
    if btnpurchase:
        response_purchase = requests.get(f"{FASTAPI_URL}/purchase/")
        if response_purchase.status_code == 200:
            st.success("Items purchased successfully.")
            response_total = requests.get(f"{FASTAPI_URL}/total/")
            if response_total.status_code == 200:
                total_cost = response_total.json().get('TotalCost')
                st.write(f"Total Cost: ${total_cost}")
            else:
                st.error("Failed to fetch total cost.")
        else:
            st.error("Failed to purchase items.")


# Streamlit UI for viewing cart
def view_cart():
    st.title("View Cart")
    st.write("Your Cart:")

    response = requests.get(f"{FASTAPI_URL}/Cart/")
    if response.status_code == 200:
        cart_items = response.json()
        st.table(cart_items)
    else:
        st.write("Failed to fetch cart items.")


def clear():
    btnclear = st.button("clear")
    if btnclear:
        response = requests.get(f"{FASTAPI_URL}/clearPurchase/")
        if response.status_code == 200:
            st.success("clear Purchase ")
# Main function
def main():
    add_to_cart()
    purchase()
    clear()


if __name__ == "__main__":
    main()
