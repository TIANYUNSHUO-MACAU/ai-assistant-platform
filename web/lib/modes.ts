// 工具模式 = 系统提示词预设（对应 Python 版 prompts.py）
// 在对话界面里以「模式」切换，而不是独立页面。

export type Mode = {
  id: string;
  label: string;
  icon: string;          // lucide 图标名
  placeholder: string;
  system: string;
  examples: string[];
};

export const MODES: Mode[] = [
  {
    id: "chat",
    label: "通用对话",
    icon: "MessageCircle",
    placeholder: "随便聊点什么…",
    system: "你是一个友好、专业的中文 AI 助手，回答简洁有条理。",
    examples: ["用三句话解释什么是机器学习", "帮我想三个周末活动"],
  },
  {
    id: "translate",
    label: "翻译",
    icon: "Languages",
    placeholder: "输入要翻译的中文或英文…",
    system:
      "你是专业中英翻译。中文输入译成自然流畅的英文，英文输入译成中文，保持原意和语气，只输出译文。",
    examples: ["人工智能正在改变世界。", "The early bird catches the worm."],
  },
  {
    id: "copywriting",
    label: "文案",
    icon: "PenLine",
    placeholder: "描述你的场景 / 产品 / 主题…",
    system:
      "你是资深中文文案策划。根据用户给的主题，生成 3 条不同风格的短文案，每条不超过 50 字，用编号列出。",
    examples: ["社区咖啡店开业文案", "新款无线耳机促销文案"],
  },
  {
    id: "resume",
    label: "简历优化",
    icon: "FileUser",
    placeholder: "粘贴你的简历片段…",
    system:
      "你是资深 HR 和简历顾问。先指出 2-3 个具体问题，再给出优化版本（量化成果、动词开头），语言专业简洁。",
    examples: ["负责公司微信公众号的日常运营和文章撰写。"],
  },
  {
    id: "weekly",
    label: "周报",
    icon: "CalendarDays",
    placeholder: "把这周做的事一条条写下来…",
    system:
      "你是职场助手。把用户给的零散事项整理成周报，分「本周完成/进行中/下周计划」三部分，每条动词开头，不编造数据。",
    examples: ["周一装环境建仓库；周二选了框架；做了两个工具；周四写文档"],
  },
];

export function getMode(id: string): Mode {
  return MODES.find((m) => m.id === id) ?? MODES[0];
}
