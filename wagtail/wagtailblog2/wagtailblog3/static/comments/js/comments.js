// comments.js - 完整版本，使用HTML模板

const CommentSystem = (function() {
    'use strict';

    // ===== 模板管理器 =====
    const TemplateManager = {
        /**
         * 获取模板并克隆
         */
        getTemplate(templateId) {
            const template = $(`#${templateId}`);
            if (!template.length) {
                console.warn(`模板 ${templateId} 不存在`);
                return $();
            }
            return template.children().first().clone().removeClass('template-hidden');
        },

        /**
         * 显示登录提示
         */
        showLoginPrompt() {
            const $commentsList = $('#comments-list');
            if ($commentsList.find('.login-prompt').length > 0) {
                return; // 已存在
            }

            const $loginPrompt = this.getTemplate('login-prompt-template');
            $commentsList.append($loginPrompt);
        },

        /**
         * 显示暂无评论
         */
        showNoComments() {
            const $commentsList = $('#comments-list');
            if ($commentsList.find('.no-comments').length > 0) {
                return; // 已存在
            }

            const $noComments = this.getTemplate('no-comments-template');
            $commentsList.append($noComments);
        },

        /**
         * 显示加载指示器
         */
        showLoadingIndicator() {
            const $commentsList = $('#comments-list');
            const $loading = this.getTemplate('loading-indicator-template');
            $commentsList.append($loading);
            return $loading;
        },

        /**
         * 显示回复加载指示器
         */
        showRepliesLoading($container) {
            const $loading = this.getTemplate('replies-loading-template');
            $container.append($loading);
            return $loading;
        },

        /**
         * 创建编辑表单
         */
        createEditForm(commentId, currentContent) {
            const $editForm = this.getTemplate('edit-form-template');
            $editForm.find('.edit-textarea').val(currentContent);
            $editForm.find('.save-edit-btn').attr('data-comment-id', commentId);
            $editForm.find('.cancel-edit-btn').attr('data-comment-id', commentId);
            return $editForm;
        },

        /**
         * 显示错误消息
         */
        showError(message, $container = null) {
            const $error = this.getTemplate('error-message-template');
            $error.find('.error-text').text(message);

            if ($container) {
                $container.append($error);
                // 3秒后自动移除
                setTimeout(() => $error.fadeOut(300, () => $error.remove()), 3000);
            } else {
                // 全局错误提示
                alert('❌ ' + message);
            }
        },

        /**
         * 显示成功消息
         */
        showSuccess(message, $container = null) {
            const $success = this.getTemplate('success-message-template');
            $success.find('.success-text').text(message);

            if ($container) {
                $container.append($success);
                // 2秒后自动移除
                setTimeout(() => $success.fadeOut(300, () => $success.remove()), 2000);
            } else {
                console.log('✅ ' + message);
            }
        }
    };

    // ===== 认证管理器 =====
    const AuthManager = {
        isAuthenticated() {
            return $('#main-comment-form-wrapper').length > 0 &&
                   $('#main-comment-form-wrapper').find('form').length > 0;
        },

        showLoginPrompt() {
            TemplateManager.showLoginPrompt();
        },

        redirectToLogin() {
            console.log('重定向到登录页面');
            const currentUrl = encodeURIComponent(window.location.pathname + window.location.search);
            const loginUrl = `/admin/login/?next=${currentUrl}`;
            console.log('登录URL:', loginUrl);
            window.location.href = loginUrl;
        },

        requireAuth(callback) {
            if (this.isAuthenticated()) {
                callback();
                return true;
            } else {
                alert('请先登录才能进行此操作！');
                this.redirectToLogin();
                return false;
            }
        }
    };

    // ===== AJAX管理器 =====
    const AjaxManager = {
        getCookie(name) {
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
        },

        handleError(xhr, defaultMessage = '操作失败，请重试') {
            let message = defaultMessage;

            if (xhr.status === 403) {
                message = '权限不足，请重新登录';
                setTimeout(() => AuthManager.redirectToLogin(), 1500);
            } else if (xhr.status === 429) {
                message = xhr.responseJSON?.message || '操作太频繁，请稍后再试';
            } else if (xhr.responseJSON?.message) {
                message = xhr.responseJSON.message;
            }

            TemplateManager.showError(message);
        },

        post(url, data = {}) {
            if (typeof data === 'object' && !(data instanceof FormData)) {
                data.csrfmiddlewaretoken = this.getCookie('csrftoken');
            }

            return $.ajax({
                url,
                method: 'POST',
                data,
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                ...(data instanceof FormData ? {
                    processData: false,
                    contentType: false
                } : {})
            });
        },

        get(url, data = {}) {
            return $.ajax({
                url,
                method: 'GET',
                data,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
        }
    };

    // ===== 表单管理器 =====
const FormManager = {
    activeReplyForm: null,

    /**
     * 重置所有回复表单
     */
    resetReplyForms() {
        $('.active-reply-form').remove();
        $('.dynamic-reply-form-container').empty();
        this.activeReplyForm = null;
        console.log('🧹 所有回复表单已重置');
    },

    /**
     * 创建回复表单 - 修复版本
     */
    createReplyForm(commentId, username, userId, rootCommentId) {
        console.log('💬 创建回复表单:', {
            commentId,
            username,
            userId,
            rootCommentId
        });

        // 先重置现有表单
        this.resetReplyForms();

        // 关键修复：找到正确的目标容器
        let $targetContainer;

        if (commentId === rootCommentId) {
            // 这是一级评论的回复
            console.log('📝 这是一级评论的回复');
            $targetContainer = $(`#comment-${commentId}`)
                .find('> .inner-box > .comment-content-wrapper > .dynamic-reply-form-container')
                .first();
        } else {
            // 这是二级评论的回复，应该添加到一级评论（rootCommentId）下
            console.log('📝 这是二级评论的回复，添加到一级评论下');
            $targetContainer = $(`#comment-${rootCommentId}`)
                .find('> .inner-box > .comment-content-wrapper > .dynamic-reply-form-container')
                .first();
        }

        console.log('🎯 目标容器:', {
            found: $targetContainer.length > 0,
            container: $targetContainer[0]
        });

        if (!$targetContainer.length) {
            console.error('❌ 未找到回复表单容器');
            alert('无法创建回复表单，请刷新页面重试');
            return;
        }

        // 克隆主表单
        const $originalForm = $('#main-comment-form-wrapper').find('form');
        if (!$originalForm.length) {
            console.error('❌ 未找到原始表单');
            return;
        }

        const $newForm = $originalForm.clone();

        // 为克隆的表单生成唯一ID，避免冲突
        const uniqueId = `reply-form-${Date.now()}`;
        $newForm.attr('id', uniqueId);
        $newForm.find('#comment-content').attr('id', `comment-content-${uniqueId}`);
        $newForm.find('#comment-parent-id').attr('id', `comment-parent-id-${uniqueId}`);
        $newForm.find('#replied-to-user-id').attr('id', `replied-to-user-id-${uniqueId}`);

        // 创建包装容器
        const $wrapper = $('<div>')
            .addClass('active-reply-form')
            .attr('data-reply-to-comment', commentId)
            .attr('data-root-comment', rootCommentId)
            .append($newForm);

        // 设置表单字段
        const pageId = $('#comments-list').attr('data-page-id');
        $newForm.attr('action', `/comments/post/${pageId}/`);
        $newForm.find(`#comment-parent-id-${uniqueId}`).val(rootCommentId); // 始终使用根评论ID
        $newForm.find(`#replied-to-user-id-${uniqueId}`).val(userId);

        // 预填充内容
        const $textarea = $newForm.find(`#comment-content-${uniqueId}`);
        $textarea.val(`@${username} `);

        // 显示回复信息
        const $replyInfo = $newForm.find('#reply-to-info');
        $replyInfo.find('#reply-to-name').text(username);
        $replyInfo.removeClass('template-hidden').show();

        // 清空目标容器并添加新表单
        $targetContainer.empty().append($wrapper);

        // 聚焦输入框
        $textarea.focus();

        // 将光标移到末尾
        const textLength = $textarea.val().length;
        $textarea[0].setSelectionRange(textLength, textLength);

        this.activeReplyForm = $wrapper;

        console.log('✅ 回复表单创建成功');

        // 滚动到表单
        $('html, body').animate({
            scrollTop: $wrapper.offset().top - 100
        }, 500);

        // 添加视觉提示：高亮目标评论
        this.highlightTargetComment(commentId);
    },

    /**
     * 高亮目标评论 - 新增功能
     */
    highlightTargetComment(commentId) {
        // 移除之前的高亮
        $('.comment').removeClass('comment-replying');

        // 高亮当前要回复的评论
        $(`#comment-${commentId}`).addClass('comment-replying');

        // 3秒后移除高亮
        setTimeout(() => {
            $(`#comment-${commentId}`).removeClass('comment-replying');
        }, 3000);
    },

    /**
     * 提交表单
     */
    submitForm(form, isReply = false) {
        const $form = $(form);
        const $submitBtn = $form.find('button[type="submit"]'); // 更精确的选择器

        console.log('📤 提交表单:', {
            isReply,
            formAction: form.action
        });

        // 禁用提交按钮
        $submitBtn.prop('disabled', true).text('提交中...');

        const formData = new FormData(form);

        return AjaxManager.post(form.action, formData)
            .done((data) => {
                if (data.status === 'success') {
                    this.handleSubmitSuccess(data, $form, isReply);
                    TemplateManager.showSuccess(data.message || '评论发表成功');
                } else {
                    this.handleSubmitError(data, $form);
                }
            })
            .fail((xhr) => {
                AjaxManager.handleError(xhr, '评论发表失败');
            })
            .always(() => {
                $submitBtn.prop('disabled', false).text('发表评论');
            });
    },

    /**
     * 处理提交成功
     */
    handleSubmitSuccess(data, $form, isReply) {
        const parentId = $form.find('input[id$="comment-parent-id"]').val(); // 更灵活的选择器

        console.log('✅ 表单提交成功:', {
            parentId,
            isReply
        });

        if (parentId && isReply) {
            // 处理回复成功 - 统一添加到一级评论的回复列表中
            const $repliesContainer = $(`#replies-${parentId}`);

            if ($repliesContainer.is(':visible') && $repliesContainer.html().trim() !== '') {
                // 回复列表已展开，直接添加新回复
                $repliesContainer.append(data.html);
                console.log('➕ 新回复已添加到现有列表');
            } else {
                // 回复列表未展开，重新加载回复列表
                CommentLoader.loadReplies(parentId);
                console.log('🔄 重新加载回复列表');
            }

            // 重置回复表单
            this.resetReplyForms();

            // 滚动到新添加的回复（延迟执行，等待DOM更新）
            setTimeout(() => {
                const $newReplies = $repliesContainer.children().last();
                if ($newReplies.length) {
                    $('html, body').animate({
                        scrollTop: $newReplies.offset().top - 100
                    }, 500);
                }
            }, 300);

        } else {
            // 处理主评论成功
            const $commentsList = $('#comments-list');
            $commentsList.prepend(data.html);
            $form[0].reset();
            $form.find('.comment-error-message').remove();

            console.log('➕ 新主评论已添加');

            // 滚动到新评论
            setTimeout(() => {
                const $newComment = $commentsList.children().first();
                $('html, body').animate({
                    scrollTop: $newComment.offset().top - 100
                }, 500);
            }, 100);
        }
    },

    /**
     * 处理提交错误
     */
    handleSubmitError(data, $form) {
        console.error('❌ 表单提交失败:', data);
        TemplateManager.showError(data.message || '提交失败');

        // 显示表单错误
        if (data.errors) {
            $form.find('.comment-error-message').remove();
            for (const fieldName in data.errors) {
                const errorMessages = data.errors[fieldName];
                const $input = $form.find(`[name="${fieldName}"]`);
                if ($input.length) {
                    $input.after(`<div class="comment-error-message">${errorMessages.join('<br>')}</div>`);
                }
            }
        }
    }
};

    // ===== 评论加载器 =====
    const CommentLoader = {
        loadComments(pageNumber = 1, sortBy = 'hot') {
            const $commentsList = $('#comments-list');
            const $loadMoreBtn = $('#load-more-comments');
            const pageId = $commentsList.attr('data-page-id');

            // 显示加载状态
            $loadMoreBtn.hide();
            const $loading = TemplateManager.showLoadingIndicator();

            return AjaxManager.get(`/comments/load/${pageId}/`, {
                page: pageNumber,
                sort: sortBy
            })
            .done((data) => {
                if (data.status === 'success') {
                    // 第一页清空列表
                    if (pageNumber === 1) {
                        $commentsList.empty();
                        this.restoreMainForm();
                    }

                    // 添加评论HTML
                    $commentsList.append(data.html);

                    // 处理空状态
                    this.handleEmptyState(data, pageNumber);

                    // 更新加载更多按钮
                    if (data.has_next) {
                        $loadMoreBtn.data('page', pageNumber + 1).show();
                    } else {
                        $loadMoreBtn.hide();
                    }
                } else {
                    TemplateManager.showError(data.message || '加载评论失败');
                }
            })
            .fail((xhr) => {
                AjaxManager.handleError(xhr, '加载评论失败');
            })
            .always(() => {
                $loading.remove();
            });
        },

        handleEmptyState(data, pageNumber) {
            if (data.total_comments === 0 && pageNumber === 1) {
                const isAuthenticated = data.is_authenticated !== undefined ?
                    data.is_authenticated : AuthManager.isAuthenticated();

                if (!isAuthenticated) {
                    TemplateManager.showLoginPrompt();
                } else {
                    TemplateManager.showNoComments();
                }
            }
        },

        restoreMainForm() {
            const $container = $('#main-comment-form-wrapper');
            const $placement = $('#initial-comment-form-placement');

            if ($container.length && $placement.length) {
                $placement.append($container.show());
                const $form = $container.find('form');
                $form[0].reset();
                $form.find('#comment-parent-id').val('');
                $form.find('#replied-to-user-id').val('');
                $form.find('#reply-to-info').addClass('template-hidden').hide();
                $form.find('.comment-error-message').remove();
            }
        },

        loadReplies(commentId) {
            const $repliesContainer = $(`#replies-${commentId}`);
            const $btn = $(`.show-replies-btn[data-comment-id="${commentId}"]`);

            if ($repliesContainer.html().trim() !== '' &&
                !$repliesContainer.find('.replies-loading-indicator').length) {
                $repliesContainer.slideDown(200);
                return;
            }

            const $loading = TemplateManager.showRepliesLoading($repliesContainer);

            return AjaxManager.get(`/comments/load-replies/${commentId}/`)
                .done((data) => {
                    if (data.status === 'success') {
                        $repliesContainer.html(data.html).slideDown(200);

                        if ($btn.length) {
                            $btn.text(`收起 ${data.reply_count} 条回复`);
                        }
                    } else {
                        TemplateManager.showError(data.message || '加载回复失败');
                    }
                })
                .fail((xhr) => {
                    AjaxManager.handleError(xhr, '加载回复失败');
                })
                .always(() => {
                    $loading.remove();
                });
        }
    };

    // ===== 交互管理器 =====
    const InteractionManager = {
        /**
         * 处理点赞/踩
         */
        handleVote(commentId, reactionType) {
            return AuthManager.requireAuth(() => {
                AjaxManager.post('/comments/react/', {
                    comment_id: commentId,
                    reaction_type: reactionType
                })
                .done((data) => {
                    if (data.status === 'success') {
                        this.updateVoteDisplay(commentId, data);
                        TemplateManager.showSuccess('操作成功');
                    } else {
                        TemplateManager.showError(data.message || '操作失败');
                    }
                })
                .fail((xhr) => {
                    AjaxManager.handleError(xhr, '操作失败');
                });
            });
        },

        /**
         * 更新投票显示
         */
        updateVoteDisplay(commentId, data) {
            const $comment = $(`#comment-${commentId}`);
            $comment.find('.like-count').text(data.like_count);
            $comment.find('.dislike-count').text(data.dislike_count);

            // 更新按钮状态
            $comment.find('.vote-link').removeClass('active');
            if (data.action === 'added') {
                $comment.find(`[data-reaction="${data.reaction_type}"]`).addClass('active');
            }
        },

        /**
         * 编辑评论
         */
        editComment(commentId) {
            return AuthManager.requireAuth(() => {
                const $commentText = $(`#comment-text-${commentId}`);
                const $comment = $commentText.closest('.comment');

                // 获取纯文本内容
                let currentContent = $commentText.clone()
                    .children('.replied-to-user').remove().end()
                    .text().trim();

                // 隐藏操作按钮，显示编辑表单
                $comment.find('.comment-actions-list').hide();

                const $editForm = TemplateManager.createEditForm(commentId, currentContent);
                $commentText.html($editForm);
            });
        },

        /**
         * 保存编辑
         */
        saveEdit(commentId, newContent) {
            if (!newContent.trim()) {
                TemplateManager.showError('评论内容不能为空！');
                return;
            }

            const $saveBtn = $(`.save-edit-btn[data-comment-id="${commentId}"]`);
            $saveBtn.prop('disabled', true).text('保存中...');

            return AjaxManager.post('/comments/edit/', {
                comment_id: commentId,
                content: newContent
            })
            .done((data) => {
                if (data.status === 'success') {
                    const $commentText = $(`#comment-text-${commentId}`);
                    const $comment = $commentText.closest('.comment');

                    // 重新渲染内容
                    const repliedToUserSpan = $commentText.find('.replied-to-user').prop('outerHTML') || '';
                    $commentText.html(repliedToUserSpan + data.content);
                    $comment.find('.comment-actions-list').show();

                    TemplateManager.showSuccess('评论已更新', $comment);
                } else {
                    TemplateManager.showError(data.message || '编辑失败');
                }
            })
            .fail((xhr) => {
                AjaxManager.handleError(xhr, '编辑失败');
            })
            .always(() => {
                $saveBtn.prop('disabled', false).text('保存');
            });
        },

        /**
         * 删除评论
         */
        deleteComment(commentId) {
            return AuthManager.requireAuth(() => {
                const $comment = $(`#comment-${commentId}`);
                const isRootComment = $comment.hasClass('comment') && !$comment.hasClass('nested-comment');

                let confirmMessage = '确定要删除这条评论吗？\n此操作不可撤销。';
                if (isRootComment) {
                    const replyCount = $comment.find('.show-replies-btn').text().match(/\d+/);
                    if (replyCount && parseInt(replyCount[0]) > 0) {
                        confirmMessage = `删除这条一级评论将同时删除其下的所有 ${replyCount[0]} 条回复，确定要继续吗？`;
                    }
                }

                if (!confirm(confirmMessage)) return;

                AjaxManager.post('/comments/delete/', {
                    comment_id: commentId
                })
                .done((data) => {
                    if (data.status === 'success') {
                        this.handleDeleteSuccess(commentId, data, isRootComment);
                        TemplateManager.showSuccess('评论已删除');
                    } else {
                        TemplateManager.showError(data.message || '删除失败');
                    }
                })
                .fail((xhr) => {
                    AjaxManager.handleError(xhr, '删除失败');
                });
            });
        },

        /**
         * 处理删除成功
         */
        handleDeleteSuccess(commentId, data, isRootComment) {
            const $comment = $(`#comment-${commentId}`);

            if (isRootComment && data.deleted_replies) {
                // 删除整个评论项
                $comment.fadeOut(300, function() {
                    $(this).remove();
                });
            } else {
                // 标记为已删除
                const $commentText = $comment.find(`#comment-text-${commentId}`);
                $commentText.html('<em>此评论已被删除</em>');
                $comment.find('.comment-actions-list a, .comment-actions-list button').hide();
                $comment.find('.show-replies-btn').hide();
                $comment.find('.dynamic-reply-form-container').empty();
            }

            // 重置相关的回复表单
            if (FormManager.activeReplyForm) {
                FormManager.resetReplyForms();
            }
        }
    };

    // ===== 事件管理器 =====
    const EventManager = {
        bindEvents() {
            // 登录按钮
            $(document).on('click', '.login-btn, .theme-btn[class*="login"]', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('登录按钮被点击'); // 调试用
                AuthManager.redirectToLogin();
            });

            // 排序按钮
            $(document).on('click', '.sort-btn', function() {
                const $btn = $(this);
                $('.sort-btn').removeClass('active');
                $btn.addClass('active');

                const sortBy = $btn.attr('data-sort');
                $('#load-more-comments').data('page', 1);
                CommentLoader.loadComments(1, sortBy);
            });

            // 加载更多
            $(document).on('click', '#load-more-comments', function() {
                const $btn = $(this);
                const nextPage = $btn.data('page');
                const sortBy = $('.sort-btn.active').attr('data-sort');
                CommentLoader.loadComments(nextPage, sortBy);
            });

            // 展开/折叠回复
            $(document).on('click', '.show-replies-btn', function() {
                const $btn = $(this);
                const commentId = $btn.attr('data-comment-id');
                const $repliesContainer = $(`#replies-${commentId}`);

                if ($repliesContainer.is(':hidden')) {
                    CommentLoader.loadReplies(commentId);
                } else {
                    $repliesContainer.slideUp(200, function() {
                        $repliesContainer.empty();
                    });
                    const match = $btn.text().match(/\d+/);
                    if (match) {
                        $btn.text(`查看全部 ${match[0]} 条回复`);
                    }
                }
            });

            // 表单提交
            $(document).on('submit', '#initial-comment-form-placement form', function(e) {
                e.preventDefault();
                console.log('📤 主评论表单提交');
                FormManager.submitForm(this, false);
            });

            $(document).on('submit', '.active-reply-form form', function(e) {
                e.preventDefault();
                console.log('📤 回复表单提交');
                FormManager.submitForm(this, true);
            });

            // 回复功能
            $(document).on('click', '.reply-btn', function(e) {
                e.preventDefault(); // 阻止默认行为
                e.stopPropagation(); // 阻止事件冒泡

                const $btn = $(this);
                const commentId = $btn.attr('data-comment-id');
                const username = $btn.attr('data-username');
                const userId = $btn.attr('data-user-id');
                const rootCommentId = $btn.attr('data-root-comment-id');

                console.log('🖱️ 回复按钮点击:', {
                    commentId,
                    username,
                    userId,
                    rootCommentId
                });

                AuthManager.requireAuth(() => {
                    FormManager.createReplyForm(commentId, username, userId, rootCommentId);
                });
            });

            // 取消回复
            $(document).on('click', '#cancel-reply', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('❌ 取消回复');
                FormManager.resetReplyForms();
            });

            // 点赞/踩
            $(document).on('click', '.vote-link', function(e) {
                e.preventDefault();
                const $btn = $(this);
                const commentId = $btn.attr('data-comment-id');
                const reactionType = $btn.attr('data-reaction');
                InteractionManager.handleVote(commentId, reactionType);
            });

            // 编辑功能
            $(document).on('click', '.edit-btn', function() {
                const commentId = $(this).data('comment-id');
                InteractionManager.editComment(commentId);
            });

            $(document).on('click', '.save-edit-btn', function() {
                const $btn = $(this);
                const commentId = $btn.data('comment-id');
                const newContent = $btn.closest('.edit-comment-form').find('.edit-textarea').val();
                InteractionManager.saveEdit(commentId, newContent);
            });

            $(document).on('click', '.cancel-edit-btn', function() {
                // 简化处理：直接刷新页面
                location.reload();
            });

            // 删除功能
            $(document).on('click', '.delete-btn', function() {
                const commentId = $(this).attr('data-comment-id');
                InteractionManager.deleteComment(commentId);
            });
        }
    };

    // ===== 主控制器 =====
    const Controller = {
        init() {
            console.log('=== 评论系统初始化 ===');

            if (!$('#comments-section').length) {
                return;
            }

            EventManager.bindEvents();

            const pageId = $('#comments-list').attr('data-page-id');
            if (pageId) {
                CommentLoader.loadComments(1, 'hot');
            }

            console.log('=== 初始化完成 ===');
        }
    };

    return {
        init: Controller.init.bind(Controller),

        // 暴露一些有用的方法供外部调用
        loadComments: CommentLoader.loadComments.bind(CommentLoader),
        isAuthenticated: AuthManager.isAuthenticated.bind(AuthManager)
    };
})();

// 文档就绪时初始化
$(document).ready(function() {
    CommentSystem.init();
});