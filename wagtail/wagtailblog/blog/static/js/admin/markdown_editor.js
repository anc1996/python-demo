(function() {
    // 等待 DOM 加载完成
    document.addEventListener('DOMContentLoaded', function() {
        // 找到所有 Markdown 编辑器字段
        const markdownFields = document.querySelectorAll('.field-content [data-streamfield-block-type="markdown_block"]');

        markdownFields.forEach(function(field) {
            // 获取文本区域
            const textarea = field.querySelector('textarea');
            if (!textarea) return;

            // 创建工具栏
            const toolbar = document.createElement('div');
            toolbar.className = 'markdown-toolbar';

            // 添加工具栏按钮组
            const buttonGroups = [
                // 标题组
                [
                    { name: 'h1', text: 'H1', action: () => insertText(textarea, '# ', '') },
                    { name: 'h2', text: 'H2', action: () => insertText(textarea, '## ', '') },
                    { name: 'h3', text: 'H3', action: () => insertText(textarea, '### ', '') },
                ],
                // 文本格式组
                [
                    { name: 'bold', text: 'B', action: () => insertText(textarea, '**', '**') },
                    { name: 'italic', text: 'I', action: () => insertText(textarea, '*', '*') },
                    { name: 'strike', text: '~', action: () => insertText(textarea, '~~', '~~') },
                ],
                // 链接和媒体组
                [
                    { name: 'link', text: '🔗', action: () => insertText(textarea, '[', '](url)') },
                    { name: 'image', text: '🖼️', action: () => insertText(textarea, '![alt text](', ')') },
                ],
                // 列表组
                [
                    { name: 'ul', text: '•', action: () => insertText(textarea, '- ', '') },
                    { name: 'ol', text: '1.', action: () => insertText(textarea, '1. ', '') },
                    { name: 'task', text: '☑', action: () => insertText(textarea, '- [ ] ', '') },
                ],
                // 代码和数学组
                [
                    { name: 'code', text: '`{}`', action: () => insertCodeBlock(textarea) },
                    { name: 'math', text: '∑', action: () => insertText(textarea, '$$\n', '\n$$') },
                ],
                // 其他组
                [
                    { name: 'quote', text: '❝', action: () => insertText(textarea, '> ', '') },
                    { name: 'hr', text: '―', action: () => insertText(textarea, '\n---\n', '') },
                    { name: 'table', text: '◫', action: () => insertTable(textarea) },
                ]
            ];

            // 为每个按钮组创建一个容器
            buttonGroups.forEach(function(group) {
                const groupDiv = document.createElement('div');
                groupDiv.className = 'markdown-toolbar-group';

                group.forEach(function(button) {
                    const btn = document.createElement('button');
                    btn.type = 'button';
                    btn.className = `markdown-${button.name}-button`;
                    btn.title = button.name.charAt(0).toUpperCase() + button.name.slice(1);
                    btn.textContent = button.text;
                    btn.addEventListener('click', button.action);
                    groupDiv.appendChild(btn);
                });

                toolbar.appendChild(groupDiv);
            });

            // 创建预览区域
            const previewContainer = document.createElement('div');
            previewContainer.className = 'markdown-preview-container';

            const previewToggle = document.createElement('button');
            previewToggle.type = 'button';
            previewToggle.className = 'markdown-preview-toggle';
            previewToggle.textContent = '预览';

            const preview = document.createElement('div');
            preview.className = 'markdown-preview';
            preview.style.display = 'none';

            previewContainer.appendChild(previewToggle);
            previewContainer.appendChild(preview);

            // 切换预览
            previewToggle.addEventListener('click', function() {
                if (preview.style.display === 'none') {
                    // 显示预览
                    preview.innerHTML = markdownToHtml(textarea.value);
                    preview.style.display = 'block';
                    textarea.style.display = 'none';
                    previewToggle.textContent = '编辑';
                } else {
                    // 返回编辑
                    preview.style.display = 'none';
                    textarea.style.display = 'block';
                    previewToggle.textContent = '预览';
                }
            });

            // 将工具栏和预览区域添加到编辑器
            textarea.parentNode.insertBefore(toolbar, textarea);
            textarea.parentNode.appendChild(previewContainer);

            // 添加样式
            textarea.style.height = '400px';
            textarea.style.fontFamily = 'monospace';
            textarea.style.padding = '10px';
            textarea.style.lineHeight = '1.5';

            // 添加快捷键支持
            textarea.addEventListener('keydown', function(e) {
                // Ctrl+B: 粗体
                if (e.ctrlKey && e.key === 'b') {
                    e.preventDefault();
                    insertText(textarea, '**', '**');
                }
                // Ctrl+I: 斜体
                else if (e.ctrlKey && e.key === 'i') {
                    e.preventDefault();
                    insertText(textarea, '*', '*');
                }
                // Ctrl+K: 链接
                else if (e.ctrlKey && e.key === 'k') {
                    e.preventDefault();
                    insertText(textarea, '[', '](url)');
                }
            });
        });
    });

    // 辅助函数：在光标位置插入文本
    function insertText(textarea, before, after) {
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const text = textarea.value;
        const selection = text.substring(start, end);

        textarea.value = text.substring(0, start) + before + selection + after + text.substring(end);

        // 重新设置光标位置
        textarea.focus();
        textarea.setSelectionRange(start + before.length, start + before.length + selection.length);
    }

    // 插入代码块，带有语言选择
    function insertCodeBlock(textarea) {
        const languages = ['python', 'javascript', 'html', 'css', 'bash', 'sql', 'java', 'php', 'c', 'cpp'];
        const language = prompt('请选择编程语言（默认为python）: ' + languages.join(', '), 'python');

        if (language !== null) {
            insertText(textarea, '```' + language + '\n', '\n```');
        }
    }

    // 插入表格
    function insertTable(textarea) {
        const rows = prompt('表格行数:', '3');
        const cols = prompt('表格列数:', '3');

        if (rows !== null && cols !== null) {
            let tableText = '';

            // 表头
            tableText += '| ';
            for (let c = 0; c < parseInt(cols); c++) {
                tableText += `列${c+1} | `;
            }
            tableText += '\n';

            // 分隔线
            tableText += '| ';
            for (let c = 0; c < parseInt(cols); c++) {
                tableText += '--- | ';
            }
            tableText += '\n';

            // 表格内容
            for (let r = 0; r < parseInt(rows) - 1; r++) {
                tableText += '| ';
                for (let c = 0; c < parseInt(cols); c++) {
                    tableText += `内容 | `;
                }
                tableText += '\n';
            }

            insertText(textarea, tableText, '');
        }
    }

    // 辅助函数：增强的 Markdown 到 HTML 转换（用于预览）
    function markdownToHtml(markdown) {
        // 简化版本，实际应用中应使用更完整的库
        let html = markdown
            // 代码块处理（需要在其他处理之前）
            .replace(/```(\w*)\n([\s\S]*?)```/g, function(match, lang, code) {
                return `<pre><code class="language-${lang}">${escapeHtml(code)}</code></pre>`;
            })
            // 数学公式
            .replace(/\$\$([\s\S]*?)\$\$/g, '<div class="math">$1</div>')
            // 标题
            .replace(/^# (.*?)$/gm, '<h1>$1</h1>')
            .replace(/^## (.*?)$/gm, '<h2>$1</h2>')
            .replace(/^### (.*?)$/gm, '<h3>$1</h3>')
            .replace(/^#### (.*?)$/gm, '<h4>$1</h4>')
            // 加粗、斜体、删除线
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/~~(.*?)~~/g, '<del>$1</del>')
            // 链接和图片
            .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>')
            .replace(/!\[(.*?)\]\((.*?)\)/g, '<img src="$2" alt="$1">')
            // 任务列表
            .replace(/^- \[ \] (.*?)$/gm, '<div class="task-list-item"><input type="checkbox" disabled> $1</div>')
            .replace(/^- \[x\] (.*?)$/gm, '<div class="task-list-item"><input type="checkbox" checked disabled> $1</div>')
            // 引用
            .replace(/^> (.*?)$/gm, '<blockquote>$1</blockquote>')
            // 水平线
            .replace(/^\s*---\s*$/gm, '<hr>')
            // 列表
            .replace(/^- (.*?)$/gm, '<li>$1</li>')
            .replace(/^\d+\. (.*?)$/gm, '<li>$1</li>')
            // 段落
            .replace(/([^\n]+)(?:\n|$)/g, function(match, p1) {
                if (/<\/(h1|h2|h3|h4|blockquote|pre|li|div|hr)>/.test(p1)) return match;
                return '<p>' + p1 + '</p>\n';
            });

        return html;
    }

    // 辅助函数：HTML转义
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
})();