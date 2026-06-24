from groq import Groq
import os


class BaseAgent:
    def __init__(self, agent_id: str, name: str, role: str, personality: str):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.personality = personality
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"])

    def _call(self, system: str, user: str, max_tokens: int = 1024) -> str:
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ]
        )
        return response.choices[0].message.content

    def think(self, context: str) -> str:
        system = f"""당신은 DANTE CORPORATION의 {self.role} 에이전트 {self.name}입니다.
성격: {self.personality}
당신의 역할에 맞는 분석과 판단을 한국어로 간결하게 제공하세요.
반드시 실행 가능한 인사이트를 포함하세요."""
        return self._call(system, context)
