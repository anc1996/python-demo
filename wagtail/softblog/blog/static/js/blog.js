document.addEventListener('DOMContentLoaded', function() {
    // 初始化代码高亮
    document.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block);
    });

    // 向所有代码块添加复制按钮
    document.querySelectorAll('pre code').forEach((codeBlock, index) => {
        // 设置ID以便复制功能
        codeBlock.id = `code-${index}`;

        // 创建包装容器
        const wrapper = document.createElement('div');
        wrapper.className = 'code-block';
        codeBlock.parentNode.insertBefore(wrapper, codeBlock);
        wrapper.appendChild(codeBlock);

        // 创建header
        const header = document.createElement('div');
        header.className = 'code-header';

        // 创建复制按钮
        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-button';
        copyBtn.textContent = '复制';
        copyBtn.setAttribute('data-clipboard-target', `#code-${index}`);

        // 将语言标识添加到header
        const language = document.createElement('span');
        language.className = 'language';
        const codeClass = codeBlock.className;
        const langMatch = codeClass.match(/language-(\w+)/);
        language.textContent = langMatch ? langMatch[1] : 'code';

        // 组装header
        header.appendChild(language);
        header.appendChild(copyBtn);

        // 插入header到wrapper
        wrapper.insertBefore(header, codeBlock);
    });

    // 初始化代码复制
    const clipboard = new ClipboardJS('.copy-button');
    clipboard.on('success', function(e) {
        const button = e.trigger;
        button.textContent = '已复制!';
        setTimeout(() => {
            button.textContent = '复制';
        }, 2000);
    });

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