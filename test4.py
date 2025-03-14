import random
import streamlit as st

skills = {
    "gold": ["나무열매수S", "수면EXP보너스", "도우미 보너스", "리서치 EXP 보너스", "꿈의조각 보너스", "스킬 레벨업M", "기력회복 보너스"],
    "blue": ["도우미 스피드M", "식재료 확률업 M", "최대 소지 수 업L", "최대 소지 수 업M", "스킬확률업M", "스킬 레벨업S"],
    "white": ["도우미 스피드S", "식재료 확률업 S", "최대 소지 수 업S", "스킬확률업S"]
}

def generate_skillsets(iterations):
    colors = ["gold", "blue", "white"]
    color_probs = [0.14, 0.33, 0.53]
    
    skillsets = []
    for _ in range(iterations):
        available_skills = {color: skill_list[:] for color, skill_list in skills.items()}
        selected_skills = []
        
        for i in range(3):
            color = random.choices(colors, weights=color_probs)[0]
            skill = random.choice(available_skills[color])
            selected_skills.append(skill)
            available_skills[color].remove(skill)
        
        skillsets.append(selected_skills)
    
    return skillsets

def monte_carlo_simulation(skillsets, target_skills, level, fix_gold_level):
    levels = {10: 1, 25: 2, 50: 3}
    num_skills = levels[level]
    
    if fix_gold_level == 1:
        skillsets = [s for s in skillsets if s[0] in skills["gold"]]
    elif fix_gold_level == 2:
        skillsets = [s for s in skillsets if s[0] in skills["gold"] and s[1] in skills["gold"]]
    
    match_count = sum(1 for s in skillsets if all(skill in s[:num_skills] for skill in target_skills))
    return round((match_count / len(skillsets)) * 100, 1) if skillsets else 0

# Streamlit UI
st.title("포켓몬슬립 서브스킬 확률 계산기")

iterations = st.slider("반복 횟수 (Iterations):", min_value=100000, max_value=1000000, value=500000, step=100)
selected_level = st.selectbox("레벨 선택:", [10, 25, 50])
target_skills = st.multiselect("원하는 스킬 선택 (최대 3개)", 
    ["나무열매수S", "수면EXP보너스", "도우미 보너스", "리서치 EXP 보너스", "꿈의조각 보너스", "스킬 레벨업M", "기력회복 보너스",
     "도우미 스피드M", "식재료 확률업 M", "최대 소지 수 업L", "최대 소지 수 업M", "스킬확률업M", "스킬 레벨업S",
     "도우미 스피드S", "식재료 확률업 S", "최대 소지 수 업S", "스킬확률업S"])

fix_gold_level = st.radio("금색 스킬 고정:", [0, 1, 2], format_func=lambda x: ["고정 없음", "10레벨 금색 고정", "10,25레벨 금색 고정"][x])

if st.button("확률 계산"):
    if not target_skills:
        st.error("적어도 하나의 스킬을 선택해주세요.")
    else:
        skillsets = generate_skillsets(iterations)
        probability = monte_carlo_simulation(skillsets, target_skills, selected_level, fix_gold_level)
        st.success(f"해당 조합의 확률: {probability:.2f}%")
