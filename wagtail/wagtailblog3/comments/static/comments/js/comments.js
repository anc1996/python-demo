document.addEventListener('DOMContentLoaded', function() {
    const commentsSection = document.getElementById('comments-section');
    if (!commentsSection) return;

    const commentForm = document.getElementById('comment-form');
    const commentsList = document.getElementById('comments-list');
    const loadMoreBtn = document.getElementById('load-more-comments');
    const sortBtns = document.querySelectorAll('.sort-btn');
    const pageId = commentsList ? commentsList.getAttribute('data-page-id') : null;

    // 检查登录状态，给所有需要登录的按钮添加重定向功能
    function handleAuthRequired(element) {
        if (!element.classList.contains('auth-required')) return;

        element.addEventListener('click', function(e) {
            e.preventDefault();
            const loginUrl = `/admin/login/?next=${window.location.pathname}`;
            window.location.href = loginUrl;
        });
    }

// 处理评论提交
if (commentForm) {
    commentForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const submitBtn = this.querySelector('#submit-comment');
        submitBtn.disabled = true;
        submitBtn.textContent = '提交中...';

        const formData = new FormData(this);

        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            // 首先检查HTTP状态码是否成功
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                // 重置表单
                this.reset();

                const parentId = document.getElementById('comment-parent-id').value;

                // 处理回复或新评论
                if (parentId) {
                    // 是回复评论
                    const repliesContainer = document.getElementById(`replies-${parentId}`);

                    if (repliesContainer) {
                        // 显示回复容器
                        repliesContainer.style.display = 'block';

                        // 添加新回复
                        repliesContainer.insertAdjacentHTML('beforeend', data.html);

                        // 更新回复计数
                        const showRepliesBtn = document.querySelector(`.show-replies-btn[data-comment-id="${parentId}"]`);
                        if (showRepliesBtn) {
                            // 获取实际回复数
                            const replyCount = repliesContainer.querySelectorAll('.reply-item').length;
                            showRepliesBtn.textContent = `查看全部 ${replyCount} 条回复`;
                            showRepliesBtn.setAttribute('data-actual-count', replyCount);
                        }
                    }

                    // 重置父评论ID
                    document.getElementById('comment-parent-id').value = '';
                    document.getElementById('replied-to-user-id').value = '';
                    document.getElementById('reply-to-info').style.display = 'none';

                    // 将表单移回原位置
                    const formContainer = document.querySelector('.comment-form-container');
                    if (formContainer) {
                        formContainer.appendChild(commentForm);
                    }
                } else {
                    // 是主评论
                    // 检查是否有"暂无评论"的提示
                    const noComments = commentsList.querySelector('.no-comments');
                    if (noComments) {
                        noComments.remove();
                    }

                    // 添加新评论到顶部
                    commentsList.insertAdjacentHTML('afterbegin', data.html);

                    // 更新评论计数
                    const commentsCount = document.getElementById('comments-count');
                    if (commentsCount) {
                        commentsCount.textContent = parseInt(commentsCount.textContent || 0) + 1;
                    }
                }
            } else {
                alert(data.message || '提交评论失败');
            }
        })
        .catch(error => {
            console.error('提交评论出错:', error);

            // 检查是否已成功提交但返回处理有误
            // 避免重复提交
            if (commentForm.getAttribute('data-submitted') === 'true') {
                alert('评论已成功提交，请刷新页面查看');
            } else {
                alert('提交评论时出错，请重试');
            }
        })
        .finally(() => {
            submitBtn.disabled = false;
            submitBtn.textContent = '发表评论';

            // 标记表单已尝试提交
            commentForm.setAttribute('data-submitted', 'true');

            // 3秒后重置标记
            setTimeout(() => {
                commentForm.removeAttribute('data-submitted');
            }, 3000);
        });
    });
}

    // 处理回复按钮点击
    document.addEventListener('click', function(e) {
        if (!e.target.classList.contains('reply-btn')) return;

        // 检查登录状态
        if (e.target.classList.contains('auth-required')) return;

        const commentId = e.target.getAttribute('data-comment-id');
        const username = e.target.getAttribute('data-username');
        const userId = e.target.getAttribute('data-user-id');

        if (!commentForm || !commentId || !username) return;

        // 设置父评论ID和被回复用户ID
        document.getElementById('comment-parent-id').value = commentId;
        document.getElementById('replied-to-user-id').value = userId;

        // 显示回复信息
        const replyToInfo = document.getElementById('reply-to-info');
        const replyToName = document.getElementById('reply-to-name');

        if (replyToInfo && replyToName) {
            replyToName.textContent = username;
            replyToInfo.style.display = 'inline-block';
        }

        // 移动表单到回复位置
        const repliesContainer = document.getElementById(`replies-${commentId}`);
        if (repliesContainer) {
            repliesContainer.style.display = 'block';
            repliesContainer.appendChild(commentForm);
        }

        // 聚焦输入框
        document.getElementById('comment-content').focus();
    });

    // 处理取消回复
    const cancelReply = document.getElementById('cancel-reply');
    if (cancelReply) {
        cancelReply.addEventListener('click', function() {
            // 重置父评论ID和被回复用户ID
            document.getElementById('comment-parent-id').value = '';
            document.getElementById('replied-to-user-id').value = '';

            // 隐藏回复信息
            document.getElementById('reply-to-info').style.display = 'none';

            // 将表单移回原位置
            const formContainer = document.querySelector('.comment-form-container');
            if (formContainer) {
                formContainer.appendChild(commentForm);
            }
        });
    }

    // 处理点赞/踩
    document.addEventListener('click', function(e) {
        if (!e.target.classList.contains('vote-btn') && !e.target.closest('.vote-btn')) return;

        const voteBtn = e.target.classList.contains('vote-btn') ? e.target : e.target.closest('.vote-btn');

        // 检查登录状态
        if (voteBtn.classList.contains('auth-required')) return;

        const commentId = voteBtn.getAttribute('data-comment-id');
        const reactionType = voteBtn.getAttribute('data-reaction');

        // 获取CSRF令牌
        const csrfToken = getCookie('csrftoken');

        fetch('/comments/react/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: `comment_id=${commentId}&reaction_type=${reactionType}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 更新点赞/踩计数
                const likeCount = voteBtn.closest('.comment-votes, .reply-votes').querySelector('.like-count');
                const dislikeCount = voteBtn.closest('.comment-votes, .reply-votes').querySelector('.dislike-count');

                if (likeCount) likeCount.textContent = data.like_count;
                if (dislikeCount) dislikeCount.textContent = data.dislike_count;

                // 更新按钮状态
                const likeBtn = voteBtn.closest('.comment-votes, .reply-votes').querySelector('.like-btn');
                const dislikeBtn = voteBtn.closest('.comment-votes, .reply-votes').querySelector('.dislike-btn');

                if (data.action === 'removed') {
                    // 取消反应
                    voteBtn.classList.remove('active');
                } else {
                    // 新增或更改反应
                    if (parseInt(reactionType) === 1) {
                        likeBtn.classList.add('active');
                        dislikeBtn.classList.remove('active');
                    } else {
                        likeBtn.classList.remove('active');
                        dislikeBtn.classList.add('active');
                    }
                }
            } else {
                alert(data.message || '操作失败');
            }
        })
        .catch(error => {
            console.error('点赞/踩出错:', error);
            alert('操作失败，请重试');
        });
    });

// 加载评论回复
document.addEventListener('click', function(e) {
    if (!e.target.classList.contains('show-replies-btn')) return;

    const commentId = e.target.getAttribute('data-comment-id');
    const repliesContainer = document.getElementById(`replies-${commentId}`);

    if (!repliesContainer) return;

    // 如果已经加载过，则只是切换显示状态
    if (repliesContainer.children.length > 0) {
        const isVisible = repliesContainer.style.display !== 'none';
        repliesContainer.style.display = isVisible ? 'none' : 'block';

        // 使用存储的实际回复数
        const actualCount = e.target.getAttribute('data-actual-count');

        e.target.textContent = isVisible ?
            `查看全部 ${actualCount} 条回复` :
            '收起回复';
        return;
    }

    // 加载回复
    e.target.textContent = '加载中...';

    fetch(`/comments/load-replies/${commentId}/`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            repliesContainer.innerHTML = data.html;
            repliesContainer.style.display = 'block';
            e.target.textContent = `收起回复`;

            // 存储实际回复数量
            e.target.setAttribute('data-actual-count', data.reply_count);

            // 给新加载的按钮添加登录检查
            repliesContainer.querySelectorAll('.auth-required').forEach(handleAuthRequired);
        } else {
            e.target.textContent = `查看全部回复`;
            alert(data.message || '加载回复失败');
        }
    })
    .catch(error => {
        console.error('加载回复出错:', error);
        e.target.textContent = `查看全部回复`;
        alert('加载回复失败，请重试');
    });
});
    // 加载更多评论
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            const sortBy = document.querySelector('.sort-btn.active').getAttribute('data-sort');

            this.textContent = '加载中...';
            this.disabled = true;

            fetch(`/comments/load/${pageId}/?page=${page}&sort=${sortBy}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // 添加评论到列表
                    commentsList.insertAdjacentHTML('beforeend', data.html);

                    // 更新加载更多按钮
                    if (data.has_next) {
                        this.setAttribute('data-page', parseInt(page) + 1);
                        this.textContent = '加载更多评论';
                        this.disabled = false;
                    } else {
                        this.parentNode.remove();
                    }

                    // 给新加载的按钮添加登录检查
                    commentsList.querySelectorAll('.auth-required').forEach(handleAuthRequired);
                } else {
                    this.textContent = '加载更多评论';
                    this.disabled = false;
                    alert(data.message || '加载评论失败');
                }
            })
            .catch(error => {
                console.error('加载评论出错:', error);
                this.textContent = '加载更多评论';
                this.disabled = false;
                alert('加载评论失败，请重试');
            });
        });
    }

    // 处理排序按钮
    sortBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const sortBy = this.getAttribute('data-sort');

            // 更新按钮状态
            sortBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');

            // 加载排序后的评论
            fetch(`/comments/load/${pageId}/?sort=${sortBy}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // 替换评论列表
                    commentsList.innerHTML = data.html;

                    // 更新加载更多按钮
                    if (loadMoreBtn) {
                        if (data.has_next) {
                            loadMoreBtn.setAttribute('data-page', 2);
                            loadMoreBtn.style.display = 'block';
                        } else {
                            loadMoreBtn.style.display = 'none';
                        }
                    }

                    // 给新加载的按钮添加登录检查
                    commentsList.querySelectorAll('.auth-required').forEach(handleAuthRequired);
                } else {
                    alert(data.message || '加载评论失败');
                }
            })
            .catch(error => {
                console.error('加载评论出错:', error);
                alert('加载评论失败，请重试');
            });
        });
    });

    // 处理评论编辑
    document.addEventListener('click', function(e) {
        if (!e.target.classList.contains('edit-btn')) return;

        const commentId = e.target.getAttribute('data-comment-id');
        const commentText = document.getElementById(`comment-text-${commentId}`);

        if (!commentText) return;

        // 已经在编辑状态
        if (commentText.querySelector('textarea')) return;

        // 保存原始内容
        const originalContent = commentText.innerHTML;
        let contentText = commentText.textContent.trim();

        // 如果是回复且包含@用户名，需要去除
        const replyToTag = commentText.querySelector('.reply-to-tag');
        if (replyToTag) {
            contentText = contentText.replace(replyToTag.textContent, '').trim();
        }

        // 创建编辑表单
        const editForm = document.createElement('form');
        editForm.className = 'edit-comment-form';
        editForm.innerHTML = `
            <textarea>${contentText}</textarea>
            <div class="edit-actions">
                <button type="button" class="cancel-edit">取消</button>
                <button type="submit">保存</button>
            </div>
        `;

        // 替换评论内容为编辑表单
        commentText.innerHTML = '';
        commentText.appendChild(editForm);

        // 聚焦文本框
        const textarea = editForm.querySelector('textarea');
        textarea.focus();
        textarea.setSelectionRange(textarea.value.length, textarea.value.length);

        // 处理取消编辑
        editForm.querySelector('.cancel-edit').addEventListener('click', function() {
            commentText.innerHTML = originalContent;
        });

        // 处理提交编辑
        editForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const newContent = textarea.value.trim();
            if (!newContent) {
                alert('评论内容不能为空');
                return;
            }

            // 禁用按钮
            const submitBtn = this.querySelector('[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = '保存中...';

            // 获取CSRF令牌
            const csrfToken = getCookie('csrftoken');

            fetch('/comments/edit/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: `comment_id=${commentId}&content=${encodeURIComponent(newContent)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // 更新评论内容
                    if (replyToTag) {
                        commentText.innerHTML = replyToTag.outerHTML + ' ' + data.content;
                    } else {
                        commentText.innerHTML = data.content;
                    }
                } else {
                    alert(data.message || '保存失败');
                    commentText.innerHTML = originalContent;
                }
            })
            .catch(error => {
                console.error('保存评论出错:', error);
                alert('保存失败，请重试');
                commentText.innerHTML = originalContent;
            });
        });
    });

    // 处理评论删除
    document.addEventListener('click', function(e) {
        if (!e.target.classList.contains('delete-btn')) return;

        if (!confirm('确定要删除这条评论吗？')) return;

        const commentId = e.target.getAttribute('data-comment-id');
        const commentItem = document.getElementById(`comment-${commentId}`);

        if (!commentItem) return;

        // 获取CSRF令牌
        const csrfToken = getCookie('csrftoken');

        fetch('/comments/delete/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: `comment_id=${commentId}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 更新评论内容为"已删除"
                const commentText = commentItem.querySelector(`#comment-text-${commentId}`);
                if (commentText) {
                    commentText.innerHTML = '<em>此评论已被删除</em>';
                }

                // 禁用所有按钮
                const buttons = commentItem.querySelectorAll('button');
                buttons.forEach(btn => {
                    btn.disabled = true;
                    btn.style.opacity = 0.5;
                });
            } else {
                alert(data.message || '删除失败');
            }
        })
        .catch(error => {
            console.error('删除评论出错:', error);
            alert('删除失败，请重试');
        });
    });

    // 工具函数：获取Cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // 初始化：检查所有需要登录的元素
    document.querySelectorAll('.auth-required').forEach(handleAuthRequired);
});