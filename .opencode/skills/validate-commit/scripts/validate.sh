#!/bin/bash
#==============================================================================
# HJPLUS Taiwan Architect Knowledge Base - Validation Script
# 
# This script validates contributions to ensure consistency, format compliance,
# and proper licensing before merging.
# 
# Usage: bash .opencode/skills/validate-commit/scripts/validate.sh
#==============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

#-------------------------------------------------------------------------------
# Helper Functions
#-------------------------------------------------------------------------------

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  HJPLUS 知識庫驗證工具${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

print_check() {
    local status="$1"
    local message="$2"
    if [ "$status" = "PASS" ]; then
        echo -e "✅ ${GREEN}PASS${NC}: $message"
    else
        echo -e "❌ ${RED}FAIL${NC}: $message"
    fi
}

ask_choice() {
    local prompt="$1"
    local options=("$@")
    local num_opts=$(($# - 1))
    
    echo "$prompt"
    for i in $(seq 1 $num_opts); do
        echo "  [$i] ${*:$(($i + 1)):$((num_opts + 1 - $i))}"
    done
    echo ""
    read -p "請選擇 [1-$num_opts]: " choice
    echo ""
}

#-------------------------------------------------------------------------------
# Validation Functions
#-------------------------------------------------------------------------------

validate_single_file() {
    local file="$1"
    local results=()
    local json_results=()
    
    echo -e "${YELLOW}正在檢查: $file${NC}"
    echo "-----------------------------------"
    
    # Check 1: File exists
    if [ -f "$file" ]; then
        results+=("✅ 檔案存在")
        json_results+=("\"file_exists\": true")
    else
        results+=("❌ 檔案不存在")
        json_results+=("\"file_exists\": false")
        return 1
    fi
    
    # Check 2: Extension-based validation
    local ext="${file##*.}"
    local basename=$(basename "$file")
    
    if [ "$ext" = "md" ]; then
        # Check for frontmatter in .md files
        if grep -q '^---' "$file" 2>/dev/null; then
            if [[ "$basename" == "skill.md" ]]; then
                results+=("✅ skill.md has frontmatter (expected)")
                json_results+=("\"has_frontmatter\": true")
            else
                results+=("⚠️  warning: domain.md has frontmatter (should not)")
                json_results+=("\"has_frontmatter_unexpected\": true")
            fi
        else
            if [[ "$basename" == "skill.md" ]]; then
                results+=("❌ skill.md missing frontmatter")
                json_results+=("\"missing_frontmatter\": true")
            else
                results+=("✅ domain.md no frontmatter (expected)")
                json_results+=("\"no_frontmatter\": true")
            fi
        fi
        
        # Check for license
        if grep -qi "CC BY-NC-SA 4.0\|creativecommons.org/licenses/by-nc-sa" "$file"; then
            results+=("✅ License reference found")
            json_results+=("\"has_license\": true")
        else
            results+=("❌ Missing license reference")
            json_results+=("\"has_license\": false")
        fi
        
        # Check for Simplified Chinese
        if grep -q '[^\x00-\x7F]' "$file" 2>/dev/null; then
            if grep -qP '[\x{4e00}-\x{9fff}]' "$file" 2>/dev/null; then
                results+=("⚠️  Contains CJK characters (verify: Simplified?)")
                json_results+=("\"has_cjk_chars\": true")
            fi
        fi
        
        # Check for H1 header
        if grep -q '^# ' "$file"; then
            results+=("✅ H1 header present")
            json_results+=("\"has_h1\": true")
        else
            results+=("❌ Missing H1 header")
            json_results+=("\"has_h1\": false")
        fi
    fi
    
    # Output results
    echo ""
    for result in "${results[@]}"; do
        echo "  $result"
    done
    echo ""
    
    # JSON summary
    local json="{"
    local first=true
    for jr in "${json_results[@]}"; do
        if [ "$first" = "true" ]; then
            first=false
        else
            json+=", "
        fi
        json+="$jr"
    done
    json+="}"
    echo "JSON: $json"
    echo ""
}

validate_pr_files() {
    echo -e "${YELLOW}檢查 PR 新增檔案${NC}"
    echo "========================================"
    echo ""
    
    # Get list of changed files (assuming git available)
    if command -v git &> /dev/null && git rev-parse --git-dir &> /dev/null 2>&1; then
        echo "偵測到 Git 儲存庫"
        echo ""
        read -p "輸入 PR 編號（或直接 Enter 使用 git status --short）: " pr_num
        
        if [ -n "$pr_num" ]; then
            local files=$(git diff --name-only HEAD~1 --format="" 2>/dev/null || echo "")
            if [ -z "$files" ]; then
                files=$(git diff --name-only origin/main --name-only 2>/dev/null || echo "")
            fi
        fi
        
        if [ -z "$files" ]; then
            read -p "輸入要檢查的檔案（用空格分格）: " input_files
            local files=($input_files)
        fi
    else
        read -p "輸入要檢查的檔案（用空格分格）: " input_files
        local files=($input_files)
    fi
    
    if [ ${#files[@]} -eq 0 ] || [ -z "${files[*]}" ]; then
        echo -e "${RED}沒有檔案可檢查${NC}"
        return
    fi
    
    echo "即將檢查 ${#files[@]} 個檔案..."
    echo ""
    
    local all_pass=true
    for f in "${files[@]}"; do
        validate_single_file "$f" || all_pass=false
    done
    
    if [ "$all_pass" = "true" ]; then
        echo -e "${GREEN}✅ 所有檢查通過${NC}"
    else
        echo -e "${RED}❌ 有些檢查失敗，請修正後再試${NC}"
    fi
}

validate_full_repo() {
    echo -e "${YELLOW}全量儲存庫檢查${NC}"
    echo "========================================"
    echo ""
    
    local repo_root="$(git rev-parse --show-toplevel 2>/dev/null || echo ".")"
    cd "$repo_root" || return
    
    echo "掃描中..."
    echo ""
    
    # Check 1: LICENSE exists
    echo -e "${BLUE}[1/8] LICENSE 檔案${NC}"
    if [ -f "LICENSE" ]; then
        print_check "PASS" "LICENSE file exists"
    else
        print_check "FAIL" "LICENSE file missing"
    fi
    
    # Check 2: LICENSE-CODE exists
    echo -e "${BLUE}[2/8] LICENSE-CODE 檔案${NC}"
    if [ -f "LICENSE-CODE" ]; then
        print_check "PASS" "LICENSE-CODE file exists"
    else
        print_check "FAIL" "LICENSE-CODE file missing"
    fi
    
    # Check 3: skill.md files have frontmatter (at the top of file)
    echo -e "${BLUE}[3/8] skill.md frontmatter${NC}"
    local skill_md_count=$(find . -name "skill.md" -type f 2>/dev/null | wc -l)
    local skill_with_fm=0
    while IFS= read -r f; do
        # Frontmatter must be at the beginning (first 3 lines)
        if head -n 3 "$f" 2>/dev/null | grep -q "^---"; then
            skill_with_fm=$((skill_with_fm + 1))
        fi
    done < <(find . -name "skill.md" -type f 2>/dev/null)
    if [ "$skill_with_fm" -eq "$skill_md_count" ]; then
        print_check "PASS" "$skill_with_fm/$skill_md_count skill.md files have frontmatter"
    else
        print_check "FAIL" "$skill_with_fm/$skill_md_count skill.md files have frontmatter"
    fi
    
    # Check 4: domain.md files NO frontmatter (at the top of file)
    echo -e "${BLUE}[4/8] domain.md 無 frontmatter${NC}"
    local domain_md_count=$(find . -name "domain.md" -type f 2>/dev/null | wc -l)
    local domain_with_fm=0
    while IFS= read -r f; do
        # Frontmatter must be at the beginning (first 3 lines)
        if head -n 3 "$f" 2>/dev/null | grep -q "^---"; then
            domain_with_fm=$((domain_with_fm + 1))
        fi
    done < <(find . -name "domain.md" -type f 2>/dev/null)
    if [ "$domain_with_fm" -eq 0 ]; then
        print_check "PASS" "All $domain_md_count domain.md files have no frontmatter"
    else
        print_check "FAIL" "$domain_with_fm/$domain_md_count domain.md files have unexpected frontmatter"
    fi
    
    # Check 5: License references in .md files
    echo -e "${BLUE}[5/8] .md 檔案授權參照${NC}"
    local md_with_license=$(grep -rli "CC BY-NC-SA\|creativecommons.org/licenses/by-nc-sa" --include="*.md" . 2>/dev/null | wc -l)
    local total_md=$(find . -name "*.md" -type f | wc -l)
    if [ "$md_with_license" -gt 0 ]; then
        print_check "PASS" "$md_with_license/$total_md .md files have license reference"
    else
        print_check "FAIL" "No .md files have license reference"
    fi
    
    # Check 6: B-class TODO markers
    echo -e "${BLUE}[6/8] B 類 TODO 標記${NC}"
    local b_class_todos=$(grep -r "TODO: Taiwan adaptation" --include="*.md" . 2>/dev/null | wc -l)
    echo "  找到 $b_class_todos 個 B 類 TODO 標記"
    
    # Check 7: C-class MCP examples
    echo -e "${BLUE}[7/8] C 類 MCP 範例${NC}"
    local c_class_mcp=$(grep -r "taiwan-building-code_search" --include="*.md" . 2>/dev/null | wc -l)
    echo "  找到 $c_class_mcp 個 MCP tool call 範例"
    
    # Check 8: Check for obvious Simplified Chinese common phrases
    echo -e "${BLUE}[8/8] 簡體中文檢查${NC}"
    local zh_cn_phrases="记者|人民币|计算机|软件|网络|电话|手机|电脑|打��机"
    local zh_cn_count=$(grep -riE "$zh_cn_phrases" --include="*.md" . 2>/dev/null | wc -l)
    if [ "$zh_cn_count" -eq 0 ]; then
        print_check "PASS" "No obvious Simplified Chinese phrases found"
    else
        echo "  ⚠️  warning: $zh_cn_count lines may contain Simplified Chinese"
    fi
    
    echo ""
    echo "========================================"
    echo -e "${GREEN}全量檢查完成${NC}"
    echo "========================================"
}

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

main() {
    print_header
    
    echo "選擇檢查模式："
    echo ""
    echo "  [1] 檢查 PR / 新增檔案"
    echo "  [2] 檢查單一檔案"
    echo "  [3] 全量儲存庫檢查"
    echo ""
    read -p "請選擇 [1-3]: " mode
    
    case "$mode" in
        1)
            validate_pr_files
            ;;
        2)
            read -p "輸入檔案路徑: " file
            validate_single_file "$file"
            ;;
        3)
            validate_full_repo
            ;;
        *)
            echo -e "${RED}無效選擇${NC}"
            exit 1
            ;;
    esac
}

main "$@"