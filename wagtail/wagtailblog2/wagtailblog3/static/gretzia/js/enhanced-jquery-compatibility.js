/**
 * 增强版jQuery兼容性修复脚本
 * 解决mCustomScrollbar与现代jQuery版本的兼容性问题
 * 文件路径: static/gretzia/js/enhanced-jquery-compatibility.js
 */

(function($) {
    'use strict';

    console.log('🔧 jQuery兼容性修复脚本启动');

    // 1. 修复jQuery.fn.load方法的参数类型检查问题
    if (typeof $ !== 'undefined' && $.fn && $.fn.load) {
        const originalLoad = $.fn.load;

        $.fn.load = function(url, params, callback) {
            // 增强的参数类型检查
            if (typeof url !== 'string' && url !== null && url !== undefined) {
                // 如果第一个参数不是字符串、null或undefined，说明这是事件绑定调用
                if (typeof url === 'function') {
                    // .load(handler) - 绑定load事件
                    return this.on('load', url);
                } else if (typeof url === 'object' && url.nodeType) {
                    // 处理DOM元素参数的情况
                    return this.on('load', url, params);
                } else {
                    // 其他非字符串情况，尝试转换为事件绑定
                    console.warn('jQuery.load: 非字符串参数被转换为事件绑定', url);
                    return this.on('load', url, params, callback);
                }
            }

            // 如果是正常的AJAX load调用（字符串URL）
            return originalLoad.apply(this, arguments);
        };

        console.log('✅ jQuery.fn.load方法已修复');
    }

    // 2. 为mCustomScrollbar提供安全的初始化环境
    function safeMCustomScrollbarInit() {
        // 检查mCustomScrollbar插件是否可用
        if (!$.fn.mCustomScrollbar) {
            console.warn('⚠️ mCustomScrollbar插件未加载');
            return;
        }

        try {
            // 安全初始化mCustomScrollbar的默认设置
            if ($.mCustomScrollbar && $.mCustomScrollbar.defaults) {
                // 设置更安全的默认配置
                $.mCustomScrollbar.defaults = $.extend($.mCustomScrollbar.defaults, {
                    scrollInertia: 300,
                    mouseWheel: {
                        enable: true,
                        scrollAmount: "auto",
                        axis: "y",
                        preventDefault: false
                    },
                    advanced: {
                        updateOnContentResize: true,
                        updateOnImageLoad: "auto",
                        autoUpdateTimeout: 100
                    }
                });
            }

            console.log('✅ mCustomScrollbar默认配置已优化');
        } catch (error) {
            console.error('❌ mCustomScrollbar配置失败:', error);
        }
    }

    // 3. 错误捕获和处理机制
    function setupErrorHandling() {
        // 捕获mCustomScrollbar相关的错误
        const originalError = window.onerror;
        window.onerror = function(message, source, lineno, colno, error) {
            if (message && message.includes('indexOf') && source && source.includes('mCustomScrollbar')) {
                console.warn('🛡️ 已拦截mCustomScrollbar兼容性错误:', message);
                return true; // 阻止错误继续传播
            }

            // 其他错误继续正常处理
            if (originalError) {
                return originalError.apply(this, arguments);
            }
            return false;
        };

        console.log('🛡️ 错误处理机制已激活');
    }

    // 4. 延迟初始化滚动条，避免冲突
    function initCustomScrollbars() {
        setTimeout(function() {
            try {
                // 只在必要时初始化自定义滚动条
                const $scrollableElements = $('.content-wrapper, .blog-content-area');

                if ($scrollableElements.length && $.fn.mCustomScrollbar) {
                    $scrollableElements.each(function() {
                        const $element = $(this);

                        // 检查元素是否需要滚动条
                        if ($element[0].scrollHeight > $element.height() ||
                            $element[0].scrollWidth > $element.width()) {

                            // 检查是否已经初始化
                            if (!$element.hasClass('mCS_destroyed') &&
                                !$element.find('.mCSB_container').length) {

                                try {
                                    $element.mCustomScrollbar({
                                        theme: "minimal-dark",
                                        scrollInertia: 300,
                                        mouseWheel: {
                                            enable: true,
                                            preventDefault: false
                                        },
                                        advanced: {
                                            updateOnContentResize: true,
                                            autoUpdateTimeout: 60
                                        }
                                    });

                                    console.log('✅ 自定义滚动条初始化成功');
                                } catch (initError) {
                                    console.warn('⚠️ 滚动条初始化失败:', initError);
                                }
                            }
                        }
                    });
                }
            } catch (error) {
                console.warn('⚠️ 滚动条整体初始化过程出错:', error);
            }
        }, 800); // 延迟800ms确保DOM完全就绪
    }

    // 5. 提供安全的滚动条销毁方法
    window.safeDestroyScrollbars = function() {
        try {
            if ($.fn.mCustomScrollbar) {
                $('.mCustomScrollbar').each(function() {
                    try {
                        $(this).mCustomScrollbar('destroy');
                    } catch (destroyError) {
                        console.warn('单个滚动条销毁失败:', destroyError);
                    }
                });
                console.log('🗑️ 滚动条安全销毁完成');
            }
        } catch (error) {
            console.warn('⚠️ 滚动条销毁过程出错:', error);
        }
    };

    // 6. 页面可见性API优化
    function setupVisibilityOptimization() {
        let isPageVisible = !document.hidden;

        document.addEventListener('visibilitychange', function() {
            isPageVisible = !document.hidden;

            if (isPageVisible) {
                // 页面变为可见时，重新检查滚动条状态
                setTimeout(function() {
                    if ($.fn.mCustomScrollbar) {
                        $('.mCustomScrollbar').mCustomScrollbar('update');
                    }
                }, 100);
            }
        });

        console.log('👁️ 页面可见性优化已激活');
    }

    // 7. DOM就绪时执行初始化
    $(document).ready(function() {
        setupErrorHandling();
        safeMCustomScrollbarInit();
        setupVisibilityOptimization();
        initCustomScrollbars();

        console.log('🎯 jQuery兼容性修复完成');
    });

    // 8. 页面卸载前清理
    $(window).on('beforeunload', function() {
        window.safeDestroyScrollbars();
    });

    // 9. 调试工具（仅在开发环境使用）
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        window.debugScrollbars = function() {
            console.log('🔍 滚动条调试信息:');
            $('.mCustomScrollbar').each(function(index) {
                const $el = $(this);
                console.log(`滚动条 ${index + 1}:`, {
                    element: $el[0],
                    hasPlugin: $el.data('mCS') !== undefined,
                    scrollHeight: $el[0].scrollHeight,
                    clientHeight: $el[0].clientHeight,
                    needsScrollbar: $el[0].scrollHeight > $el[0].clientHeight
                });
            });
        };
    }

})(jQuery);