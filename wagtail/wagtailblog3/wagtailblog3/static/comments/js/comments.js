$(document).ready(function() {
    const commentsSection = $('#comments-section');
    if (!commentsSection.length) return;

    const commentForm = $('#comment-form');
    const commentsList = $('#comments-list');
    const loadMoreBtn = $('#load-more-comments');
    const sortBtns = $('.sort-btn');
    const pageId = commentsList.length ? commentsList.attr('data-page-id') : null;

    // 检查登录状态，给所有需要登录的按钮添加重定向功能
    function handleAuthRequired(element) {
        if (!element.hasClass('auth-required')) return;

        element.on('click', function(e) {
            e.preventDefault();
            const loginUrl = `/admin/login/?next=${window.location.pathname}`;
            window.location.href = loginUrl;
        });
    }

    // 处理评论提交
    if (commentForm.length) {
        commentForm.on('submit', function(e) {
            e.preventDefault();

            const submitBtn = $(this).find('#submit-comment');
            submitBtn.prop('disabled', true).text('提交中...');

            const formData = new FormData(this);

            $.ajax({
                url: this.action,
                method: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                success: function(data) {
                    if (data.status === 'success') {
                        commentForm[0].reset();

                        const parentId = $('#comment-parent-id').val();

                        // 处理回复或新评论
                        if (parentId) {
                            // 是回复评论
                            const repliesContainer = $(`#replies-${parentId}`);

                            if (repliesContainer.length) {
                                // 显示回复容器
                                repliesContainer.show();

                                // 添加新回复
                                repliesContainer.append(data.html);

                                // 更新回复计数
                                const showRepliesBtn = $(`.show-replies-btn[data-comment-id="${parentId}"]`);
                                if (showRepliesBtn.length) {
                                    // 获取实际回复数
                                    const replyCount = repliesContainer.find('.reply-item').length;
                                    showRepliesBtn.text(`查看全部 ${replyCount} 条回复`).attr('data-actual-count', replyCount);
                                }
                            }

                            // 重置父评论ID
                            $('#comment-parent-id').val('');
                            $('#replied-to-user-id').val('');
                            $('#reply-to-info').hide();

                            // 将表单移回原位置
                            const formContainer = $('.comment-form-container');
                            if (formContainer.length) {
                                formContainer.append(commentForm);
                            }
                        } else {
                            // 是主评论
                            // 检查是否有"暂无评论"的提示
                            const noComments = commentsList.find('.no-comments');
                            if (noComments.length) {
                                noComments.remove();
                            }

                            // 添加新评论到顶部
                            commentsList.prepend(data.html);

                            // 更新评论计数
                            const commentsCount = $('#comments-count');
                            if (commentsCount.length) {
                                commentsCount.text(parseInt(commentsCount.text() || 0) + 1);
                            }
                        }
                    } else {
                        alert(data.message || '提交评论失败');
                    }
                },
                error: function(error) {
                    console.error('提交评论出错:', error);

                    // 检查是否已成功提交但返回处理有误
                    // 避免重复提交
                    if (commentForm.attr('data-submitted') === 'true') {
                        alert('评论已成功提交，请刷新页面查看');
                    } else {
                        alert('提交评论时出错，请重试');
                    }
                },
                complete: function() {
                    submitBtn.prop('disabled', false).text('发表评论');

                    // 标记表单已尝试提交
                    commentForm.attr('data-submitted', 'true');

                    // 3秒后重置标记
                    setTimeout(() => {
                        commentForm.removeAttr('data-submitted');
                    }, 3000);
                }
            });
        });
    }

    // 处理回复按钮点击
    $(document).on('click', '.reply-btn', function(e) {
        // 检查登录状态
        if ($(this).hasClass('auth-required')) return;

        const commentId = $(this).attr('data-comment-id');
        const username = $(this).attr('data-username');
        const userId = $(this).attr('data-user-id');

        if (!commentForm.length || !commentId || !username) return;

        // 设置父评论ID和被回复用户ID
        $('#comment-parent-id').val(commentId);
        $('#replied-to-user-id').val(userId);

        // 显示回复信息
        const replyToInfo = $('#reply-to-info');
        const replyToName = $('#reply-to-name');

        if (replyToInfo.length && replyToName.length) {
            replyToName.text(username);
            replyToInfo.show();
        }

        // 移动表单到回复位置
        const repliesContainer = $(`#replies-${commentId}`);
        if (repliesContainer.length) {
            repliesContainer.show();
            repliesContainer.append(commentForm);
        }

        // 聚焦输入框
        $('#comment-content').focus();
    });

    // 处理取消回复
    const cancelReply = $('#cancel-reply');
    if (cancelReply.length) {
        cancelReply.on('click', function() {
            // 重置父评论ID和被回复用户ID
            $('#comment-parent-id').val('');
            $('#replied-to-user-id').val('');

            // 隐藏回复信息
            $('#reply-to-info').hide();

            // 将表单移回原位置
            const formContainer = $('.comment-form-container');
            if (formContainer.length) {
                formContainer.append(commentForm);
            }
        });
    }

    // 处理点赞/踩
    $(document).on('click', '.vote-btn', function(e) {
        const voteBtn = $(this);

        // 检查登录状态
        if (voteBtn.hasClass('auth-required')) return;

        const commentId = voteBtn.attr('data-comment-id');
        const reactionType = voteBtn.attr('data-reaction');

        // 处理点赞/踩逻辑
    });

    // 加载评论回复
    $(document).on('click', '.show-replies-btn', function(e) {
        if (!e.target.classList.contains('show-replies-btn')) return;

        const commentId = e.target.getAttribute('data-comment-id');
        const repliesContainer = $(`#replies-${commentId}`);

        if (!repliesContainer.length) return;

        // 如果已经加载过，则只是切换显示状态
        if (repliesContainer.children().length > 0) {
            const isVisible = repliesContainer.css('display') !== 'none';
            repliesContainer.css('display', isVisible ? 'none' : 'block');

            // 使用存储的实际回复数
            const actualCount = e.target.getAttribute('data-actual-count');

            e.target.textContent = isVisible ?
                `查看全部 ${actualCount} 条回复` :
                '收起回复';
            return;
        }

        // 加载回复
        e.target.textContent = '加载中...';

        $.ajax({
            url: `/comments/load-replies/${commentId}/`,
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(data) {
                if (data.status === 'success') {
                    repliesContainer.html(data.html);
                    repliesContainer.css('display', 'block');
                    e.target.textContent = `收起回复`;

                    // 存储实际回复数量
                    e.target.setAttribute('data-actual-count', data.reply_count);

                    // 给新加载的按钮添加登录检查
                    repliesContainer.find('.auth-required').each(function() {
                        handleAuthRequired(this);
                    });
                } else {
                    e.target.textContent = `查看全部回复`;
                    alert(data.message || '加载回复失败');
                }
            },
            error: function(error) {
                console.error('加载回复出错:', error);
                e.target.textContent = `查看全部回复`;
                alert('加载回复失败，请重试');
            }
        });
    });

    // 加载更多评论
    if (loadMoreBtn.length) {
        loadMoreBtn.on('click', function() {
            const page = this.getAttribute('data-page');
            const sortBy = $('.sort-btn.active').attr('data-sort');

            this.textContent = '加载中...';
            this.disabled = true;

            $.ajax({
                url: `/comments/load/${pageId}/?page=${page}&sort=${sortBy}`,
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                success: function(data) {
                    if (data.status === 'success') {
                        // 添加评论到列表
                        commentsList.append(data.html);

                        // 更新加载更多按钮
                        if (data.has_next) {
                            this.setAttribute('data-page', parseInt(page) + 1);
                            this.textContent = '加载更多评论';
                            this.disabled = false;
                        } else {
                            this.parentNode.remove();
                        }

                        // 给新加载的按钮添加登录检查
                        commentsList.find('.auth-required').each(function() {
                            handleAuthRequired(this);
                        });
                    } else {
                        this.textContent = '加载更多评论';
                        this.disabled = false;
                        alert(data.message || '加载评论失败');
                    }
                },
                error: function(error) {
                    console.error('加载评论出错:', error);
                    this.textContent = '加载更多评论';
                    this.disabled = false;
                    alert('加载评论失败，请重试');
                }
            });
        });
    }

    // 处理排序按钮
    sortBtns.each(function() {
        $(this).on('click', function() {
            const sortBy = $(this).attr('data-sort');

            // 更新按钮状态
            sortBtns.removeClass('active');
            $(this).addClass('active');

            // 加载排序后的评论
            $.ajax({
                url: `/comments/load/${pageId}/?sort=${sortBy}`,
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                success: function(data) {
                    if (data.status === 'success') {
                        // 替换评论列表
                        commentsList.html(data.html);

                        // 更新加载更多按钮
                        if (loadMoreBtn.length) {
                            if (data.has_next) {
                                loadMoreBtn.attr('data-page', 2);
                                loadMoreBtn.css('display', 'block');
                            } else {
                                loadMoreBtn.css('display', 'none');
                            }
                        }

                        // 给新加载的按钮添加登录检查
                        commentsList.find('.auth-required').each(function() {
                            handleAuthRequired(this);
                        });
                    } else {
                        alert(data.message || '加载评论失败');
                    }
                },
                error: function(error) {
                    console.error('加载评论出错:', error);
                    alert('加载评论失败，请重试');
                }
            });
        });
    });

    // 处理评论编辑
    $(document).on('click', '.edit-btn', function(e) {
        if (!e.target.classList.contains('edit-btn')) return;

        const commentId = $(this).attr('data-comment-id');
        const commentText = $(`#comment-text-${commentId}`);

        if (!commentText.length) return;

        // 已经在编辑状态
        if (commentText.find('textarea').length) return;

        // 保存原始内容
        const originalContent = commentText.html();
        let contentText = commentText.text().trim();

        // 如果是回复且包含@用户名，需要去除
        const replyToTag = commentText.find('.reply-to-tag');
        if (replyToTag.length) {
            contentText = contentText.replace(replyToTag.text(), '').trim();
        }

        // 创建编辑表单
        const editForm = $('<form class="edit-comment-form">');
        editForm.html(`
            <textarea>${contentText}</textarea>
            <div class="edit-actions">
                <button type="button" class="cancel-edit">取消</button>
                <button type="submit">保存</button>
            </div>
        `);

        // 替换评论内容为编辑表单
        commentText.html('');
        commentText.append(editForm);

        // 聚焦文本框
        const textarea = editForm.find('textarea');
        textarea.focus();
        textarea.setSelectionRange(textarea.val().length, textarea.val().length);

        // 处理取消编辑
        editForm.find('.cancel-edit').on('click', function() {
            commentText.html(originalContent);
        });

        // 处理提交编辑
        editForm.on('submit', function(event) {
            event.preventDefault();

            const newContent = textarea.val().trim();
            if (!newContent) {
                alert('评论内容不能为空');
                return;
            }

            // 禁用按钮
            const submitBtn = $(this).find('[type="submit"]');
            submitBtn.prop('disabled', true).text('保存中...');

            // 获取CSRF令牌
            const csrfToken = getCookie('csrftoken');

            $.ajax({
                url: '/comments/edit/',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                data: {
                    comment_id: commentId,
                    content: encodeURIComponent(newContent)
                },
                success: function(data) {
                    if (data.status === 'success') {
                        // 更新评论内容
                        if (replyToTag.length) {
                            commentText.html(replyToTag.outerHTML + ' ' + data.content);
                        } else {
                            commentText.html(data.content);
                        }
                    } else {
                        alert(data.message || '保存失败');
                        commentText.html(originalContent);
                    }
                },
                error: function(error) {
                    console.error('保存评论出错:', error);
                    alert('保存失败，请重试');
                    commentText.html(originalContent);
                },
                complete: function() {
                    submitBtn.prop('disabled', false).text('保存');
                }
            });
        });
    });

    // 处理评论删除
    $(document).on('click', '.delete-btn', function(e) {
        if (!e.target.classList.contains('delete-btn')) return;

        if (!confirm('确定要删除这条评论吗？')) return;

        const commentId = $(this).attr('data-comment-id');
        const commentItem = $(`#comment-${commentId}`);

        if (!commentItem.length) return;

        // 获取CSRF令牌
        const csrfToken = getCookie('csrftoken');

        $.ajax({
            url: '/comments/delete/',
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            data: {
                comment_id: commentId
            },
            success: function(data) {
                if (data.status === 'success') {
                    // 更新评论内容为"已删除"
                    const commentText = commentItem.find(`#comment-text-${commentId}`);
                    if (commentText.length) {
                        commentText.html('<em>此评论已被删除</em>');
                    }

                    // 禁用所有按钮
                    commentItem.find('button').prop('disabled', true).css('opacity', 0.5);
                } else {
                    alert(data.message || '删除失败');
                }
            },
            error: function(error) {
                console.error('删除评论出错:', error);
                alert('删除失败，请重试');
            }
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
    commentsList.find('.auth-required').each(function() {
        handleAuthRequired(this);
    });
});