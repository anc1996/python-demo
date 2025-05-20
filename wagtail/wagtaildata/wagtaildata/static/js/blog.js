// 创建Vue应用来增强博客功能
import Vue from 'vue';
import hljs from 'highlight.js';
import { marked } from 'marked';

// 博客内容渲染组件
Vue.component('blog-content', {
  props: ['content'],
  template: `
    <div class="blog-content">
      <div v-html="renderedContent"></div>
    </div>
  `,
  computed: {
    renderedContent() {
      return this.content;
    }
  },
  mounted() {
    // 代码高亮
    this.$nextTick(() => {
      document.querySelectorAll('pre code').forEach(block => {
        hljs.highlightBlock(block);
      });
    });

    // 数学公式渲染
    if (window.MathJax) {
      window.MathJax.typeset();
    }
  }
});

// Markdown渲染组件
Vue.component('markdown-renderer', {
  props: ['text'],
  template: `
    <div v-html="renderedMarkdown"></div>
  `,
  computed: {
    renderedMarkdown() {
      // 配置marked选项，支持代码高亮
      marked.setOptions({
        highlight: (code, lang) => {
          const language = hljs.getLanguage(lang) ? lang : 'plaintext';
          return hljs.highlight(code, { language }).value;
        },
        langPrefix: 'hljs language-',
        breaks: true,
      });
      
      return this.text ? marked.parse(this.text) : '';
    }
  },
  mounted() {
    // 渲染后的处理
    this.$nextTick(() => {
      // 数学公式渲染
      if (window.MathJax) {
        window.MathJax.typeset();
      }
    });
  }
});

// 代码块组件
Vue.component('code-block', {
  props: ['code', 'language', 'showLineNumbers'],
  template: `
    <div class="code-block">
      <div class="code-header">
        <span class="language-badge">{{ language }}</span>
        <button @click="copyCode" class="copy-btn">复制代码</button>
      </div>
      <pre :class="{'line-numbers': showLineNumbers}"><code :class="'language-' + language" ref="codeBlock">{{ code }}</code></pre>
    </div>
  `,
  methods: {
    copyCode() {
      const code = this.code;
      navigator.clipboard.writeText(code).then(() => {
        // 显示复制成功提示
        this.$emit('copied');
      });
    }
  },
  mounted() {
    // 代码高亮
    this.$nextTick(() => {
      hljs.highlightBlock(this.$refs.codeBlock);
    });
  }
});

// 数学公式组件
Vue.component('math-formula', {
  props: ['formula', 'displayMode'],
  template: `
    <div class="math-formula">
      <div v-if="displayMode" class="tex-math" v-html="'$' + formula + '$'"></div>
      <span v-else class="tex-math-inline" v-html="'\\\\(' + formula + '\\\\)'"></span>
    </div>
  `,
  mounted() {
    // 渲染公式
    this.$nextTick(() => {
      if (window.MathJax) {
        window.MathJax.typeset();
      }
    });
  }
});

// 博客搜索组件
Vue.component('blog-search', {
  data() {
    return {
      query: '',
      isSearching: false,
      results: [],
      noResults: false
    };
  },
  template: `
    <div class="blog-search">
      <div class="search-input-wrapper">
        <input 
          type="text" 
          v-model="query" 
          @input="debounceSearch" 
          placeholder="搜索博客文章..." 
          class="search-input" 
        />
        <button @click="performSearch" class="search-button">
          <span v-if="isSearching">搜索中...</span>
          <span v-else>搜索</span>
        </button>
      </div>
      
      <div v-if="results.length > 0" class="search-results">
        <h3>搜索结果</h3>
        <ul>
          <li v-for="result in results" :key="result.id" class="result-item">
            <a :href="result.url" class="result-link">
              <h4>{{ result.title }}</h4>
              <p v-if="result.intro">{{ result.intro }}</p>
              <span v-if="result.date" class="result-date">{{ formatDate(result.date) }}</span>
            </a>
          </li>
        </ul>
      </div>
      
      <div v-if="noResults && query" class="no-results">
        没有找到匹配 "{{ query }}" 的结果
      </div>
    </div>
  `,
  methods: {
    debounceSearch: function() {
      if (this.debounceTimer) {
        clearTimeout(this.debounceTimer);
      }
      
      this.debounceTimer = setTimeout(() => {
        if (this.query.length >= 2) {
          this.performSearch();
        } else {
          this.results = [];
          this.noResults = false;
        }
      }, 300);
    },
    performSearch: function() {
      if (!this.query || this.query.length < 2) return;
      
      this.isSearching = true;
      this.results = [];
      
      // 调用搜索API
      fetch(`/blog/api/search/?query=${encodeURIComponent(this.query)}`)
        .then(response => response.json())
        .then(data => {
          this.results = data.results;
          this.noResults = data.count === 0;
          this.isSearching = false;
        })
        .catch(error => {
          console.error('搜索出错:', error);
          this.isSearching = false;
        });
    },
    formatDate: function(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    }
  }
});

// 博客目录导航组件
Vue.component('blog-toc', {
  props: ['content'],
  data() {
    return {
      headings: [],
      activeId: ''
    };
  },
  template: `
    <div class="blog-toc" v-if="headings.length > 0">
      <h3 class="toc-title">目录</h3>
      <ul class="toc-list">
        <li v-for="heading in headings" :key="heading.id" :class="[heading.level, { 'active': activeId === heading.id }]">
          <a :href="'#' + heading.id" @click="scrollToHeading(heading.id)">{{ heading.text }}</a>
        </li>
      </ul>
    </div>
  `,
  methods: {
    extractHeadings() {
      const headingElements = document.querySelectorAll('.blog-content h2, .blog-content h3, .blog-content h4');
      this.headings = Array.from(headingElements).map(el => {
        // 确保每个标题都有ID
        if (!el.id) {
          el.id = this.slugify(el.textContent);
        }
        
        return {
          id: el.id,
          text: el.textContent,
          level: el.tagName.toLowerCase()
        };
      });
    },
    slugify(text) {
      return text
        .toString()
        .toLowerCase()
        .trim()
        .replace(/\s+/g, '-')
        .replace(/[^\w\-]+/g, '')
        .replace(/\-\-+/g, '-');
    },
    scrollToHeading(id) {
      const element = document.getElementById(id);
      if (element) {
        window.scrollTo({
          top: element.offsetTop - 20,
          behavior: 'smooth'
        });
        this.activeId = id;
      }
    },
    handleScroll() {
      const headingElements = document.querySelectorAll('.blog-content h2, .blog-content h3, .blog-content h4');
      const fromTop = window.scrollY + 100;
      
      let currentHeading = null;
      
      headingElements.forEach(heading => {
        if (heading.offsetTop <= fromTop) {
          currentHeading = heading;
        }
      });
      
      if (currentHeading && this.activeId !== currentHeading.id) {
        this.activeId = currentHeading.id;
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.extractHeadings();
      window.addEventListener('scroll', this.handleScroll);
    });
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.handleScroll);
  }
});

// 创建Vue实例，将组件挂载到页面
document.addEventListener('DOMContentLoaded', () => {
  // 博客内容页Vue实例
  if (document.getElementById('blog-page-app')) {
    new Vue({
      el: '#blog-page-app',
      data: {
        isCodeCopied: false,
        showToc: true
      },
      methods: {
        handleCodeCopied() {
          this.isCodeCopied = true;
          setTimeout(() => {
            this.isCodeCopied = false;
          }, 2000);
        },
        toggleToc() {
          this.showToc = !this.showToc;
        }
      }
    });
  }
  
  // 博客列表页Vue实例
  if (document.getElementById('blog-list-app')) {
    new Vue({
      el: '#blog-list-app'
    });
  }
  
  // 搜索页Vue实例
  if (document.getElementById('blog-search-app')) {
    new Vue({
      el: '#blog-search-app'
    });
  }
});