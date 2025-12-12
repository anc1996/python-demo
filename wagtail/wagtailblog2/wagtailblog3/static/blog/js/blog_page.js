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
    // 4. TOC 目录与滚动监听 (用户定制版 - 带折叠三角)
    // ===================================
    function initTOC() {
        // 1. 定义容器
        // 注意：在当前 Sticky 布局下，文章内容在 .article-body-content 中，滚动的是 Window
        const contentContainer = document.querySelector('.article-body-content');
        const tocContainer = document.getElementById('toc-content');

        if (!contentContainer || !tocContainer) return;

        // 2. 获取标题 (仅限文章内容区域)
        const headers = contentContainer.querySelectorAll('h2, h3, h4');
        if (headers.length === 0) {
            tocContainer.innerHTML = '<p class="text-muted" style="padding:10px;">暂无目录</p>';
            return;
        }

        // 清空容器
        tocContainer.innerHTML = '';

        // 3. 构建目录树 (保留原本的 Stack 逻辑)
        const tocList = document.createElement('ul');
        tocList.className = 'toc-list';
        let stack = [{ level: 1, element: tocList }]; // 栈底设为 level 1 (兼容 H2 起步)

        headers.forEach((header, index) => {
            if (!header.id) header.id = 'heading-' + index;

            // 获取当前层级 (H2 -> 2, H3 -> 3)
            const currentLevel = parseInt(header.tagName.substring(1));

            // 创建列表项
            const li = document.createElement('li');
            li.className = 'toc-item';
            li.setAttribute('data-target', header.id);

            // 创建条目容器
            const entry = document.createElement('div');
            entry.className = 'toc-entry';

            // 三角折叠按钮
            const toggle = document.createElement('span');
            toggle.className = 'toc-toggle'; // CSS 将处理图标

            // 链接文本
            const a = document.createElement('a');
            a.className = 'toc-link';
            a.textContent = header.innerText;
            a.href = '#' + header.id; // 保持原生锚点行为

            entry.appendChild(toggle);
            entry.appendChild(a);
            li.appendChild(entry);

            // --- 绑定事件 ---

            // 1. 折叠点击
            toggle.addEventListener('click', function(e) {
                e.stopPropagation();
                e.preventDefault();
                // 只有包含子菜单时才切换
                if (li.querySelector('ul')) {
                    li.classList.toggle('collapsed');
                    // 切换图标方向 (通过 CSS 类或直接操作 HTML)
                    const icon = toggle.querySelector('i');
                    if (icon) {
                        icon.classList.toggle('fa-caret-down');
                        icon.classList.toggle('fa-caret-right');
                    }
                }
            });

            // 2. 跳转点击
            a.addEventListener('click', function(e) {
                e.preventDefault();
                isClicking = true;

                // 移除旧激活
                document.querySelectorAll('.toc-link.active').forEach(el => el.classList.remove('active'));
                document.querySelectorAll('.toc-item.active').forEach(el => el.classList.remove('active'));

                this.classList.add('active');
                li.classList.add('active');

                // 计算滚动位置 (适配顶部导航栏高度 80px)
                const targetTop = header.getBoundingClientRect().top + window.scrollY - 100;

                window.scrollTo({ top: targetTop, behavior: 'smooth' });

                // 移动端点击后收起侧边栏
                if (window.innerWidth < 992) {
                    const btn = document.getElementById('btn-hide-left');
                    if(btn) btn.click();
                }

                setTimeout(() => { isClicking = false; }, 800);
            });

            // --- 栈逻辑处理层级嵌套 ---
            let parent = stack[stack.length - 1];

            if (currentLevel > parent.level) {
                // 进入深层：创建新 UL
                const newUl = document.createElement('ul');
                newUl.className = 'toc-sub-menu';

                // 挂载到父级 LI 下
                if (parent.element.lastElementChild && parent.element.lastElementChild.tagName === 'LI') {
                    parent.element.lastElementChild.appendChild(newUl);
                } else {
                    parent.element.appendChild(newUl);
                }
                stack.push({ level: currentLevel, element: newUl });
            } else if (currentLevel < parent.level) {
                // 返回浅层：出栈直到找到对应层级
                while (stack.length > 1 && currentLevel <= stack[stack.length - 1].level) {
                    stack.pop();
                }
            }
            // 挂载当前项
            stack[stack.length - 1].element.appendChild(li);
        });

        // 4. 后处理：添加折叠图标
        const allItems = tocList.querySelectorAll('li.toc-item');
        allItems.forEach(item => {
            const toggle = item.querySelector('.toc-toggle');
            if (item.querySelector('ul')) {
                item.classList.add('has-children');
                // 默认展开：向下箭头
                toggle.innerHTML = '<i class="fa fa-caret-down"></i>';
                toggle.style.cursor = 'pointer';
            } else {
                toggle.classList.add('placeholder'); // 占位，保持缩进对齐
            }
        });

        tocContainer.appendChild(tocList);

        // 5. 滚动监听 (ScrollSpy)
        let isClicking = false;
        let scrollTimeout;

        const onScroll = function() {
            if (isClicking) return;
            if (scrollTimeout) clearTimeout(scrollTimeout);

            scrollTimeout = setTimeout(function() {
                const scrollTop = window.scrollY;
                let currentActiveId = null;

                // 寻找当前视口中最接近顶部的标题
                for (let i = 0; i < headers.length; i++) {
                    const header = headers[i];
                    // 阈值：标题进入视口上方 150px 范围内
                    if ((header.getBoundingClientRect().top + window.scrollY) <= scrollTop + 150) {
                        currentActiveId = header.id;
                    } else {
                        break;
                    }
                }

                if (currentActiveId) {
                    // 移除旧状态
                    const oldActiveLink = tocContainer.querySelector('.toc-link.active');
                    const oldActiveItem = tocContainer.querySelector('.toc-item.active');
                    if (oldActiveLink) oldActiveLink.classList.remove('active');
                    if (oldActiveItem) oldActiveItem.classList.remove('active');

                    // 激活新状态
                    const activeItem = tocContainer.querySelector(`.toc-item[data-target="${currentActiveId}"]`);
                    if (activeItem) {
                        activeItem.classList.add('active');
                        const activeLink = activeItem.querySelector('.toc-link');
                        if (activeLink) activeLink.classList.add('active');

                        // 自动展开父级目录
                        let parent = activeItem.parentElement;
                        while (parent) {
                            if (parent.classList.contains('toc-list')) break;
                            if (parent.tagName === 'UL') {
                                const parentLi = parent.parentElement;
                                if (parentLi && parentLi.classList.contains('toc-item')) {
                                    parentLi.classList.remove('collapsed');
                                    // 确保图标同步为展开状态
                                    const icon = parentLi.querySelector('.toc-toggle i');
                                    if(icon) {
                                        icon.classList.remove('fa-caret-right');
                                        icon.classList.add('fa-caret-down');
                                    }
                                }
                            }
                            parent = parent.parentElement;
                        }
                    }
                }
            }, 50);
        };

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

    // ... 前面是你原有的代码 (initReactions 等) ...

    // ===================================
    // [新增] Zen Mode 沉浸阅读初始化
    // ===================================
    function initZenMode() {
        const container = document.getElementById('blog-layout-container');
        if (!container) return;

        // 获取元素
        const btnHideLeft = document.getElementById('btn-hide-left');
        const btnHideRight = document.getElementById('btn-hide-right');
        const triggerLeft = document.getElementById('zen-trigger-left');
        const triggerRight = document.getElementById('zen-trigger-right');

        // 状态 Key
        const KEY_LEFT = 'blog_hide_left';
        const KEY_RIGHT = 'blog_hide_right';

        // 核心切换逻辑
        function toggleSide(side, hide) {
            const cls = 'hide-sidebar-' + side; // 对应 CSS 类
            const bodyCls = 'zen-' + side + '-hidden'; // 用于控制 Trigger 显示

            if (hide) {
                container.classList.add(cls);
                document.body.classList.add(bodyCls);
            } else {
                container.classList.remove(cls);
                document.body.classList.remove(bodyCls);
            }

            // 存入本地存储
            localStorage.setItem(side === 'left' ? KEY_LEFT : KEY_RIGHT, hide);

            // 触发 resize 事件，确保图表(Mermaid/Echarts)重新自适应宽度
            setTimeout(() => window.dispatchEvent(new Event('resize')), 300);
        }

        // 初始化读取状态
        if (localStorage.getItem(KEY_LEFT) === 'true') toggleSide('left', true);
        if (localStorage.getItem(KEY_RIGHT) === 'true') toggleSide('right', true);

        // 绑定点击事件
        if (btnHideLeft) btnHideLeft.onclick = () => toggleSide('left', true);
        if (btnHideRight) btnHideRight.onclick = () => toggleSide('right', true);

        if (triggerLeft) triggerLeft.onclick = () => toggleSide('left', false);
        if (triggerRight) triggerRight.onclick = () => toggleSide('right', false);
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
    // 执行 Zen Mode 初始化
    initZenMode();
    console.log("🎉 博客页面脚本加载完成");
});