# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

### Exercise 1: Scaffold a New Feature: extract_action_items_llm()

Toi prompt
```
look at this file(extract.py) and read it, telll me about each function
example:
_is_action_line: check if a line is a action statememnt or not
extract_action_items: do this do that, given input, it would parse each lines and.....
```

Toi muon no hieu context du an truoc

Toi prompt:
```
You are a coding assistant and very familiar with integrating AI into system. You already knew the function of extract_action_items, that is returning the final list of unique action items; The way it work is still logic-based extracting. Now, i want you implement the same function extract_action_items_llm() but instead, using AI model to scan input, and automatically extracting list of action items, where all items are applied the same pattern format as extract_action_items does. My local MAC already installed llama3.1:8b in Ollama. Here is reference to produce structured outputs: https://ollama.com/blog/structured-outputs. Ask me questtions if you want to clarify anything that make your work easier and better.

Planiing first, then i would confirm and you implement
``` 
Toi cho no mot Role, no da phan nao biet context cua dua an, noi qua lai ve ham extract_action_item(), noi ro ve myGoal, noi qua ve he thong may toi chay model gi, toi co reference tai lieu nhung co ve nhu no khong doc qua; Toi bao noi hoi toi truoc de lam ro van de; Roi toi bao no plan truoc de toi xac nhan

### Exercise 2: Add Unit Tests
Toi proompt
```
implement plan for me

(context: after approval of the implementation plan, tests were requested and validated with pytest)
``` 
No tu dong tao cac test cho toi

### Exercise 3: Refactor Existing Code for Clarity
toi prompt:
```
Perform a refactor of the code in the backend, focusing in particular on well-defined API contracts/schemas, database layer cleanup, app lifecycle/configuration, error handling. 
```

No giup toi refactor code, kem them tai lieu REFACTORING.md, tu dong test lai

### NOTE: CONTEXT.md, PROCESS.md
Tai thoi diem nay, truuowc khi chuyen sang Ex4, toi cam thay agent dang thuc hien cham dan, co dau hieu chay sai, ket qua khong dung, Toi prompt:
```
Help me write CONTEXT.md file about this project, and then summary our process so far into PROCESS.md
```

Toi nhan hai file CONTEXT.md noi ve tong quan toan bo du an, va PROCESS.md noi ve qua trinh toi va AI lam viec den bay gio. Ca hai file deu giup AI hieu duoc CONTEXT ngay khi toi chuyen sang cua so chat moi

Toi nhan ra, moi lan toi ask no lam dieu gi, no deu tu dong chay test laij, va tom tat lai nhuwng thay doi ma no thuc hieen. Dieu do khong lam tang len Context qua nhieu, chi ton token nhuwng giup AI hieu ro hon du an va cac lan thuc hien sau toot  hon.

### Exercise 4: Use Agentic Mode to Automate a Small Task
Toi dinh kem hai file vao chat moi: CONTEXT.md, PROCESS.md, Toi prompt:
```
Expose one final endpoint to retrieve all notes. Update the frontend to include a "List Notes" button that, when clicked, fetches and displays them.
```

Toi khong thay no chay quet cac file de hieu lai du an nua(ro rang la hai file CONTEXT.md va PROCESS.md giup AI hieu du an ma do ton TOKEN).

Toi da check va moi thuc deu hoat dong dung.

### Exercise 5: Generate a README from the Codebase
Toi prompt:
```
analyze the current codebase and generate a well-structured `README.md` file. The README should include, at a minimum:
- A brief overview of the project
- How to set up and run the project
- API endpoints and functionality
- Instructions for running the test suite
```