import streamlit as st
import requests

st.set_page_config(page_title="🎨 Explore Artworks with MET Museum API", page_icon="🖼️")

st.title("🎨 Explore Artworks with MET Museum API")
st.write("🔍 MET Museum의 Open API를 이용해 예술 작품을 탐색해보세요.")

query = st.text_input("작품이나 작가 이름을 입력하세요", placeholder="예: Van Gogh, Cat, Korea")

if query:
    with st.spinner("검색 중..."):
        # 1️⃣ Object ID 검색
        search_url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={query}"
        res = requests.get(search_url)
        data = res.json()

        if data["total"] == 0:
            st.warning("검색 결과가 없습니다.")
        else:
            st.success(f"{data['total']}개의 작품 중 일부를 표시합니다.")

            object_ids = data["objectIDs"][:10]  # 상위 10개만
            for object_id in object_ids:
                object_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
                obj_res = requests.get(object_url)
                obj = obj_res.json()

                # 이미지가 있을 때만 표시
                if obj.get("primaryImageSmall"):
                    st.image(obj["primaryImageSmall"], width=300)
                    st.markdown(f"**{obj.get('title', 'Untitled')}**")
                    st.caption(f"{obj.get('artistDisplayName', 'Unknown')} ({obj.get('objectDate', '')})")
                    st.markdown(f"[🔗 View on MET Museum]({obj.get('objectURL')})")
                    st.divider()
