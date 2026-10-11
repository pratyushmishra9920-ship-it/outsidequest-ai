import requests
import streamlit as st
import json
from pathlib import Path


# ---------- Configuration ----------

OLLAMA_URL = "http://localhost:11434/api/chat"
DATA_FILE = Path(__file__).parent / "discoveries.json"
MODEL = "qwen3.5:4b"


# ---------- Page setup ----------

st.set_page_config(
    page_title="OutsideQuest",
    page_icon="🌿",
    layout="centered",
)


# ---------- Session state ----------


if "discoveries" not in st.session_state:
    if DATA_FILE.exists():
        try:
            st.session_state["discoveries"] = json.loads(
                DATA_FILE.read_text(encoding="utf-8")
            )
        except (json.JSONDecodeError, OSError):
            st.session_state["discoveries"] = []
    else:
        st.session_state["discoveries"] = []

st.session_state.setdefault("completed", False)
st.session_state.setdefault("follow_up", "")
st.session_state.setdefault("quest", "")


# ---------- Page introduction ----------

st.title("🌿 OutsideQuest")
st.subheader("The world is the interface.")

st.write(
    "Trade screen time for green time. Discover overlooked details "
    "in the world around you with quests powered by a local AI model."
)

st.caption(
    "Free to use • Local AI • No special equipment • "
    "Designed for real-world exploration"
)


# ---------- Sidebar settings ----------

with st.sidebar:
    st.header("Your adventure")

    duration = st.selectbox(
        "How much time do you have?",
        [10, 20, 30],
        index=1,
    )

    environment = st.selectbox(
        "Where can you explore?",
        [
            "Park or green space",
            "Street or neighbourhood",
            "College campus",
            "Garden or courtyard",
        ],
    )

    difficulty = st.selectbox(
        "Choose your pace",
        ["Relaxed", "Curious", "Observant"],
        index=1,
    )

    mission_type = st.selectbox(
        "Choose your investigation",
        [
            "Sound Detective",
            "Light & Shadow",
            "Urban Nature Mystery",
            "Human Impact",
            "Micro-Discovery",
        ],
    )

    st.divider()
    st.caption(
        "Your quest runs on your local Ollama model. "
        "Put your device away while exploring."
    )


# ---------- Mission instructions ----------

MISSION_GUIDES = {
    "Sound Detective": (
        "Investigate the soundscape. Notice at least three sounds, "
        "compare their rhythm, distance, or intensity, and consider "
        "possible sources. Do not assume a source without evidence."
    ),
    "Light & Shadow": (
        "Investigate light, shadows, and reflections. Compare shapes, "
        "edges, or directions and consider how objects and sunlight "
        "create the patterns you observe."
    ),
    "Urban Nature Mystery": (
        "Look for traces of nature in a built environment, such as "
        "plants growing through gaps, insects at a distance, or "
        "weathering. Build a small investigation from visible evidence."
    ),
    "Human Impact": (
        "Observe how human activity shapes the surroundings. Look for "
        "evidence of design, litter, shade, noise, or green spaces. "
        "Distinguish what you directly observe from your interpretation."
    ),
    "Micro-Discovery": (
        "Look closely at small details and patterns: textures, leaf "
        "shapes, surface patterns, or repeated forms. Choose one detail "
        "and investigate what makes it interesting without touching "
        "unknown plants, fungi, or animals."
    ),
}


# ---------- Ollama helper ----------

def ask_local_model(prompt, system_prompt, temperature=0.5, max_tokens=300):
    """Send a prompt to the locally running Ollama model and return its text."""
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "think": False,
            "keep_alive": "5m",
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens + 250,
                "num_ctx": 2048,
            },
        },
        timeout=240,
    )
    response.raise_for_status()

    content = response.json().get("message", {}).get("content", "").strip()
    if not content:
        raise ValueError("The model returned an empty response.")

    return content


# ---------- Generate quest ----------

if st.button(
    "Generate my quest",
    type="primary",
    use_container_width=True,
):
    prompt = f"""
Design one distinctive, practical outdoor investigation.

Time available: {duration} minutes.
Environment: {environment}.
Pace: {difficulty}.
Investigation type: {mission_type}.

Investigation rules:
{MISSION_GUIDES[mission_type]}

Create a specific mission, not a generic walking activity.
The user should investigate something observable, compare evidence,
and finish with a question or discovery.

Return exactly these four sections, using these Markdown headings:

## Mission
Start with a short, memorable mission title in bold.
Then give one clear investigation question and a concise objective.

## Field Steps
Give exactly 3 numbered steps with realistic time ranges.
Each step must describe a specific action the user can perform.
Ensure the timings fit within {duration} minutes.

## What to Notice
List 2 or 3 concrete details the user can observe.
Describe possible findings, not guaranteed results.

## Reflection
Give exactly 2 complete questions based on the investigation.
Finish both questions completely.

Requirements:
- Match the selected investigation type exactly.
- Adapt the activity to the selected environment and pace.
- Require no purchases, equipment, photography, or phone use outdoors.
- Make the activity achievable for a beginner.
- Stay in public, permitted, safe areas.
- Never cross roads as part of the activity, cross fences, or enter
  private property or restricted areas.
- Never touch or eat unknown plants, fungi, or animals.
- Do not approach wildlife or disturb living things.
- Do not claim to know what is actually present around the user.
- Separate observable evidence from guesses.
- Do not invent scientific facts or claim an identification is certain.
- Return only the quest, without revealing internal reasoning.
- Never require users to close their eyes or ignore their surroundings.
- Never assume a particular sound, animal, plant, or object exists nearby.
- Give exactly 3 complete field steps with realistic time ranges.
- Make every step an observation task, not a predetermined conclusion.
- Keep the response concise and finish every section completely.
- Use clean Markdown headings without labels like "TITLE:" in headings.
- Include a practical alternative when weather or the environment makes an observation impossible.
- Avoid repeating the same observation across multiple steps.
- Use these exact section headings: ## Mission, ## Field Steps, ## What to Notice, and ## Reflection.
- Every step must contribute new evidence or test a specific hypothesis.
- Do not require repetitive walking or waiting without a clear purpose.
- Never claim that a short observation proves a broad scientific conclusion.
- Explain what the user should do if the required environmental condition is absent.
- Do not assume that sunlight, shadows, animals, plants, or particular sounds are present.
- Make the investigation feasible within the selected duration.
- Do not include a separate "Title:" label when the mission title is already bold.
- SAFETY OVERRIDE: Never tell the user to close their eyes, even briefly.
- Do not make a sound or other observation a prerequisite for completing a step.
- If the expected sound is absent, instruct the user to record its absence and investigate another observable sound.
- Use these exact time ranges for a 20-minute mission: 0–5, 5–12, and 12–20 minutes.
- Make every step useful even if the user's surroundings are quiet or different from the examples.  
- Never instruct the user to find a specific replacement sound; let them choose any sound they can actually observe.
- Prefer observing from one safe, permitted location unless movement is essential to the investigation.
- Use simple, direct instructions; each field step should have one main task and one clear outcome.
- Never require the user to locate or compare sounds that are not actually audible.
- If a sound disappears, ask the user to record that change or continue observing an available sound; never prescribe a replacement sound as though it must exist.
"""

    with st.spinner("Your local AI is designing an investigation..."):
        try:
            quest = ask_local_model(
                prompt,
                (
                    
                    "You are OutsideQuest, an expert designer of safe, evidence-based "
                    "outdoor investigations. Follow the selected investigation type, "
                    "environment, and duration. Create a specific mystery that users "
                    "can investigate through direct observation without equipment. "
                    "Never tell users to close their eyes, even briefly. Never assume "
                    "any particular sound, object, animal, plant, sunlight, or shadow "
                    "exists nearby. Present examples only as optional possibilities. "
                    "Give exactly three distinct, useful field steps with complete "
                    "time ranges that fit the selected duration. Each step must gather "
                    "new evidence or test a hypothesis; avoid pointless repetition. "
                    "Include a practical alternative if the expected conditions are "
                    "absent. Separate observations from hypotheses and never claim "
                    "that a short observation proves a broad scientific conclusion. "
                    "Return complete sections using exactly the requested headings. "
                    "Finish both reflection questions and keep the response concise. "
                    "Prioritize safety and direct observation over creative wording. "
                    "Do not reveal internal reasoning. "


                ),
                temperature=0.6,
                max_tokens=300,
            )

            st.session_state["quest"] = quest
            st.session_state["duration"] = duration
            st.session_state["mission_type"] = mission_type
            st.session_state["environment"] = environment
            st.session_state["completed"] = False
            st.session_state["follow_up"] = ""

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to Ollama. Make sure Ollama is running "
                "and try again."
            )
        except requests.exceptions.Timeout:
            st.error(
                "The local model took too long to respond. Please try again."
            )
        except requests.exceptions.RequestException as exc:
            st.error(f"Request failed: {exc}")
        except ValueError as exc:
            st.error(str(exc))


# ---------- Display quest and discovery journal ----------

if st.session_state["quest"]:
    st.divider()
    st.markdown("## Your field mission")

    st.caption(
        f"{st.session_state.get('mission_type', 'Outdoor investigation')} · "
        f"{st.session_state.get('duration', 20)} minutes · "
        f"{st.session_state.get('environment', 'Your surroundings')}"
    )

    st.markdown(st.session_state["quest"])

    st.warning(
        "Read the mission, put your device away, and explore safely. "
        "You do not need to photograph or upload anything."
    )

    if not st.session_state["completed"]:
        if st.button(
            "I've completed my exploration",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["completed"] = True
            st.success(
                "Welcome back. Now record what you actually noticed."
            )
    else:
        st.success(
            "Exploration complete. Your observations are the "
            "most important part of this quest."
        )

    # ---------- Discovery journal ----------

    st.divider()
    st.markdown("## Your discovery journal")

    st.write(
        "Record what you observed, not what you think the AI wants "
        "to hear. A small detail or an unanswered question is enough."
    )

    with st.form("discovery_form", clear_on_submit=True):
        discovery = st.text_area(
            "What did you notice?",
            placeholder=(
                "Example: I heard two different bird-like calls. "
                "One repeated several times, while the other was brief. "
                "I could not identify their sources with certainty."
            ),
            height=120,
        )

        submitted = st.form_submit_button(
            "Save my discovery",
            use_container_width=True,
        )

    if submitted:
        if discovery.strip():
            st.session_state["discoveries"].append(
                {
                    "mission": st.session_state.get(
                        "mission_type", "Outdoor discovery"
                    ),
                    "observation": discovery.strip(),
                }
            )
            st.session_state["follow_up"] = ""
            
            try:
                DATA_FILE.write_text(
                    json.dumps(
                        st.session_state["discoveries"],
                        ensure_ascii=False,
                        indent=2,
                    ),
                    encoding="utf-8",
                )
                st.success("Discovery saved permanently on this device.")
            except OSError as exc:
                st.error(f"Could not save discoveries to file: {exc}")

        else:
            st.warning("Write a short observation before saving.")

    discoveries = st.session_state["discoveries"]

    if discoveries:
        st.markdown("### Your field notes")

        for number, item in enumerate(reversed(discoveries), start=1):
            with st.container(border=True):
                st.caption(f"Field note {number} · {item['mission']}")
                st.write(item["observation"])

        st.caption(
            "Your field notes are saved locally in discoveries.json."
        )

        # ---------- Observation-to-discovery loop ----------

        st.divider()
        st.markdown("## Turn a detail into a discovery")

        st.write(
            "Your observation is the starting point. Let your local AI "
            "help you decide what to investigate next."
        )

        if st.button(
            "Explore this observation further",
            type="primary",
            use_container_width=True,
        ):
            latest = discoveries[-1]

            follow_up_prompt = f"""
The user's actual observation:
{latest["observation"]}

Original investigation:
{latest["mission"]}

Create a follow-up investigation based ONLY on this observation.

Return these sections:

WHAT WE KNOW
State only what the user directly observed.

POSSIBLE EXPLANATIONS
Give up to two cautious possibilities. Clearly label them as hypotheses,
not facts. If evidence is insufficient, say so.

THE NEXT MYSTERY
Ask one specific question that can be investigated through direct
observation in the real world.

YOUR NEXT EXPERIMENT
Give three simple steps the user can perform safely without a phone,
special equipment, purchases, or disturbing living things.

WHAT WOULD CHANGE YOUR MIND?
Explain what new observation might support or weaken a hypothesis.

Rules:
- Never invent details about the user's surroundings.
- Never claim an uncertain identification is confirmed.
- Do not present guesses as scientific facts.
- Keep the experiment suitable for the original environment.
- Prioritize curiosity, safety, and real-world observation.
- Keep the response concise.
"""

            with st.spinner(
                "Qwen is turning your field note into a new mystery..."
            ):
                try:
                    follow_up = ask_local_model(
                        follow_up_prompt,
                        (
                            "You are an evidence-first outdoor investigation "
                            "guide. Distinguish observations from hypotheses. "
                            "Never invent evidence. Create safe, practical "
                            "follow-up experiments."
                        ),
                        temperature=0.4,
                        max_tokens=250,
                    )
                    st.session_state["follow_up"] = follow_up

                except requests.exceptions.ConnectionError:
                    st.error(
                        "Cannot connect to Ollama. Make sure Ollama is running."
                    )
                except requests.exceptions.Timeout:
                    st.error(
                        "The local model took too long to respond. "
                        "Please try again."
                    )
                except requests.exceptions.RequestException as exc:
                    st.error(f"Could not generate the follow-up: {exc}")
                except ValueError as exc:
                    st.error(str(exc))

        if st.session_state["follow_up"]:
            st.markdown("### Your next field investigation")
            st.markdown(st.session_state["follow_up"])
            st.warning(
                "Take this investigation outside. Observe first; treat "
                "possible explanations as hypotheses."
            )


# ---------- Footer ----------

st.divider()
st.caption(
    "OutsideQuest · Local AI, real-world curiosity. "
    "Respect nature, local rules, and personal safety."
)
