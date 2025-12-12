// wagtailblog3/static/blog/js/blog_page.js

$(function() {
    console.log("🚀 博客页面脚本初始化...");

    // ===================================
    // 0. 工具函数：获取 CSRF Token (这是修复 ReferenceError 的关键)
    // ===================================
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // ===================================
    // 1. 基础插件初始化 (KaTeX)
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
            }
        } catch (e) { console.error("KaTeX error", e); }
    }


    // ===================================
    // 2. 表格美化
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
    // 3. 用户反应 (Reactions) 逻辑 (修复版：状态全量刷新)
    // ===================================
    function initReactions() {
        const reactionContainer = $('.reaction-buttons');
        if (reactionContainer.length === 0) return;

        console.log("👍 初始化反应模块");

        // 绑定点击事件
        reactionContainer.on('click', '.reaction-btn', function(e) {
            e.preventDefault();
            const btn = $(this);
            const container = btn.closest('.reaction-buttons');

            const actionUrl = container.data('action-url');
            const reactionId = btn.data('reaction-id');
            const csrftoken = getCookie('csrftoken'); // 现在 getCookie 已定义，不会报错了

            if (!actionUrl) {
                console.error("❌ 缺少 data-action-url");
                return;
            }

            // 防止快速重复点击
            if (btn.hasClass('processing')) return;
            btn.addClass('processing');

            // 发送 AJAX 请求
            $.ajax({
                url: actionUrl,
                type: 'POST',
                data: JSON.stringify({ reaction_id: reactionId }),
                contentType: 'application/json',
                headers: { 'X-CSRFToken': csrftoken },
                success: function(data) {
                    btn.removeClass('processing');

                    if (data.success) {
                        // 调用 UI 更新函数
                        updateReactionUI(container, data, reactionId);
                    } else {
                        console.error("❌ 更新失败:", data.error);
                    }
                },
                error: function(xhr, status, error) {
                    btn.removeClass('processing');
                    console.error("❌ AJAX 错误:", error);
                }
            });
        });
    }

    /**
     * UI 更新函数：无脑刷新所有按钮状态
     * 解决“只加不减”和“多选高亮”问题的核心逻辑
     */
    function updateReactionUI(container, data, clickedId) {
        const allBtns = container.find('.reaction-btn');

        // 遍历所有按钮，使用后端返回的 counts 强制覆盖前端显示
        allBtns.each(function() {
            const currentBtn = $(this);
            const btnId = currentBtn.data('reaction-id');
            const countSpan = currentBtn.find('.count');

            // A. 更新计数：如果后端没有返回该ID的计数，说明为0
            const newCount = (data.counts && data.counts[btnId]) ? data.counts[btnId] : 0;
            countSpan.text(newCount);

            // B. 更新高亮 (Active) 状态
            // 只有当前点击的按钮，且动作是 'added' 或 'changed' 时才高亮
            // 其他所有按钮一律移除高亮，防止出现两个亮着的按钮
            if (btnId === clickedId) {
                if (data.action === 'added' || data.action === 'changed') {
                    currentBtn.addClass('active');
                } else {
                    currentBtn.removeClass('active'); // 'removed'
                }
            } else {
                // 如果当前发生了 'changed' 或 'added'，说明其他按钮一定不再是活跃状态
                if (data.action === 'added' || data.action === 'changed') {
                     currentBtn.removeClass('active');
                }
                // 如果是 'removed'，说明用户取消了点赞，其他按钮本来就没亮，保持原样即可
            }
        });
    }

    // ===================================
    // 4. TOC 目录与滚动监听 (完整保留逻辑)
    // ===================================
    function initTOC() {
        const scrollContainer = document.getElementById('article-scroll-container');
        const tocContainer = document.getElementById('toc-content');

        if (!scrollContainer || !tocContainer) return;

        const headers = scrollContainer.querySelectorAll('h1, h2, h3, h4');
        if (headers.length === 0) {
            $('.blog-sidebar-left').hide();
            return;
        }

        const tocList = document.createElement('ul');
        tocList.className = 'toc-list';
        let stack = [{ level: 0, element: tocList }];

        headers.forEach((header, index) => {
            if (!header.id) header.id = 'heading-' + index;
            const currentLevel = parseInt(header.tagName.substring(1));
            const li = document.createElement('li');
            li.className = 'toc-item';
            li.setAttribute('data-target', header.id);

            const entry = document.createElement('div');
            entry.className = 'toc-entry';
            const toggle = document.createElement('span');
            toggle.className = 'toc-toggle';
            const a = document.createElement('a');
            a.className = 'toc-link';
            a.textContent = header.innerText;
            a.href = 'javascript:void(0);';

            entry.appendChild(toggle);
            entry.appendChild(a);
            li.appendChild(entry);

            toggle.addEventListener('click', function(e) {
                e.stopPropagation();
                if (li.querySelector('ul')) li.classList.toggle('collapsed');
            });

            a.addEventListener('click', function(e) {
                e.preventDefault();
                isClicking = true;
                document.querySelectorAll('.toc-link').forEach(el => el.classList.remove('active'));
                document.querySelectorAll('.toc-item').forEach(el => el.classList.remove('active'));
                this.classList.add('active');
                li.classList.add('active');

                if (window.innerWidth > 1100) {
                    const targetTop = header.offsetTop - scrollContainer.offsetTop;
                    scrollContainer.scrollTo({ top: targetTop - 20, behavior: 'smooth' });
                } else {
                    const targetTop = header.getBoundingClientRect().top + window.scrollY - 80;
                    window.scrollTo({ top: targetTop, behavior: 'smooth' });
                }
                setTimeout(() => { isClicking = false; }, 600);
            });

            let parent = stack[stack.length - 1];
            if (currentLevel > parent.level) {
                const newUl = document.createElement('ul');
                newUl.className = 'toc-sub-menu';
                if (parent.element.lastElementChild && parent.element.lastElementChild.tagName === 'LI') {
                    parent.element.lastElementChild.appendChild(newUl);
                } else {
                    parent.element.appendChild(newUl);
                }
                stack.push({ level: currentLevel, element: newUl });
            } else if (currentLevel < parent.level) {
                while (stack.length > 1 && currentLevel <= stack[stack.length - 1].level) {
                    stack.pop();
                }
            }
            stack[stack.length - 1].element.appendChild(li);
        });

        const allItems = tocList.querySelectorAll('li.toc-item');
        allItems.forEach(item => {
            const toggle = item.querySelector('.toc-toggle');
            if (item.querySelector('ul')) {
                item.classList.add('has-children');
                toggle.innerHTML = '<i class="fa fa-caret-down"></i>';
            } else {
                toggle.classList.add('placeholder');
            }
        });

        tocContainer.appendChild(tocList);

        let isClicking = false;
        let scrollTimeout;
        const onScroll = function() {
            if (isClicking) return;
            if (scrollTimeout) clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(function() {
                const isDesktop = window.innerWidth > 1100;
                const scrollTop = isDesktop ? scrollContainer.scrollTop : window.scrollY;
                const containerTop = isDesktop ? scrollContainer.offsetTop : 0;
                let currentActiveId = null;

                for (let i = 0; i < headers.length; i++) {
                    const header = headers[i];
                    let headerTop;
                    if (isDesktop) {
                        headerTop = header.offsetTop - containerTop;
                    } else {
                        headerTop = header.getBoundingClientRect().top + window.scrollY;
                    }
                    if (headerTop <= scrollTop + 150) {
                        currentActiveId = header.id;
                    } else {
                        break;
                    }
                }

                if (currentActiveId) {
                    document.querySelectorAll('.toc-link').forEach(el => el.classList.remove('active'));
                    document.querySelectorAll('.toc-item').forEach(el => el.classList.remove('active'));
                    const activeLink = tocContainer.querySelector(`.toc-item[data-target="${currentActiveId}"] .toc-link`);
                    const activeItem = tocContainer.querySelector(`.toc-item[data-target="${currentActiveId}"]`);
                    if (activeLink && activeItem) {
                        activeLink.classList.add('active');
                        activeItem.classList.add('active');
                        let parent = activeItem.parentElement;
                        while (parent) {
                            if (parent.classList.contains('toc-list')) break;
                            if (parent.tagName === 'UL') {
                                const parentLi = parent.parentElement;
                                if (parentLi && parentLi.classList.contains('toc-item')) {
                                    parentLi.classList.remove('collapsed');
                                }
                            }
                            parent = parent.parentElement;
                        }
                    }
                }
            }, 50);
        };
        scrollContainer.addEventListener('scroll', onScroll);
        window.addEventListener('scroll', onScroll);
    }

    // ===================================
    // 5. 移动端布局适配
    // ===================================
    function handleMobileLayout() {
        const sidebarRight = document.getElementById('sidebar-right');
        const mobilePlaceholder = document.getElementById('mobile-interactions-placeholder');
        const breakpoint = 1100;

        function adjustLayout() {
            if (window.innerWidth <= breakpoint) {
                if (sidebarRight && sidebarRight.children.length > 0 && mobilePlaceholder) {
                    while (sidebarRight.children.length > 0) {
                        mobilePlaceholder.appendChild(sidebarRight.children[0]);
                    }
                }
            } else {
                if (mobilePlaceholder && mobilePlaceholder.children.length > 0 && sidebarRight) {
                    while (mobilePlaceholder.children.length > 0) {
                        sidebarRight.appendChild(mobilePlaceholder.children[0]);
                    }
                }
            }
        }

        if (sidebarRight || mobilePlaceholder) {
            adjustLayout();
            window.addEventListener('resize', adjustLayout);
        }
    }

    // ===================================
    // 执行所有初始化
    // ===================================
    beautifyTables();
    initKaTeX();

    // 确保 DOM 元素存在后再执行
    setTimeout(function() {
        handleMobileLayout();
        initTOC();
    }, 100);

    initReactions(); // 启动反应逻辑

    console.log("🎉 博客页面脚本加载完成");
});