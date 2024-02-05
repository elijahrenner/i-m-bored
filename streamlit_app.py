import streamlit as st
import streamlit.components.v1 as components
from annotated_text import annotated_text

from openai import OpenAI
import os
from datetime import date
import random

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

hobbies = [
    '📚 Reading', '✍️ Writing', '✏️ Drawing', '🎨 Painting', '📷 Photography', '🍳 Cooking', '🍰 Baking',
    '🌱 Gardening', '🧶 Knitting', '🪡 Crocheting', '🧵 Sewing', '🪵 Woodworking', '🎻 Playing an Instrument',
    '🎤 Singing', '💃 Dancing', '🎭 Acting', '🥾 Hiking', '🏕️ Camping', '🎣 Fishing', '🐦 Bird Watching',
    '🌌 Stargazing', '💌 Collecting Stamps', '💰 Collecting Coins', '📬 Collecting Postcards',
    '🕰️ Collecting Vintage Items', '♟️ Chess', '🎲 Board Games', '🃏 Card Games', '🧩 Puzzle Solving',
    '📖 Scrapbooking', '✒️ Calligraphy', '🎈 Origami', '🛠️ Model Building', '🕯️ Candle Making', '🧼 Soap Making',
    '🏺 Pottery', '🏺 Ceramics', '🧵 Quilting', '🛠️ Metalworking', '🏡 DIY Home Decor', '🍺 Home Brewing',
    '🍷 Wine Tasting', '🍺 Beer Tasting', '🪑 Furniture Restoration', '💻 Digital Art', '🎨 Graphic Design',
    '🌐 Web Development', '📱 App Development', '💻 Programming', '🤖 Robotics', '🌐 Virtual Reality',
    '🌐 Augmented Reality', '🖨️ 3D Printing', '🕹️ VR Gaming', '🕹️ AR Gaming', '🎥 Video Editing',
    '🎞️ Animation', '🎮 Game Development', '📚 Reading Comics', '💬 Collecting Comics', '🎭 Cosplaying',
    '👗 Costume Design', '💄 Makeup Artistry', '🎭 Special Effects Makeup', '📸 Photomanipulation',
    '📈 Digital Marketing', '📱 Social Media Management', '📝 Blogging', '🎥 Vlogging', '🎙️ Podcasting',
    '🎤 Public Speaking', '🎉 Event Planning', '✈️ Traveling', '🏚️ Exploring Abandoned Places',
    '🚴 Cycling', '🏃 Running', '🏊 Swimming', '🧘 Yoga', '🧘 Meditation', '🤸 Pilates', '🏋️ Weightlifting',
    '🏋️‍♂️ Crossfit', '🥋 Martial Arts', '🏹 Archery', '⛷️ Skiing', '🏂 Snowboarding', '🏄 Surfing', '🛹 Skateboarding',
    '🧗 Rock Climbing', '❄️ Ice Climbing', '🤿 Scuba Diving', '🤿 Snorkeling', '🛶 Canoeing', '🚣 Kayaking',
    '🪂 Skydiving', '🪂 Paragliding', '🏗️ Bungee Jumping', '🎈 Hot Air Ballooning', '🪂 Hang Gliding',
    '🤸‍♂️ Zip Lining', '⛵ Sailing', '🏍️ Motorcycling', '🏎️ Car Racing', '🚗 Auto Detailing', '🚗 Antique Cars',
    '🌌 Astronomy', '📷 Astrophotography', '🌦️ Meteorology', '🌧️ Weather Watching', '💰 Numismatics','🌳 Genealogy', 
    '🗺️ Geocaching', '🕵️ Metal Detecting', '🏢 Urban Exploration',
    '🐦 Bird Keeping', '🐠 Aquarium Keeping', '🌵 Terrarium Keeping', '🦎 Reptile Keeping', '📻 Amateur Radio',
    '🔐 Cryptography', '🔓 Lock Picking', '🎩 Magic Tricks', '🤹 Juggling', '🎪 Circus Arts', '🔥 Fire Spinning',
    '🪁 Kite Flying', '🔄 Boomerang Throwing', '🦅 Falconry', '🏇 Horseback Riding', '🦴 Fossil Hunting',
    '🤲 Volunteer Work', '💰 Charity Fundraising', '🐕 Dog Training', '📸 Pet Photography',
    '🦁 Wildlife Conservation', '🌳 Planting Trees', '🌍 Environmental Cleanup', '🏖️ Beach Cleanup',
    '🍳 Culinary Arts', '🍷 Wine Making', '🧀 Cheese Making', '🍫 Chocolate Making', '🍵 Tea Blending',
    '☕ Coffee Roasting', '📸 Food Photography', '👨‍🍳 Gourmet Cooking', '🍷 Wine Pairing', '🍲 Food Blogging',
    '📚 Teaching', '👥 Mentoring', '📚 Tutoring', '🗣️ Language Learning', '🏰 Historical Reenactment',
    '🎭 Role-playing Games', '⚔️ LARPing', '🤺 Fencing', '🎯 Marksmanship', '🎯 Shooting Sports',
    '🎮 Radio Controlled Models', '🚁 Drone Flying', '♍ Astrology', '🔮 Tarot Reading', '🖐️ Palmistry',
    '🌀 Hypnosis', '📜 Writing Poetry', '📜 Haiku Writing', '📖 Storytelling', '📝 Novel Writing',
    '🎭 Playwriting', '📝 Screenwriting', '📓 Journaling', '📔 Scrapbook Journaling', '💭 Dream Journaling',
    '📬 Pen Palling', '🎗️ Origami Folding', '✂️ Paper Cutting', '🌌 Metal Clay Jewelry Making',
    '💎 Beading', '🔗 Wire Wrapping', '🪶 Stone Carving', '💎 Gemstone Cutting', '🪶 Lapidary',
    '🏡 Birdhouse Building', '🪁 Kite Making', '🌿 Botany', '🌿 Herb Gardening', '🌵 Cactus Collecting',
    '🪢 Hammock Making', '🪢 Paracord Crafts', '🧺 Basket Weaving', '🪑 Wood Carving', '🏺 Ceramic Sculpture',
    '🔥 Glass Blowing', '🌳 Bonsai Cultivation', '♻️ Feng Shui', '🏠 Home Automation', '🤖 Robot Building',
    '🔧 Antique Restoration', '👗 Vintage Clothing Restoration', '🔥 Welding', '🔩 Metal Sculpture',
    '📓 Bullet Journaling', '🤿 Scuba Diving Photography', '🧺 Underwater Basket Weaving',
    '🎵 Vintage Record Collecting', '📷 Vintage Camera Collecting', '🎵 Record Label Creation',
    '🎮 Retro Gaming', '🕹️ Arcade Cabinet Building', '⚙️ Mechanical Keyboards', '🦑 Call of Cthulhu',
    '🔐 Escape Room Design', '📚 Bookbinding', '🗺️ Cartography', '🎨 Graffiti Art', '🎨 Street Art',
    '🖼️ Photorealistic Drawing', '🎨 Abstract Art', '🌀 Surrealism', '🎨 Impressionism', '🎨 Watercolor Painting',
    '🎨 Oil Painting', '🎨 Acrylic Painting', '🎨 Mixed Media Art', '🎨 Collage Art', '💻 Digital Painting',
    '💡 Neon Art', '🔄 Kinetic Art', '🔊 Sound Art', '🔄 Interactive Art', '🌐 Projection Mapping',
    '🛠️ DIY Electronics', '🎵 Electronic Music Production', '🔄 Circuit Bending', '🔮 Holography',
    '🎛️ VJing', '🎞️ 3D Animation', '🎈 Paper Mache Sculpture', '🏖️ Sand Sculpture', '❄️ Ice Sculpture',
    '🎈 Balloon Sculpture', '🎭 Puppetry', '🎭 Marionette Making', '👥 Shadow Puppetry', '🎞️ Stop Motion Animation',
    '🧱 LEGO Building', '🚂 Model Railroad Building', '🎪 Diorama Making', '🔩 Kintsugi', '🧵 Sashiko Embroidery',
    '🎨 Batik', '🎨 Shibori Dyeing', '🏺 Sculptural Ceramics', '💍 Enamel Jewelry Making', '👢 Leatherworking',
    '🔗 Chainmaille Jewelry', '🔬 Polymer Clay Crafts', '🌀 Quilling', '🎨 Glass Etching', '🎨 Glass Painting',
    '🪵 Wood Burning', '🔥 Pyrography', '⚙️ Steampunk Crafting', '👥 Cosplay Crafting', '🛡️ Foam Armor Making',
    '🛡️ Chainmail Armor Crafting', '⚔️ LARP Weapon Crafting', '🎨 Miniature Painting', '⚔️ Warhammer 40k',
    '🚢 Model Ship Building', '🛩️ Model Airplane Building', '🛡️ Model Tank Building', '🚗 Model Car Building',
    '🚀 Model Rocketry', '🔭 Astronomical Observing', '📸 Astroimaging', '📡 Radio Astronomy', '🔭 Amateur Astronomy',
    '💰 Numismatic Collecting', '💰 Philatelic Collecting', '🚂 Model Train Collecting', '🏎️ Hot Rod Building',
    '🏁 Drag Racing', '🚚 Truck Customization', '🏍️ Motorcycle Customization', '🚗 Classic Car Restoration',
    '🌞 Alternative Energy', '☀️ Solar Power'
]

def main():
    st.set_page_config(page_title="I'm Bored", page_icon="🥱", layout="centered")
    
    st.title("I'm Bored 🥱")
    st.subheader("Bored? Let's find a project!")
    
    st.divider()
    HOBBY = ""
    selected_hobby = st.selectbox("Select from our list of hobbies.", ['', *hobbies])
    if selected_hobby == '':
        custom_hobby = st.text_input("Or, enter your own!")

        # If the user entered a custom hobby, update the selected_hobby variable
        if custom_hobby:
            HOBBY = custom_hobby
            st.write(f"Hobby: {HOBBY}")
        else:
            st.warning('Be sure to select a hobby!', icon="⚠️")
    else:
        HOBBY = selected_hobby
        st.write(f"Hobby: {HOBBY}")
    st.divider()
    PURPOSE = st.select_slider(
      "What's the project's purpose?",
      options = ['🏋️ Practice', '📚 Educational', '🎓 Fun-Educational', '🎉 Entertaining', '✨ Whimsical'],
      value = '🎓 Fun-Educational')
    st.divider()
    AUDIENCE = st.select_slider(
      "Who do you want to show this to?",
      options = ['📚 Academic', '👨‍💼 Friends/Family', '💼 Work'],
      value = '👨‍💼 Friends/Family')
    st.divider()
    UNIQUENESS = st.select_slider(
      "What type of project?",
      options = ['🌐 Very Common', '🔄 Common', '📊 Normal', '🔍 Uncommon', '🚀 Highly Original'],
      value = '📊 Normal')
    st.divider()
    HOURS = st.number_input("How long should it take? (Hours)", value = 1, min_value = 1)

    st.divider()
    if st.button("Generate Idea"):
        generate_idea(HOBBY, PURPOSE, AUDIENCE, UNIQUENESS, HOURS)

def generate_idea(HOBBY, PURPOSE, AUDIENCE, UNIQUENESS, HOURS):
    PROMPT = f"Propose a {UNIQUENESS} idea for a {PURPOSE} {HOBBY} project attainable in {HOURS} hours, encapsulated in a concise sentence (max 10 words), designed to captivate a {AUDIENCE} audience."

    # st.text("Generated Prompt:")
    # st.text(PROMPT)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're a person with extremely great ideas. Everyone needs ideas, and you're the one who has them. Provide a user with ideas relevant to their interests"},
            {"role": "user", "content": PROMPT}
        ]
    )
    st.divider()
    annotated_text(
    "Here's your ",
    (f"{UNIQUENESS}", "uniqueness"),
    "",
    (f"{HOBBY}", "hobby"),
    " project for ",
    (f"{PURPOSE}", "purpose(s)"),
    " to showcase in a ",
    (f"{AUDIENCE}", "environment"),
    " achievable in ",
    (f"{HOURS}", "hours "),
    ". ",
    "You've gotta try it!"
    )
    content_with_quotes = str(completion.choices[0].message.content)
    content_without_quotes = content_with_quotes[1:-1] if content_with_quotes.startswith('"') and content_with_quotes.endswith('"') else content_with_quotes
    st.subheader(content_without_quotes)
    st.divider()
    st.link_button("by Elijah Renner", "https://elijahrenner.com")


if __name__ == "__main__":
    main()
