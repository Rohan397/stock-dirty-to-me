import os
import sys
from github import Github
from langchain_community.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

def get_pr_changes():
    """Get the changes in the current PR"""
    g = Github(os.getenv('GITHUB_TOKEN'))
    repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))
    pr_number = int(os.getenv('GITHUB_REF').split('/')[-2])
    pr = repo.get_pull(pr_number)
    
    changes = []
    for file in pr.get_files():
        if file.filename != 'README.md':
            changes.append(f"File: {file.filename}\nChanges: {file.patch}")
    
    return "\n\n".join(changes)

def generate_readme_suggestion(changes):
    """Generate a suggestion for README updates based on code changes"""
    model = OllamaLLM(model="llama2")
    
    template = """
    You are an expert at maintaining documentation. Based on the following code changes in a pull request, 
    suggest updates to the README.md file. Only suggest updates if the changes affect user-facing functionality 
    or require documentation updates. If no documentation updates are needed, respond with "No README updates needed."

    Code changes:
    {changes}

    Please provide your suggestion in the following format:
    ```markdown
    [Your suggested README updates here]
    ```
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    
    result = chain.invoke({"changes": changes})
    return result

def create_comment(suggestion):
    """Create a comment on the PR with the README suggestion"""
    g = Github(os.getenv('GITHUB_TOKEN'))
    repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))
    pr_number = int(os.getenv('GITHUB_REF').split('/')[-2])
    pr = repo.get_pull(pr_number)
    
    comment_body = f"""
    🤖 **README Update Suggestion**
    
    {suggestion}
    
    Please review these suggested updates to the README.md file. If you agree, you can apply these changes to your PR.
    """
    
    pr.create_issue_comment(comment_body)

def main():
    changes = get_pr_changes()
    suggestion = generate_readme_suggestion(changes)
    
    if "No README updates needed" not in suggestion:
        create_comment(suggestion)

if __name__ == "__main__":
    main()