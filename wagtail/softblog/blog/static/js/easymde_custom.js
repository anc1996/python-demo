window.wagtailMarkdown = window.wagtailMarkdown || {};
window.wagtailMarkdown.options = {
    autofocus: false,
    spellChecker: false,
    indentWithTabs: true,
    tabSize: 4,
    toolbar: [
        "bold", "italic", "heading", "|",
        "code", "quote", "unordered-list", "ordered-list", "|",
        "link", "image", "table", "|",
        "preview", "side-by-side", "fullscreen"
    ],
    status: ["autosave", "lines", "words", "cursor"],
    renderingConfig: {
        codeSyntaxHighlighting: true
    },
    shortcuts: {
        "togglePreview": "Ctrl-P",
        "toggleSideBySide": "Ctrl-Alt-P",
        "drawTable": "Ctrl-Alt-T"
    }
};