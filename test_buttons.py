#!/usr/bin/env python3
"""
Test script to verify button functionality in AI Study Planner
"""

import streamlit as st
import sys
import os

def test_button_functionality():
    """Test if all button handlers work correctly"""
    
    st.title("🧪 Button Functionality Test")
    
    # Initialize session state for testing
    if 'test_counter' not in st.session_state:
        st.session_state.test_counter = 0
    
    st.markdown("### Testing Button Handlers")
    
    # Test navigation handler
    if st.button("Test Navigation (Go to Home)", key="test_nav"):
        st.session_state.current_page = "Home"
        st.success("✅ Navigation button works!")
        st.rerun()
    
    # Test simple counter
    if st.button("Test Counter", key="test_counter_btn"):
        st.session_state.test_counter += 1
        st.success(f"✅ Counter button works! Count: {st.session_state.test_counter}")
        st.rerun()
    
    # Test form submission
    with st.form("test_form"):
        st.text_input("Test Input", key="test_input")
        submitted = st.form_submit_button("Test Form Submit")
        
        if submitted:
            st.success("✅ Form submission works!")
            st.write(f"Input value: {st.session_state.test_input}")
    
    # Test checkbox
    if st.checkbox("Test Checkbox", key="test_checkbox"):
        st.success("✅ Checkbox works!")
    
    # Test download button
    test_data = "Test CSV Content\nColumn1,Column2\nValue1,Value2"
    st.download_button(
        label="Test Download",
        data=test_data,
        file_name="test.csv",
        mime="text/csv"
    )
    
    # Show current session state
    st.markdown("### Current Session State")
    st.json(st.session_state)

if __name__ == "__main__":
    test_button_functionality()
