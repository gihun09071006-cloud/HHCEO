from agents.base_agent import BaseAgent
from core import database as db


class ARIA(BaseAgent):
    def __init__(self):
        super().__init__("Agent-01", "ARIA", "CEO", "전략적, 결단력 있음, 큰 그림을 봄")

    async def run_daily(self, projects: list, agents: list, pending_decisions: list) -> str:
        await db.update_agent("Agent-01", "Strategic Command Room", "일일 전략 검토 및 지시 하달")
        context = f"""
오늘 DANTE CORPORATION 현황:
- 활성 프로젝트: {[p['name'] + ' (' + p['status'] + ' ' + str(p['progress']) + '%)' for p in projects]}
- 에이전트: {len(agents)}명 운영 중
- 미결 결정사항: {len(pending_decisions)}건

오늘의 전략 우선순위를 정하고, 각 에이전트에 지시를 내리세요.
신규 기회나 위험이 있다면 회장님께 보고할 결정사항을 제안하세요.
"""
        return self.think(context)


class NEXUS(BaseAgent):
    def __init__(self):
        super().__init__("Agent-02", "NEXUS", "Research", "호기심 많음, 데이터 지향, 트렌드에 민감")

    async def run_daily(self, projects: list) -> str:
        await db.update_agent("Agent-02", "Research Department", "시장 동향 및 경쟁사 분석")
        context = f"""
현재 진행 중인 프로젝트:
{[p['name'] for p in projects]}

오늘의 시장 조사 과제:
1. PRJ-001 (LinkedIn AI): LinkedIn AI 툴 경쟁사 최신 동향, 고객 페인포인트
2. PRJ-002 (마켓플레이스): AI 에이전트 마켓플레이스 시장 동향, 잠재 파트너사
3. 새로운 시장 기회가 있다면 발굴하여 보고

구체적인 인사이트와 수치를 포함하세요.
"""
        return self.think(context)


class VECTOR(BaseAgent):
    def __init__(self):
        super().__init__("Agent-03", "VECTOR", "Analysis", "정밀함, 수치 기반, 패턴 탐지")

    async def run_daily(self, projects: list) -> str:
        await db.update_agent("Agent-03", "Analysis Lab", "프로젝트 진척도 분석 및 수익 모델 업데이트")
        context = f"""
분석 대상 프로젝트:
{[(p['name'], p['status'], p['progress']) for p in projects]}

오늘의 분석 과제:
1. 각 프로젝트의 현재 진척도 평가 (0-100%)
2. 수익 달성 가능성 재계산
3. 가장 빠른 수익화 경로 제안
4. 리소스 배분 최적화 제안

수치와 근거를 명확히 포함하세요.
"""
        return self.think(context)


class LEDGER(BaseAgent):
    def __init__(self):
        super().__init__("Agent-04", "LEDGER", "Finance", "보수적, 정확함, 현금흐름 집착")

    async def run_daily(self, projects: list) -> str:
        await db.update_agent("Agent-04", "Finance Desk", "재무 상태 점검 및 수익 예측 업데이트")
        context = f"""
재무 검토 대상:
{[(p['name'], p['revenue_target'], p['status']) for p in projects]}

오늘의 재무 분석:
1. 각 프로젝트의 이번 달 예상 수익
2. 손익분기점 도달 예상 시점
3. 현금 소요 리스크
4. 재무적 우선순위 추천

보수적 관점에서 현실적인 수치를 제시하세요.
"""
        return self.think(context)


class SENTINEL(BaseAgent):
    def __init__(self):
        super().__init__("Agent-05", "SENTINEL", "Risk", "신중함, 최악의 시나리오 항상 고려")

    async def run_daily(self, projects: list) -> str:
        await db.update_agent("Agent-05", "Risk Assessment Room", "리스크 모니터링 및 위협 평가")
        context = f"""
리스크 모니터링 대상:
{[p['name'] for p in projects]}

오늘의 리스크 점검:
1. PRJ-001: LinkedIn API 정책 변화 동향
2. PRJ-002: 마켓플레이스 법적/경쟁 리스크
3. 신규 위협 요소
4. 리스크 완화 조치 제안

HIGH/MEDIUM/LOW로 등급을 매기고 대응책을 제시하세요.
"""
        return self.think(context)


class FORGE(BaseAgent):
    def __init__(self):
        super().__init__("Agent-06", "FORGE", "Execution", "실행력 강함, 완벽주의, 데드라인 집착")

    async def run_daily(self, projects: list) -> str:
        await db.update_agent("Agent-06", "Development Room", "개발 진척도 관리 및 기술 이슈 해결")
        context = f"""
빌드 현황:
{[(p['name'], p['status'], p['progress'], p['target_launch']) for p in projects]}

오늘의 실행 계획:
1. 각 프로젝트 이번 주 완료해야 할 기술 작업
2. 현재 기술적 병목 지점
3. 다음 마일스톤까지 예상 일수
4. 리소스가 더 필요한 부분

구체적인 기술 과제와 타임라인을 포함하세요.
"""
        return self.think(context)


class PRISM(BaseAgent):
    def __init__(self):
        super().__init__("Agent-07", "PRISM", "Product", "창의적, 사용자 중심, 아름다운 UX 추구")

    async def run_daily(self, projects: list) -> str:
        await db.update_agent("Agent-07", "Development Room", "제품 설계 및 사용자 경험 최적화")
        context = f"""
제품 설계 현황:
{[p['name'] for p in projects]}

오늘의 제품 과제:
1. PRJ-001: LinkedIn AI 핵심 사용자 플로우 개선 아이디어
2. PRJ-002: 마켓플레이스 온보딩 경험 설계
3. 사용자 획득을 위한 제품 훅(hook) 제안
4. 이번 주 완성해야 할 UX 산출물

사용자 관점에서 구체적인 제안을 하세요.
"""
        return self.think(context)
