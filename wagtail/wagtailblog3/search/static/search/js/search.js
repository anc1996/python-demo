document.addEventListener('DOMContentLoaded', function() {
    // 搜索过滤器
    const filterButtons = document.querySelectorAll('.filter-button');
    const searchForm = document.getElementById('search-form');

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const type = this.dataset.type;
            const url = new URL(window.location);
            url.searchParams.set('type', type);
            url.searchParams.set('page', '1');
            window.location.href = url.toString();
        });
    });

    // 搜索建议功能
    const searchInput = document.getElementById('search-input');
    const suggestionsBox = document.getElementById('suggestions');
    let debounceTimer;

    searchInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        const query = this.value.trim();

        if (query.length < 2) {
            suggestionsBox.style.display = 'none';
            return;
        }

        debounceTimer = setTimeout(() => {
            fetch(`/search/suggestions/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.suggestions.length > 0) {
                        displaySuggestions(data.suggestions);
                    } else {
                        suggestionsBox.style.display = 'none';
                    }
                });
        }, 300);
    });

    function displaySuggestions(suggestions) {
        suggestionsBox.innerHTML = '';
        suggestions.forEach(suggestion => {
            const item = document.createElement('div');
            item.className = 'suggestion-item';
            item.textContent = suggestion.query;
            item.addEventListener('click', function() {
                searchInput.value = suggestion.query;
                searchForm.submit();
            });
            suggestionsBox.appendChild(item);
        });
        suggestionsBox.style.display = 'block';
    }

    // 点击外部隐藏建议
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
            suggestionsBox.style.display = 'none';
        }
    });

    // 高亮搜索词
    function highlightSearchTerms() {
        const searchQuery = '{{ search_query|escapejs }}';
        if (!searchQuery) return;

        const terms = searchQuery.split(' ').filter(term => term.length > 0);
        const elements = document.querySelectorAll('.result-title a, .result-intro');

        elements.forEach(element => {
            let html = element.innerHTML;
            terms.forEach(term => {
                const regex = new RegExp(`(${term})`, 'gi');
                html = html.replace(regex, '<span class="highlight">$1</span>');
            });
            element.innerHTML = html;
        });
    }

    highlightSearchTerms();
});