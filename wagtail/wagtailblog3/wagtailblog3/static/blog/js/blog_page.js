// wagtailblog3/static/js/custom_scripts.js

$(function() {

    // (A) 初始化 Mermaid.js (这部分逻辑不变)
    try {
        if (typeof mermaid !== 'undefined') {
            mermaid.initialize({ startOnLoad: true });
        }
    } catch (e) {
        console.error("Mermaid.js 初始化失败: ", e);
    }

    // (B) 初始化 KaTeX (这部分逻辑不变)
    try {
        if (typeof renderMathInElement !== 'undefined') {
            renderMathInElement(document.body, {
                delimiters: [
                    {left: "$$", right: "$$", display: true},
                    {left: "\\(", right: "\\)", display: false},
                    {left: "$", right: "$", display: false},
                    {left: "\\[", right: "\\]", display: true}
                ],
                throwOnError: false
            });
        }
    } catch (e) {
        console.error("KaTeX 渲染失败: ", e);
    }

    // (C) 美化 Markdown 表格 (这部分逻辑不变)
    try {
        $('.content-block-wrapper[data-block-type="markdown_block"] table:not([class])').each(function() {
            $(this)
                .addClass('table table-bordered table-hover')
                .wrap('<div class="table-responsive"></div>');
        });
    } catch (e) {
        console.error("自动美化 Markdown 表格失败: ", e);
    }

    // (D) 🚀【最终解决方案】延迟执行 Prism.js 高亮
    // 检查页面上是否存在代码块，只有存在时才设置延迟
    if ($('pre[class*="language-"]').length > 0) {
        console.log("检测到Prism.js代码块，设置延迟高亮...");

        // 延迟100毫秒执行，以确保所有动态加载的Prism脚本都已完成
        setTimeout(function() {
            if (typeof Prism !== 'undefined') {
                console.log("延迟后，Prism.js可用。Firing highlightAll().");
                Prism.highlightAll();
            } else {
                console.error("延迟后，Prism.js仍然不可用！");
            }
        }, 100); // 100毫秒的延迟对于绝大多数情况都已足够
    }
});