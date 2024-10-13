tinymce.init({
    selector: '#markdown',
    // 中文
    language: 'zh_CN',
    plugins: [
    "markdown", "advlist", "anchor", "autolink", "charmap", "code", "fullscreen",
    "help", "image", "insertdatetime", "link", "lists", "media",
    "preview", "searchreplace", "table", "visualblocks",
    ],
    toolbar: "undo redo | styles | bold italic underline strikethrough | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image",
    height: 600,
    content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:16px }',
    markdown_symbols: {
        C: '©', TM: '™', R: '®'
    },
    branding:false,
    setup: function (editor) {
    // 添加一个自定义按钮到工具栏
        editor.ui.registry.addButton('copyMarkdown', {
            text: 'Copy Markdown',
            onAction: function () {
                // 获取 Markdown 内容
                editor.plugins.markdown.getContent().then(function (markdownContent) {
                  // 将 Markdown 内容插入到编辑器中
                  editor.execCommand('mceInsertContent', false, markdownContent);
                });
            }
        });
    }
});