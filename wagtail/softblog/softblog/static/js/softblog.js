document.addEventListener('DOMContentLoaded', function() {
    // 初始化代码高亮配置
    hljs.configure({
        languages: ['javascript', 'python', 'java', 'html', 'css', 'bash', 'c', 'cpp', 'csharp', 'go', 'php', 'sql', 'typescript'],
        tabReplace: '    '
    });

    // 高亮所有代码块
    document.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block);
        enhanceCodeBlock(block);
    });

    // 初始化代码复制功能
    initializeClipboard();

    // 初始化数学公式渲染
    if (typeof renderMathInElement !== 'undefined') {
        renderMathInElement(document.body, {
            delimiters: [
                {left: '$$', right: '$$', display: true},
                {left: '$', right: '$', display: false},
                {left: '\\(', right: '\\)', display: false},
                {left: '\\[', right: '\\]', display: true}
            ],
            throwOnError: false
        });
    }
});

// 增强代码块，添加语言标签和复制按钮
function enhanceCodeBlock(codeBlock) {
    const preElement = codeBlock.parentElement;
    if (!preElement || preElement.tagName !== 'PRE') return;

    // 给代码块添加ID
    if (!codeBlock.id) {
        codeBlock.id = 'code-' + Math.random().toString(36).substr(2, 9);
    }

    // 获取语言
    let language = '';
    const classMatch = codeBlock.className.match(/language-(\w+)/);
    language = classMatch ? classMatch[1] : 'code';

    // 创建代码块头部
    const codeHeader = document.createElement('div');
    codeHeader.className = 'code-header';

    // 添加语言标签
    const languageLabel = document.createElement('span');
    languageLabel.className = 'language-label';
    languageLabel.textContent = language;
    codeHeader.appendChild(languageLabel);

    // 创建复制按钮
    const copyButton = document.createElement('button');
    copyButton.className = 'copy-button';
    copyButton.setAttribute('data-clipboard-target', `#${codeBlock.id}`);
    copyButton.textContent = '复制';
    codeHeader.appendChild(copyButton);

    // 在pre元素前插入代码头部
    preElement.insertAdjacentElement('afterbegin', codeHeader);
}

// 初始化代码复制功能
function initializeClipboard() {
    if (typeof ClipboardJS !== 'undefined') {
        const clipboard = new ClipboardJS('.copy-button');

        clipboard.on('success', function(e) {
            const button = e.trigger;
            button.textContent = '已复制';

            setTimeout(() => {
                button.textContent = '复制';
            }, 2000);

            e.clearSelection();
        });
    }
}