# Lab Flow Guide: Legal Multi-Agent System with A2A

Tai lieu nay tom tat toan bo flow bai lab theo tung stage. Moi stage la mot cach nang cap he thong LLM/Agent len muc phuc tap va thuc te hon.

## 1. Y tuong tong quan

Du an xay dung mot he thong tu van phap ly multi-agent:

```text
User
-> Customer Agent
-> Law Agent
-> Tax Agent + Compliance Agent
-> Tong hop cau tra loi
```

Trong qua trinh hoc, repo di theo lo trinh:

```text
Stage 1: Direct LLM
-> Stage 2: LLM + RAG/Tools
-> Stage 3: Single ReAct Agent
-> Stage 4: Multi-Agent in-process
-> Stage 5: Distributed A2A
```

Bang nang cap:

| Stage | Cach nang cap | Van de duoc giai quyet |
|---|---|---|
| Stage 1 | Goi LLM truc tiep | Co baseline don gian de hieu LLM |
| Stage 2 | Them RAG va tools | LLM co the tra cuu va tinh toan |
| Stage 3 | Them ReAct agent loop | Agent tu quyet dinh goi tool nao va goi khi nao |
| Stage 4 | Tach thanh nhieu agent trong 1 process | Moi agent chuyen mon hoa, co the chay song song |
| Stage 5 | Tach moi agent thanh service A2A rieng | He thong distributed, discovery dong, co the scale rieng |

## 2. Setup can biet

File can chu y:

| File | Chuc nang |
|---|---|
| `pyproject.toml` | Khai bao dependencies: LangGraph, LangChain, A2A SDK, FastAPI, uvicorn, httpx, dotenv |
| `.env.example` | Mau bien moi truong can copy thanh `.env` |
| `common/llm.py` | Tao LLM client dung chung qua OpenRouter |
| `README.md` | Mo ta kien truc tong quan va cach chay |
| `CODELAB.md` | Huong dan lab cho sinh vien |
| `QUICK_REFERENCE.md` | Lenh nhanh va code snippet |
| `INSTRUCTOR_GUIDE.md` | Flow giang day cho giang vien |

Lenh setup:

```bash
uv sync
cp .env.example .env
```

Sau do sua `.env`:

```text
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=anthropic/claude-sonnet-4-5
REGISTRY_URL=http://localhost:10000
```

## 3. Shared code nen hieu truoc

### `common/llm.py`

Chuc nang: tao LLM client dung chung cho tat ca stages va agents.

Thanh phan chinh:

| Thanh phan | Chuc nang |
|---|---|
| `get_llm()` | Tra ve `ChatOpenAI` client tro den OpenRouter |
| `OPENROUTER_MODEL` | Chon model qua bien moi truong |
| `OPENROUTER_API_KEY` | API key goi OpenRouter |
| `openai_api_base` | Tro ve endpoint OpenRouter OpenAI-compatible |

Tat ca stage deu goi:

```python
llm = get_llm()
```

## 4. Stage 1: Direct LLM Calling

Muc tieu: hieu cach goi LLM co ban nhat.

Nang cap o stage nay:

```text
Chua nang cap gi ca. Day la baseline:
SystemMessage + HumanMessage -> LLM -> response
```

Lenh chay:

```bash
uv run python stages/stage_1_direct_llm/main.py
```

File can chu y:

| File | Chuc nang |
|---|---|
| `stages/stage_1_direct_llm/main.py` | Demo goi LLM truc tiep |
| `stages/stage_1_direct_llm/architecture.svg` | So do kien truc Stage 1 |
| `common/llm.py` | Tao LLM client |

Trong `stages/stage_1_direct_llm/main.py`:

| Thanh phan code | Chuc nang |
|---|---|
| `QUESTION` | Cau hoi mau ve vi pham NDA |
| `load_dotenv()` | Load bien moi truong tu `.env` |
| `get_llm()` | Khoi tao LLM |
| `SystemMessage` | Dinh nghia vai tro: legal expert, tra loi ngan gon |
| `HumanMessage` | Noi dung cau hoi cua user |
| `await llm.ainvoke(messages)` | Goi LLM bat dong bo va nhan response |
| `main()` | In huong dan, goi LLM, in ket qua va gioi han cua Stage 1 |

Flow code:

```text
Load .env
-> Tao llm
-> Tao messages
-> llm.ainvoke(messages)
-> In response.content
```

Gioi han:

- Khong co tool.
- Khong co RAG.
- Khong co memory.
- Khong tra cuu du lieu moi.
- Khong co kha nang chia task phuc tap.

## 5. Stage 2: LLM + RAG / Tools

Muc tieu: nang LLM tu hoi dap truc tiep len LLM co the dung cong cu.

Nang cap so voi Stage 1:

```text
Stage 1: LLM tra loi tu training data
Stage 2: LLM duoc bind tools, co the search knowledge base va tinh damages
```

Lenh chay:

```bash
uv run python stages/stage_2_rag_tools/main.py
```

File can chu y:

| File | Chuc nang |
|---|---|
| `stages/stage_2_rag_tools/main.py` | Demo RAG/toolling voi manual orchestration |
| `stages/stage_2_rag_tools/architecture.svg` | So do Stage 2 |
| `exercises/exercise_2_tools.py` | Bai tap them knowledge base va tool moi |
| `common/llm.py` | Tao LLM client |

Trong `stages/stage_2_rag_tools/main.py`:

| Thanh phan code | Chuc nang |
|---|---|
| `LEGAL_KNOWLEDGE` | Knowledge base gia lap bang list dict, moi entry co `id`, `keywords`, `text` |
| `@tool search_legal_database(query)` | Tool search knowledge base dua tren keyword overlap |
| `@tool calculate_damages(breach_type, contract_value)` | Tool uoc tinh thiet hai dua tren loai vi pham va gia tri hop dong |
| `TOOLS` | Danh sach tools bind vao LLM |
| `llm.bind_tools(TOOLS)` | Cho LLM biet co nhung tool nao co the goi |
| `tool_map` | Map ten tool sang function de execute tool call |
| `response.tool_calls` | Danh sach tool ma LLM yeu cau goi |
| `ToolMessage` | Dua ket qua tool quay lai conversation |
| `final_response` | LLM tong hop cau tra loi cuoi cung tu ket qua tool |

Flow code:

```text
User question
-> LLM nhan question + tools
-> LLM quyet dinh tool_calls
-> Python code tu execute tool
-> Them ToolMessage vao messages
-> Goi LLM lan 2 de tong hop answer
```

Diem can nhan manh:

- RAG trong stage nay la knowledge base don gian, chua phai vector database.
- Tool calling da co, nhung orchestration con manual.
- Moi vong tool call do lap trinh vien tu viet.

Bai tap lien quan: `exercises/exercise_2_tools.py`

Trong file bai tap:

| Thanh phan code | Chuc nang |
|---|---|
| `LEGAL_KNOWLEDGE` | Noi sinh vien them entry `labor_law` |
| `search_legal_knowledge(query)` | Tool search knowledge base bang keyword |
| TODO `check_statute_of_limitations(case_type)` | Tool can sinh vien viet de tra thoi hieu khoi kien |
| `tools = [...]` | Noi them tool moi vao danh sach |
| Vong `if response.tool_calls` | Noi them logic execute tool moi |

## 6. Stage 3: Single Agent voi ReAct

Muc tieu: nang Stage 2 thanh agent tu lap ke hoach va goi tools.

Nang cap so voi Stage 2:

```text
Stage 2: code tu viet manual tool loop
Stage 3: create_react_agent tu quan ly Think -> Act -> Observe
```

Lenh chay:

```bash
uv run python stages/stage_3_single_agent/main.py
```

File can chu y:

| File | Chuc nang |
|---|---|
| `stages/stage_3_single_agent/main.py` | Demo ReAct agent voi nhieu tools |
| `stages/stage_3_single_agent/architecture.svg` | So do Stage 3 |
| `common/llm.py` | Tao LLM client |

Trong `stages/stage_3_single_agent/main.py`:

| Thanh phan code | Chuc nang |
|---|---|
| `LEGAL_KNOWLEDGE` | Knowledge base mo rong: NDA, contract, tax, offshore tax, privacy, SOX |
| `@tool search_legal_database(query)` | Tool tra cuu legal knowledge |
| `@tool calculate_penalty(violation_type, severity, annual_revenue)` | Tool tinh penalty uoc tinh theo revenue va severity |
| `@tool check_compliance_requirements(industry, company_size)` | Tool tra framework compliance theo industry va company size |
| `TOOLS` | Tap tools cua agent |
| `QUESTION` | Cau hoi phuc tap gom privacy + tax + compliance |
| `SYSTEM_PROMPT` | Prompt dinh huong agent: search rieng tung mang data privacy, tax, compliance |
| `create_react_agent(model=llm, tools=TOOLS, prompt=SYSTEM_PROMPT)` | Tao ReAct agent cua LangGraph |
| `graph.astream(..., stream_mode="updates")` | Stream tung buoc agent lam viec de hien thi Think/Act/Observe |
| Kiem tra `msg.tool_calls` | In ra buoc agent quyet dinh goi tool nao |
| `msg.type == "tool"` | In ket qua observe tu tool |
| `msg.type == "ai"` | In cau tra loi cuoi cung |

Flow code:

```text
User question phuc tap
-> ReAct agent suy luan can thong tin gi
-> Agent goi tool 1
-> Nhan ket qua tool
-> Agent co the goi tiep tool 2, tool 3
-> Tong hop final answer
```

Diem can nhan manh:

- Agent co kha nang multi-step reasoning.
- Agent tu quyet dinh thu tu tool.
- Van chi la mot agent duy nhat, nen tat ca domain deu nam trong mot prompt.
- Tool calls co xu huong tuan tu, chua co parallel specialist agents.

## 7. Stage 4: Multi-Agent In-Process

Muc tieu: tach single agent thanh nhieu specialist agents, nhung van chay trong cung process.

Nang cap so voi Stage 3:

```text
Stage 3: mot agent lam tat ca
Stage 4: nhieu agent chuyen mon hoa + LangGraph StateGraph + parallel Send
```

Luu y: thu muc trong repo dang dat ten la `stage_4_milti_agent`, co typo `milti`.

Lenh chay:

```bash
uv run python stages/stage_4_milti_agent/main.py
```

File can chu y:

| File | Chuc nang |
|---|---|
| `stages/stage_4_milti_agent/main.py` | Demo multi-agent chay trong mot process |
| `stages/stage_4_milti_agent/architecture.svg` | So do Stage 4 |
| `exercises/exercise_4_multiagent.py` | Bai tap them `privacy_agent` |
| `common/llm.py` | Tao LLM client |

Kien truc Stage 4:

```text
analyze_law
-> check_routing
-> call_tax_specialist + call_compliance_specialist
-> aggregate
-> END
```

Trong `stages/stage_4_milti_agent/main.py`:

| Thanh phan code | Chuc nang |
|---|---|
| `search_tax_law(query)` | Tool local cho tax specialist search kien thuc thue |
| `search_compliance_law(query)` | Tool local cho compliance specialist search kien thuc regulatory |
| `_last_wins(a, b)` | Reducer de xu ly ghi state tu parallel branches |
| `LegalState` | Shared state cua graph: question, law_analysis, flags routing, tax_result, compliance_result, final_answer |
| `analyze_law(state)` | Lead attorney phan tich phap ly tong quat |
| `check_routing(state)` | LLM router quyet dinh co can tax/compliance khong, tra JSON |
| `route_to_specialists(state)` | Tao danh sach `Send(...)` de dispatch cac specialist song song |
| `call_tax_specialist(state)` | Tao inline ReAct tax agent va goi `search_tax_law` |
| `call_compliance_specialist(state)` | Tao inline ReAct compliance agent va goi `search_compliance_law` |
| `aggregate(state)` | Tong hop law, tax, compliance thanh final answer |
| `create_graph()` | Xay `StateGraph`, add nodes, add edges, compile graph |
| `main()` | Khoi tao state ban dau, invoke graph, in final answer |

Flow code:

```text
Initial state
-> analyze_law ghi law_analysis
-> check_routing ghi needs_tax/needs_compliance
-> route_to_specialists tra list Send
-> tax/compliance branches chay song song
-> aggregate doc cac analysis
-> final_answer
```

Diem can nhan manh:

- `StateGraph` bien flow thanh graph ro rang.
- `Send` giup dispatch nhieu node song song.
- `Annotated[str, _last_wins]` giup cac branch parallel ghi state khong bi conflict.
- Van la in-process, chua co HTTP, chua co A2A, chua co Registry.

Bai tap lien quan: `exercises/exercise_4_multiagent.py`

Trong file bai tap:

| Thanh phan code | Chuc nang |
|---|---|
| `State` | Them field `privacy_analysis` |
| `law_agent(state)` | Agent phan tich phap ly tong quat |
| `check_routing(state)` | Them dieu kien route theo keyword data/privacy/gdpr |
| `tax_agent(state)` | Agent thue |
| `compliance_agent(state)` | Agent compliance |
| TODO `privacy_agent(state)` | Sinh vien implement agent ve GDPR/data protection/privacy rights |
| `aggregate_results(state)` | Them privacy section vao bao cao tong hop |
| `build_graph()` | Them node va edge cua `privacy_agent` |

## 8. Stage 5: Distributed A2A System

Muc tieu: dua kien truc Stage 4 thanh he thong distributed that su.

Nang cap so voi Stage 4:

```text
Stage 4: nhieu agent nhung cung mot process, goi nhau bang function
Stage 5: moi agent la mot HTTP service rieng, goi nhau qua A2A protocol
```

Lenh chay full system:

```bash
./start_all.sh
uv run python test_client.py
```

Ports:

| Service | Port | Vai tro |
|---|---:|---|
| Registry | 10000 | Luu agent registry va discovery |
| Customer Agent | 10100 | Entry point nhan cau hoi user |
| Law Agent | 10101 | Orchestrator phap ly |
| Tax Agent | 10102 | Specialist ve tax |
| Compliance Agent | 10103 | Specialist ve regulatory compliance |

Task discovery:

| Task | Agent xu ly |
|---|---|
| `legal_question` | Law Agent |
| `tax_question` | Tax Agent |
| `compliance_question` | Compliance Agent |

Flow request Stage 5:

```text
test_client.py
-> Customer Agent /.well-known/agent.json
-> Customer Agent A2A message
-> Customer graph goi delegate_to_legal_agent
-> Registry discover("legal_question")
-> Law Agent
-> Law graph analyze_law + check_routing
-> Registry discover("tax_question") va discover("compliance_question")
-> Tax Agent + Compliance Agent qua A2A
-> Law Agent aggregate
-> Customer Agent tra response cho client
```

### File shared cho Stage 5

| File | Chuc nang |
|---|---|
| `start_all.sh` | Start Registry, Tax, Compliance, Law, Customer theo dung thu tu |
| `test_client.py` | Client E2E gui cau hoi den Customer Agent bang A2A |
| `common/registry_client.py` | Ham `register()` va `discover()` goi Registry |
| `common/a2a_client.py` | Ham `delegate()` gui A2A message den agent khac |
| `common/llm.py` | Tao LLM client dung chung |

### `registry/__main__.py`

Chuc nang: FastAPI service lam service discovery.

| Thanh phan code | Chuc nang |
|---|---|
| `agents` | In-memory store: `agent_name -> agent_info` |
| `AgentRegistration` | Pydantic model cho request register |
| `POST /register` | Agent tu dang ky endpoint va tasks khi startup |
| `GET /discover/{task}` | Tim agent dau tien co task phu hop |
| `GET /agents` | Liet ke tat ca agents da register |
| `GET /health` | Kiem tra registry va so agent da dang ky |
| `uvicorn.run(... port=10000)` | Chay registry service |

### `common/registry_client.py`

| Thanh phan code | Chuc nang |
|---|---|
| `REGISTRY_URL` | Lay tu env, default `http://localhost:10000` |
| `discover(task)` | Goi `GET /discover/{task}` va tra ve endpoint |
| `register(agent_info)` | Goi `POST /register` de agent self-register |

### `common/a2a_client.py`

Chuc nang: helper de mot agent delegate cau hoi sang agent khac qua A2A.

| Thanh phan code | Chuc nang |
|---|---|
| `delegate(endpoint, question, context_id, trace_id, depth)` | Gui A2A message den endpoint agent khac |
| Fetch `/.well-known/agent.json` | Lay Agent Card cua agent dich |
| `A2AClient(...)` | Tao client tu Agent Card |
| `Message(...)` | Dong goi question, context_id, trace_id, delegation_depth |
| `SendMessageRequest(...)` | Request chuan de gui message |
| `client.send_message(request)` | Gui request qua A2A |
| `_extract_text(response)` | Lay text tu Task artifact, Message parts, hoac history |
| `_part_text(part)` | Lay text tu `Part(root=TextPart)` |

### Customer Agent

Thu muc: `customer_agent/`

| File | Chuc nang |
|---|---|
| `customer_agent/graph.py` | Dinh nghia ReAct Customer Agent va tool delegate sang Law Agent |
| `customer_agent/agent_executor.py` | Bridge A2A RequestContext sang LangGraph graph |
| `customer_agent/__main__.py` | Start HTTP A2A server port 10100, tao Agent Card, register |

Trong `customer_agent/graph.py`:

| Thanh phan code | Chuc nang |
|---|---|
| `CUSTOMER_SYSTEM_PROMPT` | Huong dan Customer Agent luon delegate cau hoi phap ly sang Law Agent |
| `build_graph(trace_id, context_id, depth)` | Tao graph moi cho moi request de closure giu metadata |
| `delegate_to_legal_agent(question)` | Tool discover Law Agent va goi `delegate(...)` |
| `discover("legal_question")` | Hoi Registry endpoint cua Law Agent |
| `create_react_agent(...)` | Tao ReAct agent co tool `delegate_to_legal_agent` |

Trong `customer_agent/agent_executor.py`:

| Thanh phan code | Chuc nang |
|---|---|
| `CustomerAgentExecutor` | Class executor cua A2A SDK |
| `execute(context, event_queue)` | Nhan A2A request, extract question, tao graph, invoke graph |
| `context_id`, `task_id` | ID cho conversation/task |
| `trace_id` | ID trace de theo doi request qua nhieu agent |
| `delegation_depth` | Do sau delegate, tranh loop vo han |
| `TaskUpdater` | Cap nhat task status: submit, start_work, add_artifact, complete/failed |
| `_extract_question(context)` | Lay text user tu A2A message parts |

Trong `customer_agent/__main__.py`:

| Thanh phan code | Chuc nang |
|---|---|
| `PORT = 10100` | Port Customer Agent |
| `_register_with_retry()` | Thu register voi Registry nhieu lan cho den khi Registry san sang |
| `AgentCard(...)` | Metadata cua agent tai `/.well-known/agent.json` |
| `AgentSkill(...)` | Mo ta skill `legal_assistant` |
| `A2AFastAPIApplication(...)` | Tao FastAPI app theo A2A SDK |
| `uvicorn.Server(...)` | Chay HTTP server |

### Law Agent

Thu muc: `law_agent/`

| File | Chuc nang |
|---|---|
| `law_agent/graph.py` | StateGraph orchestrator: phan tich, route, delegate Tax/Compliance, aggregate |
| `law_agent/agent_executor.py` | Bridge A2A request sang Law StateGraph |
| `law_agent/__main__.py` | Start A2A server port 10101, register task `legal_question` |

Trong `law_agent/graph.py`:

| Thanh phan code | Chuc nang |
|---|---|
| `MAX_DELEGATION_DEPTH = 3` | Chan delegate vo han |
| `_last_wins(a, b)` | Reducer cho state ghi tu parallel branch |
| `LawState` | Shared state gom question, context_id, trace_id, depth, law/tax/compliance/final |
| `analyze_law(state)` | LLM phan tich contract/tort/business law |
| `check_routing(state)` | LLM router tra JSON `needs_tax`, `needs_compliance` |
| `route_to_subagents(state)` | Tra list `Send("call_tax", state)` va/hoac `Send("call_compliance", state)` |
| `call_tax(state)` | Discover `tax_question`, delegate qua A2A den Tax Agent |
| `call_compliance(state)` | Discover `compliance_question`, delegate qua A2A den Compliance Agent |
| `aggregate(state)` | Tong hop law/tax/compliance thanh final answer |
| `create_graph()` | Add nodes/edges va compile StateGraph |

Trong `law_agent/agent_executor.py`:

| Thanh phan code | Chuc nang |
|---|---|
| `_graph = create_graph()` | Compile graph mot lan khi module load |
| `LawAgentExecutor.execute(...)` | Nhan request A2A, invoke graph voi state day du |
| `trace_id`, `context_id`, `delegation_depth` | Metadata duoc propagate xuong sub-agents |
| `answer = result.get("final_answer")` | Lay final answer tu graph |
| `updater.add_artifact(...)` | Tra ket qua ve A2A task |

Trong `law_agent/__main__.py`:

| Thanh phan code | Chuc nang |
|---|---|
| `PORT = 10101` | Port Law Agent |
| `_register_with_retry()` | Register voi Registry |
| `tasks: ["legal_question"]` | Cho Registry biet Law Agent xu ly legal question |
| `AgentCard(...)` | Metadata va endpoint cua Law Agent |
| `AgentSkill(id="legal_question", ...)` | Mo ta skill legal |
| `A2AFastAPIApplication(...)` | Build A2A HTTP app |

### Tax Agent

Thu muc: `tax_agent/`

| File | Chuc nang |
|---|---|
| `tax_agent/graph.py` | Tao ReAct agent chuyen ve tax |
| `tax_agent/agent_executor.py` | Bridge A2A request sang Tax graph |
| `tax_agent/__main__.py` | Start A2A server port 10102, register task `tax_question` |

Trong `tax_agent/graph.py`:

| Thanh phan code | Chuc nang |
|---|---|
| `TAX_SYSTEM_PROMPT` | Prompt chuyen sau ve tax law, IRS, penalties, FBAR/FATCA, transfer pricing |
| `create_graph()` | Tao `create_react_agent(model=llm, tools=[], prompt=TAX_SYSTEM_PROMPT)` |
| `tools=[]` | Tax Agent hien tra loi bang LLM knowledge, chua co tool rieng |

Trong `tax_agent/agent_executor.py`:

| Thanh phan code | Chuc nang |
|---|---|
| `_get_graph()` | Lazy init graph de dung lai |
| `TaxAgentExecutor.execute(...)` | Extract question, invoke graph, lay last AI message |
| `TaskUpdater` | Tra artifact ten `tax_analysis` |
| `_extract_question(context)` | Lay text tu A2A message |

Trong `tax_agent/__main__.py`:

| Thanh phan code | Chuc nang |
|---|---|
| `PORT = 10102` | Port Tax Agent |
| `tasks: ["tax_question"]` | Dang ky kha nang xu ly tax question |
| `AgentCard(...)` | Metadata cua Tax Agent |
| `AgentSkill(id="tax_question", ...)` | Mo ta skill tax |
| `uvicorn.Server(...)` | Chay A2A server |

### Compliance Agent

Thu muc: `compliance_agent/`

| File | Chuc nang |
|---|---|
| `compliance_agent/graph.py` | Tao ReAct agent chuyen ve regulatory compliance |
| `compliance_agent/agent_executor.py` | Bridge A2A request sang Compliance graph |
| `compliance_agent/__main__.py` | Start A2A server port 10103, register task `compliance_question` |

Trong `compliance_agent/graph.py`:

| Thanh phan code | Chuc nang |
|---|---|
| `COMPLIANCE_SYSTEM_PROMPT` | Prompt ve SEC, SOX, FTC, FCPA, AML/BSA, GDPR/CCPA, governance |
| `create_graph()` | Tao `create_react_agent(model=llm, tools=[], prompt=COMPLIANCE_SYSTEM_PROMPT)` |
| `tools=[]` | Compliance Agent hien tra loi bang LLM knowledge, chua co tool rieng |

Trong `compliance_agent/agent_executor.py`:

| Thanh phan code | Chuc nang |
|---|---|
| `_get_graph()` | Lazy init graph |
| `ComplianceAgentExecutor.execute(...)` | Extract question, invoke graph, lay last AI message |
| `TaskUpdater` | Tra artifact ten `compliance_analysis` |
| `_extract_question(context)` | Lay text tu A2A message |

Trong `compliance_agent/__main__.py`:

| Thanh phan code | Chuc nang |
|---|---|
| `PORT = 10103` | Port Compliance Agent |
| `tasks: ["compliance_question"]` | Dang ky kha nang xu ly compliance question |
| `AgentCard(...)` | Metadata cua Compliance Agent |
| `AgentSkill(id="compliance_question", ...)` | Mo ta skill compliance |
| `uvicorn.Server(...)` | Chay A2A server |

### `start_all.sh`

Chuc nang: start toan bo Stage 5.

Thu tu start:

```text
Registry
-> Tax Agent + Compliance Agent
-> Law Agent
-> Customer Agent
```

Ly do:

- Registry phai chay truoc vi agent can register vao Registry.
- Tax/Compliance nen chay truoc Law vi Law se discover va delegate sang chung.
- Customer chay cuoi vi la entry point cua user.

### `test_client.py`

Chuc nang: client test end-to-end.

| Thanh phan code | Chuc nang |
|---|---|
| `CUSTOMER_AGENT_URL` | Endpoint Customer Agent, default `http://localhost:10100` |
| `QUESTION` | Cau hoi test |
| Fetch `/.well-known/agent.json` | Lay Agent Card cua Customer Agent |
| `A2AClient(...)` | Tao client A2A |
| `Message(...)` | Dong goi cau hoi user |
| `SendMessageRequest(...)` | Request gui message |
| `client.send_message(request)` | Gui request den Customer Agent |
| Parse artifacts/parts | Lay text response cuoi cung |

## 9. So sanh nhanh cac stage khi giang

| Stage | Nen noi voi hoc vien |
|---|---|
| Stage 1 | "Day la LLM API call nguyen thuy." |
| Stage 2 | "Bay gio LLM co tay chan: tools va knowledge base." |
| Stage 3 | "Bay gio LLM thanh agent: tu quyet dinh hanh dong." |
| Stage 4 | "Bay gio mot agent thanh mot team chuyen gia." |
| Stage 5 | "Bay gio team chuyen gia thanh cac service doc lap giao tiep qua A2A." |

## 10. File nen mo khi demo tung phan

Thu tu demo de khong bi roi:

```text
1. common/llm.py
2. stages/stage_1_direct_llm/main.py
3. stages/stage_2_rag_tools/main.py
4. exercises/exercise_2_tools.py
5. stages/stage_3_single_agent/main.py
6. stages/stage_4_milti_agent/main.py
7. exercises/exercise_4_multiagent.py
8. registry/__main__.py
9. common/registry_client.py
10. common/a2a_client.py
11. customer_agent/graph.py
12. law_agent/graph.py
13. tax_agent/graph.py
14. compliance_agent/graph.py
15. test_client.py
16. start_all.sh
```

## 11. Lenh chay theo flow lab

Stage 1:

```bash
uv run python stages/stage_1_direct_llm/main.py
```

Stage 2:

```bash
uv run python stages/stage_2_rag_tools/main.py
```

Bai tap Stage 2:

```bash
uv run python exercises/exercise_2_tools.py
```

Stage 3:

```bash
uv run python stages/stage_3_single_agent/main.py
```

Stage 4:

```bash
uv run python stages/stage_4_milti_agent/main.py
```

Bai tap Stage 4:

```bash
uv run python exercises/exercise_4_multiagent.py
```

Stage 5:

```bash
./start_all.sh
```

Terminal khac:

```bash
uv run python test_client.py
```

Chay tung service rieng:

```bash
uv run python -m registry
uv run python -m tax_agent
uv run python -m compliance_agent
uv run python -m law_agent
uv run python -m customer_agent
```

## 12. Debug nhanh

Loi API key:

```bash
cat .env
```

Can kiem tra cac bien:

```text
OPENROUTER_API_KEY
OPENROUTER_MODEL
REGISTRY_URL
```

Loi khong ket noi duoc Customer Agent:

```bash
lsof -i :10100
```

Loi Registry khong co agent:

```bash
curl http://localhost:10000/agents
```

Kiem tra service:

```bash
curl http://localhost:10000/health
curl http://localhost:10100/.well-known/agent.json
curl http://localhost:10101/.well-known/agent.json
curl http://localhost:10102/.well-known/agent.json
curl http://localhost:10103/.well-known/agent.json
```

## 13. Bieu do kien truc va slide

Thu muc can chu y:

```text
docs/slide_bai_giang/
```

File noi dung:

| File | Chu de |
|---|---|
| `01_why_multiagent.svg` | Vi sao can multi-agent |
| `02_a2a_vs_traditional.svg` | A2A vs cach goi truyen thong |
| `03_a2a_protocol.svg` | A2A protocol |
| `04_a2a_system_architecture.svg` | Kien truc full system |
| `05_law_agent_graph.svg` | Law Agent graph |
| `06_request_flow.svg` | Request flow |
| `07_a2a_intro.svg` | Gioi thieu A2A |
| `08_a2a_core_concepts.svg` | Agent Card, Task, Part |
| `09_a2a_interaction_flow.svg` | Interaction flow |
| `10_llm_roadmap.svg` | Roadmap Stage 1 -> Stage 5 |
| `day09-multi-agent-mcp-a2a.pdf` | Slide PDF |
| `day9-MCP-A2A-Infrastructure.html` | Slide/html ve infrastructure |

## 14. Ket luan nen chot bai

Thong diep cuoi bai:

```text
Multi-agent khong phai bat dau bang viec tach service ngay.
Ta di theo tung muc:

LLM -> LLM co tools -> Agent -> Team agent -> Distributed agent system.
```

Khi nao nen dung stage nao:

| Nhu cau | Nen dung |
|---|---|
| Hoi dap don gian | Stage 1 |
| Can tra cuu/tinh toan | Stage 2 |
| Tac vu multi-step | Stage 3 |
| Nhieu domain chuyen mon | Stage 4 |
| Can scale, deploy doc lap, loose coupling | Stage 5 |

