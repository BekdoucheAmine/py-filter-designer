# Filter Designer

This repository contains a simple filter designer (built-with & hosted on streamlit)

## Repository structure

app: contains the streamlit app with all the source code  
docs: documentation (mainly how to use the app and how to improve it)  
tests: making sure that future edits doesn't break current functions through testcases  

## Intended design

This app-design focused on python-generated filter coefficients for FIR/IIR digital filters. This app relies on Scipy for calculating theses coefficients mainly the functions: (firwin, firwin2, firls, remez) More are to be added later

# Whats supported for now

- Filter types: FIR
- Design method: firwin
- Coefficient: float, fixed point, canonical signed digit, raw(scaled integers)
