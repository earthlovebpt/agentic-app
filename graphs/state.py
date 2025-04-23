from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class AgentState(BaseModel):
    # 🧠 User intent
    user_prompt: Optional[str] = None
    og_prompt: Optional[str] = None
    generated_prompt: Optional[List[Dict[str, Any]]] = None
    gen_questions: Optional[List[Dict[str, Any]]] = None

    data_sufficient: Optional[bool] = None
    user_action: Optional[str] = None  # "upload_more_data" or "ask_other_question"
    recommendations_if_insufficient: Optional[List[str]] = None

    # 🏢 Business context
    business_profile: Dict[str, str] = Field(default_factory=dict)

    # 📦 Dataset management
    datasets: Dict[str, Any] = Field(default_factory=dict)       # full dataset pool
    new_datasets: Dict[str, Any] = Field(default_factory=dict)   # newly added datasets
    schema_context: Optional[str] = None
    data_sufficient: Optional[bool] = None
    explored_datasets: List[str] = []

    # 💡 Question suggestion
    suggested_questions: List[str] = Field(default_factory=list)

    # 🧮 Planning & execution
    plan: List[Dict[str, Any]] = Field(default_factory=list)
    results: List[Dict[str, Any]] = Field(default_factory=list)
    replan: Optional[bool] = False
    new_prompt: Optional[str] = None

    # 🔁 Reflection
    prior_summary: Optional[str] = None

    # 🧠 Memory
    memory_log: List[str] = Field(default_factory=list)

    step_successful: Optional[bool] = None
    retry_step: Optional[bool] = None
    replan_step: Optional[bool] = None
    step_blocker: Optional[str] = None

    plan_successful: Optional[bool] = None

    replan_step_multiple: Optional[bool] = False  # whether to replace multiple steps
    abandon_question: Optional[bool] = False  # whether to stop and inform user

    current_step_index: Optional[int] = 0

    answer_to_question: Optional[str] = None  # 🎯 Direct answer to user's question
    insight_summary: Optional[str] = None     # 📊 Broader summary of findings
    recommended_actions: Optional[List[str]] = []  # ✅ Concrete strategic next steps

    retry_count: int = 0
    max_retries: int = 4
    exceed_max_retries: bool = False

    variable_env: Optional[Dict[str, Any]] = None

    #For storing insights and actions
    insights: Optional[List[List[str]]] = []
    answers: Optional[List[str]] = []
    complete_gen_question: Optional[bool] = False
    strategies: Optional[List[Dict[str, Any]]] = None
    selected_strategy: Optional[Dict[str, Any]] = None

