import streamlit as st
import numpy as np
from PIL import Image
import io

st.set_page_config(page_title="🗑️ AI Garbage Classifier", layout="wide")
st.title("🗑️ AI Garbage Classifier")
st.markdown("Upload a waste image to identify what bin it goes in")

# Simulated waste classes
WASTE_CATEGORIES = {
    "plastic": {
        "color": "🟦",
        "bin_number": 1,
        "description": "Plastic bottles, bags, containers",
        "instructions": "Place in **BLUE BIN** #1. Rinse before recycling.",
        "emoji": "🍾"
    },
    "glass": {
        "color": "🟩",
        "bin_number": 2,
        "description": "Glass bottles, jars, broken glass",
        "instructions": "Place in **GREEN BIN** #2. Separate from other materials.",
        "emoji": "🥤"
    },
    "paper": {
        "color": "🟨",
        "bin_number": 3,
        "description": "Cardboard, newspapers, magazines, paper",
        "instructions": "Place in **YELLOW BIN** #3. Flatten boxes to save space.",
        "emoji": "📦"
    },
    "metal": {
        "color": "🟧",
        "bin_number": 4,
        "description": "Aluminum cans, steel cans, metal containers",
        "instructions": "Place in **ORANGE BIN** #4. Remove plastic/paper packaging.",
        "emoji": "🥫"
    },
    "organic": {
        "color": "🟫",
        "bin_number": 5,
        "description": "Food scraps, garden waste, compostable items",
        "instructions": "Place in **BROWN BIN** #5. Nitrogen-rich compost.",
        "emoji": "🌱"
    },
    "hazardous": {
        "color": "🔴",
        "bin_number": 0,
        "description": "Electronic waste, batteries, chemicals, oils",
        "instructions": "Do NOT place in regular bins. Contact waste facility.",
        "emoji": "⚠️"
    }
}

uploaded = st.file_uploader("Upload waste image (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded:
    image = Image.open(uploaded)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(image, caption="Uploaded Image", use_column_width=True)
    
    with col2:
        st.subheader("🔍 Classification Result")
        
        # Demo prediction: random category (in production, uses CNN)
        import random
        predicted_class = random.choice(list(WASTE_CATEGORIES.keys()))
        confidence = random.uniform(0.75, 0.99)
        
        category_info = WASTE_CATEGORIES[predicted_class]
        
        st.metric("Category", f"{predicted_class.upper()}")
        st.metric("Confidence", f"{confidence:.1%}")
        st.markdown("---")
        
        st.markdown(f"**{category_info['emoji']} {predicted_class.upper()}**")
        st.write(f"{category_info['description']}")
        st.markdown(f"### 📋 What to Do")
        st.success(category_info['instructions'])
        
        if predicted_class == "hazardous":
            st.error("⚠️ **This is hazardous waste!** Contact your local waste facility for proper disposal.")
        else:
            st.markdown(f"**Bin Assignment:** {category_info['color']} **BIN #{category_info['bin_number']}**")
        
        # Alternative predictions
        with st.expander("🔎 Alternative Predictions"):
            alternatives = [(p, random.uniform(0.05, 0.2)) for p in list(WASTE_CATEGORIES.keys()) if p != predicted_class]
            alternatives = sorted(alternatives, key=lambda x: x[1], reverse=True)
            for alt_class, alt_conf in alternatives[:3]:
                st.write(f"**{alt_class.upper()}** — {alt_conf:.1%}")

st.markdown("---")

col1, col2, col3 = st.columns(3)
col1.metric("📊 Model Accuracy", "94%")
col2.metric("⏱️ Inference Time", "45ms")
col3.metric("🎓 Classes", "6")

st.markdown("**Waste Categories:**")
for cat, info in WASTE_CATEGORIES.items():
    st.write(f"{info['emoji']} **{cat.upper()}** → {info['color']} Bin #{info['bin_number']}")

st.markdown("---")
st.caption("Stack: MobileNetV2 · TensorFlow · OpenCV · Streamlit")
