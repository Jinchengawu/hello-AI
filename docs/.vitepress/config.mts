import { defineConfig } from 'vitepress'

export default defineConfig({
    lang: 'zh-CN',
    title: 'Hello AI',
    description: '从原理、数据、训练、对齐、评测到部署的大模型全链路工程自学指南',
    base: '/hello-AI/',
    cleanUrls: true,
    lastUpdated: true,
    head: [
      ['meta', { name: 'theme-color', content: '#315cfd' }],
      ['meta', { property: 'og:type', content: 'website' }],
      ['meta', { property: 'og:title', content: 'Hello AI：大模型全链路工程自学指南' }],
      ['meta', { property: 'og:description', content: '用一个贯穿项目，打通大模型数据、训练、对齐、评测、部署与迭代。' }]
    ],
    markdown: {
      lineNumbers: true,
      config(md) {
        const defaultFence = md.renderer.rules.fence!
        md.renderer.rules.fence = (tokens, index, options, env, self) => {
          const token = tokens[index]
          if (token.info.trim() === 'mermaid') {
            return `<MermaidDiagram code="${encodeURIComponent(token.content)}" />`
          }
          return defaultFence(tokens, index, options, env, self)
        }
      }
    },
    vite: {
      build: {
        // Mermaid is loaded only when a diagram is present; its parser is intentionally sizeable.
        chunkSizeWarningLimit: 1200
      }
    },
    themeConfig: {
      logo: '/logo.svg',
      siteTitle: 'Hello AI',
      search: {
        provider: 'local',
        options: {
          translations: {
            button: { buttonText: '搜索文档', buttonAriaLabel: '搜索文档' },
            modal: {
              noResultsText: '没有找到相关内容',
              resetButtonTitle: '清除查询',
              footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' }
            }
          }
        }
      },
      nav: [
        { text: '学习路线', link: '/roadmap/' },
        { text: '开始学习', link: '/guide/01-getting-started' },
        { text: '动手实验', link: '/labs/shoplm-mini' },
        { text: 'GitHub', link: 'https://github.com/Jinchengawu/hello-AI' }
      ],
      sidebar: {
        '/guide/': [
          {
            text: '开始学习',
            items: [
              { text: '第 1 章：学习导览与工程环境', link: '/guide/01-getting-started' },
              { text: '第 2 章：大模型核心原理', link: '/guide/02-llm-fundamentals' },
              { text: '第 3 章：大模型全链路工程', link: '/guide/03-llm-lifecycle' }
            ]
          },
          {
            text: '实践',
            items: [{ text: 'ShopLM Mini：CPU 全链路实验', link: '/labs/shoplm-mini' }]
          },
          {
            text: '项目',
            items: [{ text: '完整课程地图', link: '/roadmap/' }]
          }
        ],
        '/labs/': [
          {
            text: '动手实验',
            items: [{ text: 'ShopLM Mini：CPU 全链路实验', link: '/labs/shoplm-mini' }]
          },
          {
            text: '关联章节',
            items: [{ text: '第 3 章：大模型全链路工程', link: '/guide/03-llm-lifecycle' }]
          }
        ],
        '/roadmap/': [
          {
            text: '学习路线',
            items: [
              { text: '九部分课程地图', link: '/roadmap/' },
              { text: '从第 1 章开始', link: '/guide/01-getting-started' }
            ]
          }
        ]
      },
      outline: { level: [2, 3], label: '本页目录' },
      docFooter: { prev: '上一章', next: '下一章' },
      editLink: {
        pattern: 'https://github.com/Jinchengawu/hello-AI/edit/main/docs/:path',
        text: '在 GitHub 上编辑此页'
      },
      lastUpdated: { text: '最后更新于', formatOptions: { dateStyle: 'medium', timeStyle: 'short' } },
      socialLinks: [{ icon: 'github', link: 'https://github.com/Jinchengawu/hello-AI' }],
      footer: {
        message: '教程内容采用 CC BY-NC-SA 4.0；示例代码采用 Apache-2.0。',
        copyright: 'Copyright © 2026 Jinchengawu and contributors'
      }
    }
  })
