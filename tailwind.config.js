module.exports = {
  darkMode: "class",
  content: [
    "./*.html",
    "./!(node_modules)/**/*.html"
  ],
  theme: { extend: {
    colors: { primary:"#1C7E84", background:"#FFFFFF", surface:"#F9F9F9", "on-surface":"#111111", "text-muted":"#3f3f46", "border-subtle":"#E5E5E5", "accent-green":"#1C7E84" },
    borderRadius: { DEFAULT:"0px", lg:"4px", xl:"8px", full:"9999px" },
    spacing: { "section-gap":"160px", "container-max":"1200px" },
    fontFamily: { sans:["Geist","Inter","sans-serif"], mono:["JetBrains Mono","monospace"] }
  }},
  plugins: [ require("@tailwindcss/forms"), require("@tailwindcss/container-queries") ]
}
