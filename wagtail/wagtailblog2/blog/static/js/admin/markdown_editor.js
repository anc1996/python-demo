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

            // 添加工具栏按钮
            const buttons = [
                { name: 'h1', text: 'H1', action: () => insertText(textarea, '# ', '') },
                { name: 'h2', text: 'H2', action: () => insertText(textarea, '## ', '') },
                { name: 'h3', text: 'H3', action: () => insertText(textarea, '### ', '') },
                { name: 'bold', text: 'B', action: () => insertText(textarea, '**', '**') },
                { name: 'italic', text: 'I', action: () => insertText(textarea, '*', '*') },
                { name: 'link', text: '🔗', action: () => insertText(textarea, '[', '](url)') },
                { name: 'image', text: '🖼️', action: () => insertText(textarea, '![alt text](', ')') },
                { name: 'code', text: '`{}`', action: () => insertText(textarea, '```\n', '\n```') },
                { name: 'quote', text: '❝', action: () => insertText(textarea, '> ', '') },
                { name: 'list', text: '•', action: () => insertText(textarea, '- ', '') },
                { name: 'math', text: '∑', action: () => insertText(textarea, '$$\n', '\n$$') },
            ];

            buttons.forEach(function(button) {
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = `markdown-${button.name}-button`;
                btn.textContent = button.text;
                btn.addEventListener('click', button.action);
                toolbar.appendChild(btn);
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
            textarea.style.height = '300px';
            textarea.style.fontFamily = 'monospace';

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

    // 辅助函数：简单的 Markdown 到 HTML 转换（仅用于预览）
    function markdownToHtml(markdown) {
        // 这只是一个简单的实现，实际应用中应使用更完整的 Markdown 解析库
        let html = markdown
            // 标题
            .replace(/^# (.*?)$/gm, '<h1>$1</h1>')
            .replace(/^## (.*?)$/gm, '<h2>$1</h2>')
            .replace(/^### (.*?)$/gm, '<h3>$1</h3>')
            // 加粗和斜体
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            // 链接
            .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>')
            // 图片
            .replace(/!\[(.*?)\]\((.*?)\)/g, '<img src="$2" alt="$1">')
            // 代码块
            .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
            // 引用
            .replace(/^> (.*?)$/gm, '<blockquote>$1</blockquote>')
            // 列表
            .replace(/^- (.*?)$/gm, '<li>$1</li>')
            // 段落
            .replace(/([^\n]+)(?:\n|$)/g, function(match, p1) {
                if (/<\/(h1|h2|h3|blockquote|pre|ul|ol|li)>/.test(p1)) return match;
                return '<p>' + p1 + '</p>\n';
            });
        return html;
    }
})();