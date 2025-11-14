// wagtailblog3/static/blog/js/blog_page.js

$(function() {
    console.log("🚀 博客页面初始化...");


    // ===================================
    // KaTeX 数学公式
    // ===================================
    function initKaTeX() {
        try {
            if (typeof renderMathInElement !== 'undefined') {
                renderMathInElement(document.body, {
                    delimiters: [
                        {left: "$$", right: "$$", display: true},
                        {left: "\\[", right: "\\]", display: true},
                        {left: "$", right: "$", display: false},
                        {left: "\\(", right: "\\)", display: false}
                    ],
                    throwOnError: false
                });
                console.log("✅ KaTeX 渲染完成");
            }
        } catch (e) {
            console.error("❌ KaTeX 失败:", e);
        }
    }

    // ===================================
    // 表格美化
    // ===================================
    function beautifyTables() {
        try {
            $('.content-block-wrapper[data-block-type="markdown_block"] table:not([class])').each(function() {
                $(this)
                    .addClass('table table-bordered table-hover')
                    .wrap('<div class="table-responsive"></div>');
            });
            console.log("✅ 表格美化完成");
        } catch (e) {
            console.error("❌ 表格美化失败:", e);
        }
    }

    // ===================================
    // 按顺序执行
    // ===================================
    beautifyTables();
    initKaTeX();

    console.log("🎉 博客页面脚本加载完成");
});