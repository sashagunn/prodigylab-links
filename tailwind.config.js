module.exports = {
  darkMode: "class",
  content: [
    "./index.html","./newdesign.html","./prodigybot/index.html",
    "./en/index.html","./en/prodigybot/index.html",
    "./es/index.html","./es/prodigybot/index.html",
    "./pt/index.html","./pt/prodigybot/index.html",
    "./de/index.html","./de/prodigybot/index.html",
    "./ai-automation/index.html","./ai-chatbot/index.html",
    "./conversion-rate-optimization/index.html","./ecommerce-consulting/index.html",
    "./meta-ads-management/index.html",
    "./shopify-audit/index.html","./shopify-development/index.html","./shopify-redesign/index.html",
    "./website-audit/index.html","./website-development/index.html","./website-redesign/index.html"
  ],
  theme: { extend: {
    colors: { primary:"#1C7E84", background:"#FFFFFF", surface:"#F9F9F9", "on-surface":"#111111", "text-muted":"#3f3f46", "border-subtle":"#E5E5E5", "accent-green":"#1C7E84" },
    borderRadius: { DEFAULT:"0px", lg:"4px", xl:"8px", full:"9999px" },
    spacing: { "section-gap":"160px", "container-max":"1200px" },
    fontFamily: { sans:["Geist","Inter","sans-serif"], mono:["JetBrains Mono","monospace"] }
  }},
  plugins: [ require("@tailwindcss/forms"), require("@tailwindcss/container-queries") ]
}
