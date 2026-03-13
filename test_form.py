import streamlit as st

def test_simple_form():
    """Test simple form to isolate the issue"""
    st.title("🧪 Form Test")
    
    with st.form("test_form"):
        st.write("This is a test form")
        
        name = st.text_input("Name")
        age = st.slider("Age", 1, 100)
        
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            st.success(f"Form submitted! Name: {name}, Age: {age}")

if __name__ == "__main__":
    test_simple_form()
