##Step1
Dau tien du an rat don gian, toi yeu cau copilot viet file CLAUDE.md cho toi:

'''Read the entire repository structure in /week4, then write a CLAUDE.md file 
that captures:
- What this project does in 2-3 sentences
- How to run, test, format, and lint the project
- Where key files live (routers, models, tests, config)
- The tech stack and conventions used
- Safe commands to run
- Commands to avoid
- Any workflow rules a developer should follow

Ask me anything for your better understanding'''

Thuc chat day la bai thuc hanh su dung Claude Code cho vibecoding nen nhung thu toi thao tac chir la tuowng trung

##Step2
Toi yeu cau no tao slash command (nhung command /docs-sync, /ttd-feature) giup ta thuc hien cac task repeatable

##step3
Toi yeu cau no viet cac sub-agent(/test-agent.md, /code-agent.md)

#Step4 
Toi yeu cau no implement mot chuc nang Search
'''
run ttd-feature for : add Search endpoint for notes
- Add/extend `GET /notes/search?q=...` (case-insensitive) using SQLAlchemy filters
- Update `frontend/app.js` to use the search query
- Add tests in `backend/tests/test_notes.py` '''

trong ttd-feature: se spawn 2 sub agent la test-agent : gen ra cac test case roi test, ra loi thif code-agent viet code de pass test-case do, lap 2 vong ta duocj chuc nang do