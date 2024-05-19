import streamlit as st
from openai import OpenAI
import base64

# Initialize OpenAI client
client = OpenAI(api_key='<ADD YOUR OWN KEY>')  # Make sure to replace with your OpenAI API key

# Define predefined messages and descriptions for each role
role_details = {
    "Safety Alerter 🚨": {
        "description": "Safety Alerter: This role analyzes the image feed for any safety violations and alerts if any are found, citing specific safety codes and policies. 🛡️",
        "message": "You are a safety alerter AI. You look at pictures from a camera feed and say RED alert if any safety violations are occurring and also mention the safety violation and how to avoid. Cite any violation rules and policies by code. If there is no danger and everything looks normal just respond with Situation Normal."
    },
    "Meal Planner 🍲": {
        "description": "Meal Planner: This role analyzes the captured image of ingredients and suggests a recipe based on the available ingredients. 🍲",
        "message": "You are a meal planner AI. You will be provided with a photo of a pantry or refrigirator, try to gather the ingredients present,you need to suggest a recipe based on those ingredients. If some essential ingredient is missing, suggest alternatives or inform the user."
    },
    "Know It All 📚": {
        "description": "GENERAL USE CASE - Material Identifier: This role analyzes the captured image to identify the materials and components that make up the objects in the image, such as plastic, metal, glass, etc. 📚 Additionally, provide details on when such an invention occurred and two lines about the science principles involved.",
        "message": "You are a material identifier AI. You will be provided with an image, and you need to identify the components and materials that make up the objects in the image, such as plastic, metal, glass, etc. Additionally, provide details on when such an invention occurred and two lines about the science principles involved."
    }
}

def analyze_image(role_message, image_data):
    # Create the chat completion request with the image data
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f"{role_message}"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].message.content

def main():
    # Title of the app
    st.title("Role-Based Message and Image Analysis App")

    # Sidebar for role selection
    st.sidebar.title("Select Role")
    role = st.sidebar.radio(
        "Role",
        ("Safety Alerter 🚨", "Meal Planner 🍲", "Know It All 📚")
    )

    st.sidebar.write(role_details[role]["description"])

    # Image input options
    st.write("## Upload or Capture an Image")
    img_file_buffer = st.camera_input("Take a picture")
    uploaded_file = st.file_uploader("Or upload a picture", type=["jpg", "jpeg", "png"])

    if st.button("Analyze"):
        if img_file_buffer is not None or uploaded_file is not None:
            if img_file_buffer is not None:
                # Read image file buffer as bytes
                bytes_data = img_file_buffer.getvalue()
            else:
                # Read uploaded file as bytes
                bytes_data = uploaded_file.read()
                
            # Convert the image to base64
            image_data = base64.b64encode(bytes_data).decode('utf-8')
            
            # Display the captured or uploaded image at a smaller size
            st.image(bytes_data, caption="Selected Image.", use_column_width=False, width=300)
            st.write(f"You selected {role}")

            # Get the role-specific message
            role_message = role_details[role]["message"]

            # Get the AI response
            ai_response = analyze_image(role_message, image_data)

            # Display the AI response
            st.write(ai_response)
        else:
            st.write("No image selected. Please upload or capture an image.")

if __name__ == "__main__":
    main()
