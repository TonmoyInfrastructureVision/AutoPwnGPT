#!/bin/bash

# Author: Eshan Roy
# Date: 2025.01.27
# Description: Automates the process of committing and pushing changes to a GitLab repository
#              with support for conventional commit messages, including options for reverting commits.

# ==========================
# Color Definitions
# ==========================
RESET="\e[0m"
GREEN="\e[32m"
RED="\e[31m"
YELLOW="\e[33m"
BLUE="\e[34m"
CYAN="\e[36m"
MAGENTA="\e[35m"

# ==========================
# Function Definitions
# ==========================

# Check and configure Git user details
configure_git_user() {
    if [[ -z $(git config --get user.name) ]]; then
        echo -e "${YELLOW}Git username is not configured.${RESET}"
        read -p "Enter your Git username: " GIT_USERNAME
        git config --global user.name "$GIT_USERNAME"
    fi

    if [[ -z $(git config --get user.email) ]]; then
        echo -e "${YELLOW}Git email is not configured.${RESET}"
        read -p "Enter your Git email: " GIT_EMAIL
        git config --global user.email "$GIT_EMAIL"
    fi

    echo -e "${GREEN}Git user details configured.${RESET}"
}

# Display usage instructions
usage() {
    echo -e "${GREEN}Usage: $0 [options]${RESET}"
    echo -e "${YELLOW}Options:${RESET}"
    echo -e "  -b, --branch <branch_name>   Specify the branch to push to (default: current branch)"
    echo -e "  -h, --help                   Show this help message"
    exit 1
}

# Display commit types
display_commit_types() {
    echo -e "${CYAN}Select a conventional commit type:${RESET}"
    echo -e "1) ${GREEN}🚀 Feature:${RESET} A new feature"
    echo -e "2) ${RED}🐛 Fix:${RESET} A bug fix"
    echo -e "3) ${YELLOW}📚 Documentation:${RESET} Documentation only changes"
    echo -e "4) ${MAGENTA}🎨 Style:${RESET} Changes that do not affect the meaning of the code (white-space, formatting, etc.)"
    echo -e "5) ${BLUE}🧹 Chore:${RESET} Changes to the build process or auxiliary tools and libraries"
    echo -e "6) ${GREEN}⚡ Performance:${RESET} A code change that improves performance"
    echo -e "7) ${RED}🛠️ Refactor:${RESET} A code change that neither fixes a bug nor adds a feature"
    echo -e "8) ${YELLOW}🧪 Test:${RESET} Adding missing tests or correcting existing tests"
    echo -e "9) ${MAGENTA}⏪ Revert:${RESET} Revert a previous commit"
    echo -e "10) ${BLUE}🔐 Security:${RESET} Security improvements"
    echo -e "11) ${CYAN}🚧 WIP:${RESET} Work in progress"
}

# Check for uncommitted changes
check_uncommitted_changes() {
    if [[ -z $(git status --porcelain) ]]; then
        echo -e "${YELLOW}No changes to commit.${RESET}"
        exit 0
    fi
}

# Log the last few commits
log_commits() {
    echo -e "${CYAN}Last few commits:${RESET}"
    git log --oneline -n 5
}

# Get the current branch name
get_current_branch() {
    if [[ -f .git/HEAD ]]; then
        BRANCH=$(cat .git/HEAD | sed 's|ref: refs/heads/||')
    else
        echo -e "${RED}Error: Unable to determine the current branch.${RESET}"
        exit 1
    fi
}

# ==========================
# Main Script Logic
# ==========================

# Default branch
BRANCH=""

# Parse command-line options
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -b|--branch) BRANCH="$2"; shift ;;
        -h|--help) usage ;;
        *) echo -e "${RED}Unknown option: $1${RESET}"; usage ;;
    esac
    shift
done

# Check and configure Git user details
configure_git_user

# If no branch is specified, get the current branch
if [[ -z "$BRANCH" ]]; then
    get_current_branch
fi

# Check for uncommitted changes
check_uncommitted_changes

# Display commit types
display_commit_types

# Read user selection for commit type
read -p "Enter the number corresponding to your choice: " choice

# Map user choice to conventional commit type
case $choice in
    1) COMMIT_TYPE="🚀 Feature:" ;;
    2) COMMIT_TYPE="🐛 Fix:" ;;
    3) COMMIT_TYPE="📚 Documentation:" ;;
    4) COMMIT_TYPE="🎨 Style:" ;;
    5) COMMIT_TYPE="🧹 Chore:" ;;
    6) COMMIT_TYPE="⚡ Performance:" ;;
    7) COMMIT_TYPE="🛠️ Refactor:" ;;
    8) COMMIT_TYPE="🧪 Test:" ;;
    9) 
        # Handle revert case
        log_commits
        read -p "Enter the commit hash to revert: " COMMIT_HASH
        if git revert "$COMMIT_HASH"; then
            echo -e "${GREEN}Commit $COMMIT_HASH reverted successfully.${RESET}"
            # Push the revert commit
            if ! git push origin "$BRANCH"; then
                echo -e "${RED}Push failed. Please check for errors.${RESET}"
                exit 1
            fi
            log_commits
            exit 0
        else
            echo -e "${RED}Failed to revert commit $COMMIT_HASH. Please check for errors.${RESET}"
            exit 1
        fi
        ;;
    10) COMMIT_TYPE="🔐 Security:" ;;
    11) COMMIT_TYPE="🚧 WIP:" ;;
    *) echo -e "${RED}Invalid choice${RESET}"; exit 1 ;;
esac

# Prompt for commit description
read -p "Enter a brief description for the commit: " COMMIT_DESCRIPTION

# Construct the full commit message
COMMIT_MESSAGE="$COMMIT_TYPE $COMMIT_DESCRIPTION"

# Automatically stage all changes
git add .

# Commit with the constructed message
if ! git commit -m "$COMMIT_MESSAGE"; then
    echo -e "${RED}Commit failed. Please check for errors.${RESET}"
    exit 1
fi

# Push changes to the specified branch
if ! git push origin "$BRANCH"; then
    echo -e "${RED}Push failed. Please check for errors.${RESET}"
    exit 1
fi

# Log the last few commits
log_commits

# Output success message
echo -e "${GREEN}Changes pushed successfully to branch: $BRANCH with message: $COMMIT_MESSAGE${RESET}"