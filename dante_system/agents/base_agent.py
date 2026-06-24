import anthropic
import os


class BaseAgent:
    def __init__(self, agent_id: str, name: str, role: str, personality: str):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.personality = personality
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def _call(self, system: str, user: str, max_tokens: int = 1024) -> str:
        message = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}]
        )
        return message.content[0].text

    def think(self, context: str) -> str:
        system = f"""당신은 DANTE CORPORATION의 {self.role} 에이전트 {self.name}입니다.
성격: {self.personality}
당신의 역할에 맞는 분석과 판단을 한국어로 간결하게 제공하세요.
반드시 실행 가능한 인사이트를 포함하세요."""
        return self._call(system, context)
